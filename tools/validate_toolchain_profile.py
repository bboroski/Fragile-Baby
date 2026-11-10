#!/usr/bin/env python3
"""Validate an Elbrus/E2K toolchain profile with Python's standard library."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_TOOLCHAIN_FIELDS = (
    "compiler", "compiler_version", "target_triple", "sysroot", "linker"
)
VALID_STATUSES = {"planned", "unverified", "host-validated", "target-validated"}


def validate_profile(profile: dict[str, Any]) -> None:
    required = {"schema_version", "profile_id", "architecture", "toolchain", "status", "evidence"}
    missing = required - profile.keys()
    if missing:
        raise ValueError(f"missing profile fields: {', '.join(sorted(missing))}")
    if profile["schema_version"] != 1:
        raise ValueError("unsupported schema_version")
    if not isinstance(profile["profile_id"], str) or not profile["profile_id"].strip():
        raise ValueError("profile_id must be a non-empty string")

    architecture = profile["architecture"]
    if not isinstance(architecture, dict) or architecture.get("family") != "e2k":
        raise ValueError("architecture.family must be e2k")
    if architecture.get("word_bits") not in (32, 64):
        raise ValueError("architecture.word_bits must be 32 or 64")
    if architecture.get("endianness") not in ("unknown", "little", "big"):
        raise ValueError("architecture.endianness is invalid")
    if not isinstance(architecture.get("abi"), str) or not architecture["abi"].strip():
        raise ValueError("architecture.abi must be non-empty")

    toolchain = profile["toolchain"]
    if not isinstance(toolchain, dict):
        raise ValueError("toolchain must be an object")
    for field in REQUIRED_TOOLCHAIN_FIELDS:
        if not isinstance(toolchain.get(field), str) or not toolchain[field].strip():
            raise ValueError(f"toolchain.{field} must be non-empty")

    status = profile["status"]
    if status not in VALID_STATUSES:
        raise ValueError(f"unsupported status: {status!r}")
    evidence = profile["evidence"]
    if not isinstance(evidence, list):
        raise ValueError("evidence must be an array")
    for index, item in enumerate(evidence):
        if not isinstance(item, dict) or not all(
            isinstance(item.get(key), str) and item[key].strip()
            for key in ("kind", "reference", "result")
        ):
            raise ValueError(f"evidence[{index}] needs kind, reference and result")
    if status == "target-validated":
        if not evidence:
            raise ValueError("target-validated requires recorded evidence")
        if any(toolchain[field].strip().lower() == "unknown" for field in REQUIRED_TOOLCHAIN_FIELDS):
            raise ValueError("target-validated cannot use unknown toolchain values")
        if not any(item["kind"] == "hardware" for item in evidence):
            raise ValueError("target-validated requires at least one hardware evidence record")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path)
    args = parser.parse_args()
    with args.profile.open("r", encoding="utf-8") as stream:
        profile = json.load(stream)
    validate_profile(profile)
    print(f"Valid profile: {profile['profile_id']} ({profile['status']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
