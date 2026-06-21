# Codebase AI Readiness Plugin

Assess how AI-friendly a codebase is and produce an autonomy maturity map.

## What it does

This plugin reviews an existing codebase and evaluates it across 15 categories that determine how safely and effectively AI agents can operate. It produces:

- **Overall score** (0-100)
- **Category breakdown** with per-category scores
- **Recommended autonomy level** (L0-L5)
- **Collaboration effectiveness** with optional **alignment note** when agent practices and codebase score diverge
- **Blockers** preventing advancement to the next level
- **Prioritized roadmap** of improvement actions

## Skills

### `/assess-readiness`

Performs a full assessment of the codebase. Examines structure, documentation, tests, CI (including test impact analysis), typing, setup, architecture decisions, machine-readable intent (schemas, contracts, executable acceptance criteria, requirement traceability), progressive context disclosure, workflow artifacts, collaboration effectiveness metrics, hidden state, repository-scale reasoning, failure mode legibility, and feedforward surfaces (including non-bypassable hooks). Outputs `readiness-report.md` with an alignment note when practices and score diverge.

### `/generate-roadmap`

Takes an existing readiness report and generates a detailed improvement plan to reach the next autonomy level (or a specified target). Outputs `readiness-roadmap.md` with an **L2 → L3 hinge** section when the plan crosses that boundary (current ≤ L2, target ≥ L3).

## Categories assessed

| Category | What it measures |
|----------|-----------------|
| Structure and modularity | Directory organization, module boundaries, naming, architectural isolation |
| Documentation | README, API docs, ADRs, changelogs |
| Testable boundaries | Test coverage, isolation, fixtures |
| CI reliability | Pipeline existence, check count, flakiness |
| Typing strength | Annotations, strict mode, escape hatches |
| Deterministic environment and deployment | Containers, reproducible envs, seed data, Infrastructure as Code |
| Architecture decisions | ADRs, design docs, ownership |
| Machine-readable intent | Schemas, contracts, property tests, specs |
| Progressive context disclosure | Agent context files, layered docs, cross-linking |
| Hidden state and magic | Env var docs, config schemas, explicit defaults |
| Repository-scale reasoning | Naming consistency, predictable patterns |
| Failure mode legibility | Error handling, structured errors, fail-fast |
| Feedforward surfaces | Instruction files, strict types, boundary linters, non-bypassable pre-commit hooks |
| Compound engineering readiness | Iterative instruction growth, custom skills, workflow artifacts, regression-from-bugs |
| Context engineering friendliness | File size distribution, layered docs, retrieval-friendly naming |

## Installation

Install via the Cairn plugin marketplace in your AI agent (Claude Code, Codex, or Cursor).
