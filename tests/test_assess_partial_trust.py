"""assess_partial_trust — Test Loop RED (세션 3).

중요도 순: T-TRUST-01 → T-TRUST-02 → T-TRUST-03
"""

import pytest

from entity.constants import CELL_MAX
from src.assess_partial_trust import assess_partial_trust


# --- T-TRUST-01 (FR-TRUST-05) — 신뢰 관문: trusted + can_verify ---
def test_t1_trusted_when_given_cells_preserved_and_blanks_filled(grid_g1_original):
    # Arrange: 주어진 칸 보존, 빈칸만 7·8로 채움
    working = [
        [16, 3, 2, 13],
        [5, 10, 11, 7],
        [9, 6, 8, 12],
        [4, 15, 14, 1],
    ]

    # Act
    result = assess_partial_trust(grid_g1_original, working)

    # Assert — GREEN 목표 (현재 RED)
    assert result["status"] == "trusted"
    assert result["can_verify"] is True
    assert result["violations"] == []


# --- T-TRUST-02 (FR-TRUST-01,04,06) — 오염: 주어진 칸 변경 ---
def test_t2_contaminated_when_given_cell_modified(grid_g1_original):
    # Arrange: 주어진 칸 (1,1)=10 → 11 변경 (Mom Test: 주어진 vs 추론 혼재)
    working = [
        [16, 3, 2, 13],
        [5, 11, 11, 7],
        [9, 6, 8, 12],
        [4, 15, 14, 1],
    ]

    # Act
    result = assess_partial_trust(grid_g1_original, working)

    # Assert — GREEN 목표 (현재 RED)
    assert result["status"] == "contaminated"
    assert result["can_verify"] is False
    assert any(v["rule_id"] == "R1" and v["row"] == 1 and v["col"] == 1 for v in result["violations"])


# --- T-TRUST-03 (FR-TRUST-03) — 오염: 값 범위 위반 (R3) ---
def test_t3_contaminated_when_value_out_of_range(grid_g1_original):
    # Given: 빈칸 (1,3)에 CELL_MAX 초과 값 입력
    working = [row[:] for row in grid_g1_original]
    working[1][3] = CELL_MAX + 1

    # When: 신뢰 판정 호출
    result = assess_partial_trust(grid_g1_original, working)

    # Then: GREEN에서 contaminated + R3 at (1,3) 검증
    pytest.fail(
        f"RED: T-TRUST-03 — result={result}, "
        f"expected contaminated/can_verify=False/R3 at (1,3), CELL_MAX={CELL_MAX}"
    )
