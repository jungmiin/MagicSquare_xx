# MagicSquare_XX — PRD (Product Requirements Document)

**작성일:** 2026-06-10  
**버전:** 0.1.0  
**SSOT 순위:** 본 문서 → `.cursorrules` → `report/MagicSquare_XX_STEP2_Workbook.md` → `.cursor/commands/`

---

## 1. 문서 목적

본 PRD는 **4×4 부분 마방진 시뮬레이터**의 제품 요구사항·기능 ID(FR)·테스트 ID·API 계약을 한곳에 정의한다. TDD 설계(`/red-test-plan`), 구현, 리뷰 시 **1차 참조 문서**이다.

---

## 2. 제품 비전 (북극성)

> **마방진 시뮬레이터** — 부분 마방진 풀이 과정을 **상태 추적·단계별 검증**으로 재현하는 도구.

### 최종 목표 (풀이 성공)

학습자가 ECB 패턴 기반 **4×4 부분 마방진**(빈칸 2개, 합 34)을 채워, **10선 모두 합 34**인 완성 격자에 도달한다.

### 파이프라인

```
풀이 성공 (빈칸 2개 채움 + 10선 합 34)
    ↑
validate_lines — 10선 검증 (can_verify=True 이후)
    ↑
assess_partial_trust — 부분 상태 신뢰 관문
    ↑
entity 계층 — 좌표·상수 등 도메인 기반 (Dual-Track TDD)
```

---

## 3. 문제 정의

### 3.1 진짜 문제 (Mom Test, 한 문장)

4×4 부분 마방진을 체계적 절차 없이 검산·추론하다 **어느 시점의 부분 상태까지 믿을 수 있는지 판정하지 못해** 수정이 오염되고, 30분~1시간을 쓴 뒤에도 결과를 재현·신뢰할 수 없어 중단한다. 핵심은 **풀이·검증 방법 자체가 명확하지 않았던 것**이다.

### 3.2 Mom Test 증거

| # | 인용 요지 |
|---|-----------|
| E1 | 지운 자국, X, `?` 후보, 취소 숫자가 섞여 **주어진 값 vs 추론값 구분 불가** |
| E2 | 계속하면 **검산이 아니라 오염된 기억으로 억지 수정**하는 것 같아 멈춤 |
| E3 | 코드에서 **「부분 상태를 어디까지 유효하다고 볼 것인가」** 에서 막힘 |

### 3.3 표면 문제 (이번 제품 범위 밖)

Mom Test에서 **기록만** 하고 제품 요구로 승격하지 않는다.

| 표면 욕구 | 제외 사유 |
|-----------|-----------|
| Cell `state` 필드, 주어진/추론 UI 구분 | 신뢰 **판정 API**로 경계 고정 |
| 백트래킹·리셋 프로그램/로직 | 재시작 UX — 이번엔 **판정**만 |
| "처음부터 다시" 리셋 기능 | 포기 직전 노트 — UX 아님 |
| 실패 과정 설명 슬라이드 | 과제 산출물 — 코드 계약 무관 |
| Solver, PyQt UI, BCE 전체 | 범위 초과 |

---

## 4. 페르소나

| 항목 | 내용 |
|------|------|
| **대상** | 4×4 부분 마방진을 손·코드로 다루는 **학습자** |
| **과제** | ECB 패턴, `?` 2칸, 1~16 중복 없음, 각 선 합 **34** |
| **개발자 역할** | 풀이·검증 경계를 코드로 고정하는 **TDD 개발자** (동일 페르소나 내 이중 역할) |
| **비용** | 손 풀이 약 30분 포기, 전체 45~60분, 이후 재시도 없음 |

---

## 5. R-G-I-O

| | 내용 |
|---|------|
| **Role** | 4×4 부분 마방진 **풀이 성공**을 목표로 격자를 채우는 학습자 — 풀이·검증 경계를 TDD로 고정하는 개발자 |
| **Goal** | **최종:** 빈칸 2개를 올바르게 채워 10선 합 34 **풀이 성공**. **단계:** (1) `original` vs `working` **신뢰 판정** → (2) `can_verify=True` 시 **10선 검증** → (3) entity 도메인 함수로 좌표·규칙 기반 확장 |
| **Input** | `original` / `working` (신뢰 API) · `grid` (10선 API) · G1 픽스처 격자 (테스트 SSOT) |
| **Output** | `status` · `can_verify` · `violations` (신뢰) · `status` · `failed_lines` (10선) · 도메인 함수 반환값 (entity) |

---

## 6. 도메인 모델

### 6.1 격자 규칙

| 항목 | 규칙 |
|------|------|
| 크기 | 4×4 (`GRID_SIZE = 4`) |
| 인덱스 | `grid[row][col]`, row·col 모두 **0~3** |
| 빈칸 | `0` |
| 값 | `1~16` (`CELL_MAX = 16`) |
| 마법 상수 | **34** (`MAGIC_SUM = 34`) — 행·열·대각선 각 선의 합 |
| 부분 마방진 | 빈칸 **정확히 2개** (G1 기준) |

### 6.2 G1 격자 (테스트 SSOT)

`tests/conftest.py` — 문제에서 주어진 격자, 빈칸 `(1,3)`, `(2,2)` (0-index):

```
[16,  3,  2, 13]
[ 5, 10, 11,  0]
[ 9,  6,  0, 12]
[ 4, 15, 14,  1]
```

완성 시 빈칸 값: `(1,3)=7`, `(2,2)=8`.

### 6.3 10선 ID

| 유형 | ID | 좌표 |
|------|-----|------|
| 행 | `R1`~`R4` | `grid[0]`~`grid[3]` |
| 열 | `C1`~`C4` | `grid[r][0]`~`grid[r][3]` |
| 대각 | `D1` | `(0,0)→(3,3)` |
| 대각 | `D2` | `(0,3)→(3,0)` |

### 6.4 좌표 체계 (entity)

- **테스트·golden:** 1-index, row-major — 예: `[(2, 3), (4, 4)]` = G1 빈칸
- **격자 배열:** 0-index `grid[row][col]`

---

## 7. 기능 요구사항 (FR)

### 7.1 FR-TRUST — 부분 상태 신뢰 판정

**API:** `assess_partial_trust(original, working) -> dict`  
**모듈:** `src/assess_partial_trust.py`  
**Mom Test 연결:** E1~E3 — 주어진 칸 보존·오염 차단·검증 허용 경계

| FR ID | 요구사항 | Rule | Mom Test |
|-------|----------|------|----------|
| **FR-TRUST-01** | `original`에서 `≠0`인 칸은 `working`에서 **동일**해야 한다. 불일치 시 `contaminated`, 해당 칸 `violations`에 **R1** 기록 | R1 | E1 |
| **FR-TRUST-02** | `original`에서 `0`인 칸만 `working`에서 `0` 또는 `1~16`으로 변경 가능 (R1과 함께 판정) | R2 | — |
| **FR-TRUST-03** | `working` 값이 `0` 또는 `1~16` 범위 밖이면 `contaminated`, **R3** 기록 | R3 | — |
| **FR-TRUST-04** | R1·R3 위반 시 `status="contaminated"`, `can_verify=False`, `violations` **전수** 기록 (누락 금지) | R4 | E2 |
| **FR-TRUST-05** | R1~R3 모두 통과 시 `status="trusted"`, `can_verify=True`, `violations=[]` | — | E3 |
| **FR-TRUST-06** | `contaminated`이면 `can_verify`는 **항상 `False`** | — | E2 |

#### 출력 계약

```python
{
    "status": "trusted" | "contaminated",
    "can_verify": bool,  # trusted일 때만 True
    "violations": [
        {"rule_id": str, "row": int, "col": int, "original": int, "working": int}
    ]
}
```

#### Test ID (src/boundary)

| Test ID | FR | Given | When | Then |
|---------|-----|-------|------|------|
| **T-TRUST-01** | FR-TRUST-05 | G1 `original`, 빈칸만 7·8로 채운 `working` | `assess_partial_trust` | `trusted`, `can_verify=True`, `violations=[]` |
| **T-TRUST-02** | FR-TRUST-01,04,06 | G1 `original`, 주어진 칸 `(1,1)` 10→11 변경 | `assess_partial_trust` | `contaminated`, `can_verify=False`, R1 violation at (1,1) |

> **Handoff:** `can_verify=True`일 때 `working`을 `validate_lines`에 넘긴다.

---

### 7.2 FR-VAL — 10선 검증

**API:** `validate_lines(grid) -> dict`  
**모듈:** `src/validate_lines.py`  
**선행 조건:** `assess_partial_trust`에서 `can_verify=True` (신뢰된 `working`)

| FR ID | 요구사항 |
|-------|----------|
| **FR-VAL-01** | 선 중 하나라도 `0`(빈칸) 포함 시 `status="incomplete"` — 합 34 판정 보류 |
| **FR-VAL-02** | 10선 모두 합 **34**, 빈칸 없으면 `status="pass"` |
| **FR-VAL-03** | 빈칸 없으나 합 ≠ 34인 선 1개 이상 시 `status="fail"`, `failed_lines`에 해당 ID **전부** |
| **FR-VAL-04** | `failed_lines` 항목은 `R1`~`R4`, `C1`~`C4`, `D1`, `D2` 만 사용 |

#### status 판정

| status | 조건 |
|--------|------|
| `incomplete` | 선 중 하나라도 `0` 포함 |
| `pass` | 10선 모두 합 34, 빈칸 없음 |
| `fail` | 빈칸 없으나 합 ≠ 34인 선 존재 |

#### 출력 계약

```python
{
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": list[str]  # R1~R4, C1~C4, D1, D2
}
```

#### Test ID (src/boundary)

| Test ID | FR | 시나리오 (TDD RED 예정) |
|---------|-----|-------------------------|
| **T-VAL-01** | FR-VAL-02 | G1 완성 격자 → `pass`, `failed_lines=[]` |
| **T-VAL-02** | FR-VAL-03 | 완성이나 한 선 합 ≠ 34 → `fail`, 해당 `failed_lines` |
| **T-VAL-03** | FR-VAL-01 | 빈칸 잔존 → `incomplete` |

> **Rule ID 주의:** `assess_partial_trust`의 R1~R4와 `validate_lines`의 R1~D2는 **동일 ID·다른 의미** — 네임스페이스 분리 유지.

---

### 7.3 FR-LOC — 빈칸 좌표 탐색 (entity)

**API:** `find_blank_coords(grid) -> list[tuple[int, int]]`  
**모듈:** `entity/locate.py`  
**Track:** Logic (`entity/`) · Test ID 접두 `D-`

| FR ID | 요구사항 |
|-------|----------|
| **FR-LOC-01** | 격자에서 값 `0`인 칸의 좌표를 **1-index row-major** 순으로 반환한다 |

#### Test ID (entity / Track B)

| Test ID | FR | Given | When | Then |
|---------|-----|-------|------|------|
| **D-LOC-01** | FR-LOC-01 | G1 `grid_g1` | `find_blank_coords` | `[(2, 3), (4, 4)]` |

---

### 7.4 FR-CONST — 도메인 상수 (entity)

**모듈:** `entity/constants.py`

| FR ID | 요구사항 | 상수 |
|-------|----------|------|
| **FR-CONST-01** | 격자·마방진 매직넘버는 `entity/constants.py` SSOT | `GRID_SIZE=4`, `MAGIC_SUM=34`, `CELL_MAX=16` |

---

## 8. 성공 기준

| # | 기준 | FR | Mom Test |
|---|------|-----|----------|
| **S1** | 주어진 칸 변경 → `contaminated`, R1 `violations` 기록 | FR-TRUST-01 | E1 |
| **S2** | `contaminated` → `can_verify` 항상 `False` | FR-TRUST-06 | E2 |
| **S3** | R1~R3 통과 → `trusted`, `can_verify=True`, `violations=[]` | FR-TRUST-05 | E3 |
| **S4** | `trusted`+빈칸 잔존 `working` → `validate_lines` `incomplete` | FR-VAL-01 | 파이프라인 연속 |
| **S5** | 완성 격자 10선 합 34 → `validate_lines` `pass` | FR-VAL-02 | 최종 풀이 성공 |
| **S6** | G1 빈칸 좌표 1-index row-major 반환 | FR-LOC-01 | 도메인 기반 |

---

## 9. Test ID 체계

| 접두 | Track | Layer | 대상 | 예시 |
|------|-------|-------|------|------|
| `D-*` | Logic (B) | `entity/` | 도메인 함수 | `D-LOC-01` |
| `U-*` | UI (A) | `boundary/` | 위젯·입력 경계 | `U-IN-01` (후속) |
| `T-TRUST-*` | src | `src/` | `assess_partial_trust` | `T-TRUST-01` |
| `T-VAL-*` | src | `src/` | `validate_lines` | `T-VAL-01` |

### C2C 규칙

| Rule | 내용 |
|------|------|
| C2C-1 | **판단 포함** FR·성공 기준만 To-Do 변환 |
| C2C-2 | **1 To-Do : 1 Test Case** — RED 묶음 = 테스트 함수 1개 |
| C2C-3 | **RED 먼저** — pytest **FAIL** 확인 후 GREEN |

---

## 10. TDD·개발 방법론

### 10.1 ARRR ↔ TDD

| ARRR | TDD | Command |
|------|-----|---------|
| Ask | RED ③ | `/red-test-plan` |
| Ask | RED ④ | `/red-skeleton`, `/tdd-red` |
| Respond | GREEN | `/green-minimal`, `/golden-master` |
| Refine | REFACTOR | `/refactor-smell`, `/refactor-safe` |

### 10.2 Phase 선언 (응답 첫 줄)

```
Phase: red    | Layer: entity   | Track: Logic
Phase: green  | API: validate_lines | Scope: src/ + tests/
```

### 10.3 RED 금지

- `src/`·`entity/` 구현 선행 (스켈레톤 단계)
- `pytest.skip` · `pytest.xfail`
- assert 완화·기대값 변경으로 강제 통과
- 표면 솔루션 (Cell `state`, 백트래킹, Solver, PyQt UI)

### 10.4 REFACTOR Change Budget

| 항목 | 상한 |
|------|------|
| 파일 | ≤ 3 |
| 클래스 | ≤ 1 |
| 메서드 | ≤ 3 |

---

## 11. 프로젝트 구조

```
docs/PRD.md                          # 본 문서 (FR·Test ID SSOT)
.cursorrules                         # Rule·API·TDD 계약 (현재 validate_lines 기준)
entity/
  constants.py                       # GRID_SIZE, MAGIC_SUM, CELL_MAX
  locate.py                          # find_blank_coords
src/
  assess_partial_trust.py            # 신뢰 판정 API
  validate_lines.py                  # 10선 검증 API
tests/
  conftest.py                        # grid_g1, grid_g1_original
  test_assess_partial_trust.py       # T-TRUST-*
  test_validate_lines.py             # T-VAL-*
  entity/test_d_loc_01.py            # D-LOC-01
report/                              # STEP 보고서·Mom Test
prompts/                             # 세션 프롬프트 Export
.cursor/commands/                    # TDD·Export Command
.cursor/skills/magic-square-tdd/     # Dual-Track TDD Skill
pyproject.toml                       # pytest 설정
```

---

## 12. 구현 상태 (2026-06-10)

| 구분 | API / Test ID | Phase | 상태 |
|------|---------------|-------|------|
| entity | `D-LOC-01` / `find_blank_coords` | RED | 스켈레톤 — `pytest.fail` |
| src | `T-TRUST-01`, `T-TRUST-02` | RED | `NotImplementedError` — 테스트 존재 |
| src | `T-VAL-*` / `validate_lines` | Harness | 시그니처·import만, 테스트 0건 |
| entity | `FR-CONST-01` | GREEN | `constants.py` 완료 |

### pytest 게이트

```bash
python -m pytest tests/test_assess_partial_trust.py -v
python -m pytest tests/test_validate_lines.py -v --collect-only
python -m pytest tests/entity/test_d_loc_01.py -v
python -m pytest tests/ -v
```

---

## 13. 비기능 요구사항

| 항목 | 요구 |
|------|------|
| 언어 | Python ≥ 3.11 |
| 테스트 | pytest ≥ 8.0 |
| AI 응답 | 한국어 |
| git | commit·push는 사용자 명시 요청 시만 |
| 계층 | `entity/` → `boundary/`·`control/` import 금지 |
| golden | `int[6]` 1-index, `UPDATE_GOLDEN` 없이 matched 유지 |

---

## 14. 관련 문서

| 문서 | 설명 |
|------|------|
| [MagicSquare_XX_MomTest_STEP1.md](../report/MagicSquare_XX_MomTest_STEP1.md) | Mom Test · 진짜/표면 문제 |
| [MagicSquare_XX_MomTest_Simulation.md](../report/MagicSquare_XX_MomTest_Simulation.md) | 가상 인터뷰 시뮬레이션 |
| [MagicSquare_XX_STEP2_Workbook.md](../report/MagicSquare_XX_STEP2_Workbook.md) | 세션 3 R-G-I-O 워크북 |
| [MagicSquare_XX_STEP3_ValidateLinesSetup.md](../report/MagicSquare_XX_STEP3_ValidateLinesSetup.md) | validate_lines Harness |
| [MagicSquare_XX_STEP4_RGIOGoalReview.md](../report/MagicSquare_XX_STEP4_RGIOGoalReview.md) | R-G-I-O·북극성 리뷰 |
| `.cursorrules` | Rule·API·TDD SSOT (런타임 계약) |
| `.cursor/skills/magic-square-tdd/SKILL.md` | Dual-Track TDD 워크플로 |

---

## 15. 변경 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 0.1.0 | 2026-06-10 | 초안 — Mom Test·워크북·STEP3/4·코드베이스 통합 PRD |
