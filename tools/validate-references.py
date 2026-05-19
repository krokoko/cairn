#!/usr/bin/env python3
"""Detect broken links and orphaned reference files across all plugins."""

from __future__ import annotations

import re
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = ROOT / "plugins"

EXT = r"md|py|sh|json|yaml|yml|toml"
INLINE_CODE_RE = re.compile(rf"`([^`]+\.(?:{EXT}))`")
MD_LINK_RE = re.compile(rf"\[(?:[^\]]*)\]\(([^)]+\.(?:{EXT}))\)")
MD_DIR_LINK_RE = re.compile(r"\[(?:[^\]]*)\]\((\.\./[^)]+/)\)")
PLAIN_REF_RE = re.compile(rf"(?<![/\w])(?:\./|\.\./)?references/[^\s`)\]]+\.(?:{EXT})")


def extract_refs(text: str) -> set[str]:
    refs: set[str] = set()
    refs.update(INLINE_CODE_RE.findall(text))
    refs.update(MD_LINK_RE.findall(text))
    refs.update(PLAIN_REF_RE.findall(text))
    for dir_ref in MD_DIR_LINK_RE.findall(text):
        refs.add(dir_ref + "SKILL.md")
    return refs


def find_skill_root(source_file: Path) -> Path | None:
    resolved = source_file.resolve()
    for parent in resolved.parents:
        if parent.parent.name == "skills":
            try:
                parent.relative_to(PLUGINS_DIR)
                return parent
            except ValueError:
                pass
    return None


def is_under_root(resolved: Path) -> bool:
    try:
        resolved.relative_to(ROOT)
        return True
    except ValueError:
        return False


def resolve_ref(ref: str, source_file: Path) -> list[Path]:
    if ref.startswith(("http://", "https://", "mailto:", "#")):
        return []

    candidates: list[Path] = []

    def add(raw: Path) -> None:
        resolved = raw.resolve()
        if is_under_root(resolved) and resolved not in candidates:
            candidates.append(resolved)

    add(source_file.parent / ref)
    skill_root = find_skill_root(source_file)
    if skill_root:
        add(skill_root / ref)
        add(skill_root / "references" / ref)
    return candidates


def collect_all_resource_files() -> set[Path]:
    files: set[Path] = set()
    for refs_dir in PLUGINS_DIR.glob("*/skills/*/references"):
        if refs_dir.is_dir():
            for file_path in refs_dir.rglob("*"):
                if file_path.is_file():
                    files.add(file_path.resolve())
    return files


def collect_entry_points() -> list[Path]:
    return sorted(PLUGINS_DIR.glob("*/skills/*/SKILL.md"))


def main() -> int:
    if not PLUGINS_DIR.is_dir():
        print("WARN: No plugins/ directory found")
        return 0

    all_resources = collect_all_resource_files()
    entry_points = collect_entry_points()
    if not entry_points:
        print("WARN: No SKILL.md entry points found")
        return 0

    reachable: set[Path] = set()
    broken_links: list[tuple[Path, str]] = []
    queue: deque[Path] = deque(entry_points)
    visited: set[Path] = set()

    while queue:
        current = queue.popleft()
        resolved = current.resolve()
        if resolved in visited or not current.exists():
            continue
        visited.add(resolved)

        refs = extract_refs(current.read_text(encoding="utf-8"))
        for ref in refs:
            if "*" in ref or "?" in ref:
                continue
            candidates = resolve_ref(ref, current)
            if not candidates:
                continue
            if not any(path.exists() for path in candidates):
                if "references/" in ref or ref.startswith("references/"):
                    broken_links.append((current, ref))
                continue
            for candidate in candidates:
                if candidate.exists():
                    reachable.add(candidate)
                    if candidate.suffix == ".md" and candidate.resolve() not in visited:
                        queue.append(candidate)

    orphans = all_resources - reachable

    print("Reference Integrity Check")
    print(f"Entry points: {len(entry_points)}, Resource files: {len(all_resources)}\n")

    if broken_links:
        print(f"Broken links ({len(broken_links)}):")
        for source, ref in sorted(broken_links, key=lambda item: (str(item[0]), item[1])):
            print(f"  BROKEN {source.relative_to(ROOT)} -> {ref}")
        print()

    if orphans:
        print(f"Orphaned files ({len(orphans)}):")
        for path in sorted(orphans):
            print(f"  ORPHAN {path.relative_to(ROOT)}")
        print()

    if not broken_links and not orphans:
        print(f"All {len(all_resources)} reference files are reachable. No broken links.\n")

    print(
        f"Summary: {len(all_resources) - len(orphans)}/{len(all_resources)} reachable, "
        f"{len(orphans)} orphaned, {len(broken_links)} broken"
    )
    return 1 if broken_links else 0


if __name__ == "__main__":
    sys.exit(main())
