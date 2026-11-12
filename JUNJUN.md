# Jun-Jun — Fragile-Baby

Jun-Jun is this repository's conservative engineering guardian.

## Project role
Elbrus Architecture & Platform Qualification Workstream

## Mission
Never infer E2K compatibility from host tests; track toolchain, emulator and hardware evidence separately.

## Stage 1: read-only hygiene
The workflow `.github/workflows/jun-jun-guard.yml` runs on pushes, pull requests and manual dispatch. It checks tracked source-like files for common merge-conflict markers and high-confidence private-key / GitHub / AWS credential markers. Reports contain file and line only, never secret values.

## Safety boundaries
Jun-Jun does not modify source, install dependencies, execute project code, access deployment secrets, publish artifacts, merge pull requests or claim build/test/hardware qualification. This stage is observation-only.

## Configuration
See [`.jun-jun/policy.json`](.jun-jun/policy.json). Project-specific checks require verified commands and a separate review. A green Jun-Jun job is a hygiene result, not a security certification.
