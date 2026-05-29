# Readiness Report Template

Write `readiness-report.md` at the codebase root using this structure:

```markdown
# AI Readiness Report

## Overall Score

**Score: XX/100**

## Recommended Autonomy Level

**Level: LX — [Level Name]**

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
| Machine-readable intent | XX | ... |
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

**Recommendations:**

1. ...
2. ...

## Blockers

[List of specific blockers preventing advancement to next level]

## Roadmap

| Priority | Action | Category | Effort | Impact |
|----------|--------|----------|--------|--------|
| 1 | ... | ... | ... | ... |
```
