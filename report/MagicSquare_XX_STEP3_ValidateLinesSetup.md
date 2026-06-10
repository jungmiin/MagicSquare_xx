# MagicSquare_XX — STEP3 validate_lines 세팅

**작성일:** 2026-06-10  
**프롬프트:** [../prompts/MagicSquare_XX_STEP3_ValidateLinesSetup.prompt.md](../prompts/MagicSquare_XX_STEP3_ValidateLinesSetup.prompt.md)  
**범위:** `validate_lines` 10선 검증 — Harness · Rule · Command 골격 (구현·테스트 본문 없음)

---

## 1. 작업 요약

STEP2(`assess_partial_trust`) 이후 **10선 검증 API** `validate_lines` 로 전환하며, TDD를 시작할 수 있는 최소 인프라를 구축했다.

| 순서 | 작업 | 결과 |
|------|------|------|
| 1 | 최소 Harness | `pyproject.toml`(pytest), `src/validate_lines.py`(시그니처만), `tests/test_validate_lines.py`(import만) |
| 2 | `.cursorrules` 초안 | 54줄 — 도메인(4×4·34·10선), API 계약, TDD·AI 규칙 |
| 3 | `/tdd-red` 커맨드 | `validate_lines` RED 전용 — AAA·pytest·금지사항 |
| 4 | `/export` 커맨드 | `report/`·`prompts/` STEP 번호 규칙·템플릿 |

기존 `assess_partial_trust` 관련 파일(`src/assess_partial_trust.py`, `tests/test_assess_partial_trust.py` 등)은 유지. `.cursorrules` 는 `validate_lines` 기준으로 **교체**됨.

---

## 2. 산출물

| 항목 | 경로·내용 |
|------|-----------|
| Harness | `src/__init__.py`, `src/validate_lines.py`, `tests/__init__.py`, `tests/test_validate_lines.py` |
| Rule (SSOT) | `.cursorrules` — `validate_lines(grid)` → `status` / `failed_lines` |
| Command RED | `.cursor/commands/tdd-red.md` |
| Command Export | `.cursor/commands/export.md` |
| pytest 설정 | `pyproject.toml` (기존 유지) |

### API 계약 (`.cursorrules`)

```python
def validate_lines(grid: list[list[int]]) -> dict
# status: "pass" | "fail" | "incomplete"
# failed_lines: list[str]  # R1~R4, C1~C4, D1, D2
```

### 10선 ID

| 유형 | ID |
|------|-----|
| 행 | `R1`~`R4` |
| 열 | `C1`~`C4` |
| 대각 | `D1` `(0,0)→(3,3)`, `D2` `(0,3)→(3,0)` |

---

## 3. TDD·검증 상태

| Phase | 상태 | 비고 |
|-------|------|------|
| Harness | 완료 | `pytest tests/test_validate_lines.py --collect-only` → 0 tests |
| RED | **미착수** | `/tdd-red` 로 첫 실패 테스트 추가 예정 |
| GREEN | — | — |
| REFACTOR | — | — |

```bash
python -m pytest tests/test_validate_lines.py -v --collect-only
# collected 0 items (import 정상, 테스트 함수 없음)
```

---

## 4. 다음 단계

1. `/tdd-red` — `pass` / `fail` / `incomplete` 중 **한 케이스** 실패 테스트 1개 추가
2. pytest FAIL 확인 후 GREEN — `src/validate_lines.py` 최소 구현
3. `incomplete` 시 `failed_lines` 계약을 RED 테스트에서 명시적으로 고정

---

## 관련 문서

| 문서 | 설명 |
|------|------|
| [STEP2 워크북](./MagicSquare_XX_STEP2_Workbook.md) | `assess_partial_trust` 세션 (선행) |
| [Mom Test STEP1](./MagicSquare_XX_MomTest_STEP1.md) | 진짜 문제·증거 |
