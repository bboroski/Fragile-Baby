#!/usr/bin/env python3
"""Validate Elbrus target profiles and evidence-gated qualification levels.

The validator checks declarations and referenced evidence hashes. It does not
invoke a compiler, inspect a binary, emulate a CPU, or prove hardware support.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

MAX_DOCUMENT_BYTES = 262_144
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_LEVELS = ("profile_only", "toolchain_detected", "cross_compiled", "emulated", "hardware_validated")
_EVIDENCE_KINDS = {"toolchain", "build", "emulator", "hardware", "test", "abi"}
_REQUIRED_EVIDENCE = {
    "profile_only": set(),
    "toolchain_detected": {"toolchain"},
    "cross_compiled": {"toolchain", "build"},
    "emulated": {"toolchain", "build", "emulator", "test"},
    "hardware_validated": {"toolchain", "build", "hardware", "test"},
}


class ProfileError(ValueError):
    """Raised when a target profile or its qualification evidence is invalid."""


def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ProfileError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _object(value: Any, keys: set[str], field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ProfileError(f"{field} must be an object")
    extra, missing = sorted(set(value) - keys), sorted(keys - set(value))
    if extra:
        raise ProfileError(f"{field} has unknown fields: {', '.join(extra)}")
    if missing:
        raise ProfileError(f"{field} is missing fields: {', '.join(missing)}")
    return value


def _text(value: Any, field: str, *, nullable: bool = False, limit: int = 256) -> str | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ProfileError(f"{field} must be a non-empty string of at most {limit} characters")
    return value.strip()


def _optional_text(value: Any, field: str, limit: int) -> str | None:
    return _text(value, field, nullable=True, limit=limit)


def _canonical_digest(document: dict[str, Any]) -> str:
    encoded = json.dumps(
        document, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_profile(document: Any) -> dict[str, Any]:
    root_keys = {"schema_version", "target_id", "architecture", "variant",
                 "target", "toolchain", "abi", "features", "qualification"}
    root = _object(document, root_keys, "profile")
    if root["schema_version"] != "fragile-baby.target-profile.v1":
        raise ProfileError("unsupported target profile schema_version")
    target_id = _text(root["target_id"], "target_id", limit=128)
    if root["architecture"] != "elbrus":
        raise ProfileError("architecture must be 'elbrus' for this qualification profile")
    variant = _text(root["variant"], "variant", limit=128)

    target = _object(root["target"], {"cpu_model", "board"}, "target")
    cpu_model = _optional_text(target["cpu_model"], "target.cpu_model", 128)
    board = _optional_text(target["board"], "target.board", 128)

    toolchain = _object(root["toolchain"],
                        {"compiler", "version", "target_triple", "sysroot"}, "toolchain")
    compiler = _optional_text(toolchain["compiler"], "toolchain.compiler", 256)
    version = _optional_text(toolchain["version"], "toolchain.version", 128)
    triple = _optional_text(toolchain["target_triple"], "toolchain.target_triple", 256)
    sysroot = _optional_text(toolchain["sysroot"], "toolchain.sysroot", 1024)

    abi = _object(root["abi"],
                  {"pointer_width_bits", "endianness", "calling_convention",
                   "stack_alignment_bytes"}, "abi")
    pointer_width = abi["pointer_width_bits"]
    if pointer_width is not None and (
        type(pointer_width) is not int or not 16 <= pointer_width <= 128
        or pointer_width % 8 != 0
    ):
        raise ProfileError("abi.pointer_width_bits must be null or a byte-aligned integer from 16 to 128")
    endianness = abi["endianness"]
    if endianness is not None and endianness not in {"little", "big"}:
        raise ProfileError("abi.endianness must be null, little, or big")
    calling = _optional_text(abi["calling_convention"], "abi.calling_convention", 256)
    alignment = abi["stack_alignment_bytes"]
    if alignment is not None and (
        type(alignment) is not int or not 1 <= alignment <= 4096
        or alignment & (alignment - 1)
    ):
        raise ProfileError("abi.stack_alignment_bytes must be null or a power of two from 1 to 4096")

    if not isinstance(root["features"], list) or len(root["features"]) > 128:
        raise ProfileError("features must be an array of at most 128 strings")
    features = [_text(item, f"features[{index}]", limit=128)
                for index, item in enumerate(root["features"])]
    if len(set(features)) != len(features):
        raise ProfileError("features contains duplicates")

    qualification = _object(root["qualification"], {"level", "evidence"}, "qualification")
    level = qualification["level"]
    if not isinstance(level, str) or level not in _LEVELS:
        raise ProfileError(f"qualification.level must be one of: {', '.join(_LEVELS)}")
    evidence = qualification["evidence"]
    if not isinstance(evidence, list) or len(evidence) > 128:
        raise ProfileError("qualification.evidence must be an array of at most 128 records")

    evidence_kinds: set[str] = set()
    evidence_refs: set[str] = set()
    for index, raw in enumerate(evidence):
        item = _object(raw, {"kind", "ref", "sha256"}, f"qualification.evidence[{index}]")
        kind = item["kind"]
        if not isinstance(kind, str) or kind not in _EVIDENCE_KINDS:
            raise ProfileError(f"qualification.evidence[{index}].kind is not recognized")
        reference = _text(item["ref"], f"qualification.evidence[{index}].ref", limit=1024)
        digest = item["sha256"]
        if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
            raise ProfileError(f"qualification.evidence[{index}].sha256 must be lowercase SHA-256")
        if reference in evidence_refs:
            raise ProfileError("qualification.evidence contains duplicate references")
        evidence_refs.add(reference)
        evidence_kinds.add(kind)

    required = _REQUIRED_EVIDENCE[level]
    missing_evidence = sorted(required - evidence_kinds)
    if missing_evidence:
        raise ProfileError(
            f"qualification level '{level}' requires evidence kinds: {', '.join(missing_evidence)}"
        )

    if level != "profile_only":
        if any(value is None for value in (compiler, version, triple, pointer_width,
                                           endianness, calling, alignment)):
            raise ProfileError("toolchain and ABI fields must be complete above profile_only")
    if level == "hardware_validated" and (cpu_model is None or board is None):
        raise ProfileError("hardware_validated requires explicit target.cpu_model and target.board")

    return {
        "target_id": target_id,
        "architecture": "elbrus",
        "variant": variant,
        "qualification_level": level,
        "evidence_count": len(evidence),
        "evidence_kinds": sorted(evidence_kinds),
        "toolchain_configured": all(value is not None for value in (compiler, version, triple)),
        "abi_configured": all(value is not None for value in (
            pointer_width, endianness, calling, alignment
        )),
        "profile_sha256": _canonical_digest(root),
        "support_claim": "not_established" if level == "profile_only" else level,
    }


def _fixture(level: str = "profile_only") -> dict[str, Any]:
    profile: dict[str, Any] = {
        "schema_version": "fragile-baby.target-profile.v1",
        "target_id": "elbrus-qualification-example",
        "architecture": "elbrus",
        "variant": "not-selected",
        "target": {"cpu_model": None, "board": None},
        "toolchain": {
            "compiler": None, "version": None, "target_triple": None, "sysroot": None
        },
        "abi": {
            "pointer_width_bits": None, "endianness": None,
            "calling_convention": None, "stack_alignment_bytes": None,
        },
        "features": [],
        "qualification": {"level": level, "evidence": []},
    }
    if level != "profile_only":
        profile["toolchain"].update({
            "compiler": "compiler-name", "version": "toolchain-version",
            "target_triple": "target-triple-from-vendor", "sysroot": "sysroot/path",
        })
        profile["abi"].update({
            "pointer_width_bits": 64, "endianness": "little",
            "calling_convention": "documented-abi-name", "stack_alignment_bytes": 16,
        })
    needed = _REQUIRED_EVIDENCE[level]
    for index, kind in enumerate(sorted(needed)):
        profile["qualification"]["evidence"].append({
            "kind": kind, "ref": f"evidence/{kind}-{index}.json",
            "sha256": hashlib.sha256(kind.encode("ascii")).hexdigest(),
        })
    if level == "hardware_validated":
        profile["target"].update({"cpu_model": "model-from-device", "board": "board-revision-from-device"})
    return profile


def self_test() -> int:
    report = validate_profile(_fixture())
    assert report["support_claim"] == "not_established"
    for level in _LEVELS:
        validate_profile(_fixture(level))
    incomplete = _fixture("cross_compiled")
    incomplete["qualification"]["evidence"] = [
        item for item in incomplete["qualification"]["evidence"] if item["kind"] != "build"
    ]
    try:
        validate_profile(incomplete)
    except ProfileError:
        pass
    else:
        raise AssertionError("cross-compiled profile without build evidence was accepted")
    bad_abi = _fixture("toolchain_detected")
    bad_abi["abi"]["stack_alignment_bytes"] = 24
    try:
        validate_profile(bad_abi)
    except ProfileError:
        pass
    else:
        raise AssertionError("non-power-of-two ABI alignment was accepted")
    print("Fragile-Baby profile self-test: PASS (five qualification levels + rejection cases)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Fragile-Baby target qualification profiles")
    parser.add_argument("profile", nargs="?", help="target profile JSON path")
    parser.add_argument("--self-test", action="store_true", help="run offline validator checks")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.profile:
        parser.error("profile is required unless --self-test is used")
    try:
        with Path(args.profile).open("rb") as handle:
            raw = handle.read(MAX_DOCUMENT_BYTES + 1)
        if len(raw) > MAX_DOCUMENT_BYTES:
            raise ProfileError(f"profile exceeds the {MAX_DOCUMENT_BYTES}-byte limit")
        try:
            document = json.loads(raw.decode("utf-8"), object_pairs_hook=_no_duplicate_keys)
        except UnicodeDecodeError as exc:
            raise ProfileError("profile must be UTF-8") from exc
        except json.JSONDecodeError as exc:
            raise ProfileError(
                f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
            ) from exc
        print(json.dumps(validate_profile(document), ensure_ascii=False, indent=2, sort_keys=True))
        print("Note: profile validation is not compiler, emulator or hardware qualification.")
        return 0
    except (OSError, ProfileError) as exc:
        print(f"target-profile: error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
