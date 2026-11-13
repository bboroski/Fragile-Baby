from __future__ import annotations

import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.e2k_repository_inventory import build_inventory, render_markdown, scan_repository


class E2KRepositoryInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.email", "test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.name", "Inventory Test"], check=True)
        (self.root / "src").mkdir()
        (self.root / "src" / "platform.c").write_text(
            '#if defined(__e2k__)\n/* MCST LCC / E2K */\n#endif\n', encoding="utf-8")
        (self.root / "README.md").write_text(
            "Portable arena allocator and cache benchmark; validate on each target.\n", encoding="utf-8")
        (self.root / "opaque.bin").write_bytes(b"\x00\x01\x02binary")
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "fixture"], check=True)

    def tearDown(self):
        self.temp.cleanup()

    def test_hashes_every_tracked_file_and_scans_text(self):
        report = scan_repository("fixture", self.root)
        self.assertEqual(report["counts"]["tracked"], 3)
        self.assertEqual(report["counts"]["text"], 2)
        self.assertEqual(report["counts"]["binary_or_non_utf8"], 1)
        platform = next(item for item in report["files"] if item["path"] == "src/platform.c")
        self.assertTrue(platform["e2k_specific"])
        self.assertIn("compiler-toolchain", platform["domains"])
        self.assertEqual(platform["sha256"], hashlib.sha256((self.root / "src/platform.c").read_bytes()).hexdigest())
        self.assertTrue(platform["hits"])

    def test_portable_candidate_is_not_mislabeled_as_e2k_specific(self):
        report = scan_repository("fixture", self.root)
        readme = next(item for item in report["files"] if item["path"] == "README.md")
        self.assertFalse(readme["e2k_specific"])
        self.assertTrue(readme["portable_candidate"])

    def test_untracked_files_are_excluded_from_git_inventory(self):
        (self.root / "untracked.txt").write_text("E2K not tracked", encoding="utf-8")
        report = scan_repository("fixture", self.root)
        self.assertEqual(report["counts"]["tracked"], 3)
        self.assertNotIn("untracked.txt", {item["path"] for item in report["files"]})

    def test_e2k_marker_is_found_even_after_many_generic_matches(self):
        noisy = self.root / "noisy.txt"
        noisy.write_text("".join("benchmark line\n" for _ in range(40)) + "__e2k__ target marker\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "noisy.txt"], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "noisy fixture"], check=True)
        report = scan_repository("fixture", self.root)
        item = next(entry for entry in report["files"] if entry["path"] == "noisy.txt")
        self.assertTrue(item["e2k_specific"])
        self.assertTrue(any("e2k-marker" in hit["tags"] for hit in item["hits"]))

    def test_multi_repo_summary_and_markdown_are_generated(self):
        report = build_inventory([("fixture", self.root)])
        self.assertEqual(report["repositories_scanned"], 1)
        self.assertEqual(report["totals"]["tracked"], 3)
        markdown = render_markdown(report)
        self.assertIn("E2K-specific files", markdown)
        self.assertIn("src/platform.c", markdown)
        self.assertIn("not certify E2K support", markdown)


if __name__ == "__main__":
    unittest.main()
