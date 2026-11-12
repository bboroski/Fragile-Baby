"""Evidence-gated chronology for staged E2K platform qualification."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Sequence

STAGE_ORDER = ("host", "cross-build", "emulator", "physical-target")
STAGE_TO_MATURITY = {
    "architecture-proposal": 0,
    "host-observed": 1,
    "cross-build-observed": 2,
    "emulator-observed": 3,
    "hardware-qualified": 4,
}
VALID_STATUSES = {"passed", "failed", "blocked", "unknown", "not-tested"}


def _time(value: Any) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("observed_at must be a non-empty ISO-8601 timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("observed_at must include a UTC offset")
    return parsed


def analyze_qualification_timeline(
    records: Sequence[dict[str, Any]], maturity_claim: str = "architecture-proposal"
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    by_stage: dict[str, list[dict[str, Any]]] = {stage: [] for stage in STAGE_ORDER}
    seen_evidence: set[str] = set()
    normalized: list[tuple[datetime, int, dict[str, Any]]] = []

    if maturity_claim not in STAGE_TO_MATURITY:
        errors.append("unsupported maturity_claim")
        claim_rank = 0
    else:
        claim_rank = STAGE_TO_MATURITY[maturity_claim]

    for index, item in enumerate(records):
        if not isinstance(item, dict):
            errors.append(f"records[{index}] must be an object")
            continue
        stage, status = item.get("stage"), item.get("status")
        if stage not in by_stage:
            errors.append(f"records[{index}] has unsupported stage")
            continue
        if status not in VALID_STATUSES:
            errors.append(f"records[{index}] has unsupported status")
            continue
        evidence_id = item.get("evidence_id")
        if status == "passed" and (not isinstance(evidence_id, str) or not evidence_id.strip()):
            errors.append(f"{stage}: passed evidence requires evidence_id")
        if isinstance(evidence_id, str) and evidence_id:
            if evidence_id in seen_evidence:
                errors.append(f"duplicate evidence_id: {evidence_id}")
            seen_evidence.add(evidence_id)
        try:
            when = _time(item.get("observed_at"))
        except (TypeError, ValueError) as exc:
            errors.append(f"{stage}: {exc}")
            continue
        by_stage[stage].append(item)
        normalized.append((when, STAGE_ORDER.index(stage), item))

    normalized.sort(key=lambda row: row[0])
    last_stage_rank = -1
    for _, rank, item in normalized:
        if item.get("status") != "passed":
            continue
        if rank < last_stage_rank:
            errors.append("passed qualification stages regress in observation time")
        last_stage_rank = max(last_stage_rank, rank)

    passed = [stage for stage in STAGE_ORDER
              if any(item.get("status") == "passed" for item in by_stage[stage])]
    contiguous_rank = 0
    for stage in STAGE_ORDER:
        if any(item.get("status") == "passed" for item in by_stage[stage]):
            contiguous_rank += 1
        else:
            break
    for index, stage in enumerate(STAGE_ORDER):
        if any(item.get("status") == "passed" for item in by_stage[stage]) and index >= contiguous_rank:
            warnings.append(f"{stage} evidence is present but earlier stage gates are incomplete")
    next_stage = STAGE_ORDER[contiguous_rank] if contiguous_rank < len(STAGE_ORDER) else None
    achieved = ("architecture-proposal", "host-observed", "cross-build-observed",
                "emulator-observed", "hardware-qualified")[contiguous_rank]
    claim_allowed = claim_rank <= contiguous_rank and not errors
    if not claim_allowed:
        warnings.append("claimed maturity exceeds the contiguous, evidenced qualification path")
    coverage = round(100 * contiguous_rank / len(STAGE_ORDER))
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "passed_stages": passed,
        "contiguous_stage_count": contiguous_rank,
        "coverage_percent": coverage,
        "achieved_maturity": achieved,
        "claim_allowed": claim_allowed,
        "next_stage": next_stage,
        "next_action": f"collect independently reviewable {next_stage} evidence" if next_stage else "maintain target evidence",
    }
