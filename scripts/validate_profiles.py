#!/usr/bin/env python3
"""Validate Fragile-Baby's checked-in E2K processor profile catalog."""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main() -> int:
    profile_path = ROOT / "profiles" / "elbrus-processors.json"
    try:
        payload = json.loads(profile_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Invalid processor profile catalog: {exc}", file=sys.stderr)
        return 1

    if payload.get("schema_version") != 1 or payload.get("architecture_family") != "e2k":
        print("Unsupported processor profile schema or architecture family.", file=sys.stderr)
        return 1

    generations = payload.get("generations")
    if not isinstance(generations, list):
        print("The generations field must be an array.", file=sys.stderr)
        return 1

    expected = [f"e2k-v{number}" for number in range(1, 8)]
    actual = [entry.get("id") for entry in generations]
    if actual != expected:
        print(f"Expected ordered generations {expected}, got {actual}.", file=sys.stderr)
        return 1

    for number, entry in enumerate(generations, start=1):
        if entry.get("generation") != number or not entry.get("processors"):
            print(f"Invalid generation record: {entry!r}", file=sys.stderr)
            return 1

    policy = payload.get("policy", {})
    if policy.get("infer_generation_from_model_string") is not False:
        print("Generation inference from marketing strings must remain disabled.", file=sys.stderr)
        return 1
    if policy.get("require_exact_toolchain_and_os_validation") is not True:
        print("Exact toolchain and OS validation must remain required.", file=sys.stderr)
        return 1

    print("Elbrus processor profile catalog is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
