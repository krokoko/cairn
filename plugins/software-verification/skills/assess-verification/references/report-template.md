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

| Component | Current oracle | Strength (strong/weak/none) | Gap (incl. oracle rot) | Recommended oracle type |
|-----------|---------------|-----------------------------|------------------------|------------------------|
| ... | ... | ... | ... | ... |

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
| Domain | 0-3 | ... | ... |

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

## Verification Debt

Consolidated, ticketable backlog rolled up from the gaps found in every section above
(missing/weak oracles, feedback-loop gaps, shift-left gaps, doc-verification gaps, telemetry
blind spots, traceability gaps). One row = one liability = one fileable issue.

| ID | Component | Debt type | Severity | Current → Required | Remediation |
|----|-----------|-----------|----------|--------------------|-------------|
| VD-1 | ... | Missing oracle / Weak oracle / Oracle rot / No fuzz target / Uncovered requirement / Unrouted feedback / Late shift-left / Stale docs / Telemetry blind spot | High / Medium / Low | e.g. "OpenAPI spec, no contract test" | ... |

**Severity rubric**: High = high-criticality component with no/weak oracle, or a gap that lets
silent regressions ship; Medium = business logic with partial coverage; Low = utilities, cosmetic.

**Suggested labels** (for export to issues/Jira): `verification-debt`, plus debt type and severity.
```
