from __future__ import annotations

import dataclasses

from litcompare.config import Params
from litcompare.embed import ConceptEmbedder
from litcompare.pipeline import compare
from litcompare.render import render


def _result(champion_path, challenger_path):
    return compare(champion_path, challenger_path, Params(cache=False), embedder=ConceptEmbedder())


def test_html_table_layout_contains_expected_sections(champion_path, challenger_path):
    result, left, right = _result(champion_path, challenger_path)
    params = Params(layout="html-table", cache=False)
    out = render(result, left, right, params)

    for heading in (
        "## Scorecard", "## Alignment map", "## Side-by-side",
        "## Only in champion", "## Only in challenger",
        "## Numeral cross-index", "## Citation overlap", "## Terminology diff",
    ):
        assert heading in out

    assert "Default hazard" in out  # the canonical cross-heading pair
    assert "<table" in out  # html-table layout renders side-by-side as real tables
    assert "kessler:2020" in out  # shared-citation key surfaced as a compact tag


def test_stacked_layout_renders_without_html_tables(champion_path, challenger_path):
    result, left, right = _result(champion_path, challenger_path)
    params = Params(layout="stacked", cache=False)
    out = render(result, left, right, params)
    assert "## Side-by-side" in out
    assert '<table class="lc-pair">' not in out


def test_render_is_deterministic_for_the_same_result(champion_path, challenger_path):
    result, left, right = _result(champion_path, challenger_path)
    params = Params(layout="html-table", cache=False)
    a = render(result, left, right, params)
    b = render(result, left, right, params)
    assert a == b


def test_excerpt_chars_param_shortens_blocks(champion_path, challenger_path):
    result, left, right = _result(champion_path, challenger_path)
    short = render(result, left, right, dataclasses.replace(Params(cache=False), excerpt_chars=40))
    long = render(result, left, right, dataclasses.replace(Params(cache=False), excerpt_chars=2000))
    assert len(short) < len(long)
