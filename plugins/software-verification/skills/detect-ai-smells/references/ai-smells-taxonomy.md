# AI Smells Taxonomy

AI smells are surface patterns in model-generated output suggesting content was produced for plausibility rather than understanding. They indicate **comprehension debt** — a gap between what code does and what anyone believes it does.

## The 7 AI Smells

| # | Smell | Definition | Severity | Key Indicator |
|---|-------|-----------|----------|---------------|
| 1 | **Plausible Fabrication** | Invented APIs, functions, or config options that follow real naming conventions but don't exist | High | Imports/calls referencing non-existent modules or endpoints |
| 2 | **Cargo-Cult Patterns** | Design patterns applied because they appear in similar codebases, not because the problem requires them | Medium | Single-implementation interfaces, unnecessary factories |
| 3 | **Architecture Astronaut** | Excessive abstraction disconnected from problem complexity | Medium-High | More abstraction layers than implementations; vocabulary inflation |
| 4 | **Shallow Error Handling** | Generic try/catch blocks that suppress rather than handle errors | High | Empty catch blocks, log-and-swallow, context stripping |
| 5 | **Tests Mirroring Implementation** | Tests verifying what code does rather than what it should do | Medium | Mock-ordering assertions, tautological tests, implementation duplication |
| 6 | **Symmetry Without Substance** | Parallel structures that appear organized but don't illustrate meaningful differences | Low-Medium | Copy-paste handlers, boilerplate differing only in names |
| 7 | **Local Reasoning Violations** | Code requiring understanding of distant files or global state | Medium-High | Import sprawl (>5 modules), hidden singleton access, magic values |

## Severity and CI Actions

| Level | Meaning | CI Action |
|-------|---------|-----------|
| **High** | Runtime failure, masked bugs, or blocked comprehension | Fail build / block merge |
| **Medium** | Increased maintenance cost, compounds over time | Warn in PR, track trend |
| **Low** | Cosmetic or minor; acceptable if isolated | Informational only |

## Compound Risk

Individual smells compound when combined:
- Cargo-cult + shallow error handling = invisible failures in unnecessary abstractions
- Architecture astronaut + local reasoning violations = code nobody can navigate
- Plausible fabrication + tests mirroring implementation = tests pass against non-existent APIs

Flag files exhibiting 3+ smells simultaneously as high-priority refactoring targets.

## Scoring Formula

```
smell_score = (high_findings × 3 + medium_findings × 2 + low_findings × 1) / total_files_scanned
```

Normalized 0-100:
- **0-10**: Clean — minimal AI smell
- **11-30**: Mild — some patterns, mostly cosmetic
- **31-60**: Moderate — structural smells affecting maintainability
- **61-100**: Severe — significant plausibility-over-understanding patterns

Compound multiplier: 2 smells in same file = ×1.5, 3+ smells = ×2.0.

## Rule ID Registry

| ID | Smell | SARIF Level |
|----|-------|-------------|
| AI001 | Plausible Fabrication | error |
| AI002 | Cargo-Cult Patterns | warning |
| AI003 | Architecture Astronaut | warning |
| AI004 | Shallow Error Handling | error |
| AI005 | Tests Mirroring Implementation | warning |
| AI006 | Symmetry Without Substance | note |
| AI007 | Local Reasoning Violations | warning |
