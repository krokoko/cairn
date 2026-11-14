# Workflow Gate Design Patterns

## The three-checkpoint model

Consider these review purposes when consolidating redundant checkpoints. They need not be three
separate approvals; preserve existing user authorization and project requirements.

| Gate | Purpose | Human role | Agent role |
|------|---------|------------|------------|
| Priority review | Confirm what to work on next | Correct agent-aggregated signals | Triage, rank, summarize context |
| Spec review | Validate plan before execution | Approve intent and scope | Draft spec, identify risks, propose approach |
| Ship review | Final validation before merge/deploy | Verify intent preserved, catch policy violations | High-recall automated inspection, regression checks |

## Gate anti-patterns

| Anti-pattern | Symptom | Fix |
|--------------|---------|-----|
| Rubber-stamp gate | Reviewer rarely changes outcomes | Investigate value and risk before consolidating |
| Bottleneck gate | PR queue grows faster than review capacity | Automate with agent pre-review, escalate only exceptions |
| Duplicate gate | Same mechanical check done by CI and reviewer | Consolidate after qualifying CI; retain intent review |
| Late-stage gate | Issues caught at deploy that could be caught at PR | Shift check earlier (fail fast) |
| Missing gate | A consequential decision has no adequate check | Add a scoped check or designated review |
| Bypassable gate | Agent routes around a hook (`git commit --no-verify`, skipping CI) | Deny bypass commands in agent config; make CI the non-negotiable server-side gate |
| Silent skip | An active required claim/check is declared but its gate skips when unwired | Report failure or explicit unsupported state — see **Active required claims** below |
| Vacuous gate | Gate reports green while checking nothing (empty ruleset, unconstrained invariant) | Require non-empty config + anti-vacuity probe; see **Vacuous gates** below |

## Active required claims

For each check declared required by the project, the pipeline must run it or report an explicit
missing/unsupported state under the project's opt-out policy. Never turn a silent skip into a pass.
Inventory formal files and markers, but distinguish active claims from examples and inactive drafts.

| Signal on disk | Mandatory gate behavior |
|----------------|-------------------------|
| Active requirement with a project-recognized `(verified=kani\|proptest\|tla\|dst)` claim | Matching proof/test/spec must exist and run in verify-quick or CI; otherwise report the claim unsupported |
| Active TLA+ / Alloy claim | Completed checked scope and relevant known-violating controls; justify unsupported probes |
| FSM `next()` source declared in config | Spec sync check + regenerated formal artifact in gate path |
| Required secret scanner | Confirm effective rules including inherited defaults; inspect a known secret control |
| Coverage threshold declared required | Check source/branch scope; use relevant negative controls for assertion sensitivity |

**Auditable opt-out:** "Out of scope" must be declared in versioned config (e.g. exempt list with
reason), not implied by absence. Accidental absence must never read as passing.
Examples, tutorial markers, draft specs, and optional exploratory checks do not become mandatory
merely because files exist. Record their status; an active correctness claim cannot be exempted
silently or reported as established when its check is inactive.

## Vacuous gates

Worse than no gate: a gate that **manufactures confidence**. Common vacuous patterns:

| Vacuous pattern | Why it lies | Fix |
|-----------------|-------------|-----|
| Secret scanner with no effective rules | No configured detection | Validate inherited/default rules and a known secret control |
| TLA+ invariant that constrains nothing | TLC passes vacuously | Anti-vacuity mutation table — flip guard, expect violation |
| Coverage gate on wrong package | Green while core untested | Scope coverage to verified core crate/module |
| Assertion sensitivity untested | Coverage alone cannot show detection | Run relevant controls/mutants; investigate equivalent survivors |
| Acceptance declarations without execution | Scenarios can be listed without running | Compare expected checks with fresh runner reports |
| Traceability links treated as correctness | IDs can resolve while meaning is stale | Separate deterministic link/execution checks from semantic review |

**Anti-vacuity probe:** qualify critical gates with known-good and known-bad controls within the
claimed scope. A relevant violation passing is a qualification failure; investigate configuration,
encoding, reachability, and scope before interpreting the product result. Mutation does not establish
that the requirement is current, and equivalent mutations do not demonstrate weak assertions.

Load `../../detect-ai-smells/references/detection-patterns-gates-formal.md` (AI011) for formal-spec vacuity
detection patterns.

## Enforcement integrity (agents route around blockers)

Agents are task-oriented: when a local hook blocks them too hard, they tend to bypass it
(e.g. `git commit --no-verify`, `--no-gpg-sign`, force-push). A guardrail an agent can skip is
not a guardrail. Harden enforcement in layers:

| Layer | Mechanism | Bypass risk |
|-------|-----------|-------------|
| Agent hooks (post-write) | Run tools after each edit; feed output back | High — agent controls its own loop |
| Pre-commit hooks | Block commit until tools pass | Medium — `--no-verify` skips them |
| Tool permission controls | Enforce permitted actions independently of tests | Depends on actual tool boundary and alternate paths |
| CI/CD + branch protection | Required server-side checks | Inspect bypass permissions, identities, and settings |

Local hooks provide fast feedback. Server-side policy needs verified configuration and appropriate
bypass permissions; a command denylist alone does not establish enforcement.

## Gate positioning by risk class

| Risk class | Recommended gates | Rationale |
|------------|-------------------|-----------|
| Low (utilities, internal tools) | Fast relevant checks | Retain review where intent is ambiguous |
| Medium (business logic, APIs) | Boundary evidence and scoped review | Agent review is supplemental evidence |
| High (payments, auth, data) | Qualified failure/rollback checks and consequential intent review | Follow existing approval policy |
| Critical (safety, security, compliance) | Supported scoped methods plus applicable expert review | Establish actual obligations, not inferred requirements |

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
| Many low-value human gates, low rejection rate | Evaluate consolidation after checking distinct coverage and approval requirements |
| Single gate at merge, high rejection rate | Add earlier spec review gate to catch issues sooner |
| No human gates, high revert rate | Add ship review for high-risk components |
| Human reviews everything equally | Segment by risk class, automate low-risk |

Before recommending consolidation, sample comparable decisions (start with the latest 20 if no
project window exists), record material corrections, rejected proposals, and later escapes, and
separate risk classes. Approval above 95% is a review trigger, not proof that a gate is useless:
earlier feedback or deterrence may explain it. Consolidate only after equivalent coverage and
existing approval requirements are accounted for; retain the gate when evidence is insufficient.
