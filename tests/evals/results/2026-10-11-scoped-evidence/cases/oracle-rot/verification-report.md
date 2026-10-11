# Software Verification Report

## Evidence Scope

**Source revision**: Declared snapshot `oracle-rot-r2` in [snapshot.json](snapshot.json:2). This identifier is fixture identity, not execution evidence. No commit history or dirty-change record was supplied.

**Assessment date**: 2026-10-11.

**Inspected scope**: All supplied target files: `price.py`, `tests/test_price.py`, `requirements.md`, `evidence/run.json`, `snapshot.json`, and `TASK.txt`. Recorded execution environment: local Python; interpreter/dependency versions are unknown. Hosting settings and remote history were not retrieved.

**Evidence basis**: Read-only source, requirement, and recorded-run inspection. No target checks were executed. The run record is revision-matched, but contains no execution date, native test identities, detailed mutation outcomes, or current semantic approval. Unavailable settings and history remain unknown.

## Evidence Ledger

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| Existing discount example, expecting 9000 for 10000 | [test assertion](tests/test_price.py:3); [run summary](evidence/run.json:2), `oracle-rot-r2` | Local Python; versions unknown | run_inspected | completed | no_counterexample_found | Record reports one executed test and zero failures. This supports the legacy example only; individual result identity and run date are absent. It does not support the current 15% requirement. |
| Current REQ-DISCOUNT revision 2: preferred customers receive 15% discount | [approved requirement](requirements.md:1), [implementation](price.py:2), [test](tests/test_price.py:3) | Supplied source | configuration_only | unknown | unknown | No applicable executed 15% assertion is supplied. Direct source inspection shows a 90% multiplier and a 9000 expectation; revision 2 requires 8500 for 10000. This is a concrete semantic mismatch, not a newly executed failure. |
| Mutation sensitivity for the current approved discount rule | [mutation_score](evidence/run.json:7) | Campaign environment/tool/version unknown | run_inspected | unknown | unknown | Aggregate score 0.98 is recorded, but mutant definitions, status counts, exclusions, controls, and campaign completion are unavailable. Mutation cannot approve current business intent. |
| Required enforcement and repeatability | No hosting settings or run history supplied | Merge/release environments unknown | not_inspectable | unknown | unknown | Cannot infer absence or presence of enforced checks from this snapshot. |

The passing test run and obsolete assertion can coexist: execution is matched to the assessed source, while the semantic relationship is stale.

## Verification Maturity

**Demonstrated overall tier**: **1/5 — Configured**.

**Rubric**: The supplied `assess-verification/references/maturity-model.md`, inspected 2026-10-11; the rubric has no declared revision. No historical maturity score was supplied.

**Limiting evidence / provisional target**: Tests and a revision-matched execution summary exist, but repeatability and required enforcement are uninspectable. The critical pricing path also has an oracle that contradicts the approved requirement. First restore the approved rule, then demonstrate Tier 2 reliability and enforcement; qualification requires reviewed expectations and sensitivity evidence. A mutation percentage does not advance maturity.

## Component Breakdown

| Component | Archetype | Criticality | Current methods / evidence | Demonstrated tier / limit |
|-----------|-----------|-------------|----------------------------|---------------------------|
| Preferred-customer pricing | Deterministic library | High — money | One exact-output unit test, one run summary, aggregate mutation metric | Tier 1; current intent is not checked, enforcement/repeatability unknown |

Inventory found no supplied CI, static-analysis, type-check, security-scanning, property/fuzz, contract, formal-analysis, or deployment configuration. This is an observation about supplied files, not the wider system.

## Bug-Surface Classification

| Component | Class (A–E) | Evidence | Recommended depth | Ceremony risk |
|-----------|-------------|----------|-------------------|---------------|
| Preferred-customer pricing | B — Arithmetic / conservation | Money in cents and percentage calculation in `price.py`; discount requirement | Standard | Yes for adding elaborate proof infrastructure before correcting the approved arithmetic oracle; focused boundary/property checks address the immediate gap |

**Checks with no identified claim/gap**: Concurrency simulation, provider twins, and learned-output evaluation have no identified role in this local function. Native-memory sanitizers are not justified by the supplied Python arithmetic.

**Failure surfaces lacking relevant evidence**: Approved discount rate, rounding semantics, permitted input domain, and boundaries. No supplied requirement settles fractional-cent treatment or negative inputs.

## Missing Oracles

| Component / claim | Current oracle | Strength (qualified/weak/unknown/none) | Adequacy / sensitivity / independence / freshness | Gap / action |
|-------------------|---------------|---------------------------------------|-------------------------------------------------|--------------|
| REQ-DISCOUNT revision 2 | Hard-coded exact expectation of 9000 for 10000 | weak | Adequacy: **gap**, assertion expresses 10%, not 15%. Sensitivity: **unknown**, raw mutation score lacks relevant controls/outcomes. Independence: **unknown**, literal expectation is separate from code but its derivation/reviewer provenance is absent. Freshness: **gap**, recorded review covers requirement revision 1 only. | Replace obsolete behavior and assertion together using independently reviewed revision-2 examples; retain a test that rejects the 10% implementation. |

**Oracle rot** is demonstrated: `requirements.md:2` approves 15%, while `evidence/run.json:8-10` records assertion review of revision 1 at 10%. The fresh revision-matched passing run does not renew semantic approval. This is distinct from a missing test or a run for an old source revision.

The requirement ID and revisions are known. The approved claim's owner, approval date, assertion/fixture/helper revision identifiers, and relationship-review date are unknown. The assertion is the supplied `tests/test_price.py:3`; no fixtures or helper functions are supplied. For the approved 15% claim, no applicable exact oracle exists in this snapshot. A 0.98 mutation score cannot establish that the expected value still expresses intent.

## Exactness Analysis

| Component | Feasibility | Rationale |
|-----------|-------------|-----------|
| Preferred-customer pricing | Exact within scope feasible | For a declared integer-cent domain and approved rounding rule, the percentage formula and bounded boundary cases admit exact analysis. The supplied 10000-cent example has an unambiguous revision-2 expected value of 8500. No proof/exhaustive campaign was supplied; input bounds and fractional-cent policy remain unspecified. |

## Human Review Requirements

| Component | Reason | Review type |
|-----------|--------|-------------|
| Pricing rule and oracle | Monetary impact and demonstrated requirement/assertion divergence | Domain owner reviews the 15% rule, expected examples, rounding/input policy, and revision-bound assertion changes |
| Promotion evidence | Enforcement, reliability, and current semantic approval unknown | Reviewer or existing policy owner resolves required evidence before accepting pricing changes |

## Autonomy Candidates

| Changed surface | Recommended operating scope | Evidence / confidence | Remaining claims / environment gaps |
|-----------------|-----------------------------|-----------------------|------------------------------------|
| Pricing implementation and tests | Agent may prepare a focused correction and reviewable evidence; current checks are insufficient for autonomous acceptance of price changes | Low confidence in approved behavior despite passing legacy example | Domain approval of new oracle, relevant failing control, current complete run, required gate, repeatability, recovery/blast-radius evidence |
| Evidence/report maintenance | Bounded mechanical recording of source, test status, and review revisions | Small reversible surface | Metadata updates must not be treated as semantic approval |

Maturity is not permission. Preserve applicable review policy.

## Feedback Loop Completeness

**Overall level**: **1/3 — Readable**, for supplied artifacts.

| Verification method | Output format | Routable to agents? | Level | Gap |
|---------------------|--------------|---------------------|-------|-----|
| Unit test | JSON aggregate counts in `evidence/run.json` | Routing unknown | 1 | Missing per-check identity, failure details, timestamps, artifact routing and retry evidence |
| Mutation campaign | JSON score | Routing unknown | 1 | No mutant-level attribution or classification; current claim is not linked |

No artifact-storage pipeline, API delivery, agent re-execution trigger, or isolated observability stack was supplied. Record native per-check results and route actionable failures before claiming a closed loop.

## Workflow Gate Assessment

| Gate | Risk class | Throughput concern? | Recommendation |
|------|-----------|---------------------|----------------|
| Required merge/release checks | Monetary rule changes | Unknown; no rejection/latency records | Inspect hosting settings when permitted; require current tests and reviewed oracle revisions |
| Semantic review | Pricing intent | Existing record is stale; rejection rate unknown | Invalidate review when linked requirements/assertions change |
| Local hooks | Early feedback | None supplied; wider use unknown | Any added hook is bypassable; keep authoritative checks server-side |

**Bottleneck gates**: Cannot identify from available data. No evidence justifies removing or replacing human review.

**Missing gates**: Current semantic-review evidence is missing. Hosting enforcement is not inspectable from the working tree; absence is not established. Duplicate gates and actionable rejection feedback are unknown.

## Shift-Left Assessment

| Check | Current tier | Ideal tier | Gap | Recommendation |
|-------|-------------|-----------|-----|----------------|
| Focused pricing test | Unknown; run record has no lifecycle trigger | T2, plus full applicable suite at T3 | No trigger/watch configuration | Run focused tests during implementation and enforce full required checks at merge |
| Mutation challenge | Unknown | T3 or periodic full verification | Campaign details and trigger absent | Challenge approved pricing decisions after oracle review, not every edit |
| Requirement/oracle review invalidation | No supplied automation | T2–T3 | Revision-1 relationship survived revision-2 requirement | Flag linked semantic changes early; domain review must resolve them |

**Checks running too late**: Timing cannot be established. Earlier placement alone would not fix the obsolete assertion.

## Documentation Verification

**Overall level**: **0/3 in the supplied scope**.

| Dimension | Present? | Mechanism | Gap |
|-----------|----------|-----------|-----|
| Auto-generated docs | No supplied evidence | Manual `requirements.md` | No generation/sync evidence |
| Doc build in CI | No supplied evidence | Unknown | No build validation supplied |
| Link validation | No supplied evidence | Unknown | No link validation supplied |
| Example testing | No supplied evidence | Test exists separately | Test contradicts requirement |
| Schema-doc sync | No schema supplied | Not applicable to declared local formula | Do not add schema tooling without an interface claim |
| Doc freshness enforcement | No supplied evidence | Requirement and review revisions differ | No relationship-review invalidation |

**Stale doc risk areas**: The requirement is newer than implementation/test meaning; the evidence does not show that the requirement document itself is stale. The risk is unsynchronized intent, code, and assertions.

## AgentOps Telemetry

**Overall observability level**: **1/3 demonstrated by retained run metrics**; remote telemetry is unknown.

| Stream | Level | Key gaps | Recommendation |
|--------|-------|----------|----------------|
| Trajectory | 0 demonstrated | No agent iteration or evidence-consumption records | Retain verification decisions and failure/fix chains |
| Cost | 0 demonstrated | No timings or resource data | Record check duration before optimizing |
| Quality | 1 | One pass summary and mutation percentage; no trends or semantic controls | Track relevant mutant outcomes and regressions against approved claims |
| Autonomy compliance | 0 demonstrated | No override/escalation records | Record acceptance exceptions and stale-review handling |
| Domain | 0 demonstrated | No observed pricing outcomes | If deployed, monitor approved discount outcomes and exercised rollback paths |

**Critical blind spots**: Green tests can coexist with a wrong discount. Run/mutation metrics alone do not measure current business correctness; deployed impact and recovery are unknown.

## Requirement Traceability

**Overall level**: **1/3 — manual/partial mapping**. The requirement, function, and test can be related by inspection; no complete parseable claim/check/code inventory or enforcement is supplied. PR/issue linkage is not inspectable; no history sample can be computed.

| Completeness | Evidence / current state | Gap / required review |
|--------------|--------------------------|-----------------------|
| Links | `REQ-DISCOUNT`, `preferred_price`, `test_req_discount` are manually related | Explicit claim/check/code mapping and expected inventory absent |
| Execution | Revision-matched one-test execution summary | Individual native status and approved revision-2 check absent; run date unknown |
| Meaning | Requirement revision 2 versus assertion review revision 1 | Known stale semantic relationship; reviewed decision for current intent absent |

| Property | State | Failure it allows |
|----------|-------|-------------------|
| Scope verification | Partial manual mapping | Updated discount requirement can leave implementation unchanged |
| Impact analysis | No enforced mapping/review invalidation | Requirement change does not force assertion review |
| Test sufficiency | Existing test targets obsolete rate | Approved 15% claim remains unchecked |

**Untraced changes**: History/diff unavailable; cannot enumerate changes.

**Uncovered requirements**: REQ-DISCOUNT revision 2 has no semantically applicable test in the supplied scope.

**Intent-drift risk**: Demonstrated, not inferred from a metric: the assertion approves the prior 10% rule.

## Verification Debt

| ID | Component | Debt type | Severity | Current → Required | Remediation |
|----|-----------|-----------|----------|--------------------|-------------|
| VD-1 | Pricing | Oracle rot | High | Passing 10% assertion → approved 15% behavior and oracle | Review independent expected values, fix code and test, retain old-rule rejecting control, bind semantic review to affected revisions |
| VD-2 | Pricing | Incomplete arithmetic contract | High | Unspecified boundaries/rounding → approved bounded claim | Define input/rounding semantics and add focused boundary/property checks |
| VD-3 | Pricing verification | Unqualified sensitivity | High | Aggregate 0.98 metric → relevant violating-control evidence | Retain mutant definitions, native outcomes, equivalent/out-of-scope classifications, and current-rule controls |
| VD-4 | Change acceptance | Unknown reliability/enforcement | High | One run and unavailable settings → repeatable required checks | Inspect permitted run history/hosting settings and document policy for unknown/stale semantic evidence |
| VD-5 | Traceability/docs | Partial links and absent review invalidation | High | Manual association → revision-bound claim/check/code/review chain | Maintain expected check inventory and invalidate semantic review on requirement/assertion/fixture/helper changes |
| VD-6 | Operational verification | Telemetry blind spot | High | No supplied business outcome/recovery evidence → observed approved prices if deployed | Instrument discount outcomes, escalation, and recovery; scope to actual deployment |
| VD-7 | Verification feedback | Unrouted aggregate feedback | Medium | Counts/score → attributable results and agent routing | Retain per-check results, timestamps, diagnostics, and artifact delivery evidence |
| VD-8 | Development loop | Unknown shift-left placement | Medium | Unspecified triggers → focused T2 checks and authoritative T3 gate | Record and configure lifecycle placement without treating hooks as enforcement |
| VD-9 | Verification operations | Telemetry blind spot | Medium | Isolated metrics → timing, iteration, trend and override records | Capture decision-linked telemetry rather than optimizing raw scores |

Severity: High means a consequential pricing or silent-regression gap; Medium means partial verification feedback/process evidence. Unknown remote capabilities are requests for evidence, not findings that those capabilities are absent. The backlog can be exported with a `verification-debt` label.
