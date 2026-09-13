"""Bibliographies, handled lexically.

`References` and `Selected References` match at the section level on citation
register alone -- it is often the highest raw cosine in the whole matrix -- and
block-level matching inside them would "pair" most of the entries when only a
couple are genuinely shared. Comparing normalised (surname, year) keys is both
cheaper and correct, so bibliographies are routed here and excluded from
embedding-based alignment, coverage and numeric deltas.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .models import Document
from .normalize import unicode_fix

_YEAR = re.compile(r"\(?((?:19|20)\d{2})[a-z]?\)?")
_SURNAME = re.compile(r"^\s*([A-Z][\w'’-]+)")
_TITLEISH = re.compile(r"\.\s*([^.]{10,140})\.")


@dataclass(slots=True)
class Citation:
    key: str
    surname: str
    year: str
    text: str
    line: int

    def as_dict(self) -> dict:
        return {"key": self.key, "surname": self.surname, "year": self.year,
                "text": self.text, "line": self.line}


def extract(doc: Document) -> list[Citation]:
    out: list[Citation] = []
    for blk in doc.blocks:
        if blk.kind != "citation":
            continue
        text = unicode_fix(blk.raw).strip()
        ym = _YEAR.search(text)
        sm = _SURNAME.match(text)
        if not ym or not sm:
            continue
        surname, year = sm.group(1), ym.group(1)
        out.append(
            Citation(
                key=f"{surname.lower()}:{year}",
                surname=surname,
                year=year,
                text=re.sub(r"\s+", " ", text)[:220],
                line=blk.line_start,
            )
        )
    return out


def compare(left_doc: Document, right_doc: Document) -> dict:
    left, right = extract(left_doc), extract(right_doc)
    lmap = {c.key: c for c in left}
    rmap = {c.key: c for c in right}
    shared_keys = sorted(set(lmap) & set(rmap))
    return {
        "left_count": len(left),
        "right_count": len(right),
        "shared": [
            {"key": k, "left": lmap[k].text, "right": rmap[k].text,
             "left_line": lmap[k].line, "right_line": rmap[k].line}
            for k in shared_keys
        ],
        "left_only": [c.as_dict() for c in left if c.key not in rmap],
        "right_only": [c.as_dict() for c in right if c.key not in lmap],
        "jaccard": round(
            len(shared_keys) / max(len(set(lmap) | set(rmap)), 1), 4
        ),
    }
