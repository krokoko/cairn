# Verification Strategy

The migration needs a portfolio of amount and currency checks, an independently specified v2 contract, durable state and fault-sequence tests, mixed-version migration tests, and later provider qualification. The supplied local model and its revision 2 summary do not establish the revised payment requirements. No current run or provider compatibility result is claimed here.

## Evidence Scope

**Source revision**: `strategy-provider-migration-r3`, as declared by [`snapshot.json:2`](snapshot.json). This is a fixture identity, not a Git verification, build identity, or evidence of execution. The only change made by this assessment is this report.

**Assessment date**: 2026-10-11.

**Inspected scope**: All eight supplied snapshot files: `adapter.py`, `local_model.py`, `tests/test_adapter.py`, `README.md`, `requirements.md`, `provider-api-v2.json`, `snapshot.json`, and `evidence/model-r2.json`. The named frozen design-strategy skill and its relevant frozen references informed the report. No other repository, evaluation case, remote settings, or live source was inspected.

**Evidence basis**: Static inspection of supplied source, documentation, one test, and a historical model summary. No `verification-report.md`, dependency manifest, CI configuration, hooks, native runner reports, provider receipts, or hosting settings are supplied. No target checks were executed and no remote state was retrieved. Missing snapshot artifacts do not prove an absence of checks or controls in the real project.

Requirement revision 3 is recorded as approved by the payments owner on 2026-10-10 (`requirements.md:1–2`). The provider extract independently documents v2 and records integration-owner review on that date (`provider-api-v2.json:2–3`); its explicit limitation is that no executed fidelity or live provider receipt is supplied (`:24–26`). Those approvals concern the documents; no reviewed relationship from revision 3 to implementation assertions is supplied.

## Evidence Ledger

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| Current amount example | `tests/test_adapter.py:1–6`, declared r3 snapshot | Local fake, actual runner environment unknown | configuration_only | unknown | unknown | One test asserts returned `amount == 1250`; no result inspected. Fake exposes only v1 and always returns `p1`. |
| v2 request contract | `adapter.py:1–5`; `provider-api-v2.json:4–17`, v2-2026-10 | Source and independent documented interface | configuration_only | unknown | unknown | Source uses `create_charge(amount=cents)` and ignores tenant/key. The extract requires `create_payment(tenant, idempotency_key, amount_minor, currency)`. This is an inspected mismatch, not an executed contract result. |
| REQ-ID, REQ-RETRY, REQ-MIGRATE under revision 3 | `local_model.py:1–4`; `evidence/model-r2.json:1–14`, source r2 / requirements 2 | In-memory Python model | stale | unknown | unknown | Summary reports 50 generated sequences and zero failures, but no explicit completion, native results, cases, seeds, or assertions. Provider calls: 0. Explicitly excludes timeout after commit, restarts, overlap, tenant namespaces. Cannot refresh it by relabeling it r3. |
| Retry behavior in current adapter | `adapter.py:2–5`; `README.md:5–6` | Source plus supplied failure assumption | configuration_only | unknown | unknown | Timeout triggers another unkeyed create call. Supplied assumption permits the first call to have committed; no executed duplicate-charge trace is supplied. |
| Revision 3 semantic approval of current oracles | `requirements.md:1–9`; `tests/test_adapter.py`; `local_model.py` | Requirement/assertion relationship | not_inspectable | unknown | unknown | Document approval is supplied; assertion/fixture/helper relationship review is not. Model lacks tenant scope, conflict checks, expiry, and durable storage. |
| Actual v2 provider behavior and v1/v2 identity interoperability | `provider-api-v2.json:18–26`; `README.md:4–7` | Provider / deployed environment | not_inspectable | unknown | unknown | Documented lookup by tenant/key is useful independent input, but no response schema, consistency, retention, cross-version guarantee, SDK release, or execution evidence is supplied. |
| CI enforcement, release controls, observability, current feedback | Snapshot inventory; `README.md:7` | CI / hosting / production | not_inspectable | unknown | unknown | Actual run placement, settings, required checks, bypass permissions, and monitoring are unknown. |

The historical summary remains evidence about what that artifact reports; it is not a completed current test campaign. No positive execution conclusion is supported for the assessed revision.

## Evidence Requirements

All rows below are **proposed requirements, not completed evidence**. Owners are proposed responsibilities based on the two document-review roles, not newly assigned people or authorization. Before relying on a result, record the exact requirement, assertion, fixture, helper/model, source and dirty-diff revisions; tool/dependency versions; configuration; environment; run ID; expected check inventory; completion; reports/traces; and exclusions.

| Claim / requirement | Oracle / review owner | Required evidence / environment | Completion / acceptance criteria | Scope / limits |
|---------------------|-----------------------|---------------------------------|----------------------------------|----------------|
| REQ-AMOUNT r3: preserve integer minor units for USD and reject unsupported currencies | Independent literal examples and generated integer properties; payments owner reviews domain, integration owner reviews mapping | `tests/test_amount.py` and `tests/test_provider_contract.py`; recorded outbound requests in local contract harness | Every expected case executes; USD `1250` becomes `amount_minor=1250`, with no division, float conversion, or scale change; unsupported currencies cause no provider create; generated integer equality cases have no counterexample | Minimum/maximum amounts, zero/negative policy, accepted Python input types, and provider numeric limits are unspecified. Set approved bounds before claiming full input coverage; do not invent these rules. |
| v2-2026-10: exact supplied request and conflict contract | Provider extract as independently reviewed reference; integration owner | Contract fixture derived from `provider-api-v2.json`, not adapter/model helper; strict spy rejects missing/renamed fields and unapproved methods | All four required fields captured correctly; tenant/key unchanged by version switch; only USD accepted; same payload and changed-payload controls distinguish reuse from 409 conflict | Extract is not an OpenAPI document or complete transport schema. Response shape and error translation require qualification. |
| REQ-ID r3: tenant/key and payload identity, durable result for 24 hours | Temporal oracle plus independent effect journal; payments owner | Repeated and concurrent actions through the implementation; real chosen durable store in isolated restart tests, with persistent fake-provider journal | Same tenant/key and payload yields one durable provider charge ID and exactly one committed effect in all exercised schedules; other tenant using same key remains independent; changed amount or currency never receives success for an existing conflicting payload | Verify committed effects, not simply returned IDs or call count. A fake that always returns `p1` is insufficient. Payload equivalence and ID/response normalization need explicit review. |
| REQ-RETRY r3: timeout after commit and restart do not create another charge | Fault oracle around independent commit journal and documented lookup; integration + payments owners | Faults before send, before commit, after commit before reply, before/after local durable writes; application killed/restarted with persistent provider/storage state | Recovery observes or reconciles prior payment; same durable ID persists; committed effect count never exceeds one for the exercised logical payment; unresolved outcome is explicit and does not trigger an unkeyed or newly keyed create | Lookup consistency, not-found meaning, error handling and retry timing unknown. Treat ambiguity as unresolved until a qualified recovery rule permits progress. |
| REQ-ID/REQ-MIGRATE r3: expiry needs explicit caller decision | Reviewed clock/expiry state table; payments owner | Fake-clock cases just before, at, and after the 24-hour boundary, including restart and mixed-version retry; caller-decision audit | No automatic create after expiry; expired and unresolved operations cannot silently allocate another identity; explicit decision is recorded and follows reviewed policy | Start of window, inclusive boundary, clock skew allowance, retained tombstones, and decision API are not specified. Review these before claiming exact boundary correctness. |
| REQ-MIGRATE r3: one durable identity during old/new coexistence and rollback | Reviewed mixed-version state table and durable effects; integration + payments owners | Both supported binaries/adapter versions against one persistent identity store and provider journal; v1→v2, v2→v1, rollback-after-commit, retry-after-restart cases | Same tenant/key/payload resolves the same stored identity and ID across versions; no extra committed charge; data written by new version remains interpretable by the supported rollback version; every planned coexistence cell executes | Unmodified supplied v1 has no identity support. Provider extract does not say v1 and v2 share namespaces. Migration cannot be qualified until a compatibility path is shown. |
| Local environment model corresponds to provider within stated scenarios | Per-scenario fidelity comparison; integration owner | First map model behavior to independent supplied extract; subsequently, separately authorized provider sandbox/recorded interactions using specified provider/SDK versions | Document modeled, contradicted, and unverified behaviors separately; retain provider receipts and compare same/repeated/conflicting/tenant/lookup cases; unresolved mismatches prevent those scenarios being used as integration evidence | Supplied documents allow design now, not a current fidelity pass. Sandbox evidence is still bounded and may differ from production. |
| Safe promotion and recovery | Qualified monitors and recovery drill; existing release authority | Candidate-specific full reports, deployment configuration when available, controlled canary/reconciliation evidence | No missing required claims; evidence tied to deployed version; duplicate or identity divergence triggers a halt and reconciliation; recovery drill preserves committed payments and durable records | Proposed policy must be adopted through existing project process. Application rollback cannot cancel committed charges (`README.md:5–6`). |

Escalate a model/provider mismatch, ambiguous lookup, unknown legacy payment identity, stale semantic review, missing mandatory test, or incomplete mixed-version evidence as an unresolved claim. A local pass cannot compensate for an unavailable provider or persistence claim.

## Component Strategies

| Component | Archetype | Current | Recommended additions | Effort |
|-----------|-----------|---------|----------------------|--------|
| `adapter.py`: mapping and public entry point | API boundary with deterministic amount handling; high financial consequence | v1, no currency parameter, tenant/key unused (`:1–5`) | Typed request boundary, reviewed USD mapping, v2 contract tests, backward-compatible public wrapper during expansion | Small–medium |
| Identity, persistence, retry/reconciliation | Distributed/stateful; high financial consequence | Blind timeout retry; only in-memory model supplied | Explicit states and recovery transitions, durable identity repository, fault injection and restart tests against selected real store | Large; storage/runtime design unknown |
| `local_model.py`, fake, and test suite | Deterministic environment model used to explore a stateful boundary | Model predates migration; fake only covers amount echo | Separate independent expected values, versioned provider scenarios, persistent effect journal, generated action sequences, fidelity matrix | Medium |
| v1/v2 rollout and recovery | Migration across application/provider boundary | One coexistence window required; no rollout implementation supplied | Parallel change, mixed-version fixtures, compatibility evidence, reconciliation and staged removal | Large |

Use exact examples and properties for amount preservation; use protocol and fault sequences for identity across processes and versions. No arithmetic solver is currently needed for a field-preservation claim with no specified bounds or conservation computation. No formal tool is required solely because these are payments.

Proposed files: modify `adapter.py`, retain and replace the legacy assumptions in `local_model.py` through a reviewed revision, expand `tests/test_adapter.py`, add `tests/test_amount.py`, `tests/test_provider_contract.py`, `tests/test_idempotency.py`, `tests/test_recovery.py`, `tests/test_migration.py`, `tests/fixtures/provider_v2.py`, and `tests/fixtures/effect_journal.py`. Durable storage/module names depend on the actual architecture; proposed `idempotency.py` and `payment_store.py` are design placeholders, not existing files. Keep the old artifact unchanged for historical comparison.

## Oracle Strategy

| Component | Oracle type | Implementation | Properties / review lifecycle |
|-----------|-------------|----------------|-------------------------------|
| Amount/currency boundary | Exact + property | pytest literal expectations and Hypothesis integer cases after qualification | Independent `1250` expectation and a hand-written amount mapping table; no shared conversion helper. Review accepted input domain with requirement r3. |
| v2 provider boundary | Contract + behavioral environment model | Strict local fixture from independently reviewed API extract; explicit source lines per modeled behavior | Required arguments, tenant scope, 409, reuse, lookup. Version fixture and extract; do not infer unsupported response/status details. |
| Retry/durability | Temporal + independent journal | Model actions with known commit points; restart actual adapter/store process while retaining provider journal; compare durable effects | Count committed charge records, stable ID, conflicts, unresolved recovery, expiry, independent namespaces. Replay failed traces. |
| Migration | Differential/replay under approved differences + temporal | Compare old-compatible and v2 paths by normalized business identity and effect history | Preserve amount, tenant/key identity, durable ID and effect count. v1 method name/response shape may intentionally differ; old duplicate-charge behavior must not be preserved as a golden result. |
| Domain intent and unknowns | Human semantic review | Versioned claim/assertion/fixture/helper relationship record by payments and integration owners | Review boundary time and unknown recovery decisions; tests verify approved rules, while domain review validates that outcomes meet the payment need. |

Current oracle lifecycle: **adequacy: gap** (`tests/test_adapter.py:5–6` checks only one amount echo; model omits revised claims); **sensitivity: unknown** (no controls or mutations supplied); **independence: gap** for current expectations (fake echo/model are unqualified), while the provider extract provides a **supported independent documentary input** for its stated v2 fields and behaviors; **freshness: gap** for reusing r2 model results and **unknown** for any current assertion-to-r3 review. These dimensions are separate from execution status.

Create `verification/oracle-review.json` to bind each claim to requirement r3, provider extract v2-2026-10, assertion/fixture/helper/model hashes or versions, review date/owner, approved scope and unresolved gaps. Any change to a linked requirement, assertion, fixture, or helper invalidates affected semantic review. New runs and refreshed fingerprints cannot reapprove the meaning.

Qualify each gate with known-good and known-bad controls: USD 1250 preserved versus divided by 100; tenant-scoped keys versus global key map; reject payload conflict versus accepting original record; durable journal versus wiped-on-restart map; lookup/reconcile after commit versus another create; shared cross-version identity versus version-prefixed keys; caller decision on expiry versus automatic recharge. A control itself must violate the reviewed claim. Keep equivalent, out-of-scope, timed-out and untested mutations distinct.

Use the supplied old adapter and model for an old-versus-fixed regression once an executable environment exists: the timeout-after-commit fixture should expose an additional committed effect with the old code, and the fixed candidate should prevent it in the same setup. Neither outcome has been run here. No incident traces are supplied, so proposed scenarios are synthetic, not observed incidents.

### Candidate tool qualification

No installed releases, dependency lock, Python version, maintenance evidence, or license review are supplied. Candidate official documentation locations below are recorded for future review; they were not fetched. Qualification date/status as of 2026-10-11: **unknown/unreviewed** for releases, maintenance and distribution terms.

| Candidate | Intended use / evidence mode | Documentation location for later review | Qualification before use |
|-----------|------------------------------|-----------------------------------------|--------------------------|
| pytest | Local examples, contracts, process tests; sampled dynamic evidence and JUnit | `https://docs.pytest.org/` | Pin compatible release in proposed `pyproject.toml`/lock; verify fixture lifecycle, subprocess isolation and JUnit statuses. Pytest-style source does not establish installation. |
| Hypothesis | Integer and stateful sequence generation; sampled evidence | `https://hypothesis.readthedocs.io/` | Pin supported Python release; retain settings, example database, seeds/replay traces; validate restart modeling and controls. |
| Ruff and mypy | Fast lint and typed request protocols; scoped static evidence | `https://docs.astral.sh/ruff/`; `https://mypy.readthedocs.io/` | Pin separately; verify parser/version, exclusions and client Protocol coverage; supply annotations before assuming type checking can detect mapping errors. |
| Python standard-library scripts | Requirement IDs, report inventory, narrowly scoped AST checks | `https://docs.python.org/3/` | Pin runtime; qualify parsers against accepted and rejected fixtures and actual JUnit dialect. Scripts cannot judge semantic sufficiency. |
| TLC, conditional only | Complete exploration of an explicitly finite retry/expiry/overlap model | `https://lamport.azurewebsites.net/tla/tla.html` | Adopt only if schedule uncertainty remains; qualify release, limits, assumptions, invariant controls, implementation mapping and completed state-space report. Not needed for simple amount mapping. |

A selected real durable-store integration harness is necessary for persistence claims; the storage engine is unknown and is not selected from this snapshot. Avoid adding a contract framework or record-management platform until the small native fixture/report design is demonstrated.

## Safe-Evolution Strategy

Use **expand → migrate → contract**, with the same source/oracle/evidence checks at every phase. A staged rollout alone does not preserve durable effects.

1. **Expand.** Establish a canonical, persistent `(tenant, caller key)` identity and payload record shared by both supported versions, with the original provider identity/ID, status, timing and recovery information. Define storage atomicity and expiry rules before implementation. Add v2 alongside a backward-compatible `pay(..., cents)` entry point, with USD mapping made explicit. Deploy compatibility support to the version that may receive v1 traffic or serve as rollback target before mixed-version migration. The supplied unmodified adapter ignores tenant/key, so it is not a qualified coexistence or rollback target. Do not presume provider v1 accepts v2 keys or shares their namespace.
2. **Resolve the legacy gap before migration.** Inventory in-flight/completed v1 operations and demonstrate a reliable mapping to the canonical identity using authorized historical/provider evidence when available. If old charges cannot be mapped, quarantine/reconcile ambiguous retries; do not invent a new v2 key and charge again. A shared store alone cannot repair a crash after an unkeyed provider commit but before local persistence. A qualified lookup/reconciliation bridge or an approved traffic constraint is needed; none is established by these supplied files.
3. **Migrate incrementally.** Route a bounded cohort through v2 without changing tenant/key identity; persist state compatibly and test old→new and new→old retries, concurrent overlap, process restart, timeout after commit, payload conflicts, and expiry. Shadow only side-effect-free intent/lookup comparisons; never send two real create requests as an equivalence experiment. Gate each cohort with no duplicate committed effects and no unexplained identity divergence in retained evidence.
4. **Rollback/recovery.** Revert only to a compatibility version that can interpret current durable state and honor the shared identity. Preserve journal/state; disable unsafe new creates for ambiguous operations and reconcile committed payments. An application rollback does not undo a committed charge. Refund/compensation is a separate business action needing existing authorization, not an automatic outcome of rolling code back.
5. **Contract.** Remove old call paths only after the deployment coexistence window closes, no old callers/retry sources remain, and the reviewed retention/reconciliation policy safely covers outstanding operations and expired-key decisions. Do not equate elapsed deployment window with expiry of all financial effects. Retain identity records/tombstones as required to avoid automatic recharge after expiry; exact retention remains a reviewed design decision.

Acceptance per stage requires retained exact old/new source identities, store schema/configuration, scenario matrix, native reports, effect journals, and reviewed unresolved cases. Sweep/codemod machinery is unnecessary for this single supplied call site; use it only if a later caller inventory demonstrates a larger structural migration.

## Evidence Pipeline

| Risk level / affected scope | Merge requirements | Deploy requirements | Rollback triggers |
|-----------------------------|--------------------|--------------------|-------------------|
| High: payment mapping and provider contract | Full applicable local suite, reviewed v2 expectations, qualified controls, fresh expected/executed inventory | Candidate-specific provider qualification for required boundary scenarios; actual environment/version known | Any amount/currency mismatch or rejected conflict accepted |
| High: retry, durable identity, overlap | Fault/restart/mixed-version matrix against implementation and actual selected store; unchanged authorized review policy | Expansion compatibility proven; unresolved operations reconciled; deployment and rollback versions recorded; monitored controlled rollout | Any duplicate committed charge, cross-tenant identity reuse, changed durable ID for a logical payment, or automatic expired-key recharge |
| High: recovery and evidence | Semantically current claims and reports; missing/skipped/interrupted required checks do not count as passing | Verified recovery procedure and deploy policy; provider/hosting unknowns resolved for relevant claims | Halt expansion on unknown outcomes or missing reconciliation telemetry; thresholds/time budgets need owner agreement before rollout |

Low/medium/critical rows are not separately invented: all supplied production behavior concerns payments with high financial consequences, and no distinct regulatory or safety-critical obligation is supplied.

Five lanes: **static** (lint/types and request/boundary checks), **dynamic** (examples, store/restart and migration tests), **generative** (amount and stateful campaigns), **formal** (conditional exploration of remaining interleavings, not a substitute for provider qualification), **operational** (future canary, reconciliation and runtime identity monitoring). Retain lane-specific conclusions; sampled success means no counterexample in that campaign.

Four rails: **pre-merge** local examples/properties/fault tests; **boundary** documentary contract followed by separately scoped provider evidence; **production-proximate** authorized canary and persistent-effect reconciliation; **evidence** fresh report inventory and provenance. All four are applicable to the proposed integration, although the latter two are currently uninspectable. Signing is optional unless downstream consumers or actual release policy require authenticity; signatures cannot establish correctness.

Proposed `scripts/verify.py` writes a fresh `artifacts/<run-id>/` manifest and runner-native files. A deterministic inventory check joins expected IDs to actual testcase statuses and records missing, duplicate, skipped, error, interrupted, timeout and unsupported cases separately. Validate nested-suite and parameterized-test handling with fixture reports. Retain redacted outbound requests, independent committed-effect journals and replayable fault traces with source/oracle/environment identity. Test that an empty suite or stale report cannot satisfy promotion.

Current branch protection and approvals are unknown. These recommendations do not grant merge/deploy permission or remove an existing review. Apply existing authorization separately from evidence scores.

## Verification Cost Tiers

Commands below are **proposed aliases to implement**, not existing or executed commands. `scripts/verify.py` should dispatch qualified pinned tools and save the evidence bundle. Timing is a planning target, not a measured baseline.

| Component | Class (A–E) | Check (T1) | Verify-quick | Verify-full | Opt-out (auditable) |
|-----------|-------------|------------|--------------|-------------|---------------------|
| Amount/currency and request mapping | B primary for financial amount; A local mapping, D input boundary | `python scripts/verify.py check --component adapter`: Ruff, mypy, requirement/contract inventory; seconds | `python scripts/verify.py quick --component adapter`: examples and bounded integer/currency properties; 1–3 min target | `python scripts/verify.py full --component adapter`: required contract/control suite with relevant decision mutations at migration milestones | No formal/sanitizer requirement for field preservation; no native parser supplied. Record omission and revisit if arithmetic/native parsing is introduced. |
| Identity/retry/durable state | C primary, B consequence; deep | `python scripts/verify.py check --component recovery`: typed transitions and inventory | `python scripts/verify.py quick --component recovery`: fixed fault cases and one bounded sequence campaign | `python scripts/verify.py full --component recovery`: required before merge for protocol changes, multi-seed fault/restart tests; larger campaigns nightly | Do not skip explicit restart/after-commit cases. Conditional formal analysis only when unresolved interleavings justify it. |
| Mixed-version migration | C primary, B consequence; deep | `python scripts/verify.py check --component migration`: version/schema/review identity checks | `python scripts/verify.py quick --component migration`: deterministic direction/rollback cases | `python scripts/verify.py full --component migration`: required before each rollout phase, complete approved coexistence matrix; future authorized provider job separately gated | Provider receipts absent now are unknown, not an exemption or local pass. |
| Evidence tooling and documentation | A; standard | `python scripts/verify.py check --component evidence`: ID/link/review freshness lint | `python scripts/verify.py quick --component evidence`: good/bad/skipped/stale/native-report qualification fixtures | `python scripts/verify.py full --component evidence`: same small qualification suite at CI boundary; no heavy solver | Versioned opt-out may omit unrelated deep tools with reason and owner; never silently omit inventory parsing. |

**Hook/alias recommendations**: Add a local post-write or pre-commit hook invoking Check, and focused quick aliases after a logical edit. Full suite remains authoritative at the PR boundary; affected-only selection cannot replace it. Choose fixed quick campaign bounds after measuring runtime; a proposed initial full campaign is 20 seeds × 100 action sequences, plus every required deterministic fault/overlap case. Record actual counts and lengths; this finite proposal is not a universal sufficiency threshold.

**Ceremony flags**: No hook configuration is supplied, so no actual late-only check or full-on-save misuse is established. Keep real provider calls, process restart matrices, long mutation campaigns, and any TLC exploration out of every-save hooks. Simple amount mapping has high consequence but does not automatically need model checking.

## Shift-Left Recommendations

| Check | Current tier | Target tier | Action | Tool/config |
|-------|--------------|-------------|--------|-------------|
| Lint/types/request shape | Unknown; no supplied config | T1 and repeat at T3 | Add focused checks and explicit provider Protocol | Proposed `pyproject.toml`, qualified Ruff/mypy, post-write hook |
| Amount and exact contract examples | Test source exists; execution tier unknown | T2, full suite T3 | Expand current test; expose component alias | pytest via proposed `scripts/verify.py` |
| Fault/restart/overlap | No checks supplied | Small deterministic cases T2; full matrix T3 | Separate costly campaigns from fast cases | Marker configuration and fake clock/fault hooks |
| Real provider qualification and canary | Unknown/unavailable | T3 where sandbox permits; T4 for deployed behavior | Keep boundary receipts separate from local results | Provider-specific job/config chosen after qualification |
| Requirement links and review freshness | Stable requirement IDs only | T1, authoritative T3 | Parse mappings and report changed linked artifacts | Proposed `verification/claims.json` and review records |

## Feedback Loop Improvements

| Verification method | Current level | Target level | Action | Config change |
|---------------------|--------------|--------------|--------|---------------|
| Test suite | Unknown; only source supplied | 2, then demonstrate 3 | Produce attributable structured failures and route through existing CI to authorized agent repair | pytest JUnit plus manifest; actual CI workflow to upload always, including failures |
| Model campaign | At most partial Level 1 evidence: JSON summary, no individual results/routing | 2 | Preserve scenario ID, trace, seed, bounds, status, actual effect history and versions | Replace summary-only future output with per-case records and native test reports |
| Static checks | Unknown | 2 | Emit structured lint/type diagnostics with file/line and actionable requirement context | Ruff JSON, qualified mypy output adapter in verification script |
| Recovery/operational checks | Unknown | 2 | Retrieve per-deploy redacted reconciliation evidence using existing permitted observability path | Decide actual hosting/CI API after environment inspection; do not invent configured integrations |

A rerun must have a new run ID and execute affected checks, preserving the failure artifact. Add an existing-CI dispatch/retry entry only after verifying permissions and preventing duplicate payment effects. Demonstrate structured failure → scoped repair → rerun before claiming Level 3; configuration alone establishes no closed loop.

## Workflow Gate Optimization

| Gate | Current state | Recommendation | Risk class | Impact on agent throughput |
|------|--------------|----------------|-----------|---------------------------|
| Priority/spec | r3 requirements approved; detailed expiry/recovery semantics missing | Preserve approval and close only identified consequential ambiguities with designated owners | High | Avoid reapproval of settled requirements; resolve unknowns before dependent implementation |
| Mechanical merge checks | Unknown | Consolidate local/CI invocations behind same scripts after qualifying controls and report inventory | High | Faster local repair and less repeated manual checking |
| Ship and rollout | Unknown | Require scoped migration/recovery evidence and use existing release authority; keep unresolved provider/legacy identity claims explicit | High | Prevents unreviewable large rollout; no inferred permission change |
| Gate failures | No routing evidence | Return claim ID, failing scenario, source/oracle revision, environment, trace and remediation hint | All affected | Enables targeted corrections |

The priority/spec/ship purposes need not become three new approval steps. No evidence supports removing or consolidating a particular current human gate. Inspect actual server-side check enforcement and bypass permissions later; local hooks alone cannot prove enforcement.

## Architecture Fitness Functions

These proposed decisions need review before enforcement. Snapshot maturity is Level 0 for visible automated fitness functions; actual external enforcement is unknown. Target Level 3 (local + CI), then Level 4 after scope/control qualification.

| Property | Type | Tool / qualified scope | Runs at | Controls / remaining limits |
|----------|------|------------------------|---------|-----------------------------|
| Domain identity policy independent of provider SDK | Dependency | Small Python AST import check initially; proposed domain/store modules and `adapter.py`, with documented source exclusions | Check T1/T3 | Allow adapter→domain, reject domain→provider including alias/nested import fixtures. Trace indirect edges or mark unresolved; dynamic imports/re-exports need explicit review. |
| Supported old caller surface survives expansion | API compatibility | pytest call-signature/behavior fixtures for supplied `pay(client, tenant, key, cents)` plus new v2 entry point | Quick T2/T3 | Allowed compatible wrapper and rejected parameter removal; only supplied consumer is known, so later inventory real callers. |
| Provider create/lookup flows use reviewed identity and mapping | Boundary/security | Typed request plus dynamic strict spy; narrow AST rule for provider calls only within adapter | Check + quick | Allow correct tenant/key/amount/currency; reject unkeyed calls and cross-tenant lookup. Presence of fields alone does not establish authorized tenant ownership; caller authentication is outside supplied scope. |
| Required scenarios and fixtures have ownership/revision records | Structural | Deterministic inventory parser | Check T1/T3 | Accepted record, missing ID, stale review, duplicate/missing/skipped testcase controls. File-count/coverage targets do not replace this. |
| Recovery terminates or reports unresolved within a reviewed operational budget | Performance/protocol | Fake-clock deadline cases plus later measured provider/store integration benchmark | Quick for clock logic; full/nightly for load | No latency SLO supplied; select budget after observing actual provider timing, not an invented p99 target. Timeout control must not auto-recharge. |

Actionable error format: `FIT-ID [REQ-…] path:line observed=<edge/request/state> expected=<reviewed rule> scenario=<id> remediation=<specific boundary or policy>`. Record reviewed exceptions with reason, owner, scope and expiry; start with stated boundaries rather than arbitrary file-size/coverage thresholds.

**Maintenance exercise**: After expansion, add a second test-only provider implementation through the intended adapter interface. Record expert/agent effort, unexpected edits outside the adapter, behavior regressions and import-boundary results. Success means the reviewed exercise fits intended extension points and preserves relevant checks. It does not prove general maintainability; complexity and coupling measurements are investigation aids.

## Eval Framework

No project history, issues or PRs are supplied. The following are **synthetic seed tasks derived from this snapshot**, not historical tasks or executed evaluations. Human-expert times are estimates pending calibration.

| Task | Source | Difficulty | Files | Success criteria |
|------|--------|-----------|-------|------------------|
| Preserve 1250 USD minor units in v2 | REQ-AMOUNT and v2 extract | Easy, 15–30 min | `adapter.py`, amount/contract tests | Independent literal expectation, required fields, unsupported currency rejection, types/lint |
| Reject conflicting payload and separate tenants | REQ-ID; deficiencies in local model | Medium, 45–90 min | Identity module/model and tests | Reject changed payload; same key other tenant remains independent; negative controls detect global namespace |
| Recover timeout after commit and restart | REQ-RETRY; `README.md:5–6` | Hard, 2–6 hr | Adapter/store/recovery tests | Durable effect journal records one charge; process restart trace retained; unresolved outcome does not blindly recreate |
| Introduce compatible v1/v2 overlap | REQ-MIGRATE | Hard, 4–8 hr or beyond if infrastructure absent | Adapter, store schema, migration tests/docs | Both retry directions and rollback preserve durable identity; recognizes missing v1 provider guarantees instead of inventing them |
| Correct expiry decision behavior | `requirements.md:9` | Medium, 1–2 hr after semantic decisions | State policy, clock tests, caller contract | No automatic expiry recharge; approved exact time boundary and explicit decision recorded |
| Reject stale/incomplete evidence | `evidence/model-r2.json` | Easy–medium, 30–60 min | Evidence parser/fixture reports | Old revision, skipped/missing tests and summary-only results remain unknown/incomplete; no provider pass inferred |
| Add second adapter through intended interface | Proposed architecture exercise | Medium, 1–2 hr | Test adapter, boundary tests/docs | Bounded authorized edits, existing behavior preserved, unexpected changes and effort reported |

Measurement: independently author accepted/rejected labels from requirements and provider documentation before reading candidate implementations. Record correctness, convention adherence, efficiency, scope discipline, robustness and repair attempts. Pin source fixtures, requirement/oracle labels, model/configuration, prompt, tools and budget. An initial proposed pilot is three attempts per task with counts and uncertainty reported; do not claim general reliability or deployment authorization from 21 outcomes. Separate held-back cases where practical and record exposure through feedback.

Prohibited overclaims include treating the local fake/model as live provider evidence, describing 50 old sequences as current coverage, claiming rollback reverses charges, calling a schema match durable idempotency, or accepting identical IDs without checking effects. Classify failures as oracle/harness defects, model behavior, environment/missing prerequisite, or task difficulty; preserve timeouts and unknowns. Future `scripts/run_evals.py` should run in isolated fixtures on model/harness changes and scheduled CI, without real charge creation.

## Generator-Evaluator Recommendations

| Component | Variant | When to apply | Cost management |
|-----------|---------|--------------|-----------------|
| Provider mapping and revision 3 scenarios | Generator + Test-Writer | Implementation generator receives approved spec; independent test writer receives requirements and provider extract but not implementation/reasoning | One separate pass for migration foundation; reconcile conflicting interpretations with domain owner |
| Retry and migration phases | Generator + Critic | Critic uses crash points, identity, expiry, legacy mapping and rollback rubric | Each protocol-changing phase; retain concrete findings rather than an unqualified approval score |
| Consequential checks | Generator + Mutant | Mutate no-key retry, tenant scope, payload guard, expiry and durable persistence | Small reviewed control set per change; larger campaigns scheduled; separate equivalent/out-of-scope survivors |

Tests and critique enter ordinary CI and semantic review; consequential disagreement escalates to the named owner. N-of-M consensus is not proposed: shared mistaken provider assumptions would remain, while independent contract and fault evidence address identified gaps more directly. No model judge is required for deterministic payment assertions.

## Documentation Verification

| Dimension | Current | Recommendation | Tool |
|-----------|---------|----------------|------|
| Auto-generation | Supplied README and requirement text; no docs pipeline | Add typed adapter interface and documented compatibility wrapper; large documentation framework unnecessary here | Python annotations/docstrings, reviewed Markdown |
| CI doc build | Not supplied; actual state unknown | Add small syntax/link/reference checks to same Check alias | Qualified local Markdown/reference script |
| Link validation | No result supplied | Check repository-relative links and stable claim references offline; external freshness remains unknown until authorized | Standard-library path/anchor checker |
| Example testing | Existing test is amount-only and not a documented v2 example | Add literal v2 request, conflict and unresolved-recovery examples backed by executable fixtures | pytest example cases |
| Schema-doc sync | Independent v2 extract exists; code calls v1 | Highest priority: compare extract-required fields/values to recorded request fixtures and approved intentional differences | JSON parsing + strict contract tests; do not feed the extract to an OpenAPI tool as though it were a complete specification |
| Freshness enforcement | Requirements approved, test/model relationship not reviewed | Link changes in requirements/extract/assertions/fixtures/helpers to affected review records and migration notes | Inventory fingerprints plus owner semantic review |

## Requirement Traceability

**Current evidence → proposed target**: Stable IDs and documented r3 approval exist. No explicit test-ID links, native execution inventory, PR/change reference, or assertion relationship review is supplied. The single amount test gives partial apparent relevance, not full requirement coverage.

| Obligation | Current evidence / gaps | Proposed mechanism | Completion criteria / review owner |
|------------|-------------------------|--------------------|------------------------------------|
| Links and relevant change references | REQ-AMOUNT, REQ-ID, REQ-RETRY, REQ-MIGRATE exist; expiry sentence not separately mapped | `verification/claims.json`: retain parent IDs and give expiry, namespace, conflict, recovery and overlap subclaims stable check mappings; relevant change reference when available | All affected subclaims and source/test paths resolve; missing links and maintenance exceptions explicit; payments owner reviews mapping relevance |
| Expected vs executed checks | r2 summary is stale; no current native results | Expected scenario inventory joined to fresh pytest JUnit and campaign records, separate local/store/provider/deployed environments | Required actual testcase statuses accounted for with source/oracle/environment identity; reject missing/duplicate/skipped/stale/partial reports as completion evidence; harness owner to be designated |
| Assertion-to-claim meaning and freshness | r3 approval and extract review supplied; relationship review unknown | Versioned review of requirement + assertions + fixtures + expectation helpers, adequacy/sensitivity/independence/freshness fields | Payments/integration owners approve exact supported scope; linked changes invalidate review; partial claims, deviations and unknowns remain explicit |

Start with Markdown, JSON and runner-native results. No need to adopt Sphinx-Needs, StrictDoc, Reqstool or Doorstop for four requirement IDs without demonstrating a gap. If later considered, pilot accepted/rejected/skipped/missing/stale/partial records and exact runner dialects first. Parsing or a fresh hash cannot establish semantic correctness.

## Implementation Roadmap

All work below is proposed; no tests, implementation, provider probes or deployments were performed for this report.

### Phase 1: Quick wins

| # | Action / failure addressed | Component | Effort | Completion evidence |
|---|---------------------------|-----------|--------|---------------------|
| 1 | Record r2 model limitations and r3 requirement-to-scenario mapping; prevent false reuse | Model/evidence | Small; no dependency | Reviewed claim inventory distinguishes historical summary, configuration and missing execution; pytest/JSON parser candidates qualified with stale/empty controls |
| 2 | Pin tool/runtime baseline; add Check/quick aliases and native reports | Harness | Small–medium; depends on actual supported Python/CI | Tool qualification records, lock/config, example failure artifact and expected/executed inventory; timings measured |
| 3 | Add independently derived amount/currency/v2 contract tests and bad controls | Adapter | Small–medium; depends on fixture/tool review | Complete native reports showing correct mapping and detection of scale/missing-field errors; no provider conclusion inferred |
| 4 | Resolve expiry boundary, payload identity, lookup semantics and legacy cross-version bridge | Protocol/spec | Medium; requires domain/provider knowledge absent here | Reviewed state table with explicit remaining unknowns; no dependent migration gate claimed complete while unresolved |

### Phase 2: Foundation

| # | Action / failure addressed | Component | Effort | Completion evidence |
|---|---------------------------|-----------|--------|---------------------|
| 5 | Implement expand-compatible durable identity and recovery state machine | Adapter/store | Large; depends on 4 and actual storage choice | Actual-store restart and commit-point fault reports, independent effect journal, old-versus-fixed regression outcomes |
| 6 | Build r3 local environment model and generated sequences | Model/tests | Medium; depends on reviewed transitions and controls | Seed/bound/version records, per-case outcomes and shrunk traces; modeled versus independently documented scope explicit |
| 7 | Qualify boundary against permitted provider evidence and wire full migration matrix | Provider/migration | Medium–large; depends on 4–6 and authorized environment | Per-scenario receipts/configuration, documented fidelity gaps, both coexistence directions and rollback compatibility reports |
| 8 | Close CI feedback, evidence traceability and documentation gaps | Harness/docs | Medium; depends on actual CI settings | Retrievable failure bundle, permitted rerun demonstration, stale/missing/report-parser controls, revised semantic reviews |

### Phase 3: Deeper checks where justified

| # | Action / failure addressed | Component | Effort | Completion evidence |
|---|---------------------------|-----------|--------|---------------------|
| 9 | Explore remaining interleavings; consider finite TLC model only if fault campaigns leave material protocol uncertainty | Protocol | Medium–large; depends on 5–7 | Declared finite states/assumptions, controls, complete exploration or explicit timeout/incomplete status, implementation correspondence; never provider proof |
| 10 | Controlled migrate/contract phases with recovery drill and reconciliation | Rollout | Large; depends on required current evidence and existing authorization | Exact versions, cohort history, no unexplained duplicate effects in inspected window, compatible rollback drill, unresolved records retained |
| 11 | Pilot synthetic agent tasks and representative adapter extension | Workflow/maintainability | Medium; depends on a qualified harness | Independently reviewed labels, repeated-attempt results, effort/unexpected edits/regressions, limitations and exposure record |

The immediate design blocker for migration readiness is the missing qualified bridge between legacy unkeyed effects and the durable tenant/key identity. Local test design can proceed from supplied files; provider fidelity, persistence behavior and deployment readiness remain unknown until separately scoped evidence exists.
