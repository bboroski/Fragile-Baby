# Multi-Axis Layer Architecture

**Architecture:** NUN Mesh — Multi-Axis Layer Fabric (MALF)  
**Repository:** `bboroski/Fragile-Baby`  
**Role:** Elbrus/E2K architecture research and platform qualification workstream  
**Maturity:** Architecture proposal with qualification evidence pending; no verified E2K target implementation implied.  
**Status:** Target boundary contract; planned or proposed capabilities are not implementation evidence.

## Purpose

MALF is a multi-axis model rather than a directory convention. It separates structural ownership, vertical workflows, trust boundaries, lifecycle stages and evidence. Existing files are not moved solely to satisfy the model.

## Structural layers

| ID | Layer | Responsibility |
|---|---|---|
| L0 | **Experience** | CLI, portal, UI and operator workflows. |
| L1 | **Contracts** | Versioned manifests, schemas, APIs, ABI and evidence formats. |
| L2 | **Application orchestration** | Commands, qualification workflows and integration journeys. |
| L3 | **Domain kernel** | Domain models, classification, constraints and deterministic calculations. |
| L4 | **Policy and capabilities** | Trust, risk gates, maturity thresholds and permitted operations. |
| L5 | **Ports** | Abstract compiler, platform, filesystem, registry and evidence interfaces. |
| L6 | **Adapters** | Concrete ISA/toolchain/OS/repository and external-source implementations. |
| L7 | **Data and evidence** | Registries, matrices, artifacts, reports, provenance and persistent state. |
| L8 | **Runtime and delivery** | Build, CLI packaging, environment composition and publication. |
| L9 | **Assurance** | Unit/schema tests, target matrix, qualification and reproducible evidence. |

## Dependency law

- L0 invokes L2 workflows through L1 contracts.
- L2 coordinates L3 domain logic and L4 policy through L5 ports.
- L6 adapters implement ports and contain environment-specific behavior.
- L7 stores versioned inputs, decisions and evidence with provenance.
- L8 composes and packages the system; L9 independently verifies declared claims.
- Domain and policy logic must not depend on a portal, shell command or external host API.

## Orthogonal axes

1. **Structural:** the ten layers above.
2. **Vertical slice:** from input through classification/decision, external adapter, evidence and tests.
3. **Trust:** source identity → validation → policy → authorized access → recorded result.
4. **Lifecycle:** proposal → specification → toolchain setup → host checks → cross-build → emulation → physical target → qualification/release.
5. **Evidence:** every claim carries source, target, date/toolchain, method, result and confidence; unknown remains unknown.

## Repository-specific allocation

### L0 — Qualification operator surface
CLI report, target matrix and developer workflow for examining qualification readiness.

### L1 — Platform identity and evidence contracts
Versioned CPU/SoC, stepping, ABI, board revision, compiler, image and evidence manifest schemas.

### L2 — Qualification orchestration
Check identity → verify toolchain → inspect linker/image assumptions → run host/cross-build/emulator/target stages → record evidence.

### L3 — ISA and platform domain
E2K architecture identity, ABI constraints, memory model, instruction/toolchain requirements and platform capability taxonomy.

### L4 — Evidence maturity policy
Separate verified, partial, unknown and blocked states; no support claim without exact target/compiler/method evidence.

### L5 — Toolchain and evidence ports
Abstract compiler invocation, linker inspection, target runner, artifact storage and evidence collection contracts.

### L6 — E2K-specific adapters
Future compiler/assembler/linker, emulator and physical-target adapters; do not reuse x86_64 assumptions as E2K behavior.

### L7 — Qualification evidence state
Identity manifests, tool versions, command logs, build artifacts, reports and provenance records.

### L8 — Research and build environment
Host-side scripts, pinned dependencies, cross toolchain bootstrap and controlled result publication.

### L9 — Multi-stage qualification
Host checks, cross-compilation, emulator execution and physical-target evidence as separate gates.

## Vertical slices

1. **Target identity:** CPU/SoC + stepping + board + ABI identity → schema validation → supported/unknown classification → evidence record.
2. **Cross-build qualification:** Pinned E2K toolchain → compiler/linker check → reproducible artifact → static inspection → explicit pass/block report.
3. **Physical target qualification:** Exact hardware identity → approved test procedure → captured measurements/logs → independent review → qualified scope.

## Cross-cutting planes

- **Evidence provenance:** distinguish specification, host simulation, cross-build, emulator and physical-target observations.
- **Security:** untrusted manifests and source material are data, never instructions or permission grants.
- **Resilience:** bounded scans, explicit incomplete/unknown outcomes and recoverable workflows.
- **Compatibility:** version ISA, ABI, toolchain and evidence schemas; never infer one ISA from another.
- **Observability:** logs and reports are reproducible, redacted and linked to exact inputs.
- **Accessibility:** apply to operator-facing tools.

## NUN Mesh federation

This project may consume or publish versioned manifests and evidence contracts. A catalogue entry or dependency link does not imply code execution, ABI compatibility or target qualification. Cross-repository integrations must specify provider, consumer, version, optionality, failure behavior and test evidence.

## Incremental adoption

1. Record scope, target identity and current maturity for every feature.
2. Extract contracts and schemas (L1) from ad hoc documents.
3. Separate domain reasoning (L3) from shell, vendor and platform adapters.
4. Gate external access and qualification status at L4.
5. Store immutable input/evidence identities at L7.
6. Add host, cross-build, emulator and target stages separately at L9.
7. Refactor one vertical path at a time and keep unverified claims explicitly pending.

## Definition of done

A claim identifies its target and evidence class; dependencies respect boundaries; manifests are versioned; unknowns are not upgraded to passes; and a new capability cannot bypass policy or provenance.

## Repository guardrails

Do not claim an E2K kernel, bare-metal boot path, production runtime or hardware compatibility until exact target source and reproducible evidence exist. Never infer E2K register, ABI, memory or toolchain behavior from x86/Arm. Host tests prove only host logic.
