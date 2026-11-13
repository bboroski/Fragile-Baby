# GitHub-to-Elbrus Engineering Transfer Catalogue

**Status:** research and integration proposal; no claim of completed hardware optimization  
**Inventory snapshot:** 2026-11-13  
**Target:** MCST Elbrus / E2K, Linux userspace first

## Executive statement

The 15 repositories visible in the linked GitHub installation contain reusable software-engineering assets for an Elbrus-facing stack: an E2K target profile and MCST LCC build route, a native Linux userspace bootstrap, portable C11 memory/runtime primitives, boot-image admission and evidence tooling, integrity/health contracts, deterministic lifecycle models, scientific workloads, and cross-repository validation.

These assets can improve software built for and qualified on Elbrus. They do not change processor silicon, microcode, firmware, voltage/frequency limits, cache topology, execution hardware or MCST's proprietary compiler. No such hardware-level change is claimed.

## Verified E2K baseline

The NUN E2K profile records ELF64, little-endian, `EM_MCST_ELBRUS = 175`, Linux `uname -m = e2k`, the MCST E2K Linux userspace ABI and MCST LCC. It distinguishes E2K generations and vendor target profiles instead of treating all E2K systems as identical.

The documented deployment path is **MCST PNS -> Elbrus Linux -> native E2K userspace process**. NUN's current E2K component is a Linux userspace bootstrap, not a freestanding E2K kernel. Its existing Limine kernel is x86_64-only. `qemu-e2k` user-mode emulation is not full-system or firmware emulation.

NUN's build script invokes LCC and generates a manifest checking ELF class, byte order, machine value, entry point, file size and SHA-256. The repository correctly states that cross-build success is not runtime proof, and SHA-256 alone does not authenticate a publisher.

## Repository-by-repository transfer map

| Repository | Observed asset / scope | Candidate contribution to Elbrus | Boundary / required proof |
|---|---|---|---|
| [NUN](https://github.com/bboroski/NUN) | E2K profile, LCC build route, native Linux host runtime, boot/kernel contracts | Canonical E2K integration target; unify profile, build, ELF checks, runtime tests and manifests | Keep x86_64 kernel separate; execute on identified E2K hardware |
| [Fragile-Baby](https://github.com/bboroski/Fragile-Baby) | Elbrus qualification workstream, CPU/SoC identity, staged evidence matrix | Public evidence dossier, hardware/software identity and qualification gates | Current status: architecture proposal / target evidence pending |
| [SAMBU](https://github.com/bboroski/SAMBU) | Python-hosted language/model environment, typed-IR C11 native-compiler slice, scientific and voxel workloads, E2K toolchain file | Representative compiler/runtime workloads; future E2K codegen experiments; reproducible scientific profiling | README says native slice is not a complete source-to-machine-code compiler |
| [Kloz](https://github.com/bboroski/Kloz) | C11 substrate, caller-owned arena, alignment/overflow checks, versioned platform-ops ABI, resource budgets, CPU matrix | Port and measure allocator, capability and platform abstractions under LCC | Cache, DMA, MMIO, alignment and memory-order guarantees need target-specific evidence |
| [CO](https://github.com/bboroski/CO) | Deterministic component lifecycle, explicit state model, caller-owned memory, diagnostics | Low-overhead component runtime for E2K tools and test agents | Measure latency natively; do not label it an RTOS |
| [SaintSI](https://github.com/bboroski/SaintSI) | Heartbeat registry, monotonic tick handling, health/degraded states, CRC-32 | Runtime health and telemetry-integrity checks for E2K test agents | Heartbeat does not prove correctness; CRC-32 is not authentication |
| [ReaperCripple](https://github.com/bboroski/ReaperCripple) | Portable C11 embedded runtime, BSP adapters, lifecycle/fault handling, manufacturing test workflows | Reuse fault policy, staged bring-up and board-profile discipline in lab tooling | Existing adapters target other families; E2K needs its own reviewed port |
| [NUNLauncher](https://github.com/bboroski/NUNLauncher) | Boot-image metadata validator, versioned boot contract, memory-map and entry checks | Adapt validation patterns to E2K userspace package admission and release manifests | Host-side validator, not E2K bootloader; current README marks images unsigned |
| [ToolNG](https://github.com/bboroski/ToolNG) | Read-only device evidence, readiness/completeness reporting, local diagnostics | Reuse provenance and uncertainty reporting for E2K host inventory | Windows host utility; no current Elbrus hardware probe |
| [Klipot](https://github.com/bboroski/Klipot) | Machine-readable registry, JSON schemas, mesh envelopes, contract validation and portal | Publish E2K target profile, capabilities and qualification results as versioned contracts | Browser labs are not native execution or hardware telemetry |
| [Luci](https://github.com/bboroski/Luci) | Engineering-domain registry, reference validation, fail-closed policy, maturity/evidence boundaries | Prevent unsupported E2K claims and gate releases on evidence | Registry navigation is not compatibility proof or sandboxing |
| [Hellduck](https://github.com/bboroski/Hellduck) | Workspace with six project snapshots, migration verification and integration contracts | Cross-project source-of-truth and migration-integrity checks | Snapshots do not replace source repositories or Git histories |
| [Jungelist-Massive](https://github.com/bboroski/Jungelist-Massive) | Minimal README and planning workflow in inspected tree | Possible future compiler/language experimentation front-end | No E2K compiler/backend capability established |
| [BlopScore](https://github.com/bboroski/BlopScore) | Project brief for native hardware observation and industrial UI | Future E2K observability/reporting shell once verified probes exist | README explicitly says intent is not proof of kernel access, sensor coverage or benchmark accuracy |
| [9circ](https://github.com/bboroski/9circ) | Inspected tree contains only README.md | Keep inventoried; no transferable implementation established | No capability inferred from repository name |

## Prioritized engineering work

### P0 — Reproducible E2K toolchain and native execution

1. Make NUN the canonical source for the E2K target profile and shared MCST LCC toolchain configuration; prevent silent profile drift across repositories.
2. Record CPU family/model/stepping, board revision, PNS/firmware, Elbrus Linux distribution/kernel, ABI, LCC, linker/binutils, sysroot and runtime-library versions.
3. Add a native E2K CI job that records exact commands, compiler identity, artifacts, test output and target identity.
4. Keep host-tested, cross-built, emulated, native-run and hardware-qualified as distinct statuses.
5. Retain SHA-256 artifact manifests; add signature verification and publisher-key lifecycle before claiming authenticated releases.

### P1 — Reproducible workload and benchmark suite

Add source-controlled benchmarks with fixed inputs, correctness checks, warm-up, repetitions, variance, compiler flags and raw output:
- integer and floating-point scalar kernels;
- memory bandwidth/latency over multiple working-set sizes;
- pointer chasing and cache working-set sweeps;
- branch-heavy and branch-light control flow;
- Kloz arena allocation and bounds checks;
- CO lifecycle and diagnostics overhead;
- SaintSI CRC/health-monitor overhead;
- SAMBU sparse-grid, voxel and graph workloads;
- process startup and I/O workloads for NUN userspace.

Record elapsed time/throughput, variance and peak RSS. Record energy or hardware counters only when trustworthy target instrumentation exists. Never invent cache, frequency, IPC or power values.

### P2 — LCC/compiler experiments

1. Establish a known-good LCC baseline for each supported E2K profile.
2. Preserve compiler version, target flags, sysroot, source revision and disassembly/report output.
3. Compare documented optimization options one variable at a time.
4. Add small C/C++ microbenchmarks with correctness checks and anti-dead-code-elimination safeguards.
5. With baseline data, investigate instruction scheduling, vectorization, inlining, register pressure, code size and memory access patterns using vendor compiler reports and generated assembly where available.
6. Treat assembly findings as specific to the tested compiler/CPU combination, not universal E2K rules.

### P3 — Cross-repository adapters

- Kloz: E2K platform-ops implementation and ABI conformance tests.
- CO: E2K build target and lifecycle latency benchmark.
- SaintSI: native monotonic-clock adapter and health-agent tests.
- ReaperCripple: E2K host/BSP profile only where its runtime boundary fits.
- NUNLauncher: E2K userspace artifact manifest validation, not firmware flashing.
- ToolNG/BlopScore: read-only evidence collection and reporting after a real E2K probe exists.
- Klipot/Luci/Hellduck: schemas, provenance, integration and evidence gates.
- SAMBU/Jungelist-Massive: future workload generation and compiler research after a real backend exists.

## Evidence contract for every proposed optimization

Every item must record source repository/path/commit/license; original purpose; exact adaptation; target CPU/model/stepping/board; OS/kernel/ABI/PNS/compiler/sysroot; build command and flags; correctness tests; benchmark source/inputs/repetitions/raw results/baseline; limitations and rollback.

Use these statuses:

| Status | Meaning |
|---|---|
| `proposed` | Idea only |
| `implemented-host` | Implemented and tested on non-E2K host |
| `cross-built` | Artifact emitted by named E2K cross-toolchain |
| `emulated` | Executed under named user-mode emulator profile |
| `native-e2k-tested` | Executed on identified native E2K system |
| `hardware-qualified` | Repeated, reviewed evidence for the exact stated configuration |

Never promote a status because a different stage passed.

## MCST-facing technical package

The review package should contain:
1. Scope and exact hardware/software configuration.
2. Repository-to-feature traceability matrix.
3. LCC build instructions, flags and sysroot details.
4. Native test logs and raw benchmark data.
5. Correctness, ABI and compatibility results.
6. Compiler reports/generated assembly for selected workloads, where redistribution is permitted.
7. Known limitations and questions requiring MCST guidance.

Questions for MCST should be specific: supported LCC versions/options; target ABI and memory-model guarantees; available performance-counter interfaces; supported CPU/board combinations; and recommended benchmark methodology. Do not imply MCST endorsement or partnership.

## Acceptance criteria

- [ ] All 15 visible repositories remain inventoried.
- [ ] Every transfer proposal has a source and destination repository.
- [ ] Every E2K build records compiler, flags, sysroot and target identity.
- [ ] A native E2K runner executes tests before any native-support claim.
- [ ] Benchmarks publish raw data and reproducible commands.
- [ ] No x86_64 boot code is presented as E2K boot code.
- [ ] Host/cross-build results are not described as hardware qualification.
- [ ] No undocumented register, firmware, voltage/frequency or microcode modification is proposed.

## Primary source paths

- NUN: `platforms/e2k/target.json`, `docs/ELBRUS_E2K.md`, `scripts/build-e2k-host.sh`
- SAMBU: `cmake/toolchains/e2k-linux-lcc.cmake`
- Kloz: `docs/CPU_ARCHITECTURE_MATRIX.md`
- Fragile-Baby: `docs/qualification/e2k-evidence-matrix.md`

**Conclusion:** The strongest defensible near-term improvement is a unified, native-tested E2K software stack with provenance, reusable low-level components, compiler experiments and benchmark evidence that MCST engineers can reproduce and review—not an unsupported claim to modify Elbrus silicon.
