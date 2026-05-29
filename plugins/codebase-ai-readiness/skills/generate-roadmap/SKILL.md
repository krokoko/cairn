---
name: generate-roadmap
description: |
  Generate a prioritized improvement roadmap to increase AI readiness.
  Trigger phrases: "generate roadmap", "what should I improve",
  "how to reach the next level", "autonomy improvement plan",
  "what are my next steps for AI readiness"
argument-hint: "[target-level] (L1-L5, defaults to next level above current)"
allowed-tools: Read Bash Glob Grep
user-invocable: true
---

# Generate AI Readiness Roadmap

Produce a detailed, prioritized improvement plan to advance the codebase to the next autonomy level (or a specified target level).

## Workflow

### Step 1: Load prior assessment

Search for `readiness-report.md` in the codebase root. If it exists, read it and extract:
- Current overall score
- Current autonomy level
- Category scores
- Existing blockers

If no report exists, inform the user: "No readiness report found. Run `/assess-readiness` first to generate a baseline assessment."

Also extract from the report if present: workflow artifacts summary, compound engineering score,
collaboration effectiveness recommendations.

### Step 2: Determine target level

- If the user provided a target level argument (L1-L5), use that.
- Otherwise, use the next level above the current level.
- Load `references/level-transitions.md` for transition requirements.

### Step 3: Identify gaps

For each category, compare the current score to what is needed for the target level. Load `references/improvement-actions.md` and `references/improvement-actions-agent.md` for common actions. Load `references/implementation-phases.md` for the strategic phasing model and prioritization principles.

Focus on:
- Categories that are below the threshold for the target level
- Categories with the highest weight in the scoring rubric (testable boundaries, CI reliability, machine-readable intent, structure)
- Quick wins: actions that have high impact relative to effort
- Sequence actions according to the 5-phase model (semantics -> fast loop -> deep evidence -> reality loop -> human repositioning)

### Step 3b: Dual-track gaps (compound engineering and context)

If compound engineering readiness or progressive context disclosure is below the threshold
for the target level, load `references/workflow-and-surfaces.md`. Plan **paired** improvements:
Track A (CI, types, hooks, instruction files) and Track B (workflow artifact dirs, packaged
skills for repeatable agent workflows). Do not recommend only infrastructure fixes when session
context is absent.

If the readiness report lacks collaboration metrics or marks them "not measured", add roadmap
actions from `../assess-readiness/references/collaboration-metrics.md` (tracking, PR template,
post-review rule updates).

### Step 4: Build the roadmap

For each recommended action, specify:
- **Action**: Concrete, specific task (e.g., "Add pytest configuration with coverage reporting")
- **Category**: Which assessment category it improves
- **Effort**: Small (hours), Medium (days), Large (weeks)
- **Impact**: Expected score improvement for the category
- **Dependencies**: Other actions that should happen first
- **Details**: Specific files to create/modify, tools to install, configs to add

Order actions by: (1) unblock the next level first, (2) highest impact/effort ratio, (3) foundational actions before dependent ones.

### Step 5: Write the roadmap

Write a new `readiness-roadmap.md` file in the codebase root:

```markdown
# AI Readiness Roadmap

**Current level**: LX | **Target level**: LY | **Current score**: XX/100

## Critical path (must-do for next level)

| # | Action | Category | Effort | Impact | Details |
|---|--------|----------|--------|--------|---------|
| 1 | ... | ... | ... | ... | ... |

## Session infrastructure (dual track)

Include this section when compound engineering or progressive context disclosure is below
target. Pair one Track A action (durable surfaces / CI) with one Track B action (workflow
artifacts or packaged skill) per row.

| # | Track A (durable surfaces) | Track B (workflow artifacts / skills) | Effort | Impact |
|---|----------------------------|---------------------------------------|--------|--------|
| 1 | ... | ... | ... | ... |

## Collaboration effectiveness

| # | Action | Effort | Impact | Details |
|---|--------|--------|--------|---------|
| 1 | ... | ... | ... | ... |

## High-impact improvements

| # | Action | Category | Effort | Impact | Details |
|---|--------|----------|--------|--------|---------|
| 1 | ... | ... | ... | ... | ... |

## Nice-to-have

| # | Action | Category | Effort | Impact | Details |
|---|--------|----------|--------|--------|---------|
| 1 | ... | ... | ... | ... | ... |
```
