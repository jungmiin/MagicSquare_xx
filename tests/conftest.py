"""pytest 픽스처 — G1 격자 SSOT (과제 기준, 빈칸 2개)."""

import pytest

# G1 original: 빈칸 (1,3), (2,2) — 0-index
GRID_G1_ORIGINAL: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 0],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]


@pytest.fixture
def grid_g1_original() -> list[list[int]]:
    """문제에서 주어진 G1 격자 — 빈칸 2개."""
    return [row[:] for row in GRID_G1_ORIGINAL]
