"""Block -> Chunk, respecting the model's token budget."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .models import Document
from .normalize import content_words

_SENT = re.compile(r"(?<=[.!?;])\s+")

CHUNK_OVERLAP = 0.15


@dataclass(slots=True)
class Chunk:
    id: str
    block_id: str
    section_id: str
    text: str
    weight: int          # content-word count, used for weighted means


def chunk_document(doc: Document, max_tokens: int, count_tokens) -> list[Chunk]:
    """One chunk per block where it fits, else sentence-boundary windows."""
    out: list[Chunk] = []
    for blk in doc.blocks:
        text = blk.normalized
        if not text:
            continue
        if count_tokens(text) <= max_tokens:
            out.append(Chunk(f"{blk.id}#0", blk.id, blk.section_id, text, max(blk.token_count, 1)))
            continue
        for n, piece in enumerate(_windows(text, max_tokens, count_tokens)):
            out.append(
                Chunk(f"{blk.id}#{n}", blk.id, blk.section_id, piece, max(len(content_words(piece)), 1))
            )
    return out


def _windows(text: str, max_tokens: int, count_tokens) -> list[str]:
    sents = [s for s in _SENT.split(text) if s.strip()] or [text]
    windows: list[str] = []
    cur: list[str] = []
    for sent in sents:
        trial = cur + [sent]
        if cur and count_tokens(" ".join(trial)) > max_tokens:
            windows.append(" ".join(cur))
            keep = max(1, int(len(cur) * CHUNK_OVERLAP))
            cur = cur[-keep:] + [sent]
        else:
            cur = trial
    if cur:
        windows.append(" ".join(cur))
    # A single sentence longer than the budget still has to go somewhere; the
    # tokenizer truncates it, which is acceptable for a tail fragment.
    return windows
