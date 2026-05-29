# AI Smells Taxonomy

AI smells are surface patterns in model-generated output suggesting content was produced for plausibility rather than understanding. They indicate **comprehension debt** — a gap between what code does and what anyone believes it does.

## The 9 AI Smells

| # | Smell | Definition | Severity | Key Indicator |
|---|-------|-----------|----------|---------------|
| 1 | **Plausible Fabrication** | Invented APIs, functions, or config options that follow real naming conventions but don't exist | High | Imports/calls referencing non-existent modules or endpoints |
| 2 | **Cargo-Cult Patterns** | Design patterns applied because they appear in similar codebases, not because the problem requires them | Medium | Single-implementation interfaces, unnecessary factories |
| 3 | **Architecture Astronaut** | Excessive abstraction disconnected from problem complexity | Medium-High | More abstraction layers than implementations; vocabulary inflation |
| 4 | **Shallow Error Handling** | Error handling that suppresses, masks, or defers failures rather than surfacing them | High | Empty catch blocks, log-and-swallow, context stripping, silent success masking (return []/null on failure), missing boundary validation |
| 5 | **Tests Mirroring Implementation** | Tests verifying what code does rather than what it should do | Medium | Mock-ordering assertions, tautological tests, implementation duplication |
| 6 | **Symmetry Without Substance** | Parallel structures that appear organized but don't illustrate meaningful differences | Low-Medium | Copy-paste handlers, boilerplate differing only in names |
| 7 | **Local Reasoning Violations** | Code requiring understanding of distant files or global state | Medium-High | Import sprawl (>5 modules), hidden singleton access, magic values |
| 8 | **Implicit Drift** | Unpinned references that silently resolve to different versions over time | Medium-High | `latest` tags, floating version ranges, model aliases, mutable external references |
| 9 | **Happy-Path-Only Coverage** | Tests and code exercise only the success scenario; error paths, edge cases, and boundaries are untested or unhandled | Medium-High | Tests assert on valid input only; no error-branch/exception tests; no empty/boundary/timeout cases; error branches with no covering test |

## The Pinning Principle

AI008 (Implicit Drift) is grounded in the observation that AI-generated code almost never pins references. Models default to `latest`, omit version suffixes on model IDs, and use floating semver ranges because training data shows both patterns equally. The harm: code works on the day it's generated but silently breaks when the reference resolves differently — with no traceable change in the repository.

A real pin has two parts:
1. **Immutable identifier** — SHA hashes, exact versions, dated model IDs, content-addressed references
2. **Deliberate update process** — Scheduled reviews, automated PRs (Dependabot/Renovate), evaluation suites

Pinning to an alias (e.g., `gpt-4` instead of `gpt-4-0613`) is not pinning.

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
- Implicit drift + shallow error handling = system silently degrades when pinned reference changes behavior
- Implicit drift + plausible fabrication = generated code references a version that never existed
- Happy-path-only coverage + shallow error handling = error paths are both unhandled and untested — guaranteed production failures
- Happy-path-only coverage + tests mirroring implementation = a green suite that proves nothing about real-world robustness

Flag files exhibiting 3+ smells simultaneously as high-priority refactoring targets.

## The Fail-Fast Principle

AI004 (Shallow Error Handling) extends beyond empty catch blocks to encompass **silent success masking** — the pattern of returning plausible-looking defaults on failure instead of surfacing the error. This includes:
- Returning empty arrays/lists when a data source errors
- Returning `null`/`undefined` that mimics "no data found"
- Substituting default values on parse failure without logging
- Catching exceptions at depth instead of validating at boundaries

The fail-fast principle requires: detect problems at the earliest point (system boundaries, startup, function entry), and surface them in a way that demands attention from the appropriate actor. AI-generated code almost never validates at startup or boundaries — it handles errors deep in call stacks where root cause is obscured.

## The Happy-Path Principle

AI009 (Happy-Path-Only Coverage) reflects a consistent agent bias: agents are strong happy-path
performers but under-handle error conditions. They generate working code for the well-scoped success
case, while the code that runs when assumptions break — invalid input, timeouts, unavailable
dependencies, empty/boundary values, unauthorized access — is thin or absent, and the tests rarely
exercise it. The danger is delayed: a suite with only happy-path tests passes every day until the
first real failure in production.

Detection signals: assertions only on valid inputs; no tests that expect a raised error/exception or
exercise an error branch; missing empty/boundary/null cases; error branches in source with no
covering test. The remedy is to name the happy path, then ask "what are all the ways this breaks?" —
turning each departure into an error to handle, an edge case to cover, or a documented failure mode.

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
| AI008 | Implicit Drift | warning |
| AI009 | Happy-Path-Only Coverage | warning |
