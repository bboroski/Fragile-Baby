# LOVE-50 adapter — Fragile-Baby

**Repository:** `bboroski/Fragile-Baby`  
**Role:** Elbrus/E2K architecture research and platform qualification workstream  
**Status:** SPECIFIED — mapping only; runtime conformance is not implied.  
**Canonical doctrine:** [Klipot LOVE-50](https://github.com/bboroski/Klipot/blob/feat/love-50-chinese-proverbs-20261113/docs/LOVE_50_CHINESE_DOCTRINE.md)

## Why this profile exists

The useful lesson is epistemic honesty: platform support must be earned through target-specific evidence, not inferred from an adjacent architecture or a successful host test.

## Repository-specific application

### Fate / compatibility
Bind every claim to CPU/SoC identity, stepping, ABI, compiler, linker, memory map and board revision.

### Fidelity / trust
Keep evidence source, date, tool versions and exact target configuration with each result. Preserve unknown and pending states.

### Responsiveness / care
Make the evidence advisor identify the next missing qualification step without overstating readiness.

### Harmony / integration
Reuse generic contracts only where E2K ABI and platform evidence confirm compatibility; isolate target-specific adapters.

### Wisdom / restraint
A proposal remains a proposal until cross-build, emulator or physical-target evidence exists. Never copy x86_64 or ARM constants as E2K facts.

## Local verification

- `python -m unittest discover -s tests -v`
- `python tools/evidence_advisor.py`
- `Validate the evidence matrix against its schema.`
- `For promoted statuses, attach exact toolchain, target and reproducible evidence.`

## Non-goals and safety boundaries

- No inferred E2K boot, ABI or compiler support.
- No fabricated hardware evidence or guessed specification values.
- No production-ready claim based only on documentation or host CI.

## Adoption state

This document establishes an interpretation only. A control is IMPLEMENTED only when code/configuration exists, and VERIFIED only when repository-native checks and target-specific evidence pass. Keep unknown, planned, partial and failed states distinct. Existing security, privacy, ABI, platform, licensing and release requirements remain authoritative.

---
*The Chinese expressions are engineering prompts, not claims that software has human emotions.*
