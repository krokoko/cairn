#!/usr/bin/env python3
"""Independent report examples plus negative controls for portable hook contracts."""

import importlib.util
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).with_name("fixtures")
REPORTS = {
    "readiness-report.md": ("codebase-ai-readiness", "assess-readiness/references/report-template.md"),
    "readiness-roadmap.md": ("codebase-ai-readiness", "generate-roadmap/SKILL.md"),
    "verification-report.md": ("software-verification", "assess-verification/references/report-template.md"),
    "verification-strategy.md": ("software-verification", "design-strategy/references/strategy-report-template.md"),
    "ai-smells-gates-report.md": ("software-verification", "detect-ai-smells/references/ai-smells-gates-report-template.md"),
}


class ReportContracts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cairn report ")
        self.addCleanup(self.temp.cleanup)

    def invoke(self, name, text, hook=False):
        plugin = REPORTS.get(name, ("software-verification", ""))[0]
        scripts = ROOT / "plugins" / plugin / "scripts"
        path = Path(self.temp.name) / name
        path.write_text(text)
        if hook:
            wrapper = "validate-report.sh" if plugin == "codebase-ai-readiness" else "validate-verification-report.sh"
            return subprocess.run(
                ["bash", str(scripts / wrapper)],
                input=json.dumps({"tool_input": {"file_path": str(path)}}),
                text=True, capture_output=True,
            )
        return subprocess.run(
            ["python3", str(scripts / "check-report.py"), "--check", str(path)],
            text=True, capture_output=True,
        )

    def example(self, name="verification-report.md"):
        return (FIXTURES / name).read_text()

    def assertInvalid(self, text, needle, name="verification-report.md"):
        result = self.invoke(name, text)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(needle, result.stdout)

    def test_independently_authored_examples(self):
        for name in REPORTS:
            with self.subTest(name=name):
                result = self.invoke(name, self.example(name))
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("Semantic truth and authorization are not validated", result.stdout)

    def test_contract_and_templates_match_independent_examples(self):
        for name, (plugin, template) in REPORTS.items():
            with self.subTest(name=name):
                root = ROOT / "plugins" / plugin
                contract = json.loads((root / "scripts/report-contracts.json").read_text())[name]
                expected = set(re.findall(r"^## (.+)$", self.example(name), re.M))
                self.assertEqual(set(contract["sections"]), expected)
                text = (root / "skills" / template).read_text()
                actual = set(re.findall(r"^## (.+)$", text, re.M))
                self.assertTrue(expected <= actual, expected - actual)
                for heading, columns in contract.get("tables", {}).items():
                    self.assertIn("| " + " | ".join(columns) + " |", text, heading)
                for field in ("Source revision", "Assessment date", "Inspected scope", "Evidence basis"):
                    self.assertIn(f"**{field}**:", text)

    def test_every_mandatory_section_is_checked(self):
        for name in REPORTS:
            original = self.example(name)
            for heading in re.findall(r"^## (.+)$", original, re.M):
                with self.subTest(name=name, heading=heading):
                    modified = original.replace("## " + heading + "\n", "### Removed " + heading + "\n", 1)
                    self.assertInvalid(modified, "Missing required section", name)

    def test_headings_alone_do_not_pass(self):
        for name in REPORTS:
            text = "\n".join(re.findall(r"^## .+$", self.example(name), re.M))
            self.assertInvalid(text, "substantive", name)

    def test_fenced_or_commented_report_does_not_count(self):
        for text in ("```markdown\n" + self.example() + "\n```", "<!--\n" + self.example() + "\n-->"):
            self.assertInvalid(text, "Missing required section")

    def test_missing_empty_or_placeholder_metadata(self):
        for value in ("", "...", "`...`", "TBD", "[commit/snapshot and relevant uncommitted changes]"):
            text = self.example().replace("**Source revision**: fixture-r2", "**Source revision**: " + value)
            self.assertInvalid(text, "'Source revision'")

    def test_duplicate_section(self):
        self.assertInvalid(self.example() + "\n## Evidence Scope\nAnother scope.\n", "Duplicate required")

    def test_conventional_bold_metadata_punctuation(self):
        text = self.example().replace("**Source revision**:", "**Source revision:**")
        self.assertEqual(self.invoke("verification-report.md", text).returncode, 0)

    def test_no_ledger_rows_or_placeholder_artifact(self):
        text = self.example()
        row = next(line for line in text.splitlines() if line.startswith("| Retry preserves"))
        self.assertInvalid(text.replace(row, ""), "substantive row")
        self.assertInvalid(text.replace("campaign-r2", "..."), "non-placeholder cells")
        self.assertInvalid(text.replace("campaign-r2", "[cited artifact and revision]"), "non-placeholder cells")

    def test_every_ledger_table_is_validated(self):
        ledger = (
            "| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |\n"
            "|---------------|---------------------|-------------|-------------|-----------|------------|--------|\n"
            "| Provider check | provider-r2 | staging | run_inspected | skipped | not_run | All cases skipped |\n"
        )
        text = self.example().replace("## Verification Maturity", "### Provider evidence\n\n" + ledger + "\n## Verification Maturity")
        self.assertEqual(self.invoke("verification-report.md", text).returncode, 0)
        self.assertInvalid(text.replace("| skipped | not_run |", "| skipped | established_within_scope |"), "incompatible")
        self.assertInvalid(text.replace("| Provider check | provider-r2", "| Provider check | ..."), "non-placeholder cells")
        self.assertInvalid(text.replace("| Provider check | provider-r2 | staging | run_inspected | skipped | not_run | All cases skipped |\n", ""), "substantive row")
        self.assertInvalid(text.replace("|---------------|---------------------|-------------|-------------|-----------|------------|--------|\n| Provider", "missing separator\n| Provider"), "missing Markdown table separator")

    def test_table_scaffolding_is_not_substantive(self):
        original = "Retry core is stateful and affects billing; provider adapter needs separate evidence."
        for body in (
            "| Component | Archetype |\n|-----------|-----------|",
            "| Component | Archetype |\n|-----------|-----------|\n| [component] | ... |",
            "**Component**: [name]",
            "**Component:** [name]",
        ):
            self.assertInvalid(self.example().replace(original, body), "Component Breakdown' needs substantive")

    def test_fixed_labels_do_not_complete_assessment_tables(self):
        cases = (
            (
                "ai-smells-gates-report.md",
                "Unused imports have a lint rule; no evidence of semantic assertion quality was inspected.",
                "| Smell | Scoped claim / gate | Coverage status | Enforcement / feedback | Evidence / limits |\n"
                "|-------|---------------------|-----------------|------------------------|-------------------|\n"
                "| AI001: Plausible Fabrication | ... | ... | ... | ... |\n"
                "| AI002: Cargo-Cult Patterns | ... | ... | ... | ... |",
                "Coverage Matrix",
            ),
            (
                "verification-report.md",
                "The local claim is linked and executed; provider scope remains partial.",
                "| Completeness | Evidence / current state | Gap / required review |\n"
                "|--------------|--------------------------|-----------------------|\n"
                "| Links | ... | [missing mappings] |\n"
                "| Execution | ... | [missing evidence] |\n"
                "| Meaning | ... | [unknown review] |",
                "Requirement Traceability",
            ),
        )
        for name, old, body, heading in cases:
            with self.subTest(name=name):
                self.assertInvalid(self.example(name).replace(old, body), f"{heading}' needs substantive", name)

    def test_completed_row_or_prose_cannot_hide_unfilled_assessment_cells(self):
        old = "Retry core is stateful and affects billing; provider adapter needs separate evidence."
        body = (
            "Provider evidence remains inaccessible.\n\n"
            "| Component | State | Limits |\n|-----------|-------|--------|\n"
            "| Core | reviewed | Scoped arithmetic only |\n"
            "| Provider | ... | [qualification limits] |"
        )
        self.assertInvalid(self.example().replace(old, body), "every assessment table row")
        completed = body.replace("| Provider | ... | [qualification limits] |",
                                 "| Provider | unknown | Remote run evidence could not be inspected |")
        self.assertEqual(self.invoke("verification-report.md", self.example().replace(old, completed)).returncode, 0)
        empty = "Provider evidence remains inaccessible.\n\n| Component | State |\n|-----------|-------|\n"
        self.assertInvalid(self.example().replace(old, empty), "assessment table needs a completed row")

    def test_stale_completed_run_can_leave_current_claim_incomplete(self):
        text = self.example().replace("| run_inspected | completed | no_counterexample_found |",
                                      "| stale | completed | incomplete |")
        self.assertEqual(self.invoke("verification-report.md", text).returncode, 0)

    def test_stale_execution_does_not_claim_a_current_execution_result(self):
        for execution in ("completed", "timeout", "interrupted", "skipped", "unsupported", "not_run", "unknown", "not_applicable"):
            for conclusion in ("unknown", "incomplete"):
                with self.subTest(execution=execution, conclusion=conclusion):
                    text = self.example().replace("| run_inspected | completed | no_counterexample_found |",
                                                  f"| stale | {execution} | {conclusion} |")
                    result = self.invoke("verification-report.md", text)
                    self.assertEqual(result.returncode, 0, result.stdout)
        for execution, conclusion in (("skipped", "not_run"), ("unsupported", "unsupported"),
                                      ("not_run", "not_run"), ("not_applicable", "not_applicable")):
            text = self.example().replace("| run_inspected | completed | no_counterexample_found |",
                                          f"| stale | {execution} | {conclusion} |")
            self.assertInvalid(text, "stale evidence requires an unknown or incomplete")

    def test_invalid_and_incompatible_evidence_states(self):
        for old, new in (
            ("| completed |", "| passed |"),
            ("| completed |", "| skipped |"),
            ("| completed |", "| timeout |"),
            ("| run_inspected |", "| configuration_only |"),
            ("| run_inspected |", "| stale |"),
            ("| run_inspected |", "| not_inspectable |"),
            ("| no_counterexample_found |", "| proven_everywhere |"),
        ):
            with self.subTest(new=new):
                self.assertInvalid(self.example().replace(old, new), "Evidence Ledger")

    def test_inconclusive_outcomes_remain_valid(self):
        for execution, conclusion in (
            ("timeout", "unknown"), ("interrupted", "incomplete"),
            ("skipped", "not_run"), ("unsupported", "unsupported"),
            ("not_run", "not_run"), ("unknown", "unknown"),
        ):
            text = self.example().replace("| completed | no_counterexample_found |", f"| {execution} | {conclusion} |")
            result = self.invoke("verification-report.md", text)
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_counterexample_can_survive_interrupted_campaign(self):
        text = self.example().replace("| completed | no_counterexample_found |", "| interrupted | counterexample |")
        self.assertEqual(self.invoke("verification-report.md", text).returncode, 0)

    def test_surface_cannot_exceed_evidence_ceiling(self):
        text = self.example("readiness-report.md").replace("| L3 | L4 | L3 |", "| L5 | L3 | L4 |")
        self.assertInvalid(text, "exceeds", "readiness-report.md")

    def test_unknown_score_and_ceiling_are_preserved(self):
        text = self.example("readiness-report.md").replace("| L3 | L4 | L3 |", "| unknown | unknown | L3 |")
        self.assertEqual(self.invoke("readiness-report.md", text).returncode, 0)
        self.assertInvalid(text.replace("| unknown | unknown | L3 |", "| unknown | unknown | L4 |"), "unknown evidence ceiling", "readiness-report.md")

    def test_l5_needs_all_prerequisites(self):
        text = self.example("readiness-report.md").replace("| L3 | L4 | L3 |", "| L5 | L5 | L5 |")
        for state in ("unknown", "missing", "not_applicable"):
            modified = text.replace("| unknown |", f"| {state} |")
            self.assertInvalid(modified, "all five prerequisites met", "readiness-report.md")
        met = text.replace("| unknown |", "| met |").replace("| missing |", "| met |")
        self.assertEqual(self.invoke("readiness-report.md", met).returncode, 0)

    def test_l4_requires_scoped_intent_and_oracle_evidence(self):
        text = self.example("readiness-report.md").replace("| L3 | L4 | L3 |", "| L4 | L4 | L4 |")
        for gate in ("L4-INTENT", "L4-ORACLES"):
            for status in ("missing", "unknown", "not_applicable"):
                with self.subTest(gate=gate, status=status):
                    modified = text.replace(f"| {gate} | met |", f"| {gate} | {status} |")
                    self.assertInvalid(modified, "ceiling is L3", "readiness-report.md")

    def test_l4_does_not_require_complete_l5_coverage(self):
        text = self.example("readiness-report.md").replace("| L3 | L4 | L3 |", "| L4 | L4 | L4 |")
        text = text.replace("**Level**: L3", "**Level**: L4")
        for gate in ("L5-INTENT", "L5-ORACLES", "L5-ENVIRONMENT"):
            text = text.replace(f"| {gate} | met |", f"| {gate} | unknown |")
        result = self.invoke("readiness-report.md", text)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_summary_is_explicit_and_bounded_by_every_assessed_surface(self):
        text = self.example("readiness-report.md")
        self.assertInvalid(text.replace("**Level**: L3", "**Level**: L5"), "exceeds an assessed surface", "readiness-report.md")
        for value in ("", "L3 for core", "L3 for core; L1 for provider"):
            self.assertInvalid(text.replace("**Level**: L3", "**Level**: " + value), "one '**Level**", "readiness-report.md")
        self.assertInvalid(text.replace("**Level**: L3", "L3 for core"), "one '**Level**", "readiness-report.md")
        second = "| provider | L1 | L1 | L1 | Proposal only | Evidence unavailable |\n"
        text = text.replace("| core | L3 | L4 | L3 | Pure function changes with reviewed acceptance criteria | Production recovery evidence absent |\n",
                            "| core | L3 | L4 | L3 | Pure function changes with reviewed acceptance criteria | Production recovery evidence absent |\n" + second)
        gates = "\n".join(f"| provider | {gate} | unknown | Provider evidence unavailable |" for gate in
                          ("L4-INTENT", "L4-ORACLES", "L5-INTENT", "L5-ORACLES", "L5-ENVIRONMENT", "L5-DETECTION", "L5-RECOVERY"))
        last = "| core | L5-RECOVERY | missing | No documented package version rollback |"
        text = text.replace(last, last + "\n" + gates)
        self.assertInvalid(text, "exceeds an assessed surface", "readiness-report.md")
        result = self.invoke("readiness-report.md", text.replace("**Level**: L3", "**Level**: L1"))
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_missing_duplicate_or_mismatched_prerequisites(self):
        text = self.example("readiness-report.md")
        for modified in (
            text.replace("L5-RECOVERY", "L5-DETECTION"),
            text.replace("| core | L5-RECOVERY", "| nonexistent | L5-RECOVERY"),
        ):
            self.assertInvalid(modified, "Autonomy Prerequisites", "readiness-report.md")

    def test_hook_feedback_is_json_and_advisory(self):
        for name in REPORTS:
            result = self.invoke(name, "## Evidence Scope\nIncomplete.\n", hook=True)
            self.assertEqual(result.returncode, 0)
            self.assertIn("Report validation failed", json.loads(result.stdout)["systemMessage"])
        result = self.invoke("notes.md", "Unrelated notes.", hook=True)
        self.assertEqual(result.stdout, "")

    def test_hook_malformed_event_is_safe_json(self):
        for plugin in ("codebase-ai-readiness", "software-verification"):
            engine = ROOT / "plugins" / plugin / "scripts/check-report.py"
            for event in ('{"broken": "quote\\n', '[]', '{"tool_input": []}'):
                result = subprocess.run(["python3", str(engine)], input=event, text=True, capture_output=True)
                self.assertEqual(result.returncode, 0)
                self.assertIn("could not complete", json.loads(result.stdout)["systemMessage"])

    def test_plugins_are_standalone(self):
        # Packaging copies are deliberate: neither hook imports the other plugin.
        self.assertEqual(
            (ROOT / "plugins/codebase-ai-readiness/scripts/check-report.py").read_bytes(),
            (ROOT / "plugins/software-verification/scripts/check-report.py").read_bytes(),
        )
        for plugin in ("codebase-ai-readiness", "software-verification"):
            root = ROOT / "plugins" / plugin / "scripts"
            spec = importlib.util.spec_from_file_location(plugin, root / "check-report.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            contracts = json.loads((root / "report-contracts.json").read_text())
            for name in contracts:
                self.assertEqual(module.validate(FIXTURES / name, contracts), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
