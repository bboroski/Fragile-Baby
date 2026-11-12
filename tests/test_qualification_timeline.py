import unittest

from tools.qualification_timeline import analyze_qualification_timeline


class QualificationTimelineTests(unittest.TestCase):
    def record(self, stage, date, evidence):
        return {"stage": stage, "status": "passed", "observed_at": date,
                "evidence_id": evidence}

    def test_progress_is_contiguous_and_evidence_backed(self):
        records = [
            self.record("host", "2026-01-01T10:00:00Z", "host-run-1"),
            self.record("cross-build", "2026-01-02T10:00:00Z", "cross-run-1"),
        ]
        result = analyze_qualification_timeline(records, "cross-build-observed")
        self.assertTrue(result["valid"])
        self.assertTrue(result["claim_allowed"])
        self.assertEqual(result["next_stage"], "emulator")
        self.assertEqual(result["coverage_percent"], 50)

    def test_hardware_claim_cannot_skip_emulator(self):
        records = [
            self.record("host", "2026-01-01T10:00:00Z", "host-1"),
            self.record("physical-target", "2026-01-02T10:00:00Z", "board-1"),
        ]
        result = analyze_qualification_timeline(records, "hardware-qualified")
        self.assertFalse(result["claim_allowed"])
        self.assertTrue(any("gates are incomplete" in x for x in result["warnings"]))

    def test_pass_requires_evidence_and_timezone(self):
        records = [{"stage": "host", "status": "passed",
                    "observed_at": "2026-01-01T10:00:00", "evidence_id": ""}]
        result = analyze_qualification_timeline(records, "host-observed")
        self.assertFalse(result["valid"])
        self.assertTrue(any("evidence_id" in x for x in result["errors"]))
        self.assertTrue(any("UTC offset" in x for x in result["errors"]))


if __name__ == "__main__":
    unittest.main()
