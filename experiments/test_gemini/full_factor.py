"""full_factor.py — the final human-readable factor graph for ONE canonical cohort (no LLM).

The cohort's machine output is split across cio_consensus.json (observations, as node ids),
registry.json (canonical nodes + belief status), and spans.json (raw text + measured numbers in
`note`). This stitches them into one legible document:

  * each observation (a surviving CIO pattern) rendered in prose — context / intervention vs
    reference / observed result — with the measured numbers inlined from notes, and the canonical
    group id shown so shared variables are visible;
  * the beliefs it votes on (canonical M/A), each tagged with its cohort status
    (tested / contested / assumed / weakly-tested);
  * a propose_test section: the assumed beliefs (asserted but with zero observation) — the AIO
    output RAG/caption systems don't produce.

Deterministic. Writes full_factor.md + full_factor.json next to the cohort's canonical/.
"""
import argparse
import collections
import json
from pathlib import Path


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def location_order(run_dir):
    path = Path(run_dir) / "evidence_units.json"
    if not path.exists():
        return {}
    return {u["location"]: i for i, u in enumerate(load(path))}


def _t(node_of, nid):
    """Raw node id -> 'text [note]' (note carries the measured numbers). None-safe."""
    if not nid:
        return "—"
    m = node_of.get(nid) or {}
    text = m.get("text") or "(not in spans)"
    return text + (f"  [{m['note']}]" if m.get("note") else "")


def load_belief_edges(cohort):
    """Index canonical/belief_edges.json (produced by canonicalize AFTER link_policy enforcement) by
    observation pattern. Each edge carries its policy bucket (direct / rolls_up / qualifier / demoted)
    so the doc separates genuine Observation->mechanism belief from re-routed edges instead of
    recomputing raw ensemble links (which would re-mix thesis/qualifier/demoted as 'belief')."""
    be = load(cohort / "canonical" / "belief_edges.json")
    by_pat = collections.defaultdict(list)
    for bucket, rows in be.items():
        for e in rows:
            by_pat[e["observation"]].append({**e, "bucket": bucket})
    return by_pat


STATUS_MARK = {"tested": "✓ tested", "contested": "⚔ contested",
               "assumed": "? assumed", "weakly-tested": "~ weak"}
BUCKET_KEY = {"direct": "beliefs", "rolls_up": "rolls_up", "qualifier": "qualifiers", "demoted": "demoted"}


def render(cohort, run_dir):
    cons = load(cohort / "canonical" / "cio_consensus.json")
    registry = load(cohort / "canonical" / "registry.json")
    spans = load(Path(run_dir) / "spans.json")
    node_of = {s["node_id"]: {"text": s.get("text", ""), "note": s.get("note", "")} for s in spans}
    am_reg = registry["am"]
    edges = load_belief_edges(cohort)
    loc_order = location_order(run_dir)

    def loc_rank(c):
        return loc_order.get((c.get("provenance") or {}).get("location", "?"), 10**9)

    pats = sorted(cons.values(), key=lambda c: (loc_rank(c), c["pattern"]))
    factors = []
    for i, c in enumerate(pats, 1):
        prov = c.get("provenance") or {}
        by_bucket = {"beliefs": [], "rolls_up": [], "qualifiers": [], "demoted": []}
        for e in sorted(edges.get(c["pattern"], []),
                        key=lambda e: (e["bucket"], -e["n_builds"], e["target"], e["direction"])):
            rec = am_reg.get(e["target"], {})
            by_bucket[BUCKET_KEY[e["bucket"]]].append(
                {"canonical": e["target"], "direction": e["direction"], "edge_type": e["edge_type"],
                 "n_builds": e["n_builds"], "status": rec.get("status"), "gloss": rec.get("gloss") or e["target"]})
        factors.append({
            "factor_id": f"F{i:03d}",
            "pattern": c["pattern"],
            "pattern_class": c.get("pattern_class"),
            "location": prov.get("location"),
            "context": [_t(node_of, x) for x in (c.get("context") or [])],
            "intervention": _t(node_of, c.get("intervention")) if c.get("intervention") else None,
            "reference": _t(node_of, c.get("reference")) if c.get("reference") else None,
            "eval_metric": _t(node_of, c.get("eval_metric")) if c.get("eval_metric") else None,
            "pattern_text": _t(node_of, c["pattern"]),
            "direction": c.get("direction"),
            "canonical": c.get("canonical"),
            "field_mismatch": list((c.get("field_mismatch") or {}).keys()) or None,
            "beliefs": by_bucket["beliefs"],
            "rolls_up": by_bucket["rolls_up"],
            "qualifiers": by_bucket["qualifiers"],
            "demoted": by_bucket["demoted"],
        })

    propose = sorted((rec for rec in am_reg.values() if rec.get("propose_test")),
                     key=lambda r: r.get("canonical_id", ""))
    return factors, propose, am_reg


def to_md(factors, propose, cohort_name):
    st_ct = collections.Counter(b["status"] for f in factors for b in f["beliefs"])
    pol_ct = collections.Counter()
    for f in factors:
        for k in ("beliefs", "rolls_up", "qualifiers", "demoted"):
            pol_ct[k] += len(f[k])
    lines = [f"# Full factor graph — {cohort_name}", "",
             f"{len(factors)} observations · {len(propose)} propose_test targets "
             f"(asserted beliefs with no observation).",
             "Belief edges are link_policy-enforced: only **direct** edges (↑/↓) are genuine "
             "Observation→mechanism belief_update; rolls_up / qualifier / demoted are re-routed and "
             "are **not** belief_update.", ""]
    lines.append("## Observations (φ) → beliefs (δ)")
    for f in factors:
        head = f"### {f['factor_id']} · {f['pattern']} · {f.get('pattern_class') or '?'}"
        if f.get("location"):
            head += f" · _{f['location']}_"
        lines.append(head)
        if f["context"]:
            lines.append(f"- **context**: " + "; ".join(x for x in f["context"] if x != "—"))
        if f["intervention"]:
            arm = f"  _vs_  {f['reference']}" if f["reference"] else ""
            lines.append(f"- **intervention**: {f['intervention']}{arm}")
        d = f" ({f['direction']})" if f.get("direction") else ""
        metric = f"  [metric: {f['eval_metric']}]" if f["eval_metric"] else ""
        lines.append(f"- **observed**: {f['pattern_text']}{d}{metric}")
        for b in f["beliefs"]:
            arrow = "↑" if b["direction"] == "strengthen" else "↓" if b["direction"] == "weaken" else "→"
            mark = STATUS_MARK.get(b["status"], b["status"] or "?")
            lines.append(f"    - {arrow} _{mark}_ (n{b['n_builds']}) {b['gloss'][:70]}")
        if not f["beliefs"]:
            lines.append("    - _(no direct belief edge)_")
        for b in f["rolls_up"]:
            lines.append(f"    - ⤴ _rolls_up→thesis_ (n{b['n_builds']}) {b['gloss'][:66]}")
        for b in f["qualifiers"]:
            lines.append(f"    - ◇ _qualifier (not belief)_ (n{b['n_builds']}) {b['gloss'][:66]}")
        for b in f["demoted"]:
            lines.append(f"    - ∅ _demoted-observation (not belief)_ (n{b['n_builds']}) {b['gloss'][:60]}")
        if f["field_mismatch"]:
            lines.append(f"- ⚠️ field mismatch: {f['field_mismatch']}")
        lines.append("")
    lines += ["## propose_test — asserted but untested here (AIO differentiator)", ""]
    for rec in propose:
        lines.append(f"- **{rec.get('canonical_id')}** — {rec.get('gloss')}  "
                     f"(_{rec.get('type')}_, {len(rec.get('members') or [])} raw nodes)")
    lines += ["", f"_direct belief edge status tally: {dict(st_ct)}_",
              f"_edges by policy: {dict(pol_ct)}_"]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Render the final canonical factor graph (readable).")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--cohort", required=True, help="cohort dir (ensemble.json + canonical/)")
    args = ap.parse_args()
    cohort = Path(args.cohort)
    factors, propose, _ = render(cohort, args.run_dir)
    (cohort / "full_factor.json").write_text(
        json.dumps({"factors": factors, "propose_test": [r.get("canonical_id") for r in propose]},
                   indent=2, ensure_ascii=False), encoding="utf-8")
    (cohort / "full_factor.md").write_text(to_md(factors, propose, cohort.name), encoding="utf-8")
    print(f"{len(factors)} factors, {len(propose)} propose_test -> {cohort/'full_factor.md'}")


if __name__ == "__main__":
    main()
