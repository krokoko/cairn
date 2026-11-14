# Scoped Verification Evidence

Use this contract when assessing existing checks or designing evidence requirements. A configured
tool is a capability; an inspected run is evidence about a particular artifact and claim.
Verification asks whether an approved rule holds. Validation asks whether the rule and outcome
serve the intended need. Purpose, quality goal, method, and evidence mode are separate dimensions.

## Report scope

Include `## Evidence Scope` with these exact metadata labels:

- **Source revision**: commit and any relevant uncommitted changes; otherwise identify the snapshot.
- **Assessment date**: date of inspection, distinct from the dates of inspected runs.
- **Inspected scope**: components, paths, environments, and accessible remote settings.
- **Evidence basis**: artifacts/runs inspected, configuration-only observations, and unavailable data.

Do not run every discovered command just to fill the report. Inspect relevant existing evidence;
execute bounded checks when useful and within the user's scope. Mark inaccessible CI history or
hosting settings unknown. Absence from the working tree does not establish absence in production.

## Evidence ledger

Use the exact heading `## Evidence Ledger` and table columns:

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| REQ-7 / retry invariant | run URL + source revision | local twin | run_inspected | completed | no_counterexample_found | 100 recorded sequences; provider fidelity unverified |

Record one row per relevant claim/check/environment. Link detailed evidence instead of flattening
different scopes into a single pass. Proposed checks belong in a strategy's requirements table;
they are not existing successful evidence.

### Observation

| Value | Meaning |
|-------|---------|
| `configuration_only` | Check/configuration exists; relevant execution evidence was not inspected |
| `run_inspected` | Run evidence was inspected and applies to the recorded artifact and scope |
| `not_inspectable` | Needed source, settings, or run evidence could not be inspected |
| `stale` | Available evidence does not establish the claim for the assessed revision/scope |
| `not_applicable` | Check does not apply; record a claim/risk-based reason in Limits |

### Execution

Use exactly `completed`, `timeout`, `interrupted`, `skipped`, `unsupported`, `not_run`, `unknown`,
or `not_applicable`. `not_run` requires evidence of non-execution; use `unknown` when no result was
available to inspect. A runner that exits successfully with all checks skipped did not complete
those checks. Keep test-level status visible even when the overall job is green.

An unconditional skip declared in the inspected source at the assessed revision may use
`configuration_only` + `skipped` + `not_run`. Cite the skip declaration and its unconditional
scope in Limits; this records source-defined exclusion, not an observed runner result.
For a conditional skip whose condition was not established, use `configuration_only` +
`unknown` + `unknown`. Configuration alone cannot establish completion or a positive conclusion.

### Conclusion

| Value | Meaning |
|-------|---------|
| `counterexample` | Recorded observation violates the stated claim, subject to oracle/fidelity review |
| `established_within_scope` | Completed analysis establishes the property within declared assumptions |
| `no_counterexample_found` | Exercised cases/search found no violation; no claim outside that campaign |
| `unknown` | Evidence cannot resolve the claim, including timeout or inaccessible results |
| `incomplete` | Required analysis/checks did not finish; partial results cannot establish the full claim |
| `unsupported` | Tool or environment cannot analyze the requested property/scope |
| `not_run` | The relevant check was not executed |
| `not_applicable` | Claim/risk-based exemption is documented; this is not a successful verification |

Positive conclusions (`established_within_scope`, `no_counterexample_found`) require both
`run_inspected` and `completed`. Stale evidence can describe an earlier success in Limits, but its
current conclusion remains `unknown` or `incomplete`. A genuine recorded counterexample remains
useful even if the rest of a campaign was interrupted; identify the failing case.
For stale rows, Execution records the historical artifact's state; even an earlier skipped,
unsupported or not-run result cannot establish that state for the current revision.
Thus `stale` + `skipped` + `incomplete` is valid when required current analysis is incomplete;
it does not say the historical skip was an interrupted execution. State the unfinished current
analysis in Limits. Use `unknown` when its current completion state is unknown.

Neither a positive conclusion nor a fresh artifact hash is semantic approval. Record the reviewed
relationship between requirement, assertion, fixtures/helpers, and environment separately.

## What a completed result supports

| Evidence mode | Supported conclusion | Essential limits |
|---------------|----------------------|------------------|
| Example/property tests, fuzzing, simulation | No violation in exercised cases | Oracle, generators, fault campaign, seeds, coverage, fidelity |
| Heuristic/symbolic search | No counterexample in completed search | Explored paths; search completion is not exhaustive proof |
| Bounded analysis | Property established within a completed bound | Unwinding, assumptions, supported operations, discharged obligations |
| Model checking | Property holds over the completely explored model | Completion, model state space, correspondence to implementation |
| Deductive proof | Proposition follows under proof assumptions | Specification adequacy, trusted toolchain, environment models |
| Static/architecture rule | Analyzed scope meets the configured property | Soundness for that property, parser coverage, missing edges, exceptions |
| Trace monitoring | Recorded events satisfy/violate the monitored rule | Missing/ordered events, finite-trace limits; monitoring is not enforcement |
| User/maintenance validation | Studied outcomes support the intended need | Representative tasks, participants, conditions, and interpretation |
| Metrics/provenance | A measurement or origin was recorded | Neither alone establishes behavioral correctness |

Do not assign `established_within_scope` to sampled tests or search because the tool exited zero.
A signature authenticates evidence provenance; it does not strengthen the evidence's semantics.

## Retained context and policy

Retain approved requirement/claim and oracle revisions; assertion, fixture, and helper revisions;
target source plus relevant dirty diff; environment/dependency versions; tool/version/configuration;
bounds, campaign size/seeds; assumptions/exclusions; execution and result artifacts; and review
status. Link these from the ledger's Artifact / revision and Limits cells.

Compare an expected inventory with native runner results from a fresh run directory. Missing,
skipped, duplicate, stale, or interrupted reports need explicit treatment; validate each runner's
report dialect. A declared scenario is not evidence that its steps ran.

Promotion policy names required claims, accepted evidence modes/scopes, and handling of unknowns.
An unrelated proof cannot compensate for a required integration check with no evidence. Report
recommendations do not grant operational permission; humans or configured policy own the decision.

Report cells may use `-` for no additional limits or findings, and bracketed references such as
`[ADR-7]` are valid citations. Required identities, evidence states and scope metadata still need
meaningful values; template tokens such as `[Component]` must be replaced.
