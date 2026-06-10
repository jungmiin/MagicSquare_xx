# Refactor Safe — 선택 스멜 1건 Safe Refactor

`/refactor-smell` 표에서 **선택한 스멜 1개**만 Safe Refactor 한다.  
동작·계약·golden 은 유지하고 **구조만** 개선한다.

> **Skill:** `magic-square-tdd` Skill이 있으면 자동 따름 (Phase 선언 · Change Budget · pytest · 완료 보고).

## 모드

- **Agent** — 코드 수정 허용. **스멜 1건** · Budget 이내만
- 선행: `/refactor-smell` 후보 표 · RF-ID · P · 위치 · 제안 리팩터

선행 표가 없으면 채팅 인자(스멜·대상·Budget)로 1건을 확정한다.

## 필수 선언 (응답 첫 줄)

```
Phase: refactor | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| `Layer` | `entity` \| `boundary` | 스멜 위치·Track 과 동일 |
| `Track` | `Logic` \| `UI` | 스멜 표와 동일 |

**Track A (boundary / UI):** `Layer: boundary` · `Track: UI` 로 선언만 바꾸면 재사용.

## 선행 조건 (게이트)

```bash
python -m pytest tests/ -v
```

| 결과 | 동작 |
|------|------|
| **전부 PASS** | 리팩터 진행 |
| **FAIL** | **중단** — 수정·리팩터 금지 |

```
pytest 전체 PASS가 아닙니다. 회귀 수정 후 /refactor-safe 를 다시 실행하세요.
```

## 입력 (채팅·인자)

| 항목 | 예 |
|------|-----|
| **후보 ID** | `RF-02` (`/refactor-smell` 표) |
| **스멜** | `Duplicated Code` |
| **대상** | `src/validate_lines.py` · `entity/locate.py` |
| **제안** | 10선 합 계산 4곳 → `_line_sum` extract |
| **Budget** | 파일 ≤3 · 클래스 ≤1 · 메서드 ≤3 |

**한 번에 스멜 1개만.** 복수 후보는 `/refactor-safe` 를 반복 실행한다.

## Safe Refactor 원칙

| 원칙 | 내용 |
|------|------|
| **입출력 불변** | 공개 API 시그니처·반환 구조·dict 키(`status`, `violations` 등) 변경 금지 |
| **예외 불변** | 기존에 없던 `raise` 추가·예외 타입 변경 금지 |
| **int[6] 1-index** | 좌표·golden 포맷(공백 구분 1-based) 변경 금지 |
| **ECB** | E001~E005 `raise` / `return` / emit **금지** |
| **계층** | `entity/` → `boundary/`·`control/` import 추가 금지 |
| **상수** | `entity/constants.py` SSOT 유지 — 새 매직넘버 금지 |
| **기능·버그** | 동작 추가·버그 수정 **금지** → 별도 `/green-minimal` |
| **테스트** | assert 완화·skip·xfail·golden 수동 편집 금지 |

허용: Extract Method/Function · Rename(의도 명확화) · 상수 import 치환 · 중복 제거(동일 semantics)

## Change Budget (필수 준수)

| 항목 | 상한 |
|------|------|
| 파일 | **≤ 3** |
| 클래스 | **≤ 1** |
| 메서드 (추출·이동 포함) | **≤ 3** |

Budget 초과 예상이면 **리팩터 전** 중단하고 `/refactor-smell` 에서 후보를 쪼갤 것을 안내한다.

## 절차

1. **게이트** — `python -m pytest tests/ -v` → 전부 PASS 확인
2. **스멜 1건 확정** — smell 표 RF-ID · 위치 · 제안 리팩터
3. **최소 diff** — Budget 이내로 Extract/Rename/상수 치환만
4. **pytest** — `python -m pytest tests/ -v` → 전부 PASS
5. **golden** — `UPDATE_GOLDEN` **없이** approval 테스트 matched 확인
6. **완료 보고** — 변경 요약 · pytest · golden matched

### golden 검증

approval 테스트가 있으면 반드시 실행한다 (`tests/_approval.py` · `tests/golden/*.approved.txt`).

```bash
python -m pytest tests/ -v
```

`UPDATE_GOLDEN` 을 **설정하지 않은** 상태에서 golden 비교가 통과해야 한다.

#### golden diff 발생 시

| 유형 | 조치 |
|------|------|
| **비의도** (리팩터가 출력 변경) | **즉시 롤백** — semantics 변경 = Safe Refactor 실패 |
| **의도적** (포맷 SSOT 정렬 등, 매우 드묾) | ISS(이슈·보고)에 **사유·Test ID·before/after** 문서화 → `UPDATE_GOLDEN=1` 로 **한 번만** 갱신 → matched 재확인 |

```bash
# PowerShell — 의도적 갱신 시만
$env:UPDATE_GOLDEN="1"; python -m pytest tests/entity/test_<id>.py -v; Remove-Item Env:UPDATE_GOLDEN
```

golden **수동 편집**으로 matched 우회 **금지**.

## 완료 보고 (응답 마지막)

| 항목 | 내용 |
|------|------|
| **후보 ID · 스멜** | `RF-02` · Duplicated Code |
| **변경 요약** | 추출 함수명 · 영향 파일 1~3줄 |
| **Budget** | 파일 N · 클래스 N · 메서드 N |
| **pytest** | `python -m pytest tests/ -v` → `N passed` |
| **golden matched** | `yes` / `n/a` (approval 없음) / `ISS+UPDATE` (의도적 갱신 시) |

완료 한 줄:

```
Safe Refactor 완료 — /review-rules 또는 다음 스멜 후보
```

### git

- commit·push 는 사용자 **명시 요청 시만**
- 권장 메시지: `refactor: RF-02 extract line sum helper`

## 금지

| 금지 | 이유 |
|------|------|
| 스멜 **2개 이상** 동시 해결 | 1실행 = 1스멜 |
| Budget 초과 | Change Budget SSOT |
| 기능 추가·버그 수정 | GREEN 범위 |
| 입출력·예외·int[6]·golden 포맷 변경 | Safe Refactor 원칙 |
| E001~E005 emit | ECB |
| assert 완화 · golden 수동 편집 | TDD·Approval 우회 |
| pytest FAIL 상태에서 계속 | 게이트 위반 |

## Command 체인

```
… → /refactor-smell → /refactor-safe → /review-rules
                            ↑ 본 Command (수정 1스멜)
```

---

## 실행 예시

**모드:** Agent

```
/refactor-safe
```

```
Phase: refactor | Layer: entity | Track: Logic
스멜: Duplicated Code — 10선 합 계산 4곳 반복
대상: entity/validation.py
Budget: 파일 2개, 메서드 2개 extract
```

또는 smell 표 RF-ID 지정:

```
/refactor-safe RF-02
```

게이트 PASS → Budget 내 Extract → `pytest tests/ -v` PASS → golden matched → 보고.
