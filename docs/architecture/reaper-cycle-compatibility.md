# Fragile-Baby — Reaper cycle compatibility contract

## Repository role

Fragile-Baby is currently an empty project scaffold. This document establishes a narrow, testable direction without claiming that a compiler, runtime, processor port, or bootable image already exists.

## Compatibility target

The ReaperCripple model is a deterministic C11 software workload with a 64-bit state contract and a maximum of 6666 iterations. Fragile-Baby may later provide a target-porting or compatibility layer for the workload, but it must preserve the reference outputs and failure semantics.

## Architecture policy

- Keep ISA detection, compiler identity, ABI, and platform capabilities as separate facts.
- Do not advertise x86-64 support when building for Elbrus/E2K, Arm, or RISC-V.
- Use the target's native compiler and headers; never emulate vendor support by changing a label.
- Verify integer widths, alignment, calling convention, and linker layout in target-specific tests.
- Treat host tests as portability evidence only, not physical target qualification.

## Integration sequence

1. Define the repository's actual product scope and supported targets.
2. Add a minimal CMake or Make build with strict warnings.
3. Add a host test for fixed-width arithmetic and deterministic reference vectors.
4. Add a separate Elbrus/E2K toolchain profile only when a real toolchain is available.
5. Compare the model's output against ReaperCripple before declaring compatibility.

Reference implementation: ReaperCripple. No binary or target support is claimed by this document.
