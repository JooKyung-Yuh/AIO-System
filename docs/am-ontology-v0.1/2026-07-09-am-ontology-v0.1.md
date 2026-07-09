# AM Ontology v0.1 — 설계문서 (draft, docs-jk 개인 검토용)

> 상태: **설계 고정 전용. 코드 변경 금지.** 팀 리뷰 후 tracked docs로 이동.
> 근거: 2026-07-09 L2 link audit (arm-separated assetmerged2 + hygiene + `link_factors_v2` smoke).
> 선행: asset-L1(coverage) → arm-separation → structural hygiene → `link_factors_v2`(precision)까지 닫힘.
> 이 문서는 그 다음, **prompt로 안 풀리고 ontology로만 풀리는 문제**를 고정한다.

---

## 1. 현재 AMIOC v0의 문제 정의

현재 AM 레이어는 **mechanism / assumption 두 kind만** 두고, 모든 AM 카드를 **동등한 belief target**으로 취급한다. 관측(CIO)은 전부 `strengthen/weaken` 한 종류 엣지로 아무 AM에나 붙는다. 그 결과:

1. **paper-level thesis가 belief target으로 취급됨.** "Visual learning enables abstraction"는 mechanism이 아니라 **논문 전체 결론**인데, 거의 모든 결과가 이걸 "지지"한다. v1에서 link의 **42%**가 여기로 funnel. `link_factors_v2`(specificity-first)로 **13%**까지 줄였지만, 여전히 belief target으로 남아 있어 근절 안 됨.
2. **aggregate_claim 타입 부재.** "vision prior들을 합치면 +27.7" 같은 **집계/누적 결과**가 붙을 belief 노드가 없다. 그래서 집계 결과가 단일 component mechanism(예: "2D positional")에 **오배치**된다 (v2의 남은 too_broad).
3. **observation-leaky 카드.** "attention maps **reveal**...", "TTT visualization **shows**...", "embedding **suggests**..."는 인과 mechanism이 아니라 **정성 관측(qualitative observation)**인데 mechanism으로 라벨돼 belief target 노릇을 한다. 특히 "TTT visualization shows"는 fan-in 16(**12%**)의 큰 hub인데, 실은 관측이다.

**한 줄**: v0는 "무엇이 belief이고 무엇이 결론/조건/관측인지"를 구분하지 않아, link precision이 구조적으로 샌다.

---

## 2. 23개 canonical AM cluster 재분류 (v2 코호트 기준)

fan-in = v2 5빌드의 **card-level** link를 canonical AM으로 resolve해 합산 (=133, **unresolved 0**). **ensemble `nodes.links` total(141)은 atom-level**(각 link를 AM카드 member atom들로 확장) — 133<141은 unresolved 제외가 아니라 **card-vs-atom granularity 차이**다.

| 재분류 type | canonical gloss | fan-in | v0 kind |
|---|---|---:|---|
| **paper_thesis** | Visual learning enables abstraction/inference without language | 17 (13%) | mech |
| mechanism | Explicit 2D positional modeling preserves image structure | 17 | mech |
| **observation-leaky** | TTT visualization shows model adapting to task-specific arrangement | 16 | mech |
| mechanism | Canvas patchification enriches data, reduces overfitting | 14 | mech |
| mechanism | Canvas formulation enables augmentations for translation/scale | 12 | mech |
| mechanism | Majority voting consolidates predictions from different views | 10 | mech |
| mechanism | Visual common sense is learned from offline training data | 10 | mech |
| assumption | Some ARC tasks admit multiple plausible rules | 9 | assu |
| **observation-leaky** | Attention maps reveal pixel-to-pixel reasoning relations | 7 | mech |
| scope_condition | Single pixel error invalidates entire ARC prediction | 4 | assu |
| mechanism | Model handles ambiguity by proposing multiple interpretations | 4 | mech |
| assumption | Some tasks are solvable from scratch (tabula rasa) | 3 | mech |
| **limitation** | Correct predictions exist in views but are outvoted | 3 | mech |
| mechanism | Increasing model size improves accuracy by better fitting | 3 | mech |
| mechanism | Early-layer attention reflects pattern core influence | 1 | mech |
| **observation-leaky** | Task embedding visualization suggests inter-task learning | 1 | mech |
| mechanism | Later-layer attention reflects rule for extending pixels | 1 | mech |
| mechanism | Patchification provides locality and translation invariance | 1 | mech |
| mechanism | Average pooling aggregates predictions for raw-grid location | 0 | mech |
| assumption | Multiple unseen tasks cannot be assumed simultaneously | 0 | assu |
| scope_condition | Multi-view inference cost is negligible compared to TTT | 0 | assu |
| **limitation** | Larger models beyond current regime lead to overfitting | 0 | assu |
| mechanism | Attention masks / loss focus improve foreground attention | 0 | mech |
| **aggregate_claim** | *(현재 없음 — 신설 필요)* | — | — |

**집계**: mechanism ~13, observation-leaky **3** (fan-in 16+7+1=24 = 18%가 관측인데 belief로 샘), assumption 3, scope_condition 2, limitation 2, paper_thesis 1, aggregate_claim **0(gap)**.

---

## 3. 타입별 link target policy

| type | direct Observation link? | 정책 |
|---|---|---|
| **mechanism** | ✅ 허용 | `strengthen/weaken`의 정상 대상. v2가 올바로 라우팅하는 곳. |
| **aggregate_claim** (신설) | ✅ 허용 (집계 관측만) | 누적/조합/ensemble 결과가 여기로. component mechanism으로 쪼개 붙이지 않음. |
| **paper_thesis** | ❌ **금지** | mechanism/aggregate_claim에서 `rolls_up`으로만. (예외: §5 reported_as_main_result) |
| **assumption** | ❌ 기본 | **기본 QualifierCard** (`depends_on/holds_under`). 논문이 그 assumption을 **명시적으로 test할 때만** ClaimCard로 승격. (아래 정책 참조) |
| **scope_condition** | ❌ | QUALIFIER. `qualifies`로 Observation/Claim에 부착. belief_update 아님. |
| **precondition** | ❌ | QUALIFIER. `depends_on`. |
| **limitation** | ❌ | QUALIFIER. `qualifies`(주로 부정적). |
| **observation-leaky** | — | belief 아님. **ObservationCard로 강등** (아래 §4). |

### paper_thesis (명확히 박음)
- **direct Observation link 금지.**
- mechanism / aggregate_claim → paper_thesis 를 `rolls_up` 엣지로만 연결.
- **예외**: abstract headline result처럼 **논문 전체 성능 요약 관측**(예: "VARC 60.4%, avg human 매칭")은 mechanism 경유가 어색할 수 있음 → `strengthen` 대신 **`reported_as_main_result`** 같은 별도 엣지로 thesis에 직결하는 방안 검토(v0.2). 단 이건 "구체 result가 headline임"을 표시하는 것이지 belief 강화가 아님.

### aggregate_claim (신설, 필수)
- **정의**: multiple components가 **jointly** 한 결과를 설명하는 주장.
- **부착 대상**: cumulative ablation ("b→f 합쳐 +27.7"), combined priors, ensemble-level result.
- **금지**: 이 집계 관측을 단일 component mechanism(2D/canvas 등)에 쪼개 붙이지 말 것.
- aggregate_claim → paper_thesis 는 `rolls_up`.

### observation-leaky (강등, 필수)
- "attention maps reveal...", "visualization shows...", "embedding suggests..." 류.
- **mechanism 아님 → ObservationCard로.** belief target에서 제거.
- **용어**: `observation-leaky`는 **진단(diagnosis) 용어**. **schema 타입명은 `ObservationCard(obs_kind=qualitative_observation)`.** 문서에선 둘 다 써도 됨: observation-leaky diagnosis → `obs_kind=qualitative_observation`.
- 효과: v2 fan-in의 ~18%(TTT-16 포함)가 belief 레이어에서 빠져 관측 레이어로 내려감 → thesis/mechanism hub 추가 정화.

### assumption (기본 정책 박음)
- **기본값: assumption은 belief_update(strengthen/weaken) 대상이 아니다 → `QualifierCard`.**
  ( _Assumption is not a belief_update target by default._ )
- **예외: 논문이 그 assumption을 명시적으로 test할 때만** `ClaimCard`가 될 수 있다.
  ( _Only if the paper explicitly tests the assumption, it may become a ClaimCard; otherwise it is a QualifierCard._ )
- 그 외에는 `depends_on / holds_under`로 Observation/Claim에 부착.

---

## 4. Schema: ObservationCard / ClaimCard / QualifierCard

```
ObservationCard (φ) — 측정된/관측된 사실
  pattern            측정 결과 (P-node, +note 수치)
  context[]          설정 (C-node)
  intervention       조작 arm (I-node)
  reference          비교 arm (I 또는 C)
  eval_metric        측정 도구 (E)
  direction          up/down/flat
  obs_kind           quantitative | qualitative_observation
                     ← "visualization shows/reveals/suggests" 류(구 mechanism)를 흡수
                       (진단 용어 observation-leaky = obs_kind=qualitative_observation)

ClaimCard (belief) — 논문이 주장하는 것
  claim_type         mechanism | aggregate_claim | paper_thesis
  gloss, members
  - mechanism        인과 why. Observation이 strengthen/weaken 직접 링크 대상 ✅
  - aggregate_claim  여러 component의 합/조합 주장. 집계 Observation이 여기로 ✅
  - paper_thesis     headline 결론. direct link 금지. rolls_up 수신만.

QualifierCard (조건) — Claim/Observation의 유효성 조건
  qual_type          assumption | scope_condition | precondition | limitation
  gloss, members
  → belief_update(강화/약화) 아님. qualifies/depends_on 으로 부착.
```

## 5. Edge type 정의

```
Observation --strengthen | weaken--> ClaimCard(mechanism | aggregate_claim)
    (= 지금의 belief_update. explicit + specificity + this-result 규칙은 link_factors_v2에 이미 반영)

ClaimCard(mechanism | aggregate_claim) --rolls_up--> ClaimCard(paper_thesis)
    (NEW. thesis는 관측이 직접 못 붙음. mechanism/aggregate가 집계로 올림)

QualifierCard --qualifies | depends_on--> ObservationCard | ClaimCard
    (NEW. scope/precondition/limitation/assumption이 조건으로 부착. 강화/약화 아님)

(검토) Observation(headline summary) --reported_as_main_result--> paper_thesis
    (v0.2 예외 엣지. §3 paper_thesis 예외)
```

---

## 6. 예시 factor 5개 (새 ontology)

**F1 — Table 1 ViT vs U-Net**
```
Observation(quant): ctx=[ViT 18M] interv=ViT ref=U-Net metric=acc → 54.5 vs 47.5 (up)
  --strengthen--> Claim(mechanism): "Explicit 2D positional modeling preserves structure"
Qualifier(scope): "single pixel error invalidates prediction" --qualifies--> Observation
```

**F2 — Table 2 multi-view** (v2가 이미 올바로 라우팅)
```
Observation(quant): interv=multi-view ref=single-view metric=pass@1 → 49.8 vs 35.9 (up)
  --strengthen--> Claim(mechanism): "Majority voting consolidates predictions"
Qualifier(limitation): "correct predictions can be outvoted" --qualifies--> Claim
```

**F3 — Figure 7 누적 집계 (+27.7)** ← 지금 오배치되는 것, ontology로 해소
```
Observation(quant): interv=all vision priors (b→f cumulative) metric=acc → +27.7 (up)
  --strengthen--> Claim(aggregate_claim): "Vision priors jointly enable the approach"   ← NEW 타입
     (2D/canvas 개별 mechanism에 직접 붙이지 않음)
Claim(aggregate_claim) --rolls_up--> Claim(paper_thesis): "visual learning enables abstraction"
```

**F4 — headline 60.4%** (전체 성능 요약 → 단일 mechanism에 붙이지 않음)
```
Observation(quant): VARC ensemble, ARC-1 acc → 60.4% (avg human 매칭)
  옵션A: --reported_as_main_result--> Claim(paper_thesis): "visual learning enables abstraction"
  옵션B: --strengthen--> Claim(aggregate_claim): "VARC system-level combination achieves strong ARC performance"
            --rolls_up--> Claim(paper_thesis)
  (주의: majority voting은 Table 2 multi-view엔 딱 맞지만 headline 60.4 전체 성능엔 너무 좁음
   → aggregate result를 단일 mechanism에 붙이는 실수 회피)
```

**F5 — Figure 8 model size sweep + limitation**
```
Observation(quant): interv=ViT 6M→66M metric=acc → 44.4→53.0 (up, 그 뒤 flat)
  --strengthen--> Claim(mechanism): "Increasing model size improves fitting"
Qualifier(limitation): "larger models beyond current regime overfit" --qualifies--> Claim
Qualifier(observation, 강등된 것 아님): —
```

---

## 7. v2 prompt로 해결된 것 vs ontology 변경이 필요한 것

| 문제 | 해결 주체 | 상태 |
|---|---|---|
| broad thesis funnel (42%) | `link_factors_v2` (specificity-first) | ✅ 완화 (42→13%) — 단 근절은 ontology(thesis non-linkable) |
| Table 3 system → thesis 과흡수 (93x) | v2 | ✅ (→1x) |
| multi-view result → 정확한 mechanism | v2 | ✅ (→majority voting) |
| fan-out 과다 | v2 (cap ~2) | ✅ (max 5→2) |
| **aggregate result → component 오배치** | **ontology (aggregate_claim 신설)** | 🔴 미해결 |
| **observation-leaky가 belief target** | **ontology (ObservationCard 강등)** | 🔴 미해결 |
| **thesis가 belief target** | **ontology (paper_thesis non-linkable + rolls_up)** | 🔴 미해결 (v2는 완화만) |
| Figure 7 ablation ladder rung 혼선 | L1 ladder 구조 (별개, Benseo도 미해결) | ⏸ 보류 |

---

## 8. 아직 코드 변경하지 말아야 할 부분

- **AM card schema** (extract_am 출력) — 지금 kind 2종. 타입 확장은 문서 합의 후.
- **canonicalize_v0.py** — AM 클러스터링/status 로직. 타입 주입은 prototype(§다음액션 3) 이후.
- **link prompt** — `link_factors_v2` 유지. rolls_up/qualifies 엣지타입은 ontology 합의 후 v3에서.
- **plot/eval** — 새 엣지타입 생기면 그때.

**이유**: 타입 정책을 문서로 먼저 고정하지 않으면 prompt/코드가 먼저 가고, 나중에 "이게 thesis냐 mechanism이냐"로 흔들린다. 문서 → annotation JSON → graph 재해석 → 코드 순서를 지킨다.

---

## 다음 액션 (합의된 순서)
1. ✅ **이 문서** (AM ontology v0.1, docs-jk)
2. 팀/검토자 읽고 **구조 동의** (특히 paper_thesis non-linkable, aggregate_claim 신설, observation-leaky 강등)
3. **prototype**: 기존 canonical AM 23개를 새 타입으로 annotate하는 JSON 생성 (no LLM, 수동/규칙 혼합)
4. **link graph 재해석**: 기존 링크를 새 ontology(rolls_up/qualifies 분리)로 다시 그려 precision 재추정
5. **코드 변경**: 그다음 (schema/canonicalize/link v3)

_기존 AMIOC는 이제 "coverage(asset-L1) + precision(v2 link) 개선까지 된 v0"로 정리 가능._
