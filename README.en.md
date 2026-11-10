# Fragile-Baby — Elbrus Qualification Platform

**Purpose:** reproducible qualification of compilers, ABIs, toolchains and platform adapters for the Elbrus / E2K processor architecture.

[Українська](README.md) · [Русский](README.ru.md)

## Current status

This is an initial engineering scaffold: an E2K JSON profile, a standard-library validator and tests. The repository does **not** yet claim complete Elbrus processor support. It does not contain a verified vendor toolchain, BSP, drivers, linker scripts, bootable runtime or physical-hardware test results.

## Engineering tracks

- identify the exact processor model, board and revision;
- maintain reproducible toolchain profiles with compiler version, target triple, sysroot, linker and ABI;
- reuse portable C11 contracts from Kloz, CO and SaintSI;
- qualify ReaperCripple adapters only after the actual toolchain is verified;
- align boot and capability contracts with NUN and NUNLauncher;
- keep host tests separate from emulator and target-hardware tests.

## Validate a profile

Python 3.10+ is required; no third-party packages are needed.

```sh
python3 tools/validate_toolchain_profile.py profiles/elbrus.template.json
python3 -m unittest discover -s tests -v
```

The template intentionally uses unknown values and the unverified status. It is not a working compiler configuration.

## Evidence rule

The target-validated status requires the exact CPU model and board revision, compiler/linker/sysroot versions, build command, artifact, test results and links to reproducible logs. A recommendation from Gemini or another model is not compatibility evidence.

See the [Elbrus qualification plan](docs/ELBRUS_QUALIFICATION.md) and [toolchain profile template](profiles/elbrus.template.json).

## Safety boundary

Profiles do not execute commands or change frequencies, voltages, registers or boot configuration. Never copy a setting from another CPU model without independent confirmation. Do not use this scaffold to flash physical hardware.
