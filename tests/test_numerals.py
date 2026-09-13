from __future__ import annotations

from litcompare import numerals
from litcompare.parse import parse_file


def test_lgd_cluster_extracted(champion_path, challenger_path):
    left = parse_file(champion_path, "left")
    right = parse_file(challenger_path, "right")
    idx = numerals.cross_index(left, right)
    assert any(a["left"] == "0.878" and a["right"] == "0.879" for a in idx["agreements"])
    assert idx["left_count"] > 0 and idx["right_count"] > 0


def test_champion_internal_lgd_inconsistency_flagged(champion_path):
    left = parse_file(champion_path, "left")
    found = numerals.internal_inconsistencies(left)
    assert any({r["a"], r["b"]} == {"0.851", "0.853"} for r in found)


def test_context_never_includes_digit_bearing_tokens(champion_path):
    left = parse_file(champion_path, "left")
    for n in numerals.extract(left):
        assert not any(any(c.isdigit() for c in w) for w in n.context)
