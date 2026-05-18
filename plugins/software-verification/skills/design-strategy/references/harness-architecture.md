# Harness Architecture

## Five-lane evidence pipeline

A verification harness is an evidence pipeline, not a bag of scripts. Each lane runs
independently and produces uniform evidence records.

| Lane | What it checks | Key tools |
|------|---------------|-----------|
| Static | Pre-execution: types, linting, abstract interpretation | mypy, ESLint, clippy, Semgrep |
| Dynamic | Sampled execution: unit, integration, system, regression | pytest, Jest, go test |
| Generative | Broad exploration: property tests, fuzzing, sanitizers | Hypothesis, libFuzzer, ASan |
| Formal | Machine-checked: model checking, SMT, deductive proofs | TLA+/TLC, Kani, Dafny, Z3 |
| Operational | Real-world: shadow, canary, chaos, runtime verification | Argo Rollouts, Chaos Monkey |

All lanes feed an **Evidence Store** and then a **Scoring and Policy Engine** that
decides: may this merge, may this deploy, must a human approve?

## Core interface schemas

### Spec pack

Component ID, invariants, pre/postconditions, non-functional budgets, risk class,
determinism class. Makes semantics explicit and shareable across lanes.

### Candidate manifest

Commit or model version, build flags, dependency lock, feature flags, environment
assumptions. Keeps validation reproducible and attributable.

### Evidence record

Method, tool, property, verdict, artifact hash, runtime, assumptions, links to
trace/crash/proof. Lets policy engines reason over heterogeneous evidence.

### Replay label

Scenario ID, world snapshot, oracle or ground truth, allowed tolerance, segmentation
tags. Turns incidents and historical failures into durable regression assets.

### Promotion policy

Required checks by risk class, rollback policy, approval thresholds, low-confidence
escalation rules. Converts evidence into action consistently.

## Harness metrics

### Fast-loop correctness
Unit/integration pass rate, regression replay pass rate, property-test falsification
rate, flake rate, contract violation count.

### Input exploration quality
Unique crash count, sanitizer findings, corpus growth, shrinking effectiveness.

### Formal evidence quality
Proof obligations discharged, counterexample density, bound depth reached, state-space
coverage indicators, solver timeouts.

### Operational equivalence
Shadow mismatch rate, canary error-budget burn, latency/throughput deltas, rollback
frequency, runtime-monitor violations.

### Harness health
Label freshness, scenario coverage by segment, human override rate, evidence
turnaround time (commit to decision).

## Key design principle

Each lane must produce a **uniform evidence record**: what property was checked, with
which tool, on which artifact, under which assumptions, resulting in which verdict.
Incomplete invariants can produce automated confidence in incorrect behavior, so
production telemetry and replay must always feed back into the pipeline.
