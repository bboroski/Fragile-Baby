# Contributing to Fragile-Baby

Fragile-Baby maintains the NEURO-CORE capability register, evidence advisor, and associated validation contracts. Keep claims traceable to evidence and keep uncertainty visible; do not present generated suggestions as verified facts.

## Required workflow

1. Open or link an Issue and identify affected capability register, schema, evidence source, or validation rule.
2. Use a focused branch: `feat/<topic>`, `fix/<topic>`, `docs/<topic>`, or `security/<topic>`.
3. Version changes to capability IDs, matrix dimensions, and schema fields.
4. Use synthetic/redacted fixtures; never commit private evidence or credentials.
5. Add tests for incomplete, contradictory, stale, and malformed evidence.

## Required validation

```bash
python -m unittest discover -s tests -v
python3 tools/validate_neuro_core.py
```

Run the affected evidence/domain validators from the repository's CI workflows.

## Commits and releases

Use Conventional Commit subjects (`feat:`, `fix:`, `docs:`, `refactor:`, `perf:`, `test:`, `build:`, `ci:`, `chore:`). Breaking changes require `!:` and a `BREAKING CHANGE:` footer. Use SemVer and update registry/schema migration notes before tagging.

## Pull request checklist

- State the evidence source, freshness, and confidence boundary.
- Include exact tests and validator output.
- Preserve traceability and uncertainty.
- Describe how consumers migrate if an identifier or schema changes.
