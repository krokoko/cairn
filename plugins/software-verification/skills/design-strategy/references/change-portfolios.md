# Change-Oriented Verification Portfolios

Start with the change and its bounded claim, then route into the component archetype and bug-surface
class. These are candidate checks, not mandatory tool bundles or universal assurance rankings.

| Change | Claim to establish | Complementary checks | Limits to retain |
|--------|--------------------|----------------------|------------------|
| Service behavior | Accepted/rejected inputs produce approved outcomes | Examples, generated values/action sequences, boundary contracts | Local doubles do not establish deployed provider behavior |
| Boundary refactor | Domain policy remains independent of adapters | Allowed/forbidden analyzer fixtures, dependency rules, representative extension task | Parser support, indirect edges, source scope, exceptions |
| Migration | Approved behavior and persistent effects are preserved | Differential/replay checks, equivalence tolerances, tests for intentional differences | Reference can preserve old bugs; no observed difference is not equivalence proof |
| Retries/concurrency | Identity, time window, transitions, and effects obey the domain rule | Repeated/conflicting requests, interruption points, fault/schedule exploration | Model correspondence, provider assumptions, campaign bounds |
| Agent workflow | Candidate meets reviewed requirements and stays within permitted scope | Ordinary behavior/boundary gates, independent controls, exact-diff evidence | Shared oracle mistakes, holdout exposure; scores do not authorize actions |
| Maintenance | A representative future change fits the intended extension points | Architecture rules, branch/mutation investigation, an adapter addition exercise | Metrics diagnose friction; a task outcome is not a universal maintainability score |

For each chosen check, specify oracle owner/revision, target source/environment, execution scope,
completion and acceptance criteria, exclusions, and the decision it would support. Record why
additional methods are unnecessary or what failure/uncertainty would justify escalation.

## Idempotency example

Claim: within the approved time window, the same key and payload returns the same job, while a
conflicting payload is rejected and durable work does not duplicate. Name tenant/key scope and
expiry behavior explicitly.

- Exercise accepted, conflicting, expired, duplicate, cancellation, and interrupted requests.
- Generate action sequences where ordering matters; use model checks when hidden interleavings
  justify them and the model can be related to the implementation.
- Check adapter boundaries and qualify local dependency behavior against provider evidence.
- Report a local sampled pass as no counterexample found in that campaign. Record separate
  deployed evidence before claiming the provider integration satisfies the requirement.

## Qualification and escalation

Use a known-good control and a deliberately violating case to check that a critical gate is wired
and sensitive. Investigate unresolved findings and stale semantic review before relying on a pass.
Do not add a formal tool solely for a maturity tier; choose it for a property whose scope it supports.
Keep the approval and permission rules already governing the project separate from evaluation scores.
