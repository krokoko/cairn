# Workflow Artifacts (Session Context)

## Definition

**Workflow artifacts** are versioned, in-repo documents that anchor a feature or change across
agent sessions: requirements, design decisions, implementation plans, and review learnings.
They complement durable surfaces (rules, hooks, tests) by preserving *what we decided for this
work*, not only *how the repo generally works*.

Pattern-agnostic locations to search (any subset counts):

| Artifact type | Typical paths | What "good" looks like |
|---------------|---------------|------------------------|
| Requirements / specs | `docs/requirements/`, `docs/specs/`, `requirements/`, `specs/` | Structured feature or epic docs linked to work |
| Design / blueprints | `docs/design/`, `docs/architecture/features/`, `design/` | Component or interaction design before large code changes |
| Execution plans | `docs/plans/`, `docs/exec-plans/`, `PLANS.md`, `.agents/plans/` | Active plan + progress or decision log for in-flight work |
| Review / retro notes | `docs/reviews/`, `docs/learnings/`, notes under plan dirs | Captured review findings that update rules or tests |
| ADRs tied to features | `docs/adr/`, `adr/` with recent entries referencing features | Decisions co-located with the change they govern |

Also check progressive-context signals: cross-links from README or `AGENTS.md` to these dirs.

## Verdict contribution

Workflow artifacts feed two table rows: **Workflow artifacts (feature context)** under compound
engineering readiness and **Plans as versioned artifacts** under progressive context disclosure.

| Row | PASS when | FAIL when |
|-----|-----------|-----------|
| Workflow artifacts (feature context) | Two or more artifact types with dated, feature-scoped files, cross-linked from agent entry docs | Templates only, or context lives in issues and chat |
| Plans as versioned artifacts | An active or recently completed plan lives in-repo | No versioned plans |

## Discovery commands

Use Glob for: `docs/{requirements,specs,design,plans,exec-plans,reviews,learnings}/**/*`
`requirements/**/*`, `specs/**/*`, `design/**/*`, `**/PLANS.md`, `docs/adr/**/*.md`.

Use Grep in `AGENTS.md` / `CLAUDE.md` for links to plan, spec, or requirements paths.

## Report notes

In the readiness report **Workflow artifacts** subsection, list: directories found, approximate
file count, recency if visible from git or dates, and which artifact types are missing.
