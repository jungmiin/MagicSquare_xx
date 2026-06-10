# Report 템플릿 — `Report/05.REPORT.md` SSOT

> `report/MagicSquare_XX_STEP{NN}_{슬러그}.md` 생성 시 본 템플릿을 따른다.  
> `{NN}` · `{슬러그}` · 아래 `{…}` 는 Step A 수집값으로 치환.

```markdown
# MagicSquare_XX — STEP{NN} {주제}

**작성일:** {YYYY-MM-DD}
**세션:** {NN}
**Phase:** {red | green | refactor | repeat}
**Transcript:** [../prompts/MagicSquare_XX_STEP{NN}_{슬러그}.prompt.md](../prompts/MagicSquare_XX_STEP{NN}_{슬러그}.prompt.md)
**범위:** {한 줄 요약}

---

## 0. 세션 스냅샷 (Step A)

| 항목 | 값 |
|------|-----|
| **git status** | {실행 결과 요약 — untracked/modified 파일} |
| **pytest** | `{실행 명령}` → **{N passed, M failed}** |
| **Phase** | `{Phase 선언 첫 줄}` |
| **Test ID** | `{D-LOC-01, …}` |
| **Command** | `{/red-skeleton, /green-minimal, …}` |
| **ARRR 사이클** | {Ask / Respond / Refine / Repeat 중 해당} |

> pytest·git 결과는 **이번 세션에서 실제 실행·확인한 값만** 기재.

---

## 1. ARRR 1사이클 요약

| ARRR | TDD | 이번 세션 |
|------|-----|-----------|
| Ask | RED | {③ 설계 / ④ 스켈레톤 — 해당 시} |
| Respond | GREEN | {최소 구현 / golden — 해당 시} |
| Refine | REFACTOR | {smell / safe — 해당 시} |
| Repeat | — | {다음 RED 묶음·재실행 — 해당 시} |

---

## 2. Phase별 STEP

### RED (해당 시)

| 항목 | 내용 |
|------|------|
| Test ID | {ID} |
| 설계 | {C2C·Given/When/Then 한 줄} |
| 스켈레톤 | `{tests/…::test_…}` |
| pytest | **FAIL** — `{실패 메시지 한 줄}` |

### GREEN (해당 시)

| 항목 | 내용 |
|------|------|
| Test ID | {ID} |
| 구현 | `{entity/… · src/…}` |
| pytest | **PASS** — `{N passed}` |
| golden | {matched yes/no/n/a} |

### REFACTOR (해당 시)

| 항목 | 내용 |
|------|------|
| 후보 RF-ID | {RF-01} |
| 스멜 | {Magic Number · …} |
| Budget | 파일 {n} · 메서드 {n} |
| pytest | **PASS** — 전체 `{N passed}` |
| golden | {matched / n/a} |

### repeat (해당 시)

| 항목 | 내용 |
|------|------|
| 사유 | {회귀·재RED·다음 묶음} |
| 다음 Test ID | {ID} |
| Command | {/red-test-plan …} |

---

## 3. 산출물

| 항목 | 경로 |
|------|------|
| 보고서 | `report/MagicSquare_XX_STEP{NN}_{슬러그}.md` |
| Transcript | `prompts/MagicSquare_XX_STEP{NN}_{슬러그}.prompt.md` |
| 코드·테스트 | {변경 파일 목록} |

---

## 4. 다음 단계

1. {후속 1}
2. {후속 2}
```

## 파일명 규칙

- `report/MagicSquare_XX_STEP{NN}_{슬러그}.md`
- `{슬러그}`: PascalCase 또는 짧은 영문 (`TddHarness`, `DLoc01Green`)
- 기존 파일 **덮어쓰기 금지**

## Phase → 섹션 2 포함 여부

| Phase | RED | GREEN | REFACTOR | repeat |
|-------|-----|-------|----------|--------|
| `red` | ✓ | — | — | — |
| `green` | (이전 묶음 요약) | ✓ | — | — |
| `refactor` | — | — | ✓ | — |
| `repeat` | ✓ | — | — | ✓ |
