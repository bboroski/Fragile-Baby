# Fragile-Baby

**Status:** architecture proposal and integration-reference scaffold; no verified target implementation.

**Proposed product role:** Elbrus CPU architecture and platform-support workstream. The initial scope is to establish target-specific ABI/toolchain profiles, image and memory-map validation, linker-layout checks, and a reproducible qualification matrix. No Elbrus CPU model or board is declared supported until exact compiler, linker, emulator, and/or physical-target evidence is recorded.

The repository currently has no verified Elbrus boot path or hardware qualification. Host-side checks and architecture documents must remain separate from cross-build, emulator, and physical-device results.

## Cross-project domain references

- [Reaper-inspired engineering integration notes](docs/REAPER_DOMAIN_INTEGRATION.md)
- [Canonical 50-pattern engineering catalogue in SAMBU](https://github.com/bboroski/SAMBU/blob/main/data/reaper/engineering_patterns_50.tsv)
- [Academic biology glossary in SAMBU](https://github.com/bboroski/SAMBU/blob/main/data/biology/academic_terms_500.tsv)

These references are passive documentation and research vocabulary only. They do not imply that Fragile-Baby implements a runtime, biological model, AI system, hardware controller, or Mass Effect technology.

## Promotion gate

Before implementation, define the repository owner role, supported platforms, public interfaces, threat model, build/test strategy, licensing requirements, and dependency direction. Only then should executable code or ecosystem capabilities be introduced. Any future integration must be versioned, independently testable, and reversible.

## Closed-domain metric and boundary model

- [Project-specific boundary and invariant mapping](docs/CLOSED_DOMAIN_METRIC_INTEGRATION.md)
- [Canonical CDM-1 specification and validator](https://github.com/bboroski/SAMBU/blob/main/docs/CLOSED_DOMAIN_METRIC.md)
