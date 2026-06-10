"""assess_partial_trust — Test Loop RED (세션 3)."""

from src.assess_partial_trust import assess_partial_trust


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
