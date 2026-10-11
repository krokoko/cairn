# AI Readiness Report

## Evidence Scope

**Source revision**: `snapshot.json:2` declares fixture identity `mixed-surfaces-r2`. `evidence/core.json:1` reports that same source revision and requirement review `r2`. A Git commit, history, and relevant dirty-file inventory are not supplied, so the identity is a matching declared snapshot identifier, not independent proof of source freshness or execution.

**Assessment date**: 2026-10-11.

**Inspected scope**: All supplied files: `README.md`, `requirements.md`, `core.py`, `provider.py`, `tests/test_core.py`, `evidence/core.json`, `snapshot.json`, and `TASK.txt`. The two assessed surfaces are pure core arithmetic and the provider charging adapter, including its external client dependency. Production files are 2 lines each; the supplied test is 3 lines. Their simple layout is easy to inspect, but size is not maintenance evidence. Provider implementation, staging, deployed behavior, consumer code, and remote controls are excluded because they are unavailable.

**Evidence basis**: Read-only artifacts and the retained core summary were inspected; no target checks were executed or remote state retrieved. `evidence/core.json` is a run summary reporting 20 executed checks, zero failures, and a detected negative control for core arithmetic only. Raw test identities, expected check inventory, tool/configuration version, exact runtime, campaign bounds, and the negative-control reproducer are absent. No provider qualification or previous assessment is available. CI/protection/history evidence is not inspectable.

## Evidence Ledger

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| REQ-TOTAL defines total integer cents as the sum of item amounts | `requirements.md:1-2`, reviewed `r2`; `core.py:1-2` | pure core / supplied source | configuration_only | unknown | unknown | Stable claim and reviewed revision are stated. Requirement approval details and a complete claim-to-test inventory are not supplied. Reviewed text is not a test run. |
| The inspected example expects 200 + 300 = 500 | `tests/test_core.py:1-3`; snapshot `mixed-surfaces-r2` | local Python test source | configuration_only | unknown | unknown | Literal expectation is independent of the `sum` implementation. Run summary does not identify this specific test, so its individual execution is unverified. Integer range, invalid values, empty inputs, and input representation assumptions are unspecified. |
| Reported core arithmetic executions had no failures | `evidence/core.json:1`, source `mixed-surfaces-r2`, requirement review `r2` | “supported Python runtime” as reported; exact runtime unspecified | run_inspected | completed | no_counterexample_found | Bounded to the 20 executions reported in this retained summary. Zero failures is no proof of all integer behavior; cases, seeds/bounds, exact tools, expected check count, and whole-suite completeness are unavailable. No claim is made that the named source test is among those 20. |
| A core negative control was detected | `evidence/core.json:1`, `negative_control_detected: true`, requirement review `r2` | reported core test environment | run_inspected | completed | unknown | A reported sensitivity signal is present, but the changed implementation, expected failure, reproducer, and checked fault class are absent. It does not establish adequate oracles for every critical path. |
| Charging passes `sum(items)` to an injected client | `provider.py:1-2`; `README.md:2`; snapshot `mixed-surfaces-r2` | external client / deployment unspecified | configuration_only | unknown | unknown | No provider contract, behavior tests, or environment qualification is supplied. Amount units, response/error semantics, retries, duplicate-charge behavior, and provider fidelity are unknown. Core evidence explicitly excludes this adapter. |
| CI completion and merge enforcement | no CI/protection or runner inventory artifact supplied | remote CI / repository settings unavailable | not_inspectable | unknown | unknown | Absence of a supplied CI config is observable; actual hosted CI, protection, skips, and reliability are not inspectable. |
| PR links and observed maintenance/collaboration outcomes | no Git history or review records supplied | N/A: history inspection | not_inspectable | unknown | unknown | No first-pass acceptance, correction-cycle, or rework estimate can be justified. |

## Overall Score

**Score:** Provisional **38/100**. The score summarizes the supplied repository; per-surface evidence controls the recommendation.

**Assessed weight:** **90%**. CI reliability (10%) is `unknown` because no run history, expected CI inventory, or protection evidence is supplied. Weighted points are 34.00; `34.00 / 0.90 = 37.78`, rounded to 38. This partial normalization does not satisfy any unknown gate.

## Recommended Autonomy Level

**Level:** **L2 — Reviewed** for pure core arithmetic; **L1 — Assisted** for the provider adapter and any change that depends on provider behavior. There is no uniform repository-wide permission to use core gates for charging changes.

**Decision boundary:** Recommendations only; operating permissions and human approval of intent, merges, and deployments remain external. Human review is required for the core's limited changes; humans own provider behavior decisions and integration.

**Autonomy cap applied:** Yes. Unknown critical-path oracle adequacy caps core autonomy at L3, and incomplete execution/environment/enforcement evidence lowers its practical ceiling to L2. Missing provider intent and validation lower its ceiling to L1. The repository's machine-readable intent score is below 51 and does not support higher autonomy. No surface meets all L5 gates.

## Surface Autonomy

| Surface | Provisional level | Evidence ceiling | Recommended level | Operating scope | Blockers |
|---------|-------------------|------------------|-------------------|-----------------|----------|
| Pure integer-cent arithmetic in `core.py` | L2 | L2 | L2 | Limited core-only changes with human review of REQ-TOTAL, assumptions, and relevant evidence; no provider claims. | Matching core run summary supports only reported cases. Full test mapping, reviewed boundary semantics, exact environment, strict types, reliable CI, and merge enforcement are unavailable. |
| Charging adapter in `provider.py` and external `client.charge` | L2 | L1 | L1 | Propose contract, test plan, and code fragments for a human to decide and integrate; changes involving this dependency inherit this ceiling. | README explicitly states no adapter contract or environment qualification. No supplied provider tests, fault cases, or recovery/detection evidence. Core arithmetic evidence does not transfer to charging. |

## Autonomy Prerequisites

| Surface | Prerequisite | Status | Evidence / gap |
|---------|--------------|--------|----------------|
| Pure integer-cent arithmetic in `core.py` | L5-INTENT | unknown | `requirements.md` is reviewed `r2`, and the core record cites that revision. Complete critical-behavior mapping, exact executed checks, and current assertion-meaning review are not inspectable. |
| Pure integer-cent arithmetic in `core.py` | L5-ORACLES | unknown | Independent literal example plus 20 reported successes and a negative-control flag are useful partial signals. Case inventory, control reproducer, numeric assumptions, and complete risk coverage are absent. |
| Pure integer-cent arithmetic in `core.py` | L5-ENVIRONMENT | unknown | `evidence/core.json` says “supported Python runtime” without a version, configuration, supported-consumer scope, or qualification evidence. Pure-core determinism is visible; representative consumer behavior is not established. |
| Pure integer-cent arithmetic in `core.py` | L5-DETECTION | unknown | Negative-control detection is reported, but its fault class and operational response are unspecified. No evidence covers all silent wrong-total outcomes or consumption paths. |
| Pure integer-cent arithmetic in `core.py` | L5-RECOVERY | missing | No controlled library rollout/version rollback mechanism, exercised containment, or reviewed equivalent is supplied. |
| Charging adapter in `provider.py` and external `client.charge` | L5-INTENT | missing | `README.md:2` explicitly states that the adapter has no contract. REQ-TOTAL does not specify charging behavior. |
| Charging adapter in `provider.py` and external `client.charge` | L5-ORACLES | missing | No provider assertions, independent acceptance criteria, or sensitivity controls are supplied; core summary scope excludes the adapter. |
| Charging adapter in `provider.py` and external `client.charge` | L5-ENVIRONMENT | missing | `README.md:2` explicitly states no environment qualification. No mocked-versus-provider fidelity study or representative staging evidence is supplied. |
| Charging adapter in `provider.py` and external `client.charge` | L5-DETECTION | missing | No duplicate/wrong-amount detection, reconciliation check, telemetry control, or associated response is supplied. These behaviors first need an approved contract. |
| Charging adapter in `provider.py` and external `client.charge` | L5-RECOVERY | missing | No progressive delivery, containment, exercised rollback, or provider-safe recovery policy is supplied. |

## Category Breakdown

| Category | Score | Notes |
|----------|-------|-------|
| Structure and modularity | 65 | Pure arithmetic is separated from an injected client adapter (`core.py`, `provider.py`). The adapter repeats summation instead of using the core boundary; no mechanical boundary rule or explicit exports exist. |
| Documentation | 30 | README clearly separates allowed core gating from an unqualified provider. Setup, commands, public API/error behavior, and consumer guidance are absent. |
| Testable boundaries | 55 | A directly testable pure core, independent literal expectation, and core-scoped run summary exist. Provider boundary has no tests; the 20 cases/control cannot be individually inspected. |
| CI reliability | unknown | No CI configuration, complete check inventory, hosted runs, or protection records are supplied. Core-local results cannot establish CI reliability. |
| Typing strength | 0 | Both functions and client boundary are unannotated; no checker or type configuration is supplied. |
| Deterministic environment and deployment | 20 | Core is pure, but “supported Python runtime” is unpinned and provider qualification is explicitly absent. No reproducible setup or deployment configuration is supplied. |
| Architecture decisions | 20 | README records core/adapter isolation intent. No revisioned ADR, ownership, or decision-to-enforcement link exists. |
| Machine-readable intent | 50 | Reviewed REQ-TOTAL, a relevant ordinary test, and a matching review revision in the summary provide partial core traceability. Adapter intent is missing and no complete execution/assertion review chain is supplied. Missing reviewed records elsewhere cannot be compensated by the core test; the 60-point cap does not raise this score. PR links remain not inspectable. |
| Progressive context disclosure | 20 | Root README and requirement file are short entry artifacts, but no links to a plan, agent guide, or decision corpus are supplied. |
| Hidden state and magic | 70 | Core has no ambient I/O/time/randomness. Client injection makes the dependency visible, but provider behavior and configuration are unknown. |
| Repository-scale reasoning | 70 | `core`, `provider`, and `test_core` make the small scope discoverable. Repeated `sum(items)` is a potential drift point; no maintenance outcome is available. |
| Failure mode legibility | 20 | No swallowed exception is visible; no stable error contract, contextual messages, or provider remediation exists. |
| Feedforward surfaces | 15 | README states a useful scope restriction and a test exists. Types, agent guidance, local hooks, boundary rules, templates, and enforcement evidence are absent. |
| Compound engineering readiness | 20 | Reviewed requirement and retained core evidence are durable artifacts, but no correction history, packaged workflow, plan, or learning record is supplied. |
| Context engineering friendliness | 50 | Cohesive tiny files have obvious entry functions, but no module docs, public export definition, or measured navigation/change outcome exists. No split is warranted merely on line counts. |

## Workflow artifacts

| Artifact type | Present | Location / notes |
|---------------|---------|------------------|
| Requirements / specs | yes | One `requirements.md` record, REQ-TOTAL reviewed `r2`; no date or provider requirement. |
| Design / blueprints | no | README describes separation but no feature design/ADR artifact is supplied. |
| Execution plans | no | No plan or progress record supplied. |
| Review / learnings | no | Requirement heading and summary reference review `r2`, but no substantive assertion-review or learning record is supplied. |

**Summary:** One core requirement provides session context, with a core summary retained under `evidence/`. Broader intent, feature progress, and review decisions cannot be resumed from these artifacts. Dates and maintenance history are unavailable; the `r2` label alone is not proof of recent maintenance.

## Collaboration effectiveness

| Metric | Status | Notes |
|--------|--------|-------|
| First-pass acceptance | not measured | No comparable agent PR or review outcomes supplied. |
| Iteration cycles per task | not measured | No correction-round records supplied. |
| Post-merge rework (7-day) | not measured | Git/merge history is unavailable. |

**Infrastructure:** README provides an important core-only scope rule. No PR template, labels, review rubric, agent instructions, packaged workflow, or learning directory is supplied.

**Maintenance outcome:** Not measured. A future core-only contract refinement should record baseline/review revision, expected source/test/spec edits, effort and correction rounds, completed checks, unexpected spread, regressions, and any provider touch. A provider extension is a separate exercise after contract and fidelity work; it must not borrow the core outcome.

**Recommendations:**

1. Track correction cycles informally on core agent patches and label the changed surface; retain human review decisions (roadmap 2).
2. Use a review template that distinguishes core-local evidence from provider qualification and records missing assumptions (roadmap 3–4).
3. Sample comparable task acceptance and seven-day rework; turn recurring corrections into guidance or sensitive regression tests (roadmap 6).

**Alignment note:** Aligned at a basic level: the core's reviewed scope and sparse collaboration infrastructure do not demonstrate a maturity mismatch. No organization-wide conclusion is supported.

## Blockers

- Core L2→L3: strict type enforcement, reproducible runtime, complete and reliable critical-check evidence, required merge checks, and qualified module boundaries are unavailable. The core summary's 20 reported executions are not a complete CI inventory.
- Core intent/oracles: explicit supported numeric/input semantics, complete requirement-to-check mapping, independent boundary expectations, and a retained negative-control reproducer are missing.
- Provider L1→L2: the README explicitly discloses missing contract and environment qualification, with no supplied adapter check or run. Define the charging boundary before implementing or approving behavior.
- Detection and recovery evidence is missing or incomplete on both surfaces; a pure-function check cannot establish safe charging, rollback, or containment.
- Collaboration and representative maintenance outcomes are not measured.

## L2 → L3 hinge

**Codebase critical path:** For core only, establish reliable completed critical checks, strict types, a reproducible environment, clear enforced dependency boundaries, and inspected merge enforcement. Provider work remains independently capped until its contract and integration evidence justify advancement.

**Repo enablers:** Pair those controls with a core/provider scope guide, a test-with-code policy, a review template, and a short active plan. The paired actions below describe evidence to obtain; they are not evidence already achieved.

## Session infrastructure (dual track)

Pair runtime/type/check improvements with durable entry guidance and feature-scoped review/plan records. Keep each record explicit about the surface it can support. Package a workflow only after a useful repeatable core qualification procedure exists.

## Roadmap

| Priority | Action | Category | Effort | Failure addressed | Acceptance criterion |
|----------|--------|----------|--------|-------------------|----------------------|
| 1 | Add strict core/input types and a reproducible check environment; pair with `AGENTS.md` links to REQ-TOTAL and explicit core/provider limits. | Typing strength; Deterministic environment and deployment; Progressive context disclosure | small | Invalid inputs and ambiguous runtime assumptions undermine bounded iteration. | Approved input domain is encoded; a known invalid caller fails checking; exact runtime/configuration and completed type/test results are retained, and a newcomer can find the governing scope. |
| 2 | Configure and qualify required core checks; pair with a test-with-code contribution policy and task/review metadata. | CI reliability; Feedforward surfaces; Compound engineering readiness | medium | Local summaries are mistaken for reliable, merge-blocking CI. | Expected check inventory, source/dirty state, exact tools, outcomes/skips, and a justified flakiness budget are retained; inspectable settings plus a controlled failure demonstrate merge enforcement. Comparable patches record correction cycles. |
| 3 | Extend reviewed core boundary claims, link actual test IDs, and retain sensitivity-control details; pair with a short assertion-review record. | Testable boundaries; Machine-readable intent; Compound engineering readiness | small | Twenty passing executions hide unknown case coverage and oracle meaning. | Reviewer approves each selected claim/expectation and exclusion; runner records bind current checks to requirement revision; a retained wrong implementation is detected for the intended reason. |
| 4 | Define a provider charging contract and add provider-specific fault/integration checks; pair with a qualification plan and response runbook. | Machine-readable intent; Testable boundaries; Deterministic environment and deployment | medium | Core arithmetic is incorrectly treated as evidence of safe external charging. | Approved amount, response, error, retry, and duplicate-charge policies map to checks; representative environment results and mock fidelity limits are retained separately from core evidence. |
| 5 | Qualify the core/adapter dependency rule and any chosen shared-total seam; pair with a review checklist and a short ADR. | Structure and modularity; Architecture decisions; Feedforward surfaces | small | Adapter arithmetic can drift or core changes can acquire external dependencies. | Reviewed allowed and forbidden examples exercise the checker; intended direction passes, forbidden dependency fails with actionable output, and the ADR names the enforcement artifact. |
| 6 | Exercise detection and safe containment appropriate to each surface; pair with retained maintenance/review lessons and comparable-task tracking. | Failure mode legibility; Compound engineering readiness | medium | Silent incorrect outcomes or unsafe recovery escape local tests; easy metrics mask maintenance friction. | For each surface, a declared bad outcome triggers the intended detection/response and recovery limits are recorded; task scope, effort, actual edit spread, regressions, and seven-day rework are retained without transferring claims across surfaces. |
