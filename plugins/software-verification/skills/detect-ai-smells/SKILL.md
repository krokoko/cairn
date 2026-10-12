---
name: detect-ai-smells
description: |
  Assess whether a codebase has gates to detect AI-generated code smells and recommend what to add.
  Trigger phrases: "detect ai smells", "check for ai slop gates", "ai code quality gates",
  "do I have ai smell detection", "ai hygiene checks",
  "what checks catch ai slop", "ai quality gates assessment"
  Optional argument: [path-to-codebase] (defaults to current directory)
allowed-tools: Read Bash Glob Grep
---

# Assess AI Smell Detection Gates

Assess gates for 11 quality-risk categories often associated with generated code; these signals do
not establish who wrote it. Produce `ai-smells-gates-report.md` with scoped gate evidence, gaps,
recommendations, and review heuristics. Configuration presence does not establish detection.

## Workflow

### Step 1: Load smell taxonomy

Load `references/ai-smells-taxonomy.md` for the 11 AI smell categories and their detection approaches.
Load `../assess-verification/references/evidence-semantics.md` and
`../assess-verification/references/oracle-lifecycle.md` for evidence states and oracle limits.

These are the categories of AI-generated quality problems the codebase should be protected against:
1. Plausible Fabrication
2. Cargo-Cult Patterns
3. Architecture Astronaut
4. Shallow Error Handling (including silent success masking and missing boundary validation)
5. Tests Mirroring Implementation
6. Symmetry Without Substance
7. Local Reasoning Violations (including hard-coded magic values)
8. Implicit Drift (unpinned references that silently resolve differently over time)
9. Happy-Path-Only Coverage (success path tested; error/edge/boundary paths unexercised)
10. Vacuous Tests (tests that execute code but verify nothing falsifiable)
11. Vacuous Formal Specs (formal specs, invariants, or gate configs that constrain nothing)

### Step 2: Inventory existing gates

Search for mechanisms that would catch AI smells:

**Static analysis rules:**
- Custom semgrep rules: `.semgrep/`, `semgrep.yml`, semgrep configs in CI
- Custom lint rules: eslint plugins, ruff extensions, custom clippy lints
- Complexity checkers: cognitive complexity limits, import depth limits
- Architecture enforcement: dependency-cruiser, ArchUnit, import-linter (deptry checks package hygiene)

**CI quality gates:**
- Branch coverage to locate unexercised decisions; coverage alone does not measure assertion quality
- Mutation testing: `stryker`, `mutmut`, `cargo-mutants` (sensitivity to selected changes; inspect survivors)
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

For each relevant gate, record configuration, supported source scope, current run artifacts, tool
version, and enforcement evidence separately. Unavailable branch settings or CI history remain
unknown. Inspect existing allowed/violating controls where available; do not silently run expensive
or externally mutating campaigns as part of an assessment.
Read-only assessment can use supplied CI exports, retained runner reports, control results, and
review records after checking revision and scope. Without those artifacts, report Configured or
Unknown as appropriate and name the evidence needed; do not run campaigns just to obtain a label.

### Step 3: Map gates to smell categories

Load `references/detection-patterns.md`, `references/detection-patterns-gates.md`, and
`references/detection-patterns-gates-formal.md` for what patterns each gate should catch.
Apply `references/coverage-decisions.md` for repeatable per-smell scope and Partial decisions.

For each category, state the bounded behavior a gate claims to detect and the evidence inspected:

| Smell / scoped claim | Gate | Coverage status | Evidence / limits |
|----------------------|------|-----------------|-------------------|
| AI001–AI011, each separately | Existing mechanism or none found | Qualified / Partial / Configured / None / Unknown / Not applicable | Artifact, run, and remaining scope |

Coverage status describes the declared scope, never complete protection from a smell category:
- **Qualified**: Current completed run plus relevant allowed/violating controls support the claim.
- **Partial**: Inspected evidence supports some of the scope; material gaps remain.
- **Configured**: Relevant configuration exists but execution/sensitivity is not established.
- **None**: No relevant gate found in the inspected scope.
- **Unknown**: Access or evidence is insufficient to assess.
- **Not applicable**: The failure surface is absent, with an explicit justification.

Define the category's applicable scope before assigning status. A qualified check for one subcase
does not qualify the whole category: use Partial when executed evidence leaves material applicable
subcases uncovered, and identify the narrower qualified check in Evidence / limits. With configuration
alone, use Configured and describe the known coverage gaps separately.

For AI001, code and mocks can share invented behavior. Seek independent schema/provider or consumer
evidence. A twin is an approximation requiring fidelity/version qualification; it is not a mandatory
tool or proof of deployed compatibility. Held-out cases reduce direct exposure, not all gaming.

For AI004, inspect empty catches, silent defaults, error propagation, and relevant startup/boundary
validation. Defaults can be intended behavior; use the approved error contract and negative examples.

For AI008, distinguish reproducible resolution from deliberate updates. Record actual resolved
versions and update evidence; absence of a particular dependency bot is not absence of a sound process.

For AI009, investigate important unexercised branches and rejected/boundary cases. Assertion-name
searches are heuristics: errors may be returned as values or checked through shared helpers.
Line coverage alone does not establish that the relevant outcomes are asserted.

For AI010, assertion lint, known-bad controls, old-versus-fixed regression demonstrations, and mutation
can challenge sensitivity. Surviving mutants may be equivalent or outside the claim. `not throws`
can be a valid bounded requirement; classify it as vacuous only when it cannot reject a relevant defect.
Neither mutation nor fresh execution establishes that expected outcomes reflect current intent.

For AI011, a formal file or verified marker is configuration evidence only. Inspect completion,
bounds, checked obligations, model/code correspondence, and relevant anti-vacuity probes. Verify
scanner defaults before treating an empty local override as an empty effective ruleset. Required
checks should fail visibly when unwired; document examples and intentionally inactive artifacts.
Load `../design-strategy/references/gate-design-patterns.md` for scoped gate qualification.

### Step 4: Assess gate maturity

Load `references/ci-integration.md` for pipeline positioning and fitness function patterns.

For each existing gate, evaluate:
- **Where it runs**: Pre-commit / CI / PR review / manual
- **Enforcement level**: Blocking (fails build) / Warning (annotation) / Informational (report only)
- **Feedback quality**: Does it produce actionable output for agents? (file, line, fix suggestion)
- **Trend visibility**: Is there historical tracking of gate findings?
- **Qualification and freshness**: Were allowed/violating examples exercised on the relevant version?
- **Semantic review**: Does the asserted rule still match the requirement, independently of execution?

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

Load `references/ai-smells-gates-report-template.md`. Populate all sections, including Evidence Scope
and Evidence Ledger. Use the exact shared state enums; positive conclusions require `run_inspected`
and `completed`, with the method's limitations. Separate proposed gates from existing evidence;
justify inapplicability and retain unknowns. Do not infer general correctness from category counts.
