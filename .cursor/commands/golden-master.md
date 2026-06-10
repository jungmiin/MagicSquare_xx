# Golden Master — Approval Test 구축·검증

GREEN **PASS** 직후, 대상 Test ID 의 출력을 **Golden Master(Approval Test)** 로 고정·검증한다.  
회귀 시 diff 로 계약 이탈을 잡는다 — golden 파일 **수동 편집으로 통과 우회 금지**.

> **Skill:** `magic-square-tdd` Skill이 있으면 자동 따름 (Phase 선언 · pytest · 완료 보고).

## 전제

| 항목 | 조건 |
|------|------|
| 대상 Test ID | `/green-minimal` 완료 — **pytest PASS** |
| 대상 테스트 | 채팅·인자로 지정 (예: `D-SOL-01`, `tests/entity/test_d_sol_01.py::test_d_sol_01_step_a_success`) |
| 구현 | 이미 GREEN — 본 Command는 **golden 인프라·검증**만 |

**PASS 미확인 시** 구현을 진행하지 않고 아래만 응답한다:

```
Golden Master 진행을 위해 GREEN PASS 단계를 완료해 주세요.
```

선행 확인:

```bash
python -m pytest <대상 테스트 경로> -v
```

`1 passed` 가 아니면 `/green-minimal` 을 먼저 완료한다.

## 필수 선언 (응답 첫 줄)

```
Phase: green | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| `Layer` | `entity` \| `boundary` | 대상 Test ID Track 과 동일 |
| `Track` | `Logic` \| `UI` | 대상 Test ID Track 과 동일 |

## 절차

### 1. `tests/_approval.py` — `assert_matches_golden`

파일이 없으면 생성한다. golden 비교 헬퍼 SSOT.

```python
"""Golden Master approval helpers."""

from __future__ import annotations

import os
from pathlib import Path

_GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def _format_actual(actual: str | list[int]) -> str:
    if isinstance(actual, list):
        # int[6] 1-index — 공백 구분, 대괄호 없음
        return " ".join(str(x) for x in actual)
    return actual.strip()


def assert_matches_golden(
    test_id: str,
    actual: str | list[int],
    *,
    golden_dir: Path | None = None,
) -> None:
    """Compare actual output to tests/golden/{test_id}.approved.txt."""
    base = golden_dir or _GOLDEN_DIR
    golden_path = base / f"{test_id.lower()}.approved.txt"
    formatted = _format_actual(actual)

    if os.environ.get("UPDATE_GOLDEN") == "1":
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(formatted + "\n", encoding="utf-8")
        return

    if not golden_path.is_file():
        raise AssertionError(
            f"golden missing: {golden_path} — run with UPDATE_GOLDEN=1 first"
        )

    expected = golden_path.read_text(encoding="utf-8").strip()
    if formatted != expected:
        raise AssertionError(
            f"golden mismatch [{test_id}]\n"
            f"  expected ({golden_path}):\n    {expected!r}\n"
            f"  actual:\n    {formatted!r}"
        )
```

- 테스트에서는 `from tests._approval import assert_matches_golden` 또는 상대 import 로 사용
- `UPDATE_GOLDEN=1` 일 때만 golden 파일 **쓰기** — 그 외는 읽기·비교만

### 2. Golden 파일 연결 — `tests/golden/{id}.approved.txt`

| 항목 | 규칙 |
|------|------|
| **경로** | `tests/golden/{test_id_lower}.approved.txt` |
| **예** | `D-SOL-01` → `tests/golden/d-sol-01.approved.txt` |
| **생성** | `UPDATE_GOLDEN=1` pytest 로만 생성·갱신 |
| **수동 편집** | **금지** — 통과 우회·계약 변경 불가 |

대상 테스트 Then 에 approval 호출 추가 (기존 assert 유지 가능):

```python
from tests._approval import assert_matches_golden

def test_d_sol_01_step_a_success(grid_g1):
    # Given / When …
    result = solve_step_a(grid_g1)  # 예: int[6] 1-index

    # Then — 단위 assert + golden
    assert len(result) == 6
    assert_matches_golden("D-SOL-01", result)
```

에러 코드 케이스는 **문자열** 로 golden 에 고정:

```python
assert_matches_golden("D-SOL-02", "ERR_DUPLICATE_VALUE")
```

### 3. 출력 포맷 SSOT (고정)

| 유형 | 포맷 | 예 |
|------|------|-----|
| **int[6] 1-index** | 6개 정수, **1-based**, 공백 구분, 한 줄 | `2 3 4 4 1 1` |
| **에러 코드** | 대문자 `SNAKE_CASE` 문자열, 한 줄 | `ERR_BLANK_NOT_FOUND` |

- 0-index · 쉼표 구분 · JSON · 대괄호 `[]` **금지**
- 포맷 변경은 `_approval._format_actual` SSOT 한 곳에서만

### 4. 기준 파일 생성 — `UPDATE_GOLDEN=1`

**최초 1회** (또는 구현 변경 후 의도적 갱신):

```bash
# Windows PowerShell
$env:UPDATE_GOLDEN="1"; python -m pytest tests/entity/test_d_sol_01.py::test_d_sol_01_step_a_success -v; Remove-Item Env:UPDATE_GOLDEN

# bash
UPDATE_GOLDEN=1 python -m pytest tests/entity/test_d_sol_01.py::test_d_sol_01_step_a_success -v
```

- 생성·갱신된 파일: `tests/golden/d-sol-01.approved.txt`
- 생성 직후 내용을 **검토**한다 (수동 수정하지 않고, 구현이 맞는지 확인)

### 5. matched 확인 — `UPDATE_GOLDEN` 없이

```bash
python -m pytest tests/entity/test_d_sol_01.py::test_d_sol_01_step_a_success -v
```

- 기대: **PASS** — `assert_matches_golden` 이 golden 과 **일치**
- FAIL 시 diff 는 `AssertionError` 메시지의 `expected` / `actual` — **구현 수정**, golden 수동 편집 금지

## 금지

| 금지 | 이유 |
|------|------|
| golden `.approved.txt` **수동 편집** | Approval Test 우회 |
| PASS 전 golden 생성 | 기준이 미검증 구현에 묶임 |
| 포맷 임의 변경 (0-index, JSON 등) | diff 비교 불가 |
| 이번 Test ID 외 golden 일괄 갱신 | 1묶음 = 1 golden |
| `UPDATE_GOLDEN` 없이 golden 덮어쓰기 | 절차 위반 |
| REFACTOR·다른 Test ID GREEN | 본 Command 범위 밖 |

## 완료 보고 (응답 마지막)

| 항목 | 내용 |
|------|------|
| **Test ID** | `D-SOL-01` 등 |
| **golden 경로** | `tests/golden/d-sol-01.approved.txt` |
| **matched** | `yes` / `no` |
| **diff 요약** | 불일치 시 `expected` vs `actual` 한 줄; 일치 시 `—` |
| **변경 파일** | `tests/_approval.py`, `tests/golden/…`, 대상 테스트 (approval 호출 추가 시) |

완료 한 줄:

```
Golden Master matched — 회귀 방어 준비됐다
```

### git

- commit·push 는 사용자 **명시 요청 시만**
- 권장 메시지: `golden: D-SOL-01 approval baseline`

## Command 체인

```
/red-test-plan  →  /red-skeleton  →  /green-minimal  →  /golden-master  →  /pytest-validate  →  /review-rules
                                                              ↑ 본 Command
```

---

## 실행 예시

### PASS 확인 후

```
/golden-master
```

```
Phase: green | Layer: entity | Track: Logic
대상: D-SOL-01
```

### 테스트 경로 명시

```
/golden-master
대상: D-SOL-01 (tests/entity/test_d_sol_01.py::test_d_sol_01_step_a_success)
```

### PASS 미완 시 응답

```
Golden Master 진행을 위해 GREEN PASS 단계를 완료해 주세요.
```
