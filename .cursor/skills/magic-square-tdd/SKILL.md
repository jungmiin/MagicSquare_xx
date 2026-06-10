---
name: magic-square-tdd
description: >-
  MagicSquare_XX TDD 절차(C2C, RED/GREEN/REFACTOR, assess_partial_trust, pytest).
  Use when Phase is red/green/refactor, partial trust boundary, or pytest TDD.
disable-model-invocation: true
---

# MagicSquare_XX TDD

SSOT: `.cursorrules`, `report/MagicSquare_XX_STEP2_Workbook.md`

## Phase 선언 (응답 첫 줄)

```
Phase: red | API: assess_partial_trust | Scope: tests/ only
Phase: green | API: assess_partial_trust | Scope: src/ + tests/
Phase: refactor | API: assess_partial_trust | Scope: src/ tests/
```

## C2C

1. **판단 포함** 항목만 To-Do 변환
2. **1 To-Do : 1 Test Case**
3. **RED 먼저** — FAIL 확인 후 GREEN

## RED 절대 금지

- `src/` 구현 (GREEN 선행)
- skip / xfail / assert 완화
- 표면 솔루션 (Cell state UI, 백트래킹, Solver)

## GREEN

- **1커밋 = RED 1묶음**
- Rule R1~R4 계약 불변
- `can_verify`는 `status=="trusted"`일 때만 `True`

## Command 체인

```
/tdd-red → pytest FAIL 확인 → GREEN(최소 구현) → /pytest-validate → /review-rules
```

## pytest

```bash
python -m pytest tests/test_assess_partial_trust.py -v
python -m pytest tests/ -v
```

## 완료 보고

- Phase · Test ID · pytest PASS/FAIL 한 줄
- 변경 파일 목록
- git commit은 사용자 요청 시만
