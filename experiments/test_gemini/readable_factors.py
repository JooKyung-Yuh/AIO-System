"""readable_factors.py — resolve a factors.json's node ids to full text (no LLM, deterministic).

A factor card stores only node ids (context: [C6, C7], intervention: I1, pattern: P1, ...). To
read or review a factor you otherwise have to cross-reference spans.json by hand. This inlines the
text so a factor is legible on its own, and flags any field whose id is the wrong category (e.g.
intervention: E18 -> a metric id leaked into the intervention slot), which is exactly the kind of
extraction bug that is invisible in id form but obvious in text.

Outputs, next to the factors.json:
  factors_readable.json  structure preserved, every id -> {"id":..., "text":...}, plus a
                         field_mismatch flag per offending field
  factors_readable.md    one prose block per factor for human reading / sharing
"""
import argparse
import glob
import json
import sys
from pathlib import Path

# which id prefixes are legal in each CIO field
FIELD_PREFIX = {
    "context": ("C",),
    "intervention": ("I",),
    "reference": ("I", "C"),   # baseline arm: another intervention, or a context condition
    "eval_metric": ("E",),
    "pattern": ("P",),
}


def resolve(nid, node_of):
    if not nid:
        return None
    m = node_of.get(nid) or {}
    out = {"id": nid, "text": m.get("text", "(not in spans.json)")}
    if m.get("note"):
        out["note"] = m["note"]          # notes carry the measured numbers (e.g. P-node "54.5 vs 47.5")
    return out


def mismatch(field, nid):
    """True if nid's category prefix is illegal for this field."""
    if not nid:
        return False
    allowed = FIELD_PREFIX.get(field)
    return bool(allowed) and not str(nid).startswith(allowed)


def readable_cio(cio, text_of):
    out, flags = {}, []
    for field in ("context", "intervention", "reference", "eval_metric", "pattern"):
        v = cio.get(field)
        if isinstance(v, list):
            out[field] = [resolve(x, text_of) for x in v]
            bad = [x for x in v if mismatch(field, x)]
            if bad:
                flags.append({"field": field, "bad_ids": bad})
        else:
            out[field] = resolve(v, text_of)
            if mismatch(field, v):
                flags.append({"field": field, "bad_ids": [v]})
    out["direction"] = cio.get("direction")
    out["pattern_class"] = cio.get("pattern_class")
    out["status"] = cio.get("status")
    out["provenance"] = cio.get("provenance")
    return out, flags


def readable_factor(f, text_of):
    cio, flags = readable_cio(f.get("cio", {}), text_of)
    beliefs = []
    for b in f.get("beliefs", []):
        beliefs.append({
            "node": resolve(b.get("node"), text_of),
            "kind": b.get("kind"),
            "direction": b.get("direction"),
            "gloss": b.get("gloss"),
            "evidence": b.get("evidence"),
        })
    return {"factor_id": f.get("factor_id"), "cio": cio, "beliefs": beliefs,
            "field_mismatches": flags}


def _t(node):
    if not isinstance(node, dict):
        return "—"
    return node["text"] + (f"  [{node['note']}]" if node.get("note") else "")


def factor_to_prose(rf):
    cio = rf["cio"]
    lines = [f"### {rf['factor_id']}  ({cio.get('pattern_class') or '?'}, {cio.get('status') or '?'})"]
    prov = cio.get("provenance") or {}
    if prov:
        lines.append(f"*from {prov.get('location','?')} ({prov.get('source_span','?')})*")
    ctx = "; ".join(_t(x) for x in (cio.get("context") or []) if x) or "—"
    lines.append(f"- **context**: {ctx}")
    if cio.get("intervention"):
        arm = f"  vs reference: {_t(cio['reference'])}" if cio.get("reference") else ""
        lines.append(f"- **intervention**: {_t(cio['intervention'])}{arm}")
    if cio.get("eval_metric") or cio.get("pattern"):
        d = f" ({cio['direction']})" if cio.get("direction") else ""
        metric = _t(cio["eval_metric"]) if cio.get("eval_metric") else "—"
        pat = _t(cio["pattern"]) if cio.get("pattern") else "—"
        lines.append(f"- **observed**: {pat}{d}  [metric: {metric}]")
    for b in rf["beliefs"]:
        arrow = "↑ strengthens" if b.get("direction") == "strengthen" else "↓ weakens" if b.get("direction") == "weaken" else "→"
        lines.append(f"- **{arrow}** [{b.get('kind')}] {b.get('gloss') or _t(b.get('node'))}")
    if rf["field_mismatches"]:
        for m in rf["field_mismatches"]:
            lines.append(f"- ⚠️ **field mismatch**: `{m['field']}` holds {m['bad_ids']} (wrong category)")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Inline node-id text into a factors.json (readable view).")
    ap.add_argument("--run-dir", required=True, help="runs/<run> holding spans.json")
    ap.add_argument("--factors", required=True, help="path to a factors.json (a build's, or a joined final one)")
    ap.add_argument("--out-json", default=None, help="default: factors_readable.json next to --factors")
    ap.add_argument("--out-md", default=None, help="default: factors_readable.md next to --factors")
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    spans = json.loads((run_dir / "spans.json").read_text(encoding="utf-8"))
    node_of = {s["node_id"]: {"text": s.get("text", ""), "note": s.get("note", "")} for s in spans}

    factors = json.loads(Path(args.factors).read_text(encoding="utf-8"))
    readable = [readable_factor(f, node_of) for f in factors]

    out_json = Path(args.out_json) if args.out_json else Path(args.factors).with_name("factors_readable.json")
    out_md = Path(args.out_md) if args.out_md else Path(args.factors).with_name("factors_readable.md")
    out_json.write_text(json.dumps(readable, indent=2, ensure_ascii=False), encoding="utf-8")

    n_flag = sum(1 for r in readable if r["field_mismatches"])
    header = (f"# Readable factors — {Path(args.factors).parent.name}\n\n"
              f"{len(readable)} factors, {n_flag} with a field-category mismatch.\n")
    out_md.write_text(header + "\n" + "\n\n".join(factor_to_prose(r) for r in readable), encoding="utf-8")

    print(f"{len(readable)} factors -> {out_json.name}, {out_md.name}")
    print(f"field-category mismatches: {n_flag} factors")


if __name__ == "__main__":
    main()
