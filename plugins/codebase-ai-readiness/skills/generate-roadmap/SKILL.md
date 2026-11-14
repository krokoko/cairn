---
name: generate-roadmap
description: |
  Generate a prioritized improvement roadmap to increase AI readiness.
  Trigger phrases: "generate roadmap", "what should I improve",
  "how to reach the next level", "autonomy improvement plan",
  "what are my next steps for AI readiness"
  Optional argument: [target-level] (L1-L5, defaults to next level above current)
allowed-tools: Read Bash Glob Grep
---

# Generate AI Readiness Roadmap

Produce a prioritized plan to close evidenced gaps on specific surfaces. Autonomy levels and
scores are provisional diagnostics; planned work does not establish readiness or authorize actions.

## Workflow

### Step 1: Load prior assessment

Search for `readiness-report.md` in the codebase root. If it exists, read it and extract:
- Provisional score and assessed weight
- Per-surface autonomy recommendations and prerequisites
- Category scores
- Existing blockers

If no report exists, inform the user: "No readiness report found. Run `/assess-readiness` first to generate a baseline assessment."

Also extract from the report if present: workflow artifacts summary, compound engineering score,
collaboration effectiveness recommendations, alignment note (if any).

Load `../assess-readiness/references/evidence-scope.md`. Compare source revision (including
relevant dirty changes), inspected scope, requirement/oracle revisions and evidence environments
with the current target. Reuse unaffected findings with attribution. Refresh affected findings
when evidence is available; otherwise flag them stale/unverified and prioritize gathering evidence.
Legacy reports without this metadata cannot establish current readiness. Record the source
report and freshness decision in **Evidence Scope**; do not fabricate a run ledger for planned work.

### Step 2: Determine target level

- If the user provided a target level argument (L1-L5), use that.
- Otherwise, use the next level above the evidenced current level for the chosen surface (maximum L5).
- When the current level is unknown, first plan the missing assessment evidence; label any proposed target provisional.
- Load `references/level-transitions.md` and `../assess-readiness/references/autonomy-prerequisites.md`.
  Apply the same L4 scope prerequisites, ceilings and five L5 gates as assessment;
  proposed actions do not make a prerequisite `met`.
- If **current level ≤ L2 and target level ≥ L3**, load `references/l2-to-l3-hinge.md` and add
  the **L2 → L3 hinge** section to the roadmap.

### Step 3: Identify gaps

Compare the surface's observed evidence and prerequisites with the target. Load
`references/improvement-actions.md` and `references/improvement-actions-agent.md` for actions;
adapt their acceptance criteria to the actual claim and stack. Load
`references/implementation-phases.md` for strategic phasing and prioritization.

If the report's alignment note indicates **codebase ahead of practices**, prioritize repo
enablers from `references/l2-to-l3-hinge.md` and collaboration actions from
`improvement-actions-agent.md`. If **practices ahead of codebase**, prioritize verification,
types, CI, and testable-boundaries actions before expanding agent workflows.

Focus on:
- Missing/unknown prerequisites and unsupported critical-path claims
- Failures in testable boundaries, CI reliability, reviewed intent and dependency fidelity
- Useful improvements with observable outcomes relative to effort
- Sequence actions according to the 5-phase model (semantics -> fast loop -> deep evidence -> reality loop -> human repositioning)

### Step 3b: Dual-track gaps (compound engineering and context)

If compound engineering or progressive context has observed gaps relevant to the target,
load `references/workflow-and-surfaces.md`. Plan **paired** improvements:
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
- **Failure addressed**: The concrete risk or observed friction
- **Acceptance criterion**: Observable check/outcome, required evidence and remaining limits
- **Dependencies**: Other actions that should happen first
- **Details**: Specific files to create/modify, tools to install, configs to add

Order actions by: (1) establish missing evidence and close critical gates, (2) alignment-driven
priority when the report flags a mismatch, (3) risk reduction relative to effort, (4) foundations
before dependent work. Do not promise score increments or recommend refactoring to improve
counts alone. For maintainability, pair a concrete boundary check with a representative change
exercise when useful; record unexpected edits, effort, regressions and preserved constraints.

### Step 5: Write the roadmap

Write a new `readiness-roadmap.md` file in the codebase root:

```markdown
# AI Readiness Roadmap

## Evidence Scope

**Source revision**: [current commit and relevant dirty changes, or explain unavailable identity]
**Assessment date**: [date of planning assessment]
**Inspected scope**: [target surfaces and exclusions]
**Evidence basis**: [source report path/revision/date; freshness comparison; reused, stale and unknown findings]

**Current level**: [evidenced level or unknown] | **Target level**: [surface and level] | **Current score**: [provisional score and assessed weight, or unknown]

## Critical path (must-do for next level)

| # | Action | Category | Effort | Failure addressed | Acceptance criterion | Details |
|---|--------|----------|--------|-------------------|----------------------|---------|
| 1 | ... | ... | ... | ... | ... | ... |

## L2 → L3 hinge

Include when current level ≤ L2 and target level ≥ L3. Split codebase critical path vs repo
enablers. Load `references/l2-to-l3-hinge.md`.

## Session infrastructure (dual track)

Include this section when compound engineering or progressive context disclosure is below
target. Pair one Track A action (durable surfaces / CI) with one Track B action (workflow
artifacts or packaged skill) per row.

| # | Track A (durable surfaces) | Track B (workflow artifacts / skills) | Effort | Acceptance criterion |
|---|----------------------------|---------------------------------------|--------|----------------------|
| 1 | ... | ... | ... | ... |

## Collaboration effectiveness

| # | Action | Effort | Acceptance criterion | Details |
|---|--------|--------|----------------------|---------|
| 1 | ... | ... | ... | ... |

## High-impact improvements

| # | Action | Category | Effort | Failure addressed | Acceptance criterion | Details |
|---|--------|----------|--------|-------------------|----------------------|---------|
| 1 | ... | ... | ... | ... | ... | ... |

## Nice-to-have

| # | Action | Category | Effort | Failure addressed | Acceptance criterion | Details |
|---|--------|----------|--------|-------------------|----------------------|---------|
| 1 | ... | ... | ... | ... | ... | ... |
```

**Evidence Scope**, **Critical path (must-do for next level)** and **High-impact improvements**
are mandatory and need substantive content. Where no action applies, state that with a reason.
Distinguish the acceptance evidence each action should produce from evidence already inspected.
