# Fragile-Baby — Elbrus (e2k) Platform Support

Fragile-Baby is an independent C11 platform-compatibility layer for Linux systems running on Elbrus processors. It combines target detection, explicit e2k generation profiles, an MCST LCC-aware CMake toolchain, compiler diagnostics, and integration contracts for the SAMBU repository family.

> **Status:** the portable core and host-test scaffold are in place. A real Elbrus build and execution still require an installed MCST toolchain/sysroot and validation on the target system. A toolchain file is not hardware qualification.

## Included

- E2K target detection through `__e2k__`, LCC version reporting through `__LCC__`, pointer-width and endian detection.
- Explicit e2k-v1…e2k-v7 generation selection via `FB_E2K_GENERATION`; no undocumented generation macro is guessed.
- An LCC/CMake toolchain that verifies the compiler actually defines `__e2k__`, preventing an accidental host binary from being labelled as an e2k build.
- A safe Linux probe for `uname`, online CPU count and available `/proc/cpuinfo` model fields. It does not access privileged registers or MMIO.
- One-knob commands: `python one.py test`, `python one.py e2k-doctor`, and `python one.py e2k-build`.
- Versioned integration boundaries for Kloz, CO, SaintSI, ReaperCripple, SAMBU, ToolNG and Klipot.

## Host development

Requirements: CMake 3.16+, a C11 compiler, and Python 3.10+.

```sh
python one.py test
```

Or use CMake directly:

```sh
cmake -S . -B build
cmake --build build --parallel
ctest --test-dir build --output-on-failure
```

## Build for Elbrus

On a target system or in an environment with a configured MCST SDK:

```sh
python one.py e2k-doctor
python one.py e2k-build
```

For a separately installed SDK:

```sh
E2K_CC=/opt/mcst/bin/lcc \
E2K_SYSROOT=/opt/mcst/sysroot \
FB_E2K_GENERATION=6 \
python one.py e2k-build
```

The paths above are examples and must be replaced with the actual installation paths. Vendor toolchain components are not downloaded automatically. The toolchain supports 32/64/128-bit address-model selection; 64-bit is the default.

See [toolchain and build](docs/TOOLCHAIN.md), [processor matrix](docs/PROCESSORS.md), and [ecosystem integration](docs/INTEGRATION.md).

## Ecosystem responsibilities

| Project | Fragile-Baby integration role |
|---|---|
| **Kloz** | low-level platform ABI, caller-owned memory and versioned platform operations |
| **CO** | deterministic component lifecycle, bounded polling and cleanup |
| **SaintSI** | heartbeat observation, degraded-state reporting and timeout checks |
| **ReaperCripple** | BSP, staged bootstrap, hardware profiles, telemetry and hardware qualification |
| **SAMBU** | language tooling, build models, declarative workflows and engineering contracts |
| **ToolNG** | local diagnostic reports and evidence quality; its Windows GUI is not an e2k target |
| **Klipot** | metadata projection, contract navigation and integration inventory |

These roles do not mean all repositories are already linked into one executable. Integrations are optional and versioned; the application owns composition.

## Current limitations

- Fragile-Baby does not ship an E2K compiler. Production target builds use the vendor MCST LCC toolchain.
- No unsupported LLVM/GCC e2k backend or custom machine-code generator is claimed.
- No direct clock/voltage control, IRQ manipulation, PMU access or MMIO is performed.
- Support by a particular Elbrus CPU generation depends on the installed OS, SDK and compiler release.
- Host CI validates the portable core, not the e2k cross-build, QEMU execution or physical hardware.
