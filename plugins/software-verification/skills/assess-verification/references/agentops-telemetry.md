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

## Four telemetry streams

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
