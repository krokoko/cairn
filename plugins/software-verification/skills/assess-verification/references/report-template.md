# Verification Report Template

Write `verification-report.md` with the following structure:

```markdown
# Software Verification Report

## Verification Maturity

**Overall tier**: X/5 — [Tier Name]

## Component Breakdown

| Component | Archetype | Criticality | Current methods | Maturity tier |
|-----------|-----------|-------------|-----------------|---------------|
| ... | ... | ... | ... | ... |

## Missing Oracles

| Component | Current oracle | Gap | Recommended oracle type |
|-----------|---------------|-----|------------------------|
| ... | ... | ... | ... |

## Exactness Analysis

| Component | Feasibility | Rationale |
|-----------|-------------|-----------|
| ... | Exact / Statistical / Mixed | ... |

## Human Review Requirements

| Component | Reason | Review type |
|-----------|--------|-------------|
| ... | ... | ... |

## Autonomy Candidates

| Component | Readiness | Confidence | Remaining gaps |
|-----------|-----------|------------|----------------|
| ... | Ready / Near-ready / Not ready | H/M/L | ... |

## Feedback Loop Completeness

**Overall level**: X/3 — [Level Name]

| Verification method | Output format | Routable to agents? | Level | Gap |
|---------------------|--------------|---------------------|-------|-----|
| ... | ... | ... | ... | ... |

## Workflow Gate Assessment

| Gate | Risk class | Throughput concern? | Recommendation |
|------|-----------|---------------------|----------------|
| ... | ... | ... | Keep / Automate / Remove / Add |

**Bottleneck gates**: ...
**Missing gates**: ...

## Shift-Left Assessment

| Check | Current tier | Ideal tier | Gap | Recommendation |
|-------|-------------|-----------|-----|----------------|
| ... | ... | ... | ... | ... |

**Checks running too late**: ...

## Documentation Verification

**Overall level**: X/3

| Dimension | Present? | Mechanism | Gap |
|-----------|----------|-----------|-----|
| Auto-generated docs | ... | ... | ... |
| Doc build in CI | ... | ... | ... |
| Link validation | ... | ... | ... |
| Example testing | ... | ... | ... |
| Schema-doc sync | ... | ... | ... |
| Doc freshness enforcement | ... | ... | ... |

**Stale doc risk areas**: ...

## AgentOps Telemetry

**Overall observability level**: X/3

| Stream | Level | Key gaps | Recommendation |
|--------|-------|----------|----------------|
| Trajectory | 0-3 | ... | ... |
| Cost | 0-3 | ... | ... |
| Quality | 0-3 | ... | ... |
| Autonomy compliance | 0-3 | ... | ... |

**Critical blind spots**: ...

## Requirement Traceability

**Overall level**: X/3

| Property | State | Failure it allows |
|----------|-------|-------------------|
| Scope verification | ... | Unrequested logic / missed requirement |
| Impact analysis | ... | Unknown affected tests/files on change |
| Test sufficiency | ... | Requirement with no dedicated test |

**Untraced changes** (code with no upstream requirement): ...
**Uncovered requirements** (requirement with no test): ...
**Intent-drift risk**: ...
```
