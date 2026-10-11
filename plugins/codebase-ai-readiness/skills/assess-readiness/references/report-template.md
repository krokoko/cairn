# Readiness Report Template

Write `readiness-report.md` at the codebase root using this structure:

```markdown
# AI Readiness Report

## Evidence Scope

**Source revision**: [commit and relevant dirty changes, or explain unavailable identity]
**Assessment date**: [date]
**Inspected scope**: [paths, components, dependencies and exclusions]
**Evidence basis**: [artifacts/runs inspected and inaccessible evidence]

## Evidence Ledger

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| [claim and check] | [cited artifact/run and revision] | [environment] | [allowed observation] | [allowed execution] | [allowed conclusion] | [bounds, exclusions and review status] |

## Overall Score

**Score:** [provisional XX/100 or unknown]
**Rubric:** readiness-scoring/2
**Assessed weight:** [share of category weights scored; excluded categories and reasons]

## Recommended Autonomy Level

**Level:** [exactly L0–L5; no higher than the lowest assessed surface recommendation]
**Summary scope:** [all assessed surfaces and dependencies; exclusions remain outside the recommendation]
**Decision boundary:** [recommendation only; operating permissions remain external]

**Autonomy cap applied:** [yes/no and evidence; include unknown intent/oracles and unmet L5 gates]

## Surface Autonomy

| Surface | Provisional level | Evidence ceiling | Recommended level | Operating scope | Blockers |
|---------|-------------------|------------------|-------------------|-----------------|----------|
| [surface and dependencies] | [L0–L5 or unknown] | [L0–L5 or unknown] | [L0–L5] | [change classes/human decisions] | [ceiling rationale and gaps, or reason none] |

## Autonomy Prerequisites

| Surface | Prerequisite | Status | Evidence / gap |
|---------|--------------|--------|----------------|
| [surface] | L4-INTENT | [status] | [reviewed executable intent for the proposed operating scope or gap] |
| [surface] | L4-ORACLES | [status] | [current adequate critical-path oracle evidence for that scope or gap] |
| [surface] | L5-INTENT | [status] | [cited evidence or gap] |
| [surface] | L5-ORACLES | [status] | [cited evidence or gap] |
| [surface] | L5-ENVIRONMENT | [status] | [cited evidence or gap] |
| [surface] | L5-DETECTION | [status] | [cited evidence or gap] |
| [surface] | L5-RECOVERY | [status] | [cited evidence or gap] |

## Category Breakdown

| Category | Score | Notes |
|----------|-------|-------|
| Structure and modularity | XX | ... |
| Documentation | XX | ... |
| Testable boundaries | XX | ... |
| CI reliability | XX | ... |
| Typing strength | XX | ... |
| Deterministic environment and deployment | XX | ... |
| Architecture decisions | XX | ... |
| Machine-readable intent | XX / unknown | Reviewed claims, executable criteria, links, completed evidence and semantic review; cap rule and gaps |
| Progressive context disclosure | XX | ... |
| Hidden state and magic | XX | ... |
| Repository-scale reasoning | XX | ... |
| Failure mode legibility | XX | ... |
| Feedforward surfaces | XX | ... |
| Compound engineering readiness | XX | ... |
| Context engineering friendliness | XX | ... |

## Workflow artifacts

| Artifact type | Present | Location / notes |
|---------------|---------|------------------|
| Requirements / specs | yes/no | ... |
| Design / blueprints | yes/no | ... |
| Execution plans | yes/no | ... |
| Review / learnings | yes/no | ... |

**Summary:** [One paragraph: maturity of session-scoped context; what is missing]

## Collaboration effectiveness

| Metric | Status | Notes |
|--------|--------|-------|
| First-pass acceptance | measured / estimated / not measured | ... |
| Iteration cycles per task | measured / estimated / not measured | ... |
| Post-merge rework (7-day) | measured / estimated / not measured | ... |

**Infrastructure:** [PR templates, labels, review rubric, learning docs — present or missing]

**Maintenance outcome:** [representative task, scope, effort, unexpected edits, regressions and boundary violations; or not measured with a proposed exercise]

**Recommendations:**

1. ...
2. ...

**Alignment note:** [Include only when mismatch detected — practices ahead of codebase or codebase ahead of practices. See `references/autonomy-levels.md`. Otherwise omit or write "Aligned."]

## Blockers

[List of specific blockers preventing advancement to next level]

## Roadmap

| Priority | Action | Category | Effort | Failure addressed | Acceptance criterion |
|----------|--------|----------|--------|-------------------|----------------------|
| 1 | ... | ... | ... | ... | ... |
```

Replace placeholders with substantive findings. Use `evidence-scope.md` for state vocabulary
and positive-result constraints. Use `autonomy-prerequisites.md` for canonical gate IDs,
status values and ceiling rules; repeat both L4 and all five L5 rows for each assessed surface.
Category scores may be `unknown` or justified `not applicable`; do not invent zeroes.
