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

Applicable lanes feed an **Evidence Store** and a **Policy Engine** that evaluates the configured
merge/release criteria. Scores do not grant action permissions; preserve existing authorization rules.

## Four-rail coverage

The five lanes above are *method categories*. They are orthogonal to a second question: does the
stack cover the relevant lifecycle? Review these four positions and justify inapplicable rails:

| Rail | Position | Catches | Example |
|------|----------|---------|---------|
| Pre-merge | Before code lands | Logic/regression bugs | Property tests, unit tests, types |
| Boundary | At interfaces | Integration/contract breaks | Contract tests, schema compatibility |
| Production-proximate | Near/in production | What labs miss | Shadow, canary, replay, SLOs |
| Evidence | After verdict | Unverifiable/untrusted delivery | Signed attestation (in-toto/SLSA) |

Use this as a coverage checklist. A local library may not have a deployed service; record the
consumer boundary and applicable release evidence instead of inventing a production gate.

## Evidence rail and attestations

Use **signed, portable attestations** when downstream provenance or release policy calls for them
(in-toto attestation format, SLSA provenance levels, signed via
Sigstore/Cosign or GitHub artifact attestations). This lets downstream and cross-team consumers
authenticate the issuer's recorded source, process, and verdict. This depends on signer and build
trust; signing does not establish that assertions match intent or strengthen the result's semantics.

## Core interface schemas

### Spec pack

Component ID, invariants, pre/postconditions, non-functional budgets, risk class,
determinism class. Makes semantics explicit and shareable across lanes.

### Candidate manifest

Commit or model version, build flags, dependency lock, feature flags, environment
assumptions. Keeps validation reproducible and attributable.

### Evidence record

Use `../../assess-verification/references/evidence-semantics.md` for observation, execution, and
conclusion states. Retain requirement/claim and oracle revisions; semantic-review identity; source
commit plus relevant uncommitted changes; environment/dependency fidelity; tool version/configuration;
bounds/campaign size/exclusions; completion; and links to reports, traces, or proof artifacts.

Use fresh run directories and an expected inventory. Missing/skipped/interrupted results remain
visible. A configured tool is not an inspected run; positive conclusions require `run_inspected`
and `completed`, with a conclusion appropriate to the method and supported scope.

### Replay label

Scenario ID, world snapshot, oracle or ground truth, allowed tolerance, segmentation
tags. Turns incidents and historical failures into durable regression assets.

### Promotion policy

Required scoped evidence, unresolved gaps, rollback policy where applicable, existing authorization
requirements, and escalation rules. A monitored violation needs a separate enforcement mechanism.

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

Each applicable lane produces a **uniform evidence record** without flattening different conclusions
into one green status. For operated systems, feed representative incidents and observed outcomes
back into the oracle review process. Telemetry and provenance alone are not behavioral correctness.
