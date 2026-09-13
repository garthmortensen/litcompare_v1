"""Default `--layout=html-table` body renderer.

Markdown pipe-tables can't hold this content (table rows, `$$` math, escaped
pipes, embedded newlines), but a literal HTML `<table>` can, and it nests --
so a source markdown table inside a matched block becomes a nested
`<table>`. Markdown is not processed inside an HTML block, so every block
kind is converted to HTML explicitly here rather than left as raw text.
LaTeX will not render inside an HTML cell either; math is shown as its
literal source in a `<code>` span rather than silently dropped.
"""

from __future__ import annotations

import re

from ..models import Block
from .escape import escape_html, escape_table_cell, truncate

_LIST_MARK_LEAD = ("-", "*", "+")
_DIFF_SPAN = re.compile(r"\*\*(.+?)\*\*|~~(.+?)~~")


def render_inline_diff(text: str) -> str:
    """Convert `deltas.inline_diff`'s `**ins**`/`~~del~~` markers to HTML.

    Markdown is not processed inside an HTML block, so these markers need
    explicit conversion here rather than being dropped in as-is.
    """
    out: list[str] = []
    pos = 0
    for m in _DIFF_SPAN.finditer(text):
        out.append(escape_html(text[pos : m.start()]))
        if m.group(1) is not None:
            out.append(f"<strong>{escape_html(m.group(1))}</strong>")
        else:
            out.append(f"<del>{escape_html(m.group(2))}</del>")
        pos = m.end()
    out.append(escape_html(text[pos:]))
    return "".join(out)


def _list_html(raw: str) -> str:
    items = []
    cur: list[str] = []
    ordered = False
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        lead = stripped[0]
        rest = None
        if lead in _LIST_MARK_LEAD and len(stripped) > 1 and stripped[1] == " ":
            rest = stripped[2:]
        else:
            dot = stripped.find(". ")
            if dot > 0 and stripped[:dot].isdigit():
                ordered = True
                rest = stripped[dot + 2 :]
        if rest is not None:
            if cur:
                items.append(" ".join(cur))
            cur = [rest]
        elif cur:
            cur.append(stripped)
    if cur:
        items.append(" ".join(cur))
    if not items:
        return f"<p>{escape_html(raw)}</p>"
    tag = "ol" if ordered else "ul"
    lis = "".join(f"<li>{escape_html(it)}</li>" for it in items)
    return f"<{tag}>{lis}</{tag}>"


def _table_html(block: Block) -> str:
    tbl = block.table
    if tbl is None or not tbl.headers:
        return f"<p>{escape_html(block.raw)}</p>"
    cap = f"<caption>{escape_html(tbl.caption)}</caption>" if tbl.caption else ""
    head = "".join(f"<th>{escape_html(h)}</th>" for h in tbl.headers)
    body_rows = "".join(
        "<tr>" + "".join(f"<td>{escape_html(c)}</td>" for c in row) + "</tr>" for row in tbl.rows
    )
    return f'<table class="lc-nested">{cap}<thead><tr>{head}</tr></thead><tbody>{body_rows}</tbody></table>'


def _math_html(raw: str) -> str:
    src = raw.strip()
    if src.startswith("$$") and src.endswith("$$"):
        src = src[2:-2].strip()
    return f"<code>{escape_html(src)}</code>"


def _code_html(raw: str) -> str:
    lines = [ln for ln in raw.splitlines() if not ln.strip().startswith(("```", "~~~"))]
    return f"<pre><code>{escape_html(chr(10).join(lines))}</code></pre>"


def _quote_html(raw: str) -> str:
    import re

    body = re.sub(r"^\s*>\s?", "", raw, flags=re.MULTILINE)
    return f"<blockquote>{escape_html(body).replace(chr(10), '<br>')}</blockquote>"


def render_block(block: Block, *, limit: int = 420) -> str:
    """Render one block to an HTML fragment, truncated for a scannable cell."""
    if block.kind == "table":
        return _table_html(block)
    if block.kind == "math":
        return _math_html(block.raw)
    if block.kind == "code":
        return _code_html(block.raw)
    if block.kind == "quote":
        return _quote_html(truncate(block.raw, limit))
    if block.kind == "list":
        return _list_html(truncate(block.raw, limit))
    text = truncate(block.raw, limit)
    return "<br>".join(escape_html(ln) for ln in text.splitlines())


def render_excerpt(text: str, *, limit: int = 240) -> str:
    """Excerpt for a markdown pipe-table cell (e.g. only-in-champion listings):
    escaped HTML, newlines flattened to `<br>`, and literal `|` escaped so the
    excerpt can't split the cell into extra table columns."""
    lines = truncate(text, limit).splitlines()
    return "<br>".join(escape_table_cell(escape_html(ln)) for ln in lines)
