# Inter-substrate runtime profile — Fragile-Baby

**Contract:** [SAMBU runtime API v1](https://github.com/bboroski/SAMBU/blob/feat/substrate-runtime-contract-v1/docs/INTERSUBSTRATE_RUNTIME_API_V1.md)  
**Status:** architecture/integration profile. Target-specific functionality remains gated by evidence.

## Ownership
Elbrus/E2K architecture and platform qualification workstream.

## Existing evidence
Architecture/CPU identity profile, toolchain and linker requirements, versioned target manifest and evidence-advisor workflow. Native target build, boot path and hardware qualification are not established.

## Integration slice
Define target resource descriptors for exact CPU/SoC, stepping, board revision, ABI, toolchain, linker layout, memory map and fixture. Add a binary ABI conformance pack for structure sizes, alignment, calling convention, atomics, syscall/interrupt conventions and endian assumptions, but do not fill values without authoritative vendor documentation. Link every capability to compiler output, emulator logs or board evidence.

## Explicit non-goals
No E2K support can be inferred from x86_64 or another RISC/CISC target. Do not claim working drivers, virtual memory, scheduler, network stack, atomics or hardware support from a specification or host mock.

## Acceptance tests
Schema and evidence completeness checks on host; cross-build with the exact vendor toolchain; inspect ELF machine/ABI and linker map; run on a verified E2K emulator or self-hosted physical target; preserve failures and unavailable checks in the matrix.

## Maturity rule
Host validation, a manifest, a simulator, or a successful unrelated target build cannot be promoted into kernel, firmware, ABI, or physical-hardware qualification. Every supported target requires its own reproducible evidence.
