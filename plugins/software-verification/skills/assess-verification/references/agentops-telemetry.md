# AgentOps Telemetry

Load `agentops-telemetry-assessment.md` for maturity scoring, indicators, and recommendations.

## Definition

AgentOps telemetry tracks whether verification outputs are observable, measurable, and
actionable at the operational level. It applies DevOps observability discipline to
agentic workflows — you cannot improve what you cannot measure.

## Why verification needs operational telemetry

Verification infrastructure produces evidence (test results, type errors, lint findings).
But without operational visibility into *how agents consume and respond to that evidence*,
teams cannot:
- Detect verification regressions (agent ignoring test failures)
- Identify bottlenecks (slow checks blocking iteration)
- Measure improvement (is the verification strategy working?)
- Cost-optimize (which checks provide signal vs noise?)

## Five telemetry streams

### 1. Trajectory telemetry

The ordered sequence of agent actions, tool calls, and verification results within
a single task.

| Signal | What it reveals | Where to capture |
|--------|----------------|------------------|
| Tool call sequence | Agent's verification behavior | Agent trace logs |
| Iteration count per task | Steering loop convergence speed | Agent session metadata |
| Verification calls per change | How often agent checks its work | Tool call counts |
| Failure-then-fix sequences | Self-correction effectiveness | Trace analysis |

### 2. Cost telemetry

Resource consumption of verification activities.

| Signal | What it reveals | Where to capture |
|--------|----------------|------------------|
| Time per verification step | Bottleneck identification | CI timing, tool execution logs |
| Tokens consumed in verification loops | Cost of self-correction | Agent billing/usage data |
| CI minutes per PR | Infrastructure cost | CI platform metrics |
| Model calls for LLM-as-Judge | Eval cost scaling | API usage logs |

### 3. Quality telemetry

Effectiveness of verification at catching and preventing issues.

| Signal | What it reveals | Where to capture |
|--------|----------------|------------------|
| First-pass acceptance rate | Feedforward effectiveness | PR review data, agent session logs |
| Post-merge defect rate | Verification gap detection | Issue tracker, incident data |
| Flake rate | CI reliability | CI history, test result trends |
| False positive rate | Signal vs noise ratio | Suppressed/overridden findings |
| Mutation kill rate | Test adequacy | Mutation testing reports |

### 4. Autonomy compliance telemetry

Whether agents operate within their designated verification boundaries.

| Signal | What it reveals | Where to capture |
|--------|----------------|------------------|
| Checks skipped or bypassed | Governance compliance | CI audit logs, agent traces |
| Human override rate | Gate calibration | Approval system logs |
| Escalation frequency | Autonomy tier fit | Agent decision logs |
| Policy violation count | Boundary enforcement | Runtime governance logs |

### 5. Domain telemetry

Business-meaningful outcomes instrumented as first-class signals — not derived from infrastructure
metrics. Technical telemetry answers "is the software running?"; domain telemetry answers "is the
software doing its job?". This is the stream that catches **silent failures**: an agent can refactor
code, pass every test, and return `200 OK` at normal latency while quietly breaking domain logic
(e.g. a serialization bug that drops discount codes). Only a metric that knows what the *outcome*
should look like exposes it.

| Signal | What it reveals | Where to capture |
|--------|----------------|------------------|
| Business-outcome rates | Whether behavior is correct in production | Domain event instrumentation (checkout completion, coupon redemption, signup success) |
| Outcome value distributions | Silent drift in computed results | Metrics on amounts/counts (avg order value, items per cart) with expected ranges |
| Conversion/funnel steps | Where real flows break despite green infra | Funnel/event analytics |
| Anomaly thresholds on domain metrics | Divergence from intent → rollback trigger | Alerting on domain-metric deltas post-deploy |

For autonomous change, domain telemetry is the agent's **production oracle** for behavior no unit
test covers: it is what makes automated rollback (an L5 prerequisite) trustworthy. Flag its absence
as a critical gap for any codebase aiming at L4-L5 autonomy — without it, silent regressions ship
undetected.
