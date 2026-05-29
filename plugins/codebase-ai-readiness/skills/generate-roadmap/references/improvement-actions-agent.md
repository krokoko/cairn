# Improvement Actions (Agent Surfaces)

Continues `improvement-actions.md`. Actions for failure legibility, feedforward, compound engineering, and context engineering.

## Failure mode legibility

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Audit and remove swallowed exceptions | Medium | +15-20 | No empty catch/except blocks |
| Add structured error types or codes | Medium | +10-15 | Error classes, not just strings |
| Write agent-targeted remediation in lint/CI error messages | Small | +10-15 | Errors tell agents what to fix, not just what failed |

## Feedforward surfaces

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Create instruction file (CLAUDE.md/AGENTS.md) with 10+ project rules | Small | +20-30 | Single highest-impact feedforward action for agents |
| Enable strict type checking and reduce escape hatches | Medium | +15-20 | tsconfig strict, mypy strict, eliminate `any`/`type: ignore` |
| Add module boundary linter to prevent unauthorized imports | Medium | +15-20 | eslint-plugin-boundaries, deptry, madge, ArchUnit |
| Add pre-commit hooks running type checker + linter per-file | Small | +15-20 | Catches errors before they compound |
| Add file/component templates for common patterns | Small | +10-15 | plop, hygen, or simple template files |
| Add security scanner to pre-commit (Semgrep, bandit, gitleaks) | Small | +10-15 | Prevents security issues proactively |
| Make hooks non-bypassable (deny `--no-verify`, require server-side CI checks) | Small | +10-15 | Agents route around blockers; branch protection is the non-negotiable gate |

## Compound engineering readiness

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Start instruction file and commit to adding rules after each correction | Small | +15-25 | Begin the feedback flywheel |
| Create first custom skill for a repeated workflow | Medium | +10-15 | Package a task agents perform repeatedly |
| Add `docs/plans/` (or team convention) with plan + decision log template | Small | +10-20 | Session context; pair with CI/types (dual track) |
| Add `docs/requirements/` or `docs/specs/` for feature-scoped specs before large changes | Medium | +10-15 | Design-first anchor; link from AGENTS.md |
| Add hooks that enforce recently-discovered conventions | Small | +10-15 | Convert corrections into automated enforcement |
| Add regression tests for each bug found during agent work | Small | +10-15 | Prevents re-introduction; compounds over time |
| Schedule monthly instruction file review for stale/conflicting rules | Small | +5-10 | Maintenance prevents rot |

## Collaboration effectiveness

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Sample last 10 agent-assisted PRs; estimate first-pass acceptance | Small | — | Baseline; no tooling required |
| Add PR template field for agent-assisted / task id | Small | +5-10 | Enables later metric automation |
| Document agent review checklist in CONTRIBUTING or AGENTS.md | Small | +10-15 | Reduces iteration cycles |
| After each major agent correction, add one rule or regression test | Small | +15-25 | Closes feedback flywheel |
| Set team target: first-pass acceptance ≥50% on L3 bounded tasks | Small | — | Governance for L4 transition |

## Context engineering friendliness

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Split files >500 lines into focused, single-responsibility modules | Medium | +15-25 | Largest impact on agent comprehension |
| Add per-module READMEs with purpose and API summary | Medium | +10-15 | Enables progressive context loading |
| Rename generic files (utils, helpers, common) to domain-specific names | Small | +10-15 | Improves search and retrieval |
| Add explicit module exports (barrel files, `__init__.py`) | Small | +10-15 | Clear public API surface |
| Add ARCHITECTURE.md with system-level structure | Small | +10-15 | Entry point for understanding module relationships |
| Standardize documentation headings for searchability | Small | +5-10 | Structured headings enable targeted retrieval |
