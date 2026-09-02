# Development Guide

This guide explains how to create, validate, and test plugins for the Cairn marketplace.

## Prerequisites

- [mise](https://mise.jdx.dev/) for task running and tool management
- Node.js 24+ (via mise) for markdownlint and ajv
- Python 3.10+ for reference integrity checks
- Bash for hook scripts

Install tools:

```bash
mise install
```

## Repository tooling

| Task | Command | What it checks |
|------|---------|----------------|
| Full CI build | `mise run build` | Lint + validate |
| Alias | `mise run check` | Same as build |
| Markdown | `mise run lint:md` | All `**/*.md` + custom SKILL/reference rules |
| Manifests | `mise run lint:manifests` | JSON Schema via ajv (marketplaces, plugin manifests) |
| Cross-refs | `mise run lint:cross-refs` | Claude + Codex marketplaces vs plugin dirs |
| JSON | `mise run lint:json` | JSON validity of all `.json` files |
| References | `mise run validate:refs` | Broken links and orphan reference files |
| Validators | `mise run test:validators` | Report-validator hook scripts + template-drift guard |
| Routing fixtures | `mise run test:fixtures` | `tests/routing-fixtures/`: layout, schemas, expected tools exist in references (not routing accuracy) |
| Secrets | `mise run security:secrets` | gitleaks secret scan (runs as part of `build`) |
| Pre-commit | `mise run pre-commit` | Optional local hook bundle |

Custom markdownlint rules in `tools/`:

- `markdownlint-skill-length.cjs` — SKILL.md hard max 400 lines / 6500 words (fails build); 350-line / 5500-word advisory printed to stderr without failing
- `markdownlint-reference-length.cjs` — references max 300 lines
- `markdownlint-frontmatter.cjs` — SKILL frontmatter vs schema

## Creating a new plugin

### 1. Create the directory structure

```bash
mkdir -p plugins/my-plugin/.claude-plugin
mkdir -p plugins/my-plugin/.codex-plugin
mkdir -p plugins/my-plugin/hooks
mkdir -p plugins/my-plugin/scripts
mkdir -p plugins/my-plugin/skills/my-skill/references
```

### 2. Write manifests

Create `plugins/my-plugin/.claude-plugin/plugin.json` and `plugins/my-plugin/.codex-plugin/plugin.json`. See existing plugins for Codex `interface` fields. Use `schemas/plugin.schema.json` and `schemas/codex-plugin.schema.json`.

### 3. Write your first skill

Create `plugins/my-plugin/skills/my-skill/SKILL.md` with YAML frontmatter and a step-by-step workflow. See `docs/DESIGN_GUIDELINES.md`.

### 4. Add reference documents

Create `plugins/my-plugin/skills/my-skill/references/*.md`. Keep each file under 300 lines. Link them from `SKILL.md` so `tools/validate-references.py` can reach them. For cross-skill references within a plugin, use relative paths (e.g. `../../other-skill/references/foo.md`) — bare filenames only resolve within the same `references/` directory.

### 5. Add hooks (optional)

If your skill produces a structured output file, add a PostToolUse hook. See `docs/DESIGN_GUIDELINES.md`.

### 6. Register in both marketplaces

Add entries to `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json`. See existing plugins for the Codex entry shape. Keep `version` in sync across marketplaces and both manifest files.

## Testing a plugin

**Claude Code:** `/plugin marketplace add krokoko/cairn` then install the plugin.

**Codex:** Open this repo; install from the Cairn marketplace in the plugin UI.

Verify each skill follows its workflow, loads references, produces the expected report format, and hooks validate output when applicable.

## Code style

- JSON: 2-space indentation
- Markdown: ATX headings; run `mise run lint:md` before committing
- Shell scripts: `set -euo pipefail`, quote variables
