# Fragile-Baby

**Initial integration scaffold for architecture-compatibility research.**

[Українська](README.md) · [English](README.en.md) · [Русский](README.ru.md)

## Current status

Fragile-Baby remains an initial scaffold. Its product role is not yet defined, and the repository does not contain an implemented runtime, compiler, BSP, bootloader, or verified processor support. This document describes a possible compatibility workstream without presenting it as an existing product capability.

## Reaper cycle compatibility

The [compatibility contract](docs/architecture/reaper-cycle-compatibility.md) records a possible integration point for the deterministic ReaperCripple simulation: fixed-width 64-bit state, an explicit seed, and a maximum of 6666 logical iterations.

This is a proposal only. It does not establish Fragile-Baby's product scope, claim x86-64 / Elbrus-E2K / Arm / RISC-V support, or implement a runtime.

## Engineering gates

- Define the repository's actual product role before adding executable subsystems.
- Keep ISA, ABI, compiler identity, and platform capabilities as separate facts.
- Require the target's native compiler and real hardware or emulator validation before claiming processor support.
- Add reproducible host reference tests before target-specific integration.
- Compare any future adapter against the ReaperCripple reference outputs.
