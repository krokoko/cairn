# Workflow Gate Design Patterns

## The three-checkpoint model

Consolidate human review to three high-value gates instead of many low-value interruptions:

| Gate | Purpose | Human role | Agent role |
|------|---------|------------|------------|
| Priority review | Confirm what to work on next | Correct agent-aggregated signals | Triage, rank, summarize context |
| Spec review | Validate plan before execution | Approve intent and scope | Draft spec, identify risks, propose approach |
| Ship review | Final validation before merge/deploy | Verify intent preserved, catch policy violations | High-recall automated inspection, regression checks |

## Gate anti-patterns

| Anti-pattern | Symptom | Fix |
|--------------|---------|-----|
| Rubber-stamp gate | Reviewer approves >95% without changes | Remove gate or make it agent-only |
| Bottleneck gate | PR queue grows faster than review capacity | Automate with agent pre-review, escalate only exceptions |
| Duplicate gate | Same check done by CI and human reviewer | Remove human check where CI is authoritative |
| Late-stage gate | Issues caught at deploy that could be caught at PR | Shift check earlier (fail fast) |
| Missing gate | High-risk changes ship with no human review | Add targeted approval for risk class |

## Gate positioning by risk class

| Risk class | Recommended gates | Rationale |
|------------|-------------------|-----------|
| Low (utilities, internal tools) | CI only | Automated checks sufficient; human review is waste |
| Medium (business logic, APIs) | CI + agent review | Agent catches intent drift; human escalation on ambiguity |
| High (payments, auth, data) | CI + agent review + human approval | Human judgment needed for blast radius |
| Critical (safety, security, compliance) | CI + agent review + domain expert approval | Regulatory or safety obligation |

## Assessing current gate placement

For each existing review/approval checkpoint, evaluate:

| Dimension | Question |
|-----------|----------|
| Value | Does this gate catch issues that no automated check can? |
| Position | Is this gate at the earliest point where the check is meaningful? |
| Throughput | Can this gate handle the volume of agent-generated changes? |
| Scope | Is the gate scoped to the right risk level (not too broad, not too narrow)? |
| Feedback | Does rejection at this gate produce actionable feedback for the agent? |

## Consolidation decision matrix

| Current state | Recommendation |
|---------------|----------------|
| Many low-value human gates, low rejection rate | Consolidate to three-checkpoint model |
| Single gate at merge, high rejection rate | Add earlier spec review gate to catch issues sooner |
| No human gates, high revert rate | Add ship review for high-risk components |
| Human reviews everything equally | Segment by risk class, automate low-risk |
