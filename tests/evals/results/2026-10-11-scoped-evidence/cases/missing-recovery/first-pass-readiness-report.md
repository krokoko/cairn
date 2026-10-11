# AI Readiness Report

## Evidence Scope

**Source revision**: `snapshot.json:2` declares fixture identity `missing-recovery-r2`. `evidence/controls.json:2-3` reports the same source identity and requirement review `r2`. No actual commit, history, worktree status, or relevant uncommitted-change inventory is supplied. Matching fixture labels allow comparison within this snapshot but do not independently establish source freshness or a run.

**Assessment date**: 2026-10-11.

**Inspected scope**: All supplied files: `README.md`, `requirements.md`, `service.py`, `tests/test_service.py`, `evidence/controls.json`, `snapshot.json`, and `TASK.txt`. The assessed surface is event-ID recording and its stated delivery/detection/release dependencies. `service.py` is one 5-line function; the test is 5 lines. The function is cohesive and easy to locate; no size-driven split is justified. Provider code, persistence implementation, deployment configuration, raw run outputs, CI/hosting settings, and actual runtime are unavailable and were not inspected.

**Evidence basis**: Read-only source, a reviewed requirement heading, the retained controls summary, and the README's explicit manual-recovery description. No target checks were executed and no remote state was retrieved. The controls artifact reports 24 completed checks, zero failures, oracle review, completed supported-provider scenarios, and an exercised duplicate alert. The underlying scenario inventory, known-bad reproducer, exact tool/environment configuration, and operational response/recovery results are absent. `README.md:2` mentions a previous 94/100 score, but that report, its scope, evidence, source/dirty state, and date are unavailable; no previous finding or score is reused.

## Evidence Ledger

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| At-least-once delivery must not duplicate recorded event IDs | `requirements.md:1-2`, REQ-EVENT reviewed `r2`; `service.py:1-5` | supplied local source / caller-provided set | configuration_only | unknown | unknown | Reviewed claim is supplied; lifetime, persistence, concurrent delivery, identity rules, and provider assumptions are not stated. A linked requirement revision is not complete execution or meaning evidence. |
| Sequential duplicate calls with the same set return success then rejection | `tests/test_service.py:1-5`; snapshot `missing-recovery-r2` | local Python test source | configuration_only | unknown | unknown | Actual assertions are inspectable and independent of the implementation helper. The retained summary has no test IDs, so individual execution cannot be assigned to this source test. No count/state assertion, restart, or concurrency behavior is shown. |
| Reported checks found no failures | `evidence/controls.json:2-4,8-9`, source `missing-recovery-r2`, requirement review `r2` | aggregate environment incompletely specified | run_inspected | completed | no_counterexample_found | Limited to 24 reported completed checks. Raw outcomes, exact inventory, excluded/skipped checks, tools, bounds, and mapping to individual assertions are absent. This is sampled execution evidence, not a proof of all delivery behavior. |
| Oracle review considered independent event-identity examples and a known-bad duplicate control | `evidence/controls.json:4`, requirement review `r2` | control environment unspecified | run_inspected | completed | unknown | This description accompanies the completed-check summary. It records a review claim but not the control implementation, expected/actual failure, case domain, or full critical-path review, so complete oracle adequacy is unverified. |
| Supported-provider scenarios completed in staging | `evidence/controls.json:5,8-9`, source `missing-recovery-r2` | staging, provider/runtime/version unspecified | run_inspected | completed | no_counterexample_found | The summary reports completed scenarios and aggregate zero failures. Scope is only the reported supported scenarios; actual scenario inventory, production correspondence, fault coverage, and per-scenario results are unavailable. Local set behavior is not independently established as equivalent to deployed delivery. |
| Duplicate-event alert was exercised | `evidence/controls.json:6` | outcome telemetry environment unspecified | run_inspected | completed | unknown | The exercise is reported, but stimulus, alert outcome/latency, known-bad binding, routing, and operational response record are unavailable. Exercise alone does not establish detection of all silent failures. |
| Recovery requires an engineer to redeploy a selected version; there is no automatic trigger | `README.md:2`; `evidence/controls.json:7` (`manual only`) | deployment / manual operator procedure | configuration_only | unknown | unknown | Manual recovery capability is described, not exercised. Automatic rollback trigger is explicitly absent; no progressive delivery, containment, or recovery-limit evidence is supplied. |
| The prior 94/100 assessment remains applicable | `README.md:2`; prior report not supplied | N/A: prior assessment metadata unavailable | not_inspectable | unknown | unknown | Prior categories, revision/dirty state, scope, date, requirements/oracles, and runs cannot be compared. The score is not reused or treated as current evidence. |
| CI reliability, protection, and collaboration history | no CI/protection/history artifacts supplied | remote systems unavailable | not_inspectable | unknown | unknown | Local/staging summary cannot establish required checks, no skips, historical reliability, actual merge enforcement, or agent task outcomes. |

## Overall Score

**Score:** Provisional **39/100**, independently scored from this snapshot. The README's stated previous score of 94 is not a substitute for inspectable current evidence.

**Assessed weight:** **90%**. CI reliability (10%) is excluded as `unknown`: no configuration, expected CI inventory, hosted run/protection evidence, or reliability history is supplied. Weighted points are 35.10; `35.10 / 0.90 = 39.00`. The score reflects useful but terse artifacts with substantial verification and workflow gaps; normalized partial evidence does not satisfy prerequisites.

## Recommended Autonomy Level

**Level:** **L2 — Reviewed**, for limited changes to the supplied event-recording function. Humans review requirement meaning, state-lifetime/concurrency assumptions, and the relevant validation record. Deployment, recovery, and broader delivery guarantees remain human decisions.

**Decision boundary:** This report recommends scope only. It grants no merge, deploy, rollback, or tool-use permission.

**Autonomy cap applied:** Yes. **L5-RECOVERY is missing**: the README expressly requires manual version selection/redeployment and says there is no automatic rollback trigger. That independently caps the surface at L4 even if every other gate were met or a 94-point score were accepted. On the currently supplied evidence, incomplete critical-path oracle and environment qualification caps it at L3, and absent reliable/typed/enforced iteration evidence lowers the practical ceiling to L2. The five gates are not averaged with the score.

## Surface Autonomy

| Surface | Provisional level | Evidence ceiling | Recommended level | Operating scope | Blockers |
|---------|-------------------|------------------|-------------------|-----------------|----------|
| Event-ID recording (`service.py`) and delivery/detection/release dependencies | L2 | L2 | L2 | Human-reviewed changes to local recording behavior, with explicit assumptions and relevant retained checks. Humans decide broader delivery semantics and carry out the documented manual release/recovery procedure. | Summary-only check/staging evidence, unspecified state lifetime and concurrency, no exact runtime or qualified merge checks, and no strict types. Manual recovery with no automatic trigger fails L5-RECOVERY regardless of score. |

## Autonomy Prerequisites

| Surface | Prerequisite | Status | Evidence / gap |
|---------|--------------|--------|----------------|
| Event-ID recording and delivery/detection/release dependencies | L5-INTENT | unknown | `requirements.md` is reviewed `r2`; controls summary cites it and the sequential test is relevant. All critical behavior, state lifetime/concurrency assumptions, exact executed mapping, deviations, and current assertion-meaning review are not supplied. |
| Event-ID recording and delivery/detection/release dependencies | L5-ORACLES | unknown | `controls.json:4` reports independent examples and a known-bad duplicate control; 24 checks completed with zero failures. Actual control, fault coverage, independent case domain, and complete delivery-path adequacy cannot be inspected. |
| Event-ID recording and delivery/detection/release dependencies | L5-ENVIRONMENT | unknown | `controls.json:5` reports completed supported-provider staging scenarios. Provider/runtime versions, scenario/fault inventory, persistence/concurrency representation, and production fidelity limits are unspecified. |
| Event-ID recording and delivery/detection/release dependencies | L5-DETECTION | unknown | `controls.json:6` reports an exercised `duplicate_event_id` alert, but no stimulus/result, response routing, sensitivity limits, or operational response record is supplied. |
| Event-ID recording and delivery/detection/release dependencies | L5-RECOVERY | missing | `README.md:2` explicitly says an engineer selects and redeploys the last version, with no automatic rollback trigger; `controls.json:7` says `manual only`. No exercised automated containment/recovery or reviewed equivalent exists in supplied artifacts. |

## Category Breakdown

| Category | Score | Notes |
|----------|-------|-------|
| Structure and modularity | 65 | Single cohesive recorder and a separate test; caller-provided state forms a visible seam. Persistence/provider boundaries and enforcement are unavailable. |
| Documentation | 25 | README discloses the manual recovery limit; requirement states the core goal. Setup, test commands, runtime, API/ownership, and operational details are missing. |
| Testable boundaries | 60 | Sequential duplicate behavior is directly asserted; retained summary reports independent examples, a known-bad control review, and completed checks. Exact controls and broader delivery boundaries are not inspectable. |
| CI reliability | unknown | No CI configuration, expected checks, protection settings, skips, or flakiness history is supplied. Twenty-four completed checks do not establish CI reliability. |
| Typing strength | 0 | `record(seen, event_id)` is unannotated; no type configuration/checker is supplied. |
| Deterministic environment and deployment | 25 | Caller-owned set enables simple local checks, and staging scenarios are reported complete. No pinned runtime, reproducible setup, provider details, deployment config, or recovery execution is supplied. |
| Architecture decisions | 10 | No ADR, owner, or enforcement link exists; manual redeployment is a stated operational fact, not a qualified architecture decision. |
| Machine-readable intent | 60 | REQ-EVENT reviewed `r2`, meaningful ordinary assertions, matching review revision, and a completed-check summary give partial traceability. Missing mappings, control detail, concurrency/lifetime assumptions, and semantic review prevent a systematic score. Reviewed intent exists, so the no-reviewed-records cap is not the determining rule; critical-path adequacy remains unknown. PR links are not inspectable. |
| Progressive context disclosure | 20 | README and requirement are present but no agent entry guide, linked plan, decision corpus, or layered module docs exist. |
| Hidden state and magic | 55 | The `seen` dependency is explicit and no ambient I/O/time/randomness occurs in the function. Its lifetime, ownership, persistence, and concurrent use are undocumented; deployed state remains unknown. |
| Repository-scale reasoning | 65 | `record`, `seen`, `event_id`, and `test_duplicate` are easy to retrieve in this small scope. No actual maintenance/change-spread evidence supports generalization. |
| Failure mode legibility | 30 | Boolean duplicate outcome is explicit; telemetry exercise is reported. Other errors, alert routing, remedial instructions, and recovery outcomes are unspecified. |
| Feedforward surfaces | 15 | Requirement and test supply limited guidance. No agent rules, strict types, qualified boundaries, hooks, templates, or blocking-check evidence exist. |
| Compound engineering readiness | 25 | Requirement and controls record are durable; no substantive correction history, reviewed lessons, packaged workflow, or maintained plan is supplied. Prior score alone is not a compounding outcome. |
| Context engineering friendliness | 50 | Tiny cohesive code and a clearly named test are navigable. Lack of linked operational/behavioral context means an agent cannot resolve important assumptions from source alone. |

## Workflow artifacts

| Artifact type | Present | Location / notes |
|---------------|---------|------------------|
| Requirements / specs | yes | One `requirements.md` record, REQ-EVENT reviewed `r2`; no date, detailed assumptions, or complete check mapping. |
| Design / blueprints | no | No design/ADR artifact supplied. |
| Execution plans | no | No plan/progress record supplied. |
| Review / learnings | no | Review descriptions in the requirement heading and controls summary are present; no substantive review decision or learning artifact is supplied. |

**Summary:** A requirement and a controls summary preserve a small amount of feature context. Scope, assumptions, actual review decisions, and operational changes cannot be resumed reliably from them. File recency and maintenance history are unavailable; revision labels alone do not establish maintained guidance.

## Collaboration effectiveness

| Metric | Status | Notes |
|--------|--------|-------|
| First-pass acceptance | not measured | No agent task/PR outcome sample is supplied. |
| Iteration cycles per task | not measured | No correction or review-cycle records supplied. |
| Post-merge rework (7-day) | not measured | Git/merge/revert history is unavailable. |

**Infrastructure:** No PR template, label configuration, agent review rubric, packaged workflow, plan, or learning directory is supplied. The requirement and controls summary can support a future evidence review; the historical score provides no collaboration metric.

**Maintenance outcome:** Not measured. A representative future task could clarify event-ID normalization or state lifetime through the existing recorder seam, after intent approval. Retain baseline and requirement revision, expected source/test/spec edits, effort and correction cycles, unexpected modules changed, completed checks, regressions, and boundary violations. A release/recovery drill is a separate operational exercise with its own scope and results.

**Recommendations:**

1. Add task/surface and review metadata to event-service changes; record correction rounds at L2 (roadmap 3).
2. Retain assumption and oracle-review decisions alongside exact check outputs instead of preserving only a score or aggregate count (roadmap 2).
3. Review comparable maintenance outcomes and seven-day rework; convert repeated corrections into specific rules or sensitive tests (roadmap 7).

**Alignment note:** Aligned at a basic level: the snapshot does not demonstrate strong collaboration infrastructure or an empirically established higher technical maturity. The uninspectable previous score does not justify an alignment claim.

## Blockers

- **End-to-end autonomy is blocked by observed missing automated recovery.** Manual engineer-selected redeployment does not meet L5-RECOVERY, regardless of tests, staging, detection, or prior score.
- Local sequential calls with one in-memory set cannot establish the full delivery guarantee without approved assumptions about concurrent calls, persistence, restarts, and event identity. Supplied staging/control summaries lack the details needed to resolve this.
- Exact executed checks, known-bad reproducer, independent examples, current assertion review, environment configuration, and production-fidelity limitations are not inspectable.
- Alert exercise lacks an observable stimulus→alert→response record; it cannot be assumed to trigger safe recovery.
- Moving L2→L3 requires strict types, reliable completed critical checks, qualified boundaries, and inspected required-check enforcement.
- No measured maintenance or collaboration outcomes support claims of predictable iteration.

## L2 → L3 hinge

**Codebase critical path:** Establish reliable completed checks for approved critical behavior, strict type enforcement, explicit state/provider boundaries, representative integration evidence, and required merge checks. Full autonomous operation additionally requires all five gates, including exercised automated recovery.

**Repo enablers:** Pair those controls with a linked scope/assumption guide, a test-with-code review policy, a qualification plan, and retained response/recovery decisions. A plan describes work to perform; it is not a successful drill.

## Session infrastructure (dual track)

Retain exact check/control evidence and maintain contributor guidance alongside feature-scoped intent, qualification plans, and review lessons. Link both tracks from the agent entry document so later sessions can distinguish local behavior from delivery and operational claims.

## Roadmap

| Priority | Action | Category | Effort | Failure addressed | Acceptance criterion |
|----------|--------|----------|--------|-------------------|----------------------|
| 1 | Design and implement progressive delivery with a suitable automated rollback or containment trigger; pair with an approved recovery runbook and drill plan. | Deterministic environment and deployment; Failure mode legibility; Architecture decisions | medium | Manual recovery cannot satisfy L5-RECOVERY and depends on operator selection/response. | A controlled bad rollout produces the relevant detection, triggers automated containment/recovery, and records source/version, environment, trigger, recovered behavior, timing, and recovery limits. Event-state compatibility and irreversible effects have explicit handling. No gate is marked met from design alone. |
| 2 | Specify state lifetime, identity, persistence, concurrency, and delivery assumptions; pair relevant critical checks with a current requirement/assertion-review record. | Machine-readable intent; Testable boundaries; Compound engineering readiness | medium | Local duplicate rejection is overgeneralized to all at-least-once delivery. | Reviewed claims map to exact executable checks and explicit exclusions; independent expected examples and retained known-bad reproducers support the selected scope, with current completed evidence. |
| 3 | Configure/qualify required CI checks and retain detailed results; pair with a test-with-code policy and task/review template. | CI reliability; Feedforward surfaces; Compound engineering readiness | medium | Aggregate counts hide missing/skipped checks and unchecked merges. | Exact source/dirty state, requirement/oracle revision, expected inventory, tools, outcomes/skips, and a justified reliability budget are retained; inspected protection plus controlled failure demonstrate merge enforcement. Review records include correction cycles. |
| 4 | Type the event ID/state/result boundary and pin the supported environment; pair with an `AGENTS.md` entry linking contracts, canonical commands, and change limits. | Typing strength; Deterministic environment and deployment; Progressive context disclosure | small | Implicit state and input assumptions cause avoidable implementation errors. | Supported cases pass strict checking and invalid callers fail; the exact runtime is reproducible and completed checks are retained. A contributor can find scope, assumptions, and validation without guessing. |
| 5 | Expand representative staging/fault qualification and identify allowed dependency directions; pair with a short qualification plan and decision record. | Testable boundaries; Structure and modularity; Architecture decisions | medium | Unspecified staging scenarios or local doubles hide provider/state failures. | Named provider/runtime versions, scenario/fault inventory, model-vs-deployed limits, completed outcomes, and allowed/forbidden boundary controls are inspectable; production correspondence and exclusions are reviewed. |
| 6 | Retain the full duplicate-alert sensitivity exercise and operational response; pair with a response runbook linked from contributor guidance. | Failure mode legibility; Feedforward surfaces; Documentation | small | An exercised alert is mistaken for proven silent-failure detection and response. | A known-bad duplicate outcome yields a recorded alert within the justified bounds, reaches the intended responder/automation, and invokes the approved action; false-positive, missed-case, and response limits are explicit. |
| 7 | Complete one scoped maintenance exercise and review comparable follow-up outcomes; pair regression controls with a concise learning record. | Compound engineering readiness; Repository-scale reasoning; Context engineering friendliness | medium | A high prior score or small files conceal unexpected edit spread and rework. | Record scope, effort, correction rounds, planned/actual files, relevant completed checks, regressions, dependency violations, and seven-day rework; recurring corrections become specific maintained guidance or sensitive tests. |
