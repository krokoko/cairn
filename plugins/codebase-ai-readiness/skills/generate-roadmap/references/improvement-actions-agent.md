# Improvement Actions (Agent Surfaces)

Continues `improvement-actions.md`. Choose relevant actions from observed failures.
Acceptance criteria describe evidence to obtain, not a promised score increase.
Examples are implementation candidates; retain the project's existing tools when they meet the need.

## Failure mode legibility

Examples: typed error classes/codes; ESLint `no-empty` or Semgrep rules for reviewed masking patterns;
structured CI diagnostics with rule ID, location, and remediation.

| Action | Effort | Failure addressed | Acceptance criterion |
|--------|--------|-------------------|----------------------|
| Audit swallowed errors | Medium | Failures are hidden as successful results | Representative failures surface the cause and preserve an actionable result |
| Add structured errors/codes | Medium | Agents cannot distinguish recovery paths | Known error classes have stable identifiers and supported recovery behavior |
| Add remediation to lint/CI feedback | Small | Agents repeat edits without understanding the failure | A deliberate violation identifies the rule, location and useful next action |

## Feedforward surfaces

Examples: AGENTS/CLAUDE project rules; eslint-plugin-boundaries, Import Linter or ArchUnit;
pre-commit/lefthook; plop/hygen templates; Semgrep, bandit or gitleaks; required server-side checks.

| Action | Effort | Failure addressed | Acceptance criterion |
|--------|--------|-------------------|----------------------|
| Maintain relevant project instructions | Small | Agents repeat avoidable convention errors | Current rules address observed mistakes without stale/conflicting instructions |
| Strengthen typing at consequential boundaries | Medium | Escape hatches hide invalid assumptions | Known invalid cases fail; justified exceptions remain explicit |
| Enforce module boundaries | Medium | Changes introduce prohibited dependencies | A qualified checker rejects forbidden examples and accepts intended dependencies |
| Add focused local checks | Small | Detectable errors accumulate before CI | Relevant violations fail promptly; full CI remains available |
| Add templates for repeated patterns | Small | Common modules omit required contracts/checks | A generated example passes its relevant checks and needs only task-specific content |
| Add relevant security scanning | Small | Known detectable exposures pass unnoticed | Safe positive/negative controls exercise configured rules and exclusions |
| Require server-side checks | Small | Local hook bypass produces an unchecked merge | Inspected protection configuration and a controlled failure show merge enforcement |

## Compound engineering readiness

Examples: versioned plans/specs/decisions linked from agent instructions; a module/API scaffold
containing handler, contract, tests, and docs; incident-derived regression cases; maintained skills.

| Action | Effort | Failure addressed | Acceptance criterion |
|--------|--------|-------------------|----------------------|
| Turn repeated corrections into relevant guidance | Small | The same misconception returns | A later comparable task applies the correction; remove obsolete guidance |
| Package a repeated workflow as a skill | Medium | Critical steps are rediscovered inconsistently | An independent representative task follows the workflow and produces useful evidence |
| Preserve active plans and decision logs | Small | Work cannot resume accurately | Current progress, decisions and blockers are discoverable from the agent entry point |
| Version feature-scoped intent | Medium | Implementation drifts from an ephemeral request | Approved criteria are linked to relevant executed checks |
| Add a module/API scaffold where useful | Medium | Repeated changes omit the same contract | A representative scaffold includes applicable behavior, checks and documentation |
| Enforce a recurring convention with a hook | Small | A known preventable error repeats | Allowed and forbidden examples qualify the hook; unsupported cases remain explicit |
| Retain incident-derived regression cases | Small | A fixed bug returns | A comparable old implementation fails and the fix passes the new test |
| Review stale/conflicting instructions | Small | More rules make context less reliable | Affected guidance is updated when requirements/tooling change; recency alone is not adequacy |

## Collaboration effectiveness

Examples: sample the latest 10 comparable agent-assisted PRs as an initial baseline; task IDs in
PR templates; a CONTRIBUTING review rubric; linked runbooks and a representative maintenance task.

| Action | Effort | Failure addressed | Acceptance criterion |
|--------|--------|-------------------|----------------------|
| Sample comparable agent-assisted PR outcomes | Small | Workflow claims have no outcome evidence | Record sample/scope, acceptance, correction cycles and post-merge rework |
| Add task/agent metadata where useful | Small | Outcomes cannot be related to comparable work | A sampled task can be traced through review and subsequent fixes |
| Document an agent review rubric | Small | Review ignores intent or evidence limits | Review records distinguish intent, boundary and execution gaps |
| Link relevant operations runbooks | Medium | Triage assumes hidden operational knowledge | A representative incident exercise locates the response and recovery steps |
| Validate a representative maintenance task | Medium | Improved metrics conceal harder changes | Record effort, unexpected edit spread, regressions and boundary behavior for a real extension task |

## Context engineering friendliness

Examples: per-module READMEs, an architecture overview, explicit supported exports, searchable
headings, and domain names. Load `../../assess-readiness/references/context-engineering.md`
for the triage procedure before prescribing splits.

| Action | Effort | Failure addressed | Acceptance criterion |
|--------|--------|-------------------|----------------------|
| Refactor a demonstrated cohesion/navigation problem | Medium | Unrelated concerns make a change hard to understand | Representative change/navigation improves without new cycles or unnecessary coupling |
| Add module purpose and interface notes | Medium | Agents load unrelated implementation details | A task can locate the relevant API, constraints and checks |
| Clarify ambiguous file names | Small | Search returns misleading concepts | Domain queries find the intended implementation without obscuring established terms |
| Clarify public exports | Small | Consumers rely on accidental internals | Intended consumers use the supported surface; new exports do not introduce cycles |
| Document system relationships | Small | Cross-module work ignores dependency assumptions | A representative change identifies affected boundaries and evidence requirements |
| Improve searchable headings | Small | Relevant documentation is undiscoverable | Targeted searches locate the maintained guidance |
