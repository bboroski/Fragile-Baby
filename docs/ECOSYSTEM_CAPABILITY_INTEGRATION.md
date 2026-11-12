# Ecosystem Capability Integration for Elbrus/E2K

**Status:** integration contract; adapters and target qualification are separate work items.  
**Target branch:** `integration/ecosystem-elbrus-lifecycle-2026-11-11`

## Purpose

Fragile-Baby is the qualification and integration workstream for Elbrus/E2K. This document maps reusable capabilities from the bboroski engineering ecosystem onto a complete, evidence-driven lifecycle. It does **not** copy unrelated application code, merge independent runtimes, or claim that an adapter is implemented merely because its source project has the capability.

The authoritative upstream repositories retain their own source, APIs, tests, release cycles and ownership. Fragile-Baby consumes versioned contracts and narrowly scoped adapters.

## Complete lifecycle

1. **Discover and identify** — record exact CPU model, stepping, board revision, firmware/PNS, OS release, compiler, binutils/linker, sysroot, ABI and target profile. Unknown values remain null.
2. **Configure** — resolve the MCST toolchain, target triple, data model, sysroot, linker/startup inputs and compiler feature set. Never infer E2K properties from x86, Arm or RISC-V.
3. **Build** — compile portable C11 components and target-specific slices; preserve compiler logs, command lines, versions and artifact hashes.
4. **Package and validate** — validate ELF metadata, architecture identity, entry/section bounds, image layout, memory-map constraints and versioned handoff metadata.
5. **Boot and execute** — follow the supported route PNS/firmware → Elbrus Linux → native E2K userspace unless a separately documented and proven board-specific route exists. Do not assume generic Limine or bare-metal kernel boot.
6. **Observe** — collect bounded health/heartbeat, diagnostics, device inventory and fault/degraded-state evidence with privacy-aware redaction.
7. **Recover** — define bounded retry, rollback, stop and restart behavior; never automatically write privileged hardware state.
8. **Qualify** — progress through host tests → MCST cross-build → E2K emulator → physical target. Each stage requires traceable evidence and cannot be skipped by a higher-level label.
9. **Release** — publish versioned manifests, ABI compatibility notes, SBOM/provenance where available, test reports and known limitations.

## Capability mapping

| Upstream | Reusable capability | Fragile-Baby integration boundary |
|---|---|---|
| SAMBU | Language front-end, typed IR slice, CLI/test runner, reproducible scientific and spatial models, E2K profile metadata | Optional build-description and test-generation adapter; do not claim a complete E2K native compiler backend |
| ToolNG | Read-only device inventory, event observations, local reports, evidence completeness and redaction | Host-side evidence collector only; Windows PnP/USB logic is not an E2K driver or target probe |
| ReaperCripple | C11 BSP patterns, bootstrap lifecycle, fault/degraded states, rollback, board profiles, calibration, CRC and CMake/CTest | Reuse lifecycle/BSP contracts; implement a distinct E2K board adapter only with documented board registers, startup and SDK |
| Kloz | Fixed-width status codes, versioned ABI/platform ops, caller-owned arena allocator, alignment/overflow checks, resource budgets | Candidate low-level portability substrate; agree ABI version and memory ownership before linking |
| CO | Deterministic STOPPED/STARTING/RUNNING/STEPPING/FAULTED/STOPPING lifecycle, caller-owned runtime, callbacks and recursion guards | Qualification job/runtime orchestration state machine; bounded and non-privileged |
| SaintSI | Fixed component registry, heartbeat, monotonic ticks, timeout, HEALTHY/DEGRADED, CRC-32 | Health/evidence monitoring for qualification agents and test stages |
| Klipot | Repository catalog, machine-readable registry, versioned integration protocol, schema/contract CI | Integration dashboard and manifest validation; browser UI is optional, not part of the E2K runtime |
| NUN | Kernel architecture contracts: CPU entry, exceptions, interrupts, memory, execution, synchronization and device boundaries | Reference requirements for a future E2K NUN port; NUN's current x86_64 bring-up is not E2K support |
| NUNLauncher | Kernel image header validation, entry-offset and memory-map bounds, versioned boot-info contract | Reusable format/validation concepts; E2K image format and firmware handoff require a separately versioned contract |
| Luci | Domain registry, manifest validation, fail-closed policy, maturity/evidence boundaries | Policy and capability registry; never auto-load or execute external project code |
| Hellduck | Federation registry, pinned upstream workspace, integration map and integrity checks | Source-of-truth discovery and pinned dependency metadata; no replacement for upstream CI or ownership |
| 9circ | Repository identity is known; detailed capability inventory is not established by its current README | Metadata-only until its code, APIs, tests and licence are audited; do not invent features |

## Cross-cutting contracts

- **ABI:** fixed-width types, explicit alignment, ownership, calling convention and version negotiation. Breaking changes require a new ABI major version.
- **Capabilities:** every adapter declares required/provided capabilities and fails closed when prerequisites are absent.
- **Memory:** caller-owned buffers where practical; checked arithmetic, explicit bounds and deterministic overflow behavior.
- **Lifecycle:** idempotent init/stop where possible; explicit partial-init cleanup; bounded retries and no hidden background work.
- **Evidence:** each result records stage, target identity, toolchain fingerprint, command, timestamp, artifact hash and trace reference. Sensitive data is redacted.
- **Observability:** bounded queues and logs; monotonic time; explicit HEALTHY/DEGRADED/FAULTED states.
- **Security:** no implicit code execution, firmware writes, MMIO, voltage/clock control or remote telemetry. Hardware actions require a separately reviewed, board-specific implementation.
- **Maturity:** `planned`, `implemented`, `host-tested`, `cross-compiled`, `emulator-tested`, `hardware-qualified` are distinct states. PR existence and host CI never imply hardware qualification.

## Elbrus-specific baseline

The current MCST development materials publish LCC 1.31.05 toolchains, binutils 2.45, GDB 17.1 and glibc 2.41 packages for multiple E2K variants, alongside E2K Linux 6.1 sources and qemu-user. Fragile-Baby must treat these as versioned external inputs, not vendor files to silently vendor or redistribute. Pin exact versions and checksums in a future toolchain lock manifest after licence and reproducibility review.

The initial supported execution contract is **PNS/firmware → Elbrus Linux → native E2K process**. Bare-metal boot, custom kernel handoff, driver/MMIO behavior and physical board support remain unqualified until exact board and firmware evidence exists.

## Acceptance gates

- [ ] Every source capability is mapped to a named adapter or explicitly marked out of scope.
- [ ] No upstream source tree or public API is silently overwritten.
- [ ] Every adapter has a versioned contract and negative tests for missing capabilities.
- [ ] Host CI passes independently of target claims.
- [ ] Cross-build records exact LCC/binutils/sysroot fingerprints and generated artifact hashes.
- [ ] Emulator tests identify emulator version and limitations.
- [ ] Physical qualification records exact CPU/stepping/board/firmware and reproducible logs.
- [ ] Release notes state the highest evidence stage actually passed.

## References

- MCST developer downloads: https://dev.mcst.ru/download/
- MCST Elbrus Linux platform matrix: https://www.mcst.ru/elbrus_linux
- Ecosystem integration ownership: https://github.com/bboroski/Hellduck
