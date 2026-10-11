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

## Verdicts for category 2.8

The **Machine-readable intent** rows in `category-definitions.md` are the denominator. Each
artifact above maps to a row: the **Strong signal** column is the PASS profile, the
**Weak / absent** column is FAIL.

**Cap rule:** if the computed 2.8 score exceeds 60 while both **Stable requirement IDs** and
**Executable acceptance criteria** are FAIL, cap 2.8 at 60 — schemas and property tests alone do
not prevent intent drift. Note the cap in the category's Notes cell.

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
| Systematic (REQ + scenario + traceability) | Unlocks **L4** when verification plugin confirms oracle strength |

Report spec-first findings under **Machine-readable intent** and in **Blockers** when capping autonomy.
