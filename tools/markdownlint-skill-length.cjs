/**
 * Validates SKILL.md length limits (Cairn design guidelines).
 * Max 400 lines / 6500 words: hard error (fails the build).
 * Advisory at 350 lines / 5500 words: printed to stderr, does NOT fail the build.
 *
 * Note: markdownlint custom rules signal only via onError, which always fails
 * the build. A true non-failing advisory must therefore be emitted out-of-band
 * (console.warn to stderr) rather than through onError.
 */

"use strict";

const MAX_LINES = 400;
const WARNING_LINES = 350;
const MAX_WORDS = 6500;
const WARNING_WORDS = 5500;

module.exports = {
  names: ["skill-length", "SKILL001"],
  description: "SKILL.md files should stay within Cairn size limits",
  tags: ["skill", "length"],
  parser: "none",
  function: function skillLength(params, onError) {
    if (!params.name.endsWith("SKILL.md")) {
      return;
    }

    const frontMatterLines = params.frontMatterLines || [];
    const totalLines = frontMatterLines.length + params.lines.length;
    const content = params.lines.join("\n");
    const wordCount = content.split(/\s+/).filter(Boolean).length;

    if (totalLines > MAX_LINES) {
      onError({
        lineNumber: 1,
        detail: `Line count: ${totalLines} (max: ${MAX_LINES}). Move content to references/.`,
        context: `${totalLines} lines`,
      });
    } else if (totalLines > WARNING_LINES) {
      // Advisory only — stderr, non-failing.
      console.warn(
        `[SKILL001 advisory] ${params.name}: ${totalLines} lines ` +
          `(recommended: <${WARNING_LINES}, hard max: ${MAX_LINES}). Consider moving content to references/.`
      );
    }

    if (wordCount > MAX_WORDS) {
      onError({
        lineNumber: 1,
        detail: `Word count: ${wordCount} (max: ${MAX_WORDS}). Move content to references/.`,
        context: `${wordCount} words`,
      });
    } else if (wordCount > WARNING_WORDS) {
      // Advisory only — stderr, non-failing.
      console.warn(
        `[SKILL001 advisory] ${params.name}: ${wordCount} words ` +
          `(recommended: <${WARNING_WORDS}, hard max: ${MAX_WORDS}). Consider moving content to references/.`
      );
    }
  },
};
