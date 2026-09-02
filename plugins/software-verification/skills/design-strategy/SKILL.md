---
name: design-strategy
description: |
  Design a verification strategy for specific components to unlock more autonomy.
  Trigger phrases: "design verification strategy", "what verification do I need",
  "verification plan", "how to verify this component",
  "unlock autonomy for this module", "what tests should I add"
argument-hint: "[component-name-or-path] (defaults to full codebase)"
allowed-tools: Read Bash Glob Grep
user-invocable: true
---

# Design Verification Strategy

Design a tailored verification strategy for specific components or the full codebase. Produces a `verification-strategy.md` with per-component recommendations, oracle strategies, evidence pipeline design, and an implementation roadmap.

## Workflow

### Step 1: Load prior assessment

Search for `verification-report.md` in the codebase. If it exists, read the component breakdown, maturity tier, and identified gaps.

If no report exists, perform a lightweight discovery:
- Identify main components/modules from directory structure
- Check for existing tests, CI, type checking
- Classify each component by archetype and criticality

### Step 2: Scope target components

- If the user specified a component path or name, focus on that component.
- Otherwise, prioritize components by: (1) high criticality with low verification, (2) autonomy candidates that need one more layer, (3) components with missing oracles.

### Step 3: Apply decision framework

Load `references/hybrid-strategies.md` for archetype-to-stack mappings.
Load `references/toolchain-catalog.md` and `references/toolchain-catalog-ecosystems.md` for ecosystem-specific tool recommendations.

For each target component:

1. **Identify archetype**: Deterministic lib, CRUD service, distributed/stateful, safety kernel, ML-backed, data pipeline, infrastructure/IaC, legacy monolith, agent-written, agentic application/workflow
2. **Identify change mode**: Load `references/change-semantics.md` — feature, bug fix, refactor, migration, perf optimization, etc. When the strategy is not scoped to a change, record `N/A` and skip change-mode routing
3. **Look up recommended stack**: From the hybrid strategies reference
4. **Diff current vs recommended**: What already exists? What is missing?
5. **Produce specific recommendations**:
   - Which tools/libraries to add
   - Which files to create or modify
   - Estimated effort (small/medium/large)
   - Expected impact on verification maturity

### Step 4: Design oracle strategy

Load `references/oracle-patterns.md` and `references/oracle-integrity.md`.

For each component, recommend the best oracle type:

| Component type | Recommended oracle approach |
|---------------|----------------------------|
| Pure functions | Exact expected output + property-based |
| User-facing behavior | Executable acceptance criteria (Gherkin/BDD) linked to requirements |
| API endpoints | Schema validation + contract tests |
| Data pipelines | Metamorphic relations + replay |
| ML models | Differential + statistical + human |
| State machines | Model checking + replay |
| UI components | Snapshot + visual regression + human |

For each recommendation, specify:
- The oracle type and integrity requirements (`agent_mutable: false` for L5)
- How to implement it (specific library, pattern, or technique)
- What properties or relations to check
- How to handle cases where no oracle exists yet

### Step 5: Design architecture fitness functions

Load `references/fitness-functions.md` and `references/fitness-functions-implementation.md` for types, tools, and maturity levels.

For each target component, identify architectural invariants that should be automated:

1. **Dependency constraints**: Which module boundaries must be enforced? What unauthorized imports would indicate drift?
2. **API surface checks**: Are there public interfaces that must remain backward-compatible?
3. **Performance budgets**: Are there latency, size, or resource thresholds that must hold?
4. **Structural rules**: Are there organizational invariants (file-to-test mapping, naming, export limits)?
5. **Security invariants**: Are there security properties that must always hold (auth, input validation, no secrets)?

For each recommended fitness function, specify:
- The property being protected
- The tool to implement it
- Where it runs, matched to execution cost: fast checks (seconds) at pre-commit/per-commit; slow checks (minutes — full Lighthouse, large benchmarks, deep scans) in nightly/scheduled builds so the agent's fast loop stays fast
- The error message format (actionable for agents)
- Current maturity level and target level

Calibrate deliberately (see "Calibration and execution cost" in the implementation reference): start permissive and tighten on observed violations; fitness functions enforce decisions already made, they do not replace architectural judgment.

### Step 6: Design evidence pipeline

Load `references/harness-architecture.md` for the five-lane model, interface schemas, and harness metrics.

Recommend how verification evidence should flow through CI/CD:

**Per risk level:**
- **Low risk** (utilities, internal tools): Unit tests pass, linter clean, types check
- **Medium risk** (business logic, APIs): Above + integration tests + coverage threshold
- **High risk** (payments, auth, data): Above + property tests + contract checks + human approval
- **Critical** (safety, security): Above + formal verification evidence + shadow validation

**Promotion policies:**
- What checks must pass before merge
- What checks must pass before deploy
- When to require human approval
- Rollback triggers and thresholds
- For high/critical risk, require a signed evidence attestation (in-toto/SLSA via Sigstore/Cosign or GitHub artifact attestations) as the evidence rail — it records what ran on which commit with what verdict, not output correctness

Check rail coverage (see `references/harness-architecture.md`): the stack should have one pre-merge rail, one boundary rail, one production-proximate rail, and one evidence rail.

### Step 7: Design verification cost tiers

Load `references/verification-cost-tiers.md` and `../assess-verification/references/bug-surface-routing.md`.

For each target component, assign **Check**, **Verify-quick**, and **Verify-full** command sets (or CI
jobs) matched to bug-surface class and risk class:

| Component | Class | Check (seconds) | Verify-quick (~min) | Verify-full | Skip justification |
|-----------|-------|-----------------|----------------------|-------------|-------------------|
| ... | A–E | ... | ... | required / nightly / skip | ... |

Recommend:
- Post-write or pre-commit hooks for **Check** tier (T1 execution)
- Pre-commit or CI for **Verify-quick**
- Required CI check or nightly for **Verify-full** only where class C/D or High/Critical risk
- Explicit auditable opt-outs for Class A + Low risk (never silent skip)

Flag components where verify-full tools run on every save (blocks agents) or Check tier runs only in
CI (late feedback).

When bug-surface depth and risk class conflict, use the **higher** requirement (e.g. Low risk + Class C
→ verify-full for simulation/model-check; High risk + Class A → verify-quick sufficient unless ADR
documents deeper need).

### Step 8: Design feedback loop improvements

Load `../assess-verification/references/feedback-loop-model.md` for feedback loop maturity levels and assessment criteria.

If `verification-report.md` exists, read the Feedback Loop Completeness section. Otherwise, do a lightweight check:
- Look for structured output configs in CI (JUnit XML reporters, SARIF output, JSON formatters)
- Check if CI results are accessible via API or stored as retrievable artifacts
- Look for agent re-execution patterns (workflow dispatch, retry configs, bot triggers)

For each verification method at Level 0-1, recommend how to close the loop:

| Current state | Recommended action | Tools/config |
|---------------|-------------------|--------------|
| Plain text logs only | Add structured reporter | JUnit XML, SARIF, JSON formatter |
| Structured output not stored | Add artifact upload step | actions/upload-artifact, S3, GCS |
| Artifacts not accessible to agents | Expose via API or webhook | GitHub Checks API, CI notification |
| No re-execution trigger | Add dispatch or retry mechanism | workflow_dispatch, retry-on-failure |

For each recommendation, specify the concrete config change or tool addition needed.

### Step 9: Design shift-left repositioning

Load `../assess-verification/references/shift-left-model.md` for the tier model.

If `verification-report.md` exists, read the Shift-Left Assessment section. Otherwise, check whether
type checking / linting run only in CI (should be per-file via pre-commit or hooks), whether pre-commit
hooks exist (`.pre-commit-config.yaml`, `.husky/`, `lefthook.yml`), and whether focused/affected-only
test runs are available.

For each check running later than its ideal tier, recommend how to shift it earlier:

| Check | Current | Target | Action |
|-------|---------|--------|--------|
| Type checking | T3 (CI only) | T1 (per-file) | Add pre-commit hook or agent post-write hook running `tsc --noEmit` |
| Linting | T3 (CI only) | T1 (per-file) | Add pre-commit hook; configure agent to run linter after each write |
| Secret scanning | T3 (CI) | T1 (pre-commit) | Add `detect-secrets` or `gitleaks` pre-commit hook |
| Focused / affected tests | T3 (full suite) | T2 (per-module) | Run changed-files tests only; add TIA (`pytest-testmon`, Jest `--onlyChanged`, Launchable) |

For each recommendation, specify the concrete tool and config to add.

### Step 10: Design workflow gate optimization

Load `references/gate-design-patterns.md`.

If `verification-report.md` exists, read the Workflow Gate Assessment section. Otherwise, identify gates from:
- Branch protection rules (`.github/settings.yml`, repo settings)
- CODEOWNERS file
- CI approval steps (environment protection, manual gates)
- Documented review processes

Recommend gate consolidation toward the three-checkpoint model:

1. **Gates to remove or automate**: Low-risk reviews where CI is authoritative, rubber-stamp approvals
2. **Gates to add**: High-risk components lacking human checkpoints
3. **Gates to reposition**: Checks happening too late (at deploy) that should be at PR time
4. **Feedback improvements**: Gates that reject without actionable context for agents

For each recommendation:
- State which gate to change
- What the current and proposed states are
- What risk class it serves
- Whether the change increases or decreases agent throughput

### Step 11: Design eval framework

Load `references/eval-framework.md` and `references/eval-framework-operations.md` for eval components, measurement dimensions, and building strategy.

Recommend an eval framework appropriate for the codebase:

1. **Identify 5-10 seed tasks** drawn from recent project history (bug fixes, features, refactors, config changes)
2. **Calibrate difficulty** — annotate each with estimated human-expert time
3. **Define success criteria** — for each task, what must pass (tests, types, lint, behavior)
4. **Recommend automation** — how to run evals (scripts, CI workflow, scheduled job)
5. **Map to verification gaps** — low eval scores indicate weak oracles, poor feedforward, or exceeded horizons

For each recommended eval task:
- Source (issue, PR, or synthetic scenario)
- Difficulty tier (trivial/easy/medium/hard)
- Files that should change
- Success criteria (which checks must pass)
- Measurement dimensions (correctness, convention, efficiency)

### Step 12: Design verifier-guided search and generator-evaluator strategy

Load `references/verifier-guided-search.md` (primary for L4/L5), `references/generator-evaluator.md`
(dual-agent when no deterministic verifier), and `references/candidate-selection-policy.md`.

For high-criticality components, recommend search architecture:

| Pattern | Apply when | Cost |
|---------|-----------|------|
| Verifier-guided search | Deterministic verifier exists; L4/L5 target | Variable |
| Generate → Verify → Retry | Simple agent correction loops | Low–medium |
| Best-of-N + verifier | Independent implementations | N× |
| Counterexample-guided | Informative verifier feedback | Medium |
| Generator + Test-Writer | No verifier; clear specs | 2x |
| Generator + Critic | No verifier; security-sensitive | 1.5x |
| N-of-M Consensus | Filter by verifier first, then compare | Nx |

For each recommendation:
- Which component/change type it applies to
- Which verifier is authoritative (must be deterministic when available)
- Mandatory properties vs optimization objectives
- Oracle integrity protections (AI012)
- How to integrate into CI (server-side verifier, not agent-self-judged)

### Step 13: Design documentation verification

If `verification-report.md` exists, read the Documentation Verification section. Otherwise, check:
- Whether API docs are auto-generated from code or manually maintained
- Whether doc builds run in CI with strict mode (fail on broken refs)
- Whether code examples in docs are tested

Recommend documentation-as-code practices based on current gaps:

| Current state | Recommendation | Tools |
|---------------|---------------|-------|
| No auto-generated docs | Add doc generation from code annotations | TypeDoc, Sphinx autodoc, rustdoc, springdoc |
| Docs exist but not in CI | Add strict doc build + link checking to CI | `mkdocs build --strict`, `markdown-link-check` |
| Examples not tested | Add doctest or tested snippet pipeline | `pytest --doctest-modules`, `cargo test` (doc examples) |
| No schema-doc sync | Validate API spec against implementation | schemathesis, openapi-diff, prism mock validation |
| Docs not updated with code | Add freshness enforcement (co-change requirements) | CODEOWNERS on docs, CI check for doc-alongside-code |

For each recommendation, specify the concrete tool and config needed. Priority: schema-doc sync (prevents fabrication) > example testing (catches drift) > freshness enforcement (process-level).

### Step 14: Produce implementation roadmap

Order recommendations by priority:

1. **Quick wins** (small effort, high impact): pre-commit hooks, shift type checking/linting per-file, structured CI reporters, first fitness function, doc link checking, TIA for affected tests
2. **Foundation** (medium effort, enables future): property tests, contract testing, close feedback loops, focused test scripts, seed eval suite, schema-doc sync, requirement-coverage check
3. **Deep investment** (large effort, high assurance): formal specs, model checking, shadow testing, gate redesign, generator-evaluator for critical paths, behavioral twins, pipeline-enforced RTM

For each item specify: action, component, effort, dependencies, tools to install.

### Step 15: Design requirement traceability

Load `references/traceability-design.md`. Read the report's Requirement Traceability section if present;
otherwise check for stable requirement IDs, executable acceptance criteria (Gherkin/BDD), PR→issue links,
and a requirement-coverage report. Recommend the next maturity step plus three explicit deliverables:

1. **Linking conventions**: stable requirement IDs, criterion→test tags, and code→requirement commit trailers.
2. **The gate**: a CI step that reports uncovered requirements and untraced changes, blocking vs warning per risk class.
3. **The human role**: comparing implementation to intent only where the trace is ambiguous.

**Load-bearing constraint**: the gap *check* must be a deterministic script that parses IDs/tags — not
an agent re-reading the spec. An agent re-reading the spec to "verify" the trace reintroduces the exact
indeterminism the RTM exists to remove (an agent verifying agents). Make this explicit in the recommendation.

### Step 16: Design safe-evolution strategy

For components facing breaking or large-scale change (renames, API/schema reshapes, convention
migrations), load `references/safe-evolution.md` and `references/change-semantics.md`.

- **Parallel Change** for interface/shape changes: expand (add new form alongside old) → migrate
  callers incrementally → contract (remove old). No breaking window; each phase ships reversibly.
- **Sweep** for one-rule-many-files changes: prefer codemods over regex; write the rule down, sample
  3-4 sites, execute in small batches, and gate each batch on tests + diff review.

Recommend this wherever the assessment flagged a large refactor, migration, or cross-cutting rename.
Tie the gate back to the evidence pipeline (Step 6): each incremental step passes the same checks.

For brownfield legacy components, also load `references/specification-mining.md` when explicit
invariants are missing.

### Step 17: Write the strategy

Load `references/strategy-report-template.md`. Write `verification-strategy.md` following the template, covering all sections from Steps 1-16 (component strategies through roadmap, plus traceability and safe-evolution).
