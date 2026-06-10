---
name: magic-square-docs
description: >-
  MagicSquare_XX session Report Export and Transcript archiving. Use for Report
  Export, Transcript, /export-session, Phase repeat, ARRR one-cycle completion
  reports, or session N documentation (세션 N 보고서).
disable-model-invocation: true
---

# MagicSquare_XX Docs — Report · Transcript Export

세션 산출물을 `report/` · `prompts/` 에 번호 체계로 저장한다.  
형식 SSOT: **`Report/05.REPORT.md`** · **`Prompting/05.Export-Transcript.md`** (본 Skill 템플릿으로 구현).

> **Command 연동:** Export 요청 시 **magic-square-docs Skill 로드 후 checklist 수행**.

모든 Export 응답은 **한국어**. 문서만 수정 — `src/` · `tests/` 코드 변경 금지.

## SSOT

| # | 문서 | 용도 |
|---|------|------|
| 1 | [report-template.md](report-template.md) | Report 본문 (`Report/05.REPORT.md`) |
| 2 | [transcript-template.md](transcript-template.md) | Transcript (`Prompting/05.Export-Transcript.md`) |
| 3 | [phase-checklist.md](phase-checklist.md) | Export 전 검증 |
| 4 | `.cursor/commands/export.md` | 레거시 `/export` (본 Skill과 동일 NN 규칙) |

## 트리거

- `/export-session` · `/export`
- **Report Export** · **Transcript** 요청
- `Phase: repeat` · **ARRR 1사이클 완료 보고**
- **세션 N 보고서** 작성

## 필수 선언 (응답 첫 줄)

```
Phase: export | Scope: report/ + prompts/
```

ARRR 사이클 보고 시 추가로 이번 세션 Phase:

```
Phase: export | Scope: report/ + prompts/ | Session Phase: green
```

---

## 워크플로 (Step A → F)

[phase-checklist.md](phase-checklist.md) 를 열고 항목을 순서대로 수행한다.

### Step A — 입력 수집

**실행·확인 후** 보고서에만 기재 (추측 금지).

```bash
git status
python -m pytest tests/ -v
```

| 수집 항목 | 출처 |
|-----------|------|
| **git status** | 위 명령 출력 |
| **pytest** | `N passed, M failed` + 명령 문자열 |
| **Phase** | 채팅 첫 줄 `Phase: red \| …` |
| **Test ID** | `D-LOC-01` 등 |
| **Command** | `/red-skeleton` 등 실행 목록 |

### Step B — NN = max(Report, Prompting) + 1

1. `report/MagicSquare_XX_STEP(\d+)_*.md` → 최대 **R**
2. `prompts/MagicSquare_XX_STEP(\d+)_*.prompt.md` → 최대 **P**
3. **NN = max(R, P) + 1**
4. `{슬러그}` 결정 (Test ID·주제 기반 PascalCase)

```
report/MagicSquare_XX_STEP{NN}_{슬러그}.md
prompts/MagicSquare_XX_STEP{NN}_{슬러그}.prompt.md
```

- 레거시 `Session3` · `Questions10` 은 유지 — **STEP 계열**만 NN 산출
- 기존 파일 **덮어쓰기 금지**

### Step C — Report

[report-template.md](report-template.md) 로 작성.

- §0 세션 스냅샷 (Step A)
- §2 **Phase별 STEP**: `RED` / `GREEN` / `REFACTOR` / `repeat` — 이번 Phase 해당분 상세
- Transcript 상대 링크

### Step D — Transcript

[transcript-template.md](transcript-template.md) 로 작성.

- **User** / **Cursor** 섹션
- `_Exported on {YYYY-MM-DD HH:MM}_`
- `_Source {uuid}_` (agent transcript id; 없으면 `unknown`)
- User 원문 보존 · Cursor는 Phase·pytest·변경 파일
- Report 상대 링크

### Step E — README 문서 표 갱신

`README.md` 가 없으면 최소 인덱스만 생성.

```markdown
## 문서 인덱스

| STEP | 주제 | Report | Transcript | Phase | 날짜 |
|------|------|--------|------------|-------|------|
| {NN} | {주제} | [report/…](report/…) | [prompts/…](prompts/…) | {phase} | {YYYY-MM-DD} |
```

기존 표가 있으면 **1행 추가**만.

### Step F — 완료 보고

응답 마지막에 **경로 2개**:

```
Report:   report/MagicSquare_XX_STEP{NN}_{슬러그}.md
Transcript: prompts/MagicSquare_XX_STEP{NN}_{슬러그}.prompt.md
```

| 항목 | 내용 |
|------|------|
| NN | `{max→+1}` 근거 |
| 요약 | 3줄 |

완료 한 줄:

```
Export 완료 — STEP{NN} Report·Transcript 저장됨
```

---

## ARRR 1사이클 완료 보고

RED → GREEN → (golden) → REFACTOR 또는 **repeat** 한 바퀴 후 Export 시:

| ARRR | Report §2 | 기록 |
|------|-----------|------|
| Ask (RED) | RED | 설계·스켈레톤·FAIL |
| Respond (GREEN) | GREEN | 구현·PASS·golden |
| Refine (REFACTOR) | REFACTOR | RF-ID·Budget·PASS |
| Repeat | repeat | 다음 묶음·재게이트 |

`Phase: repeat` — 회귀·재RED 시 §2 **repeat** + RED 섹션 작성.

---

## `/export-session` 연동

`.cursor/commands/export-session.md` (또는 `/export`) 실행 시:

1. **magic-square-docs** Skill 로드
2. [phase-checklist.md](phase-checklist.md) 전항목 수행
3. Step A~F 순서 고정
4. 금지 항목 위반 시 중단

레거시 `/export` 는 동일 NN·쌍 규칙 — Transcript·`_Exported on`·`_Source` 는 본 Skill이 **추가 SSOT**.

---

## 금지

| 금지 | 이유 |
|------|------|
| **git commit·push** (묵시적) | 사용자 요청 시만 |
| **`UPDATE_GOLDEN=1`** (묵시적) | golden 의도적 갱신만 |
| 채팅·실행 **없는 pytest** 결과 기재 | SSOT 위반 |
| `report/`·`prompts/` **덮어쓰기** | 번호 무결성 |
| `src/`·`tests/` 수정 | Export는 문서만 |
| User 프롬프트 과도 요약 | Transcript 재사용성 |

---

## 예시 — 완료 보고

```
Phase: export | Scope: report/ + prompts/ | Session Phase: green

Report:   report/MagicSquare_XX_STEP5_DLoc01Green.md
Transcript: prompts/MagicSquare_XX_STEP5_DLoc01Green.prompt.md

NN: max(STEP4, STEP4)+1 = 5
요약:
- D-LOC-01 GREEN — find_blank_coords 1-index
- pytest: 4 passed (실행: python -m pytest tests/ -v)
- git: modified entity/locate.py, tests/entity/test_d_loc_01.py

Export 완료 — STEP5 Report·Transcript 저장됨
```

---

## 관련 Skill

- [magic-square-tdd](../magic-square-tdd/SKILL.md) — Phase 선언 · pytest · 완료 보고 형식
