# AI smell gate report: synthetic service

## Evidence Scope

**Source revision**: fixture-r2
**Assessment date**: 2026-10-11
**Inspected scope**: lint configuration and local lint receipt
**Evidence basis**: Selected rules and one completed run inspected.

## Evidence Ledger

| Claim / check | Artifact / revision | Environment | Observation | Execution | Conclusion | Limits |
|---------------|---------------------|-------------|-------------|-----------|------------|--------|
| Configured unused imports rule | lint-r2 | local analyzer | run_inspected | completed | no_counterexample_found | Supported Python imports only; no claim of complete smell detection |

## Gate Coverage Summary

One configured detection capability has inspected execution evidence.

## Coverage Matrix

Unused imports have a lint rule; no evidence of semantic assertion quality was inspected.

## Git History Hygiene

History was unavailable in this fixture.

## Gap Analysis

Known-bad qualification of the selected rule is missing.

## Recommendations

Run allowed and forbidden import controls before treating absence of findings as meaningful.

## Human Review Heuristics

Review domain intent, coupling, and scope; lint does not establish these properties.
