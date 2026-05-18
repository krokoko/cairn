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
Load `references/toolchain-catalog.md` for ecosystem-specific tool recommendations.

For each target component:

1. **Identify archetype**: Deterministic lib, CRUD service, distributed/stateful, safety kernel, ML-backed, agent-written
2. **Look up recommended stack**: From the hybrid strategies reference
3. **Diff current vs recommended**: What already exists? What is missing?
4. **Produce specific recommendations**:
   - Which tools/libraries to add
   - Which files to create or modify
   - Estimated effort (small/medium/large)
   - Expected impact on verification maturity

### Step 4: Design oracle strategy

Load `references/oracle-patterns.md`.

For each component, recommend the best oracle type:

| Component type | Recommended oracle approach |
|---------------|----------------------------|
| Pure functions | Exact expected output + property-based |
| API endpoints | Schema validation + contract tests |
| Data pipelines | Metamorphic relations + replay |
| ML models | Differential + statistical + human |
| State machines | Model checking + replay |
| UI components | Snapshot + visual regression + human |

For each recommendation, specify:
- The oracle type
- How to implement it (specific library, pattern, or technique)
- What properties or relations to check
- How to handle cases where no oracle exists yet

### Step 5: Design evidence pipeline

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

### Step 6: Design feedback loop improvements

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

### Step 7: Design shift-left repositioning

Load `../assess-verification/references/shift-left-model.md` for the tier model.

If `verification-report.md` exists, read the Shift-Left Assessment section. Otherwise, check:
- Whether type checking / linting runs only in CI (should be per-file via pre-commit or hooks)
- Whether pre-commit hooks exist (`.pre-commit-config.yaml`, `.husky/`, `lefthook.yml`)
- Whether focused test runs are available (run only tests for changed modules)

For each check running later than its ideal tier, recommend how to shift it earlier:

| Check | Current | Target | Action |
|-------|---------|--------|--------|
| Type checking | T3 (CI only) | T1 (per-file) | Add pre-commit hook or agent post-write hook running `tsc --noEmit` |
| Linting | T3 (CI only) | T1 (per-file) | Add pre-commit hook; configure agent to run linter after each write |
| Secret scanning | T3 (CI) | T1 (pre-commit) | Add `detect-secrets` or `gitleaks` pre-commit hook |
| Focused unit tests | T3 (full suite) | T2 (per-module) | Add script to run tests for changed files only |

For each recommendation, specify the concrete tool and config to add.

### Step 8: Design workflow gate optimization

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

### Step 9: Produce implementation roadmap

Order recommendations by priority:

1. **Quick wins** (small effort, high impact): Add pre-commit hooks, shift type checking/linting to per-file, add structured CI reporters
2. **Foundation** (medium effort, enables future): Add property tests, set up contract testing, close feedback loops, add focused test scripts
3. **Deep investment** (large effort, high assurance): Formal specifications, model checking, shadow testing infrastructure, gate redesign

For each item specify: action, component, effort, dependencies, tools to install.

### Step 10: Write the strategy

Write `verification-strategy.md`:

```markdown
# Verification Strategy

## Component Strategies

| Component | Archetype | Current | Recommended additions | Effort |
|-----------|-----------|---------|----------------------|--------|
| ... | ... | ... | ... | ... |

### [Component Name]

**Current state**: ...
**Target state**: ...
**Actions**:
1. ...
2. ...

## Oracle Strategy

| Component | Oracle type | Implementation | Properties to check |
|-----------|-------------|----------------|---------------------|
| ... | ... | ... | ... |

## Evidence Pipeline

### Merge requirements by risk level

| Risk level | Required checks |
|------------|----------------|
| Low | ... |
| Medium | ... |
| High | ... |
| Critical | ... |

### Deployment requirements

...

### Rollback triggers

...

## Shift-Left Recommendations

| Check | Current tier | Target tier | Action | Tool/config |
|-------|-------------|------------|--------|-------------|
| ... | ... | ... | ... | ... |

## Feedback Loop Improvements

| Verification method | Current level | Target level | Action | Config change |
|---------------------|--------------|--------------|--------|---------------|
| ... | ... | ... | ... | ... |

## Workflow Gate Optimization

| Gate | Current state | Recommendation | Risk class | Impact on agent throughput |
|------|--------------|----------------|-----------|---------------------------|
| ... | ... | ... | ... | ... |

## Implementation Roadmap

### Phase 1: Quick wins (week 1)

| # | Action | Component | Effort | Tools |
|---|--------|-----------|--------|-------|
| 1 | ... | ... | ... | ... |

### Phase 2: Foundation (weeks 2-4)

...

### Phase 3: Deep investment (month 2+)

...
```
