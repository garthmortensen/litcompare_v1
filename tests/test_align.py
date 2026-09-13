from __future__ import annotations

import numpy as np

from litcompare import align, calibrate
from litcompare.config import Params
from litcompare.embed import ConceptEmbedder
from litcompare.pipeline import compare


def test_gate_margin_rejects_undifferentiated_best():
    """A mutual-best pair with no margin over its runner-up on either axis
    must not become an anchor -- that is the actual mechanism that keeps an
    undifferentiated match (e.g. a broad container rollup) from stealing a
    slot from a genuinely decisive pair elsewhere in the matrix."""
    scores = np.array(
        [
            [0.80, 0.79, 0.10],  # mutual best for col 0, but margin ~0.01-0.02 both axes
            [0.78, 0.10, 0.85],  # clearly decisive for col 2 (margin 0.65)
            [0.12, 0.14, 0.20],
        ],
        dtype=np.float32,
    )
    anchors, _ = align.gate(scores, top_k=2, margin=0.03, secondary_floor=0.5, anchor_floor=0.5)
    assert (0, 0) not in anchors
    assert (1, 2) in anchors


def test_b_match_never_repeats_a_pair():
    """Regression for the replication-trick bug: np.repeat-based capacity
    expansion let the solver spend one node's capacity on several copies of
    the *same* pair, collapsing a genuine merge back to a single link."""
    scores = np.array([[0.9, 0.05], [0.9, 0.05]], dtype=np.float32)
    candidates = np.array([[True, False], [True, False]])
    pairs = align.b_match(scores, candidates, capacity=2)
    assert sorted(pairs) == [(0, 0), (1, 0)]
    assert len(set(pairs)) == len(pairs)


def test_lis_flags_the_out_of_order_element():
    seq = [0, 1, 2, 0, 3]  # unique longest non-decreasing run: indices 0,1,2,4
    keep = align.lis_indices(seq)
    moved = [i for i in range(len(seq)) if i not in keep]
    assert moved == [3]
    assert len(keep) == 4


def test_percentile_calibration_expands_a_narrow_raw_floor():
    """MiniLM/bge-class models can put every raw cosine in a narrow band;
    percentile ranking must still spread that band across the full [0, 1]
    range so a downstream cutoff can discriminate at all."""
    raw = np.array(
        [[0.60, 0.65, 0.70], [0.62, 0.75, 0.68], [0.61, 0.66, 0.74]], dtype=np.float32
    )
    pct = calibrate.percentile_matrix(raw)
    assert pct.min() == 0.0
    assert pct.max() == 1.0
    assert pct[1, 1] == pct.max()  # 0.75 was the highest raw value


def test_alignment_is_order_independent():
    rng = np.random.default_rng(0)
    n = 5
    base = rng.uniform(0.1, 0.3, size=(n, n)).astype(np.float32)
    np.fill_diagonal(base, 0.95)

    kwargs = dict(top_k=2, margin=0.1, secondary_floor=0.5, anchor_floor=0.5, capacity=1, weak_floor=0.0)
    direct = align.align(base, **kwargs)
    pairs_direct = {(p.left, p.right) for p in direct.pairs}
    assert pairs_direct == {(i, i) for i in range(n)}

    perm_rows = rng.permutation(n)
    perm_cols = rng.permutation(n)
    shuffled = base[perm_rows][:, perm_cols]
    permuted = align.align(shuffled, **kwargs)
    pairs_mapped = {(int(perm_rows[p.left]), int(perm_cols[p.right])) for p in permuted.pairs}
    assert pairs_mapped == pairs_direct


def test_pipeline_finds_the_canonical_pair_and_rejects_the_related_work_trap(champion_path, challenger_path):
    """End-to-end with the offline ConceptEmbedder (real similarity geometry,
    no network): the pair the tool exists to find must appear, and the
    known false-positive trap (`2. Related Work` -> `Selected References` on
    citation-register alone) must not."""
    result, left, right = compare(
        champion_path, challenger_path, Params(cache=False), embedder=ConceptEmbedder()
    )
    heading_pairs = {
        (left.section(sm.left_id).heading if sm.left_id else None,
         right.section(sm.right_id).heading if sm.right_id else None)
        for sm in result.section_matches
    }
    assert ("4.2 Probability of default", "Default hazard") in heading_pairs

    related_work = next(s for s in left.sections if s.heading == "2. Related Work")
    assert related_work.id in result.left_only, "Related Work must not be matched on register alone"

    # a genuine many-to-one merge exists somewhere in the accepted pairs
    right_counts: dict[str, int] = {}
    for sm in result.section_matches:
        if sm.right_id:
            right_counts[sm.right_id] = right_counts.get(sm.right_id, 0) + 1
    assert any(c > 1 for c in right_counts.values())
