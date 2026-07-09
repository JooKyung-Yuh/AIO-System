# AM Ontology v0.1 → v1 Migration Spec (one-page, tracked team-review draft)

> **목적**: v0.1 ontology를 실제 schema / canonicalize / link v3로 옮기기 전, **무엇이 paper-agnostic
> general rule이고 무엇이 VARC-tuned heuristic인지 분리**해서 고정한다. 이걸 안 쓰고 구현하면
> aggregate_claim 쪽 VARC 휴리스틱이 시스템 규칙처럼 굳는다.
> **코드 변경 없음.** 근거: 같은 폴더의 annotation / overlay / projection / precision-audit.

---

## 1. General rules (paper-agnostic — 다음 논문에도 그대로 이식)

- **paper_thesis는 direct Observation link 금지.** 관측이 headline 결론을 직접 strengthen/weaken 못 함.
- **mechanism | aggregate_claim → paper_thesis는 `rolls_up`만.** thesis는 집계로만 도달.
- **observation-leaky ("shows / reveals / suggests" 류)** → `ObservationCard(obs_kind=qualitative_observation)`로
  강등. belief target 아님.
- **assumption | scope_condition | precondition | limitation은 기본 `QualifierCard`** (`qualifies` / `depends_on`).
- **명시적으로 tested된 assumption만 `ClaimCard`로 승격 가능.** (기본은 Qualifier)

→ 이식 시 이 §1은 **코드 상수/규칙**으로 하드코딩해도 됨 (논문 무관).

## 2. VARC-tuned rules (per-paper 손질 필요 — 일반 규칙 아님)

- **aggregate_claim grouping의 `canvas` / `prior` / `d-f` 문자열 휴리스틱은 VARC-specific.**
  (`generators/projection.py:agg_group()`)
- **`AGG_vision_priors_jointly_yield_gain`, `AGG_canvas_components_jointly_contribute`는 VARC claim gloss.**
- **다음 논문에서는 per-paper aggregate grouping 또는 LLM-assisted claim proposal 필요.**

→ 이식 시 이 §2는 **per-paper 설정/플러그인**으로 분리 (시스템 코어에 넣지 말 것).

## 3. Minimal implementation stages (gated — 여기서 처음 코드)

- **extract_am**: 현재 kind 2종 → `ClaimCard(mechanism | aggregate_claim | paper_thesis)` /
  `QualifierCard(assumption | scope_condition | precondition | limitation)` /
  `ObservationCard(qualitative_observation)`로 분리 (또는 `type` 필드 확장 + 강등 규칙).
- **canonicalize**: 위 타입 정책 반영 — paper_thesis non-linkable, **aggregate_claim 신설**,
  qualifier 분리, qualitative_observation 강등.
- **link_v3**: 엣지타입 분리 —
  `strengthen/weaken`(→ mechanism | aggregate_claim **only**),
  `rolls_up`(mechanism | aggregate_claim → paper_thesis),
  `qualifies` / `depends_on`(Qualifier → Observation | Claim),
  `reported_as_main_result`(headline Observation → paper_thesis, 후보).
- **eval/report**: **39% type-correct share**와 **70% manual precision(unique 27)**을 **분리해서** 보고 (합치지 말 것).

## 4. Success criteria

- 기존 v2 결과를 새 ontology로 **재현 가능** (133 link가 5범주로 소진).
- **direct belief_update는 mechanism | aggregate_claim만** 허용.
- **paper_thesis direct = 0.**
- **qualifier가 strengthen/weaken으로 들어가지 않음.**
- **aggregate_claim gap 21 중 VARC 20개는 2개 aggregate_claim으로 흡수, single-link 1개는 manual_review 유지.**

## 5. Explicit caveats (발표/공유 시 그대로 명시)

- **direct precision audit은 manual audit이지 PDF gold validation 아님.**
- **VARC prototype이지 아직 cross-paper generalization 아님.**
- **generator는 docs 재생성기이며 production validator 아님.**

---

## 순서
이 spec 합의 → §3 스테이지별 최소 구현(여기서 처음 코드) → 다음 논문에서 §2(VARC-tuned)를 일반화 규칙으로 승격할지 검증. **§1은 general, §2는 per-paper**로 코드에서 물리적으로 분리하는 게 이 spec의 핵심.
