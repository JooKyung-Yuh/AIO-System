"""eval_cohort.py — read one cohort's gate metrics (no LLM), optionally vs a baseline cohort.

Surfaces the numbers a grounding change is judged on, and — because notes carry the measured
values (a P-node's "54.5 vs 47.5") — resolves every referenced node to text + note so table
grounding is legible without a decoder ring.

Usage: python eval_cohort.py --run-dir <run> --cohort <cohort_dir> [--baseline <cohort_dir>]
"""
import argparse
import collections
import json
import statistics as st
from pathlib import Path


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def node_map(run_dir):
    spans = load(Path(run_dir) / "spans.json")
    return {s["node_id"]: {"text": s.get("text", ""), "note": s.get("note", "")} for s in spans}


def show(nid, nm):
    if not nid:
        return "—"
    m = nm.get(nid, {})
    t = m.get("text", "?")[:60]
    return f"{nid}={t!r}" + (f" [{m['note']}]" if m.get("note") else "")


def gates(cohort):
    ens = load(cohort / "ensemble.json")
    rep = ens["reproducibility_mean_pairwise_jaccard"]
    rpt = load(cohort / "canonical" / "canon_report.json")
    reg = load(cohort / "canonical" / "registry.json")
    return {
        "assumption_raw_jaccard": rep.get("am_assumption_raw"),
        "mechanism_raw_jaccard": rep.get("am_mechanism_raw"),
        "cio_pattern_jaccard": rep.get("cio_pattern"),
        "link_jaccard": rep.get("link_atomic"),
        "band_counts": ens.get("band_counts"),
        "cio_field_errors": rpt.get("cio_field_errors"),
        "promoted_interventions": rpt.get("promoted_interventions"),
        "eval_metric_clusters": sorted(reg.get("eval_metric", {}).keys()),
        "am_cluster_bands": rpt.get("am_cluster_bands"),
        "am_status": rpt.get("am_status"),
        "belief_edges_by_policy": rpt.get("belief_edges_by_policy"),
        "context_before_after": [rpt.get("before", {}).get("context"), rpt.get("after", {}).get("context")],
    }


def summarize_across(cohort_dirs, out=None):
    """Headline-metric mean±std over several cohorts built from the SAME prompt set.

    A single cohort's Jaccard is one draw from a noisy distribution (temp=0 Gemini still
    varies run-to-run), so one number can't tell a real prompt gain from luck. Repeating the
    SAME prompt across cohorts and reporting mean±std gives the confidence interval: only a
    shift larger than the std is signal. Pure deterministic aggregation — no LLM."""
    keys = ["assum", "mech", "cio", "link", "field_errors", "promoted", "comp_refs", "comp_total",
            "st_assumed", "st_contested", "st_tested", "st_rollup", "st_qualifier", "st_demoted",
            "be_direct", "be_rolls_up", "be_qualifier", "be_demoted", "propose_test"]
    acc = {k: [] for k in keys}
    per_cohort = []
    prompt_sets = set()
    for c in cohort_dirs:
        c = Path(c)
        ens = load(c / "ensemble.json")
        rpt = load(c / "canonical" / "canon_report.json")
        cons = load(c / "canonical" / "cio_consensus.json")
        j = ens["reproducibility_mean_pairwise_jaccard"]
        comp = [v for v in cons.values() if v.get("pattern_class") == "comparison"]
        amst = rpt.get("am_status") or {}
        bep = rpt.get("belief_edges_by_policy") or {}
        if ens.get("prompts"):
            prompt_sets.add(tuple(sorted(ens["prompts"].items())))
        row = {
            "cohort": c.name,
            "n_builds": j.get("n_builds"),
            "assum": j.get("am_assumption_raw"),
            "mech": j.get("am_mechanism_raw"),
            "cio": j.get("cio_pattern"),
            "link": j.get("link_atomic"),
            "field_errors": rpt.get("cio_field_errors"),
            "promoted": rpt.get("promoted_interventions"),
            "comp_refs": sum(1 for v in comp if v.get("reference")),
            "comp_total": len(comp),
            "st_assumed": amst.get("assumed", 0),
            "st_contested": amst.get("contested", 0),
            "st_tested": amst.get("tested", 0),
            "st_rollup": amst.get("rollup_target", 0),
            "st_qualifier": amst.get("qualifier", 0),
            "st_demoted": amst.get("demoted_observation", 0),
            "be_direct": bep.get("direct", 0),
            "be_rolls_up": bep.get("rolls_up", 0),
            "be_qualifier": bep.get("qualifier", 0),
            "be_demoted": bep.get("demoted", 0),
            "propose_test": len(rpt.get("propose_test_targets") or []),
        }
        per_cohort.append(row)
        for k in keys:
            if row[k] is not None:
                acc[k].append(row[k])

    if len(prompt_sets) > 1:
        print("[WARN] cohorts do NOT share one prompt set — mean±std mixes prompts, not pure variance")

    stats = {}
    for k in keys:
        vals = acc[k]
        if not vals:
            continue
        stats[k] = {"mean": round(st.mean(vals), 3),
                    "std": round(st.pstdev(vals), 3) if len(vals) > 1 else 0.0,
                    "raw": vals}

    print(f"=== across {len(cohort_dirs)} cohorts (same prompt set) ===")
    for r in per_cohort:
        print(f"  {r['cohort']}  (n={r['n_builds']} builds)")
    print(f"\n{'metric':14s} {'mean':>8s} ± {'std':<7s}  raw")
    for k in keys:
        if k not in stats:
            print(f"{k:14s} {'—':>8s}")
            continue
        print(f"{k:14s} {stats[k]['mean']:>8} ± {stats[k]['std']:<7}  {stats[k]['raw']}")

    if out:
        report = {
            "n_cohorts": len(cohort_dirs),
            "cohorts": [r["cohort"] for r in per_cohort],
            "prompt_set": dict(next(iter(prompt_sets))) if len(prompt_sets) == 1 else "MIXED",
            "per_cohort": per_cohort,
            "mean_std": stats,
            "note": "same-prompt cohort-to-cohort variance; a prompt change is signal only if it "
                    "moves a metric by more than ~2x its std here.",
        }
        Path(out).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nwrote {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", default=None, help="run dir (for node text/notes in single-cohort view)")
    ap.add_argument("--cohort", default=None, help="single cohort dir (holds ensemble.json + canonical/)")
    ap.add_argument("--cohorts", nargs="+", default=None,
                    help="two+ cohort dirs built from the SAME prompt set -> headline mean±std "
                         "(quantifies cohort-to-cohort variance; use before trusting a single number)")
    ap.add_argument("--baseline", default=None, help="another cohort dir to diff against")
    ap.add_argument("--tables", nargs="*", default=["Table 1", "Table 2", "Table 3"])
    ap.add_argument("--out", default=None, help="with --cohorts: write the variance report JSON here")
    args = ap.parse_args()

    if args.cohorts:
        summarize_across(args.cohorts, out=args.out)
        return
    if not args.cohort:
        ap.error("pass --cohort <dir> for a single cohort, or --cohorts <dir dir ...> for mean±std")
    if not args.run_dir:
        ap.error("--run-dir is required with --cohort (needed to resolve node text/notes)")

    nm = node_map(args.run_dir)
    cohort = Path(args.cohort)
    g = gates(cohort)

    print(f"=== cohort: {cohort.name} ===")
    print(f"reproducibility  assumption={g['assumption_raw_jaccard']}  mechanism={g['mechanism_raw_jaccard']}"
          f"  cio={g['cio_pattern_jaccard']}  link={g['link_jaccard']}")
    print(f"band_counts      {json.dumps(g['band_counts'], ensure_ascii=False)}")
    print(f"cio_field_errors {g['cio_field_errors']}   promoted_interventions {g['promoted_interventions']}")
    print(f"eval_metric      {g['eval_metric_clusters']}")
    print(f"am_cluster_bands {g['am_cluster_bands']}   context {g['context_before_after'][0]} -> {g['context_before_after'][1]}")
    print(f"belief_edges     {json.dumps(g['belief_edges_by_policy'], ensure_ascii=False)}")
    print(f"am_status        {json.dumps(g['am_status'], ensure_ascii=False)}")

    if args.baseline:
        gb = gates(Path(args.baseline))
        print(f"\n=== vs baseline {Path(args.baseline).name} ===")
        for k in ("cio_field_errors", "assumption_raw_jaccard", "mechanism_raw_jaccard"):
            print(f"  {k}: {gb[k]} -> {g[k]}")
        print(f"  eval_metric clusters: {len(gb['eval_metric_clusters'])} -> {len(g['eval_metric_clusters'])}")

    # --- table grounding: consensus CIO cards anchored on a table, with node notes ---
    cons = load(cohort / "canonical" / "cio_consensus.json")
    print("\n=== table grounding (CIO cards anchored on tables; notes carry the numbers) ===")
    for tbl in args.tables:
        cards = [c for c in cons.values() if (c.get("provenance") or {}).get("location") == tbl]
        print(f"\n-- {tbl}: {len(cards)} CIO card(s) --")
        for c in cards:
            print(f"  pattern   {show(c.get('pattern'), nm)}")
            print(f"    metric  {show(c.get('eval_metric'), nm)}   dir={c.get('direction')}  class={c.get('pattern_class')}")
            print(f"    interv  {show(c.get('intervention'), nm)}")
            print(f"    ref     {show(c.get('reference'), nm)}")
            if c.get("field_mismatch"):
                print(f"    ⚠ mismatch {list(c['field_mismatch'].keys())}")


if __name__ == "__main__":
    main()
