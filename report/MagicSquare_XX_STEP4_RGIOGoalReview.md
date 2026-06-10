# MagicSquare_XX — STEP4 R-G-I-O·북극성 리뷰

**작성일:** 2026-06-10  
**프롬프트:** [../prompts/MagicSquare_XX_STEP4_RGIOGoalReview.prompt.md](../prompts/MagicSquare_XX_STEP4_RGIOGoalReview.prompt.md)  
**범위:** STEP2 워크북 R-G-I-O·성공 기준 vs `validate_lines` 계약 리뷰 · 시뮬레이터 북극성 반영

---

## 1. 작업 요약

| 순서 | 작업 | 결과 |
|------|------|------|
| 1 | STEP2 워크북 R-G-I-O·성공 기준 3개 vs `validate_lines` 계약 대조 | 빠짐·어긋남 7항목 표 (리뷰만, 코드·워크북 미수정) |
| 2 | “마방진 시뮬레이터” 북극성 가시성 논의 | Mom Test 솔루션 최소화·세션 범위 분리로 최종 목표가 문서에 안 보이는 원인 정리 |
| 3 | R-G-I-O **Goal**에 풀이 성공 반영 | [`MagicSquare_XX_STEP2_Workbook.md`](./MagicSquare_XX_STEP2_Workbook.md) Role·Goal 수정 |
| 4 | `/export` | 본 보고서·프롬프트 STEP4 생성 |

### 1.1 validate_lines 계약 대조 — 빠짐·어긋남 (요약)

| 구분 | 항목 | 빠짐 / 어긋남 |
|------|------|----------------|
| R-G-I-O · Input | 후속 호출 입력 | `can_verify=True`일 때 **`working`을 `validate_lines`에 넘긴다**는 handoff 미기재 |
| R-G-I-O · Output | 상태어 매핑 | `trusted`/`contaminated` ↔ `pass`/`fail`/`incomplete` 변환 규칙 없음 |
| R-G-I-O · Output | `can_verify` 의미 | 허용 vs 통과 보장 구분 없음 |
| 성공 기준 · S3 | `incomplete` | `trusted`+`0` 잔존 시 `validate_lines` → `incomplete` 미언급 |
| 성공 기준 | validate_lines 3요소 | 10선×34 · pass/fail/incomplete · `failed_lines` 전수 — S1~S3에 없음 |
| Rule ID | R1~R4 | `assess_partial_trust` R1~R4 vs `validate_lines` R1~D2 **동일 ID·다른 의미** |
| R-G-I-O · Goal | 파이프라인 | 신뢰 판정 Goal만 있고 10선·줄 식별 Goal 연속성 없음 → **이번 세션에서 Goal 수정으로 보완** |

### 1.2 북극성·파이프라인 (문서화 방향)

```
풀이 성공 (빈칸 2개 채움 + 10선 합 34)
    ↑
validate_lines (can_verify=True 이후)
    ↑
assess_partial_trust (신뢰 관문 — STEP2 세션 3)
```

시뮬레이터 = 부분 마방진 풀이 과정을 **상태 추적·단계별 검증**으로 재현하는 도구. STEP2 워크북 Goal을 **최종(풀이 성공) / 세션 3(신뢰 판정)** 2층으로 수정함.

### 1.3 STEP2 워크북 변경 내용

| 필드 | 변경 전 | 변경 후 |
|------|---------|---------|
| **Role** | 격자를 수정하는 학습자 | **풀이 성공**을 목표로 격자를 채우는 학습자 |
| **Goal** | `trusted`/`contaminated` 판정만 | **최종:** 10선 합 34 풀이 성공 · **세션 3:** 신뢰 판정 첫 관문 |

---

## 2. 산출물

| 항목 | 경로·내용 |
|------|-----------|
| 워크북 수정 | [`report/MagicSquare_XX_STEP2_Workbook.md`](./MagicSquare_XX_STEP2_Workbook.md) — §2 R-G-I-O Role·Goal |
| 본 보고서 | `report/MagicSquare_XX_STEP4_RGIOGoalReview.md` |
| 프롬프트 | `prompts/MagicSquare_XX_STEP4_RGIOGoalReview.prompt.md` |
| SSOT (참조) | `.cursorrules` — 현재 `validate_lines` API 기준 (STEP3 이후) |

---

## 3. TDD·검증 상태

| Phase | API | 상태 | 비고 |
|-------|-----|------|------|
| RED | `assess_partial_trust` | 대기 | STEP2 범위 — `tests/test_assess_partial_trust.py` 존재 |
| — | `validate_lines` | Harness | STEP3 — 시그니처·import만, RED 미착수 |
| Export | — | 완료 | `src/`·`tests/` **미변경** |

---

## 4. 다음 단계

1. STEP2 §1 주제 한 문장을 Goal과 동일 톤(풀이 성공 → 신뢰 판정)으로 맞출지 결정.
2. `assess_partial_trust` ↔ `validate_lines` handoff·Rule ID 네임스페이스를 워크북 또는 SSOT에 명시.
3. `validate_lines` TDD RED 착수 (`/tdd-red`) — STEP3 Harness 기준.

---

## 관련 문서

| 문서 | 설명 |
|------|------|
| [MagicSquare_XX_STEP2_Workbook.md](./MagicSquare_XX_STEP2_Workbook.md) | 세션 3 워크북 (R-G-I-O 수정 반영) |
| [MagicSquare_XX_STEP3_ValidateLinesSetup.md](./MagicSquare_XX_STEP3_ValidateLinesSetup.md) | validate_lines Harness·Rule |
| [MagicSquare_XX_MomTest_STEP1.md](./MagicSquare_XX_MomTest_STEP1.md) | Mom Test · 진짜/표면 문제 |
