# Oracle Lifecycle

Assess whether a check still judges the approved requirement, not merely whether it runs.
Use `evidence-semantics.md` for execution states and scoped conclusions.

## Assess four independent dimensions

| Dimension | Inspect | Gap to report |
|-----------|---------|---------------|
| Adequacy | Approved bounded claim; assertions and exclusions that address it | Missing/partial claim, wrong expected behavior, unreviewed generated property |
| Sensitivity | Known-good/known-bad controls, relevant mutations, incident regression cases | Check cannot reject the violation it is meant to catch |
| Independence | Expected-value derivation, reference provenance, shared fixtures/helpers | Implementation and expectation repeat the same mistake |
| Freshness | Requirement/assertion/fixture/helper revisions covered by semantic review | A previously approved relationship changed without review |

Report `supported`, `gap`, or `unknown` for each dimension with artifact references. Do not infer
strength solely from oracle type, determinism, coverage, or a mutation score. A deterministic check
can encode a wrong rule; a calibrated statistical oracle can support an appropriate bounded claim.

## Review record

For each consequential oracle, identify:

- Requirement/claim ID and approved revision; owner or responsible domain reviewer.
- Assertion, fixture, helper, and relevant model/reference revisions.
- Review evidence/date and accepted scope/exclusions; use `unknown` when uninspectable.
- Controls or counterexamples used to challenge the expectation.

Changing a linked requirement, assertion, fixture, or helper makes the earlier relationship review
stale until the affected semantics are reviewed. A new run refreshes execution evidence only.
Fingerprints identify changed inputs; refreshing them does not approve their meaning.

**Oracle rot**: tests stay green after the requirement drifts. It is distinct from no oracle,
execution staleness, or a vacuous assertion. Properties and examples can both rot.

## Challenge the oracle

- Use independently derived expected values where practical. Agreement through the same helper
  does not provide independent confirmation.
- Qualify the checker with allowed and known violating examples; retain both controls.
- Mutate relevant decisions. First confirm the mutation violates the intended claim; surviving
  equivalent or out-of-scope mutations do not by themselves show weak assertions.
- For a new bug-fix regression, demonstrate failure on the comparable old implementation and
  success on the fix when feasible. If the old environment cannot be reproduced, record that limit.
- Preserve incident counterexamples, approved behavior changes, and intentionally rejected cases.
- Calibrate influential model judges against independently labeled accepted and rejected cases;
  track changes to model/rubric and feedback exposure.

Mutation measures sensitivity to selected code changes. Neither mutation nor review fingerprints
automatically detects an outdated business rule. Domain review and representative outcome evidence
remain necessary where the claim depends on intent.

## References, twins, and holdouts

A reference version may preserve old bugs. Approve intended equivalence and intentional differences.
A behavioral twin is an environment model: inspect fidelity checks against the real dependency,
supported scenarios, version assumptions, and drift handling. Local twin results do not establish
provider behavior outside validated scope.

Holdouts reduce direct exposure; repeated feedback can reveal cases indirectly. Record access and
feedback controls rather than claiming the evaluator cannot be gamed. Distinct implementations or
agents can share assumptions; agreement is corroboration, not independent truth by default.
