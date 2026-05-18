# AgentOps Telemetry

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

## Assessment criteria

### Mature AgentOps telemetry (score indicators)

**Level 3 — Full observability**
- All four telemetry streams captured
- Dashboards or reports available for verification performance
- Alerting on verification regressions (declining pass rates, increasing iterations)
- Cost tracking per task type
- Trend analysis over time

**Level 2 — Partial observability**
- CI timing and pass/fail rates visible
- Some agent trace logging
- Manual cost tracking (checking bills)
- No automated alerting on verification performance

**Level 1 — Minimal observability**
- CI pass/fail visible per run
- No trajectory or cost tracking
- No quality trend analysis
- Verification effectiveness unknown

**Level 0 — No observability**
- CI results visible only to the actor who triggered them
- No tracking of agent behavior or verification consumption
- No cost visibility
- No quality measurement

## Key indicators to search for

| Indicator | Where to find it |
|-----------|------------------|
| Agent trace/logging config | Agent config files, observability setup |
| CI timing visibility | CI platform dashboards, timing artifacts |
| Cost tracking | Billing alerts, usage dashboards, budget configs |
| Quality metrics | Coverage trends, defect tracking, flake dashboards |
| Alerting on verification | Alert configs, monitoring rules, SLO definitions |
| Structured verification output | JUnit XML, SARIF, JSON reports with timing data |

## Recommendations by gap

| Current state | Recommended action |
|---------------|-------------------|
| No timing data | Add CI step timing; log verification tool execution time |
| No iteration tracking | Enable agent trace logging; count tool calls per session |
| No quality trends | Track coverage/pass-rate over time; add flake detection |
| No cost visibility | Tag CI costs per workflow; track token usage per task type |
| No alerting | Add alerts for declining pass rates, increasing CI time, cost spikes |
