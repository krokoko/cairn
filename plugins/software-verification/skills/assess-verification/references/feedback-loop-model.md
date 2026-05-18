# Feedback Loop Completeness Model

## What makes a verification output agent-consumable

For agents to self-correct based on verification results, outputs must be:
- **Structured**: Machine-parseable format (JSON, SARIF, JUnit XML), not just prose logs
- **Attributable**: Each failure linked to a specific file, line, component, or commit
- **Actionable**: Contains enough context for an agent to determine what to fix
- **Routable**: Results flow back into agent execution, not only to human dashboards

## Feedback loop maturity levels

| Level | Name | Description |
|-------|------|-------------|
| 0 | Terminal | Results exist only in logs or dashboards; no programmatic access |
| 1 | Readable | Structured output exists (JUnit XML, JSON) but not consumed by agents |
| 2 | Routable | CI results are programmatically accessible and can trigger agent re-runs |
| 3 | Closed-loop | Agent receives structured failure, diagnoses, fixes, and re-validates autonomously |

## Assessment indicators by level

### Level 0 indicators
- CI output is plain text logs only
- Test results visible only in web UI (GitHub Actions summary, Jenkins Blue Ocean)
- No structured report artifacts (no JUnit XML, no SARIF, no JSON summaries)

### Level 1 indicators
- JUnit XML or JSON test reports generated
- SARIF or structured lint output produced
- Coverage reports in machine-readable format (lcov, cobertura)
- Reports stored as CI artifacts but not consumed downstream

### Level 2 indicators
- CI status checks accessible via API (GitHub Checks API, GitLab pipelines API)
- Structured failure data retrievable programmatically per commit/PR
- Webhook or event system can trigger re-execution on failure
- Error messages include file paths and line numbers

### Level 3 indicators
- Agent receives structured failure context automatically after CI run
- Failure attribution maps errors to specific changes in the PR
- Agent can iterate (fix + re-push) without human intervention
- Feedback latency is under 10 minutes from push to agent re-execution

## Key dimensions to assess

| Dimension | Question |
|-----------|----------|
| Output format | Are verification results in structured, parseable formats? |
| Attribution | Can failures be traced to specific files/lines/changes? |
| Accessibility | Can agents retrieve results programmatically (API, artifacts)? |
| Routing | Do failures trigger agent re-execution or only notify humans? |
| Latency | How fast does the feedback reach the agent after a push? |
| Context sufficiency | Does the failure output contain enough info to diagnose and fix? |
| Observability access | Can agents query logs, metrics, traces directly (LogQL, PromQL, TraceQL)? |
| Ephemeral environments | Can agents run isolated app instances with their own observability stack? |

## Agent-accessible observability indicators

| Signal | Where to check |
|--------|----------------|
| Local observability stack | Docker Compose with Loki/Prometheus/Tempo, Vector, or similar per-worktree |
| Queryable logs | LogQL, structured JSON logs with API access |
| Queryable metrics | PromQL/metrics API accessible to CI or agent runtime |
| Queryable traces | TraceQL or span search API available to agents |
| Per-worktree isolation | App bootable per git worktree with isolated telemetry |
