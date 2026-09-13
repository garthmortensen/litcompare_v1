"""Stable identifiers and slugs.

Every id is deterministic from document side + ordinal so that the JSON
sidecar diffs cleanly between runs and golden tests stay stable.
"""

from __future__ import annotations

import hashlib
import re

_SLUG_STRIP = re.compile(r"[^a-z0-9]+")


def section_id(side: str, index: int) -> str:
    return f"{side}:s{index:03d}"


def block_id(section: str, index: int) -> str:
    return f"{section}:b{index:02d}"


def slug(text: str, *, maxlen: int = 60) -> str:
    """GitHub-ish anchor slug, truncated and never empty."""
    s = _SLUG_STRIP.sub("-", text.strip().lower()).strip("-")
    if len(s) > maxlen:
        s = s[:maxlen].rstrip("-")
    return s or "section"


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def short_hash(text: str, n: int = 12) -> str:
    return content_hash(text)[:n]
