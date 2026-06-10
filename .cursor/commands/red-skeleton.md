# RED Skeleton — pytest.fail 스켈레톤 (RED ④)

ARRR **A단계 (RED ④)**. 직전 `/red-test-plan` 설계표(블록 1~3)를 기준으로 **pytest.fail 스켈레톤**만 `tests/` 에 작성한다.  
도메인 판정·assert 본문은 GREEN 단계 — 여기서는 **의도적 FAIL** 만 만든다.

> **Skill:** `magic-square-tdd` Skill이 있으면 자동 따름 (Phase 선언 · C2C · RED 금지 · pytest · 완료 보고).

## 선행 조건

| 항목 | 출처 |
|------|------|
| C2C 설계표 · Track B/A 표 · 테스트 플랜 | `/red-test-plan` 출력 (채팅 또는 직전 응답) |
| Rule·API 계약 | `.cursorrules` |
| Test ID · FR · Given/When/Then | 설계표 블록 1~2 |

설계표가 없으면 `/red-test-plan` 을 먼저 실행한다.

## 필수 선언 (응답 첫 줄)

```
Phase: red | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| `Layer` | `entity` \| `boundary` | 설계표와 동일 |
| `Track` | `Logic` \| `UI` | 설계표와 동일 |

**Track A (boundary / UI):** `Layer: boundary` · `Track: UI` 로 선언만 바꾸면 본 Command 재사용.

## 절차

1. **설계표 읽기** — Test ID 1개 · 대상 함수 · 파일 경로 · 함수명 · conftest 픽스처 확정
2. **conftest 점검** — `tests/conftest.py` 에 `grid_g1` 픽스처가 없으면 추가 (아래 SSOT)
3. **스켈레톤 1개 작성** — 설계표 함수명·AAA·`pytest.fail` 한 줄
4. **pytest 실행** — 설계표 블록 3 명령으로 **FAIL** 확인
5. **완료 보고** — Test ID · FAIL 한 줄 · 변경 파일 (`tests/` 만)

RED 묶음 = **테스트 함수 1개**. 여러 Test ID는 `/red-test-plan` 을 다시 돌려 묶음을 나눈다.

## AAA 구조 (주석 필수)

```python
def test_<test_id_slug>_<행위>(grid_g1):
    # Given: …
    …

    # When: …
    …

    # Then: …
    pytest.fail("RED: <Test-ID> — …")
```

| 단계 | 내용 | 허용 |
|------|------|------|
| **Given** | 설계표 Given — 격자·`original`/`working` 준비 | 픽스처·리터럴·`entity.constants` import 상수 |
| **When** | 설계표 When — 대상 함수 호출 **또는** 호출 전까지 Arrange만 | `src/` import는 Act 직전까지 가능 |
| **Then** | **`pytest.fail("RED: {Test ID} — …")` 한 줄만** | assert 본문·통과 더미·`return` 금지 |

### Then 규칙

- 메시지 형식: `pytest.fail("RED: D-LOC-01 — blank coords row-major")`
- 설계표 Then(기대 출력)은 **fail 메시지에 요약**만 넣는다 — 검증 로직은 GREEN
- `assert` / `pytest.skip` / `pytest.xfail` / `pass` 로 통과시키기 **금지**

## 상수 · 픽스처 SSOT

### `entity/constants.py` (import 전용)

격자 **픽스처 데이터**에서만 사용. 테스트 파일에 `34` / `16` / `4` 리터럴 직접 쓰지 않는다.

```python
from entity.constants import GRID_SIZE, MAGIC_SUM, CELL_MAX
```

| 상수 | 값 | 의미 |
|------|-----|------|
| `GRID_SIZE` | `4` | 4×4 격자 |
| `MAGIC_SUM` | `34` | 10선 마법 상수 |
| `CELL_MAX` | `16` | 채워진 칸 상한 |

`entity/constants.py` 가 없으면 `tests/` 에만 **import 구문**을 두고, 상수 모듈 생성은 GREEN 범위가 아니면 픽스처 주석에 `# GRID_SIZE=4` 로 대체하지 말고 사용자에게 알린다. (일반적으로 constants 는 도메인 공유 모듈로 선행 존재 가정.)

### `tests/conftest.py` — `grid_g1`

- **이름:** `grid_g1` (함수 인자·`@pytest.fixture def grid_g1`)
- **의미:** G1 과제 격자 — 빈칸 `0` **정확히 2개**, row-major `list[list[int]]`
- **빈칸 좌표 (0-index):** `(1, 3)`, `(2, 2)`

```python
import pytest

GRID_G1: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 0],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]


@pytest.fixture
def grid_g1() -> list[list[int]]:
    """G1 격자 — 빈칸 2개, row-major."""
    return [row[:] for row in GRID_G1]
```

기존 `grid_g1_original` 등 레거시 픽스처가 있으면 **동일 데이터**로 `grid_g1` alias 추가 가능. 스켈레톤은 `grid_g1` 을 사용한다.

## 템플릿 예시 — `test_d_loc_01_blank_coords_row_major`

설계표: Test ID `D-LOC-01` · FR-LOC-01 · 빈칸 좌표 row-major 목록

```python
"""D-LOC-01 — blank cell coordinates (row-major)."""

import pytest

from entity.constants import GRID_SIZE, MAGIC_SUM


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given: G1 격자, 빈칸은 row-major 순으로 (1,3), (2,2)
    blanks: list[tuple[int, int]] = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid_g1[row][col] == 0:
                blanks.append((row, col))

    # When: 빈칸 좌표가 row-major로 수집됨 (판정 API는 GREEN에서 연결)
    expected = [(1, 3), (2, 2)]

    # Then: GREEN 전 — 좌표·마법상수 계약 스켈레톤
    pytest.fail(
        f"RED: D-LOC-01 — blanks={blanks}, expected={expected}, MAGIC_SUM={MAGIC_SUM}"
    )
```

- 파일: 설계표 블록 3 경로 (예: `tests/test_locate_blanks.py`)
- **Then에 assert 없음** — GREEN에서 `blanks == expected` 등으로 교체

### `assess_partial_trust` 스켈레톤 변형

```python
import pytest

from src.assess_partial_trust import assess_partial_trust


def test_d_trust_01_given_cell_modified(grid_g1):
    # Given: original=grid_g1, working에서 주어진 칸 (1,1) 변경
    original = grid_g1
    working = [row[:] for row in original]
    working[1][1] = 11

    # When: 신뢰 판정 호출
    result = assess_partial_trust(original, working)

    # Then: GREEN에서 status·violations 검증
    pytest.fail("RED: D-TRUST-01 — contaminated + R1 violation at (1,1)")
```

`src/` **구현 추가·수정 금지**. import 는 기존 모듈이 있을 때만.

## pytest

설계표 블록 3 명령 사용:

```bash
python -m pytest tests/test_<module>.py::test_<test_id_slug>_<행위> -v
```

- 기대: **FAIL** (`pytest.fail` 또는 `Failed: RED: …`)
- PASS면 RED 무효 — Then에 assert·더미가 섞이지 않았는지 점검

## 완료 보고 (응답 마지막)

| 항목 | 내용 |
|------|------|
| Test ID | `D-LOC-01` 등 |
| pytest | **FAIL** — `Failed: RED: …` 한 줄 |
| 변경 파일 | `tests/test_….py` [, `tests/conftest.py`] |

완료 한 줄:

```
pytest FAIL 확인 — GREEN 준비됐다
```

## 금지

| 금지 | 이유 |
|------|------|
| `src/` 수정 | GREEN 선행 |
| assert 본문 (Then) | 스켈레톤 단계 — GREEN에서 작성 |
| `pytest.skip` / `pytest.xfail` | TDD SSOT |
| 통과 더미 (`pass`, 빈 assert, `return`) | RED 무효 |
| 한 번에 테스트 함수 여러 개 | 1 RED 묶음 = 1 함수 |
| Domain Mock (Logic Track) | `/red-test-plan` 블록 4 |
| E001~E005 ECB emit | 후속 단계 |
| GREEN / REFACTOR | 본 Command 범위 밖 |

## Command 체인

```
/red-test-plan  →  /red-skeleton  →  pytest FAIL  →  GREEN  →  /pytest-validate  →  /review-rules
                         ↑ 본 Command
```

---

## 실행 예시

```
/red-skeleton
```

```
Phase: red | Layer: entity | Track: Logic
이번 RED 묶음: D-LOC-01 (FR-LOC-01)
```

설계표 블록 3의 파일·함수명·픽스처를 그대로 따른다.
