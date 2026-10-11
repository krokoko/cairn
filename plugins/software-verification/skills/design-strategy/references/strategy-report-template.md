# Strategy Report Template

Write `verification-strategy.md` with this structure. Replace example rows with substantive records;
justify inapplicable sections. Use `../../assess-verification/references/evidence-semantics.md` for
ledger states. Existing observations belong in the ledger; planned checks belong in requirements.

```markdown
# Verification Strategy

## Evidence Scope

**Source revision**: [commit plus relevant working-tree changes]
**Assessment date**: [ISO date]
**Inspected scope**: [components, paths, environments, exclusions]
**Evidence basis**: [artifacts inspected, access limits, prior-report freshness]

## Evidence Ledger

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| [existing check] | [path/run and revision] | [actual environment] | configuration_only | unknown | unknown | [uninspected execution or other limits] |

## Evidence Requirements

All rows below are proposed requirements, not completed evidence.

| Claim / requirement | Oracle / review owner | Required evidence / environment | Completion / acceptance criteria | Scope / limits |
|---------------------|-----------------------|---------------------------------|----------------------------------|----------------|
| [bounded claim and revision] | [assertion revision, owner, invalidation rule] | [reports, source/config identity, environment] | [completed checks and supported result] | [bounds, exclusions, remaining gaps] |

## Component Strategies

| Component | Archetype | Current | Recommended additions | Effort |
|-----------|-----------|---------|----------------------|--------|

### [Component Name]
**Current state**: ...
**Proposed target state**: ...
**Actions**: 1. ... 2. ...

## Oracle Strategy

| Component | Oracle type | Implementation | Properties / review lifecycle |
|-----------|-------------|----------------|-------------------------------|

## Evidence Pipeline

| Risk level | Merge requirements | Deploy requirements | Rollback triggers |
|------------|-------------------|--------------------|--------------------|
| Low | ... | ... | ... |
| Medium | ... | ... | ... |
| High | ... | ... | ... |
| Critical | ... | ... | ... |

## Verification Cost Tiers

| Component | Class (A–E) | Check (T1) | Verify-quick | Verify-full | Opt-out (auditable) |
|-----------|-------------|------------|--------------|-------------|---------------------|
| ... | ... | commands/hooks | CI job / script | required / nightly / skip | ... |

**Hook/alias recommendations**: ...
**Ceremony flags** (verify-full on Class A): ...

## Shift-Left Recommendations

| Check | Current tier | Target tier | Action | Tool/config |
|-------|-------------|------------|--------|-------------|

## Feedback Loop Improvements

| Verification method | Current level | Target level | Action | Config change |
|---------------------|--------------|--------------|--------|---------------|

## Workflow Gate Optimization

| Gate | Current state | Recommendation | Risk class | Impact on agent throughput |
|------|--------------|----------------|-----------|---------------------------|

## Architecture Fitness Functions

| Property | Type | Tool / qualified scope | Runs at | Controls / remaining limits |
|----------|------|------------------------|---------|-----------------------------|

**Maintenance exercise**: [representative change, effort/unexpected edits/regressions, or justified inapplicability]

## Eval Framework

| Task | Source | Difficulty | Files | Success criteria |
|------|--------|-----------|-------|------------------|

Measurement: [reviewed task criteria, prohibited overclaims, sample size, model/configuration, uncertainty]

## Generator-Evaluator Recommendations

| Component | Variant | When to apply | Cost management |
|-----------|---------|--------------|-----------------|

## Documentation Verification

| Dimension | Current | Recommendation | Tool |
|-----------|---------|----------------|------|
| Auto-generation | ... | ... | ... |
| CI doc build | ... | ... | ... |
| Link validation | ... | ... | ... |
| Example testing | ... | ... | ... |
| Schema-doc sync | ... | ... | ... |
| Freshness enforcement | ... | ... | ... |

## Requirement Traceability

**Current evidence → proposed target**: [links, execution, and meaning separately]

| Obligation | Current evidence / gaps | Proposed mechanism | Completion criteria / review owner |
|------------|-------------------------|--------------------|------------------------------------|
| Links and relevant change references | ... | ... | ... |
| Expected vs executed checks | ... | ... | ... |
| Assertion-to-claim meaning and freshness | ... | ... | ... |

## Implementation Roadmap

### Phase 1: Quick wins
| # | Action / failure addressed | Component | Effort | Completion evidence |
|---|---------------------------|-----------|--------|---------------------|

### Phase 2: Foundation
...

### Phase 3: Deeper checks where justified
...
```
