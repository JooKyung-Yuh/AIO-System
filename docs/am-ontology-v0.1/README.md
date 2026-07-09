# AM Ontology v0.1 — design + prototype (draft, team review)

**상태**: draft. 팀 리뷰용. **아직 extract_am / canonicalize / link prompt 코드는 변경 안 함.**
생성: 2026-07-09, VARC 파이프라인(asset-L1 + arm-separation + hygiene + `link_factors_v2`) 위에서.

## 배경
`link_factors_v2`가 broad-thesis hub를 42%→13%로 억제했지만, 새 ontology를 씌워보니 v2 링크의 **61%는 진짜 Observation→Mechanism belief_update가 아니었다** — 일부는 thesis로 roll-up, 일부는 qualifier, 일부는 qualitative observation 강등, 21개는 aggregate_claim이 없어 갈 곳이 없음. 이 폴더는 그 진단을 문서·데이터로 고정한 것.

## 파일 (읽는 순서)
1. **`2026-07-09-am-ontology-v0.1.md`** — 기준 설계문서. 문제 정의 / 23개 AM 재분류 / 타입별 link policy / 3-card schema (Observation·Claim·Qualifier) / edge 정의 / 예시 factor 5개 / 코드 미변경 부분.
2. **`am_ontology_v0.1_annotations.json`** + `...-annotation-summary.md` — 23개 canonical AM에 ontology_type + link/edge/scope policy를 붙인 annotation.
3. **`am_ontology_v0.1_link_overlay.json`** + `...-link-overlay-summary.md` — 기존 v2 링크 133개를 5범주(keep_direct / rolls_up / qualifier / downgrade / unresolved)로 재분류.
4. **`am_ontology_v0.1_projection_preview.json`** + `...-projection-preview.md` — 새 ontology로 재배선한 2-level factor graph 미리보기 + 신규 aggregate_claim 후보.
5. **`2026-07-09-direct-edge-precision-audit.md`** — keep_direct edge의 실제 precision 수동 판정 (unique 27, correct+plausible 70%).
6. **`2026-07-09-am-ontology-migration-spec.md`** — v0.1 → 실제 코드(schema/canonicalize/link v3) 이식 spec. **general rule vs VARC-tuned heuristic 분리** (코드 들어가기 전 gate).
7. `generators/` — 위 JSON/audit을 만든 결정론(no-LLM) 스크립트 4개 (repo-root 상대경로, 재현용). `python docs/am-ontology-v0.1/generators/<name>.py`로 재생성.

## 핵심 수치 (v2 코호트 cohort_2026-07-09_08-44-36 기준)
- 새 ontology 적용 시 **belief_update TYPE으로 남는 것 = 39%** (keep_direct 52/133, **card-level=5빌드 vote-repeated multiset**). 나머지: qualitative_observation 강등 18% · aggregate_claim gap 16% · qualifier 14% · thesis→rolls_up 13%.
- ⚠️ **39%는 TYPE-correct이지 precision 아님**: 52 card-level → **unique 27** direct edge 중 correct+plausible **70%**, wrong+too_broad 30%(Fig7 ablation-ladder 혼선·cross-mechanism funnel). 즉 ontology는 TYPE mixing을 걷어내지만 **잔여 link precision은 link v3 / L1 ladder 과제** (necessary but not sufficient).
- **확정 구조 결정 3개**: paper_thesis는 direct link 금지(rolls_up만) / aggregate_claim 신설 / observation-leaky("visualization shows/reveals/suggests")는 ObservationCard 강등.
- **신설 필요 aggregate_claim 2개**: vision-priors-jointly(+27.7), canvas-components-jointly(+11.5). (other_cumulative는 single-link catch-all이라 claim 승격 안 함 → manual_review.)

## 다음 (합의된 순서)
문서/annotation/overlay/projection 팀 동의 → **migration spec(#6) 합의** → §3 스테이지별 최소 구현(extract_am/canonicalize/link v3, **여기서 처음 코드**). migration spec이 general rule과 VARC-tuned heuristic을 분리하는 gate. **이 폴더까지는 코드 변경 없음.**
