# review-rules — Rule·계약 리뷰

코드 수정 금지. `.cursorrules` 와 코드/테스트 계약 위반만 표로 리뷰.

## 체크 항목

- R1: original `≠0` 칸 → working 동일
- R2: original `0` 칸만 변경 허용
- R3: working 값 `0` 또는 `1~16`
- R4: 위반 시 `contaminated` + `violations` 전수 기록
- Output: `status`, `can_verify`, `violations[]` 형식
- TDD 금지 (assert 완화·skip)
- 표면 솔루션 혼입 (Cell state, 백트래킹, UI)

## 보고 형식

| 우선순위 | 위반 | 파일·위치 | 수정 제안 |
|----------|------|-----------|-----------|
