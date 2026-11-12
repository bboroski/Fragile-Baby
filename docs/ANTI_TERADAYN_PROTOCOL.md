# Anti-Teradayn Protocol — Fragile-Baby

**Status:** repository-level engineering standard. All implementation and readiness claims require source, test, and target evidence.  
**Scope:** this repository only. The protocol does not authorize destructive rewrites, blanket dependency removal, or implicit execution of code from another repository.

## Purpose

Apply measurable engineering discipline: bounded responsibilities, explicit interfaces, predictable resource use, minimal necessary dependencies, and reproducible verification. “Typified steaming” means typed, bounded, reviewable changes—not a new runtime or a claim of zero entropy.

## Seven-phase protocol

1. **Dependency discipline.** Inventory dependencies. Remove only components proven unnecessary and only after a tested replacement exists. Preserve product-required web, GUI, scripting, and network surfaces; isolate their trust boundaries.
2. **Corpuscular transparency.** Prefer explicit data flow, narrow functions, fixed-width types at ABI boundaries, clear ownership, and measured hot paths. Use assembly only for demonstrated platform needs. Swift is optional, never a universal bridge/compiler layer.
3. **Driver and hardware boundaries.** Put privileged access behind native platform adapters with explicit contracts, error paths, and capability checks. Ruby is optional tooling, not a kernel-driver ABI. Never infer hardware behavior from a design document.
4. **Applicable validation matrix.** Run tests that match this product: unit, integration, static, build, schema, emulator, and hardware checks as applicable. GUI, Lua, rendering, interrupt, and physical-device tests are conditional. Label host/emulator/target evidence separately.
5. **Hardened integration.** Use least privilege, validate untrusted inputs, bound timeouts and resource use, and document cache/retention. Google services and external APIs are optional, not mandatory architecture.
6. **SAMBU relationship.** Use SAMBU for scientific/statistical workloads only where justified and through versioned contracts. Do not add modeling dependencies to unrelated components.
7. **Resource allocation.** Keep core compute in the native implementation and orchestration/UI in supported existing layers. C/C++/C#/Swift/Ruby are not mandatory tracks. “Six-molecule allocation” is not a technical rule; define memory, CPU, concurrency, and latency budgets in measurable units.

## Typed-steaming rules

- **Never boil:** no broad refactor without scoped behavior change and regression coverage.
- **Never over-boil:** keep modules bounded; prefer composition and explicit ownership.
- **Never cook:** avoid hidden global state, unbounded queues, implicit network calls, and unnecessary runtime work.
- Preserve public contracts unless a versioned migration is supplied.
- No performance claim without reproducible benchmarks.
- Do not infer production, OS, driver, or hardware readiness from mockups, specifications, or host tests alone.

## Repository-specific application

**Verified profile:** Elbrus/E2K architecture and platform-qualification workstream with CPU/SoC identity, ABI/toolchain/linker/image/memory-map manifests, host/cross-build/emulator/physical evidence matrix, and a Python evidence advisor. Current README explicitly says verified E2K target implementation, boot path, and hardware qualification are not yet available. Do not infer E2K properties from x86/Arm. Keep evidence stages distinct and mark all target-dependent claims pending until the actual toolchain and hardware results are recorded. Check: `python3 tools/evidence_advisor.py`; `python -m unittest discover -s tests -v`.

## Acceptance checklist

- [ ] Scope and intended behavior are explicit.
- [ ] Dependency/security impact is recorded; no blanket technology purge.
- [ ] Interfaces, ownership, trust boundaries, error paths, and resource limits are documented.
- [ ] Relevant tests/checks pass; unsupported target checks remain pending.
- [ ] Documentation matches implementation and accurately labels maturity.
- [ ] Cross-repository integration uses versioned contracts and never executes foreign code implicitly.

## Ecosystem boundary

Repositories remain independently buildable with their own APIs, release cycles, and evidence. Federation means documented contracts, not a forced monolith or shared runtime. See the [Hellduck Integration Playbook](https://github.com/bboroski/Hellduck/blob/main/docs/INTEGRATION_PLAYBOOK.md) where applicable.

---

*Make every claim testable, every boundary explicit, and every optimization measurable.*
