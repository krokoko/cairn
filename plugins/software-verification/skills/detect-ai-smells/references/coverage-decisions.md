# Smell Coverage Decisions

Use with the status definitions in the skill. First list applicable behaviors, then inspect
configuration, execution, and controls. These rules define coverage breadth; they do not replace
the evidence required for Qualified. A narrow check can be qualified while category coverage is
Partial. Relevant configuration without inspected execution means Configured, even when source
inspection reveals a breadth gap.

| Smell | Material gap: Partial at best when execution is established | Evidence needed to qualify the declared applicable scope |
|-------|-------------------------------------------------------------|---------------------------------------------------------|
| AI001: Plausible Fabrication | Import/package checks or interface mocks alone leave provider semantics untested | Dependency resolution plus relevant independent provider/schema/consumer cases; document twin/mock fidelity and versions |
| AI002: Cargo-Cult Patterns | Unused-code detection alone misses unnecessary used wrappers and copied patterns | Exercise relevant dead-code/dependency rules; review representative wrappers against an identified need |
| AI003: Architecture Astronaut | Complexity/size limits alone cannot establish proportionate abstractions | Qualified boundary/dependency checks plus a representative change or design review supporting abstraction cost |
| AI004: Shallow Error Handling | Empty-catch rules alone miss silent defaults, lost context, and missing boundary validation | Controls for relevant empty catches, success-masking defaults, error propagation, and startup/boundary validation |
| AI005: Tests Mirroring Implementation | Coverage or mock-call assertions alone leave shared implementation/oracle mistakes | Independent expected results, behavior-level cases, and relevant known-bad or mutation controls |
| AI006: Symmetry Without Substance | Text duplication detection alone misses structurally similar code with invented distinctions | Exercised duplication checks plus review of whether repeated branches/modules encode meaningful domain differences |
| AI007: Local Reasoning Violations | Magic-number rules alone miss cross-module inconsistency and duplicated domain constants | Qualified boundary/global-invariant checks and reviewed ownership of consequential shared values |
| AI008: Implicit Drift | Pins without a deliberate update process address drift but leave staleness unmanaged; updates without pins lose reproducibility | Inspect resolved versions, enforced pinning, and reviewed update evidence; a manual process can suffice |
| AI009: Happy-Path-Only Coverage | Line coverage alone, or branch execution without relevant outcome assertions, leaves failure behavior unverified | Assert applicable error/boundary outcomes; use branch gaps and sensitivity controls to check what is missing |
| AI010: Vacuous Tests | Assertion-presence lint alone misses assertions unable to reject a relevant defect | Known-bad cases, old-versus-fixed regressions, or relevant mutation controls demonstrate falsifiability |
| AI011: Vacuous Formal Specs | Executed specs without relevant anti-vacuity/sync controls leave obligations or correspondence unqualified | Active required claims execute; inspect obligations/bounds, model/code correspondence, and allowed/violating controls |

## Applying the rules consistently

1. Declare the relevant subcases and exclusions before examining which gates are convenient.
2. Cite at least one inspected example for each claimed covered subcase and disclose unsupported
   languages, paths, environments, or indirect edges.
3. Apply the table's gap rules. For example, an exercised empty-catch rule can qualify its narrow
   AI004 check, but cannot qualify AI004 when silent success masking is also an applicable risk.
4. Qualified category coverage requires every declared material subcase to have supported coverage;
   disclose residual human judgment for design categories. An automated gate alone cannot qualify
   proportionality, appropriateness, or whether a domain distinction is real.
5. Use None only after sufficient inspection finds no relevant mechanism; unavailable results or
   settings are Unknown, not None. Justify Not applicable from the absent failure surface.

Do not require mutation as the only sensitivity technique, behavioral twins as the only integration
technique, or a named dependency bot as the only update process. Equivalent evidence must address
the same failure and retain its limits. A `not throws` assertion is meaningful for a no-crash claim
when a relevant defect can make it fail; it does not establish a stronger output-correctness claim.
