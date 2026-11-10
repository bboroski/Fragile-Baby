#!/usr/bin/env python3
"""Host contract checks for the Fragile-Baby Elbrus qualification gates."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def check() -> None:
    build = ROOT / ".build"
    subprocess.run(
        ["cmake", "-S", str(ROOT), "-B", str(build), "-DBUILD_TESTING=ON"],
        check=True,
    )
    subprocess.run(["cmake", "--build", str(build), "--parallel"], check=True)
    subprocess.run(["ctest", "--test-dir", str(build), "--output-on-failure"], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", nargs="?", choices=("check",), default="check")
    parser.parse_args()
    try:
        check()
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"Fragile-Baby check failed: {exc}", file=sys.stderr)
        return 1
    print("Elbrus profile gates: PASS (no compiler or hardware support implied)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
