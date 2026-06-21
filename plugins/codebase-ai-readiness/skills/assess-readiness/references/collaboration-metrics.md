# Collaboration Effectiveness Metrics

## Why these matter

A codebase can score well on structure and CI while agents still waste cycles in
generate-fix-regenerate loops. **Collaboration effectiveness** measures whether human–agent
work is improving over time—not only whether the repo is technically checkable.

## Core metrics

| Metric | Definition | How to assess without tooling |
|--------|------------|-------------------------------|
| **First-pass acceptance** | Share of agent-produced changes (PRs, patches, files) accepted with no substantive rework | Ask team or sample last 10 agent-assisted PRs; note % merged with minor vs major follow-up edits |
| **Iteration cycles per task** | Average agent↔human correction rounds before merge | Count review comments or regenerate rounds on recent agent tasks |
| **Post-merge rework** | Fixes or reverts within 7 days of agent-assisted merges | Check recent git history for hotfixes on agent-touched areas |

## Infrastructure signals (enables measurement)

| Signal | Where to check |
|--------|----------------|
| PR templates requiring agent/task metadata | `.github/pull_request_template.md`, similar |
| Labels for agent-assisted work | Issue/PR label configs |
| Documented review rubric for agents | `AGENTS.md`, `CONTRIBUTING.md`, review skill or checklist |
| Retrospective or learning docs updated after reviews | `docs/learnings/`, workflow artifact dirs |
| Instruction file growth after corrections | `AGENTS.md` / `CLAUDE.md` git history or rule count |

## Recommendations by autonomy level

| Level | Minimum collaboration practice |
|-------|--------------------------------|
| L0-L1 | Optional; focus on README and basic docs |
| L2 | Track iteration cycles informally on agent PRs |
| L3 | Estimate first-pass acceptance monthly; add rules after repeated corrections |
| L4 | Target first-pass acceptance ≥50% on bounded tasks; gate merges on CI not re-prompting |
| L5 | Track all three metrics; feed learnings into specs, tests, and instruction files |

## Report output

Always include a **Collaboration effectiveness** section with:

1. **Current state**: estimated or "not measured" for each metric
2. **Infrastructure**: which measurement enablers exist or are missing
3. **Recommendations**: 2-4 concrete steps to start or improve tracking
4. **Link to roadmap**: actions that improve both compound engineering and collaboration

## Alignment with autonomy level

After scoring collaboration infrastructure, check `references/autonomy-levels.md` **Alignment
note**. If collaboration signals are strong but the codebase maps to L1–L2, flag **practices
ahead of codebase** in the report. If the codebase maps to L3+ but infrastructure is absent,
flag **codebase ahead of practices**.
