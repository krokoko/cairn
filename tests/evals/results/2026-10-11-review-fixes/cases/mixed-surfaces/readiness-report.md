# AI Readiness Report

## Evidence Scope

**Source revision**: `mixed-surfaces-r2`, declared in `snapshot.json:2`. This is a fixture identity, not a verified Git commit or proof of any execution. No Git metadata or dirty-file record is supplied; correspondence to a commit and relevant uncommitted changes are unknown.

**Assessment date**: 2026-10-11.

**Inspected scope**: All seven supplied files: `README.md`, `core.py`, `provider.py`, `requirements.md`, `tests/test_core.py`, `evidence/core.json`, and `snapshot.json`. Surfaces are the pure integer-cent arithmetic core and the provider adapter, including its externally supplied client. No other repository, live plugin source, remote service, or remote history was inspected. Provider implementation internals and production operations are outside the supplied material and remain unknown dependencies, not qualified exclusions.

**Evidence basis**: Static source and document inspection plus the retained summary `evidence/core.json`. No target checks were executed and no remote state was retrieved. The core summary declares the same source identity and requirement review `r2`, 20 executions, zero failures, and a detected negative control. It does not supply an explicit completion record, expected check inventory, case list, control implementation, exact runtime/tool versions, or campaign bounds. Its environment is only “supported Python runtime.” These limitations prevent treating it as complete, adequate verification of the current core claim. `snapshot.json` contributes identity only. No prior assessment was reused. CI history, branch protection, PR history, and collaboration outcomes are not inspectable.

## Evidence Ledger

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| Integer-cent totals equal the sum of item amounts | `requirements.md:1-2`, reviewed `r2`; `core.py:1-2`; `tests/test_core.py:1-3` | local Python, exact version unspecified | configuration_only | unknown | unknown | Reviewed claim and executable example are inspectable. The literal expectation 500 is independent of `sum`; the single visible case does not establish the full input domain. The test has no explicit requirement annotation, though the function and assertion make this narrow mapping apparent. |
| Retained core arithmetic campaign | `evidence/core.json:1`, declared `mixed-surfaces-r2`, requirement review `r2` | supported Python runtime, otherwise unspecified | run_inspected | unknown | unknown | Reports 20 executions and zero failures for core arithmetic only. Completion, expected inventory, cases, and tool/configuration identity are absent. Matching fixture identities do not establish byte-level freshness or completion. |
| Core negative-control sensitivity | `evidence/core.json:1`, `negative_control_detected: true` | supported Python runtime, otherwise unspecified | run_inspected | unknown | unknown | Sensitivity is reported, but the deliberately wrong implementation/input, expected rejection, and actual control output are unavailable. This is not evidence of provider qualification or operational detection. |
| Provider charge boundary | `provider.py:1-2`; `README.md:2` | external client, actual environment unknown | configuration_only | unknown | unknown | README explicitly says the adapter has no contract or environment qualification. No provider tests or run artifact are supplied. `client.charge(sum(items))` has external side effects and recomputes the total rather than invoking the tested `total` function. |
| Local gate scope restriction | `README.md:2` | N/A — documented change policy | configuration_only | unknown | unknown | Only core changes may use the existing local gates. Commands, gate configuration, enforcement, and completion history are not supplied. This statement does not authorize provider changes under the core evidence. |
| CI reliability and merge enforcement | No workflow/protection export or CI history supplied | CI / hosted repository unavailable | not_inspectable | unknown | unknown | Absence of CI configuration in this snapshot is observed; actual CI reliability and server-side settings cannot be determined. |
| Representative provider behavior and recovery | `README.md:2`; no staging, detection, or recovery artifacts supplied | staging / deployed unavailable | not_inspectable | unknown | unknown | No inspection of the real client, charge semantics, fault behavior, rollout, or rollback was possible. Operational absence outside the snapshot is not inferred. |

## Overall Score

**Score:** provisional 39/100.

**Rubric:** readiness-scoring/2.

**Assessed weight:** 0.90 of 1.00. CI reliability (weight 0.10) is unknown and excluded: neither reliable execution nor server-side enforcement can be inspected. The weighted numerator is 35.40; `35.40 / 0.90 = 39.33`, rounded to 39. All other scores describe supplied artifacts, with their stated limits. Missing run evidence is not scored as a successful control. Normalization does not satisfy the unknown CI prerequisite.

## Recommended Autonomy Level

**Level**: L1

**Summary scope:** This conservative repository summary covers both the arithmetic core and the provider adapter with its external client. Core-only work supports L2 reviewed changes; provider work remains L1 assisted drafting. Changes to provider semantics or shared input assumptions must use the provider's lower level. No deployed behavior is qualified by this assessment.

**Decision boundary:** Recommendations do not grant permission to merge, deploy, charge a customer, or invoke the provider. Humans own intent changes and acceptance; provider behavior requires explicit human decisions.

**Autonomy cap applied:** Yes. The score provisionally maps to L2. Incomplete critical-path evidence and unproven enforced feedback prevent L3 for the core. The provider's missing contract and qualification justify a lower L1 ceiling. Neither surface satisfies both L4 scope prerequisites or all five L5 gates. Stronger core evidence cannot be transferred to the provider.

## Surface Autonomy

| Surface | Provisional level | Evidence ceiling | Recommended level | Operating scope | Blockers |
|---------|-------------------|------------------|-------------------|-----------------|----------|
| Arithmetic core | L2 | L2 | L2 | Small changes confined to `core.total` under the reviewed integer-cent sum requirement, with human review and explicit examination of changed assertions. No claim of autonomous merge or reliable unattended iteration. | Core evidence is local and summarized; completion, bounds, control details, tool versions, strict typing, and enforceable gates are unverified or absent from the snapshot. L4-ORACLES is unknown. |
| Provider adapter and external client | L2 | L1 | L1 | Draft proposed adapter changes for human evaluation. Humans define and review charging semantics, dependency assumptions, and acceptance evidence before implementation is relied upon. | README explicitly disclaims a provider contract and environment qualification. No adapter checks are supplied; external side effects and failure semantics are unknown. Core local gates do not cover this surface. |

## Autonomy Prerequisites

| Surface | Prerequisite | Status | Evidence / gap |
|---------|--------------|--------|----------------|
| Arithmetic core | L4-INTENT | met | `requirements.md:1-2` marks REQ-TOTAL reviewed at `r2`; `tests/test_core.py:1-3` provides a directly inspectable executable sum example against `core.total`. This supports only the narrow integer-cent sum scope; invalid inputs and provider behavior are excluded from that claim. |
| Arithmetic core | L4-ORACLES | unknown | `evidence/core.json:1` reports 20 executions, zero failures, and control detection, but lacks explicit completion, case bounds, control details, and exact environment. The visible independent expectation is useful but insufficient to qualify all paths of the proposed core scope. |
| Arithmetic core | L5-INTENT | unknown | The reviewed claim exists, but the summary does not map an expected complete check inventory to current assertions. Complete critical-behavior coverage and the semantic review of unseen cases are unverified. |
| Arithmetic core | L5-ORACLES | unknown | No inspectable campaign cases, sensitivity reproducer, or reviewed bounds accompany the result summary. All critical-path adequacy cannot be established. |
| Arithmetic core | L5-ENVIRONMENT | unknown | “Supported Python runtime” in `evidence/core.json:1` has no exact version, support matrix, package-consumer qualification, or reviewed equivalence rationale for this library. |
| Arithmetic core | L5-DETECTION | unknown | A detected negative control is reported, but the control and response are not inspectable. No evidence demonstrates detection of wrong totals at the library's operational boundary. |
| Arithmetic core | L5-RECOVERY | missing | No package rollout, version rollback, containment procedure, or exercised library-specific recovery equivalent is supplied. |
| Provider adapter and external client | L4-INTENT | missing | `README.md:2` explicitly states the adapter has no contract; REQ-TOTAL specifies arithmetic only and does not define charging behavior or critical dependency assumptions. |
| Provider adapter and external client | L4-ORACLES | missing | No provider check or qualification artifact exists in the supplied snapshot; `evidence/core.json:1` expressly covers core arithmetic only. |
| Provider adapter and external client | L5-INTENT | missing | Approved executable claims for charge amount, success/failure outcomes, and other required provider behavior are absent from the supplied artifacts. |
| Provider adapter and external client | L5-ORACLES | missing | No provider expectations, known-bad controls, representative fault checks, or completed qualification are supplied. |
| Provider adapter and external client | L5-ENVIRONMENT | missing | `README.md:2` explicitly disclaims environment qualification. The injected client alone supplies a test seam, not representative evidence. |
| Provider adapter and external client | L5-DETECTION | unknown | The code returns the client result. Actual wrong-charge detection, telemetry, and response cannot be inspected from these files. |
| Provider adapter and external client | L5-RECOVERY | unknown | No recovery evidence is supplied and the external client's capabilities are unavailable. Neither safe retries nor compensation/rollback behavior may be inferred. |

## Category Breakdown

| Category | Score | Notes |
|----------|-------|-------|
| Structure and modularity | 65 | Pure arithmetic and an injected-client adapter are visibly separate (`core.py`, `provider.py`). No boundary checker or declared public API exists. The provider duplicates `sum` rather than depending on the tested core function. |
| Documentation | 25 | Two-line README explains the boundary and local-gate restriction; one reviewed requirement exists. Setup, execution commands, API behavior, and change guidance are absent. |
| Testable boundaries | 55 | The pure core and injected client are testable seams. One visible assertion has an independent literal expected result; the retained core summary adds limited historical evidence. Provider assertions and dependency fidelity are absent. |
| CI reliability | unknown | No workflow or CI history is supplied. README's mention of local gates cannot demonstrate completed required checks, flakiness, or merge enforcement. |
| Typing strength | 0 | Both Python functions and the injected client are unannotated; no type configuration or typed boundary is supplied. This is observed absence in the snapshot. |
| Deterministic environment and deployment | 10 | Core arithmetic has no ambient time/randomness or I/O. No pinned Python environment, dependency manifest, setup command, or codified deployment is supplied; the report's generic environment is not reproducibility. |
| Architecture decisions | 20 | README states the pure-core/provider distinction and gate restriction. No ADR, owner mapping, rationale record, or decision-to-enforcement link is supplied. |
| Machine-readable intent | 60 | Reviewed REQ-TOTAL and an executable literal assertion provide narrow intent and criterion correspondence; `evidence/core.json` references review `r2`. Completion and unseen assertion meaning remain unknown; provider intent is absent. The no-reviewed-intent cap does not erase the core's reviewed record, but no complete critical-surface claim is justified. |
| Progressive context disclosure | 25 | README is a minimal entry point. No agent guide, links to requirements/evidence, module documentation, or execution plan is supplied. |
| Hidden state and magic | 65 | Core behavior is explicit with no environment lookups. The client is an explicit parameter, but client configuration, side effects, failure behavior, and supported inputs are undocumented. |
| Repository-scale reasoning | 70 | Names and three short Python files are easy to navigate. `total` and `charge` are distinct concepts; duplicated aggregation creates a potential divergence point. No representative maintenance outcome verifies change locality. |
| Failure mode legibility | 30 | No exception swallowing or silent fallback is visible. Errors propagate without documented identifiers, context, invalid-input policy, or adapter remediation guidance. |
| Feedforward surfaces | 15 | README gives one relevant scope restriction and REQ-TOTAL defines a core rule. No strict types, lint configuration, hook, boundary enforcement, agent instructions, or templates are supplied. |
| Compound engineering readiness | 30 | A reviewed requirement and retained core result provide durable material. No review learnings, active plan, packaged workflow, or evidence of corrections improving subsequent work is supplied. |
| Context engineering friendliness | 65 | Source sizes are 2 lines each for `core.py` and `provider.py`; the test is 3 lines. All are cohesive enough to inspect directly. Missing layered guidance and extension documentation limit onboarding. Short lengths alone do not demonstrate maintainability. |

## Workflow artifacts

| Artifact type | Present | Location / notes |
|---------------|---------|------------------|
| Requirements / specs | yes | One root file, `requirements.md`, contains reviewed REQ-TOTAL at revision `r2`. No calendar review date or reviewer identity is supplied. |
| Design / blueprints | no | README contains a brief scope distinction; no dedicated design document or ADR is supplied. |
| Execution plans | no | No plans directory, progress log, or task plan is supplied. |
| Review / learnings | no | No review or learning record is supplied. `evidence/core.json` is a result summary, not a review decision or retrospective. |

**Summary:** Feature intent is durable only for the core arithmetic claim. There is one requirement file and one evidence summary; no workflow artifact directories are present. Revision `r2` is visible, but temporal recency and maintenance history cannot be determined. Provider intent and resumable task context are missing.

## Collaboration effectiveness

| Metric | Status | Notes |
|--------|--------|-------|
| First-pass acceptance | not measured | No agent-assisted PR sample, review outcomes, or acceptance records are supplied. |
| Iteration cycles per task | not measured | No task logs or review history are supplied. |
| Post-merge rework (7-day) | not measured | No Git/PR history or dated follow-up records are supplied. |

**Infrastructure:** No PR template, agent labels, agent review rubric, packaged workflow, or learning notes are supplied. The reviewed requirement and README's core-only gate restriction provide a small starting point. PR-to-issue traceability is not inspectable, rather than established absent.

**Maintenance outcome:** Not measured. A future exercise could add an agreed core input case under REQ-TOTAL, retaining the baseline identity, expected files, actual edit spread, effort/correction rounds, check results, regressions, and boundary violations. A separate provider exercise must first define a provider contract and representative client. No exercise was performed during this assessment.

**Recommendations:**

1. Add task surface, requirement revision, expected check inventory, evidence limits, and correction-round fields to a PR template; use human review for core changes and explicit provider intent review for adapter proposals.
2. Retain first-pass acceptance and seven-day rework for comparable core tasks, with scope and sample size; do not combine these with unqualified provider tasks.
3. Record recurring corrections in linked guidance and sensitive regression cases, then inspect whether the next comparable task uses them. These steps pair with roadmap items 1–4 and 7.

**Alignment note:** No supported mismatch is established. The provisional score maps to L2, collaboration infrastructure is sparse, and actual collaboration outcomes are unmeasured. Do not infer organizational maturity.

## Blockers

- **Core L2 to L3:** No inspectable reliable blocking CI, strict type checking, pinned runtime, complete current campaign record, or documented local gate command. The existing run summary alone cannot support unattended bounded iteration.
- **Provider L1 to L2:** No reviewed charging contract, provider-specific tests, representative client qualification, or inspectable CI feedback. Define the client interaction and failure semantics before relying on generated implementation changes.
- **Both surfaces toward L4:** The core oracle's adequacy/completion is unknown; the provider lacks both scoped executable intent and oracle evidence. A higher arithmetic score cannot cancel the provider gap.
- **Both surfaces toward L5:** Complete reviewed critical behavior, representative environment evidence, exercised silent-failure detection, and recovery evidence remain missing or unknown as recorded separately above.

## L2 → L3 hinge

**Codebase critical path:** For the core, establish reproducible completed tests, justified reliability observations, strict type checking, explicit boundaries, and inspected merge enforcement. The adapter must first acquire its own reviewed contract and checks before it can follow that transition.

**Repo enablers:** Pair these controls with an agent entry guide linking intent/evidence, a test-with-code review policy, feature plans for adapter qualification, and task metadata that preserves correction cycles and limitations.

## Session infrastructure (dual track)

Maintain executable controls alongside feature context: gate/evidence repair with an evidence review record; strict types with project guidance; adapter checks with an approved qualification plan. The roadmap pairs these so missing shared context is addressed with the codebase gaps.

## Roadmap

| Priority | Action | Category | Effort | Failure addressed | Acceptance criterion |
|----------|--------|----------|--------|-------------------|----------------------|
| 1 | Recover or produce a complete core check record and document its requirement/assertion review in a linked evidence note. Preserve explicit completion, expected/actual cases, runtime/tool/config versions, source identity and dirty changes, and the negative-control reproducer. | Testable boundaries; Machine-readable intent; Compound engineering readiness | small | A terse green summary is mistaken for adequate complete evidence. | A reviewer can trace REQ-TOTAL `r2` to the actual independent assertions and expected inventory; the complete campaign and known-bad control have inspectable outcomes and explicit input bounds. |
| 2 | Add a pinned Python/test setup and PR checks for core tests and linting, paired with CONTRIBUTING guidance naming the exact local commands and core-only scope. | CI reliability; Deterministic environment and deployment; Progressive context disclosure | medium | Local gate claims cannot be reproduced or enforced. | A fresh supported environment reproduces the checks; retained PR runs identify completed/skipped checks; a deliberate failure demonstrates inspected required-check enforcement, and repeat observations disclose retries/flakiness. |
| 3 | Introduce strict core input/output types and an explicit client protocol, paired with an `AGENTS.md` linking reviewed requirements and explaining provider evidence limits. | Typing strength; Feedforward surfaces | small | Implicit shapes and client assumptions escape feedback. | Strict checking passes approved examples and rejects representative invalid boundary calls; guidance distinguishes shape checks from unqualified provider semantics. |
| 4 | Review a provider-specific contract and build isolated adapter tests plus representative qualification, paired with a versioned plan recording dependency assumptions, expected faults, fidelity gaps, and human decisions. | Machine-readable intent; Testable boundaries; Compound engineering readiness | medium | Core arithmetic evidence is reused to justify side-effecting charges. | Approved provider claims map to amount/interaction/outcome assertions; deliberate wrong calls and relevant faults are detected; completed local and representative-environment evidence stay distinct. |
| 5 | Decide the intended aggregation boundary and enforce it with a focused structural/behavioral check, paired with a short ADR and agent review checklist. | Structure and modularity; Architecture decisions; Feedforward surfaces | small | Duplicated aggregation can diverge while core tests remain green. | The reviewed decision explains whether `charge` delegates to `total` or has separate semantics; intended examples pass and a deliberate prohibited divergence fails the relevant check. |
| 6 | Qualify silent-wrong-result detection and recovery appropriate to a library/provider integration, paired with a reviewed response runbook and an exercise plan. | Failure mode legibility; Deterministic environment and deployment | large | Wrong charges or totals persist without a documented response. | A controlled wrong-result exercise records detection, response, containment/version recovery limits, and representative dependency behavior; no production recovery claim rests on a local double alone. |
| 7 | Add a concise PR outcome template and perform one comparable core maintenance exercise, paired with a review-learning note that updates guidance or a regression case when needed. | Compound engineering readiness; Context engineering friendliness | small | Documentation or metric changes are assumed to improve maintainability. | The retained task records intent, baseline, expected/unexpected edits, effort and correction rounds, relevant checks, regressions, boundary behavior, and seven-day rework when available. |

All roadmap checks and exercises are proposed acceptance criteria. None was run as part of this assessment.
