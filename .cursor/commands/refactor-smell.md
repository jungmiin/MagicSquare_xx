# Refactor Smell — 코드 스멜 탐지 (Refine)

ARRR **R단계 (Refine ⑦)**. `src/` · `tests/` · `entity/` 코드를 **읽기만** 하고 **코드 스멜**을 표로 정리한다.  
**수정·commit 금지** — 후속 `/refactor-safe` 에 넘길 후보만 선정한다.

> **Skill:** `magic-square-tdd` Skill이 있으면 자동 따름 (Phase 선언 · Change Budget · pytest · 완료 보고).

## 모드

- **Ask 전용** — 탐지·보고만. 파일 생성·수정·삭제 없음
- **추가 입력 불필요** — `/refactor-smell` 만으로 동작 (대상 범위는 `src/` `entity/` `tests/` 전체)

## 전제 (게이트)

```bash
python -m pytest tests/ -v
```

| 결과 | 동작 |
|------|------|
| **전부 PASS** | 스멜 탐지 진행 |
| **1건이라도 FAIL** | **즉시 중단** — 아래만 응답 후 종료 |

```
pytest 전체 PASS가 아닙니다. /green-minimal 또는 회귀 수정 후 다시 실행하세요.
```

FAIL 목록(Test ID · 파일 · 한 줄 원인)을 보고에 포함한다.

## 필수 선언 (응답 첫 줄)

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
```

| 필드 | 의미 |
|------|------|
| `Scope` | `src/` · `entity/` · `tests/` (읽기·분석만) |
| `Track` | Logic + UI 통합 스캔 — 경계·도메인 모두 |

## 탐지 절차

1. **pytest 게이트** — `python -m pytest tests/ -v` 결과 확인 (실행 또는 최근 채팅·CI 결과)
2. **범위 스캔** — `src/` · `entity/` · `tests/` (`.cursorrules` · ECB 계약 기준)
3. **스멜 분류** — 아래 유형·우선순위로 표 작성
4. **후보 선정** — `/refactor-safe` 에 넘길 항목 **1~3개** (P0 우선)
5. **다음 안내** — P0 **1개**만 골라 `/refactor-safe` 실행 권고

## 스멜 유형 · 우선순위

| 우선순위 | 스멜 | 탐지 기준 (예) |
|----------|------|----------------|
| **P0** | **ECB 위반** | `entity/` → `boundary/`·`control/` import · E001~E005 혼입 · 계층 역참조 |
| **P0** | **Magic Number** | `4`/`34`/`16` 리터럴 — `entity/constants.py` 미사용 |
| **P1** | **Duplicated Code** | 동일 격자 순회·좌표 변환·violations 조립 등 2곳 이상 복제 |
| **P1** | **Long Method** | 한 함수 40줄 초과 또는 분기·책임 3개 이상 |
| **P2** | **Mysterious Name** | `x`, `tmp`, `data`, `result` 만으로 의도 불명 · Rule ID·10선 ID 미사용 |
| **P2** | **Feature Envy** | 타 모듈/격자 데이터를 과도하게 읽고 자기 데이터는 거의 안 씀 |

- 한 항목에 복수 스멜이면 **가장 높은 우선순위**로 표기
- `.cursorrules` 계약 위반( assert 완화·표면 솔루션)은 스멜이 아니라 **P0 별도 행**으로 표기 가능

## Change Budget (후속 `/refactor-safe` 참고)

본 Command는 수정하지 않지만, 후보 제안 시 **한 번에 이 범위를 넘지 않도록** 적는다.

| 항목 | 상한 |
|------|------|
| 파일 | **≤ 3** |
| 클래스 | **≤ 1** |
| 메서드 | **≤ 3** |

후보가 Budget 초과 예상이면 표에 `⚠ Budget 초과` 표시.

## 출력 형식 (필수)

### 1) pytest 게이트

| 항목 | 값 |
|------|-----|
| 명령 | `python -m pytest tests/ -v` |
| 결과 | `N passed` / **중단** |

### 2) 스멜 표

| P | 스멜 | 위치 (파일:줄·심볼) | 요약 | Budget 적합 |
|---|------|---------------------|------|-------------|
| P0 | Magic Number | `entity/locate.py:8` `range(4)` | `GRID_SIZE` 미사용 | ✓ |
| P1 | Duplicated Code | `tests/…` · `entity/…` | 빈칸 순회 중복 | ✓ |
| … | … | … | … | … |

- **위치**: `path:line` + 함수/클래스명
- **요약**: 1문장 — 무엇이 왜 스멜인지
- **Budget 적합**: ✓ / ⚠

### 3) `/refactor-safe` 후보 (1~3개)

| # | 후보 ID | P | 스멜 | 제안 리팩터 (한 줄) | 예상 파일 수 |
|---|---------|---|------|---------------------|--------------|
| 1 | RF-01 | P0 | Magic Number | `range(4)` → `GRID_SIZE` | 1 |
| 2 | RF-02 | P1 | Duplicated Code | 빈칸 순회 헬퍼 추출 | 2 |
| 3 | … | … | … | … | … |

### 4) 다음 안내 (응답 마지막)

```
P0 후보 RF-01 1개를 골라 /refactor-safe 를 실행하세요.
```

P0가 없으면 P1 후보 1개를 권고한다.

완료 한 줄:

```
/refactor-safe 에 넘길 후보 정리 완료
```

## 금지

| 금지 | 이유 |
|------|------|
| **코드 수정** (`src/` `entity/` `tests/`) | Refine 탐지만 — `/refactor-safe` 역할 |
| **git commit·push** | 사용자 요청 시만 |
| pytest FAIL 상태에서 스멜 탐지 계속 | 게이트 위반 |
| 스멜 없이 구조 개편 제안 | 범위 밖 |
| golden 수동 편집·assert 완화 권고 | TDD SSOT 위반 |

## SSOT (읽기 전용)

| 문서 | 용도 |
|------|------|
| `.cursorrules` | API·Rule·TDD·표면 솔루션 |
| `entity/constants.py` | Magic Number 판정 |
| `report/MagicSquare_XX_STEP2_Workbook.md` | 세션 범위 |
| `/green-minimal` · ECB 규칙 | entity 계층 격리 |

## Command 체인

```
… → /green-minimal → /golden-master → /pytest-validate → /refactor-smell → /refactor-safe → /review-rules
                                                              ↑ 본 Command (탐지만)
```

---

## 실행 예시

**모드:** Ask

```
/refactor-smell
```

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
```

pytest 전체 PASS 확인 후 스멜 표 · 후보 1~3개 · P0 1개 선정 안내를 출력한다.
