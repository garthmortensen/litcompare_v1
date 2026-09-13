"""Markdown -> Document.

Hand-rolled on purpose: `markdown-it-py` is not in the lock, and the two
markdown->HTML converters that are (`markdown2`, `markdownify`) expose no
block AST. What is needed here is narrow -- sections, blocks, tables -- but
the edge cases are specific and were verified against the real fixtures:

* Every display equation in both papers is *single-line* `$$...$$`. A math
  state machine that toggles per line containing `$$` never exits, and every
  heading after the first equation disappears. Count occurrences instead.
* Table cells contain escaped pipes (`P(default in month $m$ \\| alive)`),
  so rows must split on unescaped pipes only.
* Table cells also contain currency (`$28.6bn`), which is why inline math is
  matched line-locally (see normalize._INLINE_MATH) and never across lines.
* Container headings (`## 3. Data` followed straight by `### 3.1 ...`) own no
  blocks, so their vectors must come from a rollup or they are NaN.
"""

from __future__ import annotations

import re

from . import ids
from .models import Block, Document, Section, Table
from .normalize import content_words, for_embedding, linearize_table

_ATX = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_SETEXT = re.compile(r"^\s{0,3}(=+|-+)\s*$")
_HR = re.compile(r"^\s{0,3}(?:-{3,}|\*{3,}|_{3,})\s*$")
_FENCE_OPEN = re.compile(r"^\s{0,3}(```+|~~~+)(.*)$")
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_UNESCAPED_PIPE = re.compile(r"(?<!\\)\|")
_TABLE_SEP = re.compile(r"^[\s|:-]+$")
_LIST_MARK = re.compile(r"^(\s*)(?:([-*+])|(\d+)[.)])\s+(.*)$")
_WHOLE_BOLD = re.compile(r"^\*\*([^*]+)\*\*[.:]?$")
_SENTENCE_END = re.compile(r"[.!?](?:\s|$)")
_BIB_HEADING = re.compile(
    r"^\s*(?:selected\s+)?(?:references|bibliography|works\s+cited|literature\s+cited)\b",
    re.IGNORECASE,
)
_CITATION = re.compile(
    r"^\s*[A-Z][\w'’-]+"                       # surname
    r"(?:,\s*[A-Z]\.|,\s*[A-Z][\w'’-]+|\s+and\s+|,\s+and\s+)"  # initials / co-authors
    r".{0,300}?\(?(?:19|20)\d{2}\)?[.,]",           # year
    re.DOTALL,
)
_BYLINE_HINT = re.compile(
    r"\b(?:prepared by|working paper|document id|classification|version|lead author"
    r"|contributors?|approved for|release candidate|submitted for)\b",
    re.IGNORECASE,
)

# A list whose items are longer than this, or which contain sentence-terminal
# punctuation, is split into one block per item. Champion section 7's five
# limitations merged into a single block answer one question for five items;
# split, four of the five align to the correct challenger subsection.
LIST_SPLIT_CHARS = 120


def _blank_out_comments(text: str) -> str:
    """Remove HTML comments but preserve line numbering for source anchors."""

    def repl(m: re.Match[str]) -> str:
        return "\n" * m.group(0).count("\n")

    return _HTML_COMMENT.sub(repl, text)


def _strip_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    lines = text.split("\n")
    for i in range(1, min(len(lines), 60)):
        if lines[i].strip() in ("---", "..."):
            return "\n".join([""] * (i + 1) + lines[i + 1 :])
    return text


def split_row(line: str) -> list[str]:
    """Split a table row on unescaped pipes only.

    `challenger.md:68` contains `P(default in month $m$ \\| alive at $m-1$)`;
    a naive split yields four columns instead of two.
    """
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"):
        line = line[:-1]
    return [c.replace("\\|", "|").strip() for c in _UNESCAPED_PIPE.split(line)]


def _parse_table(lines: list[str]) -> Table:
    rows = [split_row(ln) for ln in lines if ln.strip()]
    body = [r for r in rows if not _TABLE_SEP.match("".join(r) or " ")]
    # Drop the |---|---| separator row, which survives the join test above
    # only when it contains nothing but pipes, colons and dashes.
    body = [r for r in body if not all(_TABLE_SEP.match(c or "-") for c in r)]
    if not body:
        return Table(headers=[], rows=[])
    return Table(headers=body[0], rows=body[1:])


def _is_citation(text: str) -> bool:
    return bool(_CITATION.match(text.strip())) and len(text) < 500


class _Builder:
    def __init__(self, side: str) -> None:
        self.side = side
        self.sections: list[Section] = []
        self.blocks: list[Block] = []
        self._stack: list[Section] = []
        self._pending: list[tuple[int, str]] = []  # (lineno, text)
        self._pending_kind: str | None = None

    # -- sections ---------------------------------------------------------
    def open_section(self, level: int, heading: str, lineno: int) -> None:
        self.flush()
        sec = Section(
            id=ids.section_id(self.side, len(self.sections)),
            level=level,
            heading=heading,
            heading_path=(),
            order_index=len(self.sections),
            line_start=lineno,
        )
        # Tolerate level skips (challenger.md:5 is an H3 directly under the H1).
        while self._stack and self._stack[-1].level >= level:
            self._stack.pop()
        if self._stack:
            parent = self._stack[-1]
            sec.parent_id = parent.id
            parent.child_ids.append(sec.id)
            sec.heading_path = parent.heading_path + (heading,)
        else:
            sec.heading_path = (heading,)
        self._stack.append(sec)
        self.sections.append(sec)

    @property
    def current(self) -> Section:
        if not self.sections:
            # A document with no headings at all still needs somewhere to put
            # its blocks; block-level alignment then carries the comparison.
            self.open_section(1, "", 1)
        return self.sections[-1]

    # -- blocks -----------------------------------------------------------
    def add_line(self, lineno: int, text: str, kind: str | None = None) -> None:
        if kind and self._pending_kind and kind != self._pending_kind:
            self.flush()
        self._pending.append((lineno, text))
        self._pending_kind = kind or self._pending_kind

    def flush(self) -> None:
        if not self._pending:
            self._pending_kind = None
            return
        lines = self._pending
        kind = self._pending_kind
        self._pending = []
        self._pending_kind = None
        while lines and not lines[-1][1].strip():
            lines.pop()
        if not lines:
            return
        raw = "\n".join(t for _, t in lines)
        if not raw.strip():
            return
        self._emit(lines[0][0], lines[-1][0], raw, kind or self._infer_kind(lines))
        return

    @staticmethod
    def _infer_kind(lines: list[tuple[int, str]]) -> str:
        stripped = [t.strip() for _, t in lines if t.strip()]
        if not stripped:
            return "paragraph"
        if all(s.startswith("|") for s in stripped):
            return "table"
        if all(s.startswith(">") for s in stripped):
            return "quote"
        if _LIST_MARK.match(stripped[0]):
            return "list"
        return "paragraph"

    def _emit(self, start: int, end: int, raw: str, kind: str) -> None:
        sec = self.current
        bid = ids.block_id(sec.id, len(sec.block_ids))
        if kind == "table":
            tbl = _parse_table(raw.split("\n"))
            norm = linearize_table(tbl.headers, tbl.rows)
        elif kind == "quote":
            norm = for_embedding(re.sub(r"^\s*>\s?", "", raw, flags=re.MULTILINE))
        elif kind == "math":
            norm = "[equation] " + for_embedding(raw.replace("$$", " "))
        elif kind == "code":
            norm = for_embedding(re.sub(r"^\s*(```+|~~~+).*$", "", raw, flags=re.MULTILINE))
        else:
            norm = for_embedding(raw)
            if kind == "paragraph" and _is_citation(raw):
                kind = "citation"
        blk = Block(
            id=bid,
            section_id=sec.id,
            kind=kind,  # type: ignore[arg-type]
            raw=raw,
            normalized=norm,
            line_start=start,
            line_end=end,
            token_count=len(content_words(norm)),
            table=tbl if kind == "table" else None,
        )
        self.blocks.append(blk)
        sec.block_ids.append(bid)


def _split_lists(builder: _Builder) -> None:
    """Explode long list blocks into one block per item.

    The lead-in sentence is attached to each item's *normalized* text only, so
    each item carries context into the embedder without duplicating prose in
    the rendered report.
    """
    new_blocks: list[Block] = []
    by_section: dict[str, list[str]] = {}
    for blk in builder.blocks:
        if blk.kind != "list":
            new_blocks.append(blk)
            by_section.setdefault(blk.section_id, []).append(blk.id)
            continue
        items = _list_items(blk.raw)
        mean_len = sum(len(i) for i in items) / len(items) if items else 0
        multi_sentence = any(_SENTENCE_END.search(i[:-1]) for i in items)
        if len(items) < 2 or (mean_len <= LIST_SPLIT_CHARS and not multi_sentence):
            new_blocks.append(blk)
            by_section.setdefault(blk.section_id, []).append(blk.id)
            continue
        lead = _lead_in(builder, blk)
        for n, item in enumerate(items):
            norm = for_embedding(item)
            if lead:
                norm = f"{lead} {norm}".strip()
            new_blocks.append(
                Block(
                    id=f"{blk.id}i{n:02d}",
                    section_id=blk.section_id,
                    kind="list-item",
                    raw=item,
                    normalized=norm,
                    line_start=blk.line_start,
                    line_end=blk.line_end,
                    token_count=len(content_words(norm)),
                )
            )
            by_section.setdefault(blk.section_id, []).append(f"{blk.id}i{n:02d}")
    builder.blocks = new_blocks
    for sec in builder.sections:
        sec.block_ids = by_section.get(sec.id, [])


def _list_items(raw: str) -> list[str]:
    items: list[str] = []
    cur: list[str] = []
    for line in raw.split("\n"):
        m = _LIST_MARK.match(line)
        if m and len(m.group(1)) <= 2:  # top-level marker only
            if cur:
                items.append(" ".join(x.strip() for x in cur).strip())
            cur = [m.group(4)]
        elif cur:
            cur.append(line)
    if cur:
        items.append(" ".join(x.strip() for x in cur).strip())
    return [i for i in items if i]


def _lead_in(builder: _Builder, blk: Block) -> str:
    sec = next(s for s in builder.sections if s.id == blk.section_id)
    prev_id = None
    for bid in sec.block_ids:
        if bid == blk.id:
            break
        prev_id = bid
    if not prev_id:
        return ""
    prev = next(b for b in builder.blocks if b.id == prev_id)
    if prev.kind not in ("paragraph",) or prev.token_count > 60:
        return ""
    return prev.normalized


def _bind_captions(builder: _Builder) -> None:
    """Attach a whole-paragraph bold caption to the table/math that follows.

    Champion's `**Table 1. ...**` captions and challenger's `**Table - ...**`
    captions are separated from their tables by a blank line, so blank-line
    splitting orphans every one of them. The rule is deliberately strict --
    the bold span must be the *entire* paragraph and short -- so that
    paragraph lead-ins like `**Macro conditioning.** Macro features enter...`
    and the author bylines are not swallowed.
    """
    drop: set[str] = set()
    blocks = builder.blocks
    by_id = {b.id: b for b in blocks}
    for i, blk in enumerate(blocks[:-1]):
        if blk.kind != "paragraph":
            continue
        m = _WHOLE_BOLD.match(blk.raw.strip())
        if not m or len(blk.raw) > LIST_SPLIT_CHARS:
            continue
        nxt = blocks[i + 1]
        if nxt.section_id != blk.section_id or nxt.kind not in ("table", "math"):
            continue
        caption = m.group(1).strip()
        nxt.caption = caption
        if nxt.kind == "table" and nxt.table is not None:
            nxt.table.caption = caption
            nxt.normalized = linearize_table(nxt.table.headers, nxt.table.rows, caption)
        else:
            nxt.normalized = f"{for_embedding(caption)} {nxt.normalized}".strip()
        nxt.token_count = len(content_words(nxt.normalized))
        nxt.line_start = blk.line_start
        drop.add(blk.id)
    if not drop:
        return
    builder.blocks = [b for b in blocks if b.id not in drop]
    for sec in builder.sections:
        sec.block_ids = [b for b in sec.block_ids if b not in drop]
    del by_id


def _classify_sections(builder: _Builder) -> None:
    secs = builder.sections
    blocks = {b.id: b for b in builder.blocks}

    # Front matter: everything before the first H2, when that prologue is
    # short. Catches champion's title+byline and challenger's title plus its
    # H3 subtitle block (byline, Document ID, purpose blockquote).
    first_h2 = next((i for i, s in enumerate(secs) if s.level == 2), None)
    frontmatter_upto = -1
    if first_h2 is not None and first_h2 <= 3:
        frontmatter_upto = first_h2 - 1
    elif secs and secs[0].level == 1:
        frontmatter_upto = 0

    for i, sec in enumerate(secs):
        own = [blocks[b] for b in sec.block_ids]
        if i <= frontmatter_upto:
            looks_meta = not own or any(_BYLINE_HINT.search(b.raw) for b in own) or all(
                b.token_count < 40 for b in own
            )
            if looks_meta:
                sec.kind = "frontmatter"
                for b in own:
                    b.kind = "frontmatter"
                continue
        if _BIB_HEADING.match(sec.heading):
            sec.kind = "bibliography"
            for b in own:
                b.kind = "citation"
            continue
        if own and sum(1 for b in own if b.kind == "citation") / len(own) > 0.6:
            sec.kind = "bibliography"
            continue
        if not own and sec.child_ids:
            sec.kind = "container"
            continue
        if re.match(r"^\s*(appendix|annex)", sec.heading, re.IGNORECASE):
            sec.kind = "appendix"
            continue
        sec.kind = "prose"


def parse_markdown(text: str, path: str, side: str) -> Document:
    text = _blank_out_comments(_strip_frontmatter(text))
    lines = text.split("\n")
    b = _Builder(side)

    in_fence: str | None = None
    in_math = False
    title = ""

    i = 0
    while i < len(lines):
        line = lines[i]
        lineno = i + 1

        if in_fence is not None:
            b.add_line(lineno, line, "code")
            if line.strip().startswith(in_fence):
                in_fence = None
                b.flush()
            i += 1
            continue

        fence = _FENCE_OPEN.match(line)
        if fence and not in_math:
            b.flush()
            in_fence = fence.group(1)[:3]
            b.add_line(lineno, line, "code")
            i += 1
            continue

        # Math state is driven by the *count* of $$ on the line, so a
        # single-line `$$ ... $$` equation opens and closes in one step.
        dollars = line.count("$$")
        if in_math:
            b.add_line(lineno, line, "math")
            if dollars % 2 == 1:
                in_math = False
                b.flush()
            i += 1
            continue
        if dollars >= 2:
            b.flush()
            b.add_line(lineno, line, "math")
            b.flush()
            i += 1
            continue
        if dollars == 1:
            b.flush()
            in_math = True
            b.add_line(lineno, line, "math")
            i += 1
            continue

        atx = _ATX.match(line)
        if atx:
            level, heading = len(atx.group(1)), atx.group(2).strip()
            if level == 1 and not title:
                title = heading
            b.open_section(level, heading, lineno)
            i += 1
            continue

        if _SETEXT.match(line) and b._pending and not _HR.match(line):
            pend = [t for _, t in b._pending if t.strip()]
            if len(pend) == 1 and not pend[0].strip().startswith("|"):
                level = 1 if line.strip().startswith("=") else 2
                heading = pend[0].strip()
                b._pending = []
                b._pending_kind = None
                if level == 1 and not title:
                    title = heading
                b.open_section(level, heading, lineno - 1)
                i += 1
                continue

        if _HR.match(line):
            b.flush()
            i += 1
            continue

        if not line.strip():
            b.flush()
            i += 1
            continue

        b.add_line(lineno, line)
        i += 1

    b.flush()
    _bind_captions(b)
    _split_lists(b)
    _classify_sections(b)

    return Document(
        path=path,
        doc_id=ids.content_hash(text),
        title=title or (b.sections[0].heading if b.sections else path),
        side=side,
        sections=b.sections,
        blocks=b.blocks,
    )


def parse_file(path: str, side: str) -> Document:
    with open(path, encoding="utf-8") as fh:
        return parse_markdown(fh.read(), path, side)
