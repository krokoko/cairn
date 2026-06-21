---
name: assess-verification
description: |
  Assess the current verification maturity of a codebase and identify gaps.
  Trigger phrases: "assess verification", "verification maturity",
  "how is my testing", "verification strategy assessment",
  "what is my verification coverage", "audit my tests"
argument-hint: "[path-to-codebase] (defaults to current directory)"
allowed-tools: Read Bash Glob Grep
user-invocable: true
---

# Software Verification Assessment

Assess the current verification maturity of a codebase. Produce a `verification-report.md` with maturity tier, component breakdown, missing oracles, exactness analysis, human review requirements, autonomy candidates, feedback loop completeness, workflow gate assessment, and shift-left positioning.

## Workflow

### Step 1: Inventory existing verification

Search for all verification-related artifacts:

**Testing:**
- Test files: `*_test.*`, `*_spec.*`, `test_*.*`, `tests/`, `__tests__/`
- Test config: `jest.config.*`, `pytest.ini`, `pyproject.toml [tool.pytest]`, `vitest.config.*`
- Property tests: imports of `hypothesis`, `fast-check`, `proptest`, `QuickCheck`
- Fuzzing: `fuzz/`, `*_fuzz_test.go`, `cargo-fuzz` config, `AFL` configs
- Mutation testing: `mutmut`, `stryker.conf.*`, `cargo-mutants` config

**Static analysis:**
- Linters: `.eslintrc*`, `ruff.toml`, `.golangci.yml`, `clippy.toml`
- Type checkers: `tsconfig.json`, `mypy.ini`, `pyrightconfig.json`
- SAST tools: `.semgrep/`, `codeql-config.yml`
- Sanitizers: ASan/TSan/UBSan flags in build configs or CI
- Profiling: `pprof`, `perf`, `py-spy` configurations or scripts

**Security and supply chain:**
- Dependency / SCA scanning: Dependabot (`.github/dependabot.yml`), Renovate, Snyk, `npm audit`, `pip-audit`, `osv-scanner`, `govulncheck` in CI
- Secret scanning: `gitleaks`, `detect-secrets`, `trufflehog` configs or hooks
- IaC scanning: `tfsec`, `checkov`, `kics`, `terrascan` configs or CI steps

**Contracts and schemas:**
- Schemas: `*.schema.json`, `*.proto`, `openapi.*`, `*.graphql`
- Contracts: assertions, `icontract`, `contracts` library imports, `invariant`
- Consumer-driven contracts: `pact/`, `pacts/`, Pact broker config, Spring Cloud Contract stubs
- Formal specs: `*.tla`, `*.cfg` (TLC), `*.als`, `*.dfy`

**CI and operational:**
- CI config: `.github/workflows/`, `.gitlab-ci.yml`
- Coverage: `codecov.yml`, coverage report configs
- Canary/shadow: feature flag configs, deployment configs, traffic splitting

### Step 2: Classify components

Identify distinct components or modules. For each, determine:

Load `references/decision-framework.md` for classification guidance. Load `references/method-failure-modes.md` to understand risks of current methods and gaps in assurance.

| Property | Options |
|----------|---------|
| **Archetype** | Deterministic library, CRUD/API service, Distributed/stateful, Safety/security kernel, ML-backed, Data pipeline, Infrastructure/IaC, Legacy monolith, Agent-written |
| **Criticality** | High (safety, security, money, core data), Medium (business logic), Low (UI, utilities) |
| **Determinism** | Deterministic, Concurrent/distributed, Probabilistic/learned |
| **Current verification** | List which methods are already applied |

### Step 3: Classify bug-surface

Load `references/bug-surface-routing.md`. For each component from Step 2, assign a primary bug-surface
class (A–E):

| Class | Name | Route formal/sim tools? |
|-------|------|------------------------|
| A | Local invariant | Usually no — ceremony risk |
| B | Arithmetic / conservation | Yes — property tests, checked ops, bounded proofs |
| C | Protocol / concurrency | Yes — model check, DST, schedule exploration |
| D | Untrusted input | Yes — fuzz + sanitizers |
| E | Probabilistic / learned | Operational oracles, not unit formal stack |

Record evidence (spec language, domain type, failure modes), recommended verification **depth**
(floor / standard / deep), and **ceremony risk** when maturity tier 4+ formal-method tools exist on
Class A with no gap.

Use bug-surface to calibrate maturity expectations: Class C at maturity tier 2 with no formal path is a
critical gap; Class A at maturity tier 4 with full formal stack may be over-investment.

### Step 4: Score verification maturity

Load `references/maturity-model.md` and assign a tier (0-5):

- **Tier 0**: No automated verification
- **Tier 1**: Basic tests exist, may be unreliable
- **Tier 2**: Reliable test suite with CI gating
- **Tier 3**: Generative testing + contracts/schemas
- **Tier 4**: Formal methods for critical paths + operational validation
- **Tier 5**: Evidence pipeline with replay, shadow, canary, automated promotion

Score both the overall codebase and each individual component. **Apply Step 3 bug-surface when scoring:**
Class C/D at maturity tier < 3 → note as under-instrumented in component notes; Class A at maturity
tier ≥ 4 with no identified gap → note ceremony risk. The maturity tier column and Bug-Surface section
must be consistent — do not assign tier 4 to a Class A counter without documenting why.

### Step 5: Identify missing oracles

For each component, answer: "Can we determine if the output is correct?"

Load `references/verification-taxonomy.md` for oracle types.

| Oracle type | When applicable |
|-------------|----------------|
| Exact expected output | Deterministic, well-specified inputs/outputs |
| Metamorphic relations | Output hard to predict but transformations have known effects |
| Differential oracle | Multiple implementations or versions to compare |
| Contract | API/interface must conform to a schema or protocol |
| Temporal | State transitions or event ordering must follow protocol rules |
| Statistical threshold | Stochastic outputs with bounded distributions |
| Performance envelope | Measurable load/latency/resource bounds that must hold |
| Replay/held-out data | Historical inputs with known-good outputs |
| Behavioral twin | Third-party integrations where interface mocks can't verify real behavior |
| LLM-as-Judge | Non-deterministic output where human review is too slow/costly |
| Human judgment | Ambiguous outputs requiring domain expertise |

For components with third-party integrations, specifically assess:
- Are external services verified via behavioral twins or only interface mocks?
- Are integration scenarios stored externally as holdout sets (inaccessible to agents)?
- Is verification measured as satisfaction (probabilistic) or boolean pass/fail?

Flag components with **no oracle at all** as critical gaps. Flag third-party integrations verified only via interface mocks as oracle weakness — agents can fabricate plausible API behavior that mocks will not catch.

For each oracle that exists, also rate its **strength**, not just its presence (see the "Oracle
strength" section in `references/verification-taxonomy.md`):

- **Strong**: machine-checkable, deterministic, and generalizing (property checks, contracts,
  reference/differential comparison). Scales without a human in the loop.
- **Weak**: brittle or unverified (hardcoded expected values that rot as requirements change, an
  oracle copied without checking it is itself correct, satisfaction thresholds with no ground truth).

This matters because autonomy is capped by oracle strength: a component can have an oracle and still
be unsafe for autonomous change if that oracle is weak. Flag **oracle rot** — tests that pass while
the requirement has drifted, so the oracle no longer asserts the right thing — as a distinct gap from
"no oracle"; it is more dangerous because it gives false confidence.

### Step 6: Classify correctness feasibility

For each component, determine:

- **Exact correctness possible**: Deterministic, well-specified, finite inputs — amenable to proof or exhaustive testing
- **Statistical/empirical only**: Learned, stochastic, environment-dependent — requires approximation
- **Mixed**: Core logic is deterministic (provable) but integration is non-deterministic (empirical)

### Step 7: Determine human review requirements

Components that require human review:
- No automated oracle exists
- High blast radius (affects users, data, money)
- Ambiguous requirements (underspecified intent)
- Security/compliance boundaries
- Novel code with no regression baseline

### Step 8: Identify autonomy candidates

Components where AI agents could iterate autonomously:
- Strong test coverage with reliable CI gating
- Type-checked boundaries preventing interface errors
- Property tests or contracts covering key invariants
- Low blast radius or easy rollback
- Clear, well-scoped responsibilities

### Step 9: Assess feedback loop completeness

Evaluate whether verification outputs can be consumed by agents for self-correction.

Load `references/feedback-loop-model.md` for maturity levels and assessment criteria.

Search for indicators:
- **Structured output formats**: JUnit XML generation, SARIF reports, JSON test summaries, coverage in lcov/cobertura
- **CI artifact storage**: Upload steps in CI config (actions/upload-artifact, artifacts: paths)
- **API accessibility**: GitHub Checks API usage, status check webhooks, CI notification configs
- **Agent re-execution triggers**: Workflow dispatch events, retry-on-failure configs, bot-triggered re-runs
- **Failure attribution**: Error formatters that include file paths and line numbers, PR annotations
- **Agent-accessible observability**: Local observability stack (Loki, Prometheus, Tempo, Vector), queryable logs/metrics/traces, per-worktree app isolation

For each verification method found in Step 1, classify its feedback loop level (0-3):

| Method | Output format | Routable? | Feedback loop level |
|--------|--------------|-----------|---------------------|
| ... | ... | ... | ... |

Flag methods at Level 0-1 as gaps: verification exists but agents cannot act on its results.

### Step 10: Assess workflow gate placement

Identify all human review and approval checkpoints in the development workflow:

- **PR review requirements**: Branch protection rules, CODEOWNERS, required approvals count
- **Deployment gates**: Manual approval steps in CI/CD, environment protection rules
- **Change advisory**: CAB processes, architecture review boards referenced in docs
- **Compliance gates**: Security review requirements, audit sign-offs

Branch protection rules and required-approval counts live in the hosting platform's settings, not
the working tree. Read them with `gh api` (e.g. `gh api repos/{owner}/{repo}/branches/{branch}/protection`)
when available; if `gh`/network is unavailable, mark these "not inspectable from working tree" rather
than assuming they are absent.

For each gate, evaluate:

| Gate | Risk class served | Rejection rate (if estimable) | Could agent pre-review replace? | Produces actionable feedback? |
|------|-------------------|-------------------------------|-------------------------------|-------------------------------|
| ... | ... | ... | ... | ... |

Identify:
- **Bottleneck gates**: Required human review on low-risk changes where CI is authoritative
- **Missing gates**: High-risk components with no human checkpoint
- **Duplicate gates**: Same validation done by both CI and human reviewer
- **Bypassable gates**: Local-only checks an agent can skip (`git commit --no-verify`, push without CI).
  A gate that only fires client-side is not enforceable — the authoritative gate must be server-side
  (branch protection + required status checks). Flag any check that exists only as a skippable local hook.

### Step 11: Assess shift-left positioning

Evaluate whether checks run at the earliest possible point in the development loop.

Load `references/shift-left-model.md` for the tier model and indicators.

Search for shift-left indicators:
- **Pre-commit hooks**: `.pre-commit-config.yaml`, `.husky/`, `lefthook.yml`, `.git/hooks/`
- **Post-tool-use hooks**: Agent hook configs running checks after each file write
- **Watch mode / focused tests**: `jest --watch`, `vitest`, `cargo-watch`, scripts for changed-files-only test runs
- **Editor-time checks**: LSP config, IDE settings running type checker on save

For each verification method found in Step 1, classify its current execution tier (T1-T4):

| Check | Current tier | Ideal tier | Shift-left gap? |
|-------|-------------|-----------|-----------------|
| ... | ... | ... | ... |

Flag checks that run only at T3-T4 but could run at T1-T2 (e.g., type checking only in CI, no pre-commit hooks, no focused test mode).

### Step 12: Assess documentation verification

Evaluate whether documentation stays synchronized with code through automated checks.

Load `references/documentation-verification.md` for assessment dimensions and maturity levels.

Search for indicators:
- **Auto-generation**: OpenAPI/Swagger from annotations, TypeDoc, rustdoc, Sphinx autodoc, `protoc-gen-doc`
- **Doc build in CI**: Docs site build step that fails on errors, broken refs, missing pages
- **Link validation**: `markdown-link-check`, `linkinator`, internal cross-ref checks
- **Example testing**: `doctest` (Python/Rust), tested code blocks in Markdown, `markdown-exec`
- **Schema-doc sync**: OpenAPI validated against implementation, generated client docs
- **Doc freshness**: PRs requiring doc updates alongside code changes, stale-doc detection
- **ADR/changelog enforcement**: ADR templates for architectural changes, changelog entries per PR

Classify overall documentation verification level (0-3):
- **Level 0**: Docs are manually maintained, no automated sync or validation
- **Level 1**: Some docs auto-generated (e.g., API docs from code) but no CI validation
- **Level 2**: Doc build in CI, link checking, example testing for some docs
- **Level 3**: Full sync enforcement — docs derived from code, freshness tracked, examples tested, schema-doc pipeline validated

Flag Level 0-1 as a risk: stale docs become a fabrication vector for agents relying on them for context.

### Step 13: Assess AgentOps telemetry

Evaluate whether verification outputs are observable and measurable at the operational level.

Load `references/agentops-telemetry.md` and `references/agentops-telemetry-assessment.md` for telemetry streams and assessment criteria.

Search for indicators of operational visibility into verification:

- **Trajectory telemetry**: Agent trace/logging configs, tool call tracking, session metadata
- **Cost telemetry**: CI timing visibility, token usage tracking, billing alerts or budget configs
- **Quality telemetry**: Coverage trend tracking, flake dashboards, defect rate monitoring, mutation testing reports
- **Autonomy compliance telemetry**: Audit logs, override tracking, escalation frequency logging
- **Domain telemetry**: Business-outcome instrumentation, funnel/conversion analytics, anomaly thresholds on domain KPIs — the stream that catches silent failures (green infra, broken behavior)

For each telemetry stream, classify the current level (0-3):

| Stream | Current level | Key gaps | Impact on verification improvement |
|--------|--------------|----------|-------------------------------------|
| Trajectory | ... | ... | ... |
| Cost | ... | ... | ... |
| Quality | ... | ... | ... |
| Autonomy compliance | ... | ... | ... |
| Domain | ... | ... | ... |

Flag critical gaps: verification that cannot be improved because there is no measurement of its effectiveness.

### Step 14: Assess requirement traceability

Evaluate whether intent traces to evidence: requirement → acceptance criterion → test → code → result.
**Load `references/traceability-model.md` before scoring** — it defines the 0-3 maturity levels and the
three RTM properties; do not invent your own scale.

Search for these signals:

- **Requirement anchors**: `docs/requirements/`, `docs/specs/`, EARS-style statements, structured issue templates
- **Executable acceptance criteria**: Gherkin `.feature` files and BDD step definitions (Cucumber, Behave, SpecFlow)
- **PR → issue links**: this lives in git history, not the working tree — use `git log` (e.g.
  `git log --oneline -50`) and, if available, `gh pr list`. A valid link is a closing keyword
  (`Closes #123`, `Fixes #123`), a bare `#123`/`Refs:`, or a tracker key (e.g. `PROJ-123`). Sample
  recent merges and report the fraction lacking any link rather than asserting a number you cannot compute.
  If git history or `gh` is unavailable, mark this signal "not inspectable" rather than guessing.
- **Coverage-by-requirement**: any report mapping requirements to tests (not just lines to tests)
- **Trace tooling**: Kiro, SpecKit, OpenSpec, BMAD `trace`, AI-DLC

Classify the overall level (0-3). Assess the three RTM properties (scope verification, impact analysis,
test sufficiency) and flag the failure each gap allows. Flag Level 0-1 as critical: **intent drift** is
caught only by slow, fully-human review, which cannot keep pace with agents.

### Step 15: Consolidate verification debt

Roll up every gap surfaced in Steps 4-14 (missing/weak oracles, oracle rot, feedback-loop gaps,
shift-left gaps, doc-verification gaps, telemetry blind spots, traceability gaps) into a single
ticketable backlog. This is consolidation, not new analysis — collect findings already made.

For each entry produce: component, debt type, severity, current → required state, and remediation.
One row = one liability = one fileable issue. Severity: High = high-criticality component with
no/weak oracle or a gap that lets silent regressions ship; Medium = business logic with partial
coverage; Low = utilities/cosmetic. Order the backlog by severity. Note that rows can be exported
as issues/Jira tickets with a `verification-debt` label.

### Step 16: Write the report

Load `references/report-template.md` for the output structure.

Write `verification-report.md` following the template, including all sections assessed in Steps 1-15 (maturity tier through verification debt).
