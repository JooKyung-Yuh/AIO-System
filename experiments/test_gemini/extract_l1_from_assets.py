"""extract_l1_from_assets.py — deterministic L1 spans from parsed table cells (NO LLM).

The table structure in <paper>.assets.json (columns/rows already parsed by extract_text.py) was
only ever used as a coverage denominator; the real L1 pass (extract_aio.py) re-read the PDF and
routinely dropped table RESULTS. Table 2 is the canonical failure: assets.json holds
single-view/multi-view pass@1/pass@2 = 35.9 / 49.8 / 54.5, but spans.json got 3 eval_metric nodes
and ZERO pattern nodes — so no CIO card could anchor on it (cards anchor on a pattern).

This recovers them deterministically: one `pattern` node per measured cell, the metric column as
`eval_metric`, the row identity as `context`. No model call -> the numbers cannot be hallucinated
and coverage is guaranteed. Emits `source_channel: "table_asset"` for provenance; ids are
distinctive (P_<table>_r<i>_<metric>) and category-prefixed, so merge_l1_sources.py can renumber
them into the prose spans' id space later.

Scope: results tables only (Table 1/2/3 by default). Figures are deferred — their asset
`description` is prose, not exact cells, so they need a separate (lower-confidence) pass.
"""
import argparse
import json
import re
from pathlib import Path

# a column header naming a measured result (its cells become patterns), vs a spec/identity column
METRIC_RE = re.compile(r"acc\.?|accuracy|pass\s*@?\s*\d|arc-?\d|score|\bfid\b|error|\bloss\b|"
                       r"\bf1\b|bleu|\brate\b|success|top-?\d", re.I)
# a column whose value names the row (the arm), not a numeric spec
IDENTITY_HEADERS = {"model", "system", "method", "name", "approach", "variant", "config", "", "col"}
NUM_RE = re.compile(r"\d")


def is_metric(col):
    return bool(METRIC_RE.search(col or ""))


def has_num(v):
    return bool(NUM_RE.search(str(v if v is not None else "")))


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "_", (s or "").lower()).strip("_")[:20] or "x"


def _span(nid, label, text, loc, note):
    return {"node_id": nid, "source_span": None, "parent": None, "text": text,
            "location": loc, "note": note, "assigned_label": label, "confidence": 1.0,
            "source_channel": "table_asset"}


def table_spans(table):
    """Deterministic C/E/P spans for one results table, shape-aware:
      - metric columns (is_metric) -> eval_metric; their cells -> pattern
      - identity columns -> the row's context (name); spec columns -> that context's note
      - a row with no numeric cell in any metric column is a section header -> skipped
    Works for row-arm tables (Table 1/3: rows are arms) and column-arm tables (Table 2: the arm is
    folded into the metric-column header, single row)."""
    tid = str(table.get("id", "Table"))
    cols = list(table.get("columns", []))
    metric_cols = [c for c in cols if is_metric(c)]
    id_cols = [c for c in cols if c not in metric_cols]
    name_cols = [c for c in id_cols if (c or "").strip().lower() in IDENTITY_HEADERS] or id_cols[:1]
    spec_cols = [c for c in id_cols if c not in name_cols]

    spans, eval_ids = [], {}
    if not metric_cols:
        return spans, {"table": tid, "note": "no metric column detected", "patterns": 0}

    n_pat = 0
    for ri, row in enumerate(table.get("rows", [])):
        if not any(has_num(row.get(mc)) for mc in metric_cols):
            continue                                            # header / empty row
        name = " ".join(str(row.get(c, "")).strip() for c in name_cols
                        if str(row.get(c, "")).strip())
        specs = "; ".join(f"{c} {str(row[c]).strip()}" for c in spec_cols
                          if str(row.get(c, "")).strip())
        ctx_text = name or specs or f"{tid} row {ri + 1}"
        spans.append(_span(f"C_{_slug(tid)}_r{ri}", "context", ctx_text, tid, specs))
        for mc in metric_cols:
            val = str(row.get(mc, "")).strip()
            if not has_num(val):
                continue
            if mc not in eval_ids:
                eval_ids[mc] = f"E_{_slug(tid)}_{_slug(mc)}"
                spans.append(_span(eval_ids[mc], "eval_metric", mc, tid, ""))
            text = f"{name + ' — ' if name else ''}{mc} = {val}"
            spans.append(_span(f"P_{_slug(tid)}_r{ri}_{_slug(mc)}", "pattern", text, tid,
                               f"cell: {mc} = {val}" + (f"; {specs}" if specs else "")))
            n_pat += 1
    return spans, {"table": tid, "metric_cols": metric_cols, "patterns": n_pat}


def main():
    ap = argparse.ArgumentParser(description="Deterministic L1 spans from assets table cells (no LLM).")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--assets", default="./docs/VARC.assets.json")
    ap.add_argument("--tables", nargs="*", default=["Table 1", "Table 2", "Table 3"],
                    help="table ids to mine (default: the three results tables)")
    ap.add_argument("--out", default=None, help="default: <run-dir>/asset_spans.json")
    args = ap.parse_args()

    assets = json.loads(Path(args.assets).read_text(encoding="utf-8"))
    by_id = {str(t.get("id", "")): t for t in assets.get("tables", [])}

    all_spans, report = [], []
    for tid in args.tables:
        t = by_id.get(tid)
        if not t:
            report.append({"table": tid, "note": "not found in assets"})
            continue
        spans, rep = table_spans(t)
        all_spans.extend(spans)
        report.append(rep)

    out = Path(args.out) if args.out else Path(args.run_dir) / "asset_spans.json"
    out.write_text(json.dumps(all_spans, indent=2, ensure_ascii=False), encoding="utf-8")

    def cnt(lab):
        return sum(1 for s in all_spans if s["assigned_label"] == lab)
    print(f"asset spans: {len(all_spans)}  (pattern={cnt('pattern')}, eval_metric={cnt('eval_metric')}, "
          f"context={cnt('context')}) -> {out}")
    for r in report:
        print(f"  {r.get('table')}: patterns={r.get('patterns', 0)}  {r.get('note','')}")


if __name__ == "__main__":
    main()
