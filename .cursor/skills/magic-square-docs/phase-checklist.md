# Phase Checklist — Export 전 검증

`/export-session` · ARRR 1사이클 완료 보고 시 **순서대로** 확인.  
항목 미충족 시 Export **중단**하고 부족 항목만 보고.

## Step A — 입력 수집

- [ ] `git status` 실행·결과 확보
- [ ] `python -m pytest tests/ -v` 실행·결과 확보 (**채팅에 없는 결과 기재 금지**)
- [ ] Phase 선언 첫 줄 확보 (`red` / `green` / `refactor` / `repeat` / `export`)
- [ ] Test ID 목록 확보 (없으면 `—`)
- [ ] 실행된 Command 목록 확보 (`/red-test-plan` …)

## Step B — 번호 NN

- [ ] `report/` 스캔: `MagicSquare_XX_STEP(\d+)_` 최대값 = **R**
- [ ] `prompts/` 스캔: `MagicSquare_XX_STEP(\d+)_` 최대값 = **P**
- [ ] **NN = max(R, P) + 1** 확정·근거 기록
- [ ] `{슬러그}` 확정 (주제·Test ID 기반)
- [ ] 동일 NN·슬러그 파일 **미존재** 확인 (덮어쓰기 금지)

## Step C — Report

- [ ] [report-template.md](report-template.md) 적용
- [ ] §0 세션 스냅샷 — git·pytest **실측값**
- [ ] §2 Phase별 STEP — 이번 Phase 해당 섹션만 상세
- [ ] `report/MagicSquare_XX_STEP{NN}_{슬러그}.md` 생성
- [ ] Transcript 상대 링크 삽입

## Step D — Transcript

- [ ] [transcript-template.md](transcript-template.md) 적용
- [ ] `_Exported on` · `_Source {uuid}` 삽입
- [ ] User 원문 보존
- [ ] Cursor — Phase·pytest·변경 파일 (추측 금지)
- [ ] `prompts/MagicSquare_XX_STEP{NN}_{슬러그}.prompt.md` 생성
- [ ] Report 상대 링크 삽입

## Step E — README

- [ ] `README.md` 존재 시 **문서 표** 1행 추가
- [ ] 없으면 `README.md` 생성 — 문서 인덱스 표만 최소 작성
- [ ] 표 열: `STEP` · `주제` · `Report` · `Transcript` · `Phase` · `날짜`

## Step F — 완료 보고

- [ ] Report 경로 1줄
- [ ] Transcript 경로 1줄
- [ ] NN·슬러그·3줄 요약

## 금지 (체크 실패 = Export 중단)

| 금지 | 이유 |
|------|------|
| git commit·push (묵시적) | 사용자 요청 시만 |
| `UPDATE_GOLDEN=1` (묵시적) | golden 의도적 갱신만 |
| pytest 결과 **추측·기억** 기재 | SSOT 위반 |
| `report/`·`prompts/` 덮어쓰기 | 번호 무결성 |
| `src/`·`tests/` 코드 수정 | Export는 문서만 |

## Phase 빠른 매핑

| Phase | Report §2 필수 | Transcript Commands |
|-------|----------------|---------------------|
| `red` | RED | red-test-plan, red-skeleton |
| `green` | GREEN (+ RED 요약) | green-minimal, golden-master |
| `refactor` | REFACTOR | refactor-smell, refactor-safe |
| `repeat` | repeat + RED | 다음 RED 묶음 |
| `export` | 전체 요약 | export-session |
