# Autonomy Prerequisites

Load in both readiness assessment and roadmap planning. Scores are diagnostic; they do not
grant permission to merge, deploy or act. Evaluate the changed surface and its critical
dependencies, using current, scoped evidence.

## Apply ceilings before recommending a level

1. Treat the score-to-level mapping as provisional.
2. Set an evidence ceiling for each surface from its reviewed intent, oracle adequacy,
   enforced checks and dependency fidelity. Do not average away a critical gap.
3. Absent reviewed executable intent or weak/unknown critical-path oracle evidence caps
   the surface at L3; use a lower level when reliable bounded iteration is not established.
4. Apply every L5 prerequisite below. Any status other than `met` caps the surface at L4.
5. Recommend the lower of the provisional level and evidence ceiling. Record the supported
   operating scope, remaining human decisions and blockers. Permissions remain external.

Do not infer an oracle's adequacy from its method name, test count, coverage or a green CI
badge. Link the claim, actual checks, reviewed assumptions and completed evidence.

## Two L4 scope prerequisites

| ID | Evidence required for `met` |
|----|----------------------------|
| L4-INTENT | Reviewed executable intent defines the proposed operating scope and its critical dependencies; cite approved claims and their relevant checks |
| L4-ORACLES | Current, adequate oracle evidence covers the critical paths within that operating scope; cite reviewed expectations, completed checks and limits |

Both must be `met` to recommend L4 or L5. Any other status caps the recommendation at L3.
These scoped prerequisites differ from the complete critical-behavior coverage and operational
controls required for L5. L4 can remain appropriate when one or more L5 gates are unmet.
Explicitly exclude changes outside the supported scope; a critical dependency cannot be excluded
merely to obtain a higher recommendation.

## Five L5 hard gates

| ID | Prerequisite | Evidence required for `met` |
|----|--------------|----------------------------|
| L5-INTENT | Reviewed executable intent for all critical behavior | Approved, revisioned claims mapped to executed checks; sampled assertion review supports meaning, with partial claims and deviations explicit |
| L5-ORACLES | Adequate oracles on every critical path | Risk-matched checks with current evidence, independent acceptance criteria, sensitivity controls and disclosed assumptions; statistical oracles need justified bounds and calibration |
| L5-ENVIRONMENT | Representative simulation/staging | Evidence that relevant production behavior, dependencies and faults are represented; local/mocked/deployed evidence and fidelity gaps stay separate |
| L5-DETECTION | Detection of silent failures | Exercised checks/telemetry that detect wrong-but-not-crashing outcomes, with known-bad controls and an operational response |
| L5-RECOVERY | Progressive delivery and automated recovery | Exercised rollback/containment driven by relevant detection, with scope, trigger and recovery limits recorded |

All five apply to an L5 recommendation; this is a gate checklist, not five added score categories.
A small library may use a domain-specific equivalent, such as controlled package rollout
and version rollback. Mark it `met` only with a reviewed equivalence rationale and evidence.
Do not relabel a missing control as an equivalent.

## Required report tables

In `## Surface Autonomy`, use exactly:

| Surface | Provisional level | Evidence ceiling | Recommended level | Operating scope | Blockers |
|---------|-------------------|------------------|-------------------|-----------------|----------|
| Named component and dependencies | L0–L5 or unknown | L0–L5 or unknown | L0–L5 | Change classes and human decisions | Ceiling rationale and missing/unknown evidence, or reason none |

Use exactly `L0`–`L5` or `unknown` in the two bound columns; put rationale in Blockers.
Recommended level is exactly `L0`–`L5` and cannot exceed either known bound.
If no score is defensible, use `unknown` for the provisional level and make only a
conservative evidence-based recommendation. An unknown evidence ceiling cannot support above
L3. A repo-wide summary must not imply permission on excluded surfaces or conceal the lowest
relevant dependency ceiling.

In `## Recommended Autonomy Level`, write `**Level**: L0` (using the applicable L0–L5 value)
as one exact value, without a tier name or additional level on that line. This conservative
summary cannot exceed the lowest Recommended level in Surface Autonomy. Describe operating
scope on a separate line and keep different surface levels in the table.

In `## Autonomy Prerequisites`, use exactly:

| Surface | Prerequisite | Status | Evidence / gap |
|---------|--------------|--------|----------------|
| Assessed surface | One canonical L4/L5 ID above | `met`, `missing`, `unknown` or `not_applicable` | Evidence citation, missing capability or reason evidence cannot be inspected |

Use the identical Surface value in both tables; do not shorten a name or change its formatting
between the recommendation and prerequisite rows. Keep extra descriptions in Operating scope.
Include both L4 IDs and all five L5 IDs for each assessed surface, even when recommending L3 or below.
`missing` means observed absence; `unknown` means insufficient or inaccessible evidence.
`not_applicable` requires a scope-specific justification and does not satisfy a prerequisite:
an unmet L4 prerequisite caps at L3; an unmet L5 gate caps at L4.
A declared control or planned check alone is not `met`.
