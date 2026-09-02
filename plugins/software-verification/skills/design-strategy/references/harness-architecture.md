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

## Four-rail coverage

The five lanes above are *method categories*. They are orthogonal to a second question: does the
stack cover the whole lifecycle? A sound base stack has **one rail in each of four positions**:

| Rail | Position | Catches | Example |
|------|----------|---------|---------|
| Pre-merge | Before code lands | Logic/regression bugs | Property tests, unit tests, types |
| Boundary | At interfaces | Integration/contract breaks | Contract tests, schema compatibility |
| Production-proximate | Near/in production | What labs miss | Shadow, canary, replay, SLOs |
| Evidence | After verdict | Unverifiable/untrusted delivery | Signed attestation (in-toto/SLSA) |

Use this as a coverage checklist: a stack missing a rail has a blind spot regardless of how many
lanes it exercises.

## Evidence rail and attestations

The Evidence Store should not only retain records — for high/critical risk it should emit **signed,
portable attestations** (in-toto attestation format, SLSA provenance levels, signed via
Sigstore/Cosign or GitHub artifact attestations). This lets downstream and cross-team consumers
trust *what ran, on which commit, with which verdict* without rerunning the harness. Attestation is
evidence packaging — it proves the process happened, not that the output is semantically correct —
so it complements oracles, never replaces them.

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

**Mandatory vs objectives:** promotion policy applies the rule in `candidate-selection-policy.md`
(canonical) — hard gates first, ranking metrics only among passing candidates.

## Assurance evidence model (claims → evidence)

Extend the conceptual schemas above into a **claim-centric evidence graph**:

```yaml
claim:
  id: PAY-INV-001
  statement: "same request_id cannot create two payments"
requirement:
  id: REQ-PAY-042
component:
  path: src/payments/
change:
  commit: abc123
oracle:
  type: temporal
  authority: approved-spec
  agent_mutable: false
  integrity: sound
  spec_hash: 8c93...
verification:
  tool: quint
  mode: model-check
  result: pass
evidence:
  states_explored: 42118
  artifact: verification/quint-result.json
search:
  strategy: best-of-n
  candidates_evaluated: 8
  selected_candidate: candidate-6
attestation:
  format: in-toto
  signer: sigstore
```

JSON Schema: `schemas/verification-evidence.schema.json` (when implementing structured evidence).

Attestation proves **what ran**; oracle + verifier prove **what was established**. Both are required
for L5 promotion decisions.

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
