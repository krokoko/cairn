# Spec-First Artifacts

Spec-first means **intent is captured in machine-checkable files before or alongside code**, not
only in chat or PR descriptions. Agents default to code-first; these artifacts raise the autonomy
ceiling by giving oracles something to enforce.

Workflow order (not test-first TDD): **requirement → executable acceptance criterion → code → simulation/proof**.

## Artifact checklist

| Artifact | Where to look | Strong signal | Weak / absent |
|----------|---------------|---------------|---------------|
| **Stable requirement IDs** | `docs/requirements/`, `spec/requirements/`, `REQ-*.md` | EARS-style criteria with `id:` frontmatter | Requirements only in issues/chat |
| **Executable acceptance criteria** | Gherkin `.feature`, tagged scenarios (`@REQ-123`) | Scenario per active requirement | Prose criteria with no executable test |
| **Pure verified core** | IO-free domain crate/module separated from adapters | Core with no network/DB in same module as rules | Business logic mixed with HTTP/SQL |
| **Determinism ports** | Clock/Rng/Id injection; bans on direct `now()` / thread RNG | Testable simulation hooks | Ambient time/random in domain code |
| **Traceability links** | `implements_in`, test tags, traceability lock/report | Bidirectional REQ ↔ test ↔ code | PR-only linking |
| **Architecture decisions** | `spec/adr/`, `docs/adr/` tied to enforcement | ADR cites lint/fitness function | ADRs with no mechanical check |
| **Formal spec (when concurrent)** | `*.tla`, FSM with generated sync | Model-check in CI or verify-quick | Hand-wavy "thread-safe" comments |

## Scoring rubric (for category 2.8)

Add to Machine-readable intent score using these bands:

| Score band | Spec-first profile |
|------------|-------------------|
| **0–25** | No requirement files; no executable criteria; logic entangled with IO |
| **26–50** | Issues/README describe intent; some schemas; tests exist but untagged |
| **51–75** | Requirement IDs + some Gherkin/BDD; partial traceability; core partly separable |
| **76–100** | REQ files + scenario per requirement + traceability gate + pure core pattern (or justified exception documented in ADR) |

**Cap rule:** If category 2.8 raw signals look strong (schemas, property tests) but **no
requirement files and no executable acceptance criteria**, cap 2.8 at **60** until spec-first
artifacts exist — schemas alone do not prevent intent drift.

## Discovery commands

```bash
# Requirement files with stable IDs
find . -path './vendor' -prune -o -path './node_modules' -prune -o \
  \( -name 'REQ-*.md' -o -path '*/requirements/*.md' \) -print 2>/dev/null | head -20

# Executable acceptance (Gherkin)
find . \( -name '*.feature' \) -not -path '*/node_modules/*' 2>/dev/null | head -20

# Requirement tags in tests
grep -rn '@REQ-\|REQ-[0-9]\|traceability:' test/ tests/ spec/ 2>/dev/null | head -15

# IO-free core heuristic (language-dependent)
# Rust: crates/core or domain/ without tokio/sqlx in same crate
# TS/Python: domain/ or core/ without fetch/axios/requests imports
```

## Readiness impact

| Spec-first level | Autonomy implication |
|------------------|---------------------|
| Absent | Cap recommended level at **L3** regardless of test volume (assess-readiness skill applies this cap) |
| Partial (IDs, some BDD) | **L3** bounded iteration feasible on documented surfaces |
| Systematic (REQ + scenario + traceability) | Unlocks **L4** when verification plugin confirms oracle **strength and integrity** (non-mutable, sound oracles on critical paths) |

At **L5**, the software-verification plugin must confirm that a deterministic, server-side verifier is
authoritative, that critical-path oracles are sound and not agent-mutable, and that gates detect
oracle tampering (weakening tests or specs alongside implementation changes).

Report spec-first findings under **Machine-readable intent** and in **Blockers** when capping autonomy.
