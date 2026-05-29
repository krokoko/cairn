# AI Smell Detection Gates Report Template

Write `ai-smells-gates-report.md` with the following structure:

```markdown
# AI Smell Detection Gates Report

## Gate Coverage Summary

**Overall coverage**: X/9 smell categories with at least partial automated detection
**Enforcement level**: [Blocking / Warning / None] for detected smells

## Coverage Matrix

| Smell | Gate exists? | Tool/mechanism | Enforcement | Feedback quality |
|-------|-------------|----------------|-------------|------------------|
| AI001: Plausible Fabrication | ... | ... | ... | ... |
| AI002: Cargo-Cult Patterns | ... | ... | ... | ... |
| AI003: Architecture Astronaut | ... | ... | ... | ... |
| AI004: Shallow Error Handling | ... | ... | ... | ... |
| AI005: Tests Mirroring Implementation | ... | ... | ... | ... |
| AI006: Symmetry Without Substance | ... | ... | ... | ... |
| AI007: Local Reasoning Violations | ... | ... | ... | ... |
| AI008: Implicit Drift | ... | ... | ... | ... |
| AI009: Happy-Path-Only Coverage | ... | ... | ... | ... |

## Git History Hygiene

| Signal | Gate exists? | Mechanism | Enforcement |
|--------|-------------|-----------|-------------|
| Commit message quality | ... | ... | ... |
| PR descriptions | ... | ... | ... |
| PR-to-issue linking | ... | ... | ... |
| Test coverage with changes | ... | ... | ... |
| PR size awareness | ... | ... | ... |

## Gap Analysis

### Unprotected smell categories
- [List smells with no coverage and their risk]

### Weak enforcement
- [List gates that exist but only as warnings or reports]

### Missing fitness functions
- [List where trend tracking would help]

## Recommendations

### Quick wins (add to existing CI)
1. ...

### New gates to introduce
1. ...

### Strengthen existing gates
1. ...

## Human Review Heuristics

### Proportionality
- Does this solution's complexity match the problem's complexity?

### Coherence
- Does this code feel like it belongs in this codebase?

### Clarity
- Do names communicate intent, not just structure?

### Appropriateness
- Is this the right solution for this team's maintenance capacity?
```
