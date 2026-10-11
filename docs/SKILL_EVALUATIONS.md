# Independent skill evaluations

Cairn's ordinary build checks packaging, report structure, declared-state consistency,
references, fixture integrity, and retained evaluation archives. It does not execute an AI
model or establish that a skill reaches the correct conclusion.

The [scenario inventory](../tests/evals/cases.json) contains twelve independently authored
repository snapshots covering all five skills. The separate [rubric](../tests/evals/rubric.json) states required
findings and prohibited overclaims. The report-validator fixtures are also independently
authored; good reports are not generated from the validator's section list.

## Run a blind evaluation

Check the fixture inventory:

```bash
mise run evals:check
```

Freeze the implementation and evaluation definitions into a new run directory before
starting any agents. The retained source snapshot makes the evaluated implementation
reconstructible even when the working tree has uncommitted changes.

```bash
python3 tools/evaluate-skills.py snapshot --output /tmp/cairn-evaluation
```

Prepare one case from that snapshot into a new isolated directory:

```bash
python3 tools/evaluate-skills.py prepare skipped-acceptance \
  --snapshot /tmp/cairn-evaluation --output /tmp/cairn-skipped-eval
```

Give an independent agent only that directory's `TASK.txt`, the named skill, and relevant
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

- `schema_version: 2` and `provenance: "retained_source"` for new runs.
- `run_id`, `date`, source revision including dirty-state description.
- `implementation_sha256`, `fixture_sha256`, and `rubric_sha256` from the retained snapshot.
  Keep its source, catalog and rubric files with the record. Criteria text is part of
  evaluation identity, even if its keys stay the same.
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
Changing a report invalidates its prior adjudication; a new judgment must bind the new bytes.
Hashes detect drift relative to the record, not a coordinated rewrite of the record and artifacts.

`check-archives` runs in CI and checks archive integrity independently of the recorded
semantic outcome. Failed evaluations remain useful regression evidence and need not break
packaging CI. Explicit legacy provenance gaps are reported, not promoted to complete evidence.
Neither command decides whether an adjudicator's judgments are correct.

## Interpreting and improving results

The scenarios cover configured-only evidence, obsolete oracle meaning, skipped acceptance,
stale runs, model/provider fidelity, mixed surfaces, missing L5 recovery, and equivalent
mutations. Additional cases exercise a stale roadmap baseline, provider migration strategy,
smell-gate scope, and a positively qualified finite local component without formal tools.
These are focused regression cases, not a representative estimate of all agent performance.

The [11 October 2026 run](../tests/evals/results/2026-10-11-scoped-evidence/results.json)
retains all eight assessments and 24 reviewed criteria. All criteria were met in the inspected
outputs. Seven reports passed structure validation initially; one needed a Surface identifier
repair, with its first output retained. The evaluated dirty source was not preserved and
subsequent implementation changes were not rerun. This archive is marked as legacy evidence
with missing source provenance. Integrity bindings added during repair preserve the surviving
artifacts; they do not recreate the missing original implementation.

The [review-fix run](../tests/evals/results/2026-10-11-review-fixes/results.json) retains
the exact evaluated plugin source and all twelve cases. All 36 semantic criteria were met
in the reviewed outputs. Eleven submitted reports passed portable validation without parent
feedback; the skipped-acceptance report needed two ledger rows corrected using only validator
diagnostics. Its original output is retained and hashed, and its semantic findings did not
change. All final reports validate. Each case used a fresh agent context and the same frozen
source; the retained implementation fingerprint matches the completed plugin changes.

One successful run is one sample. Record variation across repeated runs before making a
reliability claim. Keep evaluation cases out of the implementation agent's context where
possible, and rotate/add independently reviewed cases when repeated feedback exposes them.
Domain judgment, real repository trials, and maintenance outcomes remain separate evidence.

When a failure occurs, fix the demonstrated workflow gap and rerun affected cases. Keep
unaffected observations attributed to the implementation fingerprint on which they ran.
For rubric changes, compare representative old and new conclusions and record why an
apparent tier movement reflects changed interpretation rather than changed software quality.
