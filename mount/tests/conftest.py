from __future__ import annotations

import pytest
from app.common.context import Context


# https://docs.pytest.org/en/7.1.x/reference/reference.html#globalvar-pytestmark
pytestmark = pytest.mark.asyncio


class TestContext(Context):
    def __init__(self) -> None:
        ...


@pytest.fixture
async def ctx() -> TestContext:
    return TestContext()
