# Fragile-Baby engineering promotion gate

**Current state:** placeholder / integration-reference scaffold. The repository has no defined product role, executable module, public API, platform target or tests.

This gate converts uncertainty into an explicit backlog instead of inventing capabilities.

## Required decisions

1. **Product boundary:** one-sentence purpose, primary operator and non-goals.
2. **Domain owner:** canonical component name, repository owner and upstream/downstream interfaces.
3. **Execution model:** language, runtime, deployment target and resource limits.
4. **State model:** lifecycle stages, evidence markers, failure states and recovery policy.
5. **Data model:** versioned schemas, provenance, integrity checks and retention rules.
6. **Automation:** allowed read-only operations, bounded retries and actions requiring explicit operator approval.
7. **Physical interface:** only if applicable, specify units, calibration source, safe envelope, interlocks and hardware-in-the-loop evidence.
8. **Verification:** unit, property, compatibility, integration and target qualification tests.

## Design constraints once promoted

Prefer one orchestration/control surface over a forced monolith. Keep domain modules independently testable. Any animation must be a projection of a recorded state marker, never a substitute for sensor evidence. Any physical-law function must name units, assumptions and valid input ranges.

Until these decisions are approved, the repository is intentionally not registered as an executable ecosystem module.
