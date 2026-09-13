"""Table-to-table matching and cell-level deltas.

Tables are matched on caption, column headers and row labels rather than on
the body text, which is what pairs a champion loss-rate build-up with a
challenger lifetime build-up (`Balance share`, `LGD`, `Loss rate` in common).

Cell deltas are produced by aligning rows on their labels and columns on their
headers -- never positionally. Champion's backtest rows are 2021/2022/2023
while challenger's are 2022H1..2023H2, so a positional diff would confidently
report `2.29% -> 2.81%`, which is fiction. When alignment is weak the module
declines to emit anything.
"""

from __future__ import annotations

from dataclasses import dataclass

from .models import Block, Document
from .normalize import content_words, unicode_fix

MIN_TABLE_SCORE = 0.22
MIN_ALIGN_CONFIDENCE = 0.5
CELL_TOL = 1e-9


def _toks(text: str) -> set[str]:
    return set(content_words(unicode_fix(text)))


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


@dataclass(slots=True)
class TablePair:
    left_id: str
    right_id: str
    score: float
    header_jaccard: float
    caption_similarity: float
    column_map: list[tuple[int, int, float]]
    row_map: list[tuple[int, int, float]]
    confidence: float
    deltas: list[dict]
    declined: str = ""

    def as_dict(self) -> dict:
        return {
            "left_id": self.left_id,
            "right_id": self.right_id,
            "score": round(self.score, 4),
            "header_jaccard": round(self.header_jaccard, 4),
            "caption_similarity": round(self.caption_similarity, 4),
            "confidence": round(self.confidence, 4),
            "n_columns_aligned": len(self.column_map),
            "n_rows_aligned": len(self.row_map),
            "deltas": self.deltas,
            "declined": self.declined,
        }


def _table_blocks(doc: Document) -> list[Block]:
    return [
        b
        for b in doc.blocks
        if b.kind == "table" and b.table and b.table.headers and b.table.rows
    ]


def _greedy_pairs(
    scores: list[list[float]], threshold: float
) -> list[tuple[int, int, float]]:
    """Deterministic greedy mutual pairing; sizes here are tiny."""
    flat = sorted(
        ((s, i, j) for i, row in enumerate(scores) for j, s in enumerate(row)),
        key=lambda t: (-t[0], t[1], t[2]),
    )
    used_l: set[int] = set()
    used_r: set[int] = set()
    out: list[tuple[int, int, float]] = []
    for s, i, j in flat:
        if s < threshold or i in used_l or j in used_r:
            continue
        used_l.add(i)
        used_r.add(j)
        out.append((i, j, round(s, 4)))
    return sorted(out)


def _cell_number(cell: str) -> float | None:
    txt = unicode_fix(cell).strip().strip("*").replace(",", "").replace("%", "")
    txt = txt.replace("$", "").strip()
    try:
        return float(txt)
    except ValueError:
        return None


def compare_pair(left: Block, right: Block) -> TablePair:
    lt, rt = left.table, right.table
    assert lt and rt
    header_j = _jaccard(
        {w for h in lt.headers for w in _toks(h)},
        {w for h in rt.headers for w in _toks(h)},
    )
    cap_sim = _jaccard(_toks(lt.caption or left.caption), _toks(rt.caption or right.caption))
    score = 0.6 * header_j + 0.4 * cap_sim

    col_scores = [[_jaccard(_toks(a), _toks(b)) for b in rt.headers] for a in lt.headers]
    column_map = _greedy_pairs(col_scores, 0.34)

    l_labels = [r[0] if r else "" for r in lt.rows]
    r_labels = [r[0] if r else "" for r in rt.rows]
    row_scores = [[_jaccard(_toks(a), _toks(b)) for b in r_labels] for a in l_labels]
    row_map = _greedy_pairs(row_scores, 0.34)

    denom = max(min(len(lt.rows), len(rt.rows)), 1)
    confidence = len(row_map) / denom if column_map else 0.0

    pair = TablePair(
        left_id=left.id,
        right_id=right.id,
        score=score,
        header_jaccard=header_j,
        caption_similarity=cap_sim,
        column_map=column_map,
        row_map=row_map,
        confidence=confidence,
        deltas=[],
    )
    if confidence < MIN_ALIGN_CONFIDENCE:
        pair.declined = (
            "row labels do not align (positional diffing would invent changes)"
        )
        return pair

    for li, ri, _ in row_map:
        for lc, rc, _ in column_map:
            if lc == 0 or rc == 0:
                continue  # the label column itself
            lrow, rrow = lt.rows[li], rt.rows[ri]
            if lc >= len(lrow) or rc >= len(rrow):
                continue
            a, b = lrow[lc].strip(), rrow[rc].strip()
            if not a or not b or a == b:
                continue
            na, nb = _cell_number(a), _cell_number(b)
            if na is None or nb is None:
                continue
            if abs(na - nb) <= CELL_TOL:
                continue
            pair.deltas.append(
                {
                    "row": lrow[0],
                    "right_row": rrow[0],
                    "column": lt.headers[lc] if lc < len(lt.headers) else "",
                    "right_column": rt.headers[rc] if rc < len(rt.headers) else "",
                    "from": a,
                    "to": b,
                    "relative_diff": round(abs(na - nb) / max(abs(na), abs(nb), 1e-9), 4),
                }
            )
    return pair


def match(left_doc: Document, right_doc: Document, *, top: int = 12) -> list[TablePair]:
    left, right = _table_blocks(left_doc), _table_blocks(right_doc)
    if not left or not right:
        return []
    scored = []
    for a in left:
        for b in right:
            p = compare_pair(a, b)
            if p.score >= MIN_TABLE_SCORE:
                scored.append(p)
    scored.sort(key=lambda p: (-p.score, p.left_id, p.right_id))
    used_l: set[str] = set()
    used_r: set[str] = set()
    out: list[TablePair] = []
    for p in scored:
        if p.left_id in used_l or p.right_id in used_r:
            continue
        used_l.add(p.left_id)
        used_r.add(p.right_id)
        out.append(p)
        if len(out) >= top:
            break
    return out
