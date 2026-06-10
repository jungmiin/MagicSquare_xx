# GREEN Minimal — 최소 구현 (Respond)

ARRR **R단계 (Respond = GREEN)**. 직전 `/red-skeleton` 으로 확정된 **RED 1묶음**에 대해 **최소 구현**만 추가해 해당 테스트를 **PASS** 시킨다.  
**1커밋 = RED 1묶음** — 이번 Test ID 외 케이스는 건드리지 않는다.

> **Skill:** `magic-square-tdd` Skill이 있으면 자동 따름 (Phase 선언 · C2C · GREEN 규칙 · pytest · 완료 보고).

## 선행 조건

| 항목 | 출처 |
|------|------|
| RED 스켈레톤 · pytest FAIL 확인 | `/red-skeleton` 산출물 |
| Test ID · Given/When/Then · Invariant | `/red-test-plan` 설계표 (채팅) |
| Rule·API 계약 | `.cursorrules` |
| 상수 SSOT | `entity/constants.py` |

RED 가 아직 FAIL 이 아니면 `/red-skeleton` 을 먼저 완료한다.

## 필수 선언 (응답 첫 줄)

```
Phase: green | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| `Layer` | `entity` \| `boundary` | RED 묶음과 동일 |
| `Track` | `Logic` \| `UI` | RED 묶음과 동일 |

**Track A (boundary / UI):** `Layer: boundary` · `Track: UI` 로 선언만 바꾸면 본 Command 재사용.

## 절차

1. **RED 재확인** — 대상 테스트만 실행해 **FAIL** (또는 `pytest.fail` / `NotImplementedError`) 확인
2. **최소 구현** — 이번 Test ID 의 Then 만 만족하는 코드만 작성
   - Logic Track + `entity` → `entity/` (예: `entity/locate.py`)
   - `src/` API 대상 → `src/` (예: `src/validate_lines.py`)
3. **테스트 GREEN** — `pytest.fail` 제거 · 설계표 Then 기준 **assert** 로 교체 (AAA 주석 유지)
4. **PASS 확인** — 대상 테스트 PASS 후 **파일 전체**·`tests/` 회귀 실행
5. **완료 보고** — PASS Test ID · 변경 파일 · 회귀 실패 시 즉시 수정

### 구현 범위 (최소)

| 허용 | 금지 |
|------|------|
| 이번 Test ID 가 요구하는 분기·반환값 **만** | 다른 Test ID·FR 선행 해결 |
| RED 스텁(`return []`, `NotImplementedError`) 교체 | REFACTOR (추출·이름 변경·구조 개편) |
| `entity/constants.py` import | 리터럴 `4` / `34` / `16` 하드코딩 |

## 상수 SSOT — `entity/constants.py`

매직넘버·하드코딩 금지. 구현·테스트 모두 import.

```python
from entity.constants import GRID_SIZE, MAGIC_SUM, CELL_MAX
```

| 상수 | 값 | 용도 |
|------|-----|------|
| `GRID_SIZE` | `4` | 격자 크기·반복 상한 |
| `MAGIC_SUM` | `34` | 10선 합 (필요 시만) |
| `CELL_MAX` | `16` | 값 범위 상한 |

새 상수가 필요하면 **이번 RED 묶음에 필수일 때만** `entity/constants.py` 에 추가한다.

## ECB · 계층 격리

| 규칙 | 내용 |
|------|------|
| **E001~E005** | `raise` / `return` / emit **금지** (GREEN·entity 구현에 혼입 금지) |
| **entity → boundary/control** | `entity/` 에서 `boundary/` · `control/` import **금지** |
| **Domain Mock** | Logic Track — 도메인 규칙 mock 금지 (RED 플랜과 동일) |
| **표면 솔루션** | Cell `state`, 백트래킹, Solver, PyQt UI 혼입 금지 |

## 테스트 GREEN — assert 교체

### Before (RED 스켈레톤)

```python
    # Then: …
    pytest.fail(f"RED: D-LOC-01 — result={result}, expected={expected}, …")
```

### After (GREEN)

```python
    # Then: 1-index row-major [(2,3), (4,4)]
    assert result == expected
```

- `pytest.fail` · `pass` · 빈 assert **제거**
- 설계표 **Then** 과 1:1 대응하는 assert 만 추가
- Given/When 변경으로 통과시키기 **금지** (assert 완화와 동일)

### 예시 — `D-LOC-01` (`entity/locate.py`)

```python
from entity.constants import GRID_SIZE

def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
  blanks: list[tuple[int, int]] = []
  for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
      if grid[row][col] == 0:
        blanks.append((row + 1, col + 1))  # 1-index
  return blanks
```

- `4` 대신 `GRID_SIZE` 사용
- 이번 Test ID 범위 밖 동작(정렬·검증 등) 추가 금지

## pytest

**1) 이번 RED 묶음 — 단일 테스트**

```bash
python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v
```

**2) 대상 파일 전체 (회귀·인접 케이스)**

```bash
python -m pytest tests/entity/test_d_loc_01.py -v
```

- 기대: 대상 Test ID **PASS**
- 파일 내 다른 테스트가 RED 스켈레톤이면 FAIL 허용 — **이번 묶음만** GREEN
- 전체 회귀 (선택):

```bash
python -m pytest tests/ -v
```

회귀 FAIL 시 **즉시** 원인 수정 또는 이번 GREEN 범위 초과 여부 보고.

## 완료 보고 (응답 마지막)

| 항목 | 내용 |
|------|------|
| Test ID | `D-LOC-01` 등 — **PASS** |
| pytest | `1 passed` (단일) · 파일/전체 요약 |
| 변경 파일 | `entity/locate.py`, `tests/entity/test_d_loc_01.py` 등 |

완료 한 줄:

```
GREEN PASS 확인 — REFACTOR 또는 다음 RED 묶음 준비됐다
```

### git

- **commit·push 는 사용자가 명시적으로 요청할 때만**
- 권장 메시지 형식: `green: D-LOC-01 find_blank_coords 1-index row-major`

## 금지

| 금지 | 이유 |
|------|------|
| 이번 RED 묶음 **외** Test ID 동시 해결 | 1커밋 = 1 RED 묶음 |
| REFACTOR (추출·리네임·파일 분할) | 별도 Phase |
| assert 완화 · 기대값 변경 · skip / xfail | TDD SSOT |
| `4`/`34`/`16` 리터럴 (구현·assert) | `entity/constants.py` SSOT |
| E001~E005 raise/return/emit | ECB 후속 |
| entity → boundary/control import | 계층 격리 |
| 표면 솔루션 혼입 | `.cursorrules` 범위 밖 |
| git commit (묵시적) | 사용자 요청 시만 |

## Command 체인

```
/red-test-plan  →  /red-skeleton  →  pytest FAIL  →  /green-minimal  →  pytest PASS  →  /pytest-validate  →  /review-rules
                                                          ↑ 본 Command
```

---

## 실행 예시

```
/green-minimal
```

```
Phase: green | Layer: entity | Track: Logic
이번 RED 묶음: D-LOC-01
```

직전 `/red-skeleton` 의 Test ID · 파일 · 함수명을 그대로 따른다.
