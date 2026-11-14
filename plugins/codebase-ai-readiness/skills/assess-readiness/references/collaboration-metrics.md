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
| Maintained lessons after corrections | `AGENTS.md` / `CLAUDE.md` history of useful edits and obsolete-rule removal |

## Recommendations by autonomy level

| Level | Minimum collaboration practice |
|-------|--------------------------------|
| L0-L1 | Optional; focus on README and basic docs |
| L2 | Track iteration cycles informally on agent PRs |
| L3 | Estimate first-pass acceptance monthly; add rules after repeated corrections |
| L4 | Track comparable bounded-task outcomes and rework; use reviewed evidence for merge decisions |
| L5 | Track all three metrics; feed learnings into specs, tests, and instruction files |

## Report output

Always include a **Collaboration effectiveness** section with:

1. **Current state**: estimated or "not measured" for each metric
2. **Infrastructure**: which measurement enablers exist or are missing
3. **Recommendations**: 2-4 concrete steps to start or improve tracking
4. **Link to roadmap**: actions that improve both compound engineering and collaboration

## Representative maintenance outcomes

Distinguish concrete rules, diagnostic signals and observed outcomes. Dependency violations
can verify a configured rule; complexity, coverage and change coupling identify areas to
investigate. Neither proves that a future change will be easy.

Where useful, inspect or propose a realistic task such as adding an adapter through documented
extension points. An assessment may recommend the exercise without performing an unrequested
implementation change. Record:

| Field | What to retain |
|-------|----------------|
| Task and scope | Requirement, affected surface, baseline revision and expected extension point |
| Change spread | Expected vs unexpected files/modules changed; dependency direction preserved or violated |
| Effort | Observed time/correction cycles and measurement limits |
| Outcome | Relevant completed checks, regressions, boundary violations and unresolved friction |

Use allowed and deliberately forbidden examples to qualify architecture checks, including
supported indirect imports, parser coverage and exceptions. A shorter file or lower complexity
score accompanied by more cycles is not demonstrated improvement. Generalize only to comparable
tasks; distinguish measured outcomes from estimates and `not measured`.

## Alignment with autonomy level

After scoring collaboration infrastructure, check `references/autonomy-levels.md` **Alignment
note**. If collaboration signals are strong but the codebase maps to L1–L2, flag **practices
ahead of codebase** in the report. If the codebase maps to L3+ but infrastructure is absent,
flag **codebase ahead of practices**.
