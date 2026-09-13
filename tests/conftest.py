from __future__ import annotations

from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"
LIT_MD = Path(__file__).parent.parent / "lit_md"


@pytest.fixture(scope="session")
def champion_path() -> str:
    return str(LIT_MD / "champion.md")


@pytest.fixture(scope="session")
def challenger_path() -> str:
    return str(LIT_MD / "challenger.md")
