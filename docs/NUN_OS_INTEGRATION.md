# NUN OS integration contract — Fragile-Baby

## Ownership
Fragile-Baby owns architecture qualification, evidence matrices and experimental platform validation, with emphasis on Elbrus/E2K-related toolchains and environments. NUN remains the canonical kernel and HAL implementation. Experimental evidence must not be promoted to a production backend without reproducible target tests.

## Integration direction
1. Maintain explicit architecture and toolchain capability matrices for every claim.
2. Define a versioned adapter boundary for NUN boot, memory-map, interrupt and device evidence.
3. Separate hardware availability, emulator availability, compiler support and successful kernel execution as independent evidence states.
4. Preserve raw logs, toolchain versions, target identifiers and artifact hashes.
5. Contribute architecture-specific tests upstream only when they are deterministic and do not weaken the x86_64 baseline.

## Acceptance gates
- Every claimed E2K capability links to a reproducible build or execution artifact.
- Unknown or untested features remain marked unsupported.
- Evidence schemas are validated and stale results are detected.
- Experimental BSP code cannot become a boot-critical NUN dependency by metadata alone.

## Current status
Fragile-Baby provides qualification and evidence support. This contract does not claim that the current NUN kernel boots on Elbrus/E2K.
