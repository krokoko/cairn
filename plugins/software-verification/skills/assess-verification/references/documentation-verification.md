# Documentation Verification

Assessing whether documentation stays synchronized with code through automated checks. Stale docs are a fabrication vector: agents trust documentation for context and will generate code against outdated APIs, removed features, or incorrect schemas.

## Assessment Dimensions

| Dimension | What to look for | Strong signal | Weak signal |
|-----------|-----------------|---------------|-------------|
| Auto-generation | Docs derived from code annotations | OpenAPI generated from decorators, TypeDoc/rustdoc in CI | Manually maintained API docs separate from code |
| Doc build in CI | Build step that fails on broken docs | CI job running `mkdocs build --strict`, broken-link failure | Docs build exists but warnings are ignored |
| Link validation | Dead link detection | `markdown-link-check` or `linkinator` in CI, fails on broken | Occasional manual link checks |
| Example testing | Code samples in docs are executed | `doctest`, `mdx-js`, tested snippets in CI | Examples copied from code but never validated |
| Schema-doc sync | API schema validated against implementation | OpenAPI spec tested against running server, generated clients | Spec exists but not validated against impl |
| Doc freshness | Enforcement that docs update with code | PR checks requiring doc changes when API files change | Last-modified dates but no enforcement |
| ADR enforcement | Architectural decisions captured as code evolves | ADR template required for certain file paths | ADRs exist but not enforced |

## Maturity Levels

| Level | Description | Risk to agents |
|-------|-------------|----------------|
| 0 | Docs manually maintained, no validation | High — agents will treat stale docs as truth |
| 1 | Some auto-generation but no CI validation | Medium — generated docs accurate, prose docs may drift |
| 2 | CI validates doc build + links + some examples | Low-Medium — structural accuracy, content may lag |
| 3 | Full sync: derived from code, freshness enforced, examples tested | Low — docs are verifiable source of truth |

## Tools by Ecosystem

| Language | Auto-gen | Link check | Example test | Schema sync |
|----------|----------|------------|--------------|-------------|
| TypeScript | TypeDoc, typedoc-plugin-markdown | markdown-link-check | ts-node doctest scripts | openapi-typescript-codegen |
| Python | Sphinx autodoc, mkdocstrings | linkchecker, markdown-link-check | `doctest` module, `pytest --doctest-modules` | schemathesis |
| Rust | rustdoc | built-in link checking | `cargo test` runs doc examples | — |
| Go | godoc, swag (Swagger) | — | testable examples in `_test.go` | — |
| Java | Javadoc, SpringDoc | — | Spring REST Docs (tested snippets) | springdoc-openapi validation |

## Key Indicators to Search For

```
# Auto-generation configs
typedoc.json, mkdocs.yml, .readthedocs.yml, docs/conf.py, Cargo.toml [package.metadata.docs]
swag init, springdoc, @ApiProperty, @swagger, /// comments with @param

# CI doc jobs
Steps named *doc*, *docs*, *documentation* in CI configs
mkdocs build --strict, sphinx-build -W, typedoc, cargo doc

# Link checking
markdown-link-check in CI, linkinator, htmltest, lychee

# Example testing
doctest in pytest config, cargo test (runs doc examples), mdx compilation

# Freshness enforcement
CODEOWNERS on docs/, PR checks for doc-alongside-code, danger.js rules
```

## Why This Matters for Autonomy

At L3+ autonomy, agents use docs as primary context for task planning. If docs describe a removed API endpoint, the agent will:
1. Write code calling that endpoint (Plausible Fabrication)
2. Write mocks matching the stale docs (closed plausibility loop)
3. Pass all tests while producing broken code

Verified documentation breaks this cycle by ensuring what agents read matches what actually exists.
