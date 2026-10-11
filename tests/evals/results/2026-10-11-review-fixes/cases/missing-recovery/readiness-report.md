# AI Readiness Report

## Evidence Scope

**Source revision**: `snapshot.json` declares `missing-recovery-r2`. This is fixture identity, not a verified Git commit or execution result. No Git metadata or dirty-file manifest is supplied, so commit identity and relevant uncommitted changes are not inspectable.

**Assessment date**: 2026-10-11.

**Inspected scope**: All six supplied files: [README.md](README.md), [snapshot.json](snapshot.json), [requirements.md](requirements.md), [service.py](service.py), [tests/test_service.py](tests/test_service.py), and [evidence/controls.json](evidence/controls.json). The assessed surface includes the event-recording function and the delivery, detection, and recovery dependencies described in those files. Provider adapters, deployed infrastructure, CI configuration, Git history, and external settings are not supplied. They remain evidence gaps, not assumed safe exclusions.

**Evidence basis**: Read-only inspection of the supplied artifacts and retained control summary. No target checks were executed and no remote state was retrieved. `evidence/controls.json` separately identifies `missing-recovery-r2`, reports 24 completed checks with zero failures, records requirement review `r2`, describes oracle review and completed staging scenarios, and says duplicate-event telemetry was exercised. This is inspectable summary evidence, but it lacks check identities, detailed outcomes, tool versions, environment configuration, scenario bounds, and timestamps. The README's previous 94/100 score has no accompanying report or rubric and is not reused.

## Evidence Ledger

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| Snapshot identity | `snapshot.json`: `missing-recovery-r2` | N/A: artifact identity | not_applicable | not_applicable | not_applicable | Declared fixture identity only; establishes neither a Git commit nor a run. |
| Reviewed event identity requirement and relevant executable criterion | `requirements.md`: `REQ-EVENT`, reviewed `r2`; `tests/test_service.py::test_duplicate`; `service.py::record` | Local, in-memory set | configuration_only | unknown | unknown | The test independently expects first acceptance and subsequent rejection of `"a"`. The requirement-to-test relationship is inspectable, but there is no explicit requirement tag or test-specific run result. Concurrency, persistence, restart, and provider delivery semantics are unspecified. |
| Retained check campaign | `evidence/controls.json`: source `missing-recovery-r2`, `completed_checks: 24`, `failures: 0` | Unspecified campaign environment | run_inspected | completed | no_counterexample_found | Limited to the aggregate checks reported. No expected inventory, individual outcomes, skipped-check accounting, tool configuration, or mapping establishes that all critical behavior was exercised. This assessment did not run them. |
| Independent expectations and sensitivity control reviewed | `evidence/controls.json`: `oracle_review` | Unspecified | configuration_only | unknown | unknown | Records review of independent event identity examples and a known-bad duplicate control. Control implementation, expected failure, execution result, and reviewed scope are not supplied. Review wording alone does not establish sensitivity across critical paths. |
| Supported provider scenarios completed | `evidence/controls.json`: `staging` | Staging, configuration unspecified | run_inspected | completed | unknown | Completion is recorded; individual scenario outcomes and provider/fault coverage are unavailable. The campaign's aggregate zero-failure count is not explicitly mapped to these scenarios. Production representativeness remains unknown. |
| Duplicate-event alert exercised | `evidence/controls.json`: `outcome_telemetry` | Unspecified operational environment | run_inspected | unknown | unknown | An exercise is recorded. Its outcome, detection latency, injected fault, and operational response are not supplied. |
| Recovery is manual with no automatic trigger | `README.md`; `evidence/controls.json`: `rollback: manual only` | Deployment, details unspecified | configuration_only | unknown | unknown | Observed explicit absence of automatic rollback. Neither an exercised recovery run nor recovery limits are supplied. Supports `L5-RECOVERY: missing`, not a claim that recovery was tested. |
| Required CI checks and branch protection | No configuration or protection export supplied | CI / server settings unavailable | not_inspectable | unknown | unknown | A completed check count does not establish required-check inventory, merge enforcement, reliability, or flakiness. |
| Previous readiness score | `README.md`: previous 94/100 | N/A: prior assessment unavailable | not_inspectable | unknown | unknown | Scope, revision, rubric, and underlying assessment cannot be inspected; not reused in the current calculation. |

## Overall Score

**Score:** provisional 39/100.

**Rubric:** readiness-scoring/2.

**Assessed weight:** 0.83 of 1.00 (83%). CI reliability (0.10) and deterministic environment and deployment (0.07) are unknown and excluded. Their configurations and sufficiently detailed execution evidence are unavailable. They are not assigned zero or treated as satisfied.

The weighted total for the scored categories is 32.05; `32.05 / 0.83 = 38.61`, rounded to 39. This diagnostic describes the supplied snapshot. It does not establish a decline from the unsupported prior 94/100 figure, production correctness, or an operating permission.

## Recommended Autonomy Level

**Level**: L2

**Summary scope:** Limited, explicitly scoped changes to the in-memory event-recording behavior, with human review before merge. Delivery semantics, persistence, concurrency, telemetry changes, and deployment/recovery changes require human decisions and additional evidence. These critical dependencies are included in the ceiling assessment.

**Decision boundary:** Recommendations do not authorize merge, deployment, tool access, or changes to operational permissions.

**Autonomy cap applied:** Yes. The provisional score maps to L2. Reliable bounded iteration is not established because enforced checks, typing, and dependency evidence are unavailable or absent. The broad delivery scope also lacks sufficient L4 intent and oracle evidence, independently limiting it to at most L3. Manual-only recovery definitively fails the L5 recovery gate and caps any otherwise qualifying scope at L4. Other unknown gates remain unknown rather than being averaged away.

## Surface Autonomy

| Surface | Provisional level | Evidence ceiling | Recommended level | Operating scope | Blockers |
|---------|-------------------|------------------|-------------------|-----------------|----------|
| Event recording and delivery/recovery dependencies | L2 | L2 | L2 | Small changes to `record` under reviewed, sequential in-memory assumptions; human reviews intent, implementation, and relevant evidence before merge and owns operational changes. | Bounded iteration is not yet supported by typed boundaries or inspected CI enforcement. Aggregate check evidence does not establish provider, persistence, concurrency, or fault coverage. Automatic recovery is explicitly missing; L5 is unsupported even if the other gates later become met. |

## Autonomy Prerequisites

| Surface | Prerequisite | Status | Evidence / gap |
|---------|--------------|--------|----------------|
| Event recording and delivery/recovery dependencies | L4-INTENT | unknown | `requirements.md` contains reviewed `REQ-EVENT r2`, and `test_duplicate` provides a relevant sequential criterion. Approved boundaries for delivery dependencies, event identity lifetime, persistence, concurrency, and restart are not supplied, so reviewed executable intent for the full assessed scope is incomplete. |
| Event recording and delivery/recovery dependencies | L4-ORACLES | unknown | The independent assertions are inspectable, and `controls.json` records oracle review and 24 completed checks. Check-specific execution, sensitivity-control results, assumptions, and coverage of critical dependencies are unavailable. |
| Event recording and delivery/recovery dependencies | L5-INTENT | unknown | One reviewed claim is present, but no reviewed inventory or executed-check mapping establishes coverage of all critical behavior. |
| Event recording and delivery/recovery dependencies | L5-ORACLES | unknown | The positive aggregate result and oracle-review description do not demonstrate adequate, current oracles on every critical path. |
| Event recording and delivery/recovery dependencies | L5-ENVIRONMENT | unknown | `controls.json` records completed supported-provider staging scenarios. The represented providers, production correspondence, fault cases, and exclusions are unavailable. |
| Event recording and delivery/recovery dependencies | L5-DETECTION | unknown | `duplicate_event_id` alert exercise is recorded, but known-bad outcome, response, and detection bounds are not inspectable. |
| Event recording and delivery/recovery dependencies | L5-RECOVERY | missing | `README.md` explicitly requires an engineer to choose and redeploy the last version and states there is no automatic rollback trigger; `controls.json` agrees with `manual only`. This is not automated rollback/containment driven by relevant detection. No reviewed equivalent or exercised automated recovery is supplied. |

No gate is marked met solely because a control is named or a check count is large. Conversely, the retained check and staging summaries are acknowledged as supplied evidence rather than treated as if no execution information exists.

## Category Breakdown

| Category | Score | Notes |
|----------|-------|-------|
| Structure and modularity | 60 | `service.py` isolates one cohesive operation from its test. `seen` is an explicit dependency; no I/O is embedded. Adapters and enforced boundary rules are not supplied. |
| Documentation | 20 | README identifies the service and clearly discloses manual recovery, but omits setup, test commands, supported assumptions, and API guidance. |
| Testable boundaries | 55 | `test_duplicate` has independent Boolean expectations and exercises repeated identity; `controls.json` reports a completed campaign. Only one concrete case is inspectable; unknown critical boundary coverage limits the score. |
| CI reliability | unknown | No CI configuration, required-check inventory, protection export, retry history, or check-specific results supplied. The aggregate report cannot establish reliability or enforcement. |
| Typing strength | 0 | Both `record` parameters and its return value lack annotations; no type-checking configuration is present in the snapshot. |
| Deterministic environment and deployment | unknown | Core has no clock, randomness, or external calls, and staging completion is recorded. Runtime versions, reproducible setup, deployment configuration, and production fidelity are unavailable. Manual recovery is an observed operational gap. |
| Architecture decisions | 0 | No ADR, ownership record, design decision, or decision-to-enforcement link supplied. |
| Machine-readable intent | 60 | `REQ-EVENT r2` is reviewed and its relationship to the executable duplicate criterion is inspectable; the core is separable from I/O. Explicit check mappings, broader semantics, and execution-to-claim detail are missing. Reviewed intent exists, so the absent-reviewed-requirements cap is not the reason for this score; incomplete scoped oracle evidence still limits autonomy. PR/issue traceability is not inspectable without history. |
| Progressive context disclosure | 15 | README and requirements exist, but there is no agent guide, cross-linking, plan, or layered decision corpus. |
| Hidden state and magic | 70 | `seen` exposes the local state dependency and the implementation has no ambient environment access. State ownership, lifetime, and provider/deployment configuration remain unspecified. Credit applies to inspected code only. |
| Repository-scale reasoning | 60 | Source and test naming are consistent, and the small source surface is directly retrievable. No canonical documented workflow or larger module pattern is available. |
| Failure mode legibility | 45 | Duplicate rejection is an explicit Boolean, and an alert exercise is recorded. Failure distinctions, invalid-input handling, diagnostic detail, and operational responses are not documented. |
| Feedforward surfaces | 10 | The requirement offers limited intent guidance; no agent instructions, linter, type checks, templates, hooks, or bypass protection is supplied. |
| Compound engineering readiness | 30 | A reviewed requirement, executable example, and retained control summary provide durable context. No correction history, plans, learning notes, packaged workflows, or evidence of maintained guidance is supplied. |
| Context engineering friendliness | 50 | `service.py` and its test are five lines each and concern the same simple behavior. Their cohesion is inspectable; size alone earns no credit. Root documentation has headings, but lacks navigation and operational context. |

The two Python files are each five lines (10 total); neither contains unrelated concerns that justify splitting. No generated or vendored source is supplied. Maintenance effort and change spread were not measured.

## Workflow artifacts

| Artifact type | Present | Location / notes |
|---------------|---------|------------------|
| Requirements / specs | yes | One file, `requirements.md`, with reviewed `REQ-EVENT r2`; no review date or history supplied. |
| Design / blueprints | no | No design files or ADRs in the supplied snapshot. |
| Execution plans | no | No plan or progress log supplied. |
| Review / learnings | yes | One partial review/evidence artifact, `evidence/controls.json`, records requirement and oracle-review descriptions. It does not contain review decisions, corrective lessons, or detailed run reports. |

**Summary:** Root requirements and the one-file `evidence/` directory preserve some feature context, but there are no active plans, architecture decisions, or maintained lessons. Revision labels are visible; calendar recency and maintenance history are not. Filesystem timestamps are not used as proof of freshness.

## Collaboration effectiveness

| Metric | Status | Notes |
|--------|--------|-------|
| First-pass acceptance | not measured | No PR sample, review history, or team measurement supplied. |
| Iteration cycles per task | not measured | No comparable task records supplied. |
| Post-merge rework (7-day) | not measured | Git and merge history are unavailable. |

**Infrastructure:** No PR template, agent-work labels, agent review rubric, or learning log is supplied. The requirement and control summary can anchor future review, but do not measure collaboration outcomes.

**Maintenance outcome:** Not measured. Propose a reviewed task that adds a distinct-ID case and clarifies set ownership/lifetime. Retain the baseline revision, intended files (`requirements.md`, `service.py`, and its test), actual edit spread, correction cycles, completed relevant checks, regressions, and any dependency-boundary violations. Do not claim improvement from shorter files or more tests alone.

**Recommendations:**

1. Add task/surface metadata and an informal correction-cycle count to reviewed changes; sample comparable tasks, rather than mixing operational and local logic work.
2. Record first-pass acceptance and seven-day fixes/reverts when review history becomes available, preserving the sample and limits.
3. Store repeated review corrections in a small plan/review record and update relevant requirements or agent guidance; connect these records to the check evidence.

These recommendations are paired with roadmap actions 2, 4, and 7.

**Alignment note:** Aligned at the observable level: neither strong collaboration infrastructure nor high operating readiness is established. Organization-wide maturity is unknown.

## Blockers

- **Advancement from L2:** No strict typing or inspectable reliable, merge-blocking CI. The snapshot lacks documented execution commands and a supported operating boundary for agent changes.
- **Critical dependency scope:** `requirements.md` does not define persistence, restart, concurrency, or supported provider assumptions. The staging summary does not expose the scenarios needed to resolve those limits.
- **L4 evidence:** The supplied aggregate campaign cannot be traced to a complete inventory of relevant assertions, reviewed assumptions, individual outcomes, and sensitivity-control results.
- **L5 recovery:** Automatic rollback is explicitly absent. Manual engineer redeployment cannot satisfy `L5-RECOVERY`, even if every other L5 gate is later established.
- **Other L5 evidence:** Production representativeness, silent-failure response, complete executable intent, and oracle coverage need inspectable supporting records. Their current status is unknown, not declared absent.

## L2 → L3 hinge

**Codebase critical path:** Establish reliable relevant tests, strict types, scoped boundaries, critical integration checks, and required checks that block failed changes.

**Repo enablers:** Pair those controls with an agent entry point, test-with-code review guidance, a feature plan, and task metadata. The paired actions below describe evidence to obtain; none has been executed by this assessment.

## Session infrastructure (dual track)

Durable checks and workflow artifacts should advance together: type/CI changes with `AGENTS.md` and contribution guidance; dependency checks with a reviewed scope plan; recovery automation with a decision record and runbook. Package a workflow only after an exercise demonstrates that its steps are useful.

## Roadmap

| Priority | Action | Category | Effort | Failure addressed | Acceptance criterion |
|----------|--------|----------|--------|-------------------|----------------------|
| 1 | Define the event-recording operating contract in `requirements.md` and map relevant tests to `REQ-EVENT`; retain a feature decision record for state ownership, restart, concurrency, and provider assumptions. | Machine-readable intent; Testable boundaries; Architecture decisions | Medium | Sequential set behavior is mistaken for complete delivery correctness. | Reviewed claims and explicit exclusions map to independent criteria; critical dependencies remain included; each mapped result identifies source, requirement, oracle, and environment revisions. |
| 2 | Add a reproducible test/lint CI command and retain its required-check configuration; pair with contribution guidance and PR evidence/task metadata. | CI reliability; Documentation; Compound engineering readiness | Medium | Missing or bypassed checks appear equivalent to passing checks. | Inspectable expected inventory and individual outcomes include skipped/missing states; a controlled failure blocks merge, and comparable reviewed changes retain correction-cycle data. |
| 3 | Type the event identity/set boundary and enforce strict checking; pair with `AGENTS.md` linking the supported contract and check commands. | Typing strength; Feedforward surfaces; Progressive context disclosure | Small | Agents infer incompatible state or identifier types. | Valid callers pass, representative invalid callers fail the enforced checker, and guidance states the reviewed boundary and relevant commands. |
| 4 | Retain the provider/staging campaign detail and known-bad duplicate-control results; pair with a resumable validation plan. | Testable boundaries; Deterministic environment and deployment; Compound engineering readiness | Medium | Aggregate green results conceal gaps in dependency fidelity or oracle sensitivity. | Records identify expected cases, actual outcomes, provider versions/configuration, faults, excluded behavior, and sensitive-control failures; reviewers assess correspondence to production. |
| 5 | Implement progressive delivery and automatic rollback or containment driven by the relevant duplicate-outcome detection; pair with a recovery decision record and runbook. | Deterministic environment and deployment; Failure mode legibility; Architecture decisions | Large | A bad deployment continues until an engineer manually intervenes. | A scoped staging exercise injects a wrong-but-running duplicate failure, demonstrates detection-triggered automatic recovery, and records trigger, elapsed time, containment scope, residual data effects, rollback limits, and cases needing human intervention. Reviewed evidence is required before marking `L5-RECOVERY` met. |
| 6 | Retain telemetry sensitivity and operational-response evidence; pair with incident/learning notes tied to `REQ-EVENT`. | Failure mode legibility; Testable boundaries; Compound engineering readiness | Medium | An exercised alert is credited without showing that it detects relevant silent failures and produces a response. | Known-good and known-bad cases record expected/actual alert outcomes, latency bounds, response behavior, and omissions; detection and recovery results remain separately inspectable. |
| 7 | Perform one reviewed maintenance exercise and preserve its plan/review record; turn repeatable successful steps into concise project guidance. | Context engineering friendliness; Repository-scale reasoning; Compound engineering readiness | Small | Apparent readiness improvements do not reduce real task friction. | Record expected/actual changed files, effort, correction cycles, relevant completed checks, regressions, and boundary violations; use later comparable tasks to assess whether the guidance helps. |
