#!/usr/bin/env python3
"""Read-only E2K environment, LCC option and ELF audit helper.

This utility never changes CPU frequency, firmware, kernel parameters, device
registers, files outside its temporary compile directory, or target state.
An E2K uname value is a platform observation, not physical qualification.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

ALLOWED_LCC_FLAGS = {
    "-O0", "-O1", "-O2", "-O3", "-O4", "-g",
    "-fprefetch", "-fcache-opt", "-fno-apb",
    "-faligned", "-faligned-check", "-ffast",
    "-fprofile-generate", "-fprofile-values",
}
CPUINFO_KEYS = {
    "processor", "model name", "cpu model", "cpu", "family",
    "revision", "stepping", "cpu revision", "vendor_id",
}
TOOLS = ("lcc", "ldis", "readelf", "objdump", "gdb", "perf", "numactl", "taskset")


def parse_cpuinfo(raw: str) -> dict[str, str]:
    """Return a small allowlisted subset; never export serials or identifiers."""
    first_block = raw.split("\n\n", 1)[0]
    result: dict[str, str] = {}
    for line in first_block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if key in CPUINFO_KEYS and value:
            result[key] = value[:160]
    return result


def inspect_readelf_header(output: str) -> dict[str, Any]:
    """Check the advertised ELF header fields for the E2K Linux userspace ABI."""
    def field(name: str) -> str | None:
        match = re.search(
            r"^\s*" + re.escape(name) + r":\s*(.*?)\s*$",
            output,
            flags=re.MULTILINE | re.IGNORECASE,
        )
        return match.group(1) if match else None

    elf_class = field("Class")
    data = field("Data")
    machine = field("Machine")
    errors: list[str] = []
    if not elf_class or "ELF64" not in elf_class.upper():
        errors.append("ELF class is not confirmed as ELF64")
    if not data or "little endian" not in data.lower():
        errors.append("ELF endianness is not confirmed as little-endian")
    if not machine or not re.search(r"MCST\s+Elbrus", machine, flags=re.IGNORECASE):
        errors.append("ELF machine is not confirmed as MCST Elbrus")
    return {
        "valid": not errors,
        "class": elf_class,
        "data": data,
        "machine": machine,
        "errors": errors,
        "scope": "ELF header preflight only; it does not execute or authenticate the binary",
    }


def build_report(
    system: str,
    machine: str,
    release: str,
    cpuinfo: dict[str, str],
    compiler: str | None,
    compiler_version: str | None,
    available_tools: dict[str, str | None],
) -> dict[str, Any]:
    native_candidate = system.lower() == "linux" and machine.lower() in {"e2k", "elbrus"}
    model = cpuinfo.get("model name") or cpuinfo.get("cpu model") or cpuinfo.get("cpu")
    stepping = cpuinfo.get("stepping") or cpuinfo.get("revision") or cpuinfo.get("cpu revision")
    return {
        "schema_version": "fragile-baby.e2k-audit.v1",
        "observed_host": {"system": system, "release": release, "machine": machine},
        "target_observation": {
            "architecture_candidate": "E2K" if native_candidate else "not-observed",
            "native_e2k_linux_candidate": native_candidate,
            "cpu_model_observed": model,
            "stepping_observed": stepping,
            "identity_complete": bool(model and stepping),
        },
        "toolchain": {
            "compiler_path": compiler,
            "compiler_version_output": compiler_version,
            "available_tools": available_tools,
        },
        "qualification": {
            "stage": "native-runner-candidate" if native_candidate else "host-not-e2k",
            "physical_hardware_qualified": False,
            "reason": "This read-only probe cannot distinguish every virtualized environment or replace reviewed physical-target evidence.",
        },
        "safety": {
            "read_only": True,
            "hardware_writes_performed": False,
            "frequency_or_voltage_changed": False,
            "firmware_or_kernel_configuration_changed": False,
        },
        "limitations": [
            "uname and /proc/cpuinfo are observations, not a complete signed hardware identity.",
            "Compiler presence/version does not prove that it targets the observed CPU or that generated code is correct.",
            "Tool availability does not prove that PMU events, affinity controls, or ISA features are supported.",
            "A successful cross-build or ELF check does not prove runtime behavior.",
        ],
    }


def _run_version(executable: str) -> str | None:
    try:
        completed = subprocess.run(
            [executable, "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    output = (completed.stdout or "") + (completed.stderr or "")
    return output.strip()[:1200] or f"version command exited {completed.returncode} without output"


def collect_report(compiler_override: str | None = None) -> dict[str, Any]:
    system = platform.system()
    machine = platform.machine()
    release = platform.release()
    cpuinfo: dict[str, str] = {}
    try:
        cpuinfo = parse_cpuinfo(
            Path("/proc/cpuinfo").read_text(encoding="utf-8", errors="replace")
        )
    except OSError:
        pass

    requested = compiler_override or os.environ.get("E2K_CC") or os.environ.get("E2K_LCC") or "lcc"
    compiler = shutil.which(requested) if os.path.sep not in requested else (
        requested if Path(requested).is_file() else None
    )
    compiler_version = _run_version(compiler) if compiler else None
    available_tools = {name: shutil.which(name) for name in TOOLS}
    if compiler and not available_tools.get("lcc"):
        available_tools["lcc"] = compiler
    return build_report(
        system, machine, release, cpuinfo,
        compiler, compiler_version, available_tools,
    )


def check_lcc_flag(compiler: str, flag: str) -> dict[str, Any]:
    if flag not in ALLOWED_LCC_FLAGS:
        return {
            "flag": flag,
            "accepted_by_toolchain": False,
            "checked": False,
            "error": "flag is not in the documented audit allowlist",
        }
    source_text = (
        "static double values[256];\n"
        "int main(void) {\n"
        "  double sum = 0.0;\n"
        "  for (int i = 0; i < 256; ++i) sum += values[i];\n"
        "  return sum > 0.0;\n"
        "}\n"
    )
    try:
        with tempfile.TemporaryDirectory(prefix="e2k-lcc-probe-") as temp:
            source = Path(temp) / "probe.c"
            output = Path(temp) / "probe.o"
            source.write_text(source_text, encoding="utf-8")
            completed = subprocess.run(
                [compiler, flag, "-c", str(source), "-o", str(output)],
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            return {
                "flag": flag,
                "accepted_by_toolchain": completed.returncode == 0 and output.is_file(),
                "checked": True,
                "return_code": completed.returncode,
                "stdout": (completed.stdout or "")[:500],
                "stderr": (completed.stderr or "")[:500],
                "scope": "compiler acceptance only; not a correctness or performance result",
            }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"flag": flag, "accepted_by_toolchain": False, "checked": True, "error": str(exc)}


def check_elf(path: Path, readelf: str | None = None) -> dict[str, Any]:
    tool = readelf or shutil.which("readelf")
    if not tool:
        return {"valid": False, "checked": False, "errors": ["readelf is unavailable"]}
    if not path.is_file():
        return {"valid": False, "checked": False, "errors": [f"file does not exist: {path}"]}
    try:
        completed = subprocess.run(
            [tool, "-h", str(path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"valid": False, "checked": False, "errors": [str(exc)]}
    if completed.returncode != 0:
        return {
            "valid": False,
            "checked": True,
            "errors": [(completed.stderr or completed.stdout or "readelf failed")[:500]],
        }
    result = inspect_readelf_header(completed.stdout)
    result["checked"] = True
    result["path"] = str(path)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only MCST E2K / LCC tuning audit.")
    parser.add_argument("--compiler", help="LCC executable or path; defaults to E2K_CC, E2K_LCC or lcc")
    parser.add_argument("--check-flag", action="append", default=[], metavar="FLAG",
                        help="Compile a temporary C probe with one documented LCC flag; repeatable")
    parser.add_argument("--elf", type=Path, help="Inspect ELF header without executing the file")
    parser.add_argument("--readelf", help="readelf executable override")
    parser.add_argument("--require-native", action="store_true",
                        help="Return non-zero unless the observed host is Linux/e2k")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument("--output", type=Path, help="Write report JSON to this path")
    args = parser.parse_args(argv)

    report: dict[str, Any] = {"environment": collect_report(args.compiler)}
    failures = False
    if args.check_flag:
        compiler = report["environment"]["toolchain"]["compiler_path"]
        checks = []
        for flag in args.check_flag:
            result = check_lcc_flag(compiler, flag) if compiler else {
                "flag": flag, "accepted_by_toolchain": False, "checked": False,
                "error": "LCC compiler was not found",
            }
            checks.append(result)
            if not result.get("accepted_by_toolchain"):
                failures = True
        report["flag_checks"] = checks
    if args.elf:
        elf_result = check_elf(args.elf, args.readelf)
        report["elf"] = elf_result
        if not elf_result.get("valid"):
            failures = True

    native = report["environment"]["target_observation"]["native_e2k_linux_candidate"]
    if args.require_native and not native:
        failures = True
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered if args.json or args.check_flag or args.elf or args.require_native else (
        "E2K candidate: " + ("yes" if native else "no") +
        "\nPhysical hardware qualified: no (requires reviewed target evidence)" +
        "\nCompiler: " + (report["environment"]["toolchain"]["compiler_path"] or "not found")
    ))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
