# Spec-First Artifacts

Spec-first means **reviewed intent is versioned and linked to executable checks before or
alongside code**. Accept requirement documents, annotated tests, contracts or equivalent
repository records. The notation and file extension do not establish meaning or execution.

Trace the workflow: **reviewed requirement → executable criterion → implementation → relevant
execution evidence → reviewed decision**. Simulation/proof is selected when the risk warrants it.

## Artifact checklist

| Artifact | Where to look | Strong signal | Weak / absent |
|----------|---------------|---------------|---------------|
| **Stable requirement records** | Requirement docs, test annotations, reviewed contracts | Approved claims with stable IDs/revisions and check mappings | Intent exists only in ephemeral discussion |
| **Executable acceptance criteria** | Ordinary tests, contracts, Gherkin with step definitions | Relevant assertions and completed evidence for critical claims | Declared criteria with no inspected execution |
| **Separable core** | IO-free domain crate/module separated from adapters | Rules can be checked independently of external IO | Business logic mixed with HTTP/SQL |
| **Determinism ports** | Clock/Rng/Id injection; bans on direct `now()` / thread RNG | Testable simulation hooks | Ambient time/random in domain code |
| **Traceability** | Requirement tags, mappings, runner reports, review records | Links, completed execution and reviewed meaning are separately evidenced | IDs resolve but execution or semantic review is unknown |
| **Architecture decisions** | `spec/adr/`, `docs/adr/` tied to enforcement | ADR cites lint/fitness function | ADRs with no mechanical check |
| **Protocol model (where risk warrants it)** | `*.tla`, state-machine models | Completed exploration with declared bounds and implementation correspondence | Concurrency claims lack relevant evidence |

## Scoring rubric (for category 2.8)

Add to Machine-readable intent score using these bands:

| Score band | Spec-first profile |
|------------|-------------------|
| **0–25** | No versioned intent or executable criteria; logic entangled with IO |
| **26–50** | Issues/README describe intent; some schemas; tests exist but untagged |
| **51–75** | Reviewed claims + linked executable criteria; partial run/meaning evidence; core partly separable |
| **76–100** | Critical claims mapped to relevant, completed checks; current assertion review; traceability gate; separable core or justified architecture |

**Cap rule:** Strong schemas/property tests without reviewed requirement records and linked
executable criteria cap 2.8 at **60**. Missing reviewed executable intent also caps autonomy
at L3 under `autonomy-prerequisites.md`. Uninspectable evidence stays unknown.

## Traceability and semantic freshness

Sample the chain: approved claim → bounded property/scenario → executed check → versioned
evidence → reviewed decision. Separate link completeness, execution completeness and meaning.
Skipped, missing, interrupted and stale reports remain gaps even when all IDs resolve.
Runner-native results and an expected check inventory help establish execution.

Review the requirement/assertion relationship when either changes, including fixtures and
expectation helpers. Rerunning refreshes execution evidence, not semantic approval.
Independent expected values and known-bad controls challenge the oracle; mutation measures
sensitivity to selected changes, not whether the current business rule is correct.

## Discovery commands

```bash
# Requirement files with stable IDs
find . -path './vendor' -prune -o -path './node_modules' -prune -o \
  \( -name 'REQ-*.md' -o -path '*/requirements/*.md' \) -print 2>/dev/null | head -20

# One optional representation: Gherkin (inspect step definitions and run reports too)
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
| Partial (reviewed claims, some linked checks) | Supports investigating **L3** bounded iteration on documented surfaces |
| Systematic (claims + execution + semantic review) | Supports **L4** only when scoped oracle evidence and the remaining gates justify it |

Report spec-first findings under **Machine-readable intent** and in **Blockers** when capping autonomy.
