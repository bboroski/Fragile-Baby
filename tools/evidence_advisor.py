"""Offline evidence-matrix advisor for the Fragile-Baby E2K workstream.

This tool checks declared evidence coverage. It does not probe hardware, infer
CPU identities, validate toolchains, or certify a physical target.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

STAGES = ("host", "cross-build", "emulator", "physical-target")
STATUSES = {"not-tested", "passed", "failed", "blocked", "unknown"}
MATURITY = {
    "architecture-proposal": 0,
    "host-observed": 1,
    "cross-build-observed": 2,
    "emulator-observed": 3,
    "hardware-qualified": 4,
}


def analyze_matrix(payload: Any) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(payload, dict):
        return {"valid": False, "errors": ["matrix must be a JSON object"],
                "warnings": [], "coverage_percent": 0, "passed_stages": [],
                "next_stage": "host", "next_action": "provide a valid evidence matrix"}

    if payload.get("schema_version") != "fragile-baby.e2k-evidence.v1":
        errors.append("unsupported or missing schema_version")
    if payload.get("architecture") != "E2K":
        errors.append("architecture must be E2K")
    maturity = payload.get("maturity")
    if maturity not in MATURITY:
        errors.append("maturity must be one of: " + ", ".join(MATURITY))
        maturity_rank = 0
    else:
        maturity_rank = MATURITY[maturity]

    identity = payload.get("target_identity")
    if not isinstance(identity, dict):
        errors.append("target_identity must be an object")
        identity = {}
    identity_fields = ("cpu_model", "stepping", "board_revision", "toolchain")
    for field in identity_fields:
        if field not in identity or identity[field] is not None and not isinstance(identity[field], str):
            errors.append(f"target_identity.{field} must be a string or null")

    raw_stages = payload.get("stages")
    if not isinstance(raw_stages, list) or not 1 <= len(raw_stages) <= 8:
        errors.append("stages must be an array containing 1..8 entries")
        raw_stages = []

    by_name: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(raw_stages):
        if not isinstance(item, dict):
            errors.append(f"stages[{index}] must be an object")
            continue
        name = item.get("stage")
        status = item.get("status")
        evidence = item.get("evidence")
        if name not in STAGES:
            errors.append(f"stages[{index}].stage is unsupported")
            continue
        if name in by_name:
            errors.append(f"duplicate stage: {name}")
            continue
        if status not in STATUSES:
            errors.append(f"stages[{index}].status is unsupported")
        if not isinstance(evidence, list) or any(not isinstance(entry, str) or len(entry) > 512 for entry in evidence):
            errors.append(f"stages[{index}].evidence must be an array of strings up to 512 characters")
            evidence = []
        fingerprint = item.get("toolchain_fingerprint")
        if fingerprint is not None and not isinstance(fingerprint, str):
            errors.append(f"stages[{index}].toolchain_fingerprint must be a string or null")
        by_name[name] = {"status": status, "evidence": evidence, "toolchain_fingerprint": fingerprint}

    passed: list[str] = []
    first_unfinished: str | None = None
    prefix_open = True
    for name in STAGES:
        item = by_name.get(name)
        if item is None:
            if first_unfinished is None:
                first_unfinished = name
            prefix_open = False
            continue
        if item["status"] == "passed" and prefix_open:
            passed.append(name)
        else:
            prefix_open = False
            if first_unfinished is None:
                first_unfinished = name

    coverage = round(len(passed) / len(STAGES) * 100)
    supported_rank = len(passed)
    maturity_consistent = maturity_rank <= supported_rank
    if not maturity_consistent:
        warnings.append(
            f"declared maturity '{maturity}' exceeds the sequential evidence prefix "
            f"({supported_rank}/{len(STAGES)} stages passed)"
        )

    for name in ("cross-build", "emulator"):
        item = by_name.get(name)
        if item and item["status"] == "passed" and not item["toolchain_fingerprint"]:
            warnings.append(f"{name} passed without a toolchain_fingerprint")
    physical = by_name.get("physical-target")
    if physical and physical["status"] == "passed":
        missing_identity = [field for field in identity_fields if not identity.get(field)]
        if missing_identity:
            warnings.append("physical-target passed but target identity is incomplete: " + ", ".join(missing_identity))
        if not physical["evidence"]:
            warnings.append("physical-target passed without traceable evidence references")

    if first_unfinished is None:
        next_action = "request independent review of traceable physical-target evidence before promoting maturity"
        next_stage = None
    else:
        stage = first_unfinished
        item = by_name.get(stage)
        status = item["status"] if item else "not-tested"
        if status == "failed":
            next_action = f"investigate the {stage} failure, attach a reproducible trace, then rerun that stage"
        elif status == "blocked":
            next_action = f"resolve the prerequisite blocking {stage}, record the blocker, then rerun"
        elif status == "unknown":
            next_action = f"collect sufficient {stage} evidence; unknown is not a pass or a failure"
        else:
            next_action = f"run the {stage} qualification stage and attach traceable evidence"
        next_stage = stage

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "coverage_percent": coverage,
        "coverage_semantics": "sequential stage coverage; not probability or confidence",
        "passed_stages": passed,
        "next_stage": next_stage,
        "next_action": next_action,
        "declared_maturity": maturity,
        "maturity_consistent": maturity_consistent,
        "target_identity_complete": all(bool(identity.get(field)) for field in identity_fields),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect E2K evidence coverage and next qualification step.")
    parser.add_argument("matrix", nargs="?", type=Path,
                        default=Path("docs/qualification/e2k-evidence-matrix.example.json"))
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        payload = json.loads(args.matrix.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"evidence-advisor: {exc}")
        return 2
    report = analyze_matrix(payload)
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("Fragile-Baby / E2K qualification evidence")
        print(f"Validity           : {'PASS' if report['valid'] else 'FAIL'}")
        print(f"Sequential coverage: {report['coverage_percent']}% (not confidence)")
        print(f"Passed stages      : {', '.join(report['passed_stages']) or 'none'}")
        print(f"Next stage         : {report['next_stage'] or 'independent review'}")
        print(f"Next action        : {report['next_action']}")
        for warning in report["warnings"]:
            print(f"WARNING: {warning}")
        for error in report["errors"]:
            print(f"ERROR: {error}")
    return 0 if report["valid"] and report["maturity_consistent"] and not report["warnings"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
