# Verification Maturity Model

**Rubric ID**: `verification-maturity/2` (software-verification 0.6). Include this ID in reports.

Maturity measures how reliably an appropriate verification portfolio informs decisions. It does
not rank methods by prestige or require proof for every component. Load `evidence-semantics.md`
before assigning tiers; use `bug-surface-routing.md` to identify relevant failure modes.

## Maturity tiers

| Tier | Name | Required evidence |
|------|------|-------------------|
| 0 | None | No applicable automated checks found in the inspected scope |
| 1 | Configured | Checks exist; current execution, reliability, or enforcement is unconfirmed |
| 2 | Reliable | Relevant checks run repeatably on identified revisions and required gates enforce results |
| 3 | Risk-matched | Approved claims and complementary checks address the component's important failure surfaces |
| 4 | Qualified | Oracles, check sensitivity, and environment fidelity are qualified for those claims |
| 5 | Managed evidence | Current traceable evidence and explicit policies govern decisions and feed ongoing improvement |

## Assignment rules

- Assign the highest tier whose applicable criteria below are supported by inspected evidence.
  Report the demonstrated tier separately from the configured or recommended target.
- Unknown evidence is not a proven failure. Mark the missing evidence and make the recommendation
  provisional; configuration alone supports Tier 1, not confirmed successful execution.
- Use `unknown` rather than Tier 0 if the scope cannot be inspected sufficiently to determine
  whether checks exist. Do not infer missing remote enforcement from working-tree absence.
- Score components separately. Overall tier is the highest tier met by every in-scope critical
  path (the lowest demonstrated component tier); identify the limiting paths. If none are critical,
  use the assessed components. An unknown critical-path tier keeps the overall tier provisional.
  Do not average away a critical gap with an unrelated proof or strong documentation.
- Justify inapplicable checks by claim, bug surface, and environment. No numerical bonus follows
  from adding a tool. Formal analysis is useful where it resolves an identified gap.
- This rubric replaces the earlier method ladder. Record the rubric version/date when comparing
  historical reports; an unchanged codebase may receive a different tier under revised criteria.

## Tier criteria

### Tier 1 — Configured

- Test/check implementations or configured analysis exist.
- Reports distinguish this capability from inspected runs.
- Missing execution evidence, unsupported scope, and skipped jobs are visible.

### Tier 2 — Reliable

- Recent representative runs apply to identified source/configuration and complete relevant checks.
- Required merge/release enforcement is inspected where relevant; local-only hooks are identified.
- Repeatability or flake observations support reliability; a single green run is insufficient.
- Failure diagnostics identify the check and affected scope.

### Tier 3 — Risk-matched

- Tier 2 plus approved claims and identified failure modes for the assessed surface.
- Checks cover appropriate cases, boundaries, faults, and environments with explicit remaining gaps.
- Choose examples, generated properties, fuzzing, schedule exploration, proofs, or operational
  validation according to the claim. A small enumerable invariant may need no generative/formal tool.
- Exemptions are justified. A complex protocol needs evidence for schedules/faults; merely lacking
  a named model checker is not itself a finding.

### Tier 4 — Qualified

- Tier 3 plus inspected semantic-review freshness and oracle adequacy/independence.
- Known-good/known-bad controls or equivalent sensitivity evidence qualify consequential checks.
- Requirement mappings identify current executed evidence and reviewed partial claims.
- Relevant environment fidelity is supported: a model/twin is not assumed equivalent to production.
- Production-facing claims have representative operational or deployed evidence where local
  evidence cannot establish them; purely local components may justify that evidence as inapplicable.

### Tier 5 — Managed evidence

- Tier 4 plus revision-bound evidence and explicit decision policies for required claims.
- Policies distinguish complete positive evidence from timeout, stale, missing, or unsupported runs;
  unresolved required claims block promotion or receive explicit, scoped exception review.
- Oracle/requirement changes trigger impact review; incidents update regression assets.
- Operational outcomes, overrides, and check effectiveness inform portfolio maintenance.
- Recovery and escalation are exercised where applicable. Automation and human review are chosen
  by consequence and ambiguity, not removed merely to satisfy a tier.

## Agentic test portfolio

| Layer | Typical checks | Interpretation |
|-------|----------------|----------------|
| Fast local loop | Validators, state machines, tool handlers | Repeatable results for declared cases/properties |
| Integration/evaluation | Recorded interactions, calibrated model judges, contract scenarios | Scope depends on replay/twin fidelity and oracle review |
| Representative environment | Staging, user/maintenance tasks, operational observations | Evidence about studied conditions; feed discoveries into cheaper checks |

Prefer fast deterministic feedback where it answers the claim. Keep expensive environment checks
when they cover failures the fast loop cannot see.

## Autonomy interpretation

There is no automatic tier-to-L0–L5 conversion. Recommend operating scope per changed surface from
oracle adequacy, current evidence, blast radius, recovery, and unresolved assumptions. A Tier 5
evidence process can correctly deny autonomous changes on an unqualified new integration.
Tier labels describe verification maturity; they do not authorize actions or replace readiness
hard prerequisites and the user's configured review policy.
