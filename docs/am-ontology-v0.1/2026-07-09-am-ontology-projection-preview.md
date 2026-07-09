# AM ontology v0.1 — projection preview (cohort_2026-07-09_08-44-36_am_v3_2_N5)

> tracked team-review draft. **코드/프롬프트 미변경.** overlay를 새 ontology 그래프로 투영한 결정론 artifact.
> 대상 v2 links: **133** (card-level, 5빌드 vote-repeated). ⚠️ 이 count는 최종 consensus edge가 아니라 multiset — unique (observation,claim) direct **27**, 전체 unique 66. precision은 unique 기준.

## 새 ontology로 투영한 factor graph 구조

- **Observation → Claim(mechanism) direct**: 52  ← 진짜 belief_update (39%)
- **Claim → paper_thesis rolls_up**: 10 mechanism (+ 신규 aggregate_claim 2개)
- **Qualifier → Observation qualifies/depends_on**: 19
- **qualitative_observation 강등**: 24 link, 3 node
- **thesis-direct 제거**: 17 (headline은 reported_as_main_result 후보)
- **unresolved (aggregate_claim 부재)**: 21 → 신규 claim 2개로 해소 제안

소진 검증: direct 52 + qualifier 19 + demoted 24 + thesis-removed 17 + unresolved 21 = **133** (=총 133)

## 강등되는 qualitative_observation 노드

- `MECH_ttt_visualization_shows_model_adapting_ta` (fan-in 16) → ObservationCard(obs_kind=qualitative_observation)
    - TTT visualization shows model adapting to task-spe
- `MECH_attention_maps_reveal_pixel_pixel_reasoni` (fan-in 7) → ObservationCard(obs_kind=qualitative_observation)
    - Attention maps reveal pixel-to-pixel reasoning rel
- `MECH_task_embedding_visualization_suggests_lea` (fan-in 1) → ObservationCard(obs_kind=qualitative_observation)
    - Task embedding visualization suggests learning int

## aggregate_claim GAP — 신규 claim 후보 (21 link 해소)

- **AGG_vision_priors_jointly_yield_gain** — "Vision priors jointly explain the accuracy gain (cumulative ablation)"  (흡수 12 link, rolls_up→thesis)
    - ex: 'The entries Fig. 7(d-f) all benefit from this design.'
    - ex: 'These priors jointly have a gain'
    - ex: 'These vision priors cumulatively yield improvement (a→f)'
- **AGG_canvas_components_jointly_contribute** — "Canvas-based design components jointly contribute to the gain"  (흡수 8 link, rolls_up→thesis)
    - ex: 'the canvas-based designs (c–f) has a gain.'
    - ex: 'the canvas-based designs (c→f) contribute an gain.'

## thesis-direct 제거된 관측의 처리

- 'achieves accuracy' → reported_as_main_result candidate (headline/top-line result)
- 'achieves accuracy' → reported_as_main_result candidate (headline/top-line result)
- 'substantially surpasses the best recurrent methods [53, 27] ' → reported_as_main_result candidate (headline/top-line result)
- 'matching the reported average human performance [31] on the ' → reported_as_main_result candidate (headline/top-line result)
- 'correctly solves these challenging tasks.' → re-route to a specific mechanism (no direct thesis edge)
- 'Single-view inference has a decent pass@1 accuracy' → reported_as_main_result candidate (headline/top-line result)
- 'Our model compares favorably with some of the most powerful ' → re-route to a specific mechanism (no direct thesis edge)
- 'our method substantially outperforms the recur-rent models: ' → reported_as_main_result candidate (headline/top-line result)

## 판정 (preview가 말하는 것)
- 새 ontology 적용 시 최종 factor graph는 **2-level**로 정돈됨: Observation→mechanism(direct 52) → paper_thesis(rolls_up).
- **belief 레이어가 관측-누수/조건/thesis-funnel를 걷어내 절반가량으로 정제** → 남는 direct link가 훨씬 설명가능.
- **aggregate_claim 2개만 신설**하면 21개 unresolved가 해소되고 집계 관측이 제자리를 찾음.
- 이 구조가 납득되면 다음: aggregate_claim을 extract_am/canonicalize에 넣고 link v3/schema migration.

## 성공기준 검증
1. 133 link 5범주 소진: 133==133 → True
2. keep_direct 52만 belief_update: True (52)
3. aggregate gap 대표패턴+신규 claim 제안: 2개 후보, 21 link 커버
4. 코드/프롬프트 변경: 없음 (tracked docs artifact only)