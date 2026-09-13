"""TF-IDF channel.

Required, not optional. The embedding channel has a narrow dynamic range on
same-domain papers, while tf-idf has a wide one, and it catches overlap that
embeddings structurally cannot: verbatim figures quoted across the two papers
(`2.84%`, `PSI 0.14`, `200 basis points`, `36-month`) and shared citations.
"""

from __future__ import annotations

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from .normalize import STOPWORDS


def _vectorizer() -> TfidfVectorizer:
    return TfidfVectorizer(
        lowercase=True,
        stop_words=list(STOPWORDS),
        # Keep percentages and decimals as tokens: they are the strongest
        # cross-document evidence in quantitative papers.
        token_pattern=r"(?u)\b[a-zA-Z0-9][a-zA-Z0-9._%/-]*\b",
        sublinear_tf=True,
        min_df=1,
    )


def cross_similarity(left_texts: list[str], right_texts: list[str]) -> np.ndarray:
    """Cosine matrix (len(left), len(right)) from a vocabulary fit on both."""
    if not left_texts or not right_texts:
        return np.zeros((len(left_texts), len(right_texts)), dtype=np.float32)
    vec = _vectorizer()
    try:
        matrix = vec.fit_transform(left_texts + right_texts)
    except ValueError:
        return np.zeros((len(left_texts), len(right_texts)), dtype=np.float32)
    n = len(left_texts)
    left, right = matrix[:n], matrix[n:]
    sim = (left @ right.T).toarray().astype(np.float32)
    return np.nan_to_num(sim, nan=0.0)


def distinctive_terms(
    left_texts: list[str], right_texts: list[str], top: int = 25
) -> tuple[list[tuple[str, float]], list[tuple[str, float]]]:
    """Terms carrying the most weight on one side and ~none on the other."""
    if not left_texts or not right_texts:
        return [], []
    vec = _vectorizer()
    matrix = vec.fit_transform([" ".join(left_texts), " ".join(right_texts)])
    terms = np.array(vec.get_feature_names_out())
    dense = matrix.toarray()
    lhs, rhs = dense[0], dense[1]
    left_only = [(terms[i], round(float(lhs[i]), 4)) for i in np.argsort(-(lhs - rhs)) if rhs[i] == 0][:top]
    right_only = [(terms[i], round(float(rhs[i]), 4)) for i in np.argsort(-(rhs - lhs)) if lhs[i] == 0][:top]
    return left_only, right_only
