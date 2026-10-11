# Codebase AI Readiness Plugin

Assess how AI-friendly a codebase is and produce an autonomy maturity map.

## What it does

This plugin reviews an existing codebase across 15 diagnostic categories and distinguishes
configured capabilities from inspected execution evidence. It produces:

- **Provisional score** (0-100 when evidence permits), with assessed weight and explicit unknowns
- **Category breakdown** with evidence-backed findings
- **Evidence scope and ledger** recording revision, environment, execution state and supported conclusions
- **Per-surface autonomy recommendations** (L0-L5), bounded by two L4 scope prerequisites and five L5 gates
- **Collaboration effectiveness** with optional **alignment note** when agent practices and codebase score diverge
- **Blockers** preventing advancement to the next level
- **Prioritized roadmap** with failures addressed and observable acceptance criteria

An assessment recommends an operating scope; it does not grant merge, deployment or tool
permissions. A high aggregate score cannot offset missing evidence on a critical path.
L4 requires `L4-INTENT` (reviewed executable intent) and `L4-ORACLES` (current adequate critical-path
evidence). L5 additionally requires complete intent/oracle coverage, representative environments,
silent-failure detection, and recovery. Read-only assessment can inspect supplied run/review/settings
artifacts; unavailable evidence remains unknown and limits the demonstrated recommendation.

## Skills

### `/assess-readiness`

Examines structure, documentation, tests, CI, typing, setup, reviewed executable intent,
traceability, context and collaboration. Outputs `readiness-report.md` with scope, evidence
ledger, surface ceilings and prerequisite status. Unavailable evidence stays unknown; linked
or declared tests do not count as inspected execution. Maintainability signals are interpreted
alongside concrete boundary rules and representative change outcomes when available.

### `/generate-roadmap`

Checks a prior report's revision, scope and freshness before planning improvements for a
target surface. Outputs `readiness-roadmap.md` with Evidence Scope and an **L2 → L3 hinge**
section when the plan crosses that boundary (current ≤ L2, target ≥ L3). Stale or missing
evidence becomes an action to resolve; plans do not count as completed verification.

## Categories assessed

| Category | What it measures |
|----------|-----------------|
| Structure and modularity | Directory organization, module boundaries, naming, architectural isolation |
| Documentation | README, API docs, ADRs, changelogs |
| Testable boundaries | Relevant assertions, isolation, fixtures and oracle controls |
| CI reliability | Expected/completed checks, enforcement, missing results and flakiness |
| Typing strength | Annotations, strict mode, escape hatches |
| Deterministic environment and deployment | Containers, reproducible envs, seed data, Infrastructure as Code |
| Architecture decisions | ADRs, design docs, ownership |
| Machine-readable intent | Schemas, contracts, property tests, specs |
| Progressive context disclosure | Agent context files, layered docs, cross-linking |
| Hidden state and magic | Env var docs, config schemas, explicit defaults |
| Repository-scale reasoning | Naming consistency, predictable patterns |
| Failure mode legibility | Error handling, structured errors, fail-fast |
| Feedforward surfaces | Instruction files, strict types, boundary linters, non-bypassable pre-commit hooks |
| Compound engineering readiness | Maintained lessons, custom skills, workflow artifacts, incident regressions |
| Context engineering friendliness | Cohesion, navigation, layered docs and contextual size signals |

## Installation

Install via the Cairn plugin marketplace in your AI agent (Claude Code, Codex, or Cursor).
