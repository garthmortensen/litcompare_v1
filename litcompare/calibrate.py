"""Per-pair score calibration.

Absolute cosine cutoffs cannot work across models or corpora. Measured on the
two fixtures, MiniLM puts 16.6% of section pairs above 0.45 and none above
0.75, while a bge-class model's compressed range puts nearly everything above
0.45. The same constant therefore matches nothing or everything depending on
the backend.

The fix is to score each candidate by its percentile *within this pair's own
cross-document distribution*, and to blend the embedding and lexical channels
on those percentiles rather than on raw values.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import rankdata

from .models import Calibration

ROUND_DP = 4  # CPU BLAS varies with thread count; rounding keeps ties stable


def percentile_matrix(sim: np.ndarray) -> np.ndarray:
    """Map every entry to its rank percentile within the whole matrix."""
    if sim.size == 0:
        return sim.astype(np.float32)
    flat = sim.astype(np.float64).ravel()
    ranks = rankdata(flat, method="average")
    pct = (ranks - 1.0) / max(len(flat) - 1, 1)
    return np.round(pct.reshape(sim.shape), ROUND_DP).astype(np.float32)


def blend(embed_sim: np.ndarray, lexical_sim: np.ndarray, weight: float = 0.5) -> np.ndarray:
    """Blend on percentile ranks, never on raw scores."""
    pe = percentile_matrix(embed_sim)
    pl = percentile_matrix(lexical_sim)
    if pl.shape != pe.shape:
        return pe
    return np.round(weight * pe + (1.0 - weight) * pl, ROUND_DP)


def describe(embed_sim: np.ndarray, lexical_sim: np.ndarray, mode: str) -> Calibration:
    flat = embed_sim.ravel() if embed_sim.size else np.zeros(1, dtype=np.float32)
    lex = lexical_sim.ravel() if lexical_sim.size else np.zeros(1, dtype=np.float32)
    q = np.percentile(flat, [5, 50, 95])
    return Calibration(
        n_pairs=int(embed_sim.size),
        raw_min=round(float(flat.min()), 4),
        raw_p05=round(float(q[0]), 4),
        raw_median=round(float(q[1]), 4),
        raw_p95=round(float(q[2]), 4),
        raw_max=round(float(flat.max()), 4),
        deciles=[round(float(x), 4) for x in np.percentile(flat, list(range(0, 101, 10)))],
        mode=mode,
        lexical_median=round(float(np.median(lex)), 4),
        lexical_max=round(float(lex.max()), 4),
    )


def cosine_matrix(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    """Rows are already L2-normalised, so this is the cosine matrix."""
    if left.size == 0 or right.size == 0:
        return np.zeros((left.shape[0], right.shape[0]), dtype=np.float32)
    return np.round(left @ right.T, ROUND_DP).astype(np.float32)
