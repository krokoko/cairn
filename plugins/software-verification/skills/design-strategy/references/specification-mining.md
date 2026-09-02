# Specification Mining (Brownfield)

## Problem

Brownfield systems often have code, tests, and production traces — but no explicit invariants.
Characterization tests and replay help, but do not discover **new** properties to verify.

Specification mining infers candidate properties from observed behavior.

## Workflow

```text
production traces
       +
existing tests
       +
code behavior
       │
       ▼
 invariant mining
       │
       ▼
candidate properties
       │
       ▼
human / requirement validation
       │
       ▼
approved oracle
```

## Tools

| Tool | Input | Output |
|------|-------|--------|
| Daikon | Runtime traces + instrumented executions | Likely invariants (`x <= y`, `size >= 0`) |
| Trace analysis | Production/staging logs | Temporal patterns, ordering constraints |
| Diff testing | Old vs new on trace replay | Regression properties |
| LLM-assisted extraction | Code + tests + docs | Candidate properties (human-reviewed) |

Daikon remains actively maintained; use for bootstrapping Tier 1–2 codebases toward Tier 3–4.

## Cairn principle

**A mined invariant is a hypothesis, not a specification.**

Without human validation against requirements, mining may formalize existing bugs. Mined properties
must pass through:

1. **Human review** — does this match intent?
2. **Requirement linkage** — assign REQ-ID or reject
3. **Promotion** — add to property tests / formal spec with `authority: approved-spec`
4. **Integrity card** — see `oracle-integrity.md`; mined starts as `degraded`

## When to recommend

| Signal | Recommend mining |
|--------|------------------|
| Legacy monolith archetype, few explicit invariants | Yes |
| Tier 1–2 maturity, rich production traces | Yes |
| Refactor planned, no characterization net | Yes — before refactor |
| Greenfield with clear spec | No — write spec first |
| Safety-critical kernel | Only as supplement to written spec |

## Integration with other methods

| Stage | Method |
|-------|--------|
| Freeze behavior | Approval/characterization tests (`../../assess-verification/references/verification-taxonomy.md`) |
| Discover properties | Daikon / trace mining (this document) |
| Validate | Human + requirement traceability |
| Enforce | Property tests, contracts, formal spec |
| Prevent regression | CI + mutation testing |
| Agent search | Promoted properties become mandatory in `candidate-selection-policy.md` |

## Anti-patterns

| Anti-pattern | Risk |
|--------------|------|
| Auto-promote mined invariants to CI | Formalizes bugs |
| Mine only from failing traces | Biased sample |
| Skip human review for "obvious" invariants | Obvious ≠ correct |
| Agent approves its own mined properties | Integrity failure |
| Mining replaces written requirements | No authority chain |

## Assessment signals

- [ ] Production trace capture exists (sanitized)
- [ ] Mining tool or manual property extraction attempted
- [ ] Review queue for candidate properties
- [ ] Promoted properties linked to requirements
- [ ] Mined properties marked distinct from approved spec in reports
