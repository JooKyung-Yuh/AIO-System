# AM ontology v0.1 — link overlay 재해석 (cohort_2026-07-09_08-44-36_am_v3_2_N5)

> tracked team-review draft. 코드/프롬프트 미변경. annotation overlay만 씌운 결정론 재분류.
> annotation: `am_ontology_v0.1_annotations.json` · 대상 v2 links(card-level, 5빌드): **133**

## 핵심 질문: 새 ontology 적용 시 몇 %가 진짜 direct belief_update로 남는가
### → **keep_direct = 39%** (52/133)

## 범주별 재분류

- **keep_direct**: 52 (39%) — Observation→mechanism 유지 (strengthen/weaken)
- **convert_to_rolls_up**: 17 (13%) — paper_thesis → direct 제거, rolls_up 후보
- **convert_to_qualifier**: 19 (14%) — assumption/scope/limitation → qualifies/depends_on
- **downgrade_to_observation**: 24 (18%) — qualitative_observation → belief layer에서 강등
- **unresolved_or_gap**: 21 (16%) — aggregate_claim 부재 등 → no-link/unresolved

## 세부

- **paper_thesis direct link 제거**: 17개 → rolls_up/reported_as_main_result 후보로
- **qualitative_observation fan-in 이동**: 24개가 belief→관측 (문서 예상 ~24와 대조)
    - node별: attention:7, ttt:16, task:1
- **aggregate_claim gap unresolved**: 21개 (집계 관측인데 갈 곳 없음)

## factor precision 관점 expected improvement
- v2 raw link 중 **~39%만 진짜 belief_update**로 남고, 나머지는:
  thesis-funnel(13%)는 rolls_up으로 격하(관측 직결 아님), 관측-누수(18%)는 belief에서 제거, 조건류(14%)는 qualifier로.
- 즉 새 ontology는 **belief 레이어를 절반가량으로 정제**하고, 남은 direct link의 precision을 높인다(가짜 지지 제거).
- 단 aggregate_claim 신설 전까지 집계 관측은 unresolved로 남음(코드 단계 과제).

## 검증
1. 23개 AM만 참조: 18개 distinct 참조, 전부 annotation 내 = True
2. paper_thesis direct link 0: keep_direct 중 paper_thesis = 0
3. qualitative_observation belief target 제거: downgrade=24 (keep_direct에 qo 0 = True)
4. mechanism direct 유지: keep_direct 전부 mechanism/aggregate = True
5. aggregate_claim gap 별도 집계: 21개