"""Text normalization.

Two separate jobs, deliberately not conflated:

* `unicode_fix` repairs typography so numeric extraction and diffing work.
  The fixtures use U+2212 MINUS SIGN on every negative coefficient, so a
  `-?\\d+\\.\\d+` pattern silently loses the sign without this.
* `for_embedding` strips markdown scaffolding so the embedder sees prose.
"""

from __future__ import annotations

import re
import unicodedata

# Order matters only in that these are all single-codepoint substitutions.
UNICODE_MAP = {
    "−": "-",   # MINUS SIGN -> hyphen (9x champion, 5x challenger)
    "–": "-",   # EN DASH (ranges: 620-659, 2009Q1-2023Q4)
    "—": " - ", # EM DASH (used as a separator, not a range)
    "‐": "-",
    "‑": "-",
    "×": "x",   # MULTIPLICATION SIGN (2.3x)
    "÷": "/",   # DIVISION SIGN
    "±": "+/-",
    "·": " ",   # MIDDLE DOT ("Annex 1 . Data lineage")
    "→": "->",
    "←": "<-",
    "↑": " up ",
    "↓": " down ",
    "‘": "'", "’": "'",
    "“": '"', "”": '"',
    "…": "...",
    " ": " ",  # NBSP
    " ": " ", " ": " ", " ": " ", " ": " ",
    "​": "",   # zero-width space
    "﻿": "",
}

_TRANS = str.maketrans(UNICODE_MAP)

# Cross-references are asymmetric noise: champion says "Section 4.5", the
# challenger says "Part II". Neither carries transferable meaning.
_XREF = re.compile(
    r"""\b(?:
          Section\s+\d+(?:\.\d+)*
        | Sections\s+\d+(?:\.\d+)*(?:\s*(?:-|and|,)\s*\d+(?:\.\d+)*)*
        | Appendix\s+[A-Z]\b
        | Annex(?:es)?\s+\d*
        | Part\s+[IVXLC]+\b
        | Table\s+\d+
        | Figure\s+\d+
        | Box\s+\d+
        | item\s+\d+
    )""",
    re.VERBOSE,
)

_FENCE = re.compile(r"^\s{0,3}(?:```+|~~~+)")
_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_BOLD_IT = re.compile(r"(\*\*\*|\*\*|\*|__|_|~~)")
_CODESPAN = re.compile(r"`([^`]*)`")
_INLINE_MATH = re.compile(r"\$([^$\n]+)\$")
_TEX_CMD = re.compile(r"\\([a-zA-Z]+)")
_WS = re.compile(r"\s+")
_HEADING_PREFIX = re.compile(
    r"^\s*(?:"
    r"\d+(?:\.\d+)*\.?"            # 4.2  /  4.2.
    r"|Appendix\s+[A-Z]\.?"
    r"|Annex(?:es)?\s+\d*\.?"
    r"|Part\s+[IVXLC]+\.?"
    r"|Box\s+\d+\.?"
    r"|Phase\s+\d+\.?"
    r"|Step\s+\d+\.?"
    r")\s*[-.:—·]*\s*",
)


def unicode_fix(text: str) -> str:
    """NFC-normalise and fold typographic characters to ASCII equivalents."""
    return unicodedata.normalize("NFC", text).translate(_TRANS)


def strip_heading_prefix(heading: str) -> str:
    """Remove structural ordinals from a heading.

    Without this, a 3-word heading vector is dominated by `Part`/`Annex`/digits
    rather than by the words that carry meaning.
    """
    out = _HEADING_PREFIX.sub("", heading, count=1).strip()
    return out or heading.strip()


def inline_md_to_text(text: str) -> str:
    """Strip inline markdown so the embedder sees words, not syntax."""
    t = _IMAGE.sub(" ", text)
    t = _LINK.sub(r"\1", t)
    t = _CODESPAN.sub(r"\1", t)
    # Inline math: keep the identifiers, drop TeX control sequences/braces.
    # Keep the command *name* (\\Delta -> Delta); dropping it entirely loses
    # the only readable token in an expression like $\\Delta u_t$.
    t = _INLINE_MATH.sub(
        lambda m: " "
        + _TEX_CMD.sub(r"\1 ", m.group(1)).replace("{", " ").replace("}", " ")
        + " ",
        t,
    )
    t = _BOLD_IT.sub("", t)
    return t


def for_embedding(text: str, *, drop_xrefs: bool = True) -> str:
    """Normalized form fed to the embedder and the tf-idf channel."""
    t = unicode_fix(text)
    t = inline_md_to_text(t)
    if drop_xrefs:
        t = _XREF.sub(" ", t)
    t = t.replace("|", " ")
    t = _WS.sub(" ", t).strip()
    # Dropping a leading xref can leave orphaned punctuation ("Table 1." ->
    # ". ..."), which is noise in a short caption.
    return t.lstrip(" .,;:-").strip()


def linearize_table(headers: list[str], rows: list[list[str]], caption: str = "") -> str:
    """Render a table as prose-ish `header: cell; header: cell` lines.

    Keeps the semantic payload (column names bound to values) that a bare
    pipe-dump loses. Tables are ~25% of non-blank lines in these fixtures and
    removing them measurably degrades matching, so they must embed well.
    """
    parts: list[str] = []
    if caption:
        parts.append(for_embedding(caption))
    clean_headers = [for_embedding(h) for h in headers]
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            val = for_embedding(cell)
            if not val:
                continue
            head = clean_headers[i] if i < len(clean_headers) else ""
            cells.append(f"{head}: {val}" if head else val)
        if cells:
            parts.append("; ".join(cells))
    return " ".join(parts).strip()


def content_words(text: str) -> list[str]:
    """Lowercased alphanumeric tokens, stopwords removed.

    Used for token-count weighting so coverage is not dominated by
    punctuation-heavy table rows.
    """
    toks = re.findall(r"[a-z0-9][a-z0-9._%-]*", text.lower())
    return [t for t in toks if t not in STOPWORDS and len(t) > 1]


STOPWORDS = frozenset(
    """a an and are as at be been but by for from has have he her his if in into is it its
    of on or our that the their then there these they this to was were which who will with
    we us you your not no than then so such both each more most other some only own same
    can may might must should would could do does did doing done very via per
    i ii iii iv v vi vii viii ix x""".split()
)
