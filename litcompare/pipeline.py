"""Wires the stages together: parse -> chunk+embed -> vectors -> signals ->
calibrate -> align -> facts -> metrics -> ComparisonResult.

Kept as one function rather than a class: every stage below it is a pure
function over `models.py` dataclasses, so this is just the glue, not logic
in its own right.
"""

from __future__ import annotations

import datetime as dt

import numpy as np

from . import align, calibrate, chunk, citations, deltas, lexical, metrics, numerals, tables, vectors
from .config import Params
from .embed import ChunkCache, Embedder, SentenceTransformerEmbedder
from .models import BlockMatch, Calibration, ComparisonResult, Document, SectionMatch
from .parse import parse_file


def _section_text(doc: Document, sid: str) -> str:
    sec = doc.section(sid)
    blocks = doc.rollup_blocks(sid) if sec.is_container else doc.own_blocks(sid)
    return " ".join(b.normalized for b in blocks)


def _alignable_blocks(doc: Document) -> list[str]:
    """Block ids eligible for block-level signal/coverage -- see Document.alignable_sections."""
    alignable_sids = {s.id for s in doc.alignable_sections}
    return [b.id for b in doc.blocks if b.section_id in alignable_sids]


def _blend(embed_sim: np.ndarray, lexical_sim: np.ndarray, params: Params) -> np.ndarray:
    if params.calibration == "absolute":
        if lexical_sim.shape != embed_sim.shape:
            return embed_sim
        return np.round(params.blend_weight * embed_sim + (1.0 - params.blend_weight) * lexical_sim, 4)
    return calibrate.blend(embed_sim, lexical_sim, weight=params.blend_weight)


def _bib_section(doc: Document) -> str | None:
    bibs = [s.id for s in doc.sections if s.kind == "bibliography"]
    return bibs[0] if len(bibs) == 1 else None


def compare(
    left_path: str,
    right_path: str,
    params: Params | None = None,
    *,
    embedder: Embedder | None = None,
) -> tuple[ComparisonResult, Document, Document]:
    params = params or Params()
    left_doc = parse_file(left_path, "left")
    right_doc = parse_file(right_path, "right")

    base_embedder = embedder or SentenceTransformerEmbedder(
        params.model, revision=params.revision, device=params.device,
        batch_size=params.batch_size, threads=params.threads,
    )
    cache = ChunkCache(base_embedder, enabled=params.cache)

    max_tokens = base_embedder.max_tokens
    chunks_left = chunk.chunk_document(left_doc, max_tokens, base_embedder.count_tokens)
    chunks_right = chunk.chunk_document(right_doc, max_tokens, base_embedder.count_tokens)

    vecs_left = cache.encode([c.text for c in chunks_left])
    vecs_right = cache.encode([c.text for c in chunks_right])

    left_vecs = vectors.build(left_doc, chunks_left, vecs_left, cache.encode)
    right_vecs = vectors.build(right_doc, chunks_right, vecs_right, cache.encode)

    doc_cosine = float(np.dot(left_vecs.doc_vec, right_vecs.doc_vec))

    # -- section-level signals -------------------------------------------
    # Containers (headings with no own blocks) are deliberately excluded from
    # the primary alignment pool, not just given a rollup vector. A rollup
    # vector aggregates an entire subtree, so a container competes for every
    # candidate slot its own children want -- measured on the fixtures,
    # leaving containers in caused `4. Methodology`'s rollup to out-rank
    # `4.2 Probability of default` for `Default hazard` (the canonical test
    # pair), and `2. Related Work` to spuriously "merge" into `Part II` via
    # the same broad-rollup effect the bibliography module already had to
    # route around for `References` vs `Selected References`. Containers are
    # still surfaced in the report -- see below -- just never as a match.
    left_sec_ids = [s.id for s in left_doc.alignable_sections if not s.is_container]
    right_sec_ids = [s.id for s in right_doc.alignable_sections if not s.is_container]
    left_container_ids = [s.id for s in left_doc.alignable_sections if s.is_container]
    right_container_ids = [s.id for s in right_doc.alignable_sections if s.is_container]
    left_sec_vecs = np.stack([left_vecs.align_vec(sid) for sid in left_sec_ids]) if left_sec_ids else np.zeros((0, left_vecs.doc_vec.shape[0]), dtype=np.float32)
    right_sec_vecs = np.stack([right_vecs.align_vec(sid) for sid in right_sec_ids]) if right_sec_ids else np.zeros((0, right_vecs.doc_vec.shape[0]), dtype=np.float32)

    sec_embed_sim = calibrate.cosine_matrix(left_sec_vecs, right_sec_vecs)
    left_sec_texts = [_section_text(left_doc, sid) for sid in left_sec_ids]
    right_sec_texts = [_section_text(right_doc, sid) for sid in right_sec_ids]
    sec_lexical_sim = lexical.cross_similarity(left_sec_texts, right_sec_texts)
    sec_blended = _blend(sec_embed_sim, sec_lexical_sim, params)

    calibration: Calibration = calibrate.describe(sec_embed_sim, sec_lexical_sim, params.calibration)

    section_alignment = align.align(
        sec_blended,
        top_k=params.section_top_k,
        margin=params.section_margin,
        secondary_floor=params.section_secondary_floor,
        anchor_floor=params.section_anchor_floor,
        capacity=params.section_capacity,
        weak_floor=params.section_weak_floor,
    )

    # -- global block-level signal, for coverage + within-section matching --
    left_block_ids = _alignable_blocks(left_doc)
    right_block_ids = _alignable_blocks(right_doc)
    left_block_vecs = np.stack([left_vecs.block_vecs[b] for b in left_block_ids]) if left_block_ids else np.zeros((0, left_vecs.doc_vec.shape[0]), dtype=np.float32)
    right_block_vecs = np.stack([right_vecs.block_vecs[b] for b in right_block_ids]) if right_block_ids else np.zeros((0, right_vecs.doc_vec.shape[0]), dtype=np.float32)
    blk_embed_sim = calibrate.cosine_matrix(left_block_vecs, right_block_vecs)
    left_block_texts = [left_doc.block(b).normalized for b in left_block_ids]
    right_block_texts = [right_doc.block(b).normalized for b in right_block_ids]
    blk_lexical_sim = lexical.cross_similarity(left_block_texts, right_block_texts)
    blk_blended = _blend(blk_embed_sim, blk_lexical_sim, params)

    _, left_best_scores = align.global_best(blk_blended, axis=1) if blk_blended.size else (np.zeros(0), np.zeros(len(left_block_ids), dtype=np.float32))
    _, right_best_scores = align.global_best(blk_blended, axis=0) if blk_blended.size else (np.zeros(0), np.zeros(len(right_block_ids), dtype=np.float32))
    left_best = {bid: float(s) for bid, s in zip(left_block_ids, left_best_scores)}
    right_best = {bid: float(s) for bid, s in zip(right_block_ids, right_best_scores)}

    left_idx_of = {b: i for i, b in enumerate(left_block_ids)}
    right_idx_of = {b: i for i, b in enumerate(right_block_ids)}

    def _block_match(lid: str, rid: str) -> BlockMatch:
        li, ri = left_idx_of[lid], right_idx_of[rid]
        score = float(blk_blended[li, ri])
        lb, rb = left_doc.block(lid), right_doc.block(rid)
        inline = ""
        ndeltas: list[dict] = []
        if score >= params.inline_diff_floor:
            inline = deltas.inline_diff(lb.raw, rb.raw)
            ndeltas = deltas.numeric_changes(lb.raw, rb.raw)
        return BlockMatch(
            left_id=lid, right_id=rid, score=round(score, 4),
            cosine=float(blk_embed_sim[li, ri]), lexical=float(blk_lexical_sim[li, ri]) if blk_lexical_sim.size else 0.0,
            inline_diff=inline, numeric_deltas=ndeltas,
        )

    section_matches: list[SectionMatch] = []
    for p in section_alignment.pairs:
        lsid, rsid = left_sec_ids[p.left], right_sec_ids[p.right]
        lb_ids = [b.id for b in left_doc.own_blocks(lsid) if b.id in left_idx_of]
        rb_ids = [b.id for b in right_doc.own_blocks(rsid) if b.id in right_idx_of]
        sub = np.zeros((len(lb_ids), len(rb_ids)), dtype=np.float32)
        for i, lid in enumerate(lb_ids):
            for j, rid in enumerate(rb_ids):
                sub[i, j] = blk_blended[left_idx_of[lid], right_idx_of[rid]]
        block_alignment = align.align(
            sub, top_k=params.block_top_k, margin=params.block_margin,
            secondary_floor=params.block_secondary_floor, anchor_floor=params.block_anchor_floor,
            capacity=params.block_capacity, weak_floor=params.block_weak_floor,
        )
        block_matches = [_block_match(lb_ids[bp.left], rb_ids[bp.right]) for bp in block_alignment.pairs]
        section_matches.append(
            SectionMatch(
                left_id=lsid, right_id=rsid, score=p.score,
                cosine=float(sec_embed_sim[p.left, p.right]),
                lexical=float(sec_lexical_sim[p.left, p.right]) if sec_lexical_sim.size else 0.0,
                relation=p.relation, moved=p.moved,
                block_matches=block_matches,
                left_only_blocks=[lb_ids[i] for i in block_alignment.left_only],
                right_only_blocks=[rb_ids[i] for i in block_alignment.right_only],
            )
        )

    left_only_sections = [left_sec_ids[i] for i in section_alignment.left_only] + left_container_ids
    right_only_sections = [right_sec_ids[i] for i in section_alignment.right_only] + right_container_ids

    # Bibliographies are handled lexically, not by embedding (see citations.py) --
    # but the two "References"-ish sections still deserve a row in the alignment
    # map, so pair them directly when each side has exactly one.
    citation_cmp = citations.compare(left_doc, right_doc)
    lbib, rbib = _bib_section(left_doc), _bib_section(right_doc)
    if lbib and rbib:
        section_matches.append(
            SectionMatch(
                left_id=lbib, right_id=rbib,
                score=citation_cmp["jaccard"], cosine=0.0, lexical=0.0,
                relation="1:1", moved=False,
            )
        )
    elif lbib:
        left_only_sections.append(lbib)
    elif rbib:
        right_only_sections.append(rbib)

    section_best: dict[str, float] = {}
    for i, lid in enumerate(left_sec_ids):
        if sec_blended.size:
            section_best[lid] = float(sec_blended[i, :].max())
    for j, rid in enumerate(right_sec_ids):
        if sec_blended.size:
            section_best[rid] = float(sec_blended[:, j].max())
    # Containers never entered the matrix above; score them against the
    # (leaf-only) other side directly off their rollup vector.
    for cid in left_container_ids:
        section_best[cid] = float((right_sec_vecs @ left_vecs.align_vec(cid)).max()) if right_sec_vecs.size else 0.0
    for cid in right_container_ids:
        section_best[cid] = float((left_sec_vecs @ right_vecs.align_vec(cid)).max()) if left_sec_vecs.size else 0.0

    metrics_dict, warnings = metrics.build(left_doc, right_doc, section_alignment, left_best, right_best, doc_cosine)

    numerals_dict = numerals.cross_index(left_doc, right_doc)
    numerals_dict["left_internal_inconsistencies"] = numerals.internal_inconsistencies(left_doc)
    numerals_dict["right_internal_inconsistencies"] = numerals.internal_inconsistencies(right_doc)

    left_terms, right_terms = lexical.distinctive_terms(
        [b.normalized for b in left_doc.blocks if b.id in left_idx_of],
        [b.normalized for b in right_doc.blocks if b.id in right_idx_of],
    )
    terminology_dict = {"left_only": left_terms, "right_only": right_terms}

    table_pairs = [tp.as_dict() for tp in tables.match(left_doc, right_doc)]

    result = ComparisonResult(
        left_path=left_path, right_path=right_path,
        left_title=left_doc.title, right_title=right_doc.title,
        model_id=base_embedder.model_id, model_revision=base_embedder.model_revision,
        params=params.to_dict(), calibration=calibration, metrics=metrics_dict,
        section_matches=section_matches, left_only=left_only_sections, right_only=right_only_sections,
        numerals=numerals_dict, citations=citation_cmp, terminology=terminology_dict,
        table_pairs=table_pairs, warnings=warnings,
        generated_at=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        section_best=section_best,
    )
    # Docs are returned alongside the (JSON-serialisable) result because the
    # renderer needs raw block text/line numbers that ComparisonResult itself
    # deliberately does not carry.
    return result, left_doc, right_doc
