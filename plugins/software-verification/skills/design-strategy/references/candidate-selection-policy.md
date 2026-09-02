# Candidate Selection Policy

**Canonical statement** of the mandatory-then-objectives rule. Other references link here; do not
restate the rule or the policy schema elsewhere.

## Problem

Autonomous search often ranks candidates by a **combined score** (correctness + performance +
maintainability). This is unsafe when correctness properties are fungible with optimization metrics.

A candidate with `authorization = FAIL` and `performance = +42%` must **never** beat a candidate
with `authorization = PASS` and `performance = baseline`.

## Lexicographic selection rule

```text
if any mandatory property fails:
    candidate is ineligible

only among eligible candidates:
    optimize secondary metrics
```

## Policy schema

```yaml
verification:
  mandatory:
    build: pass
    existing_tests: pass
    no_double_charge: pass
    authorization_invariant: pass

  objectives:
    test_coverage: maximize
    latency: minimize
    complexity: minimize
    patch_size: minimize
```

### Mandatory properties

Properties that **must** pass before a candidate is eligible for promotion:

| Category | Examples | Verifier |
|----------|----------|----------|
| Build / compile | Clean build, no type errors | Compiler, type checker |
| Regression | Existing test suite | CI test job |
| Security invariants | AuthZ, no secret leak | Custom tests, SAST, policy |
| Business invariants | `balance >= 0`, conservation laws | Property tests, formal spec |
| Contract compatibility | API/schema backward compat | Contract tests, buf breaking |

Mandatory properties are **not weighted** — one failure disqualifies the candidate regardless of
objective scores.

### Objectives

Secondary metrics used to **rank eligible candidates only**:

| Objective | Typical metric | When to use |
|-----------|----------------|-------------|
| Test coverage | Line/branch coverage delta | Tie-breaking among passing candidates |
| Latency | p99, benchmark delta | Performance optimization changes |
| Complexity | Cyclomatic, LOC, dependency count | Refactors, migrations |
| Patch size | Lines changed | Minimize blast radius |
| Maintainability | Lint score, duplication | Long-term health |

Objectives may use Pareto ranking when multiple dimensions matter and no single scalar is appropriate.

## Pareto selection

When objectives conflict (faster but larger patch), keep the **non-dominated set**:

- Candidate A dominates B if A is ≥ on all objectives and > on at least one.
- Promote from the Pareto front; human or policy picks among non-dominated candidates.

Never use Pareto ranking to excuse mandatory failures.

## Integration points

| Cairn artifact | How to apply |
|----------------|--------------|
| `harness-architecture.md` promotion policy | Declare mandatory checks by risk class |
| `gate-design-patterns.md` presence⇒mandatory | Mandatory artifacts must run, not skip |
| `verifier-guided-search.md` | Search loop filters mandatory first, then optimizes |
| `generator-evaluator.md` | N-of-M consensus: compare only verifier-eligible candidates |
| CI/CD | Separate required checks (mandatory) from informational metrics (objectives) |

## Risk-class defaults

| Risk class | Mandatory floor | Typical objectives |
|------------|-----------------|-------------------|
| Low | Build + lint + unit tests | Patch size |
| Medium | Above + integration + contracts | Coverage, complexity |
| High | Above + property tests + auth invariants | Latency (if perf-sensitive) |
| Critical | Above + formal evidence on critical paths | Pareto: perf + patch size |

## Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Single `combined_score` | Split mandatory vs objectives |
| Weighted sum including correctness | Correctness is mandatory, not weighted |
| "Best effort" on security tests | Security invariants are mandatory, not objectives |
| Objective improves while mandatory regresses | Block merge; do not auto-select |
| Agent tunes objective weights | Policy is immutable; agent cannot change selection rules |

## Assessment signals

When assessing a codebase for autonomous search readiness:

- [ ] CI distinguishes required checks from informational metrics
- [ ] No single scalar "quality score" gates merge without mandatory tier
- [ ] Promotion policy documented per risk class
- [ ] Search harness (if any) filters mandatory before ranking
- [ ] Agent cannot modify mandatory check definitions in the same PR as implementation
