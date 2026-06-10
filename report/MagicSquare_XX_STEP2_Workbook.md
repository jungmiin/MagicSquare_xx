# MagicSquare_XX — STEP2 워크북 (세션 3)

**작성일:** 2026-06-10  
**근거:** [Mom Test STEP1](./MagicSquare_XX_MomTest_STEP1.md)  
**프롬프트:** [../prompts/MagicSquare_XX_Session3_Workbook.prompt.md](../prompts/MagicSquare_XX_Session3_Workbook.prompt.md)  
**범위:** 부분 상태 **신뢰 판정** (`assess_partial_trust`) — TDD RED → GREEN → REFACTOR

---

## Mom Test 결과 (STEP1 요약)

| 항목 | 내용 |
|------|------|
| **페르소나** | 4×4 **부분 마방진**(ECB 패턴, `?` 2칸, 합 34)을 손·코드로 다루는 **학습자** |
| **진짜 문제 (한 문장)** | 부분 마방진을 체계적 절차 없이 검산·추론하다 **어느 시점의 부분 상태까지 믿을 수 있는지 판정하지 못해** 수정이 오염되고, 30분~1시간을 쓴 뒤에도 결과를 재현·신뢰할 수 없어 중단한다. |
| **Mom Test 증거 3줄** | ① “지운 자국, X, `?` 후보, 취소한 숫자가 섞여 **주어진 값과 추론값을 구분 못하는** 상태” ② “계속하면 **검산이 아니라 오염된 기억으로 억지 수정**하는 것 같아서 멈췄다.” ③ “코드에서 **‘부분 상태를 어디까지 유효하다고 볼 것인가’에서 막혔**다.” |

---

## 1) 주제 (한 문장)

> Mom Test 기반 · 솔루션·기능 이름 최소화

**부분 마방진 작업 격자가 주어진 조건을 유지한 채 검증을 이어갈 수 있는지, 아니면 이미 오염되어 더 이상 믿을 수 없는지 판정할 수 있어야 한다.**

---

## 2) R-G-I-O

| | 내용 |
|---|------|
| **Role** | 부분 마방진을 풀며 격자를 수정하는 **학습자** — 그리고 신뢰 경계를 코드로 고정하는 **TDD 개발자** |
| **Goal** | `original`(문제에서 주어진 격자)과 `working`(작업 중 격자)을 비교해, **지금 이 상태에서 검증을 계속해도 되는지** `trusted` / `contaminated` 로 판정한다. |
| **Input** | `original: list[list[int]]` — 빈칸 `0`, 고정값 `1~16` · `working: list[list[int]]` — 학습자가 채운 작업 격자 |
| **Output** | `status`: `"trusted"` \| `"contaminated"` · `can_verify`: bool — `True`일 때만 이후 검증(10선 등) 진행 · `violations`: `[{ "rule_id", "row", "col", "original", "working" }]` |

---

## 3) 성공 기준 3개

| # | 기준 | Mom Test 증거 연결 |
|---|------|-------------------|
| **S1** | `original`에서 주어진 칸(`≠0`)이 `working`에서 바뀌면 `contaminated`이고, 해당 칸이 `violations`에 **R1**으로 기록된다. | 증거 ① — “주어진 값 vs 추론값 구분 불가” → **주어진 칸 변경을 코드가 즉시 잡아낸다** |
| **S2** | `contaminated`이면 `can_verify`는 **항상 `False`** 이다. | 증거 ② — “오염된 기억으로 억지 수정” → **오염 상태에서 검산·검증을 이어가지 못하게 막는다** |
| **S3** | R1~R3을 모두 통과하면 `trusted`, `can_verify=True`, `violations=[]` 이다. | 증거 ③ — “부분 상태를 어디까지 유효하다고 볼 것인가” → **유효 경계가 명시적으로 정의된다** (이후 10선 검증으로 넘어갈 수 있는 출발점) |

---

## 4) 표면 문제 — 이번 프로젝트에서 하지 않을 것

> Mom Test STEP1 §3 · `.cursorrules` 범위 밖 — **승인 없이 추가 금지**

| 표면 문제 (기능·솔루션 욕구) | 왜 이번 세션 제외 |
|------------------------------|------------------|
| Cell `state` 필드, 주어진/추론 **UI** 구분 | 표면 솔루션 — 신뢰 **판정 API**만으로 경계 고정 |
| 백트래킹·리셋 **프로그램/로직** | “백트래킹 지점 명확화” 욕구 — 이번엔 **판정**만 |
| “처음부터 다시” **리셋 기능** | 포기 직전 노트 — **재시작 UX** 아님 |
| 실패 과정 **설명 슬라이드** | 과제 산출물 — 코드 계약과 무관 |
| **코드 검증기 전체** / Solver / PyQt UI / BCE 전체 | 범위 초과 — 세션 3는 `assess_partial_trust` 한 API |
| `validate_lines` (10선·합 34 검증) | 후속 GREEN — `can_verify=True` **이후** 단계 |

---

## 5) 8계층 — 이번 세션에서 만드는 것

> Rule · Command · (Skill) · Test Loop 만 해당. 나머지 계층(Domain UI, Solver, BCE 전체 등)은 세션 3 범위 밖.

### Rule — `.cursorrules` (R1~R4)

| ID | Rule | 위반 조건 |
|----|------|-----------|
| R1 | `original`에서 `≠0`인 칸은 `working`에서 **동일** | 값 불일치 |
| R2 | `original`에서 `0`인 칸만 `working`에서 `0` 또는 `1~16`으로 변경 가능 | (R1과 함께 판정) |
| R3 | `working` 값이 `0` 또는 `1~16` 범위 밖이면 오염 | 범위 위반 |
| R4 | R1·R3 위반 시 → `contaminated`, `can_verify=False`, `violations` **전수** 기록 | 누락 금지 |
| — | R1~R3 모두 통과 → `trusted`, `can_verify=True`, `violations=[]` | |

### Command — `.cursor/commands/`

| Command | 역할 |
|---------|------|
| `/tdd-red` | `tests/`만 — 실패 테스트 1개 추가, pytest **FAIL** 확인 |
| `/pytest-validate` | Test Loop 실행·PASS/FAIL 표 · Rule ID 매핑 |
| `/review-rules` | R1~R4·계약·표면 솔루션 혼입 **리뷰만** (코드 수정 없음) |

**체인:** `/tdd-red` → pytest FAIL → GREEN(최소 구현) → `/pytest-validate` → `/review-rules`

### (Skill) — `.cursor/skills/magic-square-tdd/`

| Skill | 역할 |
|-------|------|
| `magic-square-tdd` | Phase 선언 · C2C · RED 금지사항 · pytest · 완료 보고 형식 |

> 괄호: Cursor Agent가 TDD 절차를 따를 때 **참조**하는 보조 계층. SSOT는 `.cursorrules` + 본 워크북.

### Test Loop — RED → GREEN → REFACTOR

| 단계 | Scope | pytest 기대 | Mom Test 연결 |
|------|-------|-------------|---------------|
| **RED** | `tests/` only | **FAIL** | 오염·신뢰 상실 **재현** (예: 주어진 칸 변경 → contaminated) |
| **GREEN** | `src/` + `tests/` | **PASS** | 주어진 칸 보존 → **trusted** · S1~S3 충족 |
| **REFACTOR** | `src/` `tests/` (파일 ≤3) | **PASS 유지** | R1~R4 계약 불변 |

```bash
python -m pytest tests/test_assess_partial_trust.py -v
python -m pytest tests/ -v
```

---

## 관련 문서

| 문서 | 설명 |
|------|------|
| [MagicSquare_XX_MomTest_STEP1.md](./MagicSquare_XX_MomTest_STEP1.md) | Mom Test · 진짜/표면 문제 · 증거 |
| [MagicSquare_XX_MomTest_Simulation.md](./MagicSquare_XX_MomTest_Simulation.md) | 가상 인터뷰 시뮬레이션 |
| `.cursorrules` | Rule·API·TDD SSOT |
