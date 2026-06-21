#!/usr/bin/env python3
"""Unit tests for tools/validate-references.py path resolution."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools"))

spec = importlib.util.spec_from_file_location(
    "validate_references",
    REPO_ROOT / "tools" / "validate-references.py",
)
vr = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(vr)

SV = REPO_ROOT / "plugins" / "software-verification" / "skills"


def assert_broken(source: Path, ref: str) -> None:
    assert vr.ref_is_broken(ref, source), f"expected broken: {source} -> {ref!r}"


def assert_not_broken(source: Path, ref: str) -> None:
    assert not vr.ref_is_broken(ref, source), f"expected valid: {source} -> {ref!r}"


def test_skill_cross_skill_relative_path() -> None:
    skill = SV / "detect-ai-smells" / "SKILL.md"
    assert_not_broken(skill, "../design-strategy/references/gate-design-patterns.md")
    assert_broken(skill, "../../design-strategy/references/gate-design-patterns.md")


def test_reference_cross_skill_relative_path() -> None:
    source = SV / "design-strategy" / "references" / "verification-cost-tiers.md"
    assert_not_broken(source, "../../assess-verification/references/bug-surface-routing.md")
    assert_broken(source, "../assess-verification/references/bug-surface-routing.md")


def test_reference_same_skill_relative_path() -> None:
    source = SV / "detect-ai-smells" / "references" / "detection-patterns-gates-formal.md"
    assert_not_broken(source, "../../design-strategy/references/gate-design-patterns.md")


def test_skill_local_reference_path() -> None:
    skill = SV / "detect-ai-smells" / "SKILL.md"
    assert_not_broken(skill, "references/ai-smells-taxonomy.md")


def test_cwd_relative_does_not_use_skill_root_fallback() -> None:
    skill = SV / "detect-ai-smells" / "SKILL.md"
    wrong = "../../design-strategy/references/gate-design-patterns.md"
    candidates = vr.resolve_ref(wrong, skill)
    assert len(candidates) == 1
    assert not candidates[0].exists()


def test_preexisting_cross_plugin_skill_path() -> None:
    skill = REPO_ROOT / "plugins/codebase-ai-readiness/skills/assess-readiness/SKILL.md"
    assert_not_broken(skill, "../generate-roadmap/references/l2-to-l3-hinge.md")


def test_bare_filename_examples_are_not_internal_links() -> None:
    skill = SV / "detect-ai-smells" / "SKILL.md"
    assert not vr.ref_is_internal_link("AGENTS.md")
    assert not vr.ref_is_broken("AGENTS.md", skill)


def main() -> int:
    tests = [
        test_skill_cross_skill_relative_path,
        test_reference_cross_skill_relative_path,
        test_reference_same_skill_relative_path,
        test_skill_local_reference_path,
        test_cwd_relative_does_not_use_skill_root_fallback,
        test_preexisting_cross_plugin_skill_path,
        test_bare_filename_examples_are_not_internal_links,
    ]
    failed = 0
    for test in tests:
        name = test.__name__
        try:
            test()
            print(f"PASS {name}")
        except AssertionError as exc:
            failed += 1
            print(f"FAIL {name}: {exc}")
    print(f"\nReference validator tests: {len(tests) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
