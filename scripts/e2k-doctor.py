#!/usr/bin/env python3
"""Verify that the selected C compiler actually targets Elbrus e2k."""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile


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

    probe_source = """#ifndef __e2k__
#error Selected compiler does not target Elbrus e2k
#endif
#ifdef __LCC__
FB_LCC_VERSION __LCC__
#else
FB_LCC_VERSION unavailable
#endif
"""
    try:
        with tempfile.TemporaryDirectory(prefix="fragile-baby-e2k-") as directory:
            source_path = pathlib.Path(directory) / "target_probe.c"
            source_path.write_text(probe_source, encoding="utf-8")
            result = subprocess.run(
                [compiler, "-E", str(source_path)],
                text=True,
                capture_output=True,
                check=False,
                timeout=20,
            )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"ERROR: cannot query compiler preprocessor: {exc}", file=sys.stderr)
        return 2

    if result.returncode != 0:
        print("ERROR: compiler rejected the E2K preprocessor probe.", file=sys.stderr)
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        return 2

    if re.search(r"^\s*FB_LCC_VERSION\s+", result.stdout, re.MULTILINE) is None:
        print("ERROR: compiler output did not contain the target probe marker.", file=sys.stderr)
        return 2

    version_match = re.search(
        r"^\s*FB_LCC_VERSION\s+(\d+)\s*$", result.stdout, re.MULTILINE
    )
    lcc_version = version_match.group(1) if version_match else "not exposed"

    print(f"Compiler: {compiler}")
    print("Target: Elbrus e2k (__e2k__ confirmed)")
    print(f"LCC major version: {lcc_version}")
    qemu = shutil.which("qemu-e2k")
    print(f"qemu-e2k: {qemu if qemu else 'not found (optional)'}")
    print(
        "Result: compiler target macro verified; sysroot, linker, runtime "
        "and hardware remain separate checks."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
