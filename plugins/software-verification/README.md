# Software Verification Plugin

Design verification strategies that unlock higher levels of autonomous software development.

## What it does

This plugin analyzes a codebase's current verification posture and designs a tailored strategy to close gaps. It produces:

- **Verification maturity tier** (0-5) based on demonstrated, risk-matched evidence
- **Bug-surface classification** (A–E) with ceremony-risk and routing guidance
- **Component breakdown** with archetype classification and per-component maturity
- **Missing oracles** and recommended oracle types
- **Evidence scope and ledger** separating configuration, inspected execution, stale evidence, and unknowns
- **Oracle lifecycle** covering requirement adequacy, sensitivity, independence, and freshness
- **Maintainability evidence** from qualified boundary rules and representative maintenance tasks
- **Exactness analysis** (where exact correctness is possible vs. statistical/empirical)
- **Human review requirements** (which components need human oversight)
- **Autonomy candidates** (which components are ready for agent iteration)
- **Implementation roadmap** with prioritized verification improvements

## Skills

### `/assess-verification`

Assesses existing verification infrastructure and available execution evidence. Classifies components
by bug-surface (A–E), rates demonstrated maturity, and separates traceability links, execution, and
semantic review. Uninspected settings and runs stay unknown. Outputs `verification-report.md`.

### `/design-strategy`

Checks a prior report's freshness or performs lightweight discovery, then designs change-oriented,
per-component portfolios. Separates existing evidence from proposed **Evidence Requirements**, including
oracle review, scope, completion criteria, and limits. Includes **Verification Cost Tiers**
(check / verify-quick / verify-full), traceability, maintenance exercises, and a roadmap. Tool catalogs
are discovery aids; recommendations need release/scope qualification. Outputs `verification-strategy.md`.

### `/detect-ai-smells`

Assesses scoped gate evidence across **11 quality-risk categories** (plausible fabrication, shallow
error handling, vacuous tests/specs, implicit drift, and more). Distinguishes qualified, partial,
configured, absent, unknown, and inapplicable coverage; no category count establishes universal
protection or authorship. Outputs `ai-smells-gates-report.md`.

## Verification methods covered

| Category | Methods |
|----------|---------|
| Testing | Unit, integration, property-based, BDD/executable specs, fuzzing, regression replay |
| Traceability | Approved claim → check → executed evidence → reviewed decision, with gaps and review invalidation |
| Static analysis | Linters, type checkers, SAST, abstract interpretation |
| Contracts | Pre/postconditions, invariants, schemas, Design by Contract |
| Formal methods | Specifications, model checking, SMT, deductive verification, theorem proving |
| Operational | Runtime verification, shadow testing, canary deployment, chaos engineering |
| Human | Code review, approval gates, escalation |

All three reports include source revision, assessment date, inspected scope, evidence basis, and a
typed evidence ledger. A configured tool, linked test, signed report, or green sampled run must not
be presented as a stronger guarantee than its scope supports. Permission and release rules remain
separate from maturity scores. The structural report validator checks declared fields and state
consistency; it does not establish the truth or sufficiency of the evidence.

## Relationship to AI Readiness plugin

The AI Readiness plugin answers "where are we?" while this plugin answers "what verification do we need?" They work well together but can be used independently.

## Installation

Install via the Cairn plugin marketplace in your AI agent (Claude Code, Codex, or Cursor).
