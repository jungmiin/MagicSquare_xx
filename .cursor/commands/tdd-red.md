# TDD RED — 실패 테스트 먼저

`validate_lines` 의 새 동작을 검증하는 실패 테스트를 `tests/` 에만 작성한다.

## 필수 선언 (응답 첫 줄)
Phase: red | Target: validate_lines | Track: logic

## 절차
1. 케이스의 입력 `grid` 와 기대 출력(`status`, `failed_lines`)을 확정한다.
2. `tests/test_validate_lines.py` 에 AAA 구조 테스트 1개를 추가한다.
3. `pytest` 로 FAIL 을 확인한다 (구현이 없으므로 실패가 정상).
4. 통과시키려 하지 않는다. RED 는 실패가 목표다.

### AAA 구조
- **Arrange**: 4×4 `grid` 준비 (빈칸 `0`, 값 `1~16`)
- **Act**: `result = validate_lines(grid)`
- **Assert**: `result["status"]`, `result["failed_lines"]` 기대값과 비교

## pytest
```bash
python -m pytest tests/test_validate_lines.py -v
```

## 보고 형식
- 추가한 테스트 함수명
- 입력 grid 요약 / 기대 `status`·`failed_lines`
- pytest 결과: FAIL (이유 한 줄)
- 변경 파일: `tests/` 만

## 금지
- `src/` 수정
- assert 완화 / skip / xfail
- 한 번에 여러 케이스 (RED 는 한 번에 1개)
