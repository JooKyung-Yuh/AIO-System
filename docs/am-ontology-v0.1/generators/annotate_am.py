"""Build AM ontology v0.1 annotations for the 23 canonical AM clusters (no LLM).
Applies the v0.1 policy (docs/am-ontology-v0.1/2026-07-09-am-ontology-v0.1.md) to each cluster and derives the
link/edge/scope policy deterministically from the assigned ontology_type."""
import json, glob, collections, sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]   # generators/ -> am-ontology-v0.1/ -> docs/ -> repo root
COH = BASE / ("experiments/test_gemini/runs/2026-07-07_04-57-06_PXX_gemini-2-5-flash_assetmerged2/"
              "factors/cohort_2026-07-09_08-44-36_am_v3_2_N5")
OUT_JSON = BASE / "docs/am-ontology-v0.1/am_ontology_v0.1_annotations.json"
OUT_MD = BASE / "docs/am-ontology-v0.1/2026-07-09-am-ontology-annotation-summary.md"

am = json.load(open(COH / "canonical/am_canonical.json"))
reg = json.load(open(COH / "canonical/registry.json"))
r2c = reg["raw2canon"]

# fan_in_v2: canonical-AM-resolved links across the 5 v2 builds (unresolved excluded)
fanin = collections.Counter()
resolved = excluded = 0
for b in sorted(glob.glob(str(COH / "builds/*/"))):
    try:
        amc = {x["am_id"]: x for x in json.load(open(f"{b}/am_cards.json"))}
        links = json.load(open(f"{b}/links.json"))
    except Exception:
        continue
    for e in links:
        card = amc.get(e.get("target_am"), {})
        atoms = [card.get("node")] + list(card.get("aliases") or [])
        canon = next((r2c[a] for a in atoms if a in r2c), None)
        if canon:
            fanin[canon] += 1; resolved += 1
        else:
            excluded += 1

# --- hand-authored ontology_type per canonical_id (v0.1 §2 classification) ---
# key = unique substring of canonical_id
TYPE = {
    "visual_learning_enables_abstraction":       ("paper_thesis", "논문 headline 결론. mechanism들이 rolls_up으로 올림. 관측 직결 금지.", "high", "headline result 관측은 reported_as_main_result로 예외 처리할지(v0.2)"),
    "ttt_visualization_shows":                   ("qualitative_observation", "'visualization shows...' = 정성 관측(qualitative), 인과 mechanism 아님. belief target에서 강등.", "high", "강등 후 이 관측이 TTT mechanism을 strengthen하는 source로 남는지"),
    "attention_maps_reveal":                     ("qualitative_observation", "'attention maps reveal...' = 정성 관측. belief target 아님.", "high", "pixel-to-pixel reasoning을 별도 mechanism으로 재추출할지"),
    "task_embedding_visualization_suggests":     ("qualitative_observation", "'visualization suggests...' = 정성 관측.", "high", None),
    "single_pixel_error_invalidates":            ("scope_condition", "ARC 채점 방식의 조건(1픽셀 틀리면 전체 오답). belief 아니라 metric/관측을 qualify.", "high", None),
    "multi_view_inference_cost_negligible":      ("scope_condition", "실용 조건(추론 비용). belief_update 대상 아님.", "high", None),
    "larger_models_beyond_current_regime":       ("limitation", "경계/한계 조건(현 regime 넘으면 overfit). qualifier.", "high", None),
    "correct_predictions_exist_views_but_outvoted": ("limitation", "majority voting의 한계(맞는 view가 밀림). Claim을 qualify.", "medium", "limitation vs empirical observation 경계"),
    "some_arc_tasks_admit_multiple_plausible":   ("assumption", "데이터 전제. 기본 QualifierCard(depends_on). 논문이 명시 test 시에만 Claim.", "medium", "multi-view/ambiguity 결과가 이걸 '명시적으로 test'하는가? → 그러면 Claim 승격"),
    "multiple_unseen_tasks_cannot_assumed":      ("assumption", "scope 전제. 기본 QualifierCard.", "high", None),
    "some_tasks_solvable_from_scratch_tabula":   ("assumption", "벤치마크 속성 전제. 기본 QualifierCard.", "medium", "assumption vs mechanism 경계(현재 MECH로 라벨됨)"),
    "average_pooling_aggregates_predictions":    ("mechanism", "방법-작동원리(집계 방식). 단 method-description 성격도 있음.", "medium", "mechanism vs precondition(method) 경계"),
    # --- straightforward mechanisms ---
    "canvas_formulation_enables_augmentations":  ("mechanism", "인과: canvas가 augmentation 가능케 함.", "high", None),
    "canvas_patchification_enriches_data":       ("mechanism", "인과: patchification이 데이터 다양성↑.", "high", None),
    "early_layer_attention_reflects_pattern":    ("mechanism", "인과(층별 특화).", "medium", "정성 관측 파생이라 obs-leaky 경계"),
    "explicit_2d_positional_modeling_preserves": ("mechanism", "인과: 2D 위치 모델링이 구조 보존.", "high", None),
    "majority_voting_consolidates_predictions":  ("mechanism", "인과: voting이 예측 통합. Table 2 multi-view의 올바른 target.", "high", None),
    "visual_common_sense_learned_from_offline":  ("mechanism", "인과: offline training이 상식 학습.", "high", None),
    "model_handles_ambiguity_proposing_multiple": ("mechanism", "인과: 모델이 모호성을 다중 해석으로 처리.", "medium", None),
    "attention_masks_loss_focus_improve":        ("mechanism", "인과(설계→foreground 주의). fan-in 0 = 미검증.", "medium", "fan-in 0이라 belief로 실재하나"),
    "later_layer_attention_reflects_rule":       ("mechanism", "인과(층별 특화).", "medium", "obs-leaky 경계"),
    "patchification_provides_locality":          ("mechanism", "인과: patchification이 locality/invariance 제공.", "high", None),
    "increasing_model_size_improves_accuracy":   ("mechanism", "인과: 크기↑→fitting↑.", "high", None),
}

# derived policy per ontology_type: (link_policy, edge_policy, target_scope)
POLICY = {
    "mechanism":               ("direct_link_allowed", "strengthen_weaken", "component_level"),
    "aggregate_claim":         ("direct_link_allowed", "strengthen_weaken", "system_level"),
    "paper_thesis":            ("rolls_up_only", "rolls_up", "paper_conclusion"),
    "assumption":              ("qualifier_only", "depends_on", "claim"),
    "scope_condition":         ("qualifier_only", "qualifies", "observation"),
    "precondition":            ("qualifier_only", "depends_on", "observation"),
    "limitation":              ("qualifier_only", "qualifies", "claim"),
    "qualitative_observation": ("no_direct_link", "n/a_demoted_to_observation", "observation"),
}

def classify(cid):
    for key, val in TYPE.items():
        if key in cid:
            return val
    return ("mechanism", "기본값(미분류)", "low", "분류 규칙 누락 — 검토 필요")

annos = []
for cid, rec in am.items():
    otype, rationale, conf, unresolved = classify(cid)
    link_p, edge_p, scope = POLICY[otype]
    annos.append({
        "canonical_id": rec["canonical_id"],
        "current_kind": rec.get("type"),
        "gloss": rec.get("gloss"),
        "members": rec.get("members"),
        "fan_in_v2": fanin.get(cid, 0),
        "ontology_type": otype,
        "link_policy": link_p,
        "edge_policy": edge_p,
        "target_scope": scope,
        "rationale": rationale,
        "confidence": conf,
        "unresolved_questions": unresolved,
    })
annos.sort(key=lambda a: (-a["fan_in_v2"], a["canonical_id"]))   # deterministic order (tie-break by id)

# aggregate_claim gap is explicit
type_counts = collections.Counter(a["ontology_type"] for a in annos)
meta = {
    "source_cohort": COH.name,
    "n_am": len(annos),
    "fan_in_basis": "5 v2 빌드의 card-level links를 canonical AM으로 resolve해 합산(=133, unresolved 0). "
                    "ensemble nodes.links total(141)은 atom-level(각 link를 AM카드 member atoms로 확장)이라 "
                    "granularity가 다름 — 133<141은 unresolved 제외가 아니라 card-vs-atom 차이.",
    "fan_in_resolved": resolved, "fan_in_excluded": excluded, "fan_in_total_resolved": sum(fanin.values()),
    "type_counts": dict(type_counts),
    "aggregate_claim_gap": {"present_members": 0,
        "note": "현재 canonical AM에 aggregate_claim 타입이 하나도 없음 = 설계 gap. "
                "cumulative ablation(+27.7)/combined priors/ensemble 결과가 붙을 belief 노드가 없어 "
                "component mechanism에 오배치됨. extract_am/canonicalize에서 신설 필요(코드 변경은 이후)."},
}
OUT_JSON.write_text(json.dumps({"meta": meta, "annotations": annos}, indent=2, ensure_ascii=False), encoding="utf-8")

# --- summary md ---
L = [f"# AM ontology v0.1 — annotation summary ({COH.name})", "",
     f"> tracked team-review draft. 코드 미변경. 기준본: `2026-07-09-am-ontology-v0.1.md`", "",
     f"- AM {len(annos)}개 전부 annotate. fan_in_v2 = {meta['fan_in_basis']}.",
     f"- resolved links {resolved}, excluded {excluded} (합 {resolved+excluded}). type 분포: {dict(type_counts)}", "",
     "## 타입별", ""]
for t in ("paper_thesis","aggregate_claim","mechanism","qualitative_observation","assumption","scope_condition","limitation","precondition"):
    grp = [a for a in annos if a["ontology_type"] == t]
    L.append(f"### {t} ({len(grp)}) — link_policy: {POLICY.get(t,('?',))[0]}")
    if t == "aggregate_claim" and not grp:
        L.append(f"- ⚠️ **0개 = GAP.** {meta['aggregate_claim_gap']['note']}")
    for a in grp:
        L.append(f"- `{a['canonical_id'][:52]}`  fan_in={a['fan_in_v2']}  conf={a['confidence']}")
        L.append(f"    - {a['gloss'][:64]}")
        L.append(f"    - edge={a['edge_policy']}, scope={a['target_scope']} · {a['rationale']}")
        if a["unresolved_questions"]:
            L.append(f"    - ❓ {a['unresolved_questions']}")
    L.append("")
OUT_MD.write_text("\n".join(L), encoding="utf-8")
print(f"wrote {OUT_JSON.name} + {OUT_MD.name}")
print(f"type_counts: {dict(type_counts)}  (aggregate_claim={type_counts.get('aggregate_claim',0)} = gap)")
print(f"fan_in resolved={resolved} excluded={excluded}")
