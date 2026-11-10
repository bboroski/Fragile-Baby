<p align="center"><strong>FRAGILE-BABY</strong></p>
<p align="center"><strong>Elbrus Platform Support Workstream</strong></p>
<p align="center"><img src="https://img.shields.io/badge/STATUS-ARCHITECTURE%20PROPOSAL-FFD600?style=for-the-badge&labelColor=111111" /> <img src="https://img.shields.io/badge/FOCUS-ELBRUS%20QUALIFICATION-FFD600?style=for-the-badge&labelColor=111111" /></p>
<p align="center"><a href="README.md">🇺🇦 Українська</a> · <a href="README.en.md">🇬🇧 English</a> · <a href="README.ru.md">🇷🇺 Русский</a></p>

# Fragile-Baby

**An engineering workstream for evidence-based Elbrus processor support — from exact ABI and toolchain profiles to image and target qualification.**

> **Current status:** architecture proposal and integration scaffold. No verified implementation, boot path or qualified board is currently claimed.

## Product role

Fragile-Baby is intended to establish a reproducible way to assess whether an exact CPU/SoC, ABI, compiler, linker and board configuration can support a defined system scenario. No property is inferred from Arm, x86, RISC-V or another processor family.

## Capability development tracks

- **Target profiles:** exact CPU/SoC model, stepping, ISA profile, ABI and board revision.
- **Toolchain matrix:** compiler, assembler, linker, runtime, startup objects and versions.
- **Image validation:** format, bounds, alignment, overflow-safe address arithmetic and integrity checks.
- **Linker audit:** sections, entry point, memory regions, stack, reserved ranges and map file.
- **Evidence pipeline:** separate host-check, cross-build, emulator and physical-target results.
- **Compatibility ledger:** interface versions, known limits, regressions and migration rules.

These are planned capability areas, not features already implemented.

## Getting started

This repository is currently documentation-first. Review:
- [Closed-domain integration profile](docs/CLOSED_DOMAIN_METRIC_INTEGRATION.md)
- [Product system and feature governance](docs/PRODUCT_SYSTEM.md)

Run the documentation quality gate:

```bash
python .github/scripts/duck_quality_gate.py
```

## Support qualification gates

| Stage | Required evidence |
|---|---|
| Target definition | Exact CPU/SoC, stepping, board and ISA |
| ABI/toolchain | Compiler, linker, ABI and startup-file versions |
| Cross-build | Reproducible build and retained build logs |
| Image/linker | Validated image, map file, bounds and entry point |
| Emulator | Reproducible boot and test log, where available |
| Hardware | Result from the exact physical board |

Until evidence exists, status remains **NOT VERIFIED**. A host test is not proof of Elbrus hardware support.

## Safety and governance

Never guess the memory map, privilege mode, cache/DMA rules or ISA extensions. Missing or failed toolchains must remain visible states, not hidden fallbacks. Every capability needs an ID, acceptance criteria, tests, an owner role and a rollback plan.

## Design and communication

The ecosystem visual baseline is a black `#111111` canvas, yellow `#FFD600` accent, legible type, clear states and accessible navigation. Marketing must distinguish proposals from implemented and verified results.

**Fragile-Baby — built with care for every system-level contract.**
