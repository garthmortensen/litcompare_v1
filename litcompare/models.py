"""Data contract for the whole pipeline.

Stages are pure functions over these types, so any stage can be tested or
replaced in isolation. Vectors live outside these objects (in numpy arrays
indexed by id) to keep the dataclasses cheap to copy and serialise.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

BlockKind = Literal[
    "paragraph",
    "table",
    "math",
    "code",
    "list",
    "list-item",
    "quote",
    "citation",
    "frontmatter",
    "caption",
]

SectionKind = Literal["prose", "container", "bibliography", "frontmatter", "appendix"]

# How a matched section pair relates. `weak` is an accepted-but-low-confidence
# pair; `moved` rides on top of a 1:1/split/merge (tracked separately).
Relation = Literal["1:1", "split", "merge", "weak", "left-only", "right-only"]


@dataclass(slots=True)
class Block:
    id: str
    section_id: str
    kind: BlockKind
    raw: str
    normalized: str
    line_start: int
    line_end: int
    token_count: int = 0
    # Table blocks carry structure so tables.py can align rows/columns
    # without re-parsing the markdown.
    table: "Table | None" = None
    caption: str = ""

    @property
    def is_bibliographic(self) -> bool:
        return self.kind == "citation"


@dataclass(slots=True)
class Table:
    headers: list[str]
    rows: list[list[str]]
    caption: str = ""

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.rows), len(self.headers))


@dataclass(slots=True)
class Section:
    id: str
    level: int
    heading: str
    heading_path: tuple[str, ...]
    order_index: int
    kind: SectionKind = "prose"
    block_ids: list[str] = field(default_factory=list)
    child_ids: list[str] = field(default_factory=list)
    parent_id: str | None = None
    line_start: int = 0

    @property
    def is_container(self) -> bool:
        return self.kind == "container"

    @property
    def display(self) -> str:
        return self.heading or "(untitled)"


@dataclass(slots=True)
class Document:
    path: str
    doc_id: str
    title: str
    side: str
    sections: list[Section]
    blocks: list[Block]

    def __post_init__(self) -> None:
        self._sec_by_id = {s.id: s for s in self.sections}
        self._blk_by_id = {b.id: b for b in self.blocks}

    _sec_by_id: dict[str, Section] = field(default_factory=dict, repr=False)
    _blk_by_id: dict[str, Block] = field(default_factory=dict, repr=False)

    def section(self, sid: str) -> Section:
        return self._sec_by_id[sid]

    def block(self, bid: str) -> Block:
        return self._blk_by_id[bid]

    def own_blocks(self, sid: str) -> list[Block]:
        return [self._blk_by_id[b] for b in self._sec_by_id[sid].block_ids]

    def descendant_ids(self, sid: str) -> list[str]:
        """Section id plus every descendant, depth-first in document order."""
        out = [sid]
        for child in self._sec_by_id[sid].child_ids:
            out.extend(self.descendant_ids(child))
        return out

    def rollup_blocks(self, sid: str) -> list[Block]:
        out: list[Block] = []
        for s in self.descendant_ids(sid):
            out.extend(self.own_blocks(s))
        return out

    @property
    def alignable_sections(self) -> list[Section]:
        """Sections eligible for semantic alignment.

        Front-matter is excluded (it would consume a match slot with a byline)
        and bibliographies are excluded because citations.py handles them
        lexically -- embedding them pairs unrelated citations on register alone.
        """
        return [s for s in self.sections if s.kind not in ("frontmatter", "bibliography")]


@dataclass(slots=True)
class BlockMatch:
    left_id: str
    right_id: str
    score: float           # calibrated, 0..1
    cosine: float          # raw embedding cosine
    lexical: float         # raw tf-idf cosine
    inline_diff: str = ""
    numeric_deltas: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class SectionMatch:
    left_id: str
    right_id: str
    score: float
    cosine: float
    lexical: float
    relation: Relation
    moved: bool = False
    block_matches: list[BlockMatch] = field(default_factory=list)
    left_only_blocks: list[str] = field(default_factory=list)
    right_only_blocks: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Calibration:
    """The pair's own null distribution, so scores are interpretable."""

    n_pairs: int
    raw_min: float
    raw_p05: float
    raw_median: float
    raw_p95: float
    raw_max: float
    deciles: list[float]
    mode: str
    lexical_median: float = 0.0
    lexical_max: float = 0.0


@dataclass(slots=True)
class ComparisonResult:
    left_path: str
    right_path: str
    left_title: str
    right_title: str
    model_id: str
    model_revision: str
    params: dict[str, Any]
    calibration: Calibration
    metrics: dict[str, Any]
    section_matches: list[SectionMatch]
    left_only: list[str]
    right_only: list[str]
    numerals: dict[str, Any] = field(default_factory=dict)
    citations: dict[str, Any] = field(default_factory=dict)
    terminology: dict[str, Any] = field(default_factory=dict)
    table_pairs: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    generated_at: str = ""
    # Best blended score against anything on the other side, keyed by section
    # id. Populated for every section (matched or not) -- the renderer's
    # "only in champion/challenger" listing needs this for sections that
    # never made it into a SectionMatch.
    section_best: dict[str, float] = field(default_factory=dict)

    def to_json_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d.pop("_sec_by_id", None)
        return d
