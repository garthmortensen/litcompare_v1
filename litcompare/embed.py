"""Embedding backends and the content-addressed vector cache.

The `Embedder` protocol exists so that (a) the model is a config value and
(b) the test suite can run fully offline with a deterministic stand-in that
still has real similarity structure.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Protocol, Sequence

import numpy as np

from . import NORMALIZER_VERSION, PARSER_VERSION, ids
from .normalize import content_words

# Hugging Face tokenizers fork per process and make runs non-reproducible in
# wall-clock order; embeddings are unaffected but logs and timings are not.
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CACHE_ROOT = Path(".litcompare_cache")


class Embedder(Protocol):
    model_id: str
    model_revision: str
    dim: int
    max_tokens: int

    def encode(self, texts: Sequence[str]) -> np.ndarray: ...
    def count_tokens(self, text: str) -> int: ...


def _hf_snapshot_sha(model_id: str) -> str:
    """Resolve the local HF cache snapshot sha, so runs are pinnable."""
    slug = "models--" + model_id.replace("/", "--")
    for root in (
        Path(os.environ.get("HF_HOME", "~/.cache/huggingface")).expanduser() / "hub",
        Path("~/.cache/huggingface/hub").expanduser(),
    ):
        snaps = root / slug / "snapshots"
        if snaps.is_dir():
            entries = sorted(p.name for p in snaps.iterdir() if p.is_dir())
            if entries:
                return entries[0]
    return "unknown"


class SentenceTransformerEmbedder:
    """Local sentence-transformers backend. Lazy-loads on first encode."""

    def __init__(
        self,
        model_id: str = DEFAULT_MODEL,
        *,
        revision: str | None = None,
        device: str = "cpu",
        batch_size: int = 32,
        threads: int | None = None,
    ) -> None:
        self.model_id = model_id
        self.model_revision = revision or _hf_snapshot_sha(model_id)
        self.device = device
        self.batch_size = batch_size
        self.threads = threads
        self._model = None
        self._dim = 0
        self._max_tokens = 256

    def _load(self):
        if self._model is None:
            import torch
            from sentence_transformers import SentenceTransformer

            if self.threads:
                torch.set_num_threads(self.threads)
            kwargs = {"device": self.device}
            if self.model_revision != "unknown":
                kwargs["revision"] = self.model_revision
            self._model = SentenceTransformer(self.model_id, **kwargs)
            self._model.eval()
            self._dim = int(self._model.get_sentence_embedding_dimension())
            self._max_tokens = int(self._model.max_seq_length) - 2  # [CLS]/[SEP]
        return self._model

    @property
    def dim(self) -> int:
        self._load()
        return self._dim

    @property
    def max_tokens(self) -> int:
        self._load()
        return self._max_tokens

    def count_tokens(self, text: str) -> int:
        m = self._load()
        return len(m.tokenizer.tokenize(text))

    def encode(self, texts: Sequence[str]) -> np.ndarray:
        import torch

        m = self._load()
        if not texts:
            return np.zeros((0, self._dim), dtype=np.float32)
        # No query instruction prefix: this is symmetric similarity, not
        # asymmetric retrieval. Pooling comes from the model's own config,
        # so CLS-pooled models (bge) are handled correctly without special
        # casing here.
        with torch.inference_mode():
            vecs = m.encode(
                list(texts),
                batch_size=self.batch_size,
                normalize_embeddings=True,
                show_progress_bar=False,
                convert_to_numpy=True,
            )
        return np.ascontiguousarray(vecs, dtype=np.float32)


CONCEPT_LEXICON: dict[str, tuple[str, ...]] = {
    "pd": ("pd", "probability", "default", "hazard", "logistic", "logit", "scorecard",
           "defaulted", "survival", "attrition", "roll", "delinquency"),
    "ead": ("ead", "exposure", "ccf", "drawdown", "utilization", "balance", "balances",
            "limit", "line", "lines", "commitment", "undrawn", "conversion", "simulated"),
    "lgd": ("lgd", "recovery", "recoveries", "severity", "collections", "recovered",
            "charge-off", "discount", "discounted", "bankruptcy", "agency", "beta"),
    "validation": ("validation", "backtest", "calibration", "gini", "auc", "ks", "holdout",
                   "discriminatory", "discrimination", "realized", "predicted", "error"),
    "data": ("data", "panel", "sample", "portfolio", "cohort", "account", "accounts",
             "segment", "segments", "observation", "feed", "lineage", "quarterly"),
    "governance": ("governance", "control", "controls", "monitoring", "promotion",
                   "limitation", "limitations", "finding", "findings", "recommend",
                   "recommendation", "psi", "refit", "judgmental", "overlay"),
    "refs": ("journal", "review", "studies", "quantitative", "econometrics", "al",
             "communications", "statistics", "forecasting"),
    "math": ("equation", "sum", "product", "decomposition", "estimator", "regression",
             "coefficient", "notation", "estimated", "weighted", "mean"),
}


class ConceptEmbedder:
    """Deterministic, offline stand-in with real similarity structure.

    A hash-based fake embedder can only test plumbing: its vectors have no
    meaningful geometry, so no threshold, gate or assignment behaviour can be
    asserted against it. This one scores text against a small concept lexicon,
    which is enough to assert that `4.2 Probability of default` matches
    `Default hazard` and that a bibliography does not.
    """

    model_id = "concept-lexicon-v1"
    model_revision = "builtin"

    def __init__(self) -> None:
        self.concepts = sorted(CONCEPT_LEXICON)
        self.dim = len(self.concepts) + 1
        self.max_tokens = 10_000

    def count_tokens(self, text: str) -> int:
        return len(text.split())

    def encode(self, texts: Sequence[str]) -> np.ndarray:
        out = np.zeros((len(texts), self.dim), dtype=np.float32)
        for i, text in enumerate(texts):
            words = content_words(text)
            if not words:
                out[i, -1] = 1.0
                continue
            for j, concept in enumerate(self.concepts):
                keys = CONCEPT_LEXICON[concept]
                out[i, j] = sum(1 for w in words if w in keys or any(w.startswith(k) for k in keys))
            out[i, -1] = 0.35 * len(words) ** 0.5   # generic-prose component
        norms = np.linalg.norm(out, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return out / norms


class ChunkCache:
    """Content-addressed store: one vector per unique normalized chunk text.

    Keyed by text hash rather than by document, so identical citations shared
    across papers embed once and editing one section does not invalidate the
    rest of a document. The directory is keyed by a pipeline fingerprint, so a
    parser or model change cannot silently serve stale vectors.
    """

    def __init__(self, embedder: Embedder, root: Path | str = CACHE_ROOT, enabled: bool = True):
        self.embedder = embedder
        self.enabled = enabled
        self.fingerprint = self._fingerprint(embedder)
        self.root = Path(root) / self.fingerprint
        self.hits = 0
        self.misses = 0
        if self.enabled:
            self.root.mkdir(parents=True, exist_ok=True)
            meta = self.root / "meta.json"
            if not meta.exists():
                self._atomic_write_text(
                    meta,
                    json.dumps(
                        {
                            "model_id": embedder.model_id,
                            "model_revision": embedder.model_revision,
                            "parser_version": PARSER_VERSION,
                            "normalizer_version": NORMALIZER_VERSION,
                        },
                        indent=2,
                    ),
                )

    @staticmethod
    def _fingerprint(embedder: Embedder) -> str:
        key = "|".join(
            [
                str(PARSER_VERSION),
                str(NORMALIZER_VERSION),
                embedder.model_id,
                embedder.model_revision,
            ]
        )
        return re.sub(r"[^A-Za-z0-9_.-]", "_", embedder.model_id.split("/")[-1]) + "-" + ids.short_hash(key, 10)

    def _path(self, h: str) -> Path:
        return self.root / h[:2] / f"{h}.npy"

    @staticmethod
    def _atomic_write_text(path: Path, text: str) -> None:
        tmp = path.with_suffix(path.suffix + f".tmp{os.getpid()}")
        tmp.write_text(text, encoding="utf-8")
        tmp.replace(path)

    def _atomic_write_array(self, path: Path, arr: np.ndarray) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        # `np.save` appends `.npy` to any filename that doesn't already end
        # in it, which silently breaks a `.tmp{pid}`-suffixed temp name (the
        # file lands at `...tmp{pid}.npy`, not the path we then try to
        # rename). Keep `.npy` as the actual suffix so the write and the
        # rename target agree.
        tmp = path.parent / f"{path.stem}.tmp{os.getpid()}.npy"
        np.save(tmp, arr)
        tmp.replace(path)

    def encode(self, texts: Sequence[str]) -> np.ndarray:
        """Return (n, dim) float32, L2-normalised, in the order given."""
        if not texts:
            return np.zeros((0, self.embedder.dim), dtype=np.float32)
        if not self.enabled:
            return self.embedder.encode(texts)

        hashes = [ids.content_hash(t) for t in texts]
        vectors: list[np.ndarray | None] = []
        for h in hashes:
            p = self._path(h)
            if p.exists():
                try:
                    vectors.append(np.load(p))
                    self.hits += 1
                    continue
                except Exception:
                    pass  # corrupt entry: fall through and re-embed
            vectors.append(None)

        missing = [i for i, v in enumerate(vectors) if v is None]
        if missing:
            fresh = self.embedder.encode([texts[i] for i in missing])
            self.misses += len(missing)
            for k, i in enumerate(missing):
                vec = np.ascontiguousarray(fresh[k], dtype=np.float32)
                vectors[i] = vec
                self._atomic_write_array(self._path(hashes[i]), vec)

        out = np.vstack([v for v in vectors if v is not None]).astype(np.float32)
        if out.shape[0] != len(texts):
            raise RuntimeError("cache returned wrong number of vectors")
        return out

    def stats(self) -> dict[str, object]:
        n = sum(1 for _ in self.root.rglob("*.npy")) if self.root.is_dir() else 0
        return {
            "fingerprint": self.fingerprint,
            "entries": n,
            "hits": self.hits,
            "misses": self.misses,
            "root": str(self.root),
        }
