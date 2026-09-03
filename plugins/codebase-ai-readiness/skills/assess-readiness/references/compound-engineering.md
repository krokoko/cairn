# Compound Engineering Readiness

## Definition

Compound engineering ensures every shipped unit of work converts its lessons into
durable, agent-readable surfaces. The principle: each feature should make subsequent
features easier to build, not harder.

A codebase with strong compound engineering readiness has "landing strips" where
institutional knowledge accumulates systematically rather than evaporating between
sessions.

## Five canonical durable surfaces

| Surface | Purpose | Where to find it |
|---------|---------|------------------|
| Instruction files | Rules: "always do X" / "never do Y" | `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.cursor/rules/` |
| Skills | Packaged workflows for repeatable tasks | `.claude/skills/`, agent skill directories |
| Hooks | Deterministic gates that enforce lessons automatically | `.husky/`, `lefthook.yml`, `.pre-commit-config.yaml`, agent hook configs |
| Subagent configs | Specialized review lenses for recurring concerns | Agent team configs, specialized reviewer configs |
| Tests and evals | Executable contracts that fail if critical behaviors regress | Test suites, eval directories, benchmark configs |

## Workflow artifacts (feature-scoped context)

Durable surfaces encode repo-wide lessons; **workflow artifacts** anchor active work across
sessions (requirements, design notes, plans, review learnings). Load
`workflow-artifacts.md` for discovery paths and scoring signals. Strong compound readiness
includes both: surfaces that compound over time *and* versioned dirs where feature decisions
live in-repo—not only in chat or issue comments.

## Pass profiles

The denominator for this category is the **Compound engineering readiness** table in
`category-definitions-agent.md`. Decide PASS or FAIL per row with these profiles:

| Signal | PASS when | FAIL when |
|--------|-----------|-----------|
| Instruction file with iterative growth | >10 rules and git history shows additions after corrections | Static, generic, or absent |
| Instruction file validated | CI or a hook executes the documented commands | Commands never exercised |
| Custom skills or workflows | At least one packaged skill for a repeated task | None |
| Workflow artifacts (feature context) | Two or more artifact types with dated, feature-scoped files (see `workflow-artifacts.md`) | None, or templates only |
| Hooks enforce past corrections | A hook beyond formatting encodes a project rule | Formatting only, or none |
| Regression tests from past bugs | Tests reference issues or incidents | No traceable bug-driven tests |
| Evidence of maintenance | Hooks match current tooling; instruction file touched since the last tooling change | Broken or bypassed hooks; instruction file predates current tooling |
| Agent-authored commits | Trailers naming an agent appear in history | None |
| Collaboration measurement enablers | PR template or labels for agent-assisted work | None |

## The compounding effect

Without durable surfaces, agent productivity stays flat: the 100th task is as hard as
the first because no institutional memory accumulates. With strong compound engineering,
each correction feeds back into the system:

```
Correction → Rule in instruction file → Agent avoids mistake next time
Bug → Regression test → Agent never reintroduces the bug
Convention → Hook → Convention enforced automatically
```

## Critical companion: maintenance

Codified knowledge rots. Rules contradict, skills become stale, hooks block forgotten
requirements. Compound readiness includes evidence of maintenance:
- Instruction file touched since the last tooling change (untouched for 180+ days while tooling moved is the smell; age alone is not)
- Hooks that match current tooling (not broken or bypassed)
- Tests that still test relevant behavior (not testing removed features)

## The feedback flywheel metric

**First-pass acceptance rate** — the percentage of agent outputs accepted without
modification — indicates whether compounding is working. This metric is aspirational
(most teams don't track it explicitly), but the infrastructure to *enable* tracking
is assessable.
