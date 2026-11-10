# Fragile-Baby

**Portable compatibility layer for systems software and computational models.**

[Українська](README.md) · [English](README.en.md) · [Русский](README.ru.md)

## Current status

Fragile-Baby is an initial scaffold. The repository does not yet contain an implemented runtime, compiler, BSP, bootloader, or verified processor support. The documentation defines testable boundaries for future implementation and does not present plans as working code.

## Reaper cycle

The [compatibility contract](docs/architecture/reaper-cycle-compatibility.md) describes a future integration with the deterministic ReaperCripple model: 64-bit state, an explicit seed, and no more than 6666 logical iterations.

## Priorities

- Keep ISA, ABI, compiler, platform capabilities, and data model as separate facts.
- Do not claim x86-64, Elbrus/E2K, Arm, or RISC-V support without the relevant compiler and target validation.
- Preserve a portable C11 foundation and fixed-width data types.
- Add a build, host tests, and reproducible reference vectors before hardware integration.
- Compare results against the ReaperCripple reference model.

## Important limitation

A 64-bit data model does not create 666-bit registers or prove support for a processor architecture. Host emulation validates software invariants only, not physical hardware operation.
