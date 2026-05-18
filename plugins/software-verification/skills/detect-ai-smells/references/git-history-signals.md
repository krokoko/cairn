# Detection Patterns — Git History

Heuristics for detecting vibe-coding signals from commit history and PR metadata.

## Commit-Level Signals

### Low-quality commit messages

```bash
# Generic single-word messages with no context
git log --oneline -100 | grep -icE "^[a-f0-9]+ (fix|update|change|tweak|wip|stuff|misc|temp)$"
# Score: (generic / total) × 100 — flag if >30%
```

### Fix-revert cycles

```bash
# Same file modified in 3+ consecutive commits by same author
git log --name-only --format="%H %an" -100
# Group by author, find files appearing in 3+ sequential commits
# Especially with messages like "fix", "try", "again"
```

### Large diffs without tests

```bash
# Commits adding >100 source lines with 0 test file changes
git log --numstat -50
# Per commit: sum additions in src/ vs test/ files
# Flag: src_additions > 100 AND test_additions == 0
```

### Bulk file creation

```bash
# Commits creating >5 new files simultaneously
git log --diff-filter=A --numstat -50
# Flag commits creating >5 files with similar names/structure
```

### Unusually large initial files

```bash
# Files created with >300 lines in first commit (generated, not evolved)
git log --diff-filter=A --numstat | awk '$1 > 300 { print $3 }'
```

## PR-Level Signals (when available)

```bash
# PRs with empty descriptions
gh pr list --state merged --limit 20 --json body

# PRs with no linked issue (missing traceability)
gh pr list --state merged --limit 20 --json number,title,body | \
  jq '[.[] | select(.body | test("(close[sd]?|fix(e[sd])?|resolve[sd]?)\\s+#"; "i") | not)]'

# PRs with 0 review comments touching >5 files
gh pr list --state merged --limit 20 --json comments,files

# PRs adding source with no test changes
gh pr diff <number> --stat | # compare src vs test additions
```

## Vibe-Coding Risk Score

| Signal | Weight | Threshold |
|--------|--------|-----------|
| Generic commit messages | 3 | >30% of commits |
| Fix-revert cycles | 4 | Any 3+ consecutive same-file commits |
| Large diffs without tests | 3 | Any commit >100 lines, 0 tests |
| Bulk file creation | 2 | >5 similar files in one commit |
| Large initial files | 1 | >300 lines on creation |
| Empty PR descriptions | 2 | >50% of PRs |
| PRs without linked issues | 3 | >50% of PRs missing issue reference |
| Zero-comment PRs (>5 files) | 2 | Any occurrence |

**Risk levels:**
- **Low** (0-4 weighted points): Normal development patterns
- **Medium** (5-10): Some signals present, recommend review process improvements
- **High** (11+): Strong vibe-coding indicators, recommend immediate process changes
