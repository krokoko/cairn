# Skill evaluation records

Cairn's ordinary build checks packaging, report structure, declared-state consistency,
references, fixture integrity, and retained evaluation archives. It does not execute an AI
model or establish that a skill reaches the correct conclusion.

The [scenario inventory](../tests/evals/cases.json) contains twelve agent-authored repository
snapshots covering all five skills. Agents participating in implementation also authored the
separate [rubric](../tests/evals/rubric.json) and adjudicated results. Withholding that rubric
from fresh evaluator contexts limits answer leakage; it does not make the cases or grading
independent of implementation. Report-validator fixtures were written separately from the
validator's section list.

## Run a blind evaluation

Check the fixture inventory:

```bash
mise run evals:check
```

Freeze the implementation and evaluation definitions into a new run directory before
starting any agents. The retained source snapshot makes the evaluated implementation
reconstructible even when the working tree has uncommitted changes or Git history is rewritten.

```bash
python3 tools/evaluate-skills.py snapshot --output /tmp/cairn-evaluation
```

For committed plugin source, omit the repeated source archive with an explicit full commit SHA:

```bash
python3 tools/evaluate-skills.py snapshot --revision "$(git rev-parse HEAD)" \
  --output /tmp/cairn-committed-evaluation
```

This reads plugin files from that commit, including when the working tree has other changes.
Fixture definitions and rubric are still retained from the current working tree. Keep the
commit available in checkouts that validate or replay the run. Shallow clones, squash merges,
rebases, or expired unreachable objects can make it unavailable; the runner never fetches
history automatically. Use the default standalone snapshot when that retention cannot be ensured.

Prepare one case from that snapshot into a new isolated directory:

```bash
python3 tools/evaluate-skills.py prepare skipped-acceptance \
  --snapshot /tmp/cairn-evaluation --output /tmp/cairn-skipped-eval
```

Give a fresh evaluator context only that directory's `TASK.txt`, the named skill, and relevant
references from the materialized frozen source. Do not give it the rubric, prior findings,
other cases, or expected answer. Start a fresh context for each case.
Use the specified read-only snapshot conditions; target checks and remote state are outside
these cases' scope. The report belongs in the prepared directory's `repository/` subdirectory.

Retain each completed case before adjudicating it:

```bash
python3 tools/evaluate-skills.py retain-case skipped-acceptance \
  --prepared /tmp/cairn-skipped-eval --run /tmp/cairn-evaluation \
  --report verification-report.md
```

This checks the frozen skill source and raw inputs, copies the report and inputs into the
run, and prints a case entry containing their hashes. Fill its criterion judgments after
reviewing that retained report. Keep the report and any separately identified repair attempts.

Repeat for each case using the same frozen snapshot and retain the reports and raw inputs
with the evaluation record. Review each against
the withheld criteria; cite the report passage supporting each judgment. Record failures
and inconclusive cases as well as successes. The runner provides no automatic semantic judge.

## Required run record

Store `results.json` alongside the snapshot files with:

- `schema_version: 2` and `provenance: "retained_source"` or `"git_revision"`.
- `run_id`, `date`, source revision including dirty-state description for standalone snapshots,
  or the exact full commit SHA for Git provenance.
- `implementation_sha256`, `fixture_sha256`, and `rubric_sha256` from the retained snapshot.
  Keep its catalog, rubric, and snapshot identity with the record, plus `source.json` for
  standalone snapshots. Git provenance resolves and verifies the plugin bytes in the recorded
  commit instead. Criteria text is part of evaluation identity, even if its keys stay the same.
- Model identifier or an explicit statement that the runtime did not expose it.
- Configuration: skill/client, context isolation, permitted tools, repetitions, sampling
  settings when available, and any deviations from the task.
- Adjudicator identity/role and limitations.
- Every case ID, its report path and SHA-256, the archived input paths and SHA-256 values,
  and every criterion's
  `status` (`pass`, `fail`, or `not_evaluated`) plus cited `evidence`/rationale.

Copy the complete finished run directory into `tests/evals/results/` for CI validation.
Keep in-progress runs outside that directory; each archived run must have a complete record.

```bash
python3 tools/evaluate-skills.py check-results path/to/results.json
python3 tools/evaluate-skills.py check-archives
```

`check-results` verifies source provenance, retained fixture and rubric identity, report
bytes, raw input bytes, and complete adjudications. It returns nonzero for failed or
unassessed criteria and for legacy records whose evaluated source was not retained.
Git source that is unavailable locally also prevents `check-results` and `prepare` from succeeding.
Changing a report invalidates its prior adjudication; a new judgment must bind the new bytes.
Hashes detect drift relative to the record, not a coordinated rewrite of the record and artifacts.

`check-archives` runs in CI and checks archive integrity independently of the recorded
semantic outcome. Failed evaluations remain useful regression evidence and need not break
packaging CI. Missing local Git history produces an explicit incomplete-provenance warning;
report and input integrity are still checked. CI also warns when live plugin source differs
from the newest retained run with verified source and all criteria recorded as passing,
or no such run exists.
That comparison signals staleness; it is not an approval of the rubric or its judgments.
Neither command decides whether an adjudicator's judgments are correct.

## Interpreting and improving results

The scenarios cover configured-only evidence, obsolete oracle meaning, skipped acceptance,
stale runs, model/provider fidelity, mixed surfaces, missing L5 recovery, and equivalent
mutations. Additional cases exercise a stale roadmap baseline, provider migration strategy,
smell-gate scope, and a positively qualified finite local component without formal tools.
These are focused regression cases, not a representative estimate of all agent performance.

The [review-fix run](../tests/evals/results/2026-10-11-review-fixes/results.json) retains
the evaluated plugin source and all twelve cases. Its integrating agent recorded 36 passing
criterion judgments, one output per case. This is self-adjudicated evidence: no human or
independent reviewer graded the outputs, and short qualitative criteria do not establish
reproducible grading. Exact runtime model and sampling identifiers were unavailable, so source
replay is possible but exact model-run reproduction is not.

Eleven submitted reports passed the then-current portable validator without parent feedback.
The skipped-acceptance report had two rows changed after validator diagnostics. Its original
output is retained and hashed. The narrative findings stayed intact, but replacing a
source-declared unconditional skip with unknown reduced ledger precision; the repair was
not purely structural. Historical validation and judgments belong to the retained source,
not later plugin edits. The earlier legacy run lacked recoverable evaluated source and was
removed from the working tree; its artifacts remain in Git history.

One recorded pass is one sample. Before using these results for release qualification,
have an independent reviewer refine criterion anchors and grade reports, record disagreement,
and run repeated samples with identifiable models and sampling settings. Keep evaluation
cases out of the implementation agent's context where possible, and rotate/add independently
reviewed cases when repeated feedback exposes them.
Domain judgment, real repository trials, and maintenance outcomes remain separate evidence.

When a failure occurs, fix the demonstrated workflow gap and rerun affected cases. Keep
unaffected observations attributed to the implementation fingerprint on which they ran.
For rubric changes, compare representative old and new conclusions and record why an
apparent tier movement reflects changed interpretation rather than changed software quality.
