"""HTML/markdown escaping and span-safe truncation.

Its own module because both layouts need it and because truncation is the
one place a naive implementation reliably breaks output: cutting mid-`$...$`,
mid-`` `...` ``, mid-`**...**`, or mid-`~~...~~` leaves an unterminated span
that swallows or malforms the rest of a markdown-rendered cell.
"""

from __future__ import annotations

import html
import re

_SPAN = re.compile(r"\$[^$\n]*\$|`[^`\n]*`|\*\*[^*\n]*\*\*|~~[^~\n]*~~")
_MD_LEADING = re.compile(r"^(\s*)([#>|-])")


def escape_html(text: str) -> str:
    """Escape for embedding inside an HTML tag body (markdown is not parsed there)."""
    return html.escape(text, quote=False)


def escape_markdown_leading(text: str) -> str:
    """Escape leading `#`, `>`, `|`, `-` so a raw excerpt can't reopen markdown
    structure (a heading, blockquote, table row, or list item) once dropped
    into a report table cell or stacked block."""
    return _MD_LEADING.sub(lambda m: m.group(1) + "\\" + m.group(2), text)


def escape_table_cell(text: str) -> str:
    """Escape a literal `|` so text can sit inside a markdown pipe-table cell
    without splitting into extra columns. Callers still need to flatten
    newlines separately (a raw `\\n` ends the row, not just the cell)."""
    return text.replace("|", "\\|")


def truncate(text: str, limit: int) -> str:
    """Truncate to ~`limit` chars without cutting inside a `$...$`, `` `...` ``,
    `**...**`, or `~~...~~` span (any of those left unterminated would swallow
    or malform the rest of a markdown-rendered cell)."""
    if len(text) <= limit:
        return text
    cut = limit
    for m in _SPAN.finditer(text):
        if m.start() < cut < m.end():
            cut = m.end()
            break
    if cut >= len(text):
        return text
    return text[:cut].rstrip() + "…"


def paragraph_to_html(text: str, *, limit: int | None = None) -> str:
    """Paragraph-ish raw markdown -> escaped HTML with `<br>` line breaks."""
    body = truncate(text, limit) if limit else text
    lines = [escape_html(ln) for ln in body.splitlines()]
    return "<br>".join(lines)
