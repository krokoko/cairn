# Contributing

Thank you for helping make codebases more autonomy-ready.

## Getting started

1. Fork and clone the repository.
2. Install [mise](https://mise.jdx.dev/) and run `mise install`.
3. Run checks before opening a PR: `mise run build`

Optional: `mise run pre-commit` (installs pre-commit hooks via mise).

## What to contribute

- New or improved plugin skills and reference documents
- Validation scripts, schemas, and CI improvements
- Documentation fixes and examples

## Authoring rules

Follow [design guidelines](./docs/DESIGN_GUIDELINES.md) and the [development guide](./docs/DEVELOPMENT_GUIDE.md).

Key constraints:

- `SKILL.md`: max 400 lines, YAML frontmatter with `name` and `description`
- Reference docs: max 150 lines each, one topic per file; link from `SKILL.md`
- Plugin names: kebab-case; each plugin is self-contained
- Register in **both** `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json`

## Pull request checklist

- [ ] `mise run build` passes locally
- [ ] New skills documented in plugin `README.md` and root `README.md` if user-facing
- [ ] Report-producing skills have hook validation and a report template reference
- [ ] Versions match across marketplace entries and `plugin.json` / `.codex-plugin/plugin.json`

## License

By contributing, you agree that your contributions are licensed under the [Apache-2.0 License](./LICENSE).
