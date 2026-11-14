# Traceability Strategy Design

Connect approved requirement → bounded claim → scenario/property → executed check → versioned
evidence → reviewed decision. Load `../../assess-verification/references/traceability-model.md`
for assessment and `../../assess-verification/references/evidence-semantics.md` for result states.

## Three separate obligations

| Obligation | Mechanism | Limit |
|------------|-----------|-------|
| Links | Parse requirement IDs, check IDs, and change references | A link does not establish relevance |
| Execution | Compare expected check inventory with current runner reports | A declared scenario or skipped test is not an executed check |
| Meaning | Review assertions, conditions, exclusions, and approved claim together | A fresh run cannot establish current business intent |

## Design progression

| Current gap | Next step | Completion evidence |
|-------------|-----------|---------------------|
| Intent only in chat | Version requirements with stable IDs and acceptance criteria | Reviewable bounded claims |
| PR/issue links only | Map claims to ordinary test annotations, contracts, or executable scenarios | Parsed links and explicit unmapped claims |
| Mappings without runs | Ingest runner-native JUnit or equivalent results in fresh run directories | Expected vs executed inventory with missing/skipped checks |
| Runs without scope | Bind source/oracle/environment revisions, partial coverage, and exclusions | Current scoped evidence ledger |
| Unreviewed or stale relationships | Review assertion-to-claim sufficiency and invalidate on changes | Named review owner, reviewed revisions, remaining gaps |

Gherkin is one representation. A scenario declaration with unexecuted steps is not acceptance evidence.

## Linking and execution conventions

- Give requirements and checks stable IDs; retain revision identity independently of those IDs.
- Link PRs or commit trailers to applicable requirements; permit documented maintenance work without
  inventing a business requirement for every mechanical edit.
- Keep an expected inventory and separate run artifacts so stale reports cannot satisfy a current run.
- Validate each runner's report dialect, nested suites, skipped/error cases, and interrupted output.
- Preserve model, mocked/local, staging, and deployed scopes instead of merging their results.

## Gate design

Use deterministic scripts for ID parsing and inventory comparison. Report missing links, missing
execution, stale evidence, partial claims, deviations, and semantic-review gaps separately.
Choose warning/blocking policies for the affected risk and existing release rules; record justified
exceptions. Do not equate successful parsing with business correctness.

Bind semantic review to requirement, assertion, fixture, and expectation-helper revisions.
Changes invalidate that relationship review even if IDs still resolve. Rerunning tests refreshes
execution evidence only. Use independent expected values, relevant negative controls, and incident
cases to challenge the checks; domain review still establishes whether the rule reflects intent.

## Tool adoption

Start with native test reports and the project's existing documentation format. A record-management
tool can maintain links; it does not establish semantic sufficiency.

| Candidate | Evaluate before adoption |
|-----------|--------------------------|
| Sphinx-Needs + Sphinx-Test-Reports | Typed scope/gap fields, installed release, each runner's JUnit dialect |
| StrictDoc | Required authoring format and status of source/test integration in the exact release |
| Reqstool | Schemas preserve partial claims, deviations, missing execution, and review states |
| Doorstop | Fingerprint configuration, custom attributes, result ingestion, and review invalidation |

These are candidates, not qualified defaults. Pilot representative accepted, rejected, skipped, stale,
and partial mappings before migration; retain source URLs and reviewed release dates in the proposal.
