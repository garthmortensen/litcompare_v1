"""Numeral cross-index.

The highest-value part of the comparison, and it uses no vectors at all. For
two quantitative papers the substance of the argument lives in the numbers,
and a reviewer needs the *agreements* as much as the differences.

Context is what makes this work or fail. Two rules matter:

* Numbers inside a table take their context from the table's structure --
  caption, column header, row label -- not from a sliding window, which would
  blend every cell in the row together.
* Context never includes digit-bearing tokens. Without that, every percentage
  in one paper "shares context" with every percentage in the other.

It also runs an intra-document consistency check: champion section 5.3 states
an implied portfolio LGD of 0.853 while its own Table 5 portfolio row says
0.851 -- exactly the kind of finding a validation audience wants surfaced.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass

from .models import Document
from .normalize import content_words, unicode_fix

_UNIT = r"(?:%|bps|basis\s+points|percentage\s+points|pp|cents|bn|bps|x|months?|days?|years?)"
_NUM = re.compile(
    r"(?<![\w.])(-?\d{1,3}(?:,\d{3})+(?:\.\d+)?|-?\d+\.\d+|-?\d+)\s*(" + _UNIT + r")?",
    re.IGNORECASE,
)
_UNIT_CANON = {
    "basis points": "bps",
    "bps": "bps",
    "percentage points": "pp",
    "pp": "pp",
    "%": "%",
    "cents": "cents",
    "bn": "bn",
    "x": "x",
}
_HAS_DIGIT = re.compile(r"\d")

CONTEXT_WORDS = 10
AGREE_TOL = 0.005        # within 0.5% relative -> the papers agree
MAX_REL_DIFF = 0.5       # beyond this they are not the same quantity
MIN_SHARED_CONTEXT = 2
RARE_DF = 0.40


@dataclass(slots=True)
class Numeral:
    value: float
    raw: str
    unit: str
    context: tuple[str, ...]
    # Header/row-label words only, excluding the caption. Two numbers that
    # share only a caption are two different quantities sitting under the same
    # title, so table-to-table pairs must overlap on this narrower context.
    key_context: tuple[str, ...]
    block_id: str
    section: str
    line: int
    source: str = "prose"     # prose | table

    @property
    def display(self) -> str:
        if self.unit == "%":
            return f"{self.raw}%"
        return f"{self.raw} {self.unit}".strip()


def _canon_unit(raw: str | None) -> str:
    if not raw:
        return ""
    key = re.sub(r"\s+", " ", raw.strip().lower())
    return _UNIT_CANON.get(key, key.rstrip("s"))


def _clean_context(words: list[str]) -> list[str]:
    return [w for w in words if not _HAS_DIGIT.search(w) and len(w) > 2]


def _skip(value: float, unit: str) -> bool:
    if unit:
        return False
    if value.is_integer():
        v = int(value)
        if 1900 <= v <= 2100:        # years
            return True
        if abs(v) < 10:              # list ordinals, small counts
            return True
    return False


def _scan(text: str, ctx: tuple[str, ...], key_ctx: tuple[str, ...], blk_id: str,
          section: str, line: int, source: str, sliding: bool) -> list[Numeral]:
    out: list[Numeral] = []
    for m in _NUM.finditer(text):
        try:
            value = float(m.group(1).replace(",", ""))
        except ValueError:
            continue
        unit = _canon_unit(m.group(2))
        if _skip(value, unit):
            continue
        if sliding:
            before = _clean_context(content_words(text[max(0, m.start() - 200):m.start()]))[-CONTEXT_WORDS:]
            after = _clean_context(content_words(text[m.end():m.end() + 90]))[:3]
            local = tuple(dict.fromkeys([*before, *after]))
        else:
            local = ctx
        if len(local) < MIN_SHARED_CONTEXT:
            continue
        keys = local if sliding else key_ctx
        out.append(
            Numeral(value, m.group(1), unit, local, keys, blk_id, section, line, source)
        )
    return out


def extract(doc: Document) -> list[Numeral]:
    out: list[Numeral] = []
    for blk in doc.blocks:
        if blk.kind in ("frontmatter", "citation"):
            continue
        heading = doc.section(blk.section_id).display
        if blk.kind == "table" and blk.table and blk.table.headers:
            cap = _clean_context(content_words(unicode_fix(blk.table.caption or blk.caption)))
            heads = [_clean_context(content_words(unicode_fix(h))) for h in blk.table.headers]
            for row in blk.table.rows:
                if not row:
                    continue
                label = _clean_context(content_words(unicode_fix(row[0])))
                for k, cell in enumerate(row):
                    if k == 0 and not _HAS_DIGIT.search(cell):
                        continue
                    head = heads[k] if k < len(heads) else []
                    ctx = tuple(dict.fromkeys([*cap, *head, *label]))
                    key = tuple(dict.fromkeys([*head, *label]))
                    out.extend(
                        _scan(unicode_fix(cell), ctx, key, blk.id, heading,
                              blk.line_start, "table", sliding=False)
                    )
            continue
        out.extend(
            _scan(unicode_fix(blk.raw), (), (), blk.id, heading, blk.line_start,
                  "prose", sliding=True)
        )
    return out


def _df(nums: list[Numeral]) -> dict[str, float]:
    counter: Counter[str] = Counter()
    for n in nums:
        counter.update(set(n.context))
    total = max(len(nums), 1)
    return {w: c / total for w, c in counter.items()}


def _evidence(shared: tuple[str, ...], df_l: dict[str, float], df_r: dict[str, float]) -> float:
    """Rarity-weighted strength of the shared context."""
    return sum(-math.log(max(df_l.get(w, 1.0), df_r.get(w, 1.0), 1e-3)) for w in shared)


def cross_index(left_doc: Document, right_doc: Document, *, top: int = 30) -> dict:
    left, right = extract(left_doc), extract(right_doc)
    df_l, df_r = _df(left), _df(right)

    by_unit: dict[str, list[Numeral]] = {}
    for n in right:
        by_unit.setdefault(n.unit, []).append(n)

    best: dict[tuple[str, float, float], tuple[float, dict]] = {}
    for a in left:
        for b in by_unit.get(a.unit, ()):
            shared = tuple(sorted(set(a.context) & set(b.context)))
            if len(shared) < MIN_SHARED_CONTEXT:
                continue
            if not any(df_l.get(w, 1.0) < RARE_DF and df_r.get(w, 1.0) < RARE_DF for w in shared):
                continue
            if a.source == "table" and b.source == "table":
                if not (set(a.key_context) & set(b.key_context)):
                    continue
            denom = max(abs(a.value), abs(b.value), 1e-9)
            rel = abs(a.value - b.value) / denom
            if rel > MAX_REL_DIFF:
                continue
            ev = _evidence(shared, df_l, df_r)
            rec = {
                "quantity": " ".join(shared[:6]),
                "left": a.display,
                "left_section": a.section,
                "left_line": a.line,
                "left_source": a.source,
                "right": b.display,
                "right_section": b.section,
                "right_line": b.line,
                "right_source": b.source,
                "relative_diff": round(rel, 5),
                "evidence": round(ev, 2),
                "agrees": rel <= AGREE_TOL,
            }
            key = (" ".join(shared[:6]), a.section, b.section, rec["agrees"])
            cur = best.get(key)
            if cur is None or (ev, -rel) > (cur[0], -cur[1]["relative_diff"]):
                best[key] = (ev, rec)

    ranked = sorted(best.values(), key=lambda t: (-t[0], t[1]["relative_diff"]))
    recs = [r for _, r in ranked]
    return {
        "agreements": [r for r in recs if r["agrees"]][:top],
        "disagreements": [r for r in recs if not r["agrees"]][:top],
        "left_count": len(left),
        "right_count": len(right),
    }


def internal_inconsistencies(doc: Document, *, top: int = 12) -> list[dict]:
    """Same quantity, two different values, inside one document."""
    nums = extract(doc)
    df = _df(nums)
    found: dict[tuple[float, float], tuple[float, dict]] = {}
    for i, a in enumerate(nums):
        for b in nums[i + 1:]:
            # Must be a genuinely separate statement, not the cell next door.
            if a.block_id == b.block_id or a.unit != b.unit or a.value == b.value:
                continue
            denom = max(abs(a.value), abs(b.value), 1e-9)
            rel = abs(a.value - b.value) / denom
            if rel > 0.02 or rel <= 1e-9:
                continue
            shared = tuple(sorted(set(a.context) & set(b.context)))
            strong = tuple(w for w in shared if df.get(w, 1.0) < 0.15)
            if len(shared) < 2 or not strong:
                continue
            ev = _evidence(shared, df, df)
            key = (" ".join(strong[:5]), a.section, b.section)
            rec = {
                "quantity": " ".join(strong[:5]),
                "a": a.display,
                "a_section": a.section,
                "a_line": a.line,
                "a_source": a.source,
                "b": b.display,
                "b_section": b.section,
                "b_line": b.line,
                "b_source": b.source,
                "relative_diff": round(rel, 5),
                "evidence": round(ev, 2),
            }
            cur = found.get(key)
            if cur is None or (ev, -rel) > (cur[0], -cur[1]["relative_diff"]):
                found[key] = (ev, rec)
    ranked = sorted(found.values(), key=lambda t: (-t[0], t[1]["relative_diff"]))
    return [r for _, r in ranked][:top]
