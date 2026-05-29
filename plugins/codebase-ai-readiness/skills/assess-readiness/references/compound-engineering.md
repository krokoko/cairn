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

## Scoring signals

### Strong compound readiness (score 76-100)
- Instruction file with >10 project-specific rules showing iterative growth
- Custom skills or workflows for repeated tasks (code generation, review, deployment)
- Hooks enforce conventions discovered through past mistakes
- Tests encode past bugs as regression checks
- Evidence of recent updates to instruction files (growing, not stale)
- Workflow artifact dirs present with recent feature-scoped docs (see `workflow-artifacts.md`)
- First-pass acceptance rate tracked or improvable (see `collaboration-metrics.md`)

### Moderate compound readiness (score 51-75)
- Instruction file exists with some useful rules but gaps visible
- At least one custom workflow or skill
- Some hooks, but many conventions rely on human memory
- Tests exist but don't systematically capture past incidents
- Documentation updated occasionally

### Weak compound readiness (score 26-50)
- Minimal instruction file (generic or copied from template)
- No custom skills or packaged workflows
- Pre-commit hooks present but minimal
- No versioned plans, specs, or design docs for in-flight work
- Knowledge lives in PR comments, Slack, or developer memory
- New agents start from scratch each session

### Absent compound readiness (score 0-25)
- No instruction files, no agent context
- No hooks or automation beyond basic formatter
- No evidence of institutional knowledge codification
- Each agent session rediscovers the same constraints
- Lessons learned exist only in human memory or ephemeral channels

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
- Instruction files updated within last 30 days (not stale)
- Hooks that match current tooling (not broken or bypassed)
- Tests that still test relevant behavior (not testing removed features)

## The feedback flywheel metric

**First-pass acceptance rate** — the percentage of agent outputs accepted without
modification — indicates whether compounding is working. This metric is aspirational
(most teams don't track it explicitly), but the infrastructure to *enable* tracking
is assessable.
