# Toolchain Catalog (JVM and Cross-Language)

Continues `toolchain-catalog.md`. Java/Kotlin ecosystems and cross-language infrastructure tools.

## Java / Kotlin

| Category | Tools |
|----------|-------|
| Type checking | Built-in + NullAway, Checker Framework |
| Linting | SpotBugs, Error Prone, ktlint |
| Testing | JUnit, TestNG, Kotest |
| Property testing | jqwik, kotlin-quickcheck |
| Approval / snapshot testing | ApprovalTests (Java) |
| BDD / executable specs | Cucumber-JVM, JBehave, Serenity BDD |
| Mutation testing | PIT (pitest) |
| Test impact analysis | Drill4J, JUnit5 + affected-test plugins, Parasoft Jtest |
| Fuzzing | Jazzer (libFuzzer for JVM) |
| Sanitizers | JVM built-in (bounds checking); native via JNI: ASan |
| Profiling | JFR (Flight Recorder), async-profiler, VisualVM |
| Contracts | JML + OpenJML, cofoja |
| Formal | Java Pathfinder (model checking) |
| Coverage | JaCoCo |

## Cross-language / Infrastructure

| Category | Tools |
|----------|-------|
| Consumer-driven contracts | Pact (any language), Spring Cloud Contract (JVM), Specmatic |
| BDD / executable specs | Gherkin (Cucumber, Behave, SpecFlow, godog), Reqnroll |
| Test impact analysis | Launchable, Datadog Test Visibility, Parasoft (multi-language, coverage-graph based) |
| Formal specification (C3) | TLA+ (TLC, Apalache), Alloy, Stateright, **P**, **Quint** |
| Model↔implementation conformance | **Quint Connect**, P test drivers, TLA+ trace adapters |
| Distributed history (C4) | **Jepsen** |
| Translation validation | **Alive2** (LLVM), differential on transforms |
| Specification mining | **Daikon** |
| SMT solving | Z3, CVC5 |
| Deductive verification | Dafny, Why3, Frama-C/WP, SPARK |
| Abstract interpretation | Astree, Frama-C/EVA, Infer (Meta) |
| Theorem proving | Lean 4, Coq/Rocq, Isabelle |
| Symbolic execution | KLEE, angr, Mythril (smart contracts), Manticore |
| CI/CD | GitHub Actions, GitLab CI, CircleCI |
| Progressive delivery | Argo Rollouts, Flagger, LaunchDarkly |
| Chaos engineering | Chaos Monkey, Litmus, Gremlin |
| Runtime monitoring | OpenTelemetry, Prometheus + alerts |
| Runtime spec conformance | **PObserve** (P monitors on production traces) |
| Evidence / provenance | in-toto (attestation format), SLSA (provenance spec/levels), Sigstore/Cosign + GitHub artifact attestations (signing) |
| Agentic QA | Playwright + agent charters, CDP, Cypress + AI drivers |
| LLM-as-Judge | OpenAI Evals, Braintrust, custom rubric evaluators |
| Verifier-guided search | GEPA, OpenEvolve, ShinkaEvolve, lemmafit; SkyDiscover (unverified — see sources) |
| Agent integration verification | **Skylos** (static tool-use / guardrail checks) |
| Modernization / porting | C2Rust (reference + differential validation pattern) |
| Statistical model checking | PRISM, UPPAAL, Monte Carlo methods |

### P ecosystem (spec continuity)

| Component | Role |
|-----------|------|
| P Language | Communicating state machines |
| P Checker | Systematic interleaving/failure exploration |
| PeasyAI | Generates P machines/specs/test drivers from design docs |
| PObserve | Checks real service logs against P monitors |

### Quint ecosystem

| Component | Role |
|-----------|------|
| Quint | Executable specification + model checking |
| Quint Connect | Generates scenarios from spec, replays against implementation |

### Tool sources (0.6.0 additions)

New catalog entries with their canonical sources. Cite these rather than the tool name alone (AI001 applies to our own catalog).

| Tool | Source |
|------|--------|
| P, PeasyAI, PObserve | <https://github.com/p-org/P> (PObserve: `advanced/poseberve/`, PeasyAI: `getstarted/peasyai/` under <https://p-org.github.io/P/>) |
| Quint, Quint Connect | <https://github.com/informalsystems/quint>, <https://github.com/informalsystems/quint-connect> |
| Skylos | <https://github.com/duriantaco/skylos> — `skylos discover` / `skylos defend` for LLM tool-use and guardrail checks |
| LemmaScript, lemmafit | <https://github.com/midspiral/LemmaScript>, <https://github.com/midspiral/lemmafit> |
| Turmoil, MadSim | <https://github.com/tokio-rs/turmoil>, <https://github.com/madsim-rs/madsim> |
| Hax | <https://github.com/cryspen/hax> |
| CrossHair | <https://github.com/pschanely/CrossHair> |
| Alive2 | <https://github.com/AliveToolkit/alive2> |
| Daikon | <https://plse.cs.washington.edu/daikon/> |
| Jepsen | <https://github.com/jepsen-io/jepsen> |
| GEPA, OpenEvolve, ShinkaEvolve | <https://github.com/gepa-ai/gepa>, <https://github.com/codelion/openevolve>, <https://github.com/SakanaAI/ShinkaEvolve> |
| SkyDiscover | **Unverified** — no public source located at review time; confirm before citing in a strategy |

## Architecture Fitness Functions

| Category | Tools |
|----------|-------|
| Dependency constraints (JS/TS) | eslint-plugin-boundaries, madge, dependency-cruiser |
| Dependency constraints (Python) | deptry, import-linter, pydeps |
| Dependency constraints (Java) | ArchUnit, jdepend |
| Dependency constraints (Go) | go-arch-lint, depguard |
| API surface stability | openapi-diff, buf breaking, api-extractor, cargo-public-api |
| Performance budgets | bundlesize, size-limit, Lighthouse CI, k6 |
| Structural rules | Custom scripts, ast-grep rules, Semgrep structural patterns |
| Security invariants | gitleaks, detect-secrets, govulncheck/Snyk, Semgrep |

## Eval Frameworks

| Category | Tools |
|----------|-------|
| Agent eval platforms | Braintrust, Humanloop, Langfuse |
| Coding benchmarks | SWE-bench, Terminal Bench, Aider polyglot bench |
| Custom eval runners | Custom scripts (run agent → check git diff → run tests) |
| LLM evaluation | OpenAI Evals framework, promptfoo, RAGAS |
| Trace and observability | Langfuse, Langsmith, Braintrust traces, OpenTelemetry |
