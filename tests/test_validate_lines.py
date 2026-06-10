"""validate_lines — 10선 검증 RED (세션 3).

중요도 순: T-VAL-01 → T-VAL-02 → T-VAL-03
"""

import pytest

from entity.constants import MAGIC_SUM
from src.validate_lines import validate_lines


# --- T-VAL-01 (FR-VAL-02) — 10선 모두 합 MAGIC_SUM → pass ---
def test_t_val_01_pass_when_all_lines_sum_34(grid_g1_original):
    # Given: G1 완성 격자 (빈칸 7·8)
    grid = [row[:] for row in grid_g1_original]
    grid[1][3] = 7
    grid[2][2] = 8

    # When: 10선 검증
    result = validate_lines(grid)

    # Then: GREEN에서 pass + failed_lines=[] 검증
    pytest.fail(
        f"RED: T-VAL-01 — result={result}, "
        f"expected pass/failed_lines=[], MAGIC_SUM={MAGIC_SUM}"
    )


# --- T-VAL-02 (FR-VAL-03) — 빈칸 없으나 한 선 합 ≠ MAGIC_SUM → fail ---
def test_t_val_02_fail_when_line_sum_not_34(grid_g1_original):
    # Given: 완성 형태이나 (1,1) 10→9 변경
    grid = [row[:] for row in grid_g1_original]
    grid[1][3] = 7
    grid[2][2] = 8
    grid[1][1] = 9

    # When: 10선 검증
    result = validate_lines(grid)

    # Then: GREEN에서 fail + R2·C2 in failed_lines 검증
    pytest.fail(
        f"RED: T-VAL-02 — result={result}, "
        f"expected fail/failed_lines contains line at (1,1), MAGIC_SUM={MAGIC_SUM}"
    )


# --- T-VAL-03 (FR-VAL-01) — 빈칸 잔존 → incomplete ---
def test_t_val_03_incomplete_when_blank_remains(grid_g1_original):
    # Given: G1 original (빈칸 2개)
    grid = grid_g1_original

    # When: 10선 검증
    result = validate_lines(grid)

    # Then: GREEN에서 incomplete 검증
    pytest.fail(
        f"RED: T-VAL-03 — result={result}, expected incomplete, MAGIC_SUM={MAGIC_SUM}"
    )
