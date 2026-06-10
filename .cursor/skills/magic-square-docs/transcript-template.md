# Transcript 템플릿 — `Prompting/05.Export-Transcript.md` SSOT

> `prompts/MagicSquare_XX_STEP{NN}_{슬러그}.prompt.md` 생성 시 본 템플릿을 따른다.

```markdown
# MagicSquare_XX — STEP{NN} {주제} Transcript

**작성일:** {YYYY-MM-DD}
**산출물:** [report/MagicSquare_XX_STEP{NN}_{슬러그}.md](../report/MagicSquare_XX_STEP{NN}_{슬러그}.md)

---

_Exported on {YYYY-MM-DD HH:MM TZ}_
_Source {uuid}_

---

## User

{사용자 원문 프롬프트 — 생략·과도 요약 금지. 복수 턴이면 시간순.}

```
{첫 User 메시지 전문}
```

{추가 User 턴 — 있으면}

```
{…}
```

---

## Cursor

{에이전트 응답 요약이 아닌 **재사용 가능한 핵심** — Command 출력·Phase 선언·pytest 한 줄}

### 턴 1

```
{Phase: …}
{핵심 응답·명령 결과}
```

### 턴 N

```
{…}
```

---

## Commands 실행 (해당 시)

| Command | Phase | 결과 |
|---------|-------|------|
| {/red-test-plan} | red | {설계표 4블록} |
| {/red-skeleton} | red | {FAIL 한 줄} |
| {/green-minimal} | green | {PASS 한 줄} |
| {/golden-master} | green | {matched} |
| {/refactor-smell} | refactor | {후보 RF-ID} |
| {/refactor-safe} | refactor | {Budget·PASS} |
| {/export-session} | export | {본 Transcript} |

---

## 후속 프롬프트

```
{다음 세션에 붙여넣을 한 줄 — 예: /green-minimal D-LOC-01}
```
```

## 메타데이터 규칙

| 필드 | 형식 | 필수 |
|------|------|------|
| `_Exported on` | `YYYY-MM-DD HH:MM` + TZ(가능 시) | ✓ |
| `_Source` | 채팅·agent transcript **uuid** (알 수 없으면 `unknown`) | ✓ |

## User / Cursor 작성 원칙

| 구분 | 원칙 |
|------|------|
| **User** | 원문 보존 — 코드·Command·Test ID 포함 |
| **Cursor** | Phase 선언·pytest **실측**·변경 파일만 — 추측 금지 |
| **Commands** | 실제 실행된 Command만 표에 기재 |

## 파일명

- `prompts/MagicSquare_XX_STEP{NN}_{슬러그}.prompt.md`
- Report와 **동일 NN·슬러그** (1:1 쌍)
