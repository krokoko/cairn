# Scoring Rubric

## Category weights

| Category | Weight | Rationale |
|----------|--------|-----------|
| Structure and modularity | 0.10 | Agents need clear boundaries to scope changes |
| Documentation | 0.06 | Context for understanding intent |
| Testable boundaries | 0.13 | Tests are the primary verification mechanism |
| CI reliability | 0.10 | Unreliable CI blocks autonomous iteration |
| Typing strength | 0.07 | Types prevent entire bug classes cheaply |
| Deterministic environment and deployment | 0.07 | Agents need reproducible environments and codified deployment |
| Architecture decisions | 0.04 | Helps agents understand constraints |
| Machine-readable intent | 0.10 | Enables automated verification of correctness |
| Progressive context disclosure | 0.04 | Agents discover context through layered docs |
| Hidden state and magic | 0.04 | Implicit state causes agent failures |
| Repository-scale reasoning | 0.04 | Consistent naming enables retrieval and reasoning |
| Failure mode legibility | 0.04 | Legible errors enable agent self-correction |
| Feedforward surfaces | 0.09 | Prevents errors proactively; reduces agent iteration count |
| Compound engineering readiness | 0.04 | Enables knowledge accumulation across sessions |
| Context engineering friendliness | 0.04 | Codebase structure supports effective context management |

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
