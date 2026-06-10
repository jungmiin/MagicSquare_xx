---
name: magic-square-tdd
description: >-
  MagicSquare_XX Dual-Track TDD (ARRR, C2C, RED/GREEN/REFACTOR, pytest.fail,
  golden). Use when Phase is red, green, or refactor; when running Commands
  /red-test-plan, /red-skeleton, /green-minimal, /refactor-safe; or when the
  user mentions TDD, RED, GREEN, REFACTOR, Dual-Track, C2C, or pytest.fail.
disable-model-invocation: true
---

# MagicSquare_XX TDD

4×4 마방진 · Dual-Track TDD 워크플로 SSOT. 모든 TDD 응답은 **한국어**.

## SSOT (읽기 우선순위)

| # | 문서 | 용도 |
|---|------|------|
| 1 | `docs/PRD.md` | FR ID · Test ID · 요구사항 |
| 2 | `.cursorrules` | Rule·API·TDD 계약 |
| 3 | `report/MagicSquare_XX_STEP2_Workbook.md` | 세션 주제 · R-G-I-O |
| 4 | `.cursor/commands/` | Phase별 Command 절차 |

`docs/PRD.md` 없으면 `.cursorrules` + 워크북 + 채팅으로 추론하고 출처 명시.

---

## 1. ARRR ↔ TDD 매핑

| ARRR | TDD | 단계 | Command | Scope |
|------|-----|------|---------|-------|
| **Ask** | **RED** | ③ 설계 | `/red-test-plan` | 문서만 — `tests/`·`src/` 생성 금지 |
| **Ask** | **RED** | ④ 스켈레톤 | `/red-skeleton` | `tests/` only — `pytest.fail` |
| **Respond** | **GREEN** | 최소 구현 | `/green-minimal` | `entity/`·`src/` + `tests/` |
| **Respond** | **GREEN** | Approval | `/golden-master` | `tests/_approval.py` · golden |
| **Refine** | **REFACTOR** | ⑦ 탐지 | `/refactor-smell` | 읽기만 — 수정 금지 |
| **Refine** | **REFACTOR** | Safe | `/refactor-safe` | 스멜 1건 · Budget 내 |

흐름: **Ask(RED) → Respond(GREEN) → Refine(REFACTOR)**. RED 없이 GREEN 금지.

---

## 2. Phase 선언 (응답 첫 줄)

Command·Phase 작업 시 **반드시 첫 줄**에 선언.

```
Phase: red    | Layer: entity   | Track: Logic
Phase: red    | Layer: boundary | Track: UI
Phase: green  | Layer: entity   | Track: Logic
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
Phase: refactor | Layer: entity | Track: Logic
```

| 필드 | 값 |
|------|-----|
| `Layer` | `entity` (도메인) · `boundary` (UI·입출력) |
| `Track` | `Logic` ↔ entity · `UI` ↔ boundary |

레거시 (`.cursorrules`): `Phase: red | API: validate_lines | Scope: tests/ only`

---

## 3. C2C Rule 1~3

| Rule | 내용 |
|------|------|
| **1** | **판단 포함** FR·성공 기준만 To-Do 변환 (순수 데이터·상수 제외) |
| **2** | **1 To-Do : 1 Test Case** — RED 묶음 = 테스트 함수 1개 |
| **3** | **RED 먼저** — `pytest` **FAIL** 확인 후 GREEN |

---

## 4. RED 절대 금지

| 금지 | 비고 |
|------|------|
| `src/`·`entity/` **구현** (스켈레톤 단계) | `/green-minimal` 역할 |
| `pytest.skip` · `pytest.xfail` | |
| assert 완화 · 기대값 변경으로 통과 | |
| Then에 assert 본문 (`/red-skeleton`) | `pytest.fail` 한 줄만 |
| **Logic Track Domain Mock** | 도메인 규칙 mock 금지 |
| E001~E005 emit | ECB 후속 |
| 표면 솔루션 | Cell `state`, 백트래킹, Solver, PyQt UI |
| 한 RED 묶음에 테스트 여러 개 | |

RED 확인: 대상 테스트 **FAIL**. PASS면 RED 무효.

### RED 스켈레톤 Then

```python
pytest.fail("RED: D-LOC-01 — …")
```

---

## 5. GREEN

| 규칙 | 내용 |
|------|------|
| **1커밋 = 1 RED 묶음** | 이번 Test ID 외 동시 해결 금지 |
| **최소 구현** | Then 만족하는 코드만 |
| **constants SSOT** | `entity/constants.py` — `GRID_SIZE`·`MAGIC_SUM`·`CELL_MAX` |
| **매직넘버 금지** | `4`/`34`/`16` 리터럴 → import |
| **pytest.fail 제거** | 설계표 Then 기준 assert 로 교체 |
| **ECB** | E001~E005 raise/return/emit 금지 |
| **계층** | `entity/` → `boundary/`·`control/` import 금지 |

`can_verify`는 `status=="trusted"`일 때만 `True` (신뢰 API 해당 시).

git commit·push: **사용자 명시 요청 시만**.

---

## 6. REFACTOR

### 게이트

```bash
python -m pytest tests/ -v
```

전부 PASS 아니면 리팩터 **중단**.

### Change Budget (`/refactor-safe`)

| 항목 | 상한 |
|------|------|
| 파일 | ≤ 3 |
| 클래스 | ≤ 1 |
| 메서드 | ≤ 3 |

### Safe Refactor 원칙

- 입출력·예외·**int[6] 1-index**·golden 포맷 **불변**
- 기능 추가·버그 수정 금지 → `/green-minimal`
- **golden 유지**: `UPDATE_GOLDEN` 없이 matched — diff 비의도 시 **롤백**
- golden 수동 편집 금지
- `/refactor-smell`: 탐지만 · `/refactor-safe`: 스멜 **1개**만

---

## 7. Dual-Track — Track A vs Track B

| | **Track B (Logic)** | **Track A (UI)** |
|---|---------------------|------------------|
| Layer | `entity` | `boundary` |
| Track | `Logic` | `UI` |
| 대상 | `entity/` · `src/` API | 위젯·입력 경계 |
| Test ID | `D-*` | `U-*` |
| Mock | **Domain Mock 금지** | 경계만 stub; 도메인 mock 금지 |
| RED Then | `pytest.fail` | 동일 |
| Command | Layer·Track만 바꿔 재사용 | |

---

## 8. Command 체인

```
/red-test-plan
    → /red-skeleton      (pytest FAIL)
    → /green-minimal     (pytest PASS)
    → /golden-master     (golden matched)
    → /pytest-validate
    → /refactor-smell    (탐지만)
    → /refactor-safe     (스멜 1건)
    → /review-rules
```

| Command | Phase | 수정 |
|---------|-------|------|
| `/red-test-plan` | red Ask ③ | 없음 |
| `/red-skeleton` | red Ask ④ | `tests/` |
| `/green-minimal` | green | `entity/`·`src/`·`tests/` |
| `/golden-master` | green | `tests/_approval.py` · `tests/golden/` |
| `/refactor-smell` | refactor | 없음 |
| `/refactor-safe` | refactor | Budget 내 |

---

## 9. pytest 명령 패턴

```bash
# RED — 단일 스켈레톤 (FAIL 기대)
python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v

# GREEN — 대상 파일
python -m pytest tests/entity/test_d_loc_01.py -v

# 회귀·게이트·REFACTOR 완료
python -m pytest tests/ -v

# Golden 기준 생성 (최초·의도적 갱신만)
# PowerShell:
$env:UPDATE_GOLDEN="1"; python -m pytest tests/entity/test_d_sol_01.py -v; Remove-Item Env:UPDATE_GOLDEN
# bash:
UPDATE_GOLDEN=1 python -m pytest tests/entity/test_d_sol_01.py -v
```

| Phase | 기대 |
|-------|------|
| RED 스켈레톤 | **FAIL** (`pytest.fail` / `NotImplementedError`) |
| GREEN | 대상 **PASS** |
| REFACTOR 게이트 | `tests/` **전부 PASS** |
| golden | `UPDATE_GOLDEN` 없이 **matched** |

### 픽스처 · 포맷 SSOT

- `tests/conftest.py` — `grid_g1` (G1, 빈칸 2개, row-major)
- golden `int[6]`: 1-index, 공백 구분 한 줄
- golden 에러 코드: `ERR_SNAKE_CASE` 한 줄

---

## 10. 완료 보고 형식

### RED (`/red-skeleton`)

```
Phase: red | Layer: entity | Track: Logic
Test ID: D-LOC-01
pytest: FAIL — Failed: RED: D-LOC-01 — …
변경: tests/entity/test_d_loc_01.py [, tests/conftest.py]
```

### GREEN (`/green-minimal`)

```
Phase: green | Layer: entity | Track: Logic
Test ID: D-LOC-01 — PASS
pytest: 1 passed
변경: entity/locate.py, tests/entity/test_d_loc_01.py
```

### Golden (`/golden-master`)

```
golden: tests/golden/d-sol-01.approved.txt
matched: yes
diff: —
```

### REFACTOR (`/refactor-safe`)

```
후보: RF-02 · Duplicated Code
변경: _line_sum extract · entity/validation.py
Budget: 파일 2 · 메서드 2
pytest: N passed
golden matched: yes / n/a
```

### 공통

- Phase · Test ID · pytest PASS/FAIL **한 줄**
- 변경 파일 목록
- git commit: 사용자 요청 시만
- 모든 응답 **한국어**

---

## 도메인 요약 (`.cursorrules`)

- 4×4 격자: `0` = 빈칸, `1~16` = 값 · `grid[row][col]` 0~3
- 마법 상수 **34** · 10선: `R1`~`R4`, `C1`~`C4`, `D1`, `D2`
- 핵심 API 예: `validate_lines(grid)` → `status`, `failed_lines`

상세 Rule·FR은 SSOT 문서 참조.
