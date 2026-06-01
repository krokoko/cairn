/**
 * Validates reference markdown files stay under 150 lines.
 */

"use strict";

const MAX_LINES = 150;

module.exports = {
  names: ["reference-length", "REF001"],
  description: "Reference docs must be at most 150 lines",
  tags: ["reference", "length"],
  parser: "none",
  function: function referenceLength(params, onError) {
    if (!params.name.includes("/references/") || !params.name.endsWith(".md")) {
      return;
    }

    // markdownlint appends a trailing empty element to params.lines for newline-terminated
    // files; drop it so totalLines matches `wc -l` rather than running one line high.
    const bodyLines = params.lines.slice();
    if (bodyLines.length > 0 && bodyLines[bodyLines.length - 1] === "") {
      bodyLines.pop();
    }
    const totalLines = (params.frontMatterLines || []).length + bodyLines.length;
    if (totalLines > MAX_LINES) {
      onError({
        lineNumber: 1,
        detail: `Reference file has ${totalLines} lines (max: ${MAX_LINES}). Split into another reference file.`,
        context: `${totalLines} lines`,
      });
    }
  },
};
