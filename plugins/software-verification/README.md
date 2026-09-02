# Software Verification Plugin

Design verification **architecture** that unlocks higher levels of autonomous software development.

Cairn is a **Verification Architect / Router** — it diagnoses, prescribes, and hardens. It does not
execute verifiers (Dafny, Quint, Kani, etc.); complementary harnesses implement the prescribed
architecture.

## What it does

This plugin analyzes a codebase's verification posture and designs evidence architecture for safe
agent search and change:

- **Verification maturity tier** (0-5) with spec continuity and oracle integrity signals
- **Bug-surface classification** (A–E) with Class C subroutes (C1–C4)
- **Change semantics** (feature, refactor, migration, etc.) — orthogonal to bug surface; applied in `/design-strategy`
- **Oracle integrity** (sound / degraded / blocked) — anti-evaluator-gaming for L4/L5
- **Verifier-guided search** patterns — deterministic verifier as authority, not LLM arbitration
- **Mandatory vs objectives** candidate selection — correctness before optimization
- **Component breakdown** with 10 archetypes including agentic applications
- **Implementation roadmap** with prioritized verification improvements

## Skills

### `/assess-verification`

Full assessment: inventories verification artifacts, classifies components, scores maturity,
assesses oracle strength **and integrity**, verifier-guided search prerequisites, traceability, and
verification debt. Outputs `verification-report.md`.

### `/design-strategy`

Per-component verification strategies: tools, oracles, evidence pipeline, verifier-guided search,
candidate selection policy, change semantics, safe evolution, specification mining. Outputs `verification-strategy.md`.

### `/detect-ai-smells`

Maps gates to **12 AI smell categories** including AI012 Oracle Tampering / Evaluator Gaming.
Outputs `ai-smells-gates-report.md`.

## Key concepts

| Concept | Reference |
|---------|-----------|
| Verifier-guided search | `design-strategy/references/verifier-guided-search.md` |
| Oracle integrity | `design-strategy/references/oracle-integrity.md` |
| Change semantics | `design-strategy/references/change-semantics.md` |
| Candidate selection | `design-strategy/references/candidate-selection-policy.md` |
| Class C1–C4 routing | `assess-verification/references/bug-surface-routing.md` |
| Assurance evidence schema | `schemas/verification-evidence.schema.json` |
| Routing fixtures | `tests/routing-fixtures/fixtures/` at repo root — expectations only; layout/schema checked by `mise run test:fixtures`, routing accuracy is a manual eval |

## Verification methods covered

| Category | Methods |
|----------|---------|
| Testing | Unit, integration, property-based, BDD, fuzzing, regression replay, model↔impl conformance |
| Search | Verifier-guided search, best-of-N, counterexample-guided refinement |
| Traceability | Requirement → criterion → test → code mapping (RTM) |
| Static analysis | Linters, type checkers, SAST, symbolic (CrossHair), agent guardrails (Skylos) |
| Formal methods | TLA+, P, Quint, model checking, SMT, DST (Turmoil/MadSim), translation validation (Alive2) |
| Operational | Runtime spec conformance (PObserve), shadow, canary, chaos, Jepsen history |
| Brownfield | Specification mining (Daikon), characterization tests |
| Human | Code review, approval gates, escalation |

## Relationship to AI Readiness plugin

The AI Readiness plugin answers "where are we?" while this plugin answers "what verification
architecture lets an agent search, change, and prove software safely?" They work together but can
be used independently.

## Installation

Install via the Cairn plugin marketplace in your AI agent (Claude Code, Codex, or Cursor).
