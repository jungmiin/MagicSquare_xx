"""D-LOC-01 — blank cell coordinates (1-index row-major)."""

import pytest

from entity.constants import MAGIC_SUM
from entity.locate import find_blank_coords


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given: G1 격자
    expected = [(2, 3), (4, 4)]

    # When: find_blank_coords(grid_g1)
    result = find_blank_coords(grid_g1)

    # Then: 1-index row-major [(2,3), (4,4)]
    pytest.fail(
        f"RED: D-LOC-01 — result={result}, expected={expected}, MAGIC_SUM={MAGIC_SUM}"
    )
