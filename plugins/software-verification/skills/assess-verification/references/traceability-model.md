# Requirement Traceability Model

Trace **approved requirement → bounded claim → scenario/property → executed check → versioned
evidence → reviewed decision**, with source/code mappings identifying the implementation.
A deterministic parser establishes links and gaps. It cannot decide whether an assertion expresses
the right business rule. Load `evidence-semantics.md` and `oracle-lifecycle.md` for those limits.

## Three kinds of completeness

| Dimension | Deterministic checks | Judgment still needed |
|-----------|----------------------|-----------------------|
| Links | Requirement/claim IDs resolve to check IDs and implementation scope | Mappings are relevant; unrequested behavior may hide inside linked code |
| Execution | Expected checks join to current completed results for the artifact/environment | Campaign and environment are adequate for the bounded claim |
| Meaning | Review records identify the requirement/assertion/fixture/helper revisions | Assertions support approved intent; partial claims and deviations are accepted |

Technical checks provide scoped evidence. A passing linked test, a high coverage percentage, and
a fresh fingerprint do not independently establish business correctness.

## Trace records

| Record | Required content |
|--------|------------------|
| Requirement and claim | Stable IDs, approved revision, bounded proposition, accepted exclusions |
| Scenario/property | Check IDs, relevant cases, oracle/assertion and fixture/helper revisions |
| Implementation | Source revision plus relevant dirty changes; component/code mapping |
| Execution | Run ID/artifact, environment, expected versus actual checks, completion/status |
| Decision | Applicable evidence, review revisions, partial claims/deviations, unresolved gaps |

Gherkin is one representation. Test annotations, reviewed contracts, structured requirement files,
or supported tracker records can provide parseable links without adding a BDD framework.

## Assessment signals

- Requirement anchors: `docs/requirements/`, `docs/specs/`, structured issues, EARS statements.
- Claim/check links: requirement tags in tests, scenario IDs, property/contract mappings.
- PR/commit links: issue references with inspected source scope; sample history, report unknowns.
- Native runner reports: JUnit or structured results joined against an expected check inventory.
- Run isolation: fresh artifact directories; skipped, missing, duplicate, or interrupted results visible.
- Currentness: run revision/environment applies to the assessed scope; old results are not silently reused.
- Review invalidation: changed requirements, assertions, fixtures, or helpers trigger impact review.

Distinguish three traditional RTM uses:

| Property | What the mapping supports | What it cannot establish alone |
|----------|---------------------------|--------------------------------|
| Scope verification | Exposes untraced changes and unmapped requirements | Every linked change is requested or correct |
| Impact analysis | Identifies checks/files associated with changed intent | All implicit dependencies are captured |
| Test sufficiency | Exposes requirements with no dedicated check/evidence | One mapped test adequately covers the requirement |

## Maturity levels (0–3)

| Level | State |
|-------|-------|
| 0 | No inspected link from requirements to code/checks |
| 1 | PRs reference issues; claim-to-check mappings remain manual or partial |
| 2 | Parseable claim/check/code mappings and run results exist; execution/review gaps are reported |
| 3 | Pipeline enforces applicable link and execution completeness; revision-bound semantic reviews and deviations are maintained |

Use `unknown` if needed records are inaccessible. Missing links or weak levels are consequential
where autonomous work relies on those requirements; prioritize by affected claim and criticality.
Level 3 still does not prove intent is correct.

## Tool selection

Record-management tools can maintain relationships without adjudicating semantic sufficiency.
Candidates include Sphinx-Needs with Sphinx-Test-Reports, Doorstop, StrictDoc, and Reqstool; existing
structured files and deterministic scripts may suffice. Check current official release docs and
trial representative mappings, partial claims, review invalidation, and native runner formats.

Keep an explicit expected inventory. A declaration is not evidence that its steps executed.
Validate the selected report dialect and preserve unsupported/missing evidence states. Prefer a
small demonstrated integration over migrating records on the strength of a product description.
