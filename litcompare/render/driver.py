"""Builds the report context and renders it through the shared jinja2
template. Layout (`html-table` vs `stacked`) only changes how individual
blocks/excerpts are turned into strings -- the template structure itself is
shared, per the plan ("one context object feeding both layouts").
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import jinja2

from .. import ids
from ..models import ComparisonResult, Document
from . import html as html_layout
from . import stacked as stacked_layout

TEMPLATE_DIR = Path(__file__).parent / "templates"


def _layout_module(name: str):
    return stacked_layout if name == "stacked" else html_layout


def _anchor(path: str, line: int) -> str:
    return f"{path}:{line}"


def _section_excerpt(doc: Document, sid: str) -> str:
    sec = doc.section(sid)
    blocks = doc.rollup_blocks(sid) if sec.is_container else doc.own_blocks(sid)
    for b in blocks:
        if b.raw.strip():
            return b.raw.strip()
    return ""


def _section_size(doc: Document, sid: str) -> int:
    sec = doc.section(sid)
    blocks = doc.rollup_blocks(sid) if sec.is_container else doc.own_blocks(sid)
    return sum(len(b.raw) for b in blocks)


def _heading(doc: Document, sid: str) -> str:
    sec = doc.section(sid)
    return sec.display


def _line(doc: Document, sid: str) -> int:
    return doc.section(sid).line_start


def _build_alignment_rows(result: ComparisonResult, left_doc: Document, right_doc: Document) -> list[dict]:
    n_left = max(len(left_doc.sections), 1)
    n_right = max(len(right_doc.sections), 1)
    entries: list[tuple[float, dict]] = []

    for sm in result.section_matches:
        left_key = _line(left_doc, sm.left_id) if sm.left_id else None
        if left_key is None and sm.right_id:
            key = (_line(right_doc, sm.right_id) / n_right) * n_left
        else:
            key = float(left_key or 0)
        entries.append(
            (
                key,
                {
                    "left_heading": _heading(left_doc, sm.left_id) if sm.left_id else "",
                    "left_anchor": _anchor(result.left_path, _line(left_doc, sm.left_id)) if sm.left_id else "",
                    "cosine": round(sm.cosine, 4),
                    "score": round(sm.score, 4),
                    "right_heading": _heading(right_doc, sm.right_id) if sm.right_id else "",
                    "right_anchor": _anchor(result.right_path, _line(right_doc, sm.right_id)) if sm.right_id else "",
                    "relation": sm.relation,
                    "moved": sm.moved,
                },
            )
        )
    for lid in result.left_only:
        entries.append(
            (
                float(_line(left_doc, lid)),
                {
                    "left_heading": _heading(left_doc, lid),
                    "left_anchor": _anchor(result.left_path, _line(left_doc, lid)),
                    "cosine": None,
                    "score": round(result.section_best.get(lid, 0.0), 4),
                    "right_heading": "",
                    "right_anchor": "",
                    "relation": "left-only",
                    "moved": False,
                },
            )
        )
    for rid in result.right_only:
        key = (_line(right_doc, rid) / n_right) * n_left
        entries.append(
            (
                key,
                {
                    "left_heading": "",
                    "left_anchor": "",
                    "cosine": None,
                    "score": round(result.section_best.get(rid, 0.0), 4),
                    "right_heading": _heading(right_doc, rid),
                    "right_anchor": _anchor(result.right_path, _line(right_doc, rid)),
                    "relation": "right-only",
                    "moved": False,
                },
            )
        )

    entries.sort(key=lambda t: t[0])
    rows = []
    for i, (_, row) in enumerate(entries, start=1):
        row["idx"] = i
        rows.append(row)
    return rows


def _build_pairs(result: ComparisonResult, left_doc: Document, right_doc: Document, layout, limit: int) -> list[dict]:
    pairs = []
    for sm in result.section_matches:
        if not (sm.block_matches or sm.left_only_blocks or sm.right_only_blocks):
            continue
        rows = []
        for bm in sm.block_matches:
            lb, rb = left_doc.block(bm.left_id), right_doc.block(bm.right_id)
            row = {
                "left_html": layout.render_block(lb, limit=limit),
                "right_html": layout.render_block(rb, limit=limit),
                "sim": round(bm.score, 4),
                "left_anchor": _anchor(result.left_path, lb.line_start),
                "right_anchor": _anchor(result.right_path, rb.line_start),
                "inline_diff": layout.render_inline_diff(bm.inline_diff) if bm.inline_diff else "",
                "numeric_deltas": bm.numeric_deltas,
            }
            rows.append(row)
        left_only_rows = [
            {
                "html": layout.render_block(left_doc.block(bid), limit=limit),
                "anchor": _anchor(result.left_path, left_doc.block(bid).line_start),
            }
            for bid in sm.left_only_blocks
        ]
        right_only_rows = [
            {
                "html": layout.render_block(right_doc.block(bid), limit=limit),
                "anchor": _anchor(result.right_path, right_doc.block(bid).line_start),
            }
            for bid in sm.right_only_blocks
        ]
        pairs.append(
            {
                "left_heading": _heading(left_doc, sm.left_id) if sm.left_id else "",
                "right_heading": _heading(right_doc, sm.right_id) if sm.right_id else "",
                "relation": sm.relation,
                "moved": sm.moved,
                "score": round(sm.score, 4),
                "anchor_slug": ids.slug(f"{sm.left_id}-{sm.right_id}"),
                "rows": rows,
                "left_only_rows": left_only_rows,
                "right_only_rows": right_only_rows,
            }
        )
    return pairs


def _build_only(
    result: ComparisonResult, doc: Document, ids_list: list[str], other_path: str, limit: int, layout
) -> list[dict]:
    out = []
    for sid in ids_list:
        out.append(
            {
                "heading": _heading(doc, sid),
                "anchor": _anchor(doc.path, _line(doc, sid)),
                "size_chars": _section_size(doc, sid),
                "best_match": round(result.section_best.get(sid, 0.0), 4),
                "excerpt": layout.render_excerpt(_section_excerpt(doc, sid), limit=limit),
            }
        )
    return out


def render(result: ComparisonResult, left_doc: Document, right_doc: Document, params) -> str:
    layout = _layout_module(params.layout)
    limit = params.excerpt_chars

    ctx = {
        "left_title": result.left_title,
        "right_title": result.right_title,
        "left_path": result.left_path,
        "right_path": result.right_path,
        "model_id": result.model_id,
        "model_revision": result.model_revision,
        "params": result.params,
        "calibration": dataclasses.asdict(result.calibration),
        "generated_at": result.generated_at,
        "warnings": result.warnings,
        "metrics": result.metrics,
        "layout": params.layout,
        "alignment_rows": _build_alignment_rows(result, left_doc, right_doc),
        "pairs": _build_pairs(result, left_doc, right_doc, layout, limit),
        "left_only": _build_only(result, left_doc, result.left_only, result.right_path, limit, layout),
        "right_only": _build_only(result, right_doc, result.right_only, result.left_path, limit, layout),
        "numerals": result.numerals,
        "citations": result.citations,
        "terminology": result.terminology,
        "table_pairs": result.table_pairs,
        "include_matrix": params.include_matrix,
    }

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("report.md.j2")
    return template.render(**ctx)
