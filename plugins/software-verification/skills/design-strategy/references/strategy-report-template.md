# Strategy Report Template

Write `verification-strategy.md` with the following structure:

```markdown
# Verification Strategy

## Component Strategies

| Component | Archetype | Current | Recommended additions | Effort |
|-----------|-----------|---------|----------------------|--------|

### [Component Name]
**Current state**: ...
**Target state**: ...
**Actions**: 1. ... 2. ...

## Oracle Strategy

| Component | Oracle type | Implementation | Properties to check |
|-----------|-------------|----------------|---------------------|

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

| Property | Type | Tool | Runs at | Maturity |
|----------|------|------|---------|----------|

## Eval Framework

| Task | Source | Difficulty | Files | Success criteria |
|------|--------|-----------|-------|------------------|

Measurement: Correctness (>90% pass), Convention (<2 violations), Efficiency (<5 iterations)

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

**Current level**: X/3 → **Target level**: Y/3

| Linking convention | Current | Recommendation / mechanism | Gate (block vs warn by risk class) |
|--------------------|---------|----------------------------|-------------------------------------|
| Requirement IDs | ... | ... | ... |
| Criterion → test | ... | ... | ... |
| Code → requirement | ... | ... | ... |

## Implementation Roadmap

### Phase 1: Quick wins (week 1)
| # | Action | Component | Effort | Tools |
|---|--------|-----------|--------|-------|

### Phase 2: Foundation (weeks 2-4)
...

### Phase 3: Deep investment (month 2+)
...
```
