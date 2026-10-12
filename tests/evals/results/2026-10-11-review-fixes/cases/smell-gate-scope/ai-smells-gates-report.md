# AI Smell Detection Gates Report

## Evidence Scope

**Source revision**: Declared snapshot `smell-gate-scope-r2`, from `snapshot.json:2`. This is a fixture identity, not evidence that any command ran. No Git revision or working-tree comparison was supplied.

**Assessment date**: 2026-10-11.

**Inspected scope**: All 11 supplied files in this snapshot: application, tests, requirements, custom AST checker, two checker controls, workflow, README, snapshot identity, and two evidence receipts. Relevant frozen skill references informed interpretation. No target checks were executed, and no remote state was retrieved.

**Evidence basis**: Inspected `evidence/empty-except.json` and `evidence/tests.json` separately from source/configuration. The receipts name the declared current snapshot. CI history beyond these receipts and hosting protection are explicitly unavailable (`README.md:4`); required-check settings, bypass rights, historical trends, and actual resolved CI dependency versions remain unknown.

The empty-except gate is qualified for detecting an exception handler whose entire body is `pass`. It does not detect the catalog error masking in this snapshot. The current test receipt reports passing tests, full branch coverage, and a mutation score of 0.98, but the tests and their semantic review still encode requirement revision 1. Approved revision 2 requires a different discount and propagated catalog failures. This is a requirement/assertion freshness failure; fresh execution and high metrics do not repair it.

## Evidence Ledger

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| No exception handler consisting solely of `pass` in `checkout.py` | `evidence/empty-except.json:2-9`; `tools/empty_except.py:4-7`; snapshot r2; tool `empty-except/1` | CPython 3.12 AST parser, as recorded | run_inspected | completed | established_within_scope | Explicitly completed scan with zero violations over the one named file. Does not constrain return values, propagation, boundary validation, or business rules. |
| AST checker accepts the supplied allowed control and rejects the supplied violating control | `evidence/empty-except.json:10-22`; `gate_controls/allowed.py:1-4`; `gate_controls/violating.py:1-4`; snapshot r2 | CPython 3.12 AST parser, as recorded | run_inspected | completed | no_counterexample_found | Both expected exit codes were observed and controls completed. Qualification covers these two examples, not every possible Python construct. Controls are parsed; the undefined `operation()` need not execute. |
| The two supplied tests satisfy their encoded expectations | `evidence/tests.json:2-5`; `tests/test_checkout.py:2-12`; snapshot r2 | CPython 3.12, as recorded | run_inspected | completed | no_counterexample_found | Receipt records two executed tests and zero failures. Test runner/version and native per-test logs are absent. Expectations encode the earlier discount and fallback policy, not approved revision 2. |
| Reported branch coverage establishes assertions of the currently required outcomes | `evidence/tests.json:6`; workflow coverage options at `.github/workflows/checks.yml:13` | Receipt: CPython 3.12; exact coverage tooling unknown | run_inspected | completed | unknown | Receipt reports 1.0; no per-file/branch report establishes denominator or exclusions. This is a recorded measurement, not a behavioral-correctness conclusion. Source tests exercise both catalog outcomes but assert the wrong failure outcome. |
| Reported mutation score establishes relevant assertion sensitivity | `evidence/tests.json:7`; snapshot r2 | Mutation environment/tool/version unknown | run_inspected | unknown | unknown | Score 0.98 is present, but no campaign inventory, completion state, operators, survivors, equivalent-mutant analysis, or requirement mapping was supplied. No mutation invocation appears in the workflow. |
| Existing semantic review applies to approved requirements revision 2 | `evidence/tests.json:8-12` names revision 1; `requirements.md:1-5` declares approved revision 2 | Requirement/assertion review; owner approval recorded 2026-10-10 | stale | unknown | unknown | Review records 10% discount and empty-list fallback. Both conflict with revision 2; no renewed semantic review is supplied. Execution status for a revision-2 review is unknown. |
| Current code and assertions implement REQ-DISCOUNT and REQ-ERROR | `checkout.py:1-7`; `tests/test_checkout.py:2-12`; `requirements.md:3-5` | Source inspection only | configuration_only | unknown | unknown | Direct textual contradictions are detailed below. No current-requirement test failure was executed or supplied; the passing suite does not validate these claims. |
| PR jobs run the checker and tests and reject a failing command | `.github/workflows/checks.yml:1-13`; checker exit at `tools/empty_except.py:13` | Configured GitHub Actions `ubuntu-latest` | configuration_only | unknown | unknown | Commands have no configured failure suppression. Receipts do not establish a particular CI job's execution, package provisioning, or enforcement at merge. |
| Merge requires the relevant checks and review | `README.md:4`; no hosting-settings artifact supplied | Hosting settings unavailable | not_inspectable | unknown | unknown | Required statuses, approvals, identities, bypass permissions, and protection settings cannot be inferred from workflow YAML. |
| Formal-model or proof obligations are active in this snapshot | Supplied inventory contains no formal files, proof markers, or claimed formal obligations | Supplied snapshot only | not_applicable | not_applicable | not_applicable | No formal-verification surface is declared here. This does not exempt the existing AST gate from sensitivity assessment, nor establish absence outside the snapshot. |

The test row's `no_counterexample_found` is limited to its encoded expectations and exercised cases; it does not mean the tests prove the approved requirements. No new run was performed for this assessment.

## Gate Coverage Summary

**Overall coverage**: 2 **Qualified** scoped rows, 1 **Partial**, 0 **Configured**, 6 **None**, 2 **Unknown**, and 0 wholly **Not applicable** rows. The two Qualified rows describe the same narrow AST checker from different risk perspectives; they are not two independent protections or category-wide assurance.

**Enforcement level**: The checker returns a nonzero exit on findings (`tools/empty_except.py:13`), and the PR workflow invokes it directly. Test failures are also configured to fail their command. This supports intended CI blocking behavior, not verified merge blocking. Actual hosting enforcement is unknown. No configured coverage threshold, mutation threshold, or semantic-review gate was found.

Maturity is partial: one narrow checker has inspected qualification evidence, and a test workflow exists. Broader error-contract enforcement and requirement/assertion review are missing. No evidence supports fitness-function maturity or a universal correctness score.

## Coverage Matrix

| Smell | Scoped claim / gate | Coverage status | Enforcement / feedback | Evidence / limits |
|-------|---------------------|-----------------|------------------------|-------------------|
| AI001: Plausible Fabrication | No dedicated import/type/API-contract gate found | None | None found in supplied configuration | Tests import the local module and use toy clients (`tests/test_checkout.py:1,4-9`). No independent provider/schema/consumer evidence establishes that `list_items()` matches a real integration. This is an evidence gap, not proof that the API is fabricated. |
| AI002: Cargo-Cult Patterns | No dead-code, abstraction, or proportionality gate found | None | None found | Small source has no evident large abstraction hierarchy; that observation is not an ongoing detection mechanism. No need to introduce an architecture tool solely to fill a category. |
| AI003: Architecture Astronaut | No size, layering, or architecture review gate found | None | None found | Workflow checks only empty handlers and tests. Excess abstraction is not demonstrated in this small snapshot. |
| AI004: Shallow Error Handling | Reject an exception handler whose entire body is `pass`, in the declared `checkout.py` scope | Qualified | Checker prints file, line, explanation, and repair suggestion, then exits nonzero; merge blocking unknown | `evidence/empty-except.json` supplies completed current run and allowed/violating controls. This narrow success excludes silent default returns: `checkout.py:6-7` returns `[]`, contrary to REQ-ERROR. Propagation and boundary validation remain unprotected. |
| AI005: Tests Mirroring Implementation | Mutation score mentioned; no inspectable mutation gate/campaign or requirement-review gate | Unknown | Mutation enforcement unknown | Tests assert observable outputs, not mock order, so mirroring is not established merely because they agree with code. They do preserve outdated behavior (`evidence/tests.json:8-12`). A reported score alone cannot establish independence or current intent. |
| AI006: Symmetry Without Substance | No duplication gate found | None | None found | No consequential duplicated structure is established by this tiny snapshot. Qualify a duplication check only if maintenance problems justify it. |
| AI007: Local Reasoning Violations | No magic-value, dependency-boundary, or complexity gate found | None | None found | `90` and `100` encode discount policy in `checkout.py:2`, while the approved policy changed. Merely naming the constants would not correct or verify the rule. |
| AI008: Implicit Drift | No pinning or deliberate-update enforcement found | None | None found | Workflow uses `ubuntu-latest` and `actions/checkout@v4` (`checks.yml:5-7,10-12`). Exact resolved action SHA, runner image, Python/pytest/coverage versions, dependency installation, and update process are unknown. Mutable references permit drift; changed deployed bytes are not demonstrated. |
| AI009: Happy-Path-Only Coverage | Branch measurement and explicit success/failure catalog tests | Partial | Test command configured to fail on assertions; no branch threshold | Receipt reports 100% branch coverage; test lines 11-12 exercise success and `OSError`. These are not happy-path-only tests. Failure is asserted as `[]`, which violates revision 2. Discount rounding/input boundaries lack supplied cases; measurement detail is unavailable. |
| AI010: Vacuous Tests | Falsifiable output assertions exist; reported mutation sensitivity is unqualified | Unknown | No assertion-sensitivity gate found; mutation policy unknown | A wrong value can fail the shown equality assertions, so these tests are not demonstrably vacuous. Their principal defect is stale expectations. No known-bad business-rule controls, detailed mutants, or old-versus-fixed demonstrations were supplied. |
| AI011: Vacuous Formal Specs | Existing AST gate has an effective nonempty predicate and two anti-vacuity controls | Qualified | AST gate configured in CI; ongoing control execution is not wired in supplied workflow | Checker predicate at `tools/empty_except.py:5-7` and completed control receipt support only its empty-handler rule. It is not vacuous merely because a broader error-contract defect passes. No active formal/proof artifact exists in this snapshot, so that sub-surface is inapplicable. No unrelated formal tool is warranted. |

## Gate Maturity and Oracle Review

| Mechanism | Position / enforcement | Feedback | Qualification / freshness | Trend visibility |
|-----------|------------------------|----------|---------------------------|------------------|
| `empty-except/1` | PR CI command; nonzero on findings; required-status enforcement unknown | File, line, reason, and suggestion; no explicit rule ID or native structured report in checker source | Current completed scan and controls. Stable narrow rule matches README; neither rule nor receipt claims business-error validation | One supplied receipt; history unavailable |
| Tests / branch measurement | Separate PR CI job; ordinary test failures configured to fail; no coverage threshold | Native runner output unavailable; supplied receipt only has aggregate results | Current test execution, stale business expectations. Python version recorded, pytest/coverage versions unknown | One receipt; no historical comparison |
| Mutation measurement | No workflow wiring supplied | Scalar score only | Campaign scope, completion, relevant kills, survivors, and semantic review unknown | None supplied |

| Consequential oracle | Adequacy | Sensitivity | Independence | Freshness |
|----------------------|----------|-------------|--------------|-----------|
| Empty-handler AST predicate | supported for the exact `pass`-only rule declared in `README.md:2-3`; gap for broader REQ-ERROR | supported for supplied `raise` and `pass` controls and recorded exit codes | supported for narrow syntactic examples whose expected classifications are directly inspectable; broad error-policy independence is outside this oracle | unknown semantic-review owner/date for the syntax policy; execution is current at declared r2 |
| Checkout test expectations | gap: `9000` and `[]` contradict approved revision 2 (`requirements.md:3-5`) | unknown for systematic relevant-defect sensitivity; assertions are falsifiable, but 0.98 lacks campaign detail | unknown provenance for revision-1 expected values; no independent provider/reference evidence; current requirements provide independent contradictory intent | gap: receipt explicitly ties review to revision 1, despite current source identity |
| Branch/mutation metrics interpreted as correctness | gap: neither metric specifies the current business outcome | unknown beyond reported branch metric; mutation details unavailable | unknown metric derivation and exclusions | unknown metric-tool/configuration identity; current receipt identity does not renew requirement review |

The responsible business reviewer is the checkout owner, who approved requirements revision 2 on 2026-10-10 (`requirements.md:2`). The earlier semantic review names requirement revision 1 but supplies no reviewer, review date, assertion/helper fingerprint, or approved exclusions. Record those as unknown rather than assuming approval transferred to revision 2.

## Git History Hygiene

| Signal | Gate exists? | Mechanism | Enforcement |
|--------|-------------|-----------|-------------|
| Commit message quality | None found in supplied files | No commitlint/gitlint or commit hook supplied | Unknown outside snapshot |
| PR descriptions | None found | No template or description check supplied | Hosting settings unknown |
| PR-to-issue linking | None found | No issue-link check supplied | Hosting settings unknown |
| Test coverage with changes | Tests configured; no changed-source/test requirement found | PR test job, with branch-report option | Job failure behavior configured; required merge check unknown |
| PR size awareness | None found | No size warning/limit supplied | Unknown outside snapshot |
| Review scaled to risk/diff size | None found | No CODEOWNERS or review policy supplied | Hosting settings unknown |

No commit history or PR metadata was supplied. Generic-message rates, fix/revert cycles, source/test change ratios, review activity, and trend scores cannot be calculated. Authorship and generation history are explicitly unrecorded (`README.md:5`); these findings make no authorship inference.

## Gap Analysis

### Unprotected smell categories

- **High-priority semantic defect: REQ-DISCOUNT.** Approved revision 2 specifies 15% off (`requirements.md:3`), while `checkout.py:2` computes 90% of the input and `tests/test_checkout.py:3` demands 9000 for 10000. That input unambiguously requires 8500 under the current percentage. This contradiction follows from reading the expressions; it is not a newly executed failing test. Add non-integral discount cases after making the intended rounding interpretation explicit.
- **High-priority semantic defect: REQ-ERROR.** Approved revision 2 requires catalog failures to propagate (`requirements.md:5`). `checkout.py:6-7` swallows `OSError` and returns `[]`; `tests/test_checkout.py:12` requires that outdated fallback. The known empty-handler control does not cover this separate defect class. The old fallback may have been intentional under revision 1, but it conflicts with the current approved contract.
- **Oracle rot affects otherwise falsifiable tests.** Both assertions align with the receipt's old semantic review. Neither green tests, reported full branch coverage, nor a high mutation score establishes current business correctness. The failure test is present and exercises the failure branch; changing its expected outcome is essential.
- No relevant configured gates were found for AI001, AI002, AI003, AI006, AI007, or AI008. Prioritize contract/error and resolution risks over adding every taxonomy tool to this small project. Mutation-related evidence for AI005/AI010 remains unknown.

### Weak enforcement

- No evidence establishes that CI statuses or reviews are required for merging. YAML presence and current local-environment receipts do not establish hosting enforcement.
- The current checker scope is explicitly just `checkout.py`. Extending application paths without updating this scope could leave new code unanalyzed.
- Allowed/violating controls exist and were recorded as completed, but the supplied PR workflow does not run them. Continuous checker qualification is not demonstrated.
- The test command requests branch coverage but sets no threshold. Mutation execution and policy are absent from supplied configuration.
- CI dependency provisioning and versions are unspecified in the supplied workflow. Whether jobs have the required pytest/coverage tooling is unknown; no failure is asserted without a run artifact.

### Missing fitness functions

- No historical findings, per-PR metric deltas, false-positive reviews, or resolution times were supplied.
- More valuable than raising a score is tracking which current requirements have reviewed assertions and relevant rejecting controls. Coverage and mutation trends should retain scope/tool identity and survivor analysis.
- No deliberate pin-update process is documented. Absence of a particular dependency bot does not prove that no process exists outside this snapshot.

## Recommendations

These are proposed changes, not existing successful evidence. This assessment changed only the report and executed no target checks.

### Quick wins (add to existing CI)

1. Align the discount implementation and assertions with approved revision 2, and require catalog errors to propagate. Review the requirement-to-assertion relationship with the checkout owner; record requirement, assertion, fixture/helper revisions, review date, and accepted rounding/error scope.
2. Preserve the existing happy and failure cases, correcting the failure oracle. Add a discount case whose 10% and 15% outcomes differ, rounding cases, and approved input boundaries. Demonstrate that the revised tests reject the comparable old implementation and accept the fix when execution is authorized.
3. Run both existing AST controls in CI with their expected exit codes, separately from the production scan. Preserve the checker version, source inventory, completion, findings, and control outcomes. Do not treat a missing or skipped required control as success.
4. Make test tooling provisioning reproducible and record resolved versions. Pin the checkout action to an immutable reviewed revision and document a deliberate update process; retain runner/environment identity in receipts.

### New gates to introduce

1. Add a narrowly scoped REQ-ERROR behavior gate: a client raising `OSError` must cause catalog failure to propagate, while a valid empty result must remain distinguishable and allowed. Qualify using the current swallowing implementation as a violating control and reviewed propagation behavior as an allowed control. Retain per-case completion and results. This checks the supplied adapter contract; it does not prove real-provider compatibility.
2. Add a requirement/assertion review checkpoint when a linked requirement or expected value changes. Fresh execution is necessary for results, but a hash update is not semantic approval. Require review of whether the expected outcome still represents approved intent.
3. If mutation testing remains an advertised gate, expose the actual command/configuration, versions, mutants, outcomes, completion, and survivors. Include relevant discount and error-swallow mutations. Distinguish equivalent/out-of-scope survivors and timeouts; do not substitute a score for requirement review.
4. If `client.list_items()` targets a real dependency, add independent provider/schema or consumer contract evidence for the supported version and failure cases. A qualified twin can help where appropriate but is optional and has explicit fidelity limits.

### Strengthen existing gates

1. Keep the empty-handler rule's declared scope explicit. Either add separate, qualified checks for prohibited fallback patterns or rely on behavior tests for the approved error contract. Avoid banning every `return []` without regard to intended empty results and approved recoveries.
2. Inventory expected source paths and executed checks. Verify missing files, parser failures, missing reports, and skipped checks produce visible outcomes under project policy.
3. Retain per-branch coverage details if coverage will guide additions. Cover important rejected/boundary outcomes and meaningful assertions before selecting a threshold.
4. Inspect actual required-check and bypass settings when access becomes available. Until then, keep merge enforcement unknown.
5. Add a short review checklist for proportionality and semantic changes. Introduce dead-code, duplication, complexity, or formal tools only when the project's concrete risks justify their cost.

## Human Review Heuristics

No human-review guide, PR checklist, ADR, or design-oriented style guide was supplied. The versioned requirements and owner approval are useful intent evidence but are not a complete review process.

### Proportionality

- Does this small checkout helper need a new abstraction or gate, and which concrete failure would it prevent?
- Is the gate's claim no broader than its supported source scope and controls?

### Coherence

- Do implementation, tests, error policy, and the latest approved requirement agree?
- Does a dependency failure remain distinguishable from a legitimately empty catalog?

### Clarity

- Can a reviewer explain why the discount percentage and rounding expectation are correct without copying the implementation?
- Do findings identify the file, line, violated claim, and useful correction?

### Appropriateness

- Can the team maintain the proposed checks, review their exceptions, and deliberately update pins?
- Are green metrics being interpreted within their actual scope, with stale semantic reviews and inaccessible enforcement settings still visible?
