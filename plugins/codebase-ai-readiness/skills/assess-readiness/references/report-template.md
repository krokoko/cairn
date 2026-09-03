# Readiness Report Template

Write `readiness-report.md` at the codebase root using this structure:

```markdown
# AI Readiness Report

## Overall Score

**Score: XX/100** (weighted over N applicable categories; see Signal evidence for verdict counts)

## Recommended Autonomy Level

**Level: LX — [Level Name]**

**Gate-derived:** LX (highest level with ≥80% of gating requirements passing)
**Score-derived:** LY [if they differ by more than one step, name the signals causing the gap]

**Autonomy cap applied:** [yes/no — if yes, cite spec-first gap per `references/spec-first-artifacts.md`; e.g. "Capped at L3: no requirement files or executable acceptance criteria"]

## Level gates

| Level | Requirements passed | Pass % | Unlocked |
|-------|---------------------|--------|----------|
| L1 | n/m | XX% | yes/no |
| L2 | n/m | XX% | yes/no |
| L3 | n/m | XX% | yes/no |
| L4 | n/m | XX% | yes/no |
| L5 | n/m | XX% | yes/no |

## Category Breakdown

| Category | Score | Pass/Applicable | Notes |
|----------|-------|-----------------|-------|
| Structure and modularity | XX | n/m | ... |
| Documentation | XX | n/m | ... |
| Testable boundaries | XX | n/m | ... |
| CI reliability | XX | n/m | ... |
| Typing strength | XX | n/m | ... |
| Deterministic environment and deployment | XX | n/m | ... |
| Architecture decisions | XX | n/m | ... |
| Machine-readable intent | XX | n/m | Spec-first: REQ files [y/n], executable criteria [y/n], pure core [y/n], traceability gate [y/n]; cap rule applied [y/n] |
| Progressive context disclosure | XX | n/m | ... |
| Hidden state and magic | XX | n/m | ... |
| Repository-scale reasoning | XX | n/m | ... |
| Failure mode legibility | XX | n/m | ... |
| Feedforward surfaces | XX | n/m | ... |
| Compound engineering readiness | XX | n/m | ... |
| Context engineering friendliness | XX | n/m | ... |

Categories with zero applicable signals show `—` and are excluded from the weighted score.

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

**Infrastructure:** [PR templates, issue templates, labels, review rubric, learning docs, agent co-authored commits — present or missing]

**Recommendations:**

1. ...
2. ...

**Alignment note:** [Include only when mismatch detected — practices ahead of codebase or codebase ahead of practices. See `references/autonomy-levels.md`. Otherwise omit or write "Aligned."]

## Blockers

[Specific blockers preventing the next level gate: name the FAIL signals. List NOT INSPECTABLE signals as "verify with access".]

## Roadmap

| Priority | Action | Category | Effort | Impact |
|----------|--------|----------|--------|--------|
| 1 | ... | ... | ... | ... |

## Changes since last assessment

[Include when a prior `readiness-report.md` existed. Omit otherwise.]

| Signal | Previous | Current | Why it changed |
|--------|----------|---------|----------------|
| ... | PASS/FAIL/N/A | PASS/FAIL/N/A | file added / config changed / ... |

## Signal evidence

One row per signal. For monorepos, app-scoped rows record `n/m apps` in the evidence.

| Category | Signal | Verdict | Evidence |
|----------|--------|---------|----------|
| ... | ... | PASS / FAIL / N/A / NOT INSPECTABLE | file, config key, command output, or reason |
```
