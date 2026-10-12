# Software Verification Report

## Evidence Scope

**Source revision**: Declared snapshot `oracle-rot-r2` in [snapshot.json](snapshot.json:2). No Git history, commit identity, or dirty-diff record was supplied. The declaration identifies the fixture; it is not evidence of execution.

**Assessment date**: 2026-10-11.

**Inspected scope**: All five supplied files: [price.py](price.py), [tests/test_price.py](tests/test_price.py), [requirements.md](requirements.md), [evidence/run.json](evidence/run.json), and [snapshot.json](snapshot.json). One deterministic Python pricing component; recorded environment `local Python`. No hosting settings or remote history were inspected.

**Evidence basis**: Read-only source and requirement inspection, the supplied aggregate run record, and the named frozen assessment skill and its relevant references. No target checks were executed and no remote state was retrieved. The run record identifies the assessed revision but omits a timestamp, Python/runner versions, individual check IDs, and native runner output. Consequently, matching revision is supported; chronological recency and reproducibility are unknown.

The central finding is **oracle rot**: the approved requirement now specifies a 15% discount, while the implementation and passing assertion preserve the old 10% discount. For the supplied input of 10,000 cents, revision 2 requires 8,500 cents; the source computes and the test expects 9,000 cents. This discrepancy follows directly from the supplied text and arithmetic; it is not a newly executed test result.

## Evidence Ledger

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| Recorded local test suite: one execution, zero failures | [evidence/run.json:2-6](evidence/run.json:2), `oracle-rot-r2` | local Python; versions unknown | run_inspected | completed | no_counterexample_found | Bounded to the one execution reported by the aggregate artifact. Individual check identity and raw results are absent. This does not establish the approved 15% rule. |
| REQ-DISCOUNT revision 2: preferred customers receive 15% off | [requirements.md:1-2](requirements.md:1), [price.py:1-2](price.py:1), [tests/test_price.py:1-3](tests/test_price.py:1) | supplied source snapshot | configuration_only | unknown | unknown | No current-intent assertion/result exists in the supplied evidence. Inspection shows 9,000 expected/computed for 10,000 rather than the required 8,500; no new execution was performed. |
| Mutation sensitivity campaign | [evidence/run.json:7](evidence/run.json:7), reported score `0.98` | local Python; mutation tool/configuration unknown | run_inspected | unknown | unknown | A score is recorded, but no campaign completion, mutant inventory, relevant violating edits, survivors, equivalent mutants, timeouts, or per-mutant results are supplied. A 98% score cannot approve the current business rule. |
| Semantic review of the discount assertion | [evidence/run.json:8-11](evidence/run.json:8), requirement revision 1 / expected discount 10% | review context unknown | stale | not_applicable | unknown | Review covers the obsolete requirement. Owner, review date, assertion/fixture/helper revisions and accepted exclusions are unknown. Current-source execution does not refresh this review. |
| Required merge/release gates and repeatability | No supplied hosting settings, CI configuration, or run history | hosting/CI unknown | not_inspectable | unknown | unknown | Not inspectable from the supplied working tree; no inference that remote gates are absent. |

## Verification Maturity

**Demonstrated overall tier**: **1/5 — Configured**.

**Rubric**: `verification-maturity/2`; assessed 2026-10-11. No historical maturity report was supplied for comparison.

**Limiting evidence / provisional target**: A real test implementation and a matching-revision aggregate execution record exist. Tier 2 is not demonstrated: repeatability, representative current-intent checks, diagnostics, and required enforcement are unconfirmed. The consequential oracle also demonstrably encodes an obsolete rule, preventing higher risk-matched or qualified claims. First repair the oracle and implementation against the approved requirement, then establish Tier 2 reliability and enforcement; Tier 3 would additionally require reviewed money/rounding cases. Neither the passing run nor the reported mutation score raises the demonstrated tier.

## Component Breakdown

| Component | Archetype | Criticality | Current methods / evidence | Demonstrated tier / limit |
|-----------|-----------|-------------|----------------------------|---------------------------|
| `preferred_price` and its pricing test | Deterministic library; deterministic integer arithmetic for integer inputs | High — determines customer charges | One exact-output assertion; one reported passing execution; aggregate mutation score; stale assertion review | 1 — current intent fails source inspection; repeatability and gates unknown |

No property tests, fuzz targets, static/type/security checks, schemas/contracts, formal specifications, CI workflows, hooks, coverage artifacts, deployment configuration, or operational evidence were supplied. This is an inventory of the snapshot, not an assertion about a larger production system. No third-party integration, concurrency, or learned component is visible.

## Bug-Surface Classification

| Component | Class (A–E) | Evidence | Recommended depth | Ceremony risk |
|-----------|-------------|----------|-------------------|---------------|
| Preferred-customer price calculation | B — Arithmetic / conservation | Monetary cents and percentage rule in [requirements.md:2](requirements.md:2); multiplication and floor division in [price.py:2](price.py:2) | standard — independently derived examples, reviewed integer/rounding properties, targeted violating controls | Yes for distributed/model-checking or broad formal infrastructure without a remaining arithmetic claim; a small bounded analysis could be useful after the domain is specified |

**Checks with no identified claim/gap**: Schedule exploration, provider twins, learned-output evaluation, and native-memory sanitizers are not justified for the supplied pure Python function. Python integers avoid fixed-width integer overflow for integer inputs; input types and external conversions are not specified.

**Failure surfaces lacking relevant evidence**: Current 15% behavior, fractional-cent rounding, valid input domain (including negatives and non-integers), and downstream charging behavior if this function is integrated elsewhere. No deployment/integration claim is established by this snapshot.

## Missing Oracles

| Component / claim | Current oracle | Strength (qualified/weak/unknown/none) | Adequacy / sensitivity / independence / freshness | Gap / action |
|-------------------|---------------|---------------------------------------|-------------------------------------------------|--------------|
| REQ-DISCOUNT revision 2 / 15% discount | Exact expected output `preferred_price(10000) == 9000` | weak | **Adequacy: gap** — expectation is 10%, contrary to revision 2. **Sensitivity: gap** for the current claim — this assertion accepts the obsolete behavior and would reject the correct 8,500 result; the aggregate mutation score does not qualify intended violations. **Independence: unknown** — literal expectation does not call a shared helper, but derivation/reviewer provenance is absent. **Freshness: gap** — supplied semantic review covers requirement revision 1 only. | Repair implementation and assertion together against independently derived revision-2 values; retain obsolete 10% behavior as a known-bad control. Record revised semantic approval. |
| Price rounding and supported input domain | No dedicated assertions or approved boundary policy found | none | **Adequacy: gap** — scope unspecified and only a divisible example exists. **Sensitivity: unknown** — no boundary controls. **Independence: unknown** — no reviewed reference. **Freshness: unknown** — no applicable review record. | Approve integer-cent domain, rounding convention, and invalid-input policy; add focused examples/properties for that bounded scope. |

**Review identity**: Approved claim is `REQ-DISCOUNT` revision 2 ([requirements.md](requirements.md:1)); the only review artifact names revision 1 and 10%. Responsible domain owner and review date are unknown. The inspected assertion is [tests/test_price.py:3](tests/test_price.py:3) in snapshot `oracle-rot-r2`; no assertion-specific revision is recorded. Its input and expectation are inline literals, and it imports the production function directly; no separate fixtures or helpers are supplied. There is no recorded revision-bound approval tying these assets to revision 2.

**Oracle rot versus execution freshness**: The recorded execution source matches the snapshot. The problem is not merely an old run or missing test: a passing execution at the current declared source can preserve an obsolete expectation. Re-running the same assertion, raising its mutation score, or refreshing a fingerprint would leave this semantic defect intact. There are no provider twins, holdouts, or judge models to qualify in the inspected scope.

## Exactness Analysis

| Component | Feasibility | Rationale |
|-----------|-------------|-----------|
| Discount calculation | Exact within scope feasible | The 10,000-cent example has an exact 8,500-cent expected result without rounding ambiguity. More generally, once approved input bounds and rounding semantics exist, a precise integer postcondition can be proved or exhausted over a declared finite domain. No such proof or exhaustive campaign was supplied or run. |
| End-to-end customer charge, if integrated | Mixed | Pure arithmetic may admit exact reasoning, but customer eligibility, currency conversion, persistence and actual charging would need relevant integration evidence. These surfaces are outside the supplied snapshot and their existence/behavior is unknown. |

## Human Review Requirements

| Component | Reason | Review type |
|-----------|--------|-------------|
| Pricing rule and oracle | Money impact; demonstrated mismatch with approved intent | Domain reviewer confirms 15% expectation and independently derived values; review the code/test change together and record covered revisions. |
| Rounding/domain contract | Requirement omits consequential boundary semantics | Product/finance review of rounding, valid inputs and exclusions before broadening assertions or proof claims. |
| Promotion decision | Gate enforcement and recovery policy are unknown | Review scoped evidence and configured policy before release; this assessment grants no permission. |

## Autonomy Candidates

| Changed surface | Recommended operating scope | Evidence / confidence | Remaining claims / environment gaps |
|-----------------|-----------------------------|-----------------------|------------------------------------|
| Pricing fix and focused regression draft | Agent may prepare a reviewable code/test proposal based on revision 2 and independent arithmetic | High confidence in the supplied 10,000 → 8,500 discrepancy; low confidence in release assurance | Human semantic review, rounding/domain decisions, fresh executed evidence, required gates, and rollback context remain necessary. Existing green results cannot authorize autonomous promotion. |
| Evidence record and trace mapping | Agent may draft explicit check IDs, revision links and missing-status reports | Small local surface; records can be reviewed directly | Must not invent missing run details, reviewer approval, or hosting enforcement. |

## Feedback Loop Completeness

**Overall level**: **1/3 — Readable**, limited to the supplied JSON artifact.

| Verification method | Output format | Routable to agents? | Level | Gap |
|---------------------|--------------|---------------------|-------|-----|
| Exact-output unit test | Aggregate JSON, counts only | Artifact is readable; automated delivery/re-execution unknown | 1 | No check IDs, paths/lines, failure details, runner dialect, or routing evidence. |
| Mutation testing | Single JSON score | Routing unknown | 1 | No mutant-level actionable result or trustworthy completion accounting. |
| Semantic review | JSON requirement revision and old percentage | Readable; invalidation/routing unknown | 1 | No automatic current-requirement mismatch signal or reviewer/revision record. |

No agent feedback latency, API access, re-execution triggers, isolated runtime, or queryable logs/metrics were supplied. Structured counts alone cannot direct a reliable fix or detect wrong intent.

## Workflow Gate Assessment

| Gate | Risk class | Throughput concern? | Recommendation |
|------|-----------|---------------------|----------------|
| Merge/release status checks and required approvals | Monetary correctness | Unknown; settings and rejection history unavailable | Inspect authorized hosting settings separately when available; require current approved pricing claims and completed applicable checks before promotion. |
| Semantic-review freshness | Monetary intent drift | No throughput evidence | Make requirement/assertion/fixture/helper changes invalidate prior review, and obtain current approval. Current review remains revision 1. |
| Local hooks | Fast feedback only | No hooks supplied | If introduced, treat them as bypassable; enforce authoritative results server-side. |

**Bottleneck gates**: Unknown; there is no rejection-rate or review-latency evidence. Do not remove review on the strength of this green run.

**Missing gates**: Current semantic-review enforcement is not demonstrated and the supplied stale relationship persists. Remote gates are **not inspectable from the working tree**, not proven absent. Duplicate gates, bypass frequency, and actionable reviewer feedback are unknown. Agent pre-review can flag the concrete discrepancy; it cannot approve financial policy or replace an unknown required review process.

## Shift-Left Assessment

| Check | Current tier | Ideal tier | Gap | Recommendation |
|-------|-------------|-----------|-----|----------------|
| Pricing unit test | Unknown; `local Python` does not establish timing | T2 per logical change, full applicable suite at T3 | No workflow, focused command, watch mode or hook supplied | Run the reviewed focused cases early and preserve full required checks at the merge boundary. |
| Mutation sensitivity | Unknown | T3 periodic/pre-merge campaign | No timing/configuration or campaign evidence | Target meaningful arithmetic decisions after intent repair; retain detailed outcomes. |
| Requirement/review freshness | Unknown | T1/T2 change signal and T3 review gate | No invalidation mechanism supplied | Surface affected review immediately when requirement or oracle assets change. |

**Checks running too late**: Cannot establish lateness from these artifacts. Execution placement is unknown; recommendations do not assert CI-only execution.

## Documentation Verification

**Overall level**: **0/3 in the supplied snapshot** — manually maintained requirement with no supplied automated validation.

| Dimension | Present? | Mechanism | Gap |
|-----------|----------|-----------|-----|
| Auto-generated docs | Not found | `requirements.md` is prose | No generated-doc evidence; approved business intent should remain independently reviewed. |
| Doc build in CI | Not found | No CI supplied | Unknown outside snapshot; a full documentation site is not justified by this one file. |
| Link validation | Not found | No checker supplied | Low-priority structural validation if records grow. |
| Example testing | Not found | Test exists separately | Current test contradicts the stated discount. |
| Schema-doc sync | Not applicable to visible scope | No API/schema supplied | No schema-sync claim to assess. |
| Doc freshness enforcement | Not found | Requirement revision and review revision diverge | Need impact review and trace invalidation on business-rule changes. |
| ADR/changelog enforcement | Not found | No ADR/changelog artifacts | No specific architectural requirement identified; do not add ceremony without one. |

**Stale doc risk areas**: Here the approved requirement is explicit and current; code/test/review lag behind it. Generating documentation from the wrong implementation would entrench the defect. The needed synchronization is reviewed intent → assertion → implementation, not mechanically treating current code as authority.

## AgentOps Telemetry

**Overall observability level**: **1/3 — Minimal**, based on one accessible aggregate quality record. Wider operational systems are unknown.

| Stream | Level | Key gaps | Recommendation |
|--------|-------|----------|----------------|
| Trajectory | 0 observed | No agent traces or verification-consumption records supplied | Record how change → review → check → correction decisions occur when agents are used. |
| Cost | 0 observed | No durations, task cost or resource data | Add timestamps/durations to execution records before making optimization claims. |
| Quality | 1 | One pass/fail aggregate and mutation score; no trends, flake or defect history | Track intent-aligned regression detection and native outcomes over repeated runs. |
| Autonomy compliance | 0 observed | No gate overrides, escalations or audit history | Retain promotion decisions and explicit exceptions for unresolved claims. |
| Domain | 0 observed | No actual discount/charge outcome evidence | If deployed, compare applied discounts against approved policy and define review/response thresholds. |

**Critical blind spots**: A green test and 98% mutation score coexist with the wrong customer discount. Metrics must be tied to the current approved rule. Runtime domain instrumentation is conditional on a real integration; none can be assumed from this snapshot.

## Requirement Traceability

**Overall level**: **unknown** under the supplied 0–3 traceability model. The artifacts show a manually inferable requirement/test/code relationship, but no parseable complete claim/check/code mapping and no inspectable PR history. Thus Level 2 is not demonstrated, and the Level 1 PR-link criterion cannot be confirmed. This does not mean the visible requirement has no relationship to the test.

| Completeness | Evidence / current state | Gap / required review |
|--------------|--------------------------|-----------------------|
| Links | `REQ-DISCOUNT`, `test_req_discount`, and the imported `preferred_price` suggest the intended chain; run has source revision | Stable explicit claim/check/code mapping absent; PR/issue linkage and history not inspectable. |
| Execution | Source revision matches; aggregate records 1 executed / 0 failed | No expected inventory joined to named native results, skipped/missing accounting, run ID/date, environment versions, or isolation evidence. Cannot establish check-level completeness. |
| Meaning | Requirement revision 2 is 15%; assertion and review retain revision-1 10% semantics | Demonstrated semantic incompleteness/oracle rot; reviewer, review date, assertion/fixture/helper revisions and accepted exclusions unrecorded. |

| Property | State | Failure it allows |
|----------|-------|-------------------|
| Scope verification | Manual inference only; no change history/diff | Untraced behavior changes may remain unnoticed. |
| Impact analysis | No recorded invalidation from requirement revision 1 → 2 | Obsolete assertion and implementation persist after an approved change. |
| Test sufficiency | One example asserts the wrong percentage; input boundaries absent | A linked passing check can fail to cover the current requirement. |

**Untraced changes**: No change history was supplied, so changed-code coverage cannot be quantified. The supplied implementation is manually associated with pricing intent; a formal mapping is absent.

**Uncovered requirements**: Revision 2's 15% rule lacks a correct applicable assertion in the supplied suite. The similarly named test does not cover it semantically. Rounding and input semantics need clarification, not invented requirements.

**Intent-drift risk**: Demonstrated. Updating run metadata or parsing an ID would not repair the old expectation. Revision-bound semantic approval and an independently derived current oracle are required.

## Verification Debt

| ID | Component | Debt type | Severity | Current → Required | Remediation |
|----|-----------|-----------|----------|--------------------|-------------|
| VD-1 | Pricing calculation and assertion | Oracle rot | High | Approved 15% rule with 10% implementation/expectation → reviewed current-intent behavior | Independently derive 8,500 for 10,000 cents; repair code and test; qualify the obsolete 10% result as known bad and retain a regression. |
| VD-2 | Requirement/oracle review process | Stale semantic review and documentation synchronization | High | Revision-1-only review → current, revision-bound approval invalidated by relevant changes | Record responsible reviewer, review date, requirement/assertion/fixture/helper revisions and accepted scope; trigger impact review on change. |
| VD-3 | Pricing boundaries | Missing oracle / underspecified claim | High | No rounding/input contract → approved bounded arithmetic semantics and dedicated checks | Review cents domain, rounding and invalid inputs; independently derive boundary examples and applicable properties. |
| VD-4 | Promotion enforcement | Uninspected gate evidence | High | Unknown required checks/review policy → inspected authoritative current-intent gate | Obtain hosting settings and promotion policy when authorized/available; preserve unknowns until then, with scoped exception review if required. |
| VD-5 | Run evidence and trace mappings | Execution completeness / partial links | High | Anonymous aggregate result and implicit mapping → named expected checks joined to versioned native results | Add explicit requirement/check/code mappings, run ID/date, versions, completion/skipped/missing states and isolated artifact provenance. |
| VD-6 | Oracle qualification | Unknown independent derivation and incomplete mutation evidence | High | Literal with unknown provenance and score-only campaign → independently reviewed values and relevant sensitivity controls | Retain derivation/reviewer provenance; report known-good/bad controls and mutant relevance, survivors, equivalent cases, timeouts and completion separately. |
| VD-7 | Deployed pricing, if present | Domain telemetry blind spot | High | No supplied customer-outcome evidence → policy-aligned outcome observation for deployment claims | Determine the real integration scope; if deployed, monitor applied discounts against approved rules and record response/recovery policy. This is conditional, not a claim that a production monitor is absent. |
| VD-8 | Test reliability | Insufficient repeatability evidence | Medium | One recorded run → representative repeated current-intent runs with attributable diagnostics | Retain repeated native results and flake observations for the assessed revision/environment after repair. |
| VD-9 | Feedback delivery | Unrouted feedback | Medium | Readable summary → actionable check/mutant diagnostics delivered to the change workflow | Add check/file/context attribution and a documented delivery/re-execution mechanism; keep semantic-review decisions separate from execution success. |
| VD-10 | Local verification workflow | Unknown shift-left placement | Medium | No evidenced timing → focused T2 loop with authoritative T3 checks | Document and record the focused workflow and freshness signal; schedule mutation by actual cost. |
| VD-11 | Agent/verification operations | Trajectory, cost, quality-trend and compliance visibility | Medium | Aggregate one-run quality only → retained task decisions, timing, repeated outcomes and overrides | Capture minimal linked operational records; measure detection of wrong-rule changes rather than optimizing scores alone. |
| VD-12 | Documentation record structure | Unvalidated document links/examples | Low | Prose-only records → lightweight structural checks as records grow | Validate requirement/evidence links and approved worked examples without deriving business intent from implementation. |

**Severity rubric**: High = a high-criticality component with no/weak oracle or a gap that lets silent regressions ship; Medium = partial business-logic/process evidence; Low = structural utility concerns. VD-7 is a conditional High risk for any production promotion claim; no production system is presumed to exist. Each row is one fileable liability and may be exported with a `verification-debt` label.
