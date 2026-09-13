from __future__ import annotations

from pathlib import Path

from litcompare.parse import parse_file, parse_markdown, split_row

FIXTURES = Path(__file__).parent / "fixtures"


def test_champion_heading_count(champion_path):
    doc = parse_file(champion_path, "left")
    assert len(doc.sections) == 29


def test_challenger_heading_count(challenger_path):
    doc = parse_file(challenger_path, "right")
    assert len(doc.sections) == 25


def test_no_unterminated_math_block(champion_path, challenger_path):
    for path, side in [(champion_path, "left"), (challenger_path, "right")]:
        doc = parse_file(path, side)
        for blk in doc.blocks:
            if blk.kind == "math":
                assert blk.raw.count("$$") % 2 == 0, blk.raw


def test_champion_currency_cell_two_columns(champion_path):
    doc = parse_file(champion_path, "left")
    tables = [b.table for b in doc.blocks if b.kind == "table" and b.table]
    found = False
    for t in tables:
        for row in t.rows:
            if any("$28.6bn" in c for c in row):
                assert len(row) == 2
                found = True
    assert found, "expected the $28.6bn currency row to be found and 2 columns wide"


def test_challenger_escaped_pipe_two_columns():
    row = split_row(r"| P(default in month $m$ \| alive at $m-1$) | logistic hazard |")
    assert len(row) == 2


def test_container_sections_have_no_own_blocks(champion_path):
    doc = parse_file(champion_path, "left")
    containers = [s for s in doc.sections if s.is_container]
    assert containers, "expected at least one container section (e.g. '4. Methodology')"
    for c in containers:
        assert doc.own_blocks(c.id) == []
        assert doc.rollup_blocks(c.id) != []


def test_box_1_blockquote_captured(challenger_path):
    doc = parse_file(challenger_path, "right")
    box1 = next(s for s in doc.sections if s.heading.startswith("Box 1"))
    blocks = doc.own_blocks(box1.id)
    assert any(b.kind == "quote" for b in blocks)


def test_challenger_subtitle_classified_frontmatter(challenger_path):
    doc = parse_file(challenger_path, "right")
    subtitle = next(s for s in doc.sections if s.level == 3 and "submitted for independent" in s.heading)
    assert subtitle.kind == "frontmatter"


def test_bibliography_detected_both_fixtures(champion_path, challenger_path):
    left = parse_file(champion_path, "left")
    right = parse_file(challenger_path, "right")
    assert any(s.kind == "bibliography" for s in left.sections)
    assert any(s.kind == "bibliography" for s in right.sections)


def test_unicode_minus_round_trips():
    doc = parse_markdown("# T\n\nDrift is −1.0937 in Q1.\n", "t.md", "left")
    blk = next(b for b in doc.blocks if "1.0937" in b.raw)
    assert "-1.0937" in blk.normalized


def test_reparse_is_byte_identical(champion_path):
    text = Path(champion_path).read_text(encoding="utf-8")
    a = parse_markdown(text, champion_path, "left")
    b = parse_markdown(text, champion_path, "left")
    assert [x.normalized for x in a.blocks] == [x.normalized for x in b.blocks]
    assert [x.heading for x in a.sections] == [x.heading for x in b.sections]


def test_fenced_code_block_kept_atomic():
    doc = parse_file(str(FIXTURES / "fenced_code.md"), "left")
    headings = [s.heading for s in doc.sections]
    assert headings == [
        "A doc with a fenced code block",
        "Setup",
        "After",
    ]
    code_blocks = [b for b in doc.blocks if b.kind == "code"]
    assert len(code_blocks) == 1
    assert 'def f():' in code_blocks[0].raw


def test_heading_free_document_yields_one_section():
    doc = parse_file(str(FIXTURES / "no_headings.md"), "left")
    assert len(doc.sections) == 1
    assert doc.sections[0].block_ids
