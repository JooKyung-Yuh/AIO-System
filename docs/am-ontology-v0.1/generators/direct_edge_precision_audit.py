"""Precision audit of the keep_direct edges (manual verdicts, deterministic report).
The ontology overlay only reclassifies by target TYPE; it does NOT verify a link is CORRECT. This
dedups the 52 card-level direct edges to their 27 unique (observation, claim) pairs and records a
hand verdict (correct / plausible / too_broad / wrong) per pair, so the "39% belief_update" claim
is qualified by actual precision."""
import json, collections
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
PROJ = json.load(open(BASE / "docs/am-ontology-v0.1/am_ontology_v0.1_projection_preview.json"))
SPANS = {s["node_id"]: s for s in json.load(open(
    BASE / "experiments/test_gemini/runs/2026-07-07_04-57-06_PXX_gemini-2-5-flash_assetmerged2/spans.json"))}
OUT = BASE / "docs/am-ontology-v0.1/2026-07-09-direct-edge-precision-audit.md"

# hand verdict per unique (pattern, claim-substring). correct | plausible | too_broad | wrong
VERDICTS = [
    ("P11", "majority_voting", "plausible", "ensemble 60.4% → voting (headline이지만 ensemble=voting 방어가능)"),
    ("P24", "canvas_patchification", "wrong", "positional-embedding 패턴을 patchification에 (Fig7 ladder 혼선)"),
    ("P25", "canvas_patchification", "wrong", "2D-ROPE degradation을 patchification에 (ladder 혼선)"),
    ("P25", "explicit_2d_positional", "correct", "2D ablation → 2D positional ✓"),
    ("P27", "canvas_patchification", "plausible", "compute-neutral claim → patchification (이득 아님)"),
    ("P28", "canvas_formulation_enables", "too_broad", "patchification 결과를 augmentation belief에"),
    ("P28", "canvas_patchification", "correct", "patchification → patchification ✓"),
    ("P28", "patchification_provides_locality", "correct", "patchification → locality ✓"),
    ("P29", "increasing_model_size", "correct", "depth/width↑→acc↑ → model size ✓"),
    ("P30", "visual_common_sense_learned", "correct", "offline training → offline common sense ✓"),
    ("P34", "canvas_formulation_enables", "correct", "translation aug → augmentation ✓"),
    ("P35", "canvas_formulation_enables", "correct", "scale aug → augmentation ✓"),
    ("P39", "majority_voting", "wrong", "larger-model 결과를 voting에 (cross-mechanism funnel)"),
    ("P40", "majority_voting", "wrong", "offline-training 결과를 voting에 (cross-mechanism funnel)"),
    ("P45", "majority_voting", "correct", "multi-view → voting ✓"),
    ("P47", "majority_voting", "plausible", "ensemble headline → voting"),
    ("P57", "early_layer_attention", "too_broad", "정성 Fig12 관측 → attention (관측-leaky 패턴)"),
    ("P57", "later_layer_attention", "too_broad", "정성 Fig12 관측 → attention"),
    ("P59", "visual_common_sense_learned", "correct", "offline data↑ → offline ✓"),
    ("P60", "visual_common_sense_learned", "plausible", "task diversity → offline (diversity≠amount)"),
    ("P61", "visual_common_sense_learned", "too_broad", "bare accuracy 31.5% → offline (약한 지지)"),
    ("P62", "visual_common_sense_learned", "plausible", "offline data scaling → offline"),
    ("P63", "visual_common_sense_learned", "plausible", "task-count scaling → offline"),
    ("P80", "model_handles_ambiguity", "correct", "ambiguous examples → ambiguity handling ✓"),
    ("P82", "model_handles_ambiguity", "correct", "multiple attempts → ambiguity ✓"),
    ("P95", "majority_voting", "correct", "Table 2 multi-view asset → voting ✓"),
    ("P96", "majority_voting", "correct", "Table 2 multi-view asset → voting ✓"),
]

# dedup projection direct edges to unique (observation, claim)
uniq = {}
for d in PROJ["direct_edges"]:
    uniq.setdefault((d["observation"], d["claim"]), d)

def verdict_for(pat, claim):
    for p, sub, v, note in VERDICTS:
        if p == pat and sub in claim:
            return v, note
    return "unmatched", "no hand verdict"

rows, dist = [], collections.Counter()
for (obs, claim), d in sorted(uniq.items()):
    v, note = verdict_for(obs, claim)
    dist[v] += 1
    s = SPANS.get(obs, {})
    ptext = (s.get("text", "")[:44] + (f" [{s.get('note','')[:18]}]" if s.get("note") else ""))
    rows.append((obs, ptext, claim.replace("MECH_", "")[:40], v, note))

n = len(rows)
good = dist["correct"] + dist["plausible"]
L = [f"# Direct-edge precision audit — keep_direct (unique {n})", "",
     "> tracked team-review draft. 코드 미변경. reviewer 지적: ontology overlay는 target TYPE만 재분류하지 "
     "link가 CORRECT한지는 보증 안 함 → keep_direct edge의 실제 precision을 수동 판정.",
     f"> 52 card-level direct → **unique {n} (observation, claim)** edge로 dedup 후 판정.", "",
     "## 분포",
     f"- **correct {dist['correct']} ({round(100*dist['correct']/n)}%)** · plausible {dist['plausible']} ({round(100*dist['plausible']/n)}%) "
     f"· too_broad {dist['too_broad']} ({round(100*dist['too_broad']/n)}%) · **wrong {dist['wrong']} ({round(100*dist['wrong']/n)}%)**",
     f"- correct+plausible = **{good}/{n} = {round(100*good/n)}%** · wrong+too_broad = {n-good}/{n} = {round(100*(n-good)/n)}%", "",
     "## 계통적 오배치 (wrong/too_broad의 뿌리)",
     "1. **Fig 7 ablation ladder 혼선**: positional-embedding 패턴이 patchification belief로 (P24, P25). rung들이 서로 cross-link — L1 ladder 구조 문제(Benseo도 미해결).",
     "2. **cross-mechanism funnel → majority_voting**: larger-model/offline-training 결과가 voting으로 (P39, P40). specific mechanism이 있는데 voting hub로 샘.",
     "3. **관측-leaky 패턴**: 정성 Fig12 관측이 attention mechanism에 (P57) — annotation은 이미 attention을 mechanism으로 뒀지만 source 패턴이 정성.", "",
     "## 판정 (audit이 말하는 것)",
     f"- keep_direct(=39% belief_update)조차 **실제 precision은 correct+plausible {round(100*good/n)}%**, wrong+too_broad {round(100*(n-good)/n)}%.",
     "- 즉 **새 ontology는 TYPE mixing(thesis/qualifier/leaky/aggregate)을 걷어내지만, 잔여 link precision(ladder 혼선·cross-mechanism funnel)은 못 고침.**",
     "- ontology 변경은 **necessary but not sufficient** — 잔여는 link v3(specific-mechanism 강제) + L1 ladder 처리에서.", "",
     "## unique 27 direct edge 판정표", "",
     "| # | obs | pattern | → claim | verdict | note |",
     "|---|---|---|---|---|---|"]
for i, (obs, ptext, claim, v, note) in enumerate(rows, 1):
    L.append(f"| {i} | {obs} | {ptext} | {claim} | **{v}** | {note} |")
OUT.write_text("\n".join(L), encoding="utf-8")
print(f"wrote {OUT.name} · unique {n} · dist {dict(dist)} · correct+plausible {good}/{n}={round(100*good/n)}%")
