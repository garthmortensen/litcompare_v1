"""Scorecard.

Deliberately *not* led by document mean-vector cosine: between two papers on
the same topic that number sits near 1.0 and carries no information. The
headline numbers are the mean calibrated score over accepted pairs and
type-partitioned coverage, with the score distribution reported alongside so a
reader can see the floor rather than trusting a scalar.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import kendalltau

from .align import Alignment
from .models import Document

COVERAGE_FLOOR = 0.90         # calibrated percentile
TYPES = {
    "prose": ("paragraph", "list", "list-item", "quote"),
    "table": ("table",),
    "math": ("math", "code"),
}


def _countable(doc: Document):
    return [
        b
        for b in doc.blocks
        if b.kind not in ("citation", "frontmatter")
        and doc.section(b.section_id).kind not in ("bibliography", "frontmatter")
    ]


def coverage(
    doc: Document, best_scores: dict[str, float], floor: float = COVERAGE_FLOOR
) -> dict[str, float]:
    """Share of content-word tokens with a counterpart above `floor`.

    Weighted by content words rather than characters so punctuation-dense
    table rows cannot dominate, and partitioned by block type because a single
    blended scalar hides which *kind* of content is unmatched.
    """
    out: dict[str, float] = {}
    for name, kinds in TYPES.items():
        blocks = [b for b in _countable(doc) if b.kind in kinds]
        total = sum(max(b.token_count, 1) for b in blocks)
        hit = sum(
            max(b.token_count, 1) for b in blocks if best_scores.get(b.id, 0.0) >= floor
        )
        out[name] = round(hit / total, 4) if total else 0.0
    blocks = _countable(doc)
    total = sum(max(b.token_count, 1) for b in blocks)
    hit = sum(max(b.token_count, 1) for b in blocks if best_scores.get(b.id, 0.0) >= floor)
    out["overall"] = round(hit / total, 4) if total else 0.0
    return out


def score_distribution(best_scores: dict[str, float]) -> list[float]:
    if not best_scores:
        return []
    arr = np.fromiter(best_scores.values(), dtype=np.float64)
    return [round(float(x), 4) for x in np.percentile(arr, list(range(0, 101, 10)))]


def build(
    left_doc: Document,
    right_doc: Document,
    alignment: Alignment,
    left_best: dict[str, float],
    right_best: dict[str, float],
    doc_cosine: float,
) -> tuple[dict, list[str]]:
    pairs = alignment.pairs
    n_left = len(left_doc.alignable_sections)
    n_right = len(right_doc.alignable_sections)
    scores = [p.score for p in pairs]
    strong = [p for p in pairs if p.relation != "weak"]

    tau = 0.0
    if len(pairs) >= 3:
        t = kendalltau([p.left for p in pairs], [p.right for p in pairs]).statistic
        tau = 0.0 if np.isnan(t) else round(float(t), 4)

    metrics = {
        "mean_accepted_score": round(float(np.mean(scores)), 4) if scores else 0.0,
        "accepted_pairs": len(pairs),
        "strong_pairs": len(strong),
        "anchors": alignment.n_anchors,
        "weak_pairs": len(pairs) - len(strong),
        "sections_left": n_left,
        "sections_right": n_right,
        "left_only": len(alignment.left_only),
        "right_only": len(alignment.right_only),
        "split_count": alignment.split_count,
        "merge_count": alignment.merge_count,
        "moved_count": alignment.moved_count,
        "order_divergence": round(1.0 - alignment.lis_length / len(pairs), 4) if pairs else 0.0,
        "kendall_tau": tau,
        "coverage_left": coverage(left_doc, left_best),
        "coverage_right": coverage(right_doc, right_best),
        "left_score_deciles": score_distribution(left_best),
        "right_score_deciles": score_distribution(right_best),
        "document_cosine": round(float(doc_cosine), 4),
    }

    warnings: list[str] = []
    pairable = max(min(n_left, n_right), 1)
    if not pairs:
        warnings.append(
            "No section pair survived the gate. These documents are probably not "
            "comparable; treat the report as evidence of difference, not alignment."
        )
    elif alignment.n_anchors <= 1 or len(pairs) / pairable < 0.15:
        warnings.append(
            f"Only {alignment.n_anchors} anchor pair(s) and {len(pairs)} accepted pair(s) "
            f"across {pairable} pairable sections. Alignment is weak; read the "
            f"one-sided sections rather than the pair map."
        )
    if metrics["coverage_left"]["overall"] < 0.15 and metrics["coverage_right"]["overall"] < 0.15:
        warnings.append(
            "Coverage is below 15% in both directions, so the two documents share "
            "little content at block level."
        )
    return metrics, warnings
