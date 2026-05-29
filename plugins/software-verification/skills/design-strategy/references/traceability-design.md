# Traceability Strategy Design

How to make the requirement → criterion → test → code → result trace a living artifact the
pipeline enforces, rather than a spreadsheet maintained by hand. Load
`../../assess-verification/references/traceability-model.md` for the RTM model and maturity levels.

## Design progression by current level

| Current level | Recommended next step | Tools / mechanism |
|---------------|----------------------|-------------------|
| 0 (intent in chat only) | Capture requirements as files with stable IDs | `docs/requirements/`, EARS statements, issue templates |
| 1 (PR↔issue only) | Make acceptance criteria executable | Gherkin + Cucumber/Behave/SpecFlow; tag scenarios with requirement IDs |
| 2 (executable criteria) | Generate a requirement-coverage report in CI | Map criterion IDs → tests; fail build on uncovered criterion |
| 3 (living RTM) | Enforce bidirectional check at the gate | Block merge on untraced code or uncovered requirement |

## Linking conventions

- **Requirement IDs**: stable, referenceable (`REQ-123`, story key). Put them in spec files and issues.
- **Criterion → test**: tag tests or Gherkin scenarios with the requirement ID (`@REQ-123`,
  test name prefix, or a `traceability:` annotation). A convention a script can parse beats prose.
- **Code → requirement**: PR body references the issue; commit trailer (`Refs: REQ-123`) for durability.
- **Result**: CI publishes which criteria passed, surfacing the full chain per run.

## Pipeline enforcement (the gate)

The RTM becomes deterministic only when the pipeline checks it. Recommend a CI step that:

1. Parses requirement IDs from spec/issue sources.
2. Parses requirement tags from tests and Gherkin scenarios.
3. Reports two gap lists: **uncovered requirements** (no test) and **untraced changes** (code/PR
   with no requirement). Fail or warn per risk class.

| Risk class | Traceability gate |
|------------|-------------------|
| Low | Warn on missing PR↔issue link |
| Medium | Require PR↔issue link; warn on uncovered criterion |
| High / Critical | Block merge on uncovered criterion or untraced change; human ship-review confirms intent |

## Avoiding the agent-verifying-agents trap

An agent building the matrix by reading artifacts reintroduces indeterminism. Keep the *check*
deterministic (a script parsing IDs/tags), and reserve the agent for the *judgment* step: comparing
implementation to intent where the trace is ambiguous, escalating to a human on low confidence.
This preserves the human's role at the final ship-review after all automated analysis.
