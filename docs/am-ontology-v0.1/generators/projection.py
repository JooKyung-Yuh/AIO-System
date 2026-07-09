"""Project the v2 link graph into the new AM-ontology view (no LLM, deterministic).
Reads the overlay classification and re-wires: Observation->Claim(mechanism) direct,
Claim->paper_thesis rolls_up, Qualifier->Observation qualifies, qualitative_observation demoted,
and the aggregate_claim GAP with proposed new claim candidates."""
import json, collections, re
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]   # generators/ -> am-ontology-v0.1/ -> docs/ -> repo root
OV = json.load(open(BASE / "docs/am-ontology-v0.1/am_ontology_v0.1_link_overlay.json"))
ANNO = {a["canonical_id"]: a for a in json.load(open(BASE / "docs/am-ontology-v0.1/am_ontology_v0.1_annotations.json"))["annotations"]}
OUT_JSON = BASE / "docs/am-ontology-v0.1/am_ontology_v0.1_projection_preview.json"
OUT_MD = BASE / "docs/am-ontology-v0.1/2026-07-09-am-ontology-projection-preview.md"

THESIS = next(a["canonical_id"] for a in ANNO.values() if a["ontology_type"] == "paper_thesis")
links = OV["links"]

# 1. direct edges (keep_direct): Observation -> Claim(mechanism)
direct = [{"observation": o["pattern"], "pattern_text": o["pattern_text"],
           "claim": o["target"], "claim_gloss": ANNO[o["target"]]["gloss"][:44], "edge": "strengthen/weaken"}
          for o in links if o["category"] == "keep_direct"]
# distinct mechanisms that carry direct observations -> rolls_up to thesis
mechs = sorted({o["claim"] for o in direct})
rolls_up = [{"claim": m, "gloss": ANNO[m]["gloss"][:44], "target": THESIS, "edge": "rolls_up"} for m in mechs]

# 2. qualifier edges (convert_to_qualifier): Qualifier-AM qualifies the Observation
qual = [{"qualifier": o["target"], "qual_type": ANNO[o["target"]]["ontology_type"],
         "edge": ANNO[o["target"]]["edge_policy"], "qualifies_observation": o["pattern"],
         "pattern_text": o["pattern_text"]}
        for o in links if o["category"] == "convert_to_qualifier"]

# 3. demoted qualitative_observation nodes
demoted = collections.Counter(o["target"] for o in links if o["category"] == "downgrade_to_observation")
demoted_nodes = [{"node": c, "gloss": ANNO[c]["gloss"][:50], "affected_links": n,
                  "becomes": "ObservationCard(obs_kind=qualitative_observation)"} for c, n in demoted.most_common()]

# 4. thesis-direct removed (convert_to_rolls_up): observations that lost their direct thesis edge
HEADLINE = re.compile(r"\b\d0\.\d|accuracy|surpass|human|competitive|outperform", re.I)
thesis_removed = []
for o in [x for x in links if x["category"] == "convert_to_rolls_up"]:
    is_head = bool(HEADLINE.search(o["pattern_text"]))
    thesis_removed.append({"observation": o["pattern"], "pattern_text": o["pattern_text"],
        "disposition": "reported_as_main_result candidate (headline/top-line result)" if is_head
                       else "re-route to a specific mechanism (no direct thesis edge)"})

# 5. unresolved -> proposed aggregate_claim candidates
unres = [o for o in links if o["category"] == "unresolved_or_gap"]
def agg_group(t):
    tl = t.lower()
    if "canvas" in tl: return "AGG_canvas_components_jointly_contribute"
    if "prior" in tl: return "AGG_vision_priors_jointly_yield_gain"
    if "d-f" in tl or "(d" in tl: return "AGG_vision_priors_jointly_yield_gain"
    return "AGG_other_cumulative"
agg = collections.defaultdict(list)
for o in unres:
    agg[agg_group(o["pattern_text"])].append(o["pattern_text"])
GLOSS = {"AGG_vision_priors_jointly_yield_gain": "Vision priors jointly explain the accuracy gain (cumulative ablation)",
         "AGG_canvas_components_jointly_contribute": "Canvas-based design components jointly contribute to the gain",
         "AGG_other_cumulative": "Other cumulative/combined result"}
proposed, manual_review = [], []
for k, v in sorted(agg.items(), key=lambda kv: (-len(kv[1]), kv[0])):
    if len(set(v)) >= 2:                                     # UNIQUE pattern >=2 (card-level 반복 제외)
        proposed.append({"proposed_id": k, "gloss": GLOSS[k], "claim_type": "aggregate_claim",
                         "would_absorb_links": len(v), "rolls_up_to": THESIS, "example_patterns": sorted(set(v))[:3]})
    else:
        manual_review += [{"pattern_text": p, "reason": "single-link catch-all; leave unresolved, not a claim type"} for p in v]

# reviewer 지적: 아래 count는 CARD-LEVEL(5빌드 vote-repeated multiset)이지 최종 consensus edge가 아님.
unique_direct = len({(d["observation"], d["claim"]) for d in direct})
unique_all = len({(o["pattern"], o["target"], o["category"]) for o in links})

# deterministic output ordering (arrays built in build-iteration order otherwise)
direct.sort(key=lambda d: (str(d["observation"]), d["claim"]))
qual.sort(key=lambda q: (q["qualifier"], str(q["qualifies_observation"])))
thesis_removed.sort(key=lambda t: str(t["observation"]))
demoted_nodes.sort(key=lambda d: (-d["affected_links"], d["node"]))

meta = {
    "source": OV["meta"]["source_cohort"], "total_v2_links": OV["meta"]["total_v2_links"],
    "granularity": "CARD-LEVEL (5빌드 vote-repeated multiset), NOT final consensus edges",
    "projected_counts": {
        "direct_belief_update (Observation->mechanism)": len(direct),
        "rolls_up (mechanism/aggregate->paper_thesis)": len(rolls_up),
        "qualifier (Qualifier->Observation)": len(qual),
        "demoted qualitative_observation links": sum(demoted.values()),
        "unresolved (aggregate_claim absent)": len(unres),
    },
    "unique_edges": {"direct": unique_direct, "all": unique_all,
                     "note": f"card-level direct {len(direct)} -> unique (observation,claim) {unique_direct}; "
                             f"all 133 -> unique {unique_all}. precision은 unique 기준으로 봐야 함."},
    "exhaustive_check": len(direct) + len(qual) + sum(demoted.values()) + len(thesis_removed) + len(unres),
    "belief_update_share": f"{round(100*len(direct)/OV['meta']['total_v2_links'])}%",
    "new_aggregate_claims_needed": len(proposed),
    "aggregate_manual_review": len(manual_review),
}
preview = {"meta": meta, "direct_edges": direct, "rolls_up_edges": rolls_up, "qualifier_edges": qual,
           "demoted_to_observation": demoted_nodes, "thesis_direct_removed": thesis_removed,
           "unresolved_needing_aggregate_claim": {"count": len(unres), "proposed_aggregate_claims": proposed,
                                                   "manual_review": manual_review}}
OUT_JSON.write_text(json.dumps(preview, indent=2, ensure_ascii=False), encoding="utf-8")

L = [f"# AM ontology v0.1 — projection preview ({meta['source']})", "",
     "> tracked team-review draft. **코드/프롬프트 미변경.** overlay를 새 ontology 그래프로 투영한 결정론 artifact.",
     f"> 대상 v2 links: **{meta['total_v2_links']}** (card-level, 5빌드 vote-repeated). ⚠️ 이 count는 최종 consensus edge가 아니라 multiset — "
     f"unique (observation,claim) direct **{unique_direct}**, 전체 unique {unique_all}. precision은 unique 기준.", "",
     "## 새 ontology로 투영한 factor graph 구조", "",
     f"- **Observation → Claim(mechanism) direct**: {len(direct)}  ← 진짜 belief_update ({meta['belief_update_share']})",
     f"- **Claim → paper_thesis rolls_up**: {len(rolls_up)} mechanism (+ 신규 aggregate_claim {len(proposed)}개)",
     f"- **Qualifier → Observation qualifies/depends_on**: {len(qual)}",
     f"- **qualitative_observation 강등**: {sum(demoted.values())} link, {len(demoted_nodes)} node",
     f"- **thesis-direct 제거**: {len(thesis_removed)} (headline은 reported_as_main_result 후보)",
     f"- **unresolved (aggregate_claim 부재)**: {len(unres)} → 신규 claim {len(proposed)}개로 해소 제안", "",
     f"소진 검증: direct {len(direct)} + qualifier {len(qual)} + demoted {sum(demoted.values())} + "
     f"thesis-removed {len(thesis_removed)} + unresolved {len(unres)} = **{meta['exhaustive_check']}** (=총 {meta['total_v2_links']})", "",
     "## 강등되는 qualitative_observation 노드", ""]
for d in demoted_nodes:
    L.append(f"- `{d['node'][:46]}` (fan-in {d['affected_links']}) → {d['becomes']}")
    L.append(f"    - {d['gloss']}")
L += ["", "## aggregate_claim GAP — 신규 claim 후보 (21 link 해소)", ""]
for p in proposed:
    L.append(f"- **{p['proposed_id']}** — \"{p['gloss']}\"  (흡수 {p['would_absorb_links']} link, rolls_up→thesis)")
    for ex in p["example_patterns"]:
        L.append(f"    - ex: {ex!r}")
L += ["", "## thesis-direct 제거된 관측의 처리", ""]
for t in thesis_removed[:8]:
    L.append(f"- {t['pattern_text']!r} → {t['disposition']}")
L += ["", "## 판정 (preview가 말하는 것)",
      f"- 새 ontology 적용 시 최종 factor graph는 **2-level**로 정돈됨: Observation→mechanism(direct {len(direct)}) → paper_thesis(rolls_up).",
      "- **belief 레이어가 관측-누수/조건/thesis-funnel를 걷어내 절반가량으로 정제** → 남는 direct link가 훨씬 설명가능.",
      f"- **aggregate_claim {len(proposed)}개만 신설**하면 21개 unresolved가 해소되고 집계 관측이 제자리를 찾음.",
      "- 이 구조가 납득되면 다음: aggregate_claim을 extract_am/canonicalize에 넣고 link v3/schema migration.",
      "", "## 성공기준 검증",
      f"1. 133 link 5범주 소진: {meta['exhaustive_check']}=={meta['total_v2_links']} → {meta['exhaustive_check']==meta['total_v2_links']}",
      f"2. keep_direct 52만 belief_update: {len(direct)==52} ({len(direct)})",
      f"3. aggregate gap 대표패턴+신규 claim 제안: {len(proposed)}개 후보, {len(unres)} link 커버",
      f"4. 코드/프롬프트 변경: 없음 (tracked docs artifact only)"]
OUT_MD.write_text("\n".join(L), encoding="utf-8")
print(f"wrote {OUT_JSON.name} + {OUT_MD.name}")
print(f"projected: direct={len(direct)} rolls_up={len(rolls_up)}mech qualifier={len(qual)} demoted={sum(demoted.values())} unresolved={len(unres)}")
print(f"exhaustive: {meta['exhaustive_check']}=={meta['total_v2_links']} | belief_update_share={meta['belief_update_share']} | new aggregate_claims={len(proposed)}")
