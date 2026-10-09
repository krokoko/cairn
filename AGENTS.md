# Cairn

Plugin marketplace for making codebases ready for autonomous AI development.

## Repository layout

- `plugins/` — self-contained plugins (`skills/<name>/` with nested `references/`, plus `hooks/`, `scripts/`, manifests)
  - `plugin.json` at the plugin root is the portable [Agent Plugins](https://agent-plugins.org/) manifest; `.claude-plugin/` and `.codex-plugin/` hold client-specific ones
- `.claude-plugin/marketplace.json` — Claude Code marketplace registry
- `.agents/plugins/marketplace.json` — Codex marketplace registry
- `.cursor-plugin/marketplace.json` — Cursor marketplace registry (loads the root `plugin.json` manifests)
- `schemas/` — JSON schemas for manifests and SKILL frontmatter
- `tools/` — validators and markdownlint custom rules
- `docs/DESIGN_GUIDELINES.md` — plugin authoring rules
- `docs/DEVELOPMENT_GUIDE.md` — local development and CI

## Before changing plugins

Run `mise run build` (lint + reference integrity). See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Size limits

- `SKILL.md`: max 400 lines
- `references/*.md`: max 150 lines each
- Split content across reference files when limits are exceeded
