#!/usr/bin/env python3
"""Regression tests for retained evaluation integrity, not semantic judgments."""

import contextlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("evaluate_skills", ROOT / "tools/evaluate-skills.py")
evaluation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluation)


class EvaluationIdentity(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        previous = evaluation.ROOT, evaluation.CASES, evaluation.RUBRIC
        self.addCleanup(lambda: setattr(evaluation, "ROOT", previous[0]))
        self.addCleanup(lambda: setattr(evaluation, "CASES", previous[1]))
        self.addCleanup(lambda: setattr(evaluation, "RUBRIC", previous[2]))
        evaluation.ROOT = self.root / "live"
        evaluation.ROOT.mkdir()
        evaluation.CASES = evaluation.ROOT / "cases.json"
        evaluation.RUBRIC = evaluation.ROOT / "rubric.json"
        evaluation.write_json(evaluation.CASES, {"version": 1, "cases": [{
            "id": "example", "skill": "assess-verification", "prompt": "Assess this snapshot.",
            "files": {"snapshot.json": '{"source_revision":"r1"}', "nested/input.txt": "supplied evidence"},
        }]})
        evaluation.write_json(evaluation.RUBRIC, {"version": 1, "cases": {
            "example": {"criteria": {"scope": "Recognizes the declared local scope."}},
        }})
        self.skill_relative = "plugins/software-verification/skills/assess-verification/SKILL.md"
        self.skill = evaluation.ROOT / self.skill_relative
        self.skill.parent.mkdir(parents=True)
        self.skill.write_bytes(b"# Frozen skill\r\nPreserve these exact bytes.\r\n")
        self.run = self.root / "results/run"
        self.prepared = self.root / "prepared"
        with contextlib.redirect_stdout(io.StringIO()):
            evaluation.snapshot(self.run)
            evaluation.prepare("example", self.prepared, self.run)
        (self.prepared / "repository/report.md").write_text("Synthetic recorded report for the identity test.")
        entry = io.StringIO()
        with contextlib.redirect_stdout(entry):
            evaluation.retain_case("example", self.prepared, self.run, "report.md")
        recorded_case = json.loads(entry.getvalue())
        recorded_case["criteria"] = {
            "scope": {"status": "pass", "evidence": "Synthetic expected adjudication."},
        }
        self.result = {
            "schema_version": 2, "provenance": "retained_source",
            "run_id": "identity-test", "date": "2026-10-11", "source_revision": "synthetic-r1",
            **{key: value for key, value in evaluation.read_json(self.run / "snapshot.json").items() if key != "version"},
            "model": "not invoked", "configuration": "synthetic validator test", "adjudicator": "test fixture",
            "limitations": "Exercises record validation, not model reasoning.",
            "cases": {"example": recorded_case},
        }

    def check(self, integrity_only=False):
        path = self.run / "results.json"
        evaluation.write_json(path, self.result)
        with contextlib.redirect_stdout(io.StringIO()):
            return evaluation.check_results(path, integrity_only=integrity_only)

    def commit_source(self):
        commands = [
            ["init", "--quiet"],
            ["add", "plugins"],
            ["-c", "user.name=Evaluation Test", "-c", "user.email=evaluation@example.invalid",
             "commit", "--quiet", "-m", "Preserve synthetic evaluated source"],
        ]
        for command in commands:
            subprocess.run(["git", "-C", str(evaluation.ROOT), *command], check=True, capture_output=True)
        return subprocess.check_output(["git", "-C", str(evaluation.ROOT), "rev-parse", "HEAD"],
                                       text=True).strip()

    def use_git_provenance(self, revision):
        identity = evaluation.read_json(self.run / "snapshot.json")
        identity.update(provenance="git_revision", source_revision=revision)
        evaluation.write_json(self.run / "snapshot.json", identity)
        (self.run / "source.json").unlink()
        self.result.update(provenance="git_revision", source_revision=revision)

    def test_matching_record(self):
        self.assertEqual(self.check(), 0)

    def test_changed_retained_criterion_text_invalidates_record(self):
        path = self.run / "rubric.json"
        rubric = evaluation.read_json(path)
        rubric["cases"]["example"]["criteria"]["scope"] = "Requires representative deployed evidence."
        evaluation.write_json(path, rubric)
        with self.assertRaisesRegex(ValueError, "Rubric digest mismatch"):
            self.check()

    def test_changed_retained_catalog_invalidates_record(self):
        path = self.run / "cases.json"
        data = evaluation.read_json(path)
        data["cases"][0]["files"]["snapshot.json"] = '{"source_revision":"r2"}'
        evaluation.write_json(path, data)
        with self.assertRaisesRegex(ValueError, "Fixture digest mismatch"):
            self.check()

    def test_live_source_and_catalog_changes_do_not_change_frozen_run(self):
        self.skill.write_text("Changed live skill.")
        evaluation.CASES.write_text("{}")
        evaluation.RUBRIC.write_text("{}")
        other = self.root / "later-preparation"
        with contextlib.redirect_stdout(io.StringIO()):
            evaluation.prepare("example", other, self.run)
        self.assertEqual((other / "source" / self.skill_relative).read_bytes(),
                         b"# Frozen skill\r\nPreserve these exact bytes.\r\n")
        self.assertNotIn(str(evaluation.ROOT), (other / "TASK.txt").read_text())
        self.assertEqual(self.check(), 0)

    def test_git_revision_replays_committed_source_despite_live_changes(self):
        revision = self.commit_source()
        self.skill.write_text("Uncommitted changes must not enter this evaluation.")
        run = self.root / "git-run"
        prepared = self.root / "git-prepared"
        with contextlib.redirect_stdout(io.StringIO()):
            evaluation.snapshot(run, revision)
            evaluation.prepare("example", prepared, run)
        identity = evaluation.read_json(run / "snapshot.json")
        self.assertEqual(identity["provenance"], "git_revision")
        self.assertEqual(identity["source_revision"], revision)
        self.assertFalse((run / "source.json").exists())
        self.assertEqual((prepared / "source" / self.skill_relative).read_bytes(),
                         b"# Frozen skill\r\nPreserve these exact bytes.\r\n")

    def test_git_replacement_refs_do_not_redefine_recorded_source(self):
        original = self.commit_source()
        self.skill.write_text("A different skill in a later commit.")
        replacement = self.commit_source()
        subprocess.run(["git", "-C", str(evaluation.ROOT), "replace", original, replacement],
                       check=True, capture_output=True)
        self.use_git_provenance(original)
        self.assertEqual(self.check(), 0)
        self.assertEqual(evaluation.git_source_files(original)[self.skill_relative],
                         "# Frozen skill\r\nPreserve these exact bytes.\r\n")

    def test_default_snapshot_remains_standalone_in_git_checkout(self):
        self.commit_source()
        run = self.root / "standalone-run"
        with contextlib.redirect_stdout(io.StringIO()):
            evaluation.snapshot(run)
        self.assertEqual(evaluation.read_json(run / "snapshot.json")["provenance"], "retained_source")
        self.assertTrue((run / "source.json").is_file())

    def test_git_revision_result_binds_source_bytes_and_revision(self):
        revision = self.commit_source()
        self.use_git_provenance(revision)
        self.assertEqual(self.check(), 0)
        self.result["source_revision"] = "f" * 40
        with self.assertRaisesRegex(ValueError, "Git revision differs"):
            self.check()
        self.result["source_revision"] = revision
        identity = evaluation.read_json(self.run / "snapshot.json")
        identity["implementation_sha256"] = "0" * 64
        evaluation.write_json(self.run / "snapshot.json", identity)
        with self.assertRaisesRegex(ValueError, "Implementation digest mismatch"):
            self.check()

    def test_unavailable_git_source_is_explicitly_incomplete_and_report_integrity_still_checked(self):
        self.use_git_provenance("0" * 40)
        with self.assertRaisesRegex(evaluation.SourceUnavailable, "unavailable locally"):
            self.check()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(evaluation.check_archives(self.run.parent), 0)
        self.assertIn("source provenance incomplete", output.getvalue())
        self.assertIn("No history was fetched", output.getvalue())
        self.assertNotIn("Source and artifact integrity checked", output.getvalue())
        self.assertIn("No retained run records complete passing adjudications with source provenance",
                      output.getvalue())
        (self.run / "cases/example/report.md").write_text("Changed report while source is absent.")
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, "Report digest mismatch"):
                evaluation.check_archives(self.run.parent)
        with self.assertRaises(evaluation.SourceUnavailable):
            evaluation.prepare("example", self.root / "cannot-prepare", self.run)

    def test_git_revision_requires_a_full_sha(self):
        with self.assertRaisesRegex(ValueError, "requires a full commit SHA"):
            evaluation.snapshot(self.root / "short-revision", "HEAD")

    def test_changed_report_invalidates_adjudication(self):
        (self.run / "cases/example/report.md").write_text("A different conclusion.")
        with self.assertRaisesRegex(ValueError, "Report digest mismatch"):
            self.check()

    def test_empty_and_missing_reports_rejected(self):
        report = self.run / "cases/example/report.md"
        report.write_text("")
        with self.assertRaisesRegex(ValueError, "Empty assessment"):
            self.check()
        report.unlink()
        with self.assertRaisesRegex(ValueError, "Missing artifact"):
            self.check()

    def test_changed_and_missing_retained_input_rejected(self):
        fixture = self.run / "cases/example/nested/input.txt"
        fixture.write_text("Changed evidence")
        with self.assertRaisesRegex(ValueError, "Input digest mismatch"):
            self.check()
        fixture.unlink()
        with self.assertRaisesRegex(ValueError, "Missing artifact"):
            self.check()

    def test_input_digest_cannot_replace_catalog_content(self):
        fixture = self.run / "cases/example/nested/input.txt"
        fixture.write_text("Changed evidence")
        self.result["cases"]["example"]["input_sha256"]["nested/input.txt"] = evaluation.digest(fixture)
        with self.assertRaisesRegex(ValueError, "Input digest mismatch"):
            self.check()

    def test_missing_input_inventory_rejected(self):
        del self.result["cases"]["example"]["input_sha256"]["nested/input.txt"]
        with self.assertRaisesRegex(ValueError, "Incomplete input inventory"):
            self.check()

    def test_changed_and_missing_frozen_source_rejected(self):
        source = self.run / "source.json"
        data = evaluation.read_json(source)
        data["files"][self.skill_relative] = "Changed retained skill."
        evaluation.write_json(source, data)
        with self.assertRaisesRegex(ValueError, "Implementation digest mismatch"):
            self.check()
        source.unlink()
        with self.assertRaisesRegex(ValueError, "Missing artifact"):
            self.check()

    def test_result_identity_must_match_frozen_source(self):
        self.result["implementation_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "Result/snapshot identity differs"):
            self.check()

    def test_preparation_source_and_input_mutations_block_retention(self):
        source = self.prepared / "source" / self.skill_relative
        original = source.read_bytes()
        source.write_text("Changed during evaluation.")
        with self.assertRaisesRegex(ValueError, "Prepared source changed"):
            evaluation.retain_case("example", self.prepared, self.run, "report.md")
        source.write_bytes(original)
        (self.prepared / "repository/snapshot.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "Prepared input changed"):
            evaluation.retain_case("example", self.prepared, self.run, "report.md")

    def test_retention_rejects_input_as_report_including_path_and_file_aliases(self):
        repository = self.prepared / "repository"
        fixture = repository / "nested/input.txt"
        (repository / "input-symlink.md").symlink_to(fixture)
        (repository / "input-hardlink.md").hardlink_to(fixture)
        for name in ("nested/input.txt", "./nested/input.txt", "nested/./input.txt",
                     "input-symlink.md", "input-hardlink.md"):
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError, "Report cannot be an input"):
                    evaluation.retain_case("example", self.prepared, self.run, name)

    def test_retention_cannot_write_through_an_escaping_cases_directory(self):
        run = self.root / "new-run"
        with contextlib.redirect_stdout(io.StringIO()):
            evaluation.snapshot(run)
        external = self.root / "external-write-target"
        external.mkdir()
        (run / "cases").symlink_to(external, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "must stay within"):
            evaluation.retain_case("example", self.prepared, run, "report.md")
        self.assertEqual(list(external.iterdir()), [])

    def test_retention_rejects_escaping_prepared_directories(self):
        for name in ("source", "repository"):
            with self.subTest(directory=name):
                original = self.prepared / name
                external = self.root / f"external-{name}"
                original.rename(external)
                original.symlink_to(external, target_is_directory=True)
                try:
                    with self.assertRaisesRegex(ValueError, "must stay within"):
                        evaluation.retain_case("example", self.prepared, self.run, "report.md")
                finally:
                    original.unlink()
                    external.rename(original)

    def test_record_rejects_input_as_report_including_path_and_file_aliases(self):
        directory = self.run / "cases/example"
        fixture = directory / "nested/input.txt"
        (directory / "input-symlink.md").symlink_to(fixture)
        (directory / "input-hardlink.md").hardlink_to(fixture)
        self.result["cases"]["example"]["report_sha256"] = evaluation.digest(fixture)
        for name in ("nested/input.txt", "./nested/input.txt", "nested/./input.txt",
                     "input-symlink.md", "input-hardlink.md"):
            with self.subTest(name=name):
                self.result["cases"]["example"]["report"] = f"cases/example/{name}"
                with self.assertRaisesRegex(ValueError, "Report cannot be an input"):
                    self.check()

    def test_record_report_must_belong_to_its_own_case(self):
        other = self.run / "cases/another/report.md"
        other.parent.mkdir()
        other.write_text("A different case's assessment.")
        self.result["cases"]["example"]["report_sha256"] = evaluation.digest(other)
        self.result["cases"]["example"]["report"] = "cases/another/report.md"
        with self.assertRaisesRegex(ValueError, "must stay within their case directory"):
            self.check()
        (self.run / "cases/example/other-case.md").symlink_to(other)
        self.result["cases"]["example"]["report"] = "cases/example/other-case.md"
        with self.assertRaisesRegex(ValueError, "must stay within"):
            self.check()

    def test_record_rejects_a_whole_case_directory_outside_the_run(self):
        original = self.run / "cases/example"
        external = self.root / "external-case"
        original.rename(external)
        original.symlink_to(external, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "must stay within"):
            self.check()

    def test_archive_check_rejects_a_run_outside_the_archive_directory(self):
        self.check()
        external = self.root / "external-run"
        self.run.rename(external)
        self.run.symlink_to(external, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "must stay within"):
            evaluation.check_archives(self.run.parent)

    def test_fail_and_unassessed_results_preserve_integrity_without_passing(self):
        for status in ("fail", "not_evaluated"):
            self.result["cases"]["example"]["criteria"]["scope"]["status"] = status
            self.assertEqual(self.check(), 1)
            self.assertEqual(self.check(integrity_only=True), 0)
        self.result["cases"]["example"]["criteria"] = {}
        with self.assertRaisesRegex(ValueError, "Incomplete rubric"):
            self.check()

    def test_legacy_source_limitation_is_required_and_cannot_pass(self):
        self.result["provenance"] = "legacy_missing_source"
        with self.assertRaisesRegex(ValueError, "requires an explicit limitation"):
            self.check()
        self.result["provenance_limitation"] = "Original source unavailable; artifact hashes established retrospectively."
        (self.run / "source.json").unlink()
        self.assertEqual(self.check(), 1)
        self.assertEqual(self.check(integrity_only=True), 0)

    def test_additional_retained_artifact_is_bound(self):
        prior = self.run / "first-pass.md"
        prior.write_text("Initial output before a recorded repair.")
        self.result["cases"]["example"]["additional_artifact_sha256"] = {"first-pass.md": evaluation.digest(prior)}
        self.assertEqual(self.check(), 0)
        prior.write_text("Tampered initial output.")
        with self.assertRaisesRegex(ValueError, "Additional artifact digest mismatch"):
            self.check()

    def test_record_cannot_reference_outside_artifact_directory(self):
        self.result["cases"]["example"]["report"] = "../report.md"
        with self.assertRaisesRegex(ValueError, "must stay within"):
            self.check()
        external = self.root / "external.md"
        external.write_text("Unretained report.")
        (self.run / "external-link.md").symlink_to(external)
        self.result["cases"]["example"]["report"] = "external-link.md"
        with self.assertRaisesRegex(ValueError, "must stay within"):
            self.check()

    def test_archive_check_detects_corrupt_record_and_missing_run_record(self):
        self.check()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(evaluation.check_archives(self.run.parent), 0)
        (self.run / "results.json").write_text('{"unrelated":"valid JSON"}')
        with self.assertRaisesRegex(ValueError, "Unsupported result schema"):
            evaluation.check_archives(self.run.parent)
        (self.run / "results.json").unlink()
        with self.assertRaisesRegex(ValueError, "Missing artifact"):
            evaluation.check_archives(self.run.parent)

    def test_archive_check_warns_when_current_plugins_are_not_the_evaluated_source(self):
        self.check()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(evaluation.check_archives(self.run.parent), 0)
        self.assertNotIn("Live plugin source differs", output.getvalue())
        self.skill.write_text("New plugin behavior has no recorded evaluation.")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(evaluation.check_archives(self.run.parent), 0)
        self.assertIn("Live plugin source differs", output.getvalue())
        self.assertIn("historical judgments do not evaluate the current source", output.getvalue())
        self.assertEqual(self.check(), 0)

    def test_failed_record_does_not_suppress_missing_passing_evaluation_warning(self):
        self.result["cases"]["example"]["criteria"]["scope"]["status"] = "fail"
        self.check()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(evaluation.check_archives(self.run.parent), 0)
        self.assertIn("No retained run records complete passing adjudications", output.getvalue())

    def test_newer_unavailable_git_run_cannot_replace_verified_source_for_staleness(self):
        self.check()
        earlier = self.run.parent / "earlier-complete-run"
        shutil.copytree(self.run, earlier)
        self.use_git_provenance("0" * 40)
        self.result.update(date="2026-10-12", implementation_sha256="1" * 64)
        identity = evaluation.read_json(self.run / "snapshot.json")
        identity["implementation_sha256"] = self.result["implementation_sha256"]
        evaluation.write_json(self.run / "snapshot.json", identity)
        evaluation.write_json(self.run / "results.json", self.result)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(evaluation.check_archives(self.run.parent), 0)
        self.assertIn("source provenance incomplete", output.getvalue())
        self.assertNotIn("Live plugin source differs", output.getvalue())
        self.assertNotIn("No retained run records complete passing adjudications", output.getvalue())

    def test_optimized_python_cannot_disable_checks(self):
        self.check()
        (self.run / "cases/example/report.md").write_text("Changed report")
        result = subprocess.run([sys.executable, "-O", str(ROOT / "tools/evaluate-skills.py"),
                                 "check-results", str(self.run / "results.json")],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Report digest mismatch", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
