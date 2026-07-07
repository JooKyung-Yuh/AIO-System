"""Deterministic Layer-2 pre-step: group Layer-1 spans into evidence units.

No LLM. Groups spans by their Layer-1 "location" (Table N / Figure N / Section X),
then marks parent-sibling subgroups and a provisional pattern_class, so that factor
assembly can run LOCALLY per unit instead of over all spans at once. Emits
evidence_units.json next to spans.json.
"""
import argparse
import collections
import json
import re
from pathlib import Path

CATS = ["assumption", "mechanism", "context", "intervention", "eval_metric", "pattern"]
COMPARE_KW = re.compile(
    r"\b(better|worse|higher|lower|outperform\w*|superior|exceed\w*|versus|vs\.?|"
    r"compared|than|improve\w*|boost\w*|gain\w*|drop\w*)\b",
    re.IGNORECASE,
)


def span_num(s):
    m = re.match(r"S(\d+)", str(s.get("source_span", "")))
    return int(m.group(1)) if m else None


def unit_kind(location: str) -> str:
    loc = location.lower()
    if re.search(r"table|figure|fig", loc):
        return "table_fig"
    if re.search(r"\bsection 1\b|abstract", loc):
        return "intro"
    return "section"


def pattern_class(node: dict, kind: str) -> str:
    blob = f"{node.get('text','')} {node.get('note','')}"
    is_comparison = bool(COMPARE_KW.search(blob))
    has_number = bool(re.search(r"\d", f"{node.get('note','')}{node.get('text','')}"))
    if kind == "table_fig" or has_number:
        return "comparison" if is_comparison else "primary_result"
    if kind == "intro":
        return "summary_claim"
    return "comparison" if is_comparison else "summary_claim"


def build_units(spans):
    by_location = collections.OrderedDict()
    for s in spans:
        by_location.setdefault(s.get("location", "?"), []).append(s)

    units = []
    for idx, (location, members) in enumerate(by_location.items(), 1):
        members = sorted(members, key=lambda s: (span_num(s) is None, span_num(s) or 0))
        kind = unit_kind(location)
        nums = [span_num(s) for s in members if span_num(s) is not None]

        # parent-sibling subgroups: nodes split from the same source sentence.
        parent_groups = collections.defaultdict(list)
        for s in members:
            if s.get("parent"):
                parent_groups[s["parent"]].append(s["node_id"])
        subgroups = [
            {"parent": p, "node_ids": ids}
            for p, ids in parent_groups.items()
            if len(ids) > 1
        ]

        nodes = []
        for s in members:
            entry = {
                "node_id": s["node_id"],
                "label": s["assigned_label"],
                "source_span": s.get("source_span"),
                "parent": s.get("parent"),
                "note": s.get("note", ""),
                "text": s["text"],
            }
            if s["assigned_label"] == "pattern":
                entry["pattern_class"] = pattern_class(s, kind)
            nodes.append(entry)

        counts = collections.Counter(s["assigned_label"] for s in members)
        units.append({
            "unit_id": f"U{idx:03d}",
            "location": location,
            "kind": kind,
            "source_chunk": members[0].get("source_chunk"),
            "span_range": [min(nums), max(nums)] if nums else None,
            "node_count": len(members),
            "category_counts": {c: counts[c] for c in CATS if counts.get(c)},
            "has_pattern": counts.get("pattern", 0) > 0,
            "parent_subgroups": subgroups,
            "nodes": nodes,
        })
    return units


def parse_args():
    p = argparse.ArgumentParser(description="Group Layer-1 spans into local evidence units (no LLM).")
    p.add_argument("--run-dir", required=True, help="runs/<run_id> containing spans.json")
    return p.parse_args()


def main():
    args = parse_args()
    run_dir = Path(args.run_dir)
    spans = json.loads((run_dir / "spans.json").read_text(encoding="utf-8"))
    units = build_units(spans)

    out = run_dir / "evidence_units.json"
    out.write_text(json.dumps(units, indent=2, ensure_ascii=False), encoding="utf-8")

    n_with_pat = sum(u["has_pattern"] for u in units)
    pat_cls = collections.Counter(
        n["pattern_class"]
        for u in units for n in u["nodes"]
        if n["label"] == "pattern"
    )
    print(f"{len(spans)} spans -> {len(units)} evidence units "
          f"({n_with_pat} with >=1 pattern)")
    print(f"provisional pattern_class: {dict(pat_cls)}")
    print(f"wrote {out}")
    print(f"\n{'unit':5s} {'location':18s} {'kind':10s} {'#':>3s} {'span':>10s}  composition")
    for u in sorted(units, key=lambda u: (not u["has_pattern"], -u["node_count"]))[:20]:
        comp = " ".join(f"{k[0].upper()}:{v}" for k, v in u["category_counts"].items())
        rng = f"{u['span_range'][0]}-{u['span_range'][1]}" if u["span_range"] else "-"
        star = "*" if u["has_pattern"] else " "
        print(f"{star}{u['unit_id']:4s} {u['location'][:18]:18s} {u['kind']:10s} "
              f"{u['node_count']:3d} {rng:>10s}  {comp}")


if __name__ == "__main__":
    main()
