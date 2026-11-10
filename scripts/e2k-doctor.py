#!/usr/bin/env python3
"""Verify that the selected C compiler actually targets Elbrus e2k."""
from __future__ import annotations

import argparse
import os
import pathlib
import shutil
import subprocess
import sys


def resolve_compiler(value: str) -> str | None:
    candidate = pathlib.Path(value)
    if candidate.exists():
        return str(candidate.resolve())
    return shutil.which(value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--compiler",
        default=os.environ.get("E2K_CC", "lcc"),
        help="MCST LCC executable (default: E2K_CC or lcc)",
    )
    args = parser.parse_args()

    compiler = resolve_compiler(args.compiler)
    if compiler is None:
        print(f"ERROR: compiler not found: {args.compiler}", file=sys.stderr)
        print("Install the MCST toolchain or set E2K_CC to its compiler path.", file=sys.stderr)
        return 2

    command = [compiler, "-dM", "-E", "-x", "c", "-"]
    try:
        result = subprocess.run(
            command,
            input="\n",
            text=True,
            capture_output=True,
            check=False,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"ERROR: cannot query compiler macros: {exc}", file=sys.stderr)
        return 2

    if result.returncode != 0:
        print("ERROR: compiler rejected the predefined-macro probe.", file=sys.stderr)
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        return 2

    macros = {}
    for line in result.stdout.splitlines():
        parts = line.split(maxsplit=2)
        if len(parts) >= 2 and parts[0] == "#define":
            macros[parts[1]] = parts[2] if len(parts) == 3 else ""

    if "__e2k__" not in macros:
        print("ERROR: selected compiler does not define __e2k__.", file=sys.stderr)
        print("Refusing to classify this compiler as an Elbrus target.", file=sys.stderr)
        return 3

    print(f"Compiler: {compiler}")
    print("Target: Elbrus e2k (__e2k__ confirmed)")
    print(f"LCC version macro: {macros.get('__LCC__', 'not exposed')}")
    print(f"GCC compatibility macro: {macros.get('__GNUC__', 'not exposed')}")
    qemu = shutil.which("qemu-e2k")
    print(f"qemu-e2k: {qemu if qemu else 'not found (optional)'}")
    print("Result: compiler target macro verified; sysroot, linker, runtime and hardware remain separate checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
