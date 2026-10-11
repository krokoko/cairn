# AI Readiness Assessment
## Evidence Scope
**Source revision**: roadmap-stale-baseline-r1
**Assessment date**: 2026-10-01
**Inspected scope**: core and payment adapter against REQ-TOTAL/1 and REQ-PAY/1
**Evidence basis**: earlier local and provider receipts; exported protections at r1
## Overall Score
Provisional score: 94/100; assessed weight: 1.0. Rubric: readiness/2.
## Recommended Autonomy
L4 for both assessed surfaces at r1; next target L5.
## Surface Autonomy
| Surface | Provisional level | Prerequisite ceiling | Recommended level | Rationale |
|---------|-------------------|----------------------|-------------------|-----------|
| core | L4 | L4 | L4 | Reviewed sum contract and repeatable local runs |
| payment adapter | L4 | L4 | L4 | Provider retry evidence for REQ-PAY/1 five-minute window |
## Autonomy Prerequisites
The payment adapter had no automatic recovery at r1. Its L5 recovery gate was missing.
Other provider evidence and requirement review applied to the five-minute contract only.
## Category Scores
Test infrastructure 90; CI 95; requirements 95; compound engineering not measured.
## Blockers
Automatic recovery/escalation had not been exercised. Collaboration effectiveness and
session context durability had not been measured.
