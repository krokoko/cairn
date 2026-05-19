# Toolchain Catalog (JVM and Cross-Language)

Continues `toolchain-catalog.md`. Java/Kotlin ecosystems and cross-language infrastructure tools.

## Java / Kotlin

| Category | Tools |
|----------|-------|
| Type checking | Built-in + NullAway, Checker Framework |
| Linting | SpotBugs, Error Prone, ktlint |
| Testing | JUnit, TestNG, Kotest |
| Property testing | jqwik, kotlin-quickcheck |
| Mutation testing | PIT (pitest) |
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
| Formal specification | TLA+ (TLC, Apalache), Alloy, Stateright (Rust) |
| SMT solving | Z3, CVC5 |
| Deductive verification | Dafny, Why3, Frama-C/WP, SPARK |
| Abstract interpretation | Astree, Frama-C/EVA, Infer (Meta) |
| Theorem proving | Lean 4, Coq/Rocq, Isabelle |
| Symbolic execution | KLEE, angr, Mythril (smart contracts), Manticore |
| CI/CD | GitHub Actions, GitLab CI, CircleCI |
| Progressive delivery | Argo Rollouts, Flagger, LaunchDarkly |
| Chaos engineering | Chaos Monkey, Litmus, Gremlin |
| Runtime monitoring | OpenTelemetry, Prometheus + alerts |
| Agentic QA | Playwright + agent charters, CDP, Cypress + AI drivers |
| LLM-as-Judge | OpenAI Evals, Braintrust, custom rubric evaluators |
| Statistical model checking | PRISM, UPPAAL, Monte Carlo methods |

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
