# Toolchain Catalog

Tools organized by language ecosystem and verification category. Load `toolchain-catalog-ecosystems.md` for JVM and cross-language tools.

## Python

| Category | Tools |
|----------|-------|
| Type checking | mypy (strict), pyright, pytype |
| Linting | ruff, pylint, flake8 |
| Testing | pytest, unittest |
| Property testing | Hypothesis |
| Symbolic / contracts | CrossHair |
| Approval / snapshot testing | approvaltests, syrupy |
| BDD / executable specs | behave, pytest-bdd, radish |
| Mutation testing | mutmut, cosmic-ray |
| Test impact analysis | pytest-testmon |
| Fuzzing | Atheris (libFuzzer wrapper), python-afl |
| Specification mining | Daikon |
| Sanitizers | ASan/UBSan via C extensions, valgrind |
| Profiling | py-spy, cProfile, scalene, memray |
| Contracts | icontract, deal, dpcontracts |
| Coverage | coverage.py, pytest-cov |
| Security | bandit, semgrep |

## TypeScript / JavaScript

| Category | Tools |
|----------|-------|
| Type checking | TypeScript strict mode, tsc |
| Linting | ESLint, biome |
| Testing | Jest, Vitest, Mocha |
| Property testing | fast-check |
| Formal / spec verification | LemmaScript, lemmafit (TS → Dafny/Lean; verifier-in-agent-loop) |
| Approval / snapshot testing | Jest snapshots, jest-image-snapshot |
| BDD / executable specs | Cucumber.js, Jest-Cucumber, CodeceptJS |
| Mutation testing | Stryker |
| Test impact analysis | Jest `--onlyChanged` / `--changedSince`, Vitest `--changed` |
| Contracts | ts-contract, zod (runtime validation) |
| Profiling | Node.js --prof, clinic.js, 0x |
| Coverage | c8, istanbul |
| Security | eslint-plugin-security, semgrep |

## Go

| Category | Tools |
|----------|-------|
| Type checking | Built-in (static types) |
| Linting | golangci-lint, staticcheck, go vet |
| Testing | go test, testify |
| Property testing | rapid, gopter |
| Approval / snapshot testing | golden files (`-update` convention), goldie, cupaloy |
| BDD / executable specs | godog, ginkgo |
| Mutation testing | go-mutesting, gremlins |
| Test impact analysis | go test (package-level via `go list` + dependency graph) |
| Fuzzing | go test -fuzz (native), go-fuzz |
| Sanitizers | -race flag (ThreadSanitizer), -asan flag (Go 1.23+) |
| Profiling | pprof (CPU, memory, goroutine), trace |
| Coverage | go test -cover |
| Security | gosec, govulncheck |

## Rust

| Category | Tools |
|----------|-------|
| Type checking | Built-in (ownership + types) |
| Linting | clippy, cargo-deny |
| Testing | cargo test, #[test] |
| Property testing | proptest, quickcheck |
| Approval / snapshot testing | insta |
| BDD / executable specs | cucumber-rs |
| Mutation testing | cargo-mutants |
| Test impact analysis | cargo-nextest (partition/filter), rust-test-impact (experimental) |
| Fuzzing | cargo-fuzz (libFuzzer), afl.rs |
| Schedule exploration (C1) | Loom (exhaustive interleavings), Shuttle (randomized PCT) |
| DST — distributed sim (C2) | Turmoil, MadSim |
| Formal verification | Kani (bounded model checking), Verus |
| Proof translation | Hax (Rust → Lean/F*/Rocq/ProVerif) |
| Sanitizers | ASan, MSan, TSan, UBSan via RUSTFLAGS |
| Profiling | flamegraph, perf, cargo-flamegraph |
| Coverage | cargo-tarpaulin, llvm-cov |
