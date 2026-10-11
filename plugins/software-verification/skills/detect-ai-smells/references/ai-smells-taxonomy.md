# AI Smells Taxonomy

AI smells are quality-risk signals often associated with generated output. Confirm each against
context; they do not establish authorship or prove a defect. They can indicate **comprehension debt**.

## The 11 AI Smells

| # | Smell | Definition | Severity | Key Indicator |
|---|-------|-----------|----------|---------------|
| 1 | **Plausible Fabrication** | Invented APIs, functions, or config options that follow real naming conventions but don't exist | High | Imports/calls referencing non-existent modules or endpoints |
| 2 | **Cargo-Cult Patterns** | Design patterns applied because they appear in similar codebases, not because the problem requires them | Medium | Single-implementation interfaces, unnecessary factories |
| 3 | **Architecture Astronaut** | Excessive abstraction disconnected from problem complexity | Medium-High | More abstraction layers than implementations; vocabulary inflation |
| 4 | **Shallow Error Handling** | Error handling that suppresses, masks, or defers failures rather than surfacing them | High | Empty catch blocks, log-and-swallow, context stripping, silent success masking (return []/null on failure), missing boundary validation |
| 5 | **Tests Mirroring Implementation** | Tests verifying what code does rather than what it should do | Medium | Mock-ordering assertions, tautological tests, implementation duplication, asserts on mock call counts but never on results |
| 6 | **Symmetry Without Substance** | Parallel structures that appear organized but don't illustrate meaningful differences | Low-Medium | Copy-paste handlers, boilerplate differing only in names |
| 7 | **Local Reasoning Violations** | Code requiring understanding of distant files or global state | Medium-High | Import sprawl (>5 modules), hidden singleton access, magic values |
| 8 | **Implicit Drift** | Unpinned references that silently resolve to different versions over time | Medium-High | `latest` tags, floating version ranges, model aliases, mutable external references |
| 9 | **Happy-Path-Only Coverage** | Tests and code exercise only the success scenario; error paths, edge cases, and boundaries are untested or unhandled | Medium-High | Tests assert on valid input only; no error-branch/exception tests; no empty/boundary/timeout cases; error branches with no covering test |
| 10 | **Vacuous Tests** | Tests unable to reject a relevant violation of their claimed rule | Medium-High | No meaningful assertion, tautological expectations, unreviewed snapshot replacement |
| 11 | **Vacuous Formal Specs** | Formal specs, invariants, or verification configs that constrain nothing — green gate, zero assurance | High | TLA+ invariant always true; empty scanner ruleset; `(verified=…)` marker with no linked proof; hand-written spec diverged from code with no sync gate |

## The Pinning Principle

Mutable aliases or unresolved version ranges can change behavior without a repository change.
Inspect actual resolution/lock behavior; a version range alone does not show that deployed bytes drift.

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

AI011 enforcement follows active claims and project policy. A required check that silently skips is
a gap; absent formal artifacts can be justified as inapplicable (see `ci-integration.md`).

## Compound Risk

Individual smells compound when combined:
- Cargo-cult + shallow error handling = invisible failures in unnecessary abstractions
- Architecture astronaut + local reasoning violations = code nobody can navigate
- Plausible fabrication + tests mirroring implementation = tests pass against non-existent APIs
- Implicit drift + shallow error handling = system silently degrades when pinned reference changes behavior
- Implicit drift + plausible fabrication = generated code references a version that never existed
- Happy-path-only coverage + shallow error handling = unhandled and untested failure paths
- Happy-path-only coverage + tests mirroring implementation = a green suite that proves nothing about real-world robustness
- Vacuous tests + happy-path-only coverage = high reported coverage with near-zero defect-detection power
- Vacuous formal specs + traceability markers = `(verified=kani)` theater with no proof obligation
- Vacuous gates + agent autonomy = accelerated false confidence — wrong code ships at machine speed

Flag files exhibiting 3+ smells simultaneously as high-priority refactoring targets.

## The Fail-Fast Principle

AI004 (Shallow Error Handling) extends beyond empty catch blocks to encompass **silent success masking** — the pattern of returning plausible-looking defaults on failure instead of surfacing the error. This includes:
- Returning empty arrays/lists when a data source errors
- Returning `null`/`undefined` that mimics "no data found"
- Substituting default values on parse failure without logging
- Catching exceptions at depth instead of validating at boundaries

Check errors where context is available and surface them according to the approved contract.
Fallback values can be intentional; inspect logging, recovery, and rejected-case behavior.

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

## The Vacuity Principle

AI010 (Vacuous Tests) is distinct from AI005 and AI009 along one axis: **what the test verifies**, not
which paths it covers.
- **AI005 (Tests Mirroring Implementation)** — the test asserts, but on the *implementation's mechanics*
  (mock call order, internal calls) rather than observable behavior. It can fail, but only when the
  implementation is restructured.
- **AI009 (Happy-Path-Only Coverage)** — the test asserts on real behavior, but only for the *success
  path*; error and boundary paths are unexercised.
- **AI010 (Vacuous Tests)** — the test exercises code but makes *no falsifiable assertion about its
  output*. A no-throw assertion can be meaningful for that bounded rule; inspect whether any relevant
  violation can make the test fail rather than judging only its assertion syntax.

The diagnostic question: *"Can this test ever go red if the code under test is wrong?"* If no, it is
vacuous. Relevant negative controls and mutation challenge sensitivity. Equivalent survivors and
untested/time-out cases need separate interpretation; neither mutation nor line coverage establishes
that the assertion represents current requirements.

## The Vacuous-Spec Principle

AI011 (Vacuous Formal Specs) is distinct from AI010: the **verification artifact** is present but
load-bearing properties are missing or unconstrained.
- **AI010** — tests run but assert nothing falsifiable.
- **AI011** — specs, invariants, or gate configs exist but a deliberate mutation or vacuity probe
  still passes (TLC green on flipped guard, secret scan with zero rules, coverage scoped away from core).

Diagnostic question: *"If I introduce a known violation of the stated property, does the gate fail?"*
If a relevant reachable violation passes, investigate the gate's scope, wiring, and semantics.
Anti-vacuity controls complement specification review; fingerprints detect change, not meaning.

## Interpreting findings

Report scoped findings, severity rationale, evidence, and unknowns rather than a universal score.
Counts, duplication, file length, and import depth prioritize investigation. Do not reward splitting
files or extracting shared helpers unless the resulting change improves the relevant boundary/task.
Multiple related signals can prioritize review but do not multiply a measured correctness probability.

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
| AI010 | Vacuous Tests | warning |
| AI011 | Vacuous Formal Specs | error for failed required claim; otherwise policy/scoped applicability |
