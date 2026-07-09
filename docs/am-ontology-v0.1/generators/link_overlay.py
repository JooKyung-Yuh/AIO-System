"""Overlay AM ontology v0.1 annotations onto the v2 link graph and reclassify each link (no LLM).
Answers: applying the new ontology, what % of v2 links stay as real direct belief_update?"""
import json, glob, collections, re, sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]   # generators/ -> am-ontology-v0.1/ -> docs/ -> repo root
COH = BASE / "experiments/test_gemini/runs/2026-07-07_04-57-06_PXX_gemini-2-5-flash_assetmerged2/factors/cohort_2026-07-09_08-44-36_am_v3_2_N5"
SPANS = BASE / "experiments/test_gemini/runs/2026-07-07_04-57-06_PXX_gemini-2-5-flash_assetmerged2/spans.json"
ANNO = BASE / "docs/am-ontology-v0.1/am_ontology_v0.1_annotations.json"
OUT_JSON = BASE / "docs/am-ontology-v0.1/am_ontology_v0.1_link_overlay.json"
OUT_MD = BASE / "docs/am-ontology-v0.1/2026-07-09-am-ontology-link-overlay-summary.md"

byspan = {s["node_id"]: s for s in json.load(open(SPANS))}
anno = {a["canonical_id"]: a for a in json.load(open(ANNO))["annotations"]}
reg = json.load(open(COH / "canonical/registry.json")); r2c = reg["raw2canon"]

# aggregate / cumulative-ablation observation language (should map to aggregate_claim, which is absent)
AGG_RE = re.compile(r"cumulativ|jointly|combined|these priors|priors .*(gain|yield)|"
                    r"canvas.?based designs|\([a-f]\s*[-–→to]+\s*[a-f]\)", re.I)

TYPE2CAT = {
    "mechanism": "keep_direct", "aggregate_claim": "keep_direct",
    "paper_thesis": "convert_to_rolls_up",
    "assumption": "convert_to_qualifier", "scope_condition": "convert_to_qualifier",
    "limitation": "convert_to_qualifier", "precondition": "convert_to_qualifier",
    "qualitative_observation": "downgrade_to_observation",
}

overlay = []
cat = collections.Counter()
moved_qo = collections.Counter()          # qualitative_observation fan-in movement
referenced = set()
for b in sorted(glob.glob(str(COH / "builds/*/"))):
    try:
        cio = {x["cio_id"]: x for x in json.load(open(f"{b}/cio_cards.json"))}
        amc = {x["am_id"]: x for x in json.load(open(f"{b}/am_cards.json"))}
        links = json.load(open(f"{b}/links.json"))
    except Exception:
        continue
    for e in links:
        pat = cio.get(e.get("source_cio"), {}).get("pattern")
        ptext = byspan.get(pat, {}).get("text", "") if pat else ""
        card = amc.get(e.get("target_am"), {})
        atoms = [card.get("node")] + list(card.get("aliases") or [])
        canon = next((r2c[a] for a in atoms if a in r2c), None)
        if not canon or canon not in anno:
            cat["unresolved_or_gap"] += 1
            overlay.append({"pattern": pat, "pattern_text": ptext[:60], "target": canon,
                            "ontology_type": None, "category": "unresolved_or_gap",
                            "reason": "target not in annotation (should not happen)"})
            continue
        referenced.add(canon)
        otype = anno[canon]["ontology_type"]
        category = TYPE2CAT[otype]
        reason = otype
        # aggregate observation routed to a component mechanism -> aggregate_claim GAP -> unresolved
        is_agg = bool(AGG_RE.search(ptext))
        if category == "keep_direct" and otype == "mechanism" and is_agg:
            category = "unresolved_or_gap"; reason = "aggregate observation -> needs aggregate_claim (absent)"
        if otype == "qualitative_observation":
            moved_qo[canon] += 1
        cat[category] += 1
        overlay.append({"pattern": pat, "pattern_text": ptext[:60], "target": canon,
                        "ontology_type": otype, "is_aggregate_obs": is_agg,
                        "category": category, "reason": reason,
                        "new_edge": {"keep_direct": "strengthen/weaken", "convert_to_rolls_up": "rolls_up",
                                     "convert_to_qualifier": anno[canon]["edge_policy"],
                                     "downgrade_to_observation": "demoted", "unresolved_or_gap": "no-link"}[category]})

total = sum(cat.values())
def pct(n): return f"{round(100*n/max(total,1))}%"
meta = {
    "source_cohort": COH.name, "total_v2_links": total,
    "categories": {k: {"n": cat[k], "pct": pct(cat[k])} for k in
                   ("keep_direct","convert_to_rolls_up","convert_to_qualifier","downgrade_to_observation","unresolved_or_gap")},
    "paper_thesis_direct_links_removed": cat["convert_to_rolls_up"],
    "qualitative_observation_moved": {"total": sum(moved_qo.values()), "by_node": dict(moved_qo)},
    "aggregate_gap_unresolved": sum(1 for o in overlay if o["category"]=="unresolved_or_gap" and "aggregate" in o.get("reason","")),
    "n_distinct_am_referenced": len(referenced),
    "core_metric_direct_belief_update_share": pct(cat["keep_direct"]),
}
overlay.sort(key=lambda o: (o["category"], str(o.get("pattern")), str(o.get("target")), o.get("new_edge", "")))
OUT_JSON.write_text(json.dumps({"meta": meta, "links": overlay}, indent=2, ensure_ascii=False), encoding="utf-8")

L = [f"# AM ontology v0.1 — link overlay 재해석 ({COH.name})", "",
     "> tracked team-review draft. 코드/프롬프트 미변경. annotation overlay만 씌운 결정론 재분류.",
     f"> annotation: `am_ontology_v0.1_annotations.json` · 대상 v2 links(card-level, 5빌드): **{total}**", "",
     "## 핵심 질문: 새 ontology 적용 시 몇 %가 진짜 direct belief_update로 남는가",
     f"### → **keep_direct = {meta['core_metric_direct_belief_update_share']}** ({cat['keep_direct']}/{total})", "",
     "## 범주별 재분류", ""]
for k, label in (("keep_direct","Observation→mechanism 유지 (strengthen/weaken)"),
                 ("convert_to_rolls_up","paper_thesis → direct 제거, rolls_up 후보"),
                 ("convert_to_qualifier","assumption/scope/limitation → qualifies/depends_on"),
                 ("downgrade_to_observation","qualitative_observation → belief layer에서 강등"),
                 ("unresolved_or_gap","aggregate_claim 부재 등 → no-link/unresolved")):
    L.append(f"- **{k}**: {cat[k]} ({pct(cat[k])}) — {label}")
L += ["", "## 세부", "",
      f"- **paper_thesis direct link 제거**: {meta['paper_thesis_direct_links_removed']}개 → rolls_up/reported_as_main_result 후보로",
      f"- **qualitative_observation fan-in 이동**: {meta['qualitative_observation_moved']['total']}개가 belief→관측 (문서 예상 ~24와 대조)",
      f"    - node별: " + ", ".join(f"{c.split('_')[1] if '_' in c else c}:{n}" for c,n in meta['qualitative_observation_moved']['by_node'].items()),
      f"- **aggregate_claim gap unresolved**: {meta['aggregate_gap_unresolved']}개 (집계 관측인데 갈 곳 없음)",
      "", "## factor precision 관점 expected improvement",
      f"- v2 raw link 중 **~{meta['core_metric_direct_belief_update_share']}만 진짜 belief_update**로 남고, 나머지는:",
      f"  thesis-funnel({pct(cat['convert_to_rolls_up'])})는 rolls_up으로 격하(관측 직결 아님), "
      f"관측-누수({pct(cat['downgrade_to_observation'])})는 belief에서 제거, "
      f"조건류({pct(cat['convert_to_qualifier'])})는 qualifier로.",
      "- 즉 새 ontology는 **belief 레이어를 절반가량으로 정제**해 **precision audit 대상을 좁힌다**(type-mixing 제거). 남은 direct link의 실제 precision은 별도 audit(unique 27, correct+plausible 70%, wrong+too_broad 30%) 참조 — ontology가 precision 자체를 보장하진 않음.",
      "- 단 aggregate_claim 신설 전까지 집계 관측은 unresolved로 남음(코드 단계 과제).",
      "", "## 검증",
      f"1. 23개 AM만 참조: {len(referenced)}개 distinct 참조, 전부 annotation 내 = {all(c in anno for c in referenced)}",
      f"2. paper_thesis direct link 0: keep_direct 중 paper_thesis = {sum(1 for o in overlay if o.get('ontology_type')=='paper_thesis' and o['category']=='keep_direct')}",
      f"3. qualitative_observation belief target 제거: downgrade={cat['downgrade_to_observation']} (keep_direct에 qo 0 = {sum(1 for o in overlay if o.get('ontology_type')=='qualitative_observation' and o['category']=='keep_direct')==0})",
      f"4. mechanism direct 유지: keep_direct 전부 mechanism/aggregate = {all(o.get('ontology_type') in ('mechanism','aggregate_claim') for o in overlay if o['category']=='keep_direct')}",
      f"5. aggregate_claim gap 별도 집계: {meta['aggregate_gap_unresolved']}개"]
OUT_MD.write_text("\n".join(L), encoding="utf-8")
print(f"wrote {OUT_JSON.name} + {OUT_MD.name}")
print(f"total {total} | " + " ".join(f"{k}={cat[k]}({pct(cat[k])})" for k in
      ("keep_direct","convert_to_rolls_up","convert_to_qualifier","downgrade_to_observation","unresolved_or_gap")))
print(f"core: direct belief_update share = {meta['core_metric_direct_belief_update_share']}")
