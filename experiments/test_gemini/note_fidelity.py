"""note_fidelity.py — deterministic fidelity signal: do the numbers in a table-located node's
`note` actually appear in that table's transcribed cells? (no LLM)

The transcription produces TWO channels of the same tables: prose `note` fields on spans.json
nodes (e.g. P19 note "ViT accuracies: 44.4, 54.5, 53.0; U-Net: 42.8, 47.5, 48.3") and the
structured cells in <paper>.assets.json (rows of {column: value}). Reproducibility says nothing
about whether either is *correct*; but the two channels are independent enough that cross-checking
them is a free correctness proxy. A note number that appears in no cell of its table is a
transcription mismatch worth surfacing (hallucinated/misread value, or a note pointing at the
wrong table).

Outputs runs/<run>/note_fidelity.json + a one-line summary. Scope: nodes whose location names a
table and whose note carries >=1 number.
"""
import argparse
import collections
import json
import re
from pathlib import Path

NUM_RE = re.compile(r"\d+(?:\.\d+)?")


def nums(text):
    """Numeric tokens in a string as rounded floats (44.4 == 44.40; ignores % / M suffixes)."""
    return {round(float(m), 4) for m in NUM_RE.findall(text or "")}


def table_ids_in(location):
    """Table ids named in a node's location string (e.g. 'Table 1|Section 5' -> {'table 1'})."""
    out = set()
    for piece in (location or "").split("|"):
        m = re.search(r"table\s*\d+[a-z]?", piece, re.I)
        if m:
            out.add(m.group(0).lower().replace("  ", " "))
    return out


def main():
    ap = argparse.ArgumentParser(description="Cross-check node note numbers against assets table cells.")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--assets", default="./docs/VARC.assets.json")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    spans = json.loads((run_dir / "spans.json").read_text(encoding="utf-8"))
    assets = json.loads(Path(args.assets).read_text(encoding="utf-8"))

    # table id (normalized) -> set of all numbers across its cells
    table_nums = {}
    for t in assets.get("tables", []):
        tid = str(t.get("id", "")).lower()
        cells = set()
        for row in t.get("rows", []):
            for v in row.values():
                cells |= nums(str(v))
        table_nums[tid] = cells

    rows = []
    total_note_nums = matched = 0
    for s in spans:
        note = s.get("note") or ""
        note_nums = nums(note)
        if not note_nums:
            continue
        tids = table_ids_in(s.get("location", ""))
        tids = [t for t in tids if t in table_nums]
        if not tids:
            continue                                   # note has numbers but not table-located
        cell_pool = set().union(*(table_nums[t] for t in tids))
        missing = sorted(note_nums - cell_pool)
        total_note_nums += len(note_nums)
        matched += len(note_nums & cell_pool)
        if missing:
            rows.append({"node_id": s.get("node_id"), "location": s.get("location"),
                         "tables": tids, "note": note[:120],
                         "missing_numbers": missing,
                         "matched": sorted(note_nums & cell_pool)})

    fidelity = round(matched / total_note_nums, 3) if total_note_nums else None
    report = {
        "note_number_fidelity": fidelity,       # fraction of table-node note numbers found in cells
        "note_numbers_checked": total_note_nums,
        "note_numbers_matched": matched,
        "nodes_with_missing": len(rows),
        "mismatches": rows,
    }
    out = Path(args.out) if args.out else run_dir / "note_fidelity.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"note↔assets fidelity: {fidelity} ({matched}/{total_note_nums} note numbers found in their "
          f"table cells); {len(rows)} node(s) with an unmatched number -> {out.name}")
    for r in rows[:12]:
        print(f"  {r['node_id']} @ {r['location'][:30]}: missing {r['missing_numbers']}  note={r['note'][:60]!r}")


if __name__ == "__main__":
    main()
