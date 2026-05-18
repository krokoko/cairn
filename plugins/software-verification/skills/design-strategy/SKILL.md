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

### Step 6: Produce implementation roadmap

Order recommendations by priority:

1. **Quick wins** (small effort, high impact): Add type checking, enable linting, add missing unit tests
2. **Foundation** (medium effort, enables future): Add property tests, set up contract testing, configure coverage
3. **Deep investment** (large effort, high assurance): Formal specifications, model checking, shadow testing infrastructure

For each item specify: action, component, effort, dependencies, tools to install.

### Step 7: Write the strategy

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
