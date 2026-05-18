# Codebase AI Readiness Plugin

Assess how AI-friendly a codebase is and produce an autonomy maturity map.

## What it does

This plugin reviews an existing codebase and evaluates it across 12 categories that determine how safely and effectively AI agents can operate. It produces:

- **Overall score** (0-100)
- **Category breakdown** with per-category scores
- **Recommended autonomy level** (L0-L5)
- **Blockers** preventing advancement to the next level
- **Prioritized roadmap** of improvement actions

## Skills

### `/assess-readiness`

Performs a full assessment of the codebase. Examines structure, documentation, tests, CI, typing, setup, architecture decisions, machine-readable intent, progressive context disclosure, hidden state, repository-scale reasoning, and failure mode legibility. Outputs `readiness-report.md`.

### `/generate-roadmap`

Takes an existing readiness report and generates a detailed improvement plan to reach the next autonomy level (or a specified target). Outputs `readiness-roadmap.md`.

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

## Installation

Install via the autonomy-rails plugin marketplace in your AI agent (Claude Code, Codex, or Cursor).
