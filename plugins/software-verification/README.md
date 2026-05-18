# Software Verification Plugin

Design verification strategies that unlock higher levels of autonomous software development.

## What it does

This plugin analyzes a codebase's current verification posture and designs a tailored strategy to close gaps. It produces:

- **Verification maturity tier** (0-5)
- **Component breakdown** with archetype classification and per-component maturity
- **Missing oracles** and recommended oracle types
- **Exactness analysis** (where exact correctness is possible vs. statistical/empirical)
- **Human review requirements** (which components need human oversight)
- **Autonomy candidates** (which components are ready for agent iteration)
- **Implementation roadmap** with prioritized verification improvements

## Skills

### `/assess-verification`

Performs a full assessment of existing verification infrastructure. Inventories tests, linters, type checkers, contracts, schemas, formal specs, CI, and operational validation. Classifies components and scores maturity. Outputs `verification-report.md`.

### `/design-strategy`

Takes an existing verification report (or performs lightweight discovery) and designs per-component verification strategies. Recommends tools, oracle patterns, evidence pipeline design, and an implementation roadmap. Outputs `verification-strategy.md`.

## Verification methods covered

| Category | Methods |
|----------|---------|
| Testing | Unit, integration, property-based, fuzzing, regression replay |
| Static analysis | Linters, type checkers, SAST, abstract interpretation |
| Contracts | Pre/postconditions, invariants, schemas, Design by Contract |
| Formal methods | Specifications, model checking, SMT, deductive verification, theorem proving |
| Operational | Runtime verification, shadow testing, canary deployment, chaos engineering |
| Human | Code review, approval gates, escalation |

## Relationship to AI Readiness plugin

The AI Readiness plugin answers "where are we?" while this plugin answers "what verification do we need?" They work well together but can be used independently.

## Installation

Install via the autonomy-rails plugin marketplace in your AI agent (Claude Code, Codex, or Cursor).
