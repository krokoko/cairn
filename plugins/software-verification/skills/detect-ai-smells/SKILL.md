---
name: detect-ai-smells
description: |
  Assess whether a codebase has gates to detect AI-generated code smells and recommend what to add.
  Trigger phrases: "detect ai smells", "check for ai slop gates", "ai code quality gates",
  "do I have ai smell detection", "ai hygiene checks",
  "what checks catch ai slop", "ai quality gates assessment"
argument-hint: "[path-to-codebase] (defaults to current directory)"
allowed-tools: Read Bash Glob Grep
user-invocable: true
---

# Assess AI Smell Detection Gates

Assess whether a codebase has gates in place to catch AI-generated code smells — patterns indicating output was produced for plausibility rather than understanding. Produce an `ai-smells-gates-report.md` with coverage of the 9 AI smell categories, gap analysis, recommendations for missing gates, and human review heuristics for what automation can't catch.

## Workflow

### Step 1: Load smell taxonomy

Load `references/ai-smells-taxonomy.md` for the 9 AI smell categories and their detection approaches.

These are the categories of AI-generated quality problems the codebase should be protected against:
1. Plausible Fabrication
2. Cargo-Cult Patterns
3. Architecture Astronaut
4. Shallow Error Handling (including silent success masking and missing boundary validation)
5. Tests Mirroring Implementation
6. Symmetry Without Substance
7. Local Reasoning Violations (including hard-coded magic values)
8. Implicit Drift (unpinned references that silently resolve differently over time)

### Step 2: Inventory existing gates

Search for mechanisms that would catch AI smells:

**Static analysis rules:**
- Custom semgrep rules: `.semgrep/`, `semgrep.yml`, semgrep configs in CI
- Custom lint rules: eslint plugins, ruff extensions, custom clippy lints
- Complexity checkers: cognitive complexity limits, import depth limits
- Architecture enforcement: dependency-cruiser, ArchUnit, deptry, import-linter

**CI quality gates:**
- Test coverage thresholds that would catch "tests mirroring implementation" (mutation testing is stronger signal)
- Mutation testing: `stryker`, `mutmut`, `cargo-mutants` (catches AI005 — tests mirroring implementation)
- Dead code detection: `knip`, `ts-prune`, `vulture` (catches AI002/AI003 — unnecessary abstractions)
- Duplication detection: `jscpd`, `cpd`, `dupfinder` (catches AI006 — symmetry without substance)

**Dependency/import validation:**
- Import boundary enforcement: eslint-plugin-boundaries, dependency-cruiser rules
- Unused dependency detection: `depcheck`, `deptry`
- Package existence validation in lockfiles

**Error handling checks:**
- Linter rules for empty catch blocks (eslint no-empty, ruff B001/E722)
- Custom rules requiring error context propagation
- Silent success masking detection (catch blocks returning [], null, {}, or default values)
- Startup/boundary validation enforcement (config validated at init, not lazily)

**Pinning and drift prevention:**
- Lockfile enforcement (`npm ci`, `pip install --require-hashes`)
- Docker base image pinning (hadolint, Dockerfile lint)
- GitHub Action SHA pinning (`actionlint`, `pin-github-action`)
- Version range restrictions (no `^`/`~`/`*` beyond patch)
- Automated update mechanisms (Dependabot, Renovate)
- Model ID version pinning (for AI-using codebases)

**Hard-coded value detection:**
- Magic number linting (eslint `no-magic-numbers`, ruff `PLR2004`)
- Repeated string literal detection
- Config scatter patterns (same value in multiple files)

**Commit/PR hygiene:**
- Commit message linting: `commitlint`, `gitlint`, conventional commits config
- PR template enforcement: `.github/PULL_REQUEST_TEMPLATE.md`
- PR size limits or warnings
- Required test file changes with source changes

**Review gates:**
- CODEOWNERS requiring review for high-risk paths
- Required approvals gating on diff size
- Bot checks that flag PRs without descriptions or tests

### Step 3: Map gates to smell categories

Load `references/detection-patterns.md` and `references/detection-patterns-gates.md` for what patterns each gate should catch.

For each of the 9 AI smells, determine which existing gates provide coverage:

| Smell | Covered by | Coverage level |
|-------|-----------|----------------|
| AI001: Plausible Fabrication | [existing gates or "None"] | Full / Partial / None |
| AI002: Cargo-Cult Patterns | ... | ... |
| AI003: Architecture Astronaut | ... | ... |
| AI004: Shallow Error Handling | ... | ... |
| AI005: Tests Mirroring Implementation | ... | ... |
| AI006: Symmetry Without Substance | ... | ... |
| AI007: Local Reasoning Violations | ... | ... |
| AI008: Implicit Drift | ... | ... |
| AI009: Happy-Path-Only Coverage | ... | ... |

Coverage levels:
- **Full**: Automated gate would block or warn on this smell category
- **Partial**: Some indicators caught but significant gaps remain
- **None**: No automated mechanism exists for this category

For AI001 (Plausible Fabrication) specifically: note that interface mocks alone do NOT protect against fabrication — an agent writing both code and mocks creates a closed loop of plausibility. Behavioral twins or contract tests against real API behavior are required for full coverage. If only interface mocks exist for third-party integrations, classify as "Partial" at best.

For AI004 (Shallow Error Handling): assess both traditional empty-catch detection AND silent success masking. If only empty-catch rules exist but no detection of `catch { return [] }` / `catch { return null }` patterns, classify as "Partial". Full coverage requires startup validation enforcement and boundary validation checks.

For AI008 (Implicit Drift): check for both the pin itself AND an automated update mechanism. Lockfile enforcement without Dependabot/Renovate is "Partial" — it prevents drift but accumulates staleness. Full coverage requires pinning + deliberate update process.

For AI009 (Happy-Path-Only Coverage): line coverage alone does NOT count — a suite can hit every line via success-case tests while never exercising an error branch. Require branch coverage or mutation testing plus the presence of error-path tests (`assertRaises`/`toThrow`/`pytest.raises`). Line coverage only, with no error-path assertions, is "Partial" at best.

### Step 4: Assess gate maturity

Load `references/ci-integration.md` for pipeline positioning and fitness function patterns.

For each existing gate, evaluate:
- **Where it runs**: Pre-commit / CI / PR review / manual
- **Enforcement level**: Blocking (fails build) / Warning (annotation) / Informational (report only)
- **Feedback quality**: Does it produce actionable output for agents? (file, line, fix suggestion)
- **Trend visibility**: Is there historical tracking of gate findings?

### Step 5: Assess git history hygiene gates

Load `references/git-history-signals.md` for vibe-coding signal patterns.

Check for mechanisms that enforce commit/PR quality:
- Commit message format enforcement (commitlint, gitlint)
- PR description requirements (templates, bot checks)
- PR-to-issue linking enforcement (GitHub branch protection, bot checks requiring `Closes #`, `Fixes #`)
- PR size warnings or limits
- Required test additions with source changes
- Review requirements scaled to diff size

### Step 6: Assess human review readiness

Check for mechanisms that support taste-based quality judgment:
- Review checklists or guidelines mentioning AI-generated code
- PR review templates with quality heuristic questions
- CONTRIBUTING.md or review guides with proportionality/clarity criteria
- ADRs (Architecture Decision Records) that capture "why" for reviewers
- Style guides that go beyond formatting to address design intent

If no human review heuristics exist, the report should recommend establishing them — these smells (proportionality, coherence, clarity, appropriateness) cannot be fully automated but can be systematized through review culture.

### Step 7: Write the report

Load `references/ai-smells-gates-report-template.md` and write `ai-smells-gates-report.md` following that structure. Populate all sections with findings from Steps 1–6.
