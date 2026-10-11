# Improvement Actions Catalog

Load `improvement-actions-agent.md` for agent surfaces. Select actions from observed gaps;
effort is indicative. Adapt each acceptance criterion to the surface, claim and environment.
These actions do not promise score increments or demonstrate outcomes before execution.

## Structure and modularity

| Action | Effort | Failure addressed | Acceptance criterion |
|--------|--------|-------------------|----------------------|
| Organize code around domain boundaries | Medium | Unrelated edits spread across modules | A representative change stays within expected boundaries and passes relevant checks |
| Clarify public interfaces and dependency direction | Medium | Consumers depend on implementation details | Allowed imports pass and forbidden imports fail; review any new coupling from shared utilities or barrel exports |
| Add qualified boundary analysis to CI | Medium | Architecture drift goes unnoticed | Allowed and forbidden examples exercise supported direct/indirect edges, with parser scope and exceptions retained |
| Isolate agent-writable components where risk warrants it | Medium | A bounded task can affect unrelated critical state | An attempted out-of-scope access is rejected in the intended environment |

## Documentation

| Action | Effort | Failure addressed | Acceptance criterion |
|--------|--------|-------------------|----------------------|
| Improve setup and verification instructions | Small | New contributors cannot reproduce the workflow | A clean-environment trial reaches the documented checks; unresolved setup dependencies are recorded |
| Record consequential decisions in ADRs | Small | Constraints must be rediscovered | An affected change can locate its decision, rationale and current status |
| Document public APIs and compatibility changes | Medium | Consumers infer behavior incorrectly | Examples and compatibility claims are checked against the current revision |

## Testable boundaries

| Action | Effort | Failure addressed | Acceptance criterion |
|--------|--------|-------------------|----------------------|
| Add tests for unprotected critical behavior | Medium | A named regression can pass unnoticed | Approved accepted/rejected cases execute; a known-bad control fails |
| Add a risk-based test-with-code policy | Small | New behavior ships without relevant evidence | CI requires the relevant checks and a documented exception route |
| Separate unit and integration campaigns | Small | Slow/flaky external checks obscure local failures | Each campaign identifies its environment and reports completion independently |
| Add fixtures and seams | Medium | State/dependency coupling prevents focused checks | Cases run independently; doubles' unsupported provider behavior is documented |
| Add property tests for key invariants | Medium | Examples miss meaningful input/state combinations | Reviewed properties run with retained seeds/campaign bounds and reproduce a known violation |

## CI reliability

| Action | Effort | Failure addressed | Acceptance criterion |
|--------|--------|-------------------|----------------------|
| Add or repair CI test execution | Medium | Configured checks do not run on relevant changes | A completed run binds expected checks and results to the target revision |
| Require relevant checks and inspect coverage gaps | Small | Missing checks or unexercised decisions look green | A failed/missing required check blocks merge; critical uncovered decisions are reviewed |
| Add relevant lint/type checks early | Small | Cheap detectable errors reach review | A deliberate violation fails with an actionable message in local and CI flows |
| Add test impact analysis where needed | Medium | Feedback cost grows with the suite | Compare selection against a full run on representative changes; retain a full-run fallback |

## Typing strength

| Action | Effort | Failure addressed | Acceptance criterion |
|--------|--------|-------------------|----------------------|
| Enable relevant strict type checks | Small | Invalid states cross typed boundaries | Known invalid examples fail under the CI configuration |
| Review and reduce unsafe escape hatches | Medium | Unchecked assumptions bypass the checker | Critical casts/ignores have explicit justification or checked replacements |
| Type and validate API boundaries | Medium | External data is trusted without validation | Invalid boundary inputs are rejected; supported valid inputs remain accepted |

## Deterministic environment and deployment

| Action | Effort | Failure addressed | Acceptance criterion |
|--------|--------|-------------------|----------------------|
| Codify reproducible environment/setup | Medium | Local and CI results depend on hidden setup | A fresh environment reproduces documented checks using pinned inputs |
| Document and validate configuration | Small | Missing settings silently change behavior | Required values and invalid combinations fail with actionable errors |
| Codify deployment and infrastructure checks | Large | Deployed state diverges from versioned intent | Reviewed plans and a scoped staging exercise expose relevant drift and recovery limits |

## Architecture decisions

| Action | Effort | Failure addressed | Acceptance criterion |
|--------|--------|-------------------|----------------------|
| Record ownership and review boundaries | Small | Consequential changes lack an accountable decision | In-scope changes resolve the relevant owner and review policy |
| Back a key ADR with a qualified fitness check | Medium | Documented constraints silently erode | ADR links its check; allowed/forbidden examples establish the analyzed constraint |
| Track decision status and supersession | Small | Agents follow obsolete decisions | A superseded decision points to its current replacement and affected checks |

## Machine-readable intent

| Action | Effort | Failure addressed | Acceptance criterion |
|--------|--------|-------------------|----------------------|
| Add reviewed API/configuration contracts | Medium | Interfaces have ambiguous accepted inputs | Claims map to relevant validation checks and explicit unsupported behavior |
| Link acceptance criteria to executable checks | Medium | Tests do not reflect approved intent | Reviewed claims map to ordinary tests, contracts or BDD with inspected execution |
| Check traceability links and expected executions | Medium | A linked but skipped/stale check appears covered | Missing mappings/results and skipped checks remain gaps; report revision and environment |
| Review oracle changes and independent expectations | Medium | Green tests encode stale intent or shared errors | Requirement/assertion/fixture/helper changes invalidate review; known-bad controls are detected |
| Trial rebuilding a bounded component from specs | Large | Critical knowledge exists only in implementation | Rebuilt behavior meets reviewed criteria under a declared scope; remaining knowledge gaps are retained |

## Progressive context disclosure

| Action | Effort | Failure addressed | Acceptance criterion |
|--------|--------|-------------------|----------------------|
| Add an agent entry point with current project rules | Small | Agents guess conventions | A representative task locates its constraints and verification command |
| Add module docs and meaningful cross-links | Medium | Relevant context is hard to retrieve | A reader follows links from entry point to module contract without broken references |
| Preserve plans and consequential decisions | Small | Task context disappears between sessions | Work can resume from current progress, decisions and unresolved assumptions |

## Hidden state and magic

| Action | Effort | Failure addressed | Acceptance criterion |
|--------|--------|-------------------|----------------------|
| Validate environment and feature configuration | Medium | Ambient defaults change behavior silently | Supported configurations are explicit and invalid states fail at the boundary |
| Document runtime flags and ownership | Small | Release behavior is detached from review | Each consequential flag has declared semantics, owner and rollback behavior |

## Repository-scale reasoning

| Action | Effort | Failure addressed | Acceptance criterion |
|--------|--------|-------------------|----------------------|
| Standardize patterns where inconsistency causes errors | Medium | Similar tasks require incompatible assumptions | Representative modules use discoverable conventions without unnecessary abstraction |
| Clarify ambiguous domain terms | Small | Agents select the wrong concept | Searches resolve the intended concept and documented distinctions |
| Document canonical task commands | Small | Contributors run incomplete alternative checks | Commands enumerate expected checks and report missing or incomplete execution |
