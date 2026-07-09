"""merge_l1_sources.py — merge deterministic asset spans into the prose L1 spans (no LLM).

Renumbers asset span ids to CONTINUE each category's global sequence (so C/E/P ids stay unique
next to the prose spans), tags provenance (`source_channel`: prose | table_asset), and writes the
merged spans.json to a NEW run dir. Non-destructive on purpose: the original v7 run — and every
committed cohort that references its ids — is left untouched.

Dedup is deliberately loose for now (per the plan): a value that appears in both prose and a table
keeps BOTH nodes, distinguishable by source_channel; tighten later once the asset channel is
trusted. The new run dir starts with only spans.json; re-run group_evidence_units.py on it to
regenerate evidence_units.json, then a build to check the Table-2 CIO recovery.
"""
import argparse
import collections
import json
import re
from pathlib import Path

PREFIX = {"assumption": "A", "context": "C", "mechanism": "M",
          "intervention": "I", "eval_metric": "E", "pattern": "P"}


def max_num(spans, prefix):
    hi = 0
    for s in spans:
        m = re.fullmatch(rf"{prefix}(\d+)", str(s.get("node_id", "")))
        if m:
            hi = max(hi, int(m.group(1)))
    return hi


def main():
    ap = argparse.ArgumentParser(description="Merge asset spans into prose spans (no LLM, non-destructive).")
    ap.add_argument("--run-dir", required=True, help="run dir holding the prose spans.json")
    ap.add_argument("--asset-spans", default=None, help="default: <run-dir>/asset_spans.json")
    ap.add_argument("--out-run-dir", required=True, help="NEW run dir to write the merged spans.json")
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    prose = json.loads((run_dir / "spans.json").read_text(encoding="utf-8"))
    asset = json.loads(Path(args.asset_spans or run_dir / "asset_spans.json").read_text(encoding="utf-8"))

    for s in prose:
        s.setdefault("source_channel", "prose")

    # renumber asset ids to continue each category's sequence past the prose max
    nxt = {cat: max_num(prose, pre) + 1 for cat, pre in PREFIX.items()}
    added = collections.Counter()
    for s in asset:
        pre = PREFIX.get(s.get("assigned_label"))
        if not pre:
            continue
        s["node_id"] = f"{pre}{nxt[s['assigned_label']]}"
        nxt[s["assigned_label"]] += 1
        added[s["assigned_label"]] += 1
    # asset spans carry no parent / cross-references, so id renumber needs no remap pass

    merged = prose + asset
    out_dir = Path(args.out_run_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "spans.json").write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")

    by_ch = collections.Counter(s.get("source_channel", "prose") for s in merged)
    print(f"merged {len(prose)} prose + {len(asset)} asset -> {len(merged)} spans  ({dict(by_ch)})")
    print(f"asset nodes added by category: {dict(added)}")
    print(f"wrote {out_dir / 'spans.json'}  (original run untouched)")
    print(f"next: python group_evidence_units.py --run-dir {out_dir}")


if __name__ == "__main__":
    main()
