# Shift-Left Verification Model

## Principle

The earlier a defect is caught, the cheaper it is to fix. In agent workflows, errors
compound across steps — a mistake in one file leads to compensating workarounds in
subsequent files. Detecting issues immediately after each step prevents cascading cost.

## Execution tiers

| Tier | Timing | Latency | What belongs here |
|------|--------|---------|-------------------|
| T1: Per-file/per-write | After every file modification | Milliseconds | Type checkers, formatters, linters |
| T2: Per-step/per-module | After a logical unit of work | Seconds | Focused unit tests for modified modules, schema validation |
| T3: Per-PR/task boundary | Before merge or after full task | Minutes | Full test suite, integration tests, SAST, LLM review |
| T4: Per-deploy | Before or during deployment | Minutes-hours | System tests, canary, shadow, runtime verification |

## Assessment: where checks currently run

For each verification method found in the codebase, classify its current tier:

| Check type | Ideal tier | Common misplacement |
|------------|-----------|---------------------|
| Type checking | T1 (per-file) | Often T3 (only in CI) |
| Linting/formatting | T1 (per-file) | Often T3 (only in CI) |
| Schema validation | T2 (per-step) | Often T3 (only in CI) |
| Unit tests (focused) | T2 (per-step) | Often T3 (full suite in CI) |
| Secret scanning | T1 (pre-commit) | Often T3 (CI) or T4 (too late) |
| Dependency vulnerability | T3 (per-PR) | Often T4 (deploy/periodic) |
| Integration tests | T3 (per-PR) | Appropriate placement |
| System/E2E tests | T3-T4 | Appropriate placement |
| Canary/shadow | T4 (per-deploy) | Appropriate placement |

## Indicators of shifted-left checks

| Signal | Where to find |
|--------|---------------|
| Pre-commit hooks | `.pre-commit-config.yaml`, `.husky/`, `lefthook.yml`, `.git/hooks/` |
| Editor-time checks | IDE config running tsc/eslint on save, LSP config |
| Post-tool-use hooks | Agent hooks running checks after each file write |
| Focused test run scripts | Scripts to run only tests related to changed files |
| Test impact analysis | pytest-testmon, Jest `--onlyChanged`, Drill4J, Launchable — run only tests affected by a change |
| Watch mode configs | `jest --watch`, `vitest`, `cargo-watch`, `pytest-watch` |

## Indicators of late-only checks

| Signal | Meaning |
|--------|---------|
| Type checking only in CI workflow | Agent writes many files before finding type errors |
| Linting only in CI workflow | Style violations accumulate until PR submission |
| No pre-commit hooks | Nothing catches issues before commit |
| Full test suite only (no focused mode) | Seconds-fast feedback unavailable; must wait minutes |
| Secret scanning only at deploy | Secrets may be committed and pushed before detection |

## Test-selection soundness caveat

Two different mechanisms hide behind "run only affected tests", with different correctness guarantees:

- **Git-diff selection** (Jest `--onlyChanged`, `--changedSince`): runs tests in/importing changed
  files. Fast but **unsound** — a test in an unchanged file that exercises the changed code is skipped.
- **Coverage/dependency-graph TIA** (pytest-testmon, Drill4J, Launchable): maps each test to the code
  it covers and selects by that graph. More accurate, but only as current as its coverage map.

Use affected-only selection for the fast inner loop (T1-T2), but keep a **full suite at the PR/CI gate
(T3)** as the authoritative check. Do not recommend git-diff selection as the sole merge gate.

## Cost tiers (wall-clock routing)

Execution tiers (T1–T4) answer **when in the lifecycle** a check runs. **Cost tiers** answer **how
often** expensive checks run within implementation. Both dimensions matter for agent loops.

| Cost tier | When | Target latency | Typical contents |
|-----------|------|----------------|----------------|
| **Check** | Every save / post-write hook | Seconds | fmt, lint, types, meta-gates (traceability, spec sync), secret scan |
| **Verify-quick** | After logical unit / before commit | ~1–3 min | Unit + property tests, coverage floor, quick model-check/DST seed |
| **Verify-full** | Pre-merge, release, or nightly | Minutes+ | Mutation, fuzz, multi-seed simulation, TSAN, Loom, full integration |

### Mapping cost tier × execution tier

| Cost tier | Ideal execution tier | Common mistake |
|-----------|---------------------|----------------|
| Check | T1 (per-file/post-write) | Only in CI (T3) — agent writes many files before feedback |
| Verify-quick | T2–T3 (per-module / pre-commit) | Bundled into verify-full — too slow to run often |
| Verify-full | T3–T4 (CI required or nightly) | Run on every save — blocks agent iteration |

### Routing by bug-surface

Do not run verify-full on every component. Load `bug-surface-routing.md`:

- **Class A** (local invariant): Check + verify-quick usually sufficient
- **Class B** (arithmetic/conservation): verify-quick + bounded proofs; verify-full mutation
- **Class C** (protocol/concurrency): verify-quick TLC/DST seed; verify-full multi-seed + sanitizers
- **Class D** (untrusted input): verify-full fuzz campaigns
- **Class E** (probabilistic): operational checks at T4, not verify-full unit stack

Load `../../design-strategy/references/verification-cost-tiers.md` for per-component tier design in
strategy reports.
