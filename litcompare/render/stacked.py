"""`--layout=stacked`: the full-markdown-fidelity escape hatch.

Tables, math and lists render natively because the source markdown is
embedded as-is (span-safe truncated) rather than converted to HTML -- at the
cost of scrolling between champion/challenger instead of scanning across a
row. Leading `#`/`>`/`|`/`-` are backslash-escaped so a block excerpt can
never reopen heading/blockquote/table/list structure inside the report.
"""

from __future__ import annotations

from ..models import Block
from .escape import escape_markdown_leading, escape_table_cell, truncate


def render_block(block: Block, *, limit: int = 420) -> str:
    text = truncate(block.raw, limit)
    return "\n".join(escape_markdown_leading(ln) for ln in text.splitlines())


def render_excerpt(text: str, *, limit: int = 240) -> str:
    """Excerpt for a markdown pipe-table cell. Unlike `render_block` (used in
    free-flowing stacked prose), this must not emit raw newlines -- a `\\n`
    ends the table row, not just the cell -- so lines join on `<br>` and
    literal `|` is escaped alongside the usual leading-character escaping."""
    text = truncate(text, limit)
    # escape_table_cell first: it touches every `|`, including a leading one,
    # which would otherwise get double-escaped ("\\|") by running
    # escape_markdown_leading second on an already-escaped leading pipe.
    return "<br>".join(escape_markdown_leading(escape_table_cell(ln)) for ln in text.splitlines())


def render_inline_diff(text: str) -> str:
    """Already valid GFM (`**ins**`/`~~del~~`) -- stacked layout renders markdown natively."""
    return text
