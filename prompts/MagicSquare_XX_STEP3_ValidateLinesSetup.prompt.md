# MagicSquare_XX — STEP3 validate_lines 세팅 프롬프트

**작성일:** 2026-06-10  
**산출물:** [report/MagicSquare_XX_STEP3_ValidateLinesSetup.md](../report/MagicSquare_XX_STEP3_ValidateLinesSetup.md)

---

## 프롬프트 1 — Harness

```
MagicSquare_XX 세션 3용 최소 Harness만 만들어줘. 본문은 비워.
- pyproject.toml : pytest 만 설정
- src/__init__.py : 빈 파일
- src/validate_lines.py : 함수 시그니처만 (def validate_lines(grid): ...)
- tests/__init__.py : 빈 파일
- tests/test_validate_lines.py : 빈 파일 (import 줄만)
구현·테스트 본문은 아직 쓰지 마. 골격만.
```

## 프롬프트 2 — .cursorrules

```
루트에 .cursorrules 초안을 만들어줘. 40~60줄. 다른 파일은 만들지 마.
도메인: 4×4, 빈칸 0, 1~16, 마법상수 34, 10선(R1~R4·C1~C4·D1·D2)
API: validate_lines(grid) -> {status: pass|fail|incomplete, failed_lines:[...]}
TDD: RED→GREEN→REFACTOR, assert 완화·skip·xfail 금지, RED은 tests/만 수정
AI: 한국어, TDD 시 첫 줄 Phase 선언, git commit은 사용자 요청 시만
```

## 프롬프트 3 — tdd-red 커맨드

```
.cursor/commands/tdd-red.md 를 만들어줘. validate_lines RED 단계 전용.
포함: Phase 선언, AAA 절차, pytest 예시, 보고 형식,
      금지(src/ 수정·assert 완화). 다른 파일은 만들지 마.

# TDD RED — 실패 테스트 먼저

validate_lines 의 새 동작을 검증하는 실패 테스트를 tests/ 에만 작성한다.

## 필수 선언 (응답 첫 줄)
Phase: red | Target: validate_lines | Track: logic

## 절차
1. 케이스의 입력 grid 와 기대 출력(status, failed_lines)을 확정한다.
2. tests/test_validate_lines.py 에 AAA 구조 테스트 1개를 추가한다.
3. pytest 로 FAIL 을 확인한다 (구현이 없으므로 실패가 정상).
4. 통과시키려 하지 않는다. RED 은 실패가 목표다.

## pytest
    pytest tests/test_validate_lines.py -v

## 보고 형식
- 추가한 테스트 함수명
- 입력 grid 요약 / 기대 status·failed_lines
- pytest 결과: FAIL (이유 한 줄)
- 변경 파일: tests/ 만

## 금지
- src/ 수정
- assert 완화 / skip / xfail
- 한 번에 여러 케이스 (RED 은 한 번에 1개)
```

## 프롬프트 4 — export 커맨드

```
.cursor/commands/export.md 를 만들어줘

report 폴더에 현재 작업에 대한 보고서 생성하고, prompt 폴더에 현재 작업에 쓰인 프롬포트도 도 Export 하는 커맨드를 작성할 것
report/ prompt/  에 있는 기존의 *Number* 양식을 확인
새로 생성하는 파일은 그 최대 번호의 +1 해서 생성
```

---

## 후속 프롬프트 (저장·정리)

```
/export
```
