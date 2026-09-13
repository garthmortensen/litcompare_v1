"""Word-level and numeric deltas between two matched passages."""

from __future__ import annotations

import difflib
import re

from .normalize import unicode_fix

_TOKEN = re.compile(r"\s+")
_NUMERIC = re.compile(r"^[-+]?[\d,]*\.?\d+(?:%|x|bn)?$")
_MD_SPECIAL = re.compile(r"([\\`*_{}\[\]()#+\-.!|~])")


def _tokens(text: str) -> list[str]:
    return [t for t in _TOKEN.split(unicode_fix(text).strip()) if t]


def numeric_changes(left: str, right: str, *, limit: int = 12) -> list[dict]:
    """Changed number-bearing tokens between two aligned passages.

    Runs on unicode-normalised text, without which U+2212 negatives lose their
    sign and a sign flip reads as no change at all.
    """
    a, b = _tokens(left), _tokens(right)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    out: list[dict] = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "replace":
            continue
        lhs = [t for t in a[i1:i2] if _NUMERIC.match(t.strip(".,;:()"))]
        rhs = [t for t in b[j1:j2] if _NUMERIC.match(t.strip(".,;:()"))]
        for k in range(min(len(lhs), len(rhs))):
            if lhs[k] != rhs[k]:
                out.append({"from": lhs[k], "to": rhs[k]})
        if len(out) >= limit:
            break
    return out[:limit]


def inline_diff(left: str, right: str, *, max_tokens: int = 220) -> str:
    """GFM-safe word diff: `**insertions**` and `~~deletions~~`.

    Only worth rendering for genuinely close passages; the caller gates on
    similarity before calling.
    """
    a, b = _tokens(left)[:max_tokens], _tokens(right)[:max_tokens]
    if not a or not b:
        return ""
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    parts: list[str] = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            parts.append(" ".join(a[i1:i2]))
        elif tag == "delete":
            parts.append(f"~~{' '.join(a[i1:i2])}~~")
        elif tag == "insert":
            parts.append(f"**{' '.join(b[j1:j2])}**")
        else:
            parts.append(f"~~{' '.join(a[i1:i2])}~~ **{' '.join(b[j1:j2])}**")
    return " ".join(p for p in parts if p.strip())
