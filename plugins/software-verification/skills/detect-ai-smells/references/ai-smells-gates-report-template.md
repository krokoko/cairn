# AI Smell Detection Gates Report Template

Write `ai-smells-gates-report.md` with this structure. Replace examples with actual findings.
Use `../../assess-verification/references/evidence-semantics.md` for ledger states. A proposed gate
is a recommendation, not inspected execution evidence; justify inapplicable categories.

```markdown
# AI Smell Detection Gates Report

## Evidence Scope

**Source revision**: [commit plus relevant working-tree changes]
**Assessment date**: [ISO date]
**Inspected scope**: [paths, categories, environments, exclusions]
**Evidence basis**: [configuration and run artifacts inspected; inaccessible settings/history]

## Evidence Ledger

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| [scoped gate claim] | [config/run and revision] | [actual environment] | configuration_only | unknown | unknown | [execution/qualification not inspected] |

## Gate Coverage Summary

**Overall coverage**: [counts of qualified/partial/configured/none/unknown/not-applicable categories]
**Enforcement level**: [observed blocking/warning/informational/unknown, with evidence]

## Coverage Matrix

| Smell | Scoped claim / gate | Coverage status | Enforcement / feedback | Evidence / limits |
|-------|---------------------|-----------------|------------------------|-------------------|
| AI001: Plausible Fabrication | ... | ... | ... | ... |
| AI002: Cargo-Cult Patterns | ... | ... | ... | ... |
| AI003: Architecture Astronaut | ... | ... | ... | ... |
| AI004: Shallow Error Handling | ... | ... | ... | ... |
| AI005: Tests Mirroring Implementation | ... | ... | ... | ... |
| AI006: Symmetry Without Substance | ... | ... | ... | ... |
| AI007: Local Reasoning Violations | ... | ... | ... | ... |
| AI008: Implicit Drift | ... | ... | ... | ... |
| AI009: Happy-Path-Only Coverage | ... | ... | ... | ... |
| AI010: Vacuous Tests | ... | ... | ... | ... |
| AI011: Vacuous Formal Specs | ... | ... | ... | ... |

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
1. [Proposed gate, failure addressed, qualification controls, scope/limits, completion evidence]

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
