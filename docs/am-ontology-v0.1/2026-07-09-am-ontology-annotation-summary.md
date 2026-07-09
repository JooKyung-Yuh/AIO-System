# AM ontology v0.1 — annotation summary (cohort_2026-07-09_08-44-36_am_v3_2_N5)

> tracked team-review draft. 코드 미변경. 기준본: `2026-07-09-am-ontology-v0.1.md`

- AM 23개 전부 annotate. fan_in_v2 = 5 v2 빌드의 card-level links를 canonical AM으로 resolve해 합산(=133, unresolved 0). ensemble nodes.links total(141)은 atom-level(각 link를 AM카드 member atoms로 확장)이라 granularity가 다름 — 133<141은 unresolved 제외가 아니라 card-vs-atom 차이..
- resolved links 133, excluded 0 (합 133). type 분포: {'paper_thesis': 1, 'mechanism': 12, 'qualitative_observation': 3, 'assumption': 3, 'scope_condition': 2, 'limitation': 2}

## 타입별

### paper_thesis (1) — link_policy: rolls_up_only
- `MECH_visual_learning_enables_abstraction_inference_w`  fan_in=17  conf=high
    - Visual learning enables abstraction/inference without language.
    - edge=rolls_up, scope=paper_conclusion · 논문 headline 결론. mechanism들이 rolls_up으로 올림. 관측 직결 금지.
    - ❓ headline result 관측은 reported_as_main_result로 예외 처리할지(v0.2)

### aggregate_claim (0) — link_policy: direct_link_allowed
- ⚠️ **0개 = GAP.** 현재 canonical AM에 aggregate_claim 타입이 하나도 없음 = 설계 gap. cumulative ablation(+27.7)/combined priors/ensemble 결과가 붙을 belief 노드가 없어 component mechanism에 오배치됨. extract_am/canonicalize에서 신설 필요(코드 변경은 이후).

### mechanism (12) — link_policy: direct_link_allowed
- `MECH_explicit_2d_positional_modeling_preserves_image`  fan_in=17  conf=high
    - Explicit 2D positional modeling preserves image structure.
    - edge=strengthen_weaken, scope=component_level · 인과: 2D 위치 모델링이 구조 보존.
- `MECH_canvas_patchification_enriches_data_reduces_ove`  fan_in=14  conf=high
    - Canvas patchification enriches data, reduces overfitting, encour
    - edge=strengthen_weaken, scope=component_level · 인과: patchification이 데이터 다양성↑.
- `MECH_canvas_formulation_enables_augmentations_transl`  fan_in=12  conf=high
    - Canvas formulation enables augmentations for translation/scale i
    - edge=strengthen_weaken, scope=component_level · 인과: canvas가 augmentation 가능케 함.
- `MECH_majority_voting_consolidates_predictions_from_d`  fan_in=10  conf=high
    - Majority voting consolidates predictions from different views.
    - edge=strengthen_weaken, scope=component_level · 인과: voting이 예측 통합. Table 2 multi-view의 올바른 target.
- `MECH_visual_common_sense_learned_from_offline`  fan_in=10  conf=high
    - Visual common sense is learned from offline training data.
    - edge=strengthen_weaken, scope=component_level · 인과: offline training이 상식 학습.
- `MECH_model_handles_ambiguity_proposing_multiple_rule`  fan_in=4  conf=medium
    - Model handles ambiguity by proposing multiple rule interpretatio
    - edge=strengthen_weaken, scope=component_level · 인과: 모델이 모호성을 다중 해석으로 처리.
- `MECH_increasing_model_size_improves_accuracy_enablin`  fan_in=3  conf=high
    - Increasing model size improves accuracy by enabling better fitti
    - edge=strengthen_weaken, scope=component_level · 인과: 크기↑→fitting↑.
- `MECH_early_layer_attention_reflects_pattern_core`  fan_in=1  conf=medium
    - Early layer attention reflects pattern core influence.
    - edge=strengthen_weaken, scope=component_level · 인과(층별 특화).
    - ❓ 정성 관측 파생이라 obs-leaky 경계
- `MECH_later_layer_attention_reflects_rule_extending`  fan_in=1  conf=medium
    - Later layer attention reflects rule for extending pixels.
    - edge=strengthen_weaken, scope=component_level · 인과(층별 특화).
    - ❓ obs-leaky 경계
- `MECH_patchification_provides_locality_translation_in`  fan_in=1  conf=high
    - Patchification provides locality and translation invariance indu
    - edge=strengthen_weaken, scope=component_level · 인과: patchification이 locality/invariance 제공.
- `MECH_average_pooling_aggregates_predictions_raw_grid`  fan_in=0  conf=medium
    - Average pooling aggregates predictions for raw grid locations.
    - edge=strengthen_weaken, scope=component_level · 방법-작동원리(집계 방식). 단 method-description 성격도 있음.
    - ❓ mechanism vs precondition(method) 경계
- `MECH_attention_masks_loss_focus_improve_foreground`  fan_in=0  conf=medium
    - Attention masks and loss focus improve foreground attention/accu
    - edge=strengthen_weaken, scope=component_level · 인과(설계→foreground 주의). fan-in 0 = 미검증.
    - ❓ fan-in 0이라 belief로 실재하나

### qualitative_observation (3) — link_policy: no_direct_link
- `MECH_ttt_visualization_shows_model_adapting_task`  fan_in=16  conf=high
    - TTT visualization shows model adapting to task-specific transfor
    - edge=n/a_demoted_to_observation, scope=observation · 'visualization shows...' = 정성 관측(qualitative), 인과 mechanism 아님. belief target에서 강등.
    - ❓ 강등 후 이 관측이 TTT mechanism을 strengthen하는 source로 남는지
- `MECH_attention_maps_reveal_pixel_pixel_reasoning`  fan_in=7  conf=high
    - Attention maps reveal pixel-to-pixel reasoning relationships.
    - edge=n/a_demoted_to_observation, scope=observation · 'attention maps reveal...' = 정성 관측. belief target 아님.
    - ❓ pixel-to-pixel reasoning을 별도 mechanism으로 재추출할지
- `MECH_task_embedding_visualization_suggests_learning_`  fan_in=1  conf=high
    - Task embedding visualization suggests learning inter-task relati
    - edge=n/a_demoted_to_observation, scope=observation · 'visualization suggests...' = 정성 관측.

### assumption (3) — link_policy: qualifier_only
- `ASM_some_arc_tasks_admit_multiple_plausible`  fan_in=9  conf=medium
    - Some ARC tasks admit multiple plausible rules.
    - edge=depends_on, scope=claim · 데이터 전제. 기본 QualifierCard(depends_on). 논문이 명시 test 시에만 Claim.
    - ❓ multi-view/ambiguity 결과가 이걸 '명시적으로 test'하는가? → 그러면 Claim 승격
- `MECH_some_tasks_solvable_from_scratch_tabula`  fan_in=3  conf=medium
    - Some tasks are solvable from scratch (tabula rasa).
    - edge=depends_on, scope=claim · 벤치마크 속성 전제. 기본 QualifierCard.
    - ❓ assumption vs mechanism 경계(현재 MECH로 라벨됨)
- `ASM_multiple_unseen_tasks_cannot_assumed_simultaneou`  fan_in=0  conf=high
    - Multiple unseen tasks cannot be assumed simultaneously.
    - edge=depends_on, scope=claim · scope 전제. 기본 QualifierCard.

### scope_condition (2) — link_policy: qualifier_only
- `ASM_single_pixel_error_invalidates_entire_arc`  fan_in=4  conf=high
    - Single pixel error invalidates entire ARC prediction.
    - edge=qualifies, scope=observation · ARC 채점 방식의 조건(1픽셀 틀리면 전체 오답). belief 아니라 metric/관측을 qualify.
- `ASM_multi_view_inference_cost_negligible_compared`  fan_in=0  conf=high
    - Multi-view inference cost is negligible compared to TTT.
    - edge=qualifies, scope=observation · 실용 조건(추론 비용). belief_update 대상 아님.

### limitation (2) — link_policy: qualifier_only
- `MECH_correct_predictions_exist_views_but_outvoted`  fan_in=3  conf=medium
    - Correct predictions exist in views but are outvoted.
    - edge=qualifies, scope=claim · majority voting의 한계(맞는 view가 밀림). Claim을 qualify.
    - ❓ limitation vs empirical observation 경계
- `ASM_larger_models_beyond_current_regime_lead`  fan_in=0  conf=high
    - Larger models beyond current regime lead to overfitting.
    - edge=qualifies, scope=claim · 경계/한계 조건(현 regime 넘으면 overfit). qualifier.

### precondition (0) — link_policy: qualifier_only
