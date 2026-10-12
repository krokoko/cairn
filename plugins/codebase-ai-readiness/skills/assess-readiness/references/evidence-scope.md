# Evidence Scope

Use this contract when assessing readiness or reusing an assessment for a roadmap.
Discovery establishes which capabilities are configured. It does not establish that a
check executed or that its assertions represent the current requirement.

## Required scope metadata

Every report includes `## Evidence Scope` with these nonempty fields:

- **Source revision**: commit plus relevant uncommitted changes, or explain unavailable identity
- **Assessment date**: date of this assessment
- **Inspected scope**: paths, components and excluded surfaces
- **Evidence basis**: artifacts and runs inspected, inaccessible evidence, and any reused report

Bind an inspected run to the target revision and environment. Retain links to the
requirement/oracle revision, tool version/configuration, bounds or campaign size,
assumptions, exclusions and completion record. A commit alone does not identify dirty files.
If evidence cannot be inspected, record that limit rather than inferring absence or success.

## Readiness evidence ledger

Use these exact columns in `## Evidence Ledger`:

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| Accepted claim and relevant check | Path/run reference and revisions | model/local/mocked/staging/deployed or justified N/A | One value below | One value below | One value below | Bounds, exclusions, unknowns and review status |

Use one row per decision-relevant claim/check. Cite retained details in Artifact / revision
or Limits; do not force all run metadata into the table itself.

| Field | Allowed values |
|-------|----------------|
| Observation | `configuration_only`, `run_inspected`, `not_inspectable`, `stale`, `not_applicable` |
| Execution | `completed`, `timeout`, `interrupted`, `skipped`, `unsupported`, `not_run`, `unknown`, `not_applicable` |
| Conclusion | `counterexample`, `established_within_scope`, `no_counterexample_found`, `unknown`, `incomplete`, `unsupported`, `not_run`, `not_applicable` |

- `established_within_scope` and `no_counterexample_found` require `run_inspected` +
  `completed`. Completion alone does not justify either conclusion.
- Sampled tests support `no_counterexample_found` for exercised cases. A completed,
  appropriate proof/analysis can support `established_within_scope` under its assumptions.
- A timeout, skipped check, stale report or unresolved obligation is not a positive result.
  Preserve execution state. For stale evidence, that state describes the historical artifact;
  its conclusion about the current scope is always `unknown` or `incomplete`, including when
  the historical execution was skipped, unsupported or not run. `incomplete` describes required
  current analysis that remains unfinished, not an interrupted historical run; identify it in
  Limits. Use `unknown` if the current completion state is unknown.
- A counterexample can be useful even when a campaign did not finish; retain its reproducer.
- For inaccessible CI/history, use `not_inspectable` + `unknown` + `unknown`.
  A present configuration without inspected run evidence is normally
  `configuration_only` + `unknown` + `unknown`; use `not_run` only when that is known.
- An unconditional source skip may use `configuration_only` + `skipped` + `not_run`.
  Cite its declaration, assessed revision and unconditional scope in Limits; no observed run
  is implied. A conditional skip with an unestablished condition remains `unknown` + `unknown`.
- `not_applicable` requires a scope-specific reason. Never use it to hide missing evidence.
- Distinguish local doubles from deployed dependencies. Agreement between a test and code
  using the same expectation helper does not establish independent correctness.

Use `-` for no additional limits or findings; bracketed references such as `[ADR-7]` are valid.
Required identities, evidence states and scope metadata still need meaningful values.
Replace template tokens such as `[Component]` with the assessment.

## Reusing a report

Compare its revision, relevant dirty changes, scope, requirement/oracle revisions and run
environments with the current target. Mark affected findings stale when they differ.
Unknown revision or inaccessible run history means freshness is unverified.

Reuse unaffected findings with attribution; refresh affected conclusions when evidence is
available. Otherwise plan the evidence-gathering action first and keep the current level
provisional. A roadmap's Evidence Scope identifies the source report and freshness decision;
planned checks belong in acceptance criteria, not a fabricated execution ledger.
