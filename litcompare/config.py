"""Run parameters. Nothing about matching is hard-coded in the algorithm."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import yaml

from .embed import DEFAULT_MODEL


@dataclass(slots=True)
class Params:
    model: str = DEFAULT_MODEL
    revision: str | None = None
    device: str = "cpu"
    threads: int | None = None
    batch_size: int = 32

    calibration: str = "percentile"   # percentile | absolute
    blend_weight: float = 0.5          # weight on the embedding channel

    section_top_k: int = 3
    section_margin: float = 0.03
    section_anchor_floor: float = 0.75
    section_secondary_floor: float = 0.90
    section_capacity: int = 3
    section_weak_floor: float = 0.93

    block_top_k: int = 2
    block_margin: float = 0.02
    block_anchor_floor: float = 0.80
    block_secondary_floor: float = 0.95
    block_capacity: int = 1
    block_weak_floor: float = 0.97

    coverage_floor: float = 0.90
    inline_diff_floor: float = 0.97
    excerpt_chars: int = 420
    layout: str = "html-table"
    include_matrix: bool = False
    cache: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def load(cls, path: str | None = None, **overrides) -> "Params":
        data: dict = {}
        if path:
            with open(path, encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
            data = data.get("defaults", data)
        valid = {f for f in cls.__dataclass_fields__}
        data = {k: v for k, v in data.items() if k in valid}
        data.update({k: v for k, v in overrides.items() if v is not None and k in valid})
        return cls(**data)
