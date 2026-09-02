# Workflow Gate Design Patterns

## The three-checkpoint model

Consolidate human review to three high-value gates instead of many low-value interruptions:

| Gate | Purpose | Human role | Agent role |
|------|---------|------------|------------|
| Priority review | Confirm what to work on next | Correct agent-aggregated signals | Triage, rank, summarize context |
| Spec review | Validate plan before execution | Approve intent and scope | Draft spec, identify risks, propose approach |
| Ship review | Final validation before merge/deploy | Verify intent preserved, catch policy violations | High-recall automated inspection, regression checks |

## Gate anti-patterns

| Anti-pattern | Symptom | Fix |
|--------------|---------|-----|
| Rubber-stamp gate | Reviewer approves >95% without changes | Remove gate or make it agent-only |
| Bottleneck gate | PR queue grows faster than review capacity | Automate with agent pre-review, escalate only exceptions |
| Duplicate gate | Same check done by CI and human reviewer | Remove human check where CI is authoritative |
| Late-stage gate | Issues caught at deploy that could be caught at PR | Shift check earlier (fail fast) |
| Missing gate | High-risk changes ship with no human review | Add targeted approval for risk class |
| Bypassable gate | Agent routes around a hook (`git commit --no-verify`, skipping CI) | Deny bypass commands in agent config; make CI the non-negotiable server-side gate |
| Silent skip | Artifact exists (TLA+ module, scanner config, formal spec) but gate skips when unwired | Fail loudly — see **Presence ⇒ mandatory** below |
| Vacuous gate | Gate reports green while checking nothing (empty ruleset, unconstrained invariant) | Require non-empty config + anti-vacuity probe; see **Vacuous gates** below |

## Presence ⇒ mandatory

If the repo **looks** verifiable — a formal spec on disk, a `(verified=…)` marker, a scanner
config, an FSM source — the pipeline must either **run the corresponding gate** or **fail with an
explicit opt-out**. Never silently skip.

| Signal on disk | Mandatory gate behavior |
|----------------|-------------------------|
| Requirement with `(verified=kani\|proptest\|tla\|dst)` marker | Matching proof/test/spec must exist and run in verify-quick or CI |
| TLA+ / Alloy module with invariants | Model checker runs; each invariant has a known-violating mutation the checker must catch |
| FSM `next()` source declared in config | Spec sync check + regenerated formal artifact in gate path |
| Secret scanner config present | Non-empty ruleset; empty config = fail (not pass) |
| Coverage threshold configured | Mutation testing or equivalent on verified core (coverage alone is insufficient) |

**Auditable opt-out:** "Out of scope" must be declared in versioned config (e.g. exempt list with
reason), not implied by absence. Accidental absence must never read as passing.

## Vacuous gates

Worse than no gate: a gate that **manufactures confidence**. Common vacuous patterns:

| Vacuous pattern | Why it lies | Fix |
|-----------------|-------------|-----|
| Secret scanner with no rules | Always green | Fail if config empty; ship default ruleset |
| TLA+ invariant that constrains nothing | TLC passes vacuously | Anti-vacuity mutation table — flip guard, expect violation |
| Coverage gate on wrong package | Green while core untested | Scope coverage to verified core crate/module |
| Mutation testing never run | High line coverage, hollow tests | Run mutants on core; fail on surviving mutants |
| BDD scenarios exist but no REQ linkage | Scenarios drift from intent | Meta-gate: every active REQ has tagged scenario |
| Traceability matrix maintained by hand | Agent/human drift undetected | Deterministic script parses IDs/tags; fail on gaps |

**Anti-vacuity probe:** for each formal invariant or gate, maintain a **known-bad mutation** the
tool must reject. If the mutation passes, the gate is toothless — fail the meta-gate, not the product.

Load `../../detect-ai-smells/references/detection-patterns-gates-formal.md` (AI011) for formal-spec vacuity
detection patterns.

## Candidate selection (mandatory vs objectives)

When CI or search ranks multiple candidates, load `candidate-selection-policy.md` — the canonical
rule. Gate-design consequence: required checks and informational metrics must be separate CI
statuses, so a combined score can never trade correctness for speed.

## Enforcement integrity (agents route around blockers)

Agents are task-oriented: when a local hook blocks them too hard, they tend to bypass it
(e.g. `git commit --no-verify`, `--no-gpg-sign`, force-push). A guardrail an agent can skip is
not a guardrail. Harden enforcement in layers:

| Layer | Mechanism | Bypass risk |
|-------|-----------|-------------|
| Agent hooks (post-write) | Run tools after each edit; feed output back | High — agent controls its own loop |
| Pre-commit hooks | Block commit until tools pass | Medium — `--no-verify` skips them |
| Deny bypass commands | Agent tool config denies `.*git.*--no-verify.*` and similar | Low — agent cannot issue the command |
| CI/CD + branch protection | Server-side checks; no merge unless all pass | Lowest — outside the agent's environment |

The non-negotiable gate lives server-side (branch protection + required checks). Local hooks are
for fast feedback; deny-listing bypass commands keeps the agent honest in between.

## Gate positioning by risk class

| Risk class | Recommended gates | Rationale |
|------------|-------------------|-----------|
| Low (utilities, internal tools) | CI only | Automated checks sufficient; human review is waste |
| Medium (business logic, APIs) | CI + agent review | Agent catches intent drift; human escalation on ambiguity |
| High (payments, auth, data) | CI + agent review + human approval | Human judgment needed for blast radius |
| Critical (safety, security, compliance) | CI + agent review + domain expert approval | Regulatory or safety obligation |

## Assessing current gate placement

For each existing review/approval checkpoint, evaluate:

| Dimension | Question |
|-----------|----------|
| Value | Does this gate catch issues that no automated check can? |
| Position | Is this gate at the earliest point where the check is meaningful? |
| Throughput | Can this gate handle the volume of agent-generated changes? |
| Scope | Is the gate scoped to the right risk level (not too broad, not too narrow)? |
| Feedback | Does rejection at this gate produce actionable feedback for the agent? |

## Consolidation decision matrix

| Current state | Recommendation |
|---------------|----------------|
| Many low-value human gates, low rejection rate | Consolidate to three-checkpoint model |
| Single gate at merge, high rejection rate | Add earlier spec review gate to catch issues sooner |
| No human gates, high revert rate | Add ship review for high-risk components |
| Human reviews everything equally | Segment by risk class, automate low-risk |
