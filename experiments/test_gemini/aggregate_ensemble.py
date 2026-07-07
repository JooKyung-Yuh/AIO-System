"""Deterministic k-of-N ensemble aggregation over several split builds of ONE run.

Same-prompt split builds of the same spans.json disagree run-to-run — CIO is stable (pattern
Jaccard ~0.85) but AM belief judgement drifts, assumption especially (raw-node Jaccard ~0.08).
This tool turns N such builds into one stabilized set by DETERMINISTIC voting (no LLM), and
reports the reproducibility numbers so prompt changes can be measured before/after.

Vote keys are chosen so grouping instability never leaks into the vote (see the plan):
  - CIO       : pattern node id (the Layer-1 anchor, fixed across runs) — never cio_id.
  - AM        : raw Layer-1 node id. Each AM card's node + aliases are flattened to atoms, so a
                concept that is one card in run A and split across two in run B still votes as its
                member atoms. Clustering back into cards is a SEPARATE, later step.
  - link      : (cio_pattern_node, raw_am_node, direction) — never (cio_id, am_id).

Accept thresholds are per layer; assumptions get a higher bar by default because they are the
least reproducible. Everything kept carries confidence = votes / N.

Only builds whose prompt versions match are pooled; mixing prompts in one vote is refused
(different sampling distributions). Pass explicit build dirs, or --auto to pool every build in a
run that shares the newest build's prompt set.
"""
import argparse
import collections
import glob
import json
import sys
from pathlib import Path

CATS = {"A": "assumption", "M": "mechanism", "C": "context",
        "I": "intervention", "E": "eval_metric", "P": "pattern"}


def cat_of(node_id):
    return CATS.get(str(node_id)[:1]) if node_id else None


def load_build(d):
    d = Path(d)
    return {
        "dir": d,
        "cio": json.loads((d / "cio_cards.json").read_text(encoding="utf-8")),
        "am": json.loads((d / "am_cards.json").read_text(encoding="utf-8")),
        "links": json.loads((d / "links.json").read_text(encoding="utf-8")),
        "meta": json.loads((d / "metadata.json").read_text(encoding="utf-8")),
    }


def am_atoms(card):
    """Every raw Layer-1 node id a single AM card covers (representative + aliases)."""
    return {card.get("node")} | set(card.get("aliases") or [])


def cio_pattern(card):
    return card.get("pattern")


# ---- per-build normalized signals (as SETS, for both voting and Jaccard) -------------------
def build_signals(b):
    cio_keys = {cio_pattern(c) for c in b["cio"] if cio_pattern(c)}
    am_by_kind = collections.defaultdict(set)
    am_pattern_of_atom = {}
    for card in b["am"]:
        for atom in am_atoms(card):
            if atom:
                am_by_kind[card.get("kind")].add(atom)
    # link atoms: expand each link's target am card into its atoms
    am_card_by_id = {c.get("am_id"): c for c in b["am"]}
    cio_pat_by_id = {c.get("cio_id"): cio_pattern(c) for c in b["cio"]}
    link_keys = set()
    for e in b["links"]:
        pat = cio_pat_by_id.get(e.get("source_cio"))
        card = am_card_by_id.get(e.get("target_am"))
        if not pat or not card:
            continue
        for atom in am_atoms(card):
            if atom:
                link_keys.add((pat, atom, e.get("direction")))
    return {"cio": cio_keys, "am_by_kind": am_by_kind,
            "am_all": set().union(*am_by_kind.values()) if am_by_kind else set(),
            "links": link_keys}


def jaccard(a, b):
    return round(len(a & b) / len(a | b), 3) if (a | b) else None


def pairwise_jaccard(sets):
    """Mean pairwise Jaccard over a list of sets (None if <2 non-trivial)."""
    vals = []
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            v = jaccard(sets[i], sets[j])
            if v is not None:
                vals.append(v)
    return round(sum(vals) / len(vals), 3) if vals else None


def vote(counter, n, threshold):
    """{key: [keys with votes>=threshold] -> confidence} plus full tally."""
    accepted = {k: round(v / n, 3) for k, v in counter.items() if v >= threshold}
    return accepted


def main():
    ap = argparse.ArgumentParser(description="k-of-N deterministic ensemble over split builds.")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--builds-dir", default=None,
                    help="directory holding the build folders to pool (default: <run-dir>/factors). "
                         "Point this at one cohort's builds/ so cohorts never cross-pool.")
    ap.add_argument("--builds", nargs="*", help="explicit build dirs/names to pool (overrides --builds-dir scan)")
    ap.add_argument("--auto", action="store_true",
                    help="pool the largest same-prompt cohort under --builds-dir")
    ap.add_argument("--cio-threshold", type=int, default=None, help="default: majority ceil(N/2)+... -> 3 for N=5")
    ap.add_argument("--mech-threshold", type=int, default=None)
    ap.add_argument("--assum-threshold", type=int, default=None, help="default one higher than mech")
    ap.add_argument("--link-threshold", type=int, default=None)
    ap.add_argument("--out", default=None, help="write ensemble json here (default: run-dir/ensemble/<tag>.json)")
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    builds_dir = Path(args.builds_dir) if args.builds_dir else run_dir / "factors"
    if args.builds:
        # Accept either a bare build name (resolved under builds_dir) or a full path.
        def resolve(b):
            p = Path(b)
            if (p / "cio_cards.json").exists():
                return p
            cand = builds_dir / b
            if (cand / "cio_cards.json").exists():
                return cand
            sys.exit(f"build not found: {b} (looked at {p} and {cand})")
        build_dirs = [resolve(b) for b in args.builds]
    else:
        all_dirs = sorted(glob.glob(str(builds_dir / "*" / "cio_cards.json")))
        build_dirs = [Path(p).parent for p in all_dirs]
        if not build_dirs:
            sys.exit(f"no split builds under {builds_dir}")

    builds = [load_build(d) for d in build_dirs]

    # Refuse to mix prompt versions in one vote.
    def prompt_key(b):
        p = b["meta"].get("prompts")
        return tuple(sorted(p.items())) if p else ("legacy",)
    if args.auto:
        # Pool the LARGEST same-prompt cohort (ties broken by the most recent build), so a
        # stray one-off build on a different prompt never shrinks the vote to itself.
        groups = collections.defaultdict(list)
        for b in builds:
            groups[prompt_key(b)].append(b)
        want = max(groups, key=lambda k: (len(groups[k]),
                                          max(b["meta"].get("timestamp", "") for b in groups[k])))
        builds = groups[want]
    else:
        keys = {prompt_key(b) for b in builds}
        if len(keys) > 1:
            sys.exit(f"refusing to pool builds with different prompt versions: {keys}\n"
                     f"pass a matching subset or use --auto")

    n = len(builds)
    if n < 2:
        sys.exit(f"need >=2 builds to vote, got {n}")
    cio_t = args.cio_threshold or (n // 2 + 1)
    mech_t = args.mech_threshold or (n // 2 + 1)
    assum_t = args.assum_threshold or min(n, (n // 2 + 2))   # one stricter than mechanism
    link_t = args.link_threshold or (n // 2 + 1)

    sigs = [build_signals(b) for b in builds]

    # --- reproducibility report (mean pairwise Jaccard) ---
    repro = {
        "n_builds": n,
        "cio_pattern": pairwise_jaccard([s["cio"] for s in sigs]),
        "am_all_raw": pairwise_jaccard([s["am_all"] for s in sigs]),
        "am_mechanism_raw": pairwise_jaccard([s["am_by_kind"].get("mechanism", set()) for s in sigs]),
        "am_assumption_raw": pairwise_jaccard([s["am_by_kind"].get("assumption", set()) for s in sigs]),
        "link_atomic": pairwise_jaccard([s["links"] for s in sigs]),
    }

    # --- tallies ---
    cio_ctr = collections.Counter()
    am_ctr = collections.Counter()
    link_ctr = collections.Counter()
    for s in sigs:
        cio_ctr.update(s["cio"])
        am_ctr.update(s["am_all"])
        link_ctr.update(s["links"])

    accepted_cio = vote(cio_ctr, n, cio_t)
    # AM split by category via node-id prefix
    accepted_am = {}
    for atom, votes in am_ctr.items():
        cat = cat_of(atom)
        t = assum_t if cat == "assumption" else mech_t
        if votes >= t:
            accepted_am[atom] = {"kind": cat, "votes": votes, "confidence": round(votes / n, 3)}
    accepted_links = {f"{p}|{a}|{d}": {"cio_pattern": p, "am_node": a, "direction": d,
                                       "votes": v, "confidence": round(v / n, 3)}
                      for (p, a, d), v in link_ctr.items() if v >= link_t}

    out = {
        "run_dir": str(run_dir),
        "builds": [str(b["dir"].name) for b in builds],
        "prompts": builds[0]["meta"].get("prompts"),
        "thresholds": {"cio": cio_t, "mechanism": mech_t, "assumption": assum_t, "link": link_t},
        "reproducibility_mean_pairwise_jaccard": repro,
        "accepted": {
            "cio_patterns": accepted_cio,
            "am_nodes": accepted_am,
            "links": accepted_links,
        },
        "counts": {
            "cio_patterns": len(accepted_cio),
            "am_mechanism": sum(1 for v in accepted_am.values() if v["kind"] == "mechanism"),
            "am_assumption": sum(1 for v in accepted_am.values() if v["kind"] == "assumption"),
            "links": len(accepted_links),
        },
    }

    tag = f"ensemble_N{n}"
    out_path = Path(args.out) if args.out else run_dir / "ensemble" / f"{tag}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"pooled {n} builds: {out['builds']}")
    print(f"reproducibility (mean pairwise Jaccard): {json.dumps(repro, ensure_ascii=False)}")
    print(f"thresholds cio>={cio_t} mech>={mech_t} assum>={assum_t} link>={link_t}")
    print(f"accepted: cio={out['counts']['cio_patterns']}  "
          f"mechanism={out['counts']['am_mechanism']}  assumption={out['counts']['am_assumption']}  "
          f"links={out['counts']['links']}")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
