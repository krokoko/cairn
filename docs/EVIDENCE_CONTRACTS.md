# Evidence contracts and migration

Readiness 0.5 and software verification 0.6 distinguish configured capability, inspected
execution, and the conclusion supported by that execution. They also revise verification
maturity around the adequacy of a risk-matched portfolio.

## Report contract

Every report includes **Evidence Scope** with source revision (including relevant dirty
changes), assessment date, inspected scope, and evidence basis. An unavailable value needs
an explanation; it must not be invented.

Assessment reports and verification strategies include an **Evidence Ledger**. Strategy
ledgers describe existing observations; proposed checks belong in **Evidence Requirements**.
Roadmaps identify their source report and whether its evidence is current.

| Dimension | Values | Meaning |
|-----------|--------|---------|
| Observation | `configuration_only`, `run_inspected`, `not_inspectable`, `stale`, `not_applicable` | What the assessor actually inspected |
| Execution | `completed`, `timeout`, `interrupted`, `skipped`, `unsupported`, `not_run`, `unknown`, `not_applicable` | Whether and how the check ran |
| Conclusion | `counterexample`, `established_within_scope`, `no_counterexample_found`, `unknown`, `incomplete`, `unsupported`, `not_run`, `not_applicable` | What the evidence supports for the assessed claim |

“Completed” includes a check that found a violation. A counterexample can remain valid even
when the rest of a campaign was interrupted. Positive conclusions require inspected,
completed execution. A current skipped check yields `not_run`; unavailable remote execution
is `unknown`. A stale artifact retains its historical execution state, while its conclusion
for the assessed revision must be `unknown` or `incomplete`.

Keep requirement/assertion review separate from execution freshness. A fresh run can check
an obsolete rule. Record the approved requirement, assertion, fixture and helper revisions;
review affected relationships when they change. Mutation and negative controls challenge
sensitivity, not business intent.

## Portable validation

Claude PostToolUse hooks provide advisory JSON feedback. They always exit zero to satisfy
the hook integration. They are not merge protection or semantic approval.

The same check is available without a Claude hook:

```bash
python3 plugins/software-verification/scripts/check-report.py --check verification-report.md
python3 plugins/codebase-ai-readiness/scripts/check-report.py --check readiness-report.md
```

The CLI exits nonzero for missing sections, empty required metadata, unfinished assessment
cells, missing table rows, invalid states, and selected contradictions among declared states.
Every matching contract table is checked, including tables split into subsections.
Fixed row labels do not count as completed assessments.

Readiness reports declare two L4 prerequisites for reviewed executable intent and adequate
critical-path oracles, separately from the five stricter L5 prerequisites. Missing or unknown
L4 prerequisites cap the recommendation at L3; L5 requires all seven prerequisites to be met.
Declared recommendations cannot exceed their provisional score or evidence ceiling.
The readiness summary uses `**Level**: L0` through `L5` and cannot exceed the lowest assessed
surface recommendation; explain scoped differences in Surface Autonomy.
Each plugin includes its own validator and contract file and can be installed independently.

Successful validation means the report's structure and declared states are consistent.
It does not establish that citations are authentic, checks really ran, an oracle matches
intent, a dependency model is faithful, or a user authorized any action.

## Migrating existing reports

1. Reinspect source identity, changed scope, and available run artifacts. Preserve useful
   historical findings with attribution, but mark changed or unverifiable evidence.
2. Add scope metadata and a ledger with explicit unknowns. Do not infer successful execution
   from configuration, test names, a zero exit code with skipped tests, or old artifacts.
3. Complete every assessment cell with a finding or explicit unknown/exclusion. Revisit
   requirement links using three questions: are they complete, did the checks run,
   and do their assertions support the approved claim?
4. Reassess maturity using the new risk-relative rubric. Reassess autonomy per surface using
   the same prerequisite checklist in assessment and roadmap. Add both L4 prerequisite rows
   alongside the five L5 rows for every surface, and give the readiness summary an explicit Level.
5. Run the portable report validator and review semantic sufficiency separately.

## Rubric compatibility

Verification tiers are now **None, Configured, Reliable, Risk-matched, Qualified, and Managed
evidence**. Their numbers are not interchangeable with historical **Generative** or
**Formal + Operational** scores. Record the rubric version in maturity notes and compare
findings and supported claims before drawing a trend from the numeric tier.
The identifiers are `verification-maturity/2` and `readiness-scoring/2`; the latter also
changes how unknown categories are excluded and disclosed in a provisional score.

| Representative situation | Earlier rubric pressure | Current interpretation |
|--------------------------|-------------------------|------------------------|
| Reliable simple library, qualified examples and boundary checks | Formal methods appeared necessary for Tier 4 | Qualification is relative to its actual failure modes; formal inapplicability can be justified |
| Formal model passes but external adapter is unverified | Formal-tool presence could inflate overall maturity | Model evidence is scoped; adapter fidelity and integration gaps remain |
| High readiness score, manual recovery only | L5 requirements were explicit only in roadmap guidance | Both workflows check the same hard prerequisites and cap recommendations |
| Requirement changed, tests and mutation still green | Mutation was described as the main defense against oracle rot | Semantic review is stale until the relationship to revised intent is reviewed |

Readiness scores remain diagnostic heuristics. Unknown categories remain visible with the
assessed weight; thresholds and file/rule counts are not improvement targets. Recommendations
remain scoped advice rather than operating permissions.

For reproducible behavioral checks, use the [independent evaluation workflow](./SKILL_EVALUATIONS.md).
