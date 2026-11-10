#!/usr/bin/env python3
"""One-knob entry point for Fragile-Baby host and E2K workflows."""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent


def run(command: list[str], cwd: pathlib.Path = ROOT) -> int:
    print("+", " ".join(command), flush=True)
    return subprocess.call(command, cwd=cwd)


def host_test(build_dir: pathlib.Path) -> int:
    cmake = [
        "cmake", "-S", str(ROOT), "-B", str(build_dir),
        "-DCMAKE_BUILD_TYPE=Release",
    ]
    result = run(cmake)
    if result != 0:
        return result
    result = run(["cmake", "--build", str(build_dir), "--parallel"])
    if result != 0:
        return result
    return run(["ctest", "--test-dir", str(build_dir), "--output-on-failure"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        nargs="?",
        choices=("test", "e2k-doctor", "e2k-build", "clean"),
        default="test",
    )
    parser.add_argument("--build-dir", default=str(ROOT / "build"))
    args = parser.parse_args()

    if args.command == "test":
        return host_test(pathlib.Path(args.build_dir).resolve())
    if args.command == "e2k-doctor":
        return run([sys.executable, str(ROOT / "scripts" / "e2k-doctor.py")])
    if args.command == "e2k-build":
        return run(["sh", str(ROOT / "scripts" / "build-e2k.sh")])
    if args.command == "clean":
        return run(["cmake", "-E", "rm", "-rf", str(pathlib.Path(args.build_dir).resolve())])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
