# RED Test Plan — C2C 설계표·테스트 플랜 (Ask)

ARRR **A단계 (Ask = RED ③)**. 이번 RED 묶음에 대한 **C2C 설계표**와 **테스트 플랜**만 작성한다.  
코드·테스트 파일은 만들지 않는다 — 다음 단계 `/red-skeleton` 에 넘긴다.

## SSOT (읽기 전용)

| 우선 | 문서 | 용도 |
|------|------|------|
| 1 | `docs/PRD.md` | FR ID · 요구사항 · Test ID 체계 |
| 2 | `.cursorrules` | Rule·API·TDD 계약 |
| 3 | `report/MagicSquare_XX_STEP2_Workbook.md` | 세션 주제 · R-G-I-O · 성공 기준 |
| 4 | 현재 채팅 | 진행 중 RED 묶음 · 이미 확정된 Test ID |

`docs/PRD.md` 가 없으면 `.cursorrules` + 워크북 + 채팅 맥락으로 FR·Test ID를 추론하고, 출처를 표에 명시한다.

## 모드

- **Ask 전용** — 설계·플랜 문서만 출력
- **추가 입력 불필요** — `/red-test-plan` 만으로 동작
- 세션 주제·Test ID·FR ID는 위 SSOT와 **현재 채팅**에서 자동 추출

## 필수 선언 (응답 첫 줄)

```
Phase: red | Layer: entity | Track: Logic
```

| 필드 | 값 | 의미 |
|------|-----|------|
| `Layer` | `entity` \| `boundary` | `entity` = 도메인·로직 단위 · `boundary` = UI·입출력 경계 |
| `Track` | `Logic` \| `UI` | Logic ↔ `entity` · UI ↔ `boundary` (기본 쌍) |

**Track A (boundary / UI):** 본 Command와 출력 4블록 구조는 동일하다. `Layer: boundary` · `Track: UI` 로 선언만 바꾸면 재사용한다.

## 자동 추출 절차

1. **세션 주제** — 워크북 §1 한 문장 또는 PRD 범위 문단
2. **이번 RED 묶음** — 채팅에서 마지막으로 언급·합의된 Test ID 1~N개 (없으면 PRD FR 1건 → Test ID 1개)
3. **대상 API** — `.cursorrules` 핵심 API (`assess_partial_trust`, `validate_lines` 등)
4. **Rule 매핑** — `.cursorrules` R1~R4 또는 PRD FR → 위반 조건
5. **Layer·Track** — API·테스트 대상이 도메인 함수면 `entity`/`Logic`, 위젯·입력 경계면 `boundary`/`UI`

## C2C (Rule 1~3)

| Rule | 내용 |
|------|------|
| **Rule 1** | **판단 포함** FR·성공 기준만 To-Do로 변환 (순수 데이터·상수 제외) |
| **Rule 2** | **1 To-Do : 1 Test Case** — RED 묶음에 테스트 함수 1개 |
| **Rule 3** | **RED 먼저** — 플랜 단계에서는 구현·통과 가정 금지; Expected RED Failure 명시 |

## 출력 4블록 (표 형식 필수)

응답 본문은 아래 **4개 섹션을 순서대로** 표로 작성한다.

---

### 블록 1 — C2C 설계표

| FR (PRD 인용) | To-Do (판단 1문장) | Test ID | Given | When | Then |
|---------------|-------------------|---------|-------|------|------|
| `FR-…` 원문 또는 요약 + 출처 | 이번 RED에서 검증할 행동 1개 | `D-…-01` / `U-…-01` | 초기 격자·상태 | 호출·입력 | 기대 출력·상태 |

- FR 열: `docs/PRD.md` § 인용; 없으면 워크북 S1~S3 또는 `.cursorrules` Rule ID
- Test ID·Given/When/Then: **이번 RED 묶음 1행** (묶음에 ID가 여러 개면 블록 2에서 행 분리)

---

### 블록 2 — 테스트 케이스 표 (Track Logic 시 “Track B 표”)

Logic Track (`entity`) 기본 제목: **Track B 표**  
UI Track (`boundary`) 동일 열 구조 — 제목만 **Track A 표** 로 바꿔도 된다.

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---------|-----------|--------------|-----------|----------------------|
| … | `assess_partial_trust` 등 | Given 요약 → Then 요약 | R1~R4·`can_verify` 등 불변 | `ImportError` / `AttributeError` / assertion 실패 한 줄 |

- **Invariant**: GREEN 후에도 깨지면 안 되는 계약 (Rule ID 명시)
- **Expected RED Failure**: `src/` 미구현·스텁 시 pytest가 낼 **구체적** 실패 유형

---

### 블록 3 — 테스트 플랜

| 항목 | 내용 |
|------|------|
| **파일 경로** | `tests/test_<api>.py` (생성 예정 경로만 기재) |
| **함수명** | `test_<test_id_slug>_<행위>` — pytest 규칙·Test ID와 1:1 |
| **conftest 픽스처** | `tests/conftest.py` 에서 쓸 픽스처명·역할 (없으면 `—`) |
| **pytest 명령** | `python -m pytest tests/test_<api>.py::<함수명> -v` |
| **RED 묶음 범위** | Test ID 목록 · 대응 FR · 1커밋 = 이 묶음 1개 |

AAA 구조 메모 (플랜에 포함):

- **Arrange**: `original` / `working` 또는 `grid` 등 SSOT 타입
- **Act**: 대상 함수 1회 호출
- **Assert**: `status`, `can_verify`, `violations` 또는 `failed_lines` 등 계약 필드

---

### 블록 4 — ECB·Mock 점검

| 점검 | Logic Track (`entity`) | UI Track (`boundary`) |
|------|------------------------|------------------------|
| Domain Mock | **금지** — 도메인 규칙은 실제 API·실제 격자로 검증 | 경계만 stub; 도메인 판정 로직 mock 금지 |
| ECB emit | **E001~E005 이벤트 emit 금지** (RED·플랜 단계) | 동일 |
| 표면 솔루션 | Cell `state`, 백트래킹, Solver, PyQt UI 혼입 없음 | UI Track도 도메인 규칙을 UI에 중복 구현하지 않음 |
| SSOT 일탈 | `assess_partial_trust` / `validate_lines` 계약 밖 필드 추가 없음 | — |

점검 결과 열: `OK` / `주의: …` 한 줄씩.

---

## 완료 한 줄 (응답 마지막)

```
/red-skeleton 으로 넘길 준비됐다
```

## 금지

| 금지 | 이유 |
|------|------|
| `src/` 수정 | GREEN 선행 |
| `tests/` · `src/` **파일 생성·삭제** | `/red-skeleton` 역할 |
| GREEN / REFACTOR 단계 진행 | Ask 범위 밖 |
| `pytest.skip` / `xfail` / assert 완화 | TDD SSOT |
| 기대값 변경으로 통과 가정 | RED 무효 |
| Domain Mock (Logic Track) | 도메인 계약 우회 |
| E001~E005 emit | ECB는 후속 단계 |

## Command 체인 위치

```
/red-test-plan  →  /red-skeleton  →  pytest FAIL  →  GREEN  →  /pytest-validate  →  /review-rules
       ↑ Ask (본 Command)              ↑ RED 코드 작성
```

---

## 실행 예시

### Track Logic (entity)

```
/red-test-plan
```

```
Phase: red | Layer: entity | Track: Logic
이번 RED 묶음: D-LOC-01 (FR-LOC-01)
```

### Track UI (boundary)

```
/red-test-plan
```

```
Phase: red | Layer: boundary | Track: UI
이번 RED 묶음: U-IN-01, U-IN-02
```

(Layer·Track만 바꾸면 블록 1~4 구조·금지사항은 동일하다.)
