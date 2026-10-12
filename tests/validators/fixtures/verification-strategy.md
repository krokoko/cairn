# Verification strategy: synthetic retry service

## Evidence Scope

**Source revision**: fixture-r2
**Assessment date**: 2026-10-11
**Inspected scope**: local retry assessment
**Evidence basis**: Assessment artifact inspected; proposed campaigns have not run.

## Evidence Ledger

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| Provider retry compatibility | provider campaign configuration r2 | staging | configuration_only | not_run | not_run | Credentials unavailable; no provider conclusion |

## Component Strategies

Keep the local retry campaign and add scoped provider-fidelity checks.

## Oracle Strategy

Review identity, time-window, and rejection assertions independently of implementation helpers.

## Evidence Requirements

| Claim / requirement | Oracle / review owner | Required evidence / environment | Completion / acceptance criteria | Scope / limits |
|---------------------|-----------------------|---------------------------------|----------------------------------|----------------|
| REQ-RETRY revision 2 | Billing owner reviews independent identity assertion | Proposed staging receipt bound to source, assertion, helper and provider versions | All inventoried scenarios complete; retain negative controls and deviations | Applies to declared provider version and idempotency window |

## Evidence Pipeline

Promotion depends on current completed evidence and scoped review, with tested rollback.

## Verification Cost Tiers

Local unit checks on edits; retry sequences before merge; provider campaigns before release.

## Shift-Left Recommendations

Run the fast local sequence checks before PR review.

## Feedback Loop Improvements

Retain native runner reports in fresh per-run directories and compare expected test inventory.

## Workflow Gate Optimization

Keep domain review for changed billing semantics.

## Architecture Fitness Functions

Qualify the forbidden domain-to-provider import rule with allowed and rejected examples.

## Eval Framework

Evaluate a duplicate retry, conflicting payload, interruption, and independent adapter addition.

## Generator-Evaluator Recommendations

Use independent expected values; agreement among agents does not establish correctness.

## Documentation Verification

Check that examples cite the current time-window requirement.

## Requirement Traceability

Keep link completeness, execution completeness, and semantic review separate.

## Implementation Roadmap

Review the bounded claim, qualify the double, then run the proposed staging campaign.
