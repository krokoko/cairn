# Verification report: synthetic retry service

## Evidence Scope

**Source revision**: fixture-r2
**Assessment date**: 2026-10-11
**Inspected scope**: retry model, assertions, local campaign receipt
**Evidence basis**: Local execution artifact inspected; provider environment unavailable.

## Evidence Ledger

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| Retry preserves job identity | campaign-r2 | local double | run_inspected | completed | no_counterexample_found | 20 sequences; provider fidelity unverified |

## Verification Maturity

Tier 2 demonstrated for the local suite; critical provider evidence is missing.

## Component Breakdown

Retry core is stateful and affects billing; provider adapter needs separate evidence.

## Bug-Surface Classification

Class C: retries and interruption points affect state transitions.

## Missing Oracles

No inspected provider behavior comparison establishes double fidelity.

## Exactness Analysis

Sampled local sequences do not establish all schedules or deployed behavior.

## Human Review Requirements

A domain reviewer must confirm the idempotency window and conflicting-payload rule.

## Autonomy Candidates

Only changes within the reviewed local model are candidates for bounded iteration.

## Feedback Loop Completeness

The local receipt is inspectable; provider feedback is unknown.

## Workflow Gate Assessment

CI configuration exists; hosting-platform protection was not inspectable.

## Shift-Left Assessment

The local campaign can run before integration; provider qualification has a separate cost.

## Documentation Verification

Requirement r2 is linked to the local assertion; example documentation is not executed.

## AgentOps Telemetry

Silent duplicate-charge detection has not been inspected.

## Requirement Traceability

The local claim is linked and executed; provider scope remains partial.

## Verification Debt

Qualify the double against supported provider scenarios before widening the autonomy scope.
