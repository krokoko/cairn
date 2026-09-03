# Scoring Rubric

## Category weights

| Category | Weight | Rationale |
|----------|--------|-----------|
| Structure and modularity | 0.10 | Agents need clear boundaries to scope changes |
| Documentation | 0.06 | Context for understanding intent |
| Testable boundaries | 0.13 | Tests are the primary verification mechanism |
| CI reliability | 0.10 | Unreliable CI blocks autonomous iteration |
| Typing strength | 0.07 | Types prevent entire bug classes cheaply |
| Deterministic environment and deployment | 0.07 | Agents need reproducible environments and codified deployment |
| Architecture decisions | 0.04 | Helps agents understand constraints |
| Machine-readable intent | 0.10 | Enables automated verification of correctness |
| Progressive context disclosure | 0.04 | Agents discover context through layered docs |
| Hidden state and magic | 0.04 | Implicit state causes agent failures |
| Repository-scale reasoning | 0.04 | Consistent naming enables retrieval and reasoning |
| Failure mode legibility | 0.04 | Legible errors enable agent self-correction |
| Feedforward surfaces | 0.09 | Prevents errors proactively; reduces agent iteration count |
| Compound engineering readiness | 0.04 | Enables knowledge accumulation across sessions |
| Context engineering friendliness | 0.04 | Codebase structure supports effective context management |

## Signal verdicts

Every signal row in `category-definitions.md`, `category-definitions-agent.md`, and the
category-specific references is a binary check, not an impression. Record one verdict per signal:

| Verdict | Meaning | Evidence required |
|---------|---------|-------------------|
| PASS | Present and functional | File path, config key, or command output that proves it |
| FAIL | Absent, broken, or present only on paper | What was searched and not found, or why the presence is trivial |
| N/A | Does not apply to this kind of codebase | One-line reason (e.g. "library, not a deployed service") |
| NOT INSPECTABLE | Needs access this run does not have (git history, hosting API) | What was needed |

Rules:

- Every verdict carries an evidence string naming a concrete file, command, or search. "Looks fine" is not evidence.
- N/A means inapplicable, never "did not check". Typical N/A: IaC, health checks, tracing, alerting, and
  rollout signals for libraries and CLIs; monorepo signals for single-app repos; database signals without persistence.
- A signal that exists only on paper (empty test dir, linter configured but never run) is FAIL. Note the partial evidence.
- NOT INSPECTABLE signals are excluded from the denominator and listed under Blockers as "verify with access".

## Category score

```
category_score = round(100 * PASS / (PASS + FAIL))
```

N/A and NOT INSPECTABLE do not count. A category with zero applicable signals is dropped and its
weight is redistributed proportionally across the remaining categories.

Interpretation bands (for reading a score, not for assigning one):

- 0-25 absent or minimal
- 26-50 basic, inconsistent
- 51-75 good, mostly consistent
- 76-100 excellent, systematic

## Monorepos

App-scoped signals (linter configured, unit tests exist and run, build command documented, env
template) are checked per application. Record `n/m apps` in the evidence; the signal is PASS only
when every app passes. Repo-scoped signals (CODEOWNERS, branch protection, instruction file, CI
workflow) are checked once.

## Overall score

```
overall_score = sum(category_score[i] * weight[i]) / sum(weight[i])   over applicable categories
```

Round to nearest integer. Range 0-100. The overall score is informative; the autonomy level is set
by level gates (see `autonomy-levels.md`).

## Grounding on a prior report

If `readiness-report.md` already exists, read its Signal evidence table before assessing. Keep a
prior verdict unless the evidence changed (file added or removed, config changed, git history moved).
Record every changed verdict with old and new evidence in the report's **Changes since last
assessment** section. Re-deriving every verdict from scratch reintroduces run-to-run drift.
