from __future__ import annotations

from litcompare.render.escape import (
    escape_html,
    escape_markdown_leading,
    escape_table_cell,
    truncate,
)
from litcompare.render import html as html_layout
from litcompare.render import stacked as stacked_layout


def test_escape_html_basic():
    assert escape_html("a < b & c") == "a &lt; b &amp; c"


def test_truncate_never_cuts_inside_dollar_span():
    text = "before $x_1 + x_2 = y$ after more words here"
    out = truncate(text, 12)  # cut point would land mid-span without the guard
    assert out.count("$") % 2 == 0
    assert "$x_1 + x_2 = y$" in out


def test_truncate_never_cuts_inside_code_span():
    text = "before `some code span` after more words here padding"
    out = truncate(text, 10)
    assert out.count("`") % 2 == 0
    assert "`some code span`" in out


def test_truncate_noop_when_under_limit():
    assert truncate("short", 100) == "short"


def test_escape_markdown_leading_blocks_heading_and_pipe():
    assert escape_markdown_leading("# not a heading").startswith("\\#")
    assert escape_markdown_leading("| not | a | row |").startswith("\\|")
    assert escape_markdown_leading("> not a quote").startswith("\\>")
    assert escape_markdown_leading("plain text") == "plain text"


def test_truncate_never_cuts_inside_bold_span():
    text = "lead in **Portfolio** | **100%** trailing padding words here"
    out = truncate(text, 24)  # naive cut would land inside "**100%**"
    assert out.count("**") % 2 == 0


def test_truncate_never_cuts_inside_strike_span():
    text = "lead in ~~old value~~ trailing padding words here more"
    out = truncate(text, 12)
    assert out.count("~~") % 2 == 0


def test_escape_table_cell_escapes_pipes():
    assert escape_table_cell("a | b | c") == "a \\| b \\| c"
    assert escape_table_cell("no pipes here") == "no pipes here"


def _has_unescaped_pipe(text: str) -> bool:
    return any(
        text[i] == "|" and (i == 0 or text[i - 1] != "\\") for i in range(len(text))
    )


def test_html_render_excerpt_is_table_cell_safe():
    # A raw table-first block: embedded pipes and a real newline, which is
    # exactly what broke the "Only in champion/challenger" report rows.
    raw = "| Score band | LGD |\n|---|---|\n| <620 | 0.871 |"
    out = html_layout.render_excerpt(raw, limit=200)
    assert "\n" not in out
    # every literal pipe must be escaped -- an unescaped one would open a
    # new column in the outer report table
    assert not _has_unescaped_pipe(out)
    assert out.count("<br>") == 2  # the three source lines joined safely


def test_stacked_render_excerpt_is_table_cell_safe():
    raw = "| Score band | LGD |\n|---|---|\n| <620 | 0.871 |"
    out = stacked_layout.render_excerpt(raw, limit=200)
    assert "\n" not in out
    assert not _has_unescaped_pipe(out)
    # exactly one backslash per escaped pipe -- catches the leading-pipe
    # double-escape regression (escape_table_cell then escape_markdown_leading
    # applied in the wrong order turns "\|" into "\\|")
    assert "\\\\|" not in out
    assert out.count("<br>") == 2
