# MagicSquare_XX

4×4 **부분 마방진** 풀이 과정을 상태 추적·단계별 검증으로 재현하는 **마방진 시뮬레이터** 프로젝트입니다.

ECB 패턴 기반 격자(빈칸 2개, 각 선 합 34)를 학습자가 채우는 동안, **부분 상태가 신뢰할 수 있는지** 판정하고 **10선 검증**으로 풀이 성공 여부를 확인합니다. [Mom Test](report/MagicSquare_XX_MomTest_STEP1.md)에서 도출한 진짜 문제 — *어느 시점의 부분 상태까지 믿을 수 있는지 판정하지 못해 수정이 오염된다* — 를 TDD로 코드 계약에 고정합니다.

상세 요구사항은 [docs/PRD.md](docs/PRD.md)를 참조하세요.

---

## 목표

| 단계 | API | 역할 |
|------|-----|------|
| 1 | `assess_partial_trust` | `original` vs `working` — 주어진 칸 보존·오염 판정 |
| 2 | `validate_lines` | `can_verify=True` 이후 10선 합 34 검증 |
| 3 | `entity/` | 좌표·상수 등 도메인 기반 (Dual-Track TDD) |

**최종 목표:** 빈칸 2개를 올바르게 채워 10선 모두 합 **34**인 완성 격자에 도달.

```
풀이 성공
    ↑ validate_lines
    ↑ assess_partial_trust
    ↑ entity (좌표·상수)
```

---

## 빠른 시작

### 요구 사항

- Python ≥ 3.11
- pytest ≥ 8.0 (개발 의존성)

### 설치

```bash
pip install -e ".[dev]"
```

### 테스트 실행

```bash
# 전체
python -m pytest tests/ -v

# 신뢰 판정 (RED)
python -m pytest tests/test_assess_partial_trust.py -v

# 10선 검증 (Harness)
python -m pytest tests/test_validate_lines.py -v --collect-only

# entity — 빈칸 좌표 (RED)
python -m pytest tests/entity/test_d_loc_01.py -v
```

---

## 도메인 요약

| 항목 | 값 |
|------|-----|
| 격자 | 4×4, `grid[row][col]` (0~3) |
| 빈칸 | `0` |
| 값 | `1~16` |
| 마법 상수 | **34** (행·열·대각선 각 선의 합) |
| 10선 ID | `R1`~`R4`, `C1`~`C4`, `D1`, `D2` |

### G1 테스트 격자 (빈칸 2개)

```
[16,  3,  2, 13]
[ 5, 10, 11,  0]   ← (1,3) 빈칸
[ 9,  6,  0, 12]   ← (2,2) 빈칸
[ 4, 15, 14,  1]
```

완성 시 빈칸: `(1,3)=7`, `(2,2)=8`.

---

## 핵심 API

### `assess_partial_trust(original, working)`

부분 상태 신뢰 판정. `original`은 문제에서 주어진 격자, `working`은 학습자 작업 격자.

```python
{
    "status": "trusted" | "contaminated",
    "can_verify": bool,
    "violations": [{"rule_id", "row", "col", "original", "working"}]
}
```

- `trusted` + `can_verify=True` → 이후 `validate_lines(working)` 호출 가능
- 주어진 칸(`≠0`) 변경 시 `contaminated`, R1 위반 기록

### `validate_lines(grid)`

10선 합 34 검증.

```python
{
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": ["R1", "C2", ...]  # R1~R4, C1~C4, D1, D2
}
```

| status | 조건 |
|--------|------|
| `incomplete` | 선 중 `0`(빈칸) 포함 |
| `pass` | 10선 모두 합 34 |
| `fail` | 빈칸 없으나 합 ≠ 34인 선 존재 |

### `find_blank_coords(grid)` (entity)

값 `0`인 칸 좌표를 **1-index row-major** 순으로 반환. G1 기대값: `[(2, 3), (4, 4)]`.

---

## 프로젝트 구조

```
docs/PRD.md                 # FR·Test ID·API 계약 (SSOT)
.cursorrules                # Rule·TDD 계약
entity/
  constants.py              # GRID_SIZE, MAGIC_SUM, CELL_MAX
  locate.py                 # find_blank_coords
src/
  assess_partial_trust.py   # 신뢰 판정
  validate_lines.py         # 10선 검증
tests/
  conftest.py               # grid_g1, grid_g1_original
  test_assess_partial_trust.py
  test_validate_lines.py
  entity/test_d_loc_01.py
report/                     # Mom Test·STEP 보고서
prompts/                    # 세션 프롬프트
.cursor/commands/           # TDD Command
```

---

## TDD

**RED → GREEN → REFACTOR** (Dual-Track: Logic `entity/` · UI `boundary/`)

| Phase | Command | Scope |
|-------|---------|-------|
| RED | `/red-test-plan`, `/red-skeleton`, `/tdd-red` | `tests/` only |
| GREEN | `/green-minimal` | `entity/`, `src/`, `tests/` |
| REFACTOR | `/refactor-safe` | 파일 ≤ 3 |

- RED: pytest **FAIL** 확인 후 GREEN
- 금지: assert 완화, `skip`/`xfail`, `src/` 선행 구현

자세한 워크플로: [.cursor/skills/magic-square-tdd/SKILL.md](.cursor/skills/magic-square-tdd/SKILL.md)

---

## 구현 상태

| API / Test ID | Phase | 상태 |
|---------------|-------|------|
| `D-LOC-01` / `find_blank_coords` | RED | 스켈레톤 |
| `T-TRUST-01`, `T-TRUST-02` | RED | 테스트 존재, 미구현 |
| `T-VAL-*` / `validate_lines` | Harness | 시그니처만 |
| `FR-CONST-01` / `constants.py` | GREEN | 완료 |

---

## 문서

| 문서 | 설명 |
|------|------|
| [docs/PRD.md](docs/PRD.md) | 제품 요구사항·FR·Test ID |
| [report/MagicSquare_XX_MomTest_STEP1.md](report/MagicSquare_XX_MomTest_STEP1.md) | Mom Test · 진짜 문제 |
| [report/MagicSquare_XX_STEP2_Workbook.md](report/MagicSquare_XX_STEP2_Workbook.md) | R-G-I-O 워크북 |
| [report/MagicSquare_XX_STEP3_ValidateLinesSetup.md](report/MagicSquare_XX_STEP3_ValidateLinesSetup.md) | validate_lines Harness |
| [report/MagicSquare_XX_STEP4_RGIOGoalReview.md](report/MagicSquare_XX_STEP4_RGIOGoalReview.md) | 북극성·파이프라인 리뷰 |

---

## 범위 밖

다음은 이번 프로젝트 범위에 포함하지 않습니다.

- Cell `state` 필드, 주어진/추론 UI 구분
- 백트래킹·리셋 프로그램
- Solver, PyQt UI, BCE 전체
- 실패 과정 설명 슬라이드

---

## 라이선스

미정
