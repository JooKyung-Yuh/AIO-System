"""Quick gate check on one split build's AM cards (no API, no LLM).

Prints the numbers a smoke run is judged on when iterating the extract_am prompt:
  - mechanism / assumption counts (want mechanism back near v1's ~11-15, not v2's 39),
  - dedup health (cards_with_alias, total_aliases; alias collapse = under-merged),
  - assumption spot-check list (eyeball whether survivors are load-bearing),
  - whether the headline thesis (M7 by default) merged its restatements into one card.

Usage: python3 check_am_build.py <build_dir> [--thesis M7]
"""
import argparse
import collections
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description="Gate-check AM cards of one split build.")
    ap.add_argument("build_dir", help="runs/<run>/factors/<build> directory")
    ap.add_argument("--thesis", default="M7", help="node id of the headline thesis to check merging")
    args = ap.parse_args()

    build = Path(args.build_dir)
    am = json.loads((build / "am_cards.json").read_text(encoding="utf-8"))

    kinds = collections.Counter(a.get("kind") for a in am)
    with_alias = [a for a in am if a.get("aliases")]
    total_aliases = sum(len(a.get("aliases") or []) for a in am)

    print(f"build: {build.name}")
    meta = json.loads((build / "metadata.json").read_text(encoding="utf-8"))
    print(f"prompts: {meta.get('prompts')}")
    print(f"AM total={len(am)}  mechanism={kinds.get('mechanism',0)}  assumption={kinds.get('assumption',0)}")
    print(f"dedup: cards_with_alias={len(with_alias)}  total_aliases={total_aliases}")

    print("\n-- mechanism cards --")
    for a in am:
        if a.get("kind") == "mechanism":
            al = f"  aliases={a['aliases']}" if a.get("aliases") else ""
            print(f"  {a['node']:5s} {a.get('gloss','')[:64]}{al}")

    print("\n-- assumption cards (spot-check: are these load-bearing?) --")
    for a in am:
        if a.get("kind") == "assumption":
            al = f"  aliases={a['aliases']}" if a.get("aliases") else ""
            print(f"  {a['node']:5s} {a.get('gloss','')[:64]}{al}")

    thesis = args.thesis
    hit = [a for a in am if a.get("node") == thesis or thesis in (a.get("aliases") or [])]
    print(f"\n-- headline thesis {thesis} --")
    if hit:
        a = hit[0]
        role = "representative" if a.get("node") == thesis else f"alias of {a.get('node')}"
        print(f"  found as {role}, card aliases={a.get('aliases')}  gloss={a.get('gloss','')[:60]}")
    else:
        print(f"  {thesis} not carded at all")


if __name__ == "__main__":
    main()
