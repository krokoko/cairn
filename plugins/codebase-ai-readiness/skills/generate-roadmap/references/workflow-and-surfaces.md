# Workflow Artifacts and Durable Surfaces (Dual Track)

When **compound engineering readiness** or **progressive context disclosure** scores below
the target level, improvements need two parallel tracks—not only stronger CI or types.

## Track A: Durable surfaces (repo-wide)

Mechanisms that apply to every agent session:

- Instruction files with growing project-specific rules
- Pre-commit and CI gates (types, lint, boundaries, security)
- Custom agent skills for repo-specific repeated tasks
- Regression tests for bugs found during agent work
- Hooks that enforce conventions discovered in review

Load `improvement-actions-agent.md` for concrete actions.

## Track B: Workflow artifacts (feature-scoped)

Versioned context that survives session boundaries for active work:

- Requirements or spec docs before large features (`docs/requirements/` or team convention)
- Design notes or ADRs before cross-cutting changes
- Execution plans with progress/decision logs (`docs/plans/`, `docs/exec-plans/`)
- Review learnings merged back into rules, tests, or plan docs

Load `../../assess-readiness/references/workflow-artifacts.md` for discovery patterns.

## Critical path ordering

When both tracks are weak, prioritize in this order:

1. **Fast feedback** — CI + types + pre-commit (unblocks safe iteration)
2. **Entry point** — `AGENTS.md` / `CLAUDE.md` linking to workflow dirs and rules
3. **First workflow artifact dir** — e.g. `docs/plans/` with template for active work
4. **First packaged skill** — one repeatable workflow (review, small feature, or deploy check)
5. **Flywheel** — after each agent correction, update rules or tests; log in plan/review doc

## Roadmap section

If the readiness report shows workflow artifacts absent or compound engineering below 51,
add a roadmap subsection **## Session infrastructure (dual track)** with paired actions from
Track A and Track B. Do not recommend only CI fixes without artifact or skill steps.
