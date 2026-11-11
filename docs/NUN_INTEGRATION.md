# NUN integration — Elbrus / E2K qualification boundary

## Assigned responsibility

Fragile-Baby is the separate Elbrus/E2K architecture and platform-qualification workstream. Its NUN role is to establish target-specific CPU, ABI, compiler, linker, memory-map and boot evidence for a future E2K port.

## Current verified state

- CPU/SoC identity, stepping, ABI, toolchain and memory-map qualification requirements are documented.
- A versioned qualification manifest and host-side evidence advisor exist.
- There is no verified E2K NUN kernel build, boot path, emulator result or physical hardware qualification.

## Integration contract

1. Treat E2K as a distinct ISA and ABI. Do not reuse x86_64 register conventions, GDT/IDT setup, paging code or interrupt assumptions.
2. Require an identified E2K compiler/toolchain version, linker format and startup environment before enabling target code.
3. Record board/SoC identity, stepping, firmware revision, memory map, compiler identity and test artifact hashes in the evidence manifest.
4. Keep host checks, cross-build, emulator tests and physical target results as distinct evidence classes.
5. Do not mark an E2K target ready based only on a source-level specification or a successful host build.
6. Define the architecture port behind the NUN HAL contract only after the x86_64 phase-A interfaces are reviewed and versioned.

## Dependency order

The current [NUN](https://github.com/bboroski/NUN) phase-A branch targets x86_64 under QEMU. Fragile-Baby remains a parallel qualification design, not an implicit second supported NUN architecture. Its E2K work must pass independent build, boot and hardware gates.

## ABI status

No E2K ABI or NUN kernel ABI is changed here. Record all future NUN-facing E2K contract changes in `CHANGELOG.NUN`.
