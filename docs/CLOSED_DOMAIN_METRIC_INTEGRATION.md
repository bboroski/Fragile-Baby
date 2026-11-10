# Closed-Domain Boundary Profile — Fragile-Baby

**Proposed role:** Elbrus CPU architecture and platform-support workstream; implementation and hardware qualification must be evidenced separately.

## Transfer into the Elbrus port

The bounded-domain concept is useful as a verification framework for address spaces, ABI boundaries, memory regions, and controlled boot/runtime interfaces. The actual details must come from the exact Elbrus CPU model, vendor documentation, toolchain, and platform—not from analogy.

| CDM-1 concept | Fragile-Baby engineering use |
|---|---|
| Bounded region | Kernel/firmware image, RAM banks, reserved areas, stacks, MMIO, DMA windows |
| Boundary | ISA/ABI calling convention, privilege transitions, page permissions, alignment, and address width |
| Fixed snapshot | Versioned CPU/board/toolchain capability manifest |
| Boundary stress | Unsupported instruction, privilege fault, memory-map overlap, DMA ownership fault, or ABI mismatch |
| Invariant ledger | Memory map, linker sections, image ranges, and test-evidence inventory |
| Isolation | Separate host simulation, emulator, cross-build, and physical Elbrus validation evidence |

## Required invariants

1. Never infer an Elbrus memory map, privilege mode, cache/DMA rule, or instruction-set extension from another CPU family.
2. Record the exact CPU/SoC variant, stepping, board revision, ABI, compiler version, binutils/linker, startup objects, and linker script for each port.
3. Validate image and memory intervals with overflow-safe arithmetic and explicit alignment.
4. Keep architecture-specific code behind a narrow, versioned platform interface.
5. Treat host tests as software checks only; require native/cross compiler output, emulator results where available, and physical target results before promoting support status.
6. A failed or unavailable toolchain check remains unknown/failed; it must not be described as supported.

## Acceptance gates

- Add an Elbrus target matrix with exact model, ISA profile, ABI, toolchain, linker, emulator, and hardware evidence columns.
- Add compile-only smoke tests for each declared compiler/ABI combination.
- Add linker-map and image-layout validation.
- Add target tests for entry, privilege transition, memory boundary, and exception handling when the required platform is available.

## Scope

This is a support and validation framework, not a claim that Elbrus hardware is currently supported. CDM-1 does not add a mass model to the CPU port or substitute for official architecture specifications.
