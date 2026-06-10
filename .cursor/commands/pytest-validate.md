# pytest — assess_partial_trust Test Loop

## 절차

1. `python -m pytest tests/test_assess_partial_trust.py -v` 실행
2. PASS/FAIL 표로 요약
3. FAIL 시: 테스트명 · assert · Rule ID(R1~R4) 1줄씩

## 전체 테스트

```bash
python -m pytest tests/ -v
```

## Test Loop 판정

| 단계 | 기대 pytest | Mom Test 연결 |
|------|-------------|---------------|
| RED | FAIL | 오염·신뢰 상실 **재현** |
| GREEN | PASS | 주어진 칸 보존 → **trusted** |
| REFACTOR | PASS 유지 | 계약(R1~R4) 불변 |

## 보고 형식

| 테스트 | 결과 | Rule | 비고 |
|--------|------|------|------|
| test_... | PASS/FAIL | R1 | ... |
