# Toolchain Catalog

Tools organized by language ecosystem and verification category. Load `toolchain-catalog-ecosystems.md` for JVM and cross-language tools.

## Python

| Category | Tools |
|----------|-------|
| Type checking | mypy (strict), pyright, pytype |
| Linting | ruff, pylint, flake8 |
| Testing | pytest, unittest |
| Property testing | Hypothesis |
| Mutation testing | mutmut, cosmic-ray |
| Fuzzing | Atheris (libFuzzer wrapper), python-afl |
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
| Mutation testing | Stryker |
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
| Mutation testing | go-mutesting, gremlins |
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
| Mutation testing | cargo-mutants |
| Fuzzing | cargo-fuzz (libFuzzer), afl.rs |
| Formal verification | Kani (bounded model checking), Verus |
| Sanitizers | ASan, MSan, TSan, UBSan via RUSTFLAGS |
| Profiling | flamegraph, perf, cargo-flamegraph |
| Coverage | cargo-tarpaulin, llvm-cov |
