# Scoring Rubric

## Category weights

| Category | Weight | Rationale |
|----------|--------|-----------|
| Structure and modularity | 0.12 | Agents need clear boundaries to scope changes |
| Documentation | 0.08 | Context for understanding intent |
| Testable boundaries | 0.15 | Tests are the primary verification mechanism |
| CI reliability | 0.12 | Unreliable CI blocks autonomous iteration |
| Typing strength | 0.08 | Types prevent entire bug classes cheaply |
| Deterministic environment and deployment | 0.08 | Agents need reproducible environments and codified deployment |
| Architecture decisions | 0.05 | Helps agents understand constraints |
| Machine-readable intent | 0.12 | Enables automated verification of correctness |
| Progressive context disclosure | 0.05 | Agents discover context through layered docs |
| Hidden state and magic | 0.05 | Implicit state causes agent failures |
| Repository-scale reasoning | 0.05 | Consistent naming enables retrieval and reasoning |
| Failure mode legibility | 0.05 | Legible errors enable agent self-correction |

## Scoring tiers

### 0-25: Absent or minimal

- No evidence of the category, or only trivial/accidental presence
- Example (testing): No test files, or only a single placeholder test

### 26-50: Basic, inconsistent

- Some evidence exists but coverage is patchy or inconsistent
- Example (testing): Some test files exist but cover <30% of modules, no CI integration

### 51-75: Good, mostly consistent

- Systematic effort is visible with minor gaps
- Example (testing): Most modules have tests, CI runs them, but coverage is uneven

### 76-100: Excellent, systematic

- Comprehensive, consistent, enforced by tooling or policy
- Example (testing): High coverage, property tests for key invariants, required CI checks

## Score calculation

```
overall_score = sum(category_score[i] * weight[i]) for i in categories
```

Round to nearest integer. Range: 0-100.
