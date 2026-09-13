"""Chunk vectors -> section vectors.

Three decisions here carry most of the matching quality:

* **Leaf and rollup vectors.** Container headings own no blocks, so a plain
  mean over own chunks is NaN. Rollup (own + descendants) gives them a real
  vector and also produces the coarse top-level map.
* **Heading as a pseudo-chunk.** Rather than a fixed blend weight, the
  stripped heading path is mixed in as a ~20-token chunk. Short sections are
  therefore influenced by their heading and long ones are not, with no knob.
* **Capped weights for tables and equations.** Tables are ~25% of non-blank
  lines in these papers and must stay in the vector (removing them measurably
  hurts), but uncapped they collapse every results section onto one attractor.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .chunk import Chunk
from .models import Block, Document
from .normalize import content_words, strip_heading_prefix

HEADING_PSEUDO_TOKENS = 20
TABLE_WEIGHT_CAP = 30
MATH_WEIGHT_CAP = 8
HEADING_PATH_DEPTH = 2


def block_weight(blk: Block) -> int:
    w = max(blk.token_count, 1)
    if blk.kind == "table":
        return min(w, TABLE_WEIGHT_CAP)
    if blk.kind == "math":
        return min(w, MATH_WEIGHT_CAP)
    return w


def heading_text(doc: Document, sid: str) -> str:
    """Stripped heading plus its nearest ancestor, without ordinals.

    `Part II - The Framework` reduced to `The Framework` stops `Part`, `Annex`
    and digits from dominating what is often a three-word string.
    """
    sec = doc.section(sid)
    path = [strip_heading_prefix(h) for h in sec.heading_path if h.strip()]
    return " ".join(path[-HEADING_PATH_DEPTH:])


@dataclass(slots=True)
class DocVectors:
    doc: Document
    chunks: list[Chunk]
    chunk_vecs: np.ndarray
    leaf: dict[str, np.ndarray]
    rollup: dict[str, np.ndarray]
    block_vecs: dict[str, np.ndarray]
    doc_vec: np.ndarray

    def align_vec(self, sid: str) -> np.ndarray:
        """Vector used for alignment: rollup for containers, leaf otherwise."""
        sec = self.doc.section(sid)
        return self.rollup[sid] if sec.is_container else self.leaf[sid]


def _normalize(v: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(v))
    return v / n if n > 0 else v


def build(doc: Document, chunks: list[Chunk], chunk_vecs: np.ndarray, encode) -> DocVectors:
    by_block: dict[str, list[int]] = {}
    for i, ch in enumerate(chunks):
        by_block.setdefault(ch.block_id, []).append(i)

    # One embedding per section heading, batched.
    sids = [s.id for s in doc.sections]
    head_texts = [heading_text(doc, sid) or doc.title for sid in sids]
    head_vecs = encode(head_texts)
    head_by_sid = dict(zip(sids, head_vecs))

    block_vecs: dict[str, np.ndarray] = {}
    for blk in doc.blocks:
        idx = by_block.get(blk.id)
        if not idx:
            continue
        w = np.array([chunks[i].weight for i in idx], dtype=np.float32)
        block_vecs[blk.id] = _normalize((chunk_vecs[idx] * w[:, None]).sum(axis=0))

    def combine(blocks: list[Block], sid: str) -> np.ndarray:
        acc = np.zeros(chunk_vecs.shape[1], dtype=np.float32)
        total = 0.0
        for blk in blocks:
            idx = by_block.get(blk.id)
            if not idx:
                continue
            w = block_weight(blk) / len(idx)
            for i in idx:
                acc += w * chunk_vecs[i]
                total += w
        hw = float(HEADING_PSEUDO_TOKENS)
        acc += hw * head_by_sid[sid]
        total += hw
        return _normalize(acc / max(total, 1e-9))

    leaf: dict[str, np.ndarray] = {}
    rollup: dict[str, np.ndarray] = {}
    for sec in doc.sections:
        leaf[sec.id] = combine(doc.own_blocks(sec.id), sec.id)
        rollup[sec.id] = combine(doc.rollup_blocks(sec.id), sec.id)

    # Document vector excludes bibliography and front matter, which otherwise
    # drag every pair of academic papers toward each other.
    body = [
        b
        for b in doc.blocks
        if b.kind not in ("citation", "frontmatter")
        and doc.section(b.section_id).kind not in ("bibliography", "frontmatter")
    ]
    acc = np.zeros(chunk_vecs.shape[1], dtype=np.float32)
    for blk in body:
        v = block_vecs.get(blk.id)
        if v is not None:
            acc += block_weight(blk) * v
    doc_vec = _normalize(acc)

    return DocVectors(doc, chunks, chunk_vecs, leaf, rollup, block_vecs, doc_vec)


def content_token_total(doc: Document) -> int:
    return sum(
        len(content_words(b.normalized))
        for b in doc.blocks
        if b.kind not in ("citation", "frontmatter")
    )
