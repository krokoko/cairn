# Verification Report Template

Write `verification-report.md` with the following structure. Load `evidence-semantics.md` for ledger
statuses and `oracle-lifecycle.md` for review evidence. Fill gaps explicitly; omit no required section.

```markdown
# Software Verification Report

## Evidence Scope

**Source revision**: [commit/snapshot and relevant uncommitted changes]
**Assessment date**: [YYYY-MM-DD]
**Inspected scope**: [components, paths, environments, accessible settings]
**Evidence basis**: [inspected runs/artifacts, configuration observations, unavailable evidence]

## Evidence Ledger

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| [claim / check] | [config path / revision] | [environment] | configuration_only | unknown | unknown | [missing run evidence and relevant assumptions] |

## Verification Maturity

**Demonstrated overall tier**: X/5 — [Tier Name], or unknown
**Rubric**: verification-maturity/2; [assessment date and changes from historical method-based scores]
**Limiting evidence / provisional target**: [critical paths, unknowns, justified inapplicability]

## Component Breakdown

| Component | Archetype | Criticality | Current methods / evidence | Demonstrated tier / limit |
|-----------|-----------|-------------|----------------------------|---------------------------|

## Bug-Surface Classification

| Component | Class (A–E) | Evidence | Recommended depth | Ceremony risk |
|-----------|-------------|----------|-------------------|---------------|
| ... | ... | ... | floor / standard / deep | Yes / No — ... |

**Checks with no identified claim/gap**: ...
**Failure surfaces lacking relevant evidence**: ...

## Missing Oracles

| Component / claim | Current oracle | Strength (qualified/weak/unknown/none) | Adequacy / sensitivity / independence / freshness | Gap / action |
|-------------------|---------------|---------------------------------------|-------------------------------------------------|--------------|

Record supported/gap/unknown per dimension with evidence. Link requirement/assertion/fixture/helper
revisions and owner/review date. Separate semantic-review freshness from execution freshness.

## Exactness Analysis

| Component | Feasibility | Rationale |
|-----------|-------------|-----------|
| ... | Exact within scope feasible / Statistical-empirical / Mixed | [property, assumptions; not evidence of a completed proof] |

## Human Review Requirements

| Component | Reason | Review type |
|-----------|--------|-------------|

## Autonomy Candidates

| Changed surface | Recommended operating scope | Evidence / confidence | Remaining claims / environment gaps |
|-----------------|-----------------------------|-----------------------|------------------------------------|

Maturity does not grant permission; preserve review policy and show per-surface limits.

## Feedback Loop Completeness

**Overall level**: X/3 — [Level Name]

| Verification method | Output format | Routable to agents? | Level | Gap |
|---------------------|--------------|---------------------|-------|-----|

## Workflow Gate Assessment

| Gate | Risk class | Throughput concern? | Recommendation |
|------|-----------|---------------------|----------------|

**Bottleneck gates**: ...
**Missing gates**: ...

## Shift-Left Assessment

| Check | Current tier | Ideal tier | Gap | Recommendation |
|-------|-------------|-----------|-----|----------------|

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

**Overall level**: X/3, or unknown

| Completeness | Evidence / current state | Gap / required review |
|--------------|--------------------------|-----------------------|
| Links | ... | [missing or questionable mappings] |
| Execution | ... | [skipped/missing/stale evidence] |
| Meaning | ... | [partial claims, deviations, stale/unknown review] |

| Property | State | Failure it allows |
|----------|-------|-------------------|
| Scope verification | ... | Unrequested logic / missed requirement |
| Impact analysis | ... | Unknown affected tests/files on change |
| Test sufficiency | ... | Requirement with no dedicated test |

**Untraced changes** (code with no upstream requirement): ...
**Uncovered requirements** (requirement with no test): ...
**Intent-drift risk**: ...

## Verification Debt

Consolidate assessed gaps into one ticketable liability per row, ordered by consequence.

| ID | Component | Debt type | Severity | Current → Required | Remediation |
|----|-----------|-----------|----------|--------------------|-------------|
| VD-1 | ... | Missing oracle / Weak oracle / Oracle rot / No fuzz target / Uncovered requirement / Unrouted feedback / Late shift-left / Stale docs / Telemetry blind spot | High / Medium / Low | e.g. "OpenAPI spec, no contract test" | ... |

**Severity rubric**: High = high-criticality component with no/weak oracle, or a gap that lets
silent regressions ship; Medium = business logic with partial coverage; Low = utilities, cosmetic.
```
