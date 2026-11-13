#!/usr/bin/env python3
"""Create a byte-level inventory and evidence map for local Git repositories.

The scanner is deliberately offline and read-only. It hashes every tracked Git
entry, scans UTF-8 text files line by line, and records the exact lines that
justify E2K-related classifications. It does not build, execute, or certify code.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "fragile-baby.e2k-repository-inventory.v1"
MAX_HITS_PER_FILE = 24
MAX_SNIPPET_CHARS = 240

E2K_MARKERS = re.compile(
    r"(?i)(?<![a-z0-9_])e2k(?![a-z0-9_])|elbrus|EM_MCST_ELBRUS|__e2k__|"
    r"MCST\s+LCC|\bqemu[-_]e2k\b"
)
DOMAIN_PATTERNS: dict[str, re.Pattern[str]] = {
    "compiler-toolchain": re.compile(r"(?i)\blcc\b|mcst.{0,20}(compiler|toolchain)|toolchain|sysroot|CMAKE_C_COMPILER|E2K_CC"),
    "abi-elf-binary": re.compile(r"(?i)\bELF\b|e_machine|EM_MCST_ELBRUS|calling convention|\bABI\b|linker|relocation"),
    "platform-runtime": re.compile(r"(?i)platform|uname|clock_gettime|runtime|\bBSP\b|architecture detection|__e2k__"),
    "boot-kernel-firmware": re.compile(r"(?i)bootloader|firmware|\bPNS\b|kernel|interrupt|exception|memory map|entry point|limine"),
    "memory-data-layout": re.compile(r"(?i)memory|allocator|arena|cache|alignment|prefetch|stride|vector|SIMD|working set"),
    "performance-measurement": re.compile(r"(?i)benchmark|performance|throughput|latency|profil(e|ing)|PMU|cycle counter|perf stat"),
    "concurrency-synchronization": re.compile(r"(?i)thread|concurren|atomic|mutex|lock|scheduler|affinity|false sharing"),
    "correctness-tests": re.compile(r"(?i)test|assert|fixture|regression|golden|checksum|invariant"),
    "ci-build-automation": re.compile(r"(?i)github actions|workflow|cmake|makefile|\bCI\b|pipeline|build system"),
    "security-provenance": re.compile(r"(?i)sha-?256|signature|provenance|reproducible|supply chain|artifact digest|attestation"),
}
PORTABLE_DOMAINS = {
    "memory-data-layout",
    "performance-measurement",
    "concurrency-synchronization",
    "correctness-tests",
}


def _run_git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout.decode("utf-8", errors="replace").strip()


def _tracked_entries(root: Path) -> list[tuple[str, str, str]]:
    """Return (mode, git_blob_or_commit_sha, path) from the index."""
    raw = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--stage", "-z"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout
    entries: list[tuple[str, str, str]] = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        try:
            metadata, raw_path = record.split(b"\t", 1)
            mode, blob_sha, _stage = metadata.decode("ascii").split()
            path = os.fsdecode(raw_path)
        except (ValueError, UnicodeError):
            continue
        entries.append((mode, blob_sha, path))
    return sorted(entries, key=lambda item: item[2].casefold())


def _safe_file_bytes(root: Path, relative: str) -> tuple[str, bytes | None]:
    path = root / relative
    try:
        if path.is_symlink():
            return "symlink", os.fsencode(os.readlink(path))
        resolved = path.resolve(strict=True)
        if os.path.commonpath((str(root.resolve()), str(resolved))) != str(root.resolve()):
            return "blocked-path", None
        if not resolved.is_file():
            return "non-file", None
        return "file", resolved.read_bytes()
    except FileNotFoundError:
        return "missing", None
    except OSError:
        return "unreadable", None


def _scan_text(content: str) -> tuple[bool, list[str], list[dict[str, Any]]]:
    domains: set[str] = set()
    hits: list[dict[str, Any]] = []
    e2k_specific = False
    for line_no, line in enumerate(content.splitlines(), start=1):
        marker = bool(E2K_MARKERS.search(line))
        if marker:
            e2k_specific = True
            if "e2k-marker" not in domains:
                domains.add("e2k-marker")
        line_domains = [name for name, pattern in DOMAIN_PATTERNS.items() if pattern.search(line)]
        domains.update(line_domains)
        if marker or line_domains:
            hit = {
                "line": line_no,
                "tags": (["e2k-marker"] if marker else []) + line_domains,
                "snippet": line.strip()[:MAX_SNIPPET_CHARS],
            }
            if marker and len(hits) >= MAX_HITS_PER_FILE:
                # Preserve at least one exact E2K anchor even in a very noisy file.
                if not any("e2k-marker" in prior["tags"] for prior in hits):
                    hits[-1] = hit
            elif len(hits) < MAX_HITS_PER_FILE:
                hits.append(hit)
    return e2k_specific, sorted(domains), hits


def scan_repository(name: str, repo_path: str | Path) -> dict[str, Any]:
    root = Path(repo_path).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"repository path is not a directory: {root}")
    try:
        commit = _run_git(root, "rev-parse", "HEAD")
        branch = _run_git(root, "branch", "--show-current") or "detached"
        working_tree_clean = not bool(_run_git(root, "status", "--porcelain", "--untracked-files=no"))
        entries = _tracked_entries(root)
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"not a readable Git worktree: {root} ({detail})") from exc

    files: list[dict[str, Any]] = []
    counts = {"tracked": 0, "text": 0, "binary_or_non_utf8": 0, "missing": 0,
              "submodules": 0, "e2k_specific": 0, "portable_candidate": 0}
    total_bytes = 0

    for mode, git_object, relative in entries:
        counts["tracked"] += 1
        if mode == "160000":
            counts["submodules"] += 1
            pointer = f"git-submodule:{git_object}".encode("ascii")
            files.append({
                "path": relative, "entry_type": "submodule", "git_object": git_object,
                "size_bytes": 0, "sha256": hashlib.sha256(pointer).hexdigest(),
                "text_scanned": False, "e2k_specific": False, "portable_candidate": False,
                "domains": ["submodule-reference"], "hits": [],
            })
            continue

        entry_type, payload = _safe_file_bytes(root, relative)
        if payload is None:
            counts["missing"] += 1
            files.append({
                "path": relative, "entry_type": entry_type, "git_object": git_object,
                "size_bytes": 0, "sha256": None, "text_scanned": False,
                "e2k_specific": False, "portable_candidate": False,
                "domains": [], "hits": [],
            })
            continue

        total_bytes += len(payload)
        digest = hashlib.sha256(payload).hexdigest()
        try:
            text = None if b"\0" in payload else payload.decode("utf-8")
        except UnicodeDecodeError:
            text = None

        if text is None or entry_type != "file":
            counts["binary_or_non_utf8"] += 1
            files.append({
                "path": relative, "entry_type": entry_type if entry_type != "file" else "binary-or-non-utf8",
                "git_object": git_object, "size_bytes": len(payload), "sha256": digest,
                "text_scanned": False, "e2k_specific": False, "portable_candidate": False,
                "domains": [], "hits": [],
            })
            continue

        counts["text"] += 1
        e2k_specific, domains, hits = _scan_text(text)
        portable_candidate = bool(set(domains) & PORTABLE_DOMAINS) and not e2k_specific
        if e2k_specific:
            counts["e2k_specific"] += 1
        if portable_candidate:
            counts["portable_candidate"] += 1
        files.append({
            "path": relative, "entry_type": "text", "git_object": git_object,
            "size_bytes": len(payload), "sha256": digest,
            "text_scanned": True, "line_count": len(text.splitlines()),
            "e2k_specific": e2k_specific, "portable_candidate": portable_candidate,
            "domains": domains, "hits": hits,
        })

    return {
        "name": name,
        "path": str(root),
        "commit": commit,
        "branch": branch,
        "working_tree_clean": working_tree_clean,
        "counts": counts,
        "tracked_bytes": total_bytes,
        "files": files,
    }


def build_inventory(repositories: list[tuple[str, str | Path]]) -> dict[str, Any]:
    scanned = [scan_repository(name, path) for name, path in repositories]
    totals = {
        key: sum(repo["counts"][key] for repo in scanned)
        for key in ("tracked", "text", "binary_or_non_utf8", "missing", "submodules", "e2k_specific", "portable_candidate")
    }
    totals["tracked_bytes"] = sum(repo["tracked_bytes"] for repo in scanned)
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "scanner": "Fragile-Baby tools/e2k_repository_inventory.py",
        "mode": "offline-read-only-git-tracked-files",
        "repositories_scanned": len(scanned),
        "totals": totals,
        "repositories": scanned,
        "limitations": [
            "The path list comes from the Git index; hashes and text scans use current worktree bytes. working_tree_clean records tracked-file cleanliness; untracked and ignored files are excluded.",
            "All tracked regular-file bytes are SHA-256 hashed. UTF-8 text is scanned line by line; binary and non-UTF-8 files are hashed but not text-interpreted.",
            "Submodules are recorded by gitlink commit only; their contents require separately supplied local clones.",
            "At most 24 representative evidence lines are retained per file; all text lines are still scanned for classification tags.",
            "Classification is lexical evidence triage, not semantic proof, compiler validation, execution proof, or hardware qualification.",
            "Portable-candidate means a potentially reusable domain, not that the source is already E2K-compatible or faster on E2K.",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# E2K cross-repository source inventory",
        "",
        f"- Schema: `{report['schema_version']}`",
        f"- Generated (UTC): `{report['generated_at_utc']}`",
        f"- Mode: `{report['mode']}`",
        f"- Repositories: **{report['repositories_scanned']}**",
        f"- Tracked entries: **{report['totals']['tracked']}**; text files scanned: **{report['totals']['text']}**; binary/non-UTF-8: **{report['totals']['binary_or_non_utf8']}**",
        f"- E2K-specific text files: **{report['totals']['e2k_specific']}**; portable candidates: **{report['totals']['portable_candidate']}**",
        "",
        "> This report inventories source evidence. It does not certify E2K support or performance.",
        "",
        "## Repository summaries",
        "",
        "| Repository | Commit | Tracked | Text scanned | E2K-specific | Portable candidates | Bytes |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for repo in report["repositories"]:
        c = repo["counts"]
        lines.append(
            f"| {repo['name']} | `{repo['commit'][:12]}` | {c['tracked']} | {c['text']} | {c['e2k_specific']} | {c['portable_candidate']} | {repo['tracked_bytes']} |"
        )
    lines.extend(["", "## E2K-specific files", ""])
    for repo in report["repositories"]:
        relevant = [item for item in repo["files"] if item["e2k_specific"]]
        if not relevant:
            continue
        lines.extend([f"### {repo['name']}", ""])
        for item in relevant:
            lines.append(f"- `{item['path']}` — SHA-256 `{item['sha256']}`; tags: {', '.join(item['domains']) or 'none'}")
            for hit in item["hits"][:4]:
                lines.append(f"  - L{hit['line']}: `{hit['snippet'].replace('`', '\\`')}`")
        lines.append("")
    lines.extend(["## Portable candidate files", ""])
    for repo in report["repositories"]:
        relevant = [item for item in repo["files"] if item["portable_candidate"]]
        if not relevant:
            continue
        lines.extend([f"### {repo['name']}", ""])
        for item in relevant:
            lines.append(f"- `{item['path']}` — {', '.join(item['domains'])}")
        lines.append("")
    lines.extend(["## Limitations", ""])
    lines.extend(f"- {item}" for item in report["limitations"])
    lines.append("")
    return "\n".join(lines)


def parse_repo_arg(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("repository must use NAME=PATH")
    name, path = value.split("=", 1)
    if not name.strip() or not path.strip():
        raise argparse.ArgumentTypeError("repository name and path must be non-empty")
    return name.strip(), path.strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", action="append", type=parse_repo_arg, required=True,
                        metavar="NAME=PATH", help="local Git clone; repeat for each repository")
    parser.add_argument("--output-json", type=Path, help="write complete SHA-256 inventory JSON")
    parser.add_argument("--output-markdown", type=Path, help="write human-readable evidence summary")
    args = parser.parse_args(argv)
    try:
        report = build_inventory(args.repo)
        if args.output_json:
            args.output_json.parent.mkdir(parents=True, exist_ok=True)
            args.output_json.write_text(json.dumps(report, ensure_asckii=False, indent=2) + "\n", encoding="utf-8")
        if args.output_markdown:
            args.output_markdown.parent.mkdir(parents=True, exist_ok=True)
            args.output_markdown.write_text(render_markdown(report), encoding="utf-8")
        if not args.output_json and not args.output_markdown:
            print(json.dumps(report, ensure_asckii=False, indent=2))
        else:
            print(f"Inventoried {report['repositories_scanned']} repositories / {report['totals']['tracked']} tracked entries")
            print(f"E2K-specific: {report['totals']['e2k_specific']}; portable candidates: {report['totals']['portable_candidate']}")
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"e2k-repository-inventory: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
