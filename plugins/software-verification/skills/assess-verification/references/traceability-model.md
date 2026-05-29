# Requirement Traceability Model

The chain from intent to evidence: **requirement → acceptance criterion → test → code → result**.
When agents produce dozens of PRs per day, this trace is the only deterministic way to answer
"does this change do what the business asked?" and "why does this code exist?". Code can compile,
pass every test, and respect every lint rule, yet still be the *wrong* code — this is **intent drift**.

## Why it matters for autonomy

Technical checks (tests, types, lint, security) prove the code is *correct*. They cannot prove it
is the *right* code. Detecting intent drift requires comparing the implementation against the
original intent. An AI reviewer reading the same spec as the AI developer is no more reliable than
the developer — both interpret, neither enforces. A traceability matrix gives the reviewer a
structured checklist to verify against, turning a subjective review into a deterministic gap check.

## The Requirement Traceability Matrix (RTM)

Not a spreadsheet maintained by a project manager, but a living artifact enforced by the pipeline.

| Column | Source | Question answered |
|--------|--------|-------------------|
| Requirement / story | `docs/requirements/`, issues, EARS statements | What was asked |
| Acceptance criterion | EARS / Gherkin scenarios | How we know it is done |
| Test(s) | Test files, Gherkin step defs | What proves it |
| Code / module | Implementation files | Where it lives |
| Result | CI run, coverage report | Whether it passes |

## Three properties the RTM enforces

| Property | Failure it catches | Signal of absence |
|----------|--------------------|--------------------|
| Scope verification | Agent silently adds unrequested logic, or misses a requirement | Code with no upstream requirement; requirement with no code |
| Impact analysis | Requirement changes but affected tests/files unknown | No mapping from requirement to tests and files |
| Test sufficiency | 90% coverage still misses an entire requirement | Requirement with no dedicated test |

## Assessment signals

Search for evidence that the trace exists and is maintained:

- **Requirement anchors**: `docs/requirements/`, `docs/specs/`, structured issues, EARS statements
- **Criterion → test links**: Gherkin `.feature` files with step definitions, test names citing requirement IDs
- **PR → issue links**: PRs reference an issue/requirement (`Closes #`, `Refs`); flag PRs with none
- **Coverage-by-requirement**: any report mapping requirements to tests, not just lines to tests
- **Tooling**: SDD frameworks (Kiro, SpecKit, OpenSpec) for requirements→design→tasks; BMAD test
  architect `trace` workflow; graph-based AI-DLC `VALIDATES` edges; BDD linking criteria to scenarios

## Maturity levels (0-3)

| Level | State |
|-------|-------|
| 0 | No link from requirements to code or tests; intent lives only in chat/PR descriptions |
| 1 | PRs reference issues, but no criterion → test mapping; trace is manual and partial |
| 2 | Acceptance criteria exist as executable specs (Gherkin/BDD); tests link to criteria by convention |
| 3 | Living RTM the pipeline can check: every criterion maps to a test, every change to a requirement |

## The gap today

No mainstream tool answers, deterministically: *"For every acceptance criterion, show me the test
that proves it. For every code change, show me the requirement that justifies it."* Agents building
the matrix by reading artifacts reintroduce the indeterminism problem (an agent verifying agents).
Flag Level 0-1 as the highest-leverage gap for business-level autonomy: without it, business
validation stays fully human and cannot keep pace with agent throughput.
