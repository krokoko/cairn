# Cairn

Plugin marketplace for making codebases ready for autonomous AI development.

## Repository layout

- `plugins/` — self-contained plugins (`skills/<name>/` with nested `references/`, plus `hooks/`, `scripts/`, manifests)
- `.claude-plugin/marketplace.json` — Claude Code marketplace registry
- `.agents/plugins/marketplace.json` — Codex marketplace registry
- `schemas/` — JSON schemas for manifests and SKILL frontmatter
- `tools/` — validators and markdownlint custom rules
- `docs/DESIGN_GUIDELINES.md` — plugin authoring rules
- `docs/DEVELOPMENT_GUIDE.md` — local development and CI

## Before changing plugins

Run `mise run build` (lint + reference integrity). See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Size limits

- `SKILL.md`: max 400 lines
- `references/*.md`: max 300 lines each
- Split content across reference files when limits are exceeded
