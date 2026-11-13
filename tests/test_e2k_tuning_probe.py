from __future__ import annotations

import unittest

from tools.e2k_tuning_probe import (
    ALLOWED_LCC_FLAGS,
    build_report,
    inspect_readelf_header,
    parse_cpuinfo,
)


class E2KTuningProbeTests(unittest.TestCase):
    def test_native_e2k_is_only_a_candidate_not_hardware_qualification(self):
        report = build_report(
            "Linux", "e2k", "6.1.0",
            {"model name": "Elbrus test CPU", "stepping": "A1"},
            "/usr/bin/lcc", "LCC test version", {"readelf": "/usr/bin/readelf"},
        )
        self.assertTrue(report["target_observation"]["native_e2k_linux_candidate"])
        self.assertEqual(report["qualification"]["stage"], "native-runner-candidate")
        self.assertFalse(report["qualification"]["physical_hardware_qualified"])

    def test_non_e2k_host_is_not_promoted(self):
        report = build_report("Linux", "x86_64", "6.8.0", {}, None, None, {})
        self.assertFalse(report["target_observation"]["native_e2k_linux_candidate"])
        self.assertEqual(report["qualification"]["stage"], "host-not-e2k")

    def test_cpuinfo_parser_uses_allowlist_and_ignores_serial(self):
        parsed = parse_cpuinfo(
            "model name : Elbrus sample\nstepping : B2\nSerial : secret\n"
        )
        self.assertEqual(parsed["model name"], "Elbrus sample")
        self.assertEqual(parsed["stepping"], "B2")
        self.assertNotIn("serial", parsed)

    def test_elf_header_accepts_elf64_little_endian_mcst(self):
        header = (
            "  Class:                             ELF64\n"
            "  Data:                              2's complement, little endian\n"
            "  Machine:                           MCST Elbrus\n"
        )
        result = inspect_readelf_header(header)
        self.assertTrue(result["valid"])
        self.assertEqual(result["class"], "ELF64")

    def test_elf_header_rejects_x86(self):
        header = (
            "  Class:                             ELF64\n"
            "  Data:                              2's complement, little endian\n"
            "  Machine:                           Advanced Micro Devices X86-64\n"
        )
        result = inspect_readelf_header(header)
        self.assertFalse(result["valid"])
        self.assertTrue(any("machine" in message.lower() for message in result["errors"]))

    def test_flag_allowlist_does_not_assume_generic_gcc_flags(self):
        self.assertIn("-O4", ALLOWED_LCC_FLAGS)
        self.assertIn("-fprefetch", ALLOWED_LCC_FLAGS)
        self.assertNotIn("-funroll-loops", ALLOWED_LCC_FLAGS)
        self.assertNotIn("-march=native", ALLOWED_LCC_FLAGS)


if __name__ == "__main__":
    unittest.main()
