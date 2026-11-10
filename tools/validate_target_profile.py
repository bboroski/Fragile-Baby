#!/usr/bin/env python3
"""Validate configurable Elbrus target metadata and compose safe compiler argv."""
from __future__ import annotations

import argparse
import json
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Any

CAPABILITY_STATES = {"unknown", "declared", "verified"}
ALLOWED_POINTER_WIDTHS = {None, 32, 64, 128}


def validate_profile(document: Any, *, require_toolchain: bool = False) -> list[str]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["profile root must be an object"]
    if document.get("schema_version") != "fragile-baby.target-profile.v1":
        errors.append("unsupported schema_version")
    if document.get("architecture") != "elbrus":
        errors.append("architecture must be 'elbrus'")
    if not isinstance(document.get("profile_id"), str) or not document["profile_id"].strip():
        errors.append("profile_id must be non-empty")
    compiler = (document.get("toolchain") or {}).get("compiler")
    target = document.get("target_triple")
    if require_toolchain:
        if not isinstance(compiler, str) or not compiler.strip():
            errors.append("toolchain.compiler must be configured")
        if not isinstance(target, str) or not target.strip():
            errors.append("target_triple must be configured")
    elif compiler is not None and (not isinstance(compiler, str) or not compiler.strip()):
        errors.append("toolchain.compiler must be null or a non-empty command")
    toolchain = document.get("toolchain")
    if not isinstance(toolchain, dict):
        errors.append("toolchain must be an object")
    else:
        flags = toolchain.get("flags")
        if not isinstance(flags, list) or any(
            not isinstance(flag, str) or not flag.strip() for flag in flags
        ):
            errors.append("toolchain.flags must be an array of non-empty strings")
        elif len(set(flags)) != len(flags):
            errors.append("toolchain.flags must not contain duplicates")
        template = toolchain.get("compile_template")
        if not isinstance(template, list) or any(
            not isinstance(item, str) or not item for item in template
        ):
            errors.append("toolchain.compile_template must be a string array")
        else:
            for placeholder in ("{compiler}", "{source}", "{output}"):
                if template.count(placeholder) != 1:
                    errors.append(f"compile_template must contain {placeholder} exactly once")
            if template.count("{flags}") > 1:
                errors.append("compile_template may contain {flags} at most once")

    abi = document.get("abi")
    if not isinstance(abi, dict):
        errors.append("abi must be an object")
    else:
        if abi.get("pointer_bits") not in ALLOWED_POINTER_WIDTHS:
            errors.append("abi.pointer_bits must be null, 32, 64 or 128")
        if abi.get("endianness") not in {"unknown", "little", "big"}:
            errors.append("abi.endianness is invalid")
        if not isinstance(abi.get("calling_convention"), str) or not abi["calling_convention"].strip():
            errors.append("abi.calling_convention must be non-empty")

    capabilities = document.get("capabilities")
    if not isinstance(capabilities, dict) or not capabilities:
        errors.append("capabilities must be a non-empty object")
    else:
        for key, state in capabilities.items():
            if not isinstance(key, str) or not key.strip() or state not in CAPABILITY_STATES:
                errors.append(f"capability {key!r} must use unknown/declared/verified status")

    verification = document.get("verification")
    if not isinstance(verification, dict):
        errors.append("verification must be an object")
    else:
        for key in ("toolchain_probe", "cross_compile", "emulator", "hardware"):
            if not isinstance(verification.get(key), bool):
                errors.append(f"verification.{key} must be boolean")
        if verification.get("hardware") and not verification.get("cross_compile"):
            errors.append("hardware verification requires a recorded cross_compile result")
    return errors


def build_compile_argv(
    document: dict[str, Any], source: str, output: str
) -> list[str]:
    """Build argv from the profile's explicit template; never invokes a shell."""
    errors = validate_profile(document, require_toolchain=True)
    if errors:
        raise ValueError("; ".join(errors))
    toolchain = document["toolchain"]
    compiler = toolchain["compiler"]
    compiler_argv = shlex.split(compiler)
    if not compiler_argv:
        raise ValueError("compiler command is empty")
    template = toolchain["compile_template"]
    flags = toolchain["flags"]
    result: list[str] = []
    for token in template:
        if token == "{compiler}":
            result.extend(compiler_argv)
        elif token == "{flags}":
            result.extend(flags)
        elif token == "{source}":
            result.append(source)
        elif token == "{output}":
            result.append(output)
        else:
            result.append(token)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        default=str(Path(__file__).resolve().parents[1] / "profiles" / "elbrus-reference.json"),
    )
    parser.add_argument("--require-toolchain", action="store_true")
    parser.add_argument("--source")
    parser.add_argument("--output")
    parser.add_argument("--run", action="store_true", help="run the configured compiler command")
    args = parser.parse_args()

    try:
        document = json.loads(Path(args.profile).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2

    errors = validate_profile(document, require_toolchain=args.require_toolchain or args.run)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    if not args.run and not (args.source or args.output):
        print("Elbrus target profile: VALID (toolchain and hardware not verified)")
        return 0
    if not args.source or not args.output:
        print("ERROR: --source and --output are required together")
        return 2

    try:
        argv = build_compile_argv(document, args.source, args.output)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    if not args.run:
        print(json.dumps(argv, ensure_ascii=False))
        return 0
    compiler_path = shutil.which(argv[0])
    if compiler_path is None:
        print(f"ERROR: compiler executable not found: {argv[0]}")
        return 2
    argv[0] = compiler_path
    return subprocess.run(argv, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
