from __future__ import annotations

from pathlib import Path

from litcompare import metrics
from litcompare.align import Alignment
from litcompare.config import Params
from litcompare.embed import ConceptEmbedder
from litcompare.parse import parse_file
from litcompare.pipeline import compare

README = str(Path(__file__).parent.parent / "README.md")


def test_self_comparison_full_coverage_zero_one_sided(champion_path):
    result, _, _ = compare(champion_path, champion_path, Params(cache=False), embedder=ConceptEmbedder())
    assert result.metrics["coverage_left"]["overall"] == 1.0
    assert result.metrics["coverage_right"]["overall"] == 1.0
    assert result.metrics["left_only"] == 0
    assert result.metrics["right_only"] == 0


def test_comparability_guard_fires_when_no_pairs_survive_the_gate(champion_path):
    """Unit-level: exercise metrics.py's own warning logic directly, rather
    than depending on any particular embedder's discriminative power to
    produce zero accepted pairs for a genuinely unrelated document (the
    offline ConceptEmbedder is a concept-lexicon plumbing stand-in, not a
    general-purpose discriminator -- that end-to-end behaviour is verified
    against the real sentence-transformers model instead)."""
    left = parse_file(champion_path, "left")
    right = parse_file(README, "right")
    empty = Alignment(
        pairs=[],
        left_only=list(range(len(left.alignable_sections))),
        right_only=list(range(len(right.alignable_sections))),
    )
    metrics_dict, warnings = metrics.build(left, right, empty, {}, {}, doc_cosine=0.1)
    assert warnings, "no accepted pairs must not produce a silent, confident map"
    assert metrics_dict["left_only"] == len(left.alignable_sections)
    assert metrics_dict["right_only"] == len(right.alignable_sections)
