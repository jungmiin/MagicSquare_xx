# Export — 보고서·프롬프트 저장

현재 세션 작업을 `report/` 보고서와 `prompts/` 프롬프트 파일로보낸다.

## 필수 선언 (응답 첫 줄)
Phase: export | Scope: report/ + prompts/

## 파일 번호 규칙

`report/` · `prompts/` 에 있는 기존 파일명에서 **숫자 접두/접미**를 스캔해 최대값을 구하고 **+1** 한다.

### report/ (현재 양식)
| 파일 | 번호 |
|------|------|
| `MagicSquare_XX_MomTest_STEP1.md` | 1 |
| `MagicSquare_XX_STEP2_Workbook.md` | 2 |
| `MagicSquare_XX_MomTest_Simulation.md` | (번호 없음 — STEP 계열과 별도) |

- **STEP 계열** 최대값: **N** → 신규 보고서: **`STEPN+1`**
- 신규 파일명: `report/MagicSquare_XX_STEP{N}_<주제슬러그>.md`
  - 예: `report/MagicSquare_XX_STEP3_Harness.md`

### prompts/ (현재 양식)
| 파일 | 번호 |
|------|------|
| `MagicSquare_XX_Session3_Workbook.prompt.md` | 3 |
| `MagicSquare_XX_MomTest_Questions10.prompt.md` | 10 |

- **STEP 계열과 동일 N**을 쓴다 (보고서·프롬프트 쌍 유지).
- 신규 파일명: `prompts/MagicSquare_XX_STEP{N}_<주제슬러그>.prompt.md`
  - 예: `prompts/MagicSquare_XX_STEP3_Harness.prompt.md`

> **번호 산출 (Export 쌍):** `report/` 파일명의 `STEP(\d+)` 최대값 +1 → 이번 **3**.  
> `prompts/` 에도 **동일 N**을 써서 보고서·프롬프트를 1:1로 맞춘다.  
> (기존 `Session3`, `Questions10` 등 **레거시 명명**은 유지; 신규 Export 부터 `STEP{N}_<슬러그>` 통일.)

## 절차

1. **현재 작업 파악** — 이번 대화·세션에서 한 일, 변경 파일, TDD Phase, API(`validate_lines` 등)를 요약한다.
2. **다음 번호 확정** — 위 규칙으로 `N` 과 `<주제슬러그>` 를 정한다 (슬러그: PascalCase 또는 짧은 영문, 예: `Harness`, `ValidateLinesRED`).
3. **보고서 작성** — `report/MagicSquare_XX_STEP{N}_<주제슬러그>.md` 생성 (기존 파일 덮어쓰기 금지).
4. **프롬프트 Export** — 사용자가 이번 작업에 쓴 **원문 프롬프트**(또는 대화에서 재구성한 동등 문장)를 `prompts/MagicSquare_XX_STEP{N}_<주제슬러그>.prompt.md` 에 저장한다.
5. **상호 링크** — 보고서 헤더에 프롬프트 경로, 프롬프트 헤더에 보고서 경로를 상대 링크로 넣는다.

## 보고서 템플릿

```markdown
# MagicSquare_XX — STEP{N} <주제>

**작성일:** YYYY-MM-DD
**프롬프트:** [../prompts/MagicSquare_XX_STEP{N}_<주제슬러그>.prompt.md](../prompts/...)
**범위:** <한 줄 요약>

---

## 1. 작업 요약
<이번 세션에서 수행한 일>

## 2. 산출물
| 항목 | 경로·내용 |
|------|-----------|
| ... | ... |

## 3. TDD·검증 상태 (해당 시)
| Phase | 상태 | 비고 |
|-------|------|------|
| RED / GREEN / REFACTOR | ... | ... |

## 4. 다음 단계
<후속 작업 1~3줄>
```

## 프롬프트 템플릿

```markdown
# MagicSquare_XX — STEP{N} <주제> 프롬프트

**작성일:** YYYY-MM-DD
**산출물:** [report/MagicSquare_XX_STEP{N}_<주제슬러그>.md](../report/...)

---

## 프롬프트

\`\`\`
<사용자가 이번 작업에 입력한 원문 프롬프트 전체>
\`\`\`

---

## 후속 프롬프트 (저장·정리)

\`\`\`
/export 로 report·prompts 저장
\`\`\`
```

## 보고 형식 (커맨드 실행 후)
- 생성한 보고서 경로
- 생성한 프롬프트 경로
- 사용한 번호 `N` 과 근거 (기존 max → +1)
- 보고서 3줄 요약

## 금지
- 기존 `report/` · `prompts/` 파일 **덮어쓰기**
- 번호 없이 신규 파일 생성
- `src/` · `tests/` 코드 수정 (Export 는 문서만)
- 프롬프트 원문 생략·과도 요약 (Export 는 **재사용 가능한 원문** 보존)
