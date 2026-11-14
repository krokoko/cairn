# AI Readiness Report

## Evidence Scope

**Source revision**: `configured-only-r2`, as declared by `snapshot.json:2`. This is fixture identity, not a verified Git commit or execution revision. No Git metadata or change manifest is supplied, so the actual commit and relevant uncommitted changes are unknown.

**Assessment date**: 2026-10-11.

**Inspected scope**: All five supplied files: `ledger.py`, `tests/test_ledger.py`, `.github/workflows/test.yml`, `README.md`, and `snapshot.json`. The assessed surface is the ledger total function together with its Python runtime and configured CI check. No additional application, packaging, deployment, or production surfaces are represented; this report does not recommend autonomy for any such external surfaces.

**Evidence basis**: Static inspection only, using the named frozen assess-readiness skill and its relevant references. No target checks were executed and no remote state was retrieved. `README.md:2` explicitly says that run artifacts and hosting settings are not included. Historical local/CI execution, required branch checks, production behavior, review approvals, Git/PR history, and collaboration outcomes are not inspectable. No prior assessment was reused. `snapshot.json:3` describes a synthetic snapshot; it is not evidence of a runtime environment or completed run.

## Evidence Ledger

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| `total([2, 3])` is expected to equal `5` | `tests/test_ledger.py:1-5`, supplied identity `configured-only-r2` | Local Python/unittest intended; no runtime observed | configuration_only | unknown | unknown | Literal expected value is independent of the implementation's `sum` call. One positive integer example is declared; no execution result or semantic review is supplied. This assessment did not run it. |
| Pull requests are configured to invoke unittest discovery | `.github/workflows/test.yml:1-8`, supplied identity `configured-only-r2` | GitHub Actions `ubuntu-latest` configured; actual runner unknown | configuration_only | unknown | unknown | One job checks out source and invokes `python3 -m unittest discover -s tests`. No run ID, completion, source checkout, Python version, missing/skipped checks, or flakiness history can be inspected. |
| Local test command is documented | `README.md:2`, supplied identity `configured-only-r2` | Local Python intended; actual environment unknown | configuration_only | unknown | unknown | Matches the workflow command. Documentation does not establish setup reproducibility or a successful invocation. |
| Required CI checks and branch protection enforce the merge gate | No hosting settings supplied; exclusion stated in `README.md:2` | Hosted repository settings unavailable | not_inspectable | unknown | unknown | Workflow existence cannot establish required checks, protection, bypass restrictions, or merge safety. |
| Test meaning is approved against the intended ledger contract | `ledger.py:1-2`, `tests/test_ledger.py:4-5`; no requirement/review records or history supplied | Review context unavailable | not_inspectable | unknown | unknown | The function delegates to Python `sum`; allowed inputs, empty-input behavior, precision, and failure semantics are not documented. External approval or intent cannot be inferred. |
| Detection and recovery cover wrong-but-not-crashing outcomes | No operational records or hosting settings supplied | Deployment/release environment unavailable | not_inspectable | unknown | unknown | No observed detection exercise, rollout, containment, or recovery evidence. The snapshot does not describe a release model. |

The execution state of prior runs is **unknown**, not `not_run`. The prohibition on running checks establishes only that this assessment did not execute them. No claim above qualifies as `established_within_scope` or `no_counterexample_found`.

## Overall Score

**Score:** provisional **29/100**.

**Rubric:** readiness-scoring/2.

**Assessed weight:** **0.90 / 1.00 (90%)**. CI reliability (weight 0.10) is excluded as `unknown`: a configured workflow is visible, but neither execution reliability nor required-check enforcement is inspectable. Weighted subtotal is 26.05; `26.05 / 0.90 = 28.94`, rounded to 29. Other scores describe the supplied code and configuration, not demonstrated execution. Missing repository artifacts are scored only as absences in this snapshot. This small fixture does not establish the maturity of an upstream repository or team.

## Recommended Autonomy Level

**Level**: L1

**Summary scope:** Ledger total and Python/CI dependencies. Agents can explain the implementation and draft small changes or checks; a human owns behavior decisions and review. A supported execution baseline is needed before treating agent changes as reviewed, repeatable delivery work.

**Decision boundary:** This is a diagnostic recommendation only. It grants no permission to merge, deploy, change hosting settings, or use additional tools.

**Autonomy cap applied:** Yes. Category 2.8 is 30, reviewed executable intent is absent from the supplied artifacts, and current critical-path oracle evidence is unknown; these independently prevent recommendations above L3. Reliable bounded iteration is also unproven, so the surface evidence ceiling is L2. All five L5 gates are unmet or unknown. The score maps to L1, which is lower than these ceilings and determines the recommendation.

## Surface Autonomy

| Surface | Provisional level | Evidence ceiling | Recommended level | Operating scope | Blockers |
|---------|-------------------|------------------|-------------------|-----------------|----------|
| Ledger total and Python/CI dependencies | L1 | L2 | L1 | Draft changes to the small pure calculation and its tests; human specifies supported behavior and reviews changes. Python/runtime or CI changes require the same review and a recorded execution baseline. | Only one configured example; no inspected runs, approved contract, pinned runtime, type checks, or inspectable required-check enforcement. These gaps prevent reliable bounded iteration and higher autonomy. |

## Autonomy Prerequisites

| Surface | Prerequisite | Status | Evidence / gap |
|---------|--------------|--------|----------------|
| Ledger total and Python/CI dependencies | L4-INTENT | missing | No reviewed executable requirement record or approval mapping is included. `README.md:1-2` gives a title and test command; `tests/test_ledger.py:4-5` declares one unreviewed example. |
| Ledger total and Python/CI dependencies | L4-ORACLES | unknown | Literal expectation can be inspected, but no completed execution, reviewed supported-input scope, or critical-case adequacy evidence is supplied. |
| Ledger total and Python/CI dependencies | L5-INTENT | missing | No approved, revisioned claims covering all critical behavior and mapped to executed checks are supplied. |
| Ledger total and Python/CI dependencies | L5-ORACLES | unknown | Current execution, full critical-path scope, oracle review, and known-bad sensitivity controls are unavailable. |
| Ledger total and Python/CI dependencies | L5-ENVIRONMENT | unknown | The workflow declares `ubuntu-latest`, but no run/runtime details or representative consumer/release environment evidence exists. Fixture metadata is not environment execution evidence. |
| Ledger total and Python/CI dependencies | L5-DETECTION | unknown | One configured example cannot demonstrate exercised detection of silent incorrect totals or an operational response. No corresponding records are supplied. |
| Ledger total and Python/CI dependencies | L5-RECOVERY | unknown | No release model, controlled rollout/version rollback rationale, or exercised recovery record is supplied. The appropriate library-scale control remains to be established. |

## Category Breakdown

| Category | Score | Notes |
|----------|-------|-------|
| Structure and modularity | 60 | `ledger.py:1-2` is a cohesive, IO-free calculation, with a separate test file and no application imports or visible cycles. No boundary enforcement is configured. The tiny scope does not justify additional modules solely to improve the score. |
| Documentation | 25 | `README.md:1-2` identifies the utility and canonical check command. Input/output semantics, installation/runtime setup, API guidance, and rationale are absent from the snapshot. |
| Testable boundaries | 30 | `tests/test_ledger.py:4-5` has a meaningful independent literal expectation for two integers; the pure function is easy to exercise. Critical behavior is unspecified, and no edge/failure cases, sensitivity controls, or execution evidence are supplied. |
| CI reliability | unknown | `.github/workflows/test.yml:1-8` configures one pull-request test job. Completion, revision, skipped checks, flakiness, and required enforcement are unavailable; configuration alone is not reliability evidence. |
| Typing strength | 0 | The supplied function has no annotations, and no type-checker configuration or invocation is supplied. This is observed absence of typing mechanisms in the snapshot. |
| Deterministic environment and deployment | 20 | The command uses only Python's standard library, and the function has no time/random/IO dependency. Python is not pinned or set up explicitly; `ubuntu-latest` is mutable. No setup or release definition is supplied, and actual deployment needs are unknown. |
| Architecture decisions | 0 | No decision record, design note, ownership declaration, or decision-to-check mapping is included. This is an artifact gap, not evidence that a complex architecture is needed. |
| Machine-readable intent | 30 | The literal unittest assertion supplies a narrow executable criterion and the core is separable. No approved requirement records, contract, stable claim mappings, or semantic review are included. PR-to-issue traceability is not inspectable without history. The spec-first maximum of 60 is not approached; missing reviewed intent also triggers the autonomy cap. |
| Progressive context disclosure | 15 | One two-line README is the only context entry point; there are no agent instructions, deeper docs, plans, or cross-links in the supplied files. |
| Hidden state and magic | 70 | `ledger.py` visibly uses only its argument and built-in `sum`, with no environment variables, mutable state, or ambient clock/randomness. Input protocol and Python version remain unspecified, so this observation does not establish deterministic behavior for arbitrary supplied objects. |
| Repository-scale reasoning | 60 | `ledger.py`, `total`, and `tests/test_ledger.py` are easy to associate, and the documented and CI commands agree. There is no multi-module evidence from which to generalize about larger-scale change behavior. |
| Failure mode legibility | 35 | No exception swallowing or fallback is visible; Python failures would propagate. Domain error behavior, explanatory validation, and actionable remediation are not documented or exercised. |
| Feedforward surfaces | 5 | A test command is documented, but no agent rules, type checker, linter, hooks, templates, or boundary guards are supplied. Hosting-level bypass controls remain unknown rather than presumed absent. |
| Compound engineering readiness | 10 | The test offers a durable check location. No incident linkage, maintained guidance, packaged agent workflow, plans, or review-learning artifacts are supplied; historical maintenance cannot be inspected. |
| Context engineering friendliness | 55 | The production source is 2 lines and the test source 5 lines, with no generated/vendor source. There are no size outliers or unrelated concerns to split; the function is directly discoverable. Layered guidance and representative maintenance outcomes are missing. Brevity alone does not demonstrate maintainability. |

## Workflow artifacts

| Artifact type | Present | Location / notes |
|---------------|---------|------------------|
| Requirements / specs | no | No feature-scoped requirements/spec directories or approved contract records supplied. The single test is an example, not evidence of reviewed requirements. |
| Design / blueprints | no | No design directory or decision records supplied. |
| Execution plans | no | No plans directory or `PLANS.md` supplied. |
| Review / learnings | no | No review or learning records supplied. |

**Summary:** All four artifact classes have zero supplied records. The README and single assertion are the available context, but do not capture contract decisions or review history. Artifact recency and version-control maintenance are not inspectable. For this utility, a short reviewed contract and task/review notes would be proportionate; extra directories without useful content would not improve readiness.

## Collaboration effectiveness

| Metric | Status | Notes |
|--------|--------|-------|
| First-pass acceptance | not measured | No agent task/PR outcomes or acceptance records supplied. |
| Iteration cycles per task | not measured | No review rounds or task histories supplied. |
| Post-merge rework (7-day) | not measured | No merge history, fixes, or reverts supplied. |

**Infrastructure:** No PR template, label configuration, agent review rubric, or learning docs are supplied. Remote labels and actual review practices are not inspectable. The workflow supplies a place to run checks, but does not establish collaboration quality.

**Maintenance outcome:** Not measured. A useful future exercise is to agree and document empty-input behavior, then add its acceptance check at `tests/test_ledger.py`. Record the baseline revision, expected edits to the contract/test and any needed implementation, unexpected file changes, elapsed effort and review cycles, completed check results, regressions, and any boundary violations. This exercise was not performed during assessment.

**Recommendations:**

1. Start with the concise behavioral contract and canonical setup/check instructions in roadmap items 1 and 3; these supply context for human-reviewed drafts.
2. For the next small agent-assisted change, retain scope, correction rounds, and the human decision in a task note; this is roadmap item 7.
3. Review comparable tasks for rework after seven days and convert recurring corrections into a specific instruction or independently expected regression case; report outcomes rather than inferring improvement from test counts.

**Alignment note:** No practices/codebase mismatch can be established. Supplied collaboration infrastructure is sparse and the diagnostic score maps to L1; actual team practices are not measured.

## Blockers

- **Moving from L1 toward L2:** The configured test and workflow have no inspectable completed execution. `README.md:2` explicitly limits the snapshot, so success, failure, and required-check enforcement remain unknown.
- **Behavioral decisions:** `ledger.py:1-2` exposes `sum` without a documented supported-input contract. The `[2, 3] → 5` example does not resolve empty inputs, numeric types/precision, or invalid-input behavior. A human must define which are relevant before expanding checks.
- **Repeatable iteration:** No pinned Python version, typing gate, or documented setup is supplied. A mutable CI runner and an unspecified local `python3` leave runtime correspondence unverified.
- **Higher-level ceilings:** Reviewed executable intent is missing, current oracle evidence is unknown, and no L5 gate is met. Neither successful future execution alone nor higher artifact counts would resolve semantic review or operational evidence gaps.

## Roadmap

These are proposed actions and future acceptance criteria; none was executed or validated as part of this assessment.

| Priority | Action | Category | Effort | Failure addressed | Acceptance criterion |
|----------|--------|----------|--------|-------------------|----------------------|
| 1 | Have the owner define the supported `total` input/output and failure contract in a short versioned record, including the relevant empty-input and numeric-type decisions; map claims to test names. | Machine-readable intent; Documentation | small | Agents infer requirements from the current implementation. | Approved revisioned claims state supported scope, examples, exclusions, and linked executable criteria; the existing `5` expectation is reviewed against them. |
| 2 | Add only the contract-relevant boundary/failure cases with independent expected values, plus a deliberate wrong-result control in an isolated verification exercise. | Testable boundaries; Machine-readable intent | small | The sole positive example may miss important incorrect totals or irrelevant expectations. | Reviewed cases cover each critical claim; a future retained run includes expected test inventory, completion, revision, and a demonstrated failure for the selected known-bad control. |
| 3 | Document and select a supported Python version for local use and CI, and add explicit CI runtime setup. | Deterministic environment and deployment; Documentation | small | Local and CI behavior depend on unspecified Python/runtime state. | A clean setup using the documented runtime can invoke the canonical command; future evidence records the exact Python version and source/dirty identity. |
| 4 | Obtain an actual local/CI check record for the target revision and inspect required-check settings before promoting autonomy. | CI reliability | small | A configured workflow is mistaken for completed or enforced checks. | Retained expected/actual check results show completion and any skips/failures, bind to source and environment, and separately document whether hosting protection requires them. Unavailable settings remain unknown. |
| 5 | Add contract-appropriate type annotations and a focused strict type check to the documented command/CI path. | Typing strength; Feedforward surfaces | small | Unsupported argument or return shapes reach runtime without early feedback. | The declared supported API type-checks, and a deliberately invalid call is rejected; relevant runtime-only limits are documented. |
| 6 | Add concise `AGENTS.md` guidance linking the contract, supported runtime, test command, and human review boundary. | Progressive context disclosure; Feedforward surfaces | small | Each new session must rediscover behavior decisions and how to check changes. | A reader can locate the contract and canonical checks from the entry document; every rule is specific to this utility and agrees with the actual configuration. |
| 7 | Retain a small task/review record for the proposed maintenance exercise, including corrections and subsequent rework. | Compound engineering readiness; Context engineering friendliness | small | No evidence shows whether scoped work remains scoped or lessons improve later changes. | Record expected/actual files changed, effort, review cycles, relevant execution evidence, regressions, and seven-day follow-up; recurrent issues lead to a reviewed rule or regression case. |
| 8 | Before considering L5, document the actual consumer/release model and the appropriate silent-error detection and controlled version recovery process; exercise those controls if that operating scope is desired. | Failure mode legibility; Deterministic environment and deployment | medium | A library-scale autonomy claim assumes production fidelity, detection, and recovery without evidence. | Review an explicit equivalence rationale and retain scope-bound records of a representative wrong-total detection, response, and recovery exercise. Until then, operational gates remain unknown. |
