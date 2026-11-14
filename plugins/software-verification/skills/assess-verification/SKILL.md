---
name: assess-verification
description: |
  Assess the current verification maturity of a codebase and identify gaps.
  Trigger phrases: "assess verification", "verification maturity",
  "how is my testing", "verification strategy assessment",
  "what is my verification coverage", "audit my tests"
  Optional argument: [path-to-codebase] (defaults to current directory)
allowed-tools: Read Bash Glob Grep
---

# Software Verification Assessment

Assess the current verification maturity of a codebase. Produce a `verification-report.md` with maturity tier, component breakdown, missing oracles, exactness analysis, human review requirements, autonomy candidates, feedback loop completeness, workflow gate assessment, and shift-left positioning.

## Workflow

### Step 1: Inventory existing verification

Load `references/evidence-semantics.md`. Record source revision (including relevant dirty changes),
assessment date, inspected scope, and evidence basis. Distinguish configured capabilities from
inspected runs in an Evidence Ledger; use the reference's exact status vocabulary. Existing reports
may be reused only after checking their revision, environment, and affected scope. Record unavailable
CI history or hosting settings as unknown; do not infer successful execution from configuration.
Read-only assessment can use supplied run/review/settings artifacts; load `references/maturity-model.md` for access limits and evidence needed beyond configuration.

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
(floor / standard / deep), and **ceremony risk** when expensive methods address no identified gap.
For Class C, inspect schedule/fault exploration and model/environment assumptions; missing relevant
evidence is the gap, rather than absence of a named formal tool.

### Step 4: Score verification maturity

Load `references/maturity-model.md` and assign a tier (0-5):

- **Tier 0**: No automated verification
- **Tier 1**: Configured checks; operation or reliability unconfirmed
- **Tier 2**: Reliable, enforced checks with inspected execution evidence
- **Tier 3**: Risk-matched claims and complementary checks
- **Tier 4**: Qualified oracles, check sensitivity, and environment fidelity
- **Tier 5**: Managed evidence, decision policies, and continuing improvement

Assign each component the highest demonstrated tier under the reference's criteria, with unknowns
and limiting evidence. Configuration alone supports Tier 1; inaccessible scope may be `unknown`.
The overall tier must hold across in-scope critical paths, not average away their gaps. Record
justified inapplicability; a simple component can reach an advanced tier without formal methods.
Keep configured/recommended targets separate from demonstrated maturity.
Cross-check component tiers, bug surfaces, and oracles: Tier 3+ requires evidence addressing important
applicable failures, including Class C schedules/faults and Class D rejected inputs. A qualified simple
Class A component may reach a high tier; flag ceremony only for costly checks with no identified need.

### Step 5: Identify missing oracles

For each component, answer: "Can we determine if the output is correct?"

Load `references/verification-taxonomy.md` for oracle types and `references/oracle-lifecycle.md`
for adequacy, sensitivity, independence, and freshness.

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

For third-party integrations, inspect actual-service evidence, twin/mock fidelity, version
assumptions, supported scenarios, and holdout access/feedback controls. Neither a local twin nor
an interface mock establishes provider behavior without fidelity evidence. Holdouts reduce direct
exposure but repeated feedback can leak cases.

For each consequential oracle, record `supported`, `gap`, or `unknown` for the four lifecycle
dimensions. Identify the approved claim and requirement/assertion/fixture/helper revisions covered
by semantic review. Changed inputs make that review stale until the relationship is reviewed.
Check independent expected values, known-good/known-bad controls, relevant mutations, and incident
regressions. Investigate equivalent or out-of-scope mutants before attributing survivors to weak tests.

Report strength as qualified / weak / unknown / none for the bounded claim, with evidence.
Flag **oracle rot** separately from missing or execution-stale oracles: a fresh passing run can
assert an obsolete rule. Mutation challenges sensitivity; it does not approve current intent.
Prioritize missing/weak oracles by criticality and affected claims.
A claim with no oracle has a critical verification gap: correct and incorrect behavior cannot be
distinguished. Record it, retain review, and prioritize by consequence; not every such component is high risk.

### Step 6: Classify correctness feasibility

For each component, determine:

- **Exact within scope feasible**: A declared property is amenable to proof or exhaustive analysis under explicit assumptions
- **Statistical/empirical**: The available environment/claim requires representative samples and stated uncertainty
- **Mixed**: Some claims admit proof/exhaustion while integration or outcome claims require empirical evidence

Feasibility is not completed evidence. Name properties, bounds, supported semantics, and remaining
assumptions; a deterministic component does not imply every correctness claim is provable in practice.

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

Make recommendations per changed surface, using inspected oracle/evidence quality, blast radius,
and recovery. Unknown evidence limits the recommendation. A maturity tier is not an autonomy level
or permission to act; show the remaining claim/environment gaps for each candidate.

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
when available, or inspect a dated, scoped settings export. Otherwise record `not_inspectable`
observation and `unknown` execution/conclusion in the ledger; explain the access limit.

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

Treat coverage, complexity, hotspots, and pass rates as diagnostic signals. Tie a proposed improvement
to a concrete rule or representative change outcome; a metric increase alone does not establish
maintainability or oracle adequacy.

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

Evaluate the chain from approved requirement to bounded claim, scenario/property, executed check,
versioned evidence, and reviewed decision, including source/code mappings.
**Load `references/traceability-model.md` before scoring** — it defines the 0-3 maturity levels and the
three completeness dimensions; do not invent your own scale.

Search for these signals:

- **Requirement anchors**: `docs/requirements/`, `docs/specs/`, EARS-style statements, structured issue templates
- **Check mappings**: Requirement tags in ordinary tests, reviewed contracts/properties, or Gherkin scenarios
- **PR → issue links**: this lives in git history, not the working tree — use `git log` (e.g.
  `git log --oneline -50`) and, if available, `gh pr list`. A valid link is a closing keyword
  (`Closes #123`, `Fixes #123`), a bare `#123`/`Refs:`, or a tracker key (e.g. `PROJ-123`). Sample
  recent merges and report the fraction lacking any link rather than asserting a number you cannot compute.
  If history or `gh` is unavailable, record `not_inspectable` observation and `unknown` execution/conclusion.
- **Execution completeness**: expected checks joined to runner results for the assessed source/environment;
  fresh run directories, skipped/missing/interrupted results, and partial claims remain visible
- **Review freshness**: requirement/assertion/fixture/helper revisions covered by semantic review
- **Trace tooling**: existing structured records/scripts or tools from the traceability reference

Classify the overall level (0-3 or unknown). Report link, execution, and semantic completeness
separately, alongside scope verification, impact analysis, and test-sufficiency gaps. An ID parser
checks links; semantic sufficiency requires review even when links resolve. Prioritize by consequence
and the intended operating scope.

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
Include Evidence Scope and Evidence Ledger. Positive ledger conclusions require `run_inspected` and
`completed`; semantic approval remains separate. Explain unknowns and how they limit recommendations.
