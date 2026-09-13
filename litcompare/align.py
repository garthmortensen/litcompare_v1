"""Matching.

Global one-to-one assignment (Hungarian on 1-cosine) was measured against the
two fixtures and fails: it leaves `4.2 Probability of default` unmatched while
pairing `2. Related Work` with `Selected References` at the highest cosine in
the whole matrix. Two causes, both structural rather than tuning problems:

1. Forced 1:1 minimises a global sum, so one strong false pair evicts a true
   pair and the error cascades. Around a third of sections in these papers
   have no counterpart at all, and the true relation is many-to-many
   (champion 5.1-5.4 all correspond to challenger `Results`).
2. The highest raw similarities are shared *register* (citation-dense prose),
   not shared content.

So: gate first for precision (mutual top-k plus a Lowe-style margin test),
then recover recall by capacity-k b-matching among gated candidates only, then
read reading-order divergence off a longest-increasing-subsequence backbone.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import linear_sum_assignment

NON_CANDIDATE_COST = 10.0


@dataclass(slots=True)
class AcceptedPair:
    left: int
    right: int
    score: float
    relation: str = "1:1"
    moved: bool = False
    anchor: bool = False


@dataclass(slots=True)
class Alignment:
    pairs: list[AcceptedPair] = field(default_factory=list)
    left_only: list[int] = field(default_factory=list)
    right_only: list[int] = field(default_factory=list)
    n_anchors: int = 0
    lis_length: int = 0

    @property
    def moved_count(self) -> int:
        return sum(1 for p in self.pairs if p.moved)

    @property
    def split_count(self) -> int:
        return sum(1 for p in self.pairs if p.relation == "split")

    @property
    def merge_count(self) -> int:
        return sum(1 for p in self.pairs if p.relation == "merge")


def _top_k_mask(scores: np.ndarray, k: int, axis: int) -> np.ndarray:
    """Boolean mask of the k highest entries along `axis`."""
    if scores.size == 0:
        return np.zeros_like(scores, dtype=bool)
    kk = min(k, scores.shape[axis])
    idx = np.argsort(-scores, axis=axis, kind="stable")
    mask = np.zeros_like(scores, dtype=bool)
    if axis == 1:
        rows = np.arange(scores.shape[0])[:, None]
        mask[rows, idx[:, :kk]] = True
    else:
        cols = np.arange(scores.shape[1])[None, :]
        mask[idx[:kk, :], cols] = True
    return mask


def _margins(scores: np.ndarray, axis: int) -> np.ndarray:
    """best - second_best along an axis (the Lowe ratio test, additive form)."""
    if scores.size == 0:
        return np.zeros(scores.shape[1 - axis], dtype=np.float32)
    srt = np.sort(scores, axis=axis)
    if scores.shape[axis] < 2:
        return np.take(srt, -1, axis=axis).astype(np.float32)
    best = np.take(srt, -1, axis=axis)
    second = np.take(srt, -2, axis=axis)
    return (best - second).astype(np.float32)


def gate(
    scores: np.ndarray,
    *,
    top_k: int = 3,
    margin: float = 0.03,
    secondary_floor: float = 0.90,
    anchor_floor: float = 0.75,
) -> tuple[list[tuple[int, int]], np.ndarray]:
    """Return (anchor pairs, candidate mask).

    An anchor is a mutual best pair that is decisive from at least one side
    *and* clears `anchor_floor`. The floor matters: being the mutual best is
    only meaningful relative to the pair's own null distribution, and a mutual
    best sitting below the median of that distribution is evidence of nothing.
    Candidates additionally include mutual top-k pairs above
    `secondary_floor`, which is where split/merge relations come from.
    """
    if scores.size == 0:
        return [], np.zeros_like(scores, dtype=bool)

    row_best = scores.argmax(axis=1)
    col_best = scores.argmax(axis=0)
    row_margin = _margins(scores, axis=1)
    col_margin = _margins(scores, axis=0)

    anchors: list[tuple[int, int]] = []
    for i, j in enumerate(row_best):
        if col_best[j] != i:
            continue
        if scores[i, j] < anchor_floor:
            continue
        if row_margin[i] > margin or col_margin[j] > margin:
            anchors.append((i, int(j)))

    mutual = _top_k_mask(scores, top_k, axis=1) & _top_k_mask(scores, top_k, axis=0)
    candidates = mutual & (scores >= secondary_floor)
    for i, j in anchors:
        candidates[i, j] = True
    return anchors, candidates


def b_match(
    scores: np.ndarray, candidates: np.ndarray, capacity: int = 2
) -> list[tuple[int, int]]:
    """Capacity-k bipartite matching restricted to `candidates`.

    Solved as `capacity` successive optimal 1:1 assignments, each run over the
    candidates not yet used and over nodes that still have spare capacity.
    (Replicating the axes with `np.repeat` and solving once looks simpler but
    is wrong: the solver happily spends a node's replicas on several copies of
    the *same* pair, so a 4:1 merge collapses back to a single link.)
    """
    n, m = scores.shape
    if n == 0 or m == 0 or not candidates.any():
        return []
    remaining = candidates.copy()
    deg_l = np.zeros(n, dtype=np.int32)
    deg_r = np.zeros(m, dtype=np.int32)
    out: list[tuple[int, int]] = []

    for _ in range(max(capacity, 1)):
        mask = remaining & (deg_l < capacity)[:, None] & (deg_r < capacity)[None, :]
        if not mask.any():
            break
        cost = np.where(mask, 1.0 - scores.astype(np.float64), NON_CANDIDATE_COST)
        rows, cols = linear_sum_assignment(cost)
        added = False
        for r, c in zip(rows, cols):
            i, j = int(r), int(c)
            if not mask[i, j] or deg_l[i] >= capacity or deg_r[j] >= capacity:
                continue
            out.append((i, j))
            remaining[i, j] = False
            deg_l[i] += 1
            deg_r[j] += 1
            added = True
        if not added:
            break
    return sorted(set(out))


def lis_indices(seq: list[int]) -> list[int]:
    """Indices of a longest non-decreasing subsequence of `seq`.

    Non-decreasing rather than strictly increasing, so that the several left
    sections of a merge (which all point at the same right section) are not
    mislabelled as reordered.
    """
    if not seq:
        return []
    tails: list[int] = []       # index in seq of the smallest tail per length
    prev: list[int] = [-1] * len(seq)
    for i, v in enumerate(seq):
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = (lo + hi) // 2
            if seq[tails[mid]] <= v:
                lo = mid + 1
            else:
                hi = mid
        prev[i] = tails[lo - 1] if lo > 0 else -1
        if lo == len(tails):
            tails.append(i)
        else:
            tails[lo] = i
    out: list[int] = []
    cur = tails[-1]
    while cur >= 0:
        out.append(cur)
        cur = prev[cur]
    return out[::-1]


def align(
    scores: np.ndarray,
    *,
    top_k: int = 3,
    margin: float = 0.03,
    secondary_floor: float = 0.90,
    anchor_floor: float = 0.75,
    capacity: int = 2,
    weak_floor: float = 0.93,
) -> Alignment:
    n, m = scores.shape
    anchors, candidates = gate(
        scores,
        top_k=top_k,
        margin=margin,
        secondary_floor=secondary_floor,
        anchor_floor=anchor_floor,
    )
    matched = b_match(scores, candidates, capacity=capacity)
    anchor_set = set(anchors)
    for pair in anchors:                     # anchors are never dropped
        if pair not in matched:
            matched.append(pair)
    matched = sorted(set(matched))

    deg_left: dict[int, int] = {}
    deg_right: dict[int, int] = {}
    for i, j in matched:
        deg_left[i] = deg_left.get(i, 0) + 1
        deg_right[j] = deg_right.get(j, 0) + 1

    pairs: list[AcceptedPair] = []
    for i, j in matched:
        dl, dr = deg_left[i], deg_right[j]
        if dl > 1 and dr > 1:
            relation = "split" if dl >= dr else "merge"
        elif dl > 1:
            relation = "split"
        elif dr > 1:
            relation = "merge"
        else:
            relation = "1:1"
        score = float(scores[i, j])
        # Weak applies to anchors too: mutual-best status does not make a
        # low-percentile pair trustworthy, it only makes it the best available.
        if score < weak_floor:
            relation = "weak"
        pairs.append(
            AcceptedPair(
                left=i,
                right=j,
                score=round(score, 4),
                relation=relation,
                anchor=(i, j) in anchor_set,
            )
        )

    # Reading-order divergence: pairs off the longest increasing subsequence
    # are genuinely reordered rather than merely non-monotonic neighbours.
    pairs.sort(key=lambda p: (p.left, p.right))
    keep = set(lis_indices([p.right for p in pairs]))
    for idx, p in enumerate(pairs):
        p.moved = idx not in keep

    return Alignment(
        pairs=pairs,
        left_only=[i for i in range(n) if i not in deg_left],
        right_only=[j for j in range(m) if j not in deg_right],
        n_anchors=len(anchors),
        lis_length=len(keep),
    )


def global_best(scores: np.ndarray, axis: int) -> tuple[np.ndarray, np.ndarray]:
    """Best counterpart anywhere in the other document, and its score.

    Distinguishes "unmatched inside this section pair" (the content is simply
    filed elsewhere) from "no counterpart anywhere" (genuinely novel).
    """
    if scores.size == 0:
        shape = scores.shape[1 - axis] if scores.ndim == 2 else 0
        return np.zeros(shape, dtype=np.int64), np.zeros(shape, dtype=np.float32)
    idx = scores.argmax(axis=axis)
    val = scores.max(axis=axis)
    return idx, val.astype(np.float32)
