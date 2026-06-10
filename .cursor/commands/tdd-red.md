# TDD RED — assess_partial_trust 실패 테스트

`assess_partial_trust` 의 새 동작을 검증하는 실패 테스트를 `tests/` 에만 작성한다.

## 필수 선언 (응답 첫 줄)
Phase: red | API: assess_partial_trust | Scope: tests/ only

## 절차
1. `original` / `working` 격자와 기대 `status`, `can_verify`, `violations` 를 확정한다.
2. `tests/test_assess_partial_trust.py` 에 AAA 구조 테스트 1개를 추가한다.
3. `pytest` 로 FAIL 을 확인한다 (미구현·NotImplementedError 가 정상).
4. 통과시키려 하지 않는다. RED 는 실패가 목표다.

## pytest
```bash
python -m pytest tests/test_assess_partial_trust.py -v
```

## 보고 형식
- 추가한 테스트 함수명
- original / working 요약 · 기대 status·can_verify
- pytest 결과: FAIL (이유 한 줄)
- 변경 파일: tests/ 만

## 금지
- src/ 수정
- assert 완화 / skip / xfail
- 한 번에 여러 케이스 (RED 는 1개씩)
