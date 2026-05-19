# AgentOps Telemetry (Assessment)

Continues `agentops-telemetry.md`. Maturity scoring, indicators, and recommendations.

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
