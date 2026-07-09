# Direct-edge precision audit — keep_direct (unique 27)

> tracked team-review draft. 코드 미변경. reviewer 지적: ontology overlay는 target TYPE만 재분류하지 link가 CORRECT한지는 보증 안 함 → keep_direct edge의 실제 precision을 수동 판정.
> 52 card-level direct → **unique 27 (observation, claim)** edge로 dedup 후 판정.

## 분포
- **correct 13 (48%)** · plausible 6 (22%) · too_broad 4 (15%) · **wrong 4 (15%)**
- correct+plausible = **19/27 = 70%** · wrong+too_broad = 8/27 = 30%

## 계통적 오배치 (wrong/too_broad의 뿌리)
1. **Fig 7 ablation ladder 혼선**: positional-embedding 패턴이 patchification belief로 (P24, P25). rung들이 서로 cross-link — L1 ladder 구조 문제(Benseo도 미해결).
2. **cross-mechanism funnel → majority_voting**: larger-model/offline-training 결과가 voting으로 (P39, P40). specific mechanism이 있는데 voting hub로 샘.
3. **관측-leaky 패턴**: 정성 Fig12 관측이 attention mechanism에 (P57) — annotation은 이미 attention을 mechanism으로 뒀지만 source 패턴이 정성.

## 판정 (audit이 말하는 것)
- keep_direct(=39% belief_update)조차 **실제 precision은 correct+plausible 70%**, wrong+too_broad 30%.
- 즉 **새 ontology는 TYPE mixing(thesis/qualifier/leaky/aggregate)을 걷어내지만, 잔여 link precision(ladder 혼선·cross-mechanism funnel)은 못 고침.**
- ontology 변경은 **necessary but not sufficient** — 잔여는 link v3(specific-mechanism 강제) + L1 ladder 처리에서.

## unique 27 direct edge 판정표

| # | obs | pattern | → claim | verdict | note |
|---|---|---|---|---|---|
| 1 | P11 | further improves accuracy [to 60.4%] | majority_voting_consolidates_predictions | **plausible** | ensemble 60.4% → voting (headline이지만 ensemble=voting 방어가능) |
| 2 | P24 | Extending from 1D posi-tional embedding to i | canvas_patchification_enriches_data_redu | **wrong** | positional-embedding 패턴을 patchification에 (Fig7 ladder 혼선) |
| 3 | P25 | observe a degradation [3.5 points, from 5] | canvas_patchification_enriches_data_redu | **wrong** | 2D-ROPE degradation을 patchification에 (ladder 혼선) |
| 4 | P25 | observe a degradation [3.5 points, from 5] | explicit_2d_positional_modeling_preserve | **correct** | 2D ablation → 2D positional ✓ |
| 5 | P27 | Doing so does not increase the computational | canvas_patchification_enriches_data_redu | **plausible** | compute-neutral claim → patchification (이득 아님) |
| 6 | P28 | the 2×2 patchification leads to a noticeable [2.4 points, improv] | canvas_formulation_enables_augmentations | **too_broad** | patchification 결과를 augmentation belief에 |
| 7 | P28 | the 2×2 patchification leads to a noticeable [2.4 points, improv] | canvas_patchification_enriches_data_redu | **correct** | patchification → patchification ✓ |
| 8 | P28 | the 2×2 patchification leads to a noticeable [2.4 points, improv] | patchification_provides_locality_transla | **correct** | patchification → locality ✓ |
| 9 | P29 | increasing depth and/or width leads to highe | increasing_model_size_improves_accuracy_ | **correct** | depth/width↑→acc↑ → model size ✓ |
| 10 | P30 | offline training improves performance [54.5 vs 29.1] | visual_common_sense_learned_from_offline | **correct** | offline training → offline common sense ✓ |
| 11 | P34 | this setting yields an additional gain [2.9 points (from 4] | canvas_formulation_enables_augmentations | **correct** | translation aug → augmentation ✓ |
| 12 | P35 | Scale augmentation yields a substantial gain [6.2 points] | canvas_formulation_enables_augmentations | **correct** | scale aug → augmentation ✓ |
| 13 | P39 | this larger model achieves higher training a | majority_voting_consolidates_predictions | **wrong** | larger-model 결과를 voting에 (cross-mechanism funnel) |
| 14 | P40 | offline training greatly improves the per-fo | majority_voting_consolidates_predictions | **wrong** | offline-training 결과를 voting에 (cross-mechanism funnel) |
| 15 | P45 | multi-view inference further boosts [to 49.8] | majority_voting_consolidates_predictions | **correct** | multi-view → voting ✓ |
| 16 | P47 | VARC (ensemble) is comparable to avg. human  [VARC 60.4, avg. hu] | majority_voting_consolidates_predictions | **plausible** | ensemble headline → voting |
| 17 | P57 | the top-left corner in Fig. 12 shows two tas | early_layer_attention_reflects_pattern_c | **too_broad** | 정성 Fig12 관측 → attention (관측-leaky 패턴) |
| 18 | P57 | the top-left corner in Fig. 12 shows two tas | later_layer_attention_reflects_rule_exte | **too_broad** | 정성 Fig12 관측 → attention |
| 19 | P59 | Increasing the amount of offline training da | visual_common_sense_learned_from_offline | **correct** | offline data↑ → offline ✓ |
| 20 | P60 | Increasing task diversity is beneficial. | visual_common_sense_learned_from_offline | **plausible** | task diversity → offline (diversity≠amount) |
| 21 | P61 | our method achieves a decent accuracy [31.5%] | visual_common_sense_learned_from_offline | **too_broad** | bare accuracy 31.5% → offline (약한 지지) |
| 22 | P62 | increases [to 38.6, 52.3, and] | visual_common_sense_learned_from_offline | **plausible** | offline data scaling → offline |
| 23 | P63 | increases [from 26.4 to 43.1,] | visual_common_sense_learned_from_offline | **plausible** | task-count scaling → offline |
| 24 | P80 | Ambiguous examples | model_handles_ambiguity_proposing_multip | **correct** | ambiguous examples → ambiguity handling ✓ |
| 25 | P82 | Attempt 2 matches Ground Truth, Attempt 1 do | model_handles_ambiguity_proposing_multip | **correct** | multiple attempts → ambiguity ✓ |
| 26 | P95 | multi-view — pass@1 = 49.8 [cell: multi-view, ] | majority_voting_consolidates_predictions | **correct** | Table 2 multi-view asset → voting ✓ |
| 27 | P96 | multi-view — pass@2 = 54.5 [cell: multi-view, ] | majority_voting_consolidates_predictions | **correct** | Table 2 multi-view asset → voting ✓ |