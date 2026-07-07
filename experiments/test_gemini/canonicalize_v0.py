"""canonicalize_v0.py — deterministic Stage-2 canonicalization over N=5 ensemble survivors.

Input  = ensemble_N5.json survivors + the 5 build dirs + spans.json (raw node text).
Output = runs/<run>/canonical/{registry,cio_consensus,am_canonical,merge_queue,canon_report}.json

Determinism contract:
  - candidate generation is pure rule / union-find / string, no randomness;
  - fuzzy intervention merges are decided ONLY by merge_decisions.json (a cache);
    a pair with no cached decision is NOT merged and is written to merge_queue.json;
  - tie-breaks are fixed: votes -> link count -> source_span order.
Run it twice on the same input (and same cache) => identical registry.
"""
import argparse
import collections
import json
import re
from pathlib import Path

STOP = {"the", "a", "an", "of", "to", "on", "in", "for", "with", "as", "we", "our",
        "is", "are", "be", "it", "this", "that", "and", "or", "by", "use", "using"}


def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def load_builds(run_dir, build_names):
    out = []
    for name in build_names:
        d = run_dir / "factors" / name
        out.append({
            "name": name,
            "cio": load_json(d / "cio_cards.json"),
            "am": load_json(d / "am_cards.json"),
            "links": load_json(d / "links.json"),
        })
    return out


def slugify(text, prefix, maxtok=6):
    toks = [t for t in re.findall(r"[a-zA-Z0-9]+", (text or "").lower()) if t not in STOP][:maxtok]
    return f"{prefix}_" + "_".join(toks) if toks else f"{prefix}_x"


def norm_tokens(text):
    return {t for t in re.findall(r"[a-zA-Z0-9]+", (text or "").lower()) if t not in STOP}


def tok_overlap(a, b):
    a, b = norm_tokens(a), norm_tokens(b)
    return len(a & b) / len(a | b) if (a | b) else 0.0


class UF:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        self.p[self.find(a)] = self.find(b)


def span_num(node_id):
    m = re.search(r"(\d+)", node_id or "")
    return int(m.group(1)) if m else 10**9


# ---------- Step B: AM canonical (deterministic; aliases + votes already judged) ----------
def canonical_am(builds, survivors_am, link_counts):
    uf = UF()
    text = {}
    for b in builds:
        for card in b["am"]:
            atoms = [card["node"]] + list(card.get("aliases") or [])
            for x in atoms:
                text.setdefault(x, card.get("gloss") or "")
            for x in atoms[1:]:
                uf.union(atoms[0], x)
    clusters = collections.defaultdict(list)
    for node in survivors_am:
        clusters[uf.find(node)].append(node)
    am_canon, raw2canon = {}, {}
    for members in clusters.values():
        rep = sorted(members, key=lambda n: (-survivors_am.get(n, 0),
                                             -link_counts.get(n, 0), span_num(n)))[0]
        kind = "assumption" if rep.startswith("A") else "mechanism"
        cid = slugify(text.get(rep, rep), "ASM" if kind == "assumption" else "MECH")
        am_canon[cid] = {"canonical_id": cid, "type": kind, "gloss": text.get(rep, ""),
                         "representative": rep, "members": sorted(members),
                         "votes": survivors_am.get(rep, 0)}
        for m in members:
            raw2canon[m] = cid
    return am_canon, raw2canon


# ---------- Step A: field-consensus CIO per surviving pattern ----------
def consensus_cio(builds, survivors_patterns, ctx_min):
    by_pat = collections.defaultdict(list)
    for b in builds:
        for c in b["cio"]:
            if c.get("pattern") in survivors_patterns:
                by_pat[c["pattern"]].append(c)

    def mode(vals):
        # a field is usually a str, but the model occasionally emits a list (e.g. two
        # eval_metrics); flatten those to their elements so the counter stays hashable and
        # the single most-used value wins.
        flat = []
        for v in vals:
            if isinstance(v, list):
                flat.extend(x for x in v if x)
            elif v:
                flat.append(v)
        return collections.Counter(flat).most_common(1)[0][0] if flat else None

    out = {}
    for pat, cards in by_pat.items():
        ctx_ctr = collections.Counter(x for c in cards for x in (c.get("context") or []))
        out[pat] = {
            "pattern": pat,
            "unit": mode([c.get("unit") for c in cards]),
            "intervention": mode([c.get("intervention") for c in cards]),
            "reference": mode([c.get("reference") for c in cards]),
            "eval_metric": mode([c.get("eval_metric") for c in cards]),
            "direction": mode([c.get("direction") for c in cards]),
            "pattern_class": mode([c.get("pattern_class") for c in cards]),
            "context": sorted([x for x, v in ctx_ctr.items() if v >= ctx_min]),
            "field_support": {"n_cards": len(cards)},
        }
    return out


# ---------- Step D: context facet classify + drop pure fragments ----------
FACET_RULES = [
    ("dataset", r"arc-?1|arc-?2|re-?arc"),
    ("model", r"vit|u-?net|\d+\s?m\b|param|width|depth"),
    ("training", r"test-?time|ttt|offline|scratch|augment"),
    ("eval", r"pass@|single-?view|multi-?view|accuracy|ensemble"),
]
DROP_RE = re.compile(r"modifies the one above|circle areas|denote|entries?\s*\(", re.I)


def canonical_context(consensus, byspan):
    ctx_canon, raw2canon, dropped = {}, {}, []
    seen = {c for cc in consensus.values() for c in cc["context"]}
    for cid in sorted(seen):
        text = byspan.get(cid, {}).get("text", "")
        if DROP_RE.search(text):
            dropped.append(cid)
            continue
        facet = next((f for f, rx in FACET_RULES if re.search(rx, text, re.I)), "other")
        canon = slugify(text, f"CTX_{facet}")
        ctx_canon.setdefault(canon, {"canonical_id": canon, "type": "context",
                                     "facet": facet, "gloss": text[:80], "members": []})
        ctx_canon[canon]["members"].append(cid)
        raw2canon[cid] = canon
    return ctx_canon, raw2canon, dropped


# ---------- Step C: intervention / reference (rule + cached confirm) ----------
def canonical_intervention(consensus, byspan, cache, merge_queue):
    ids = {cc["intervention"] for cc in consensus.values() if cc.get("intervention")}
    ids |= {cc["reference"] for cc in consensus.values() if cc.get("reference")}
    ids = sorted(i for i in ids if i)
    uf = UF()
    for i in ids:
        uf.find(i)
    for a in ids:
        for b in ids:
            if a >= b:
                continue
            ta, tb = byspan.get(a, {}).get("text", ""), byspan.get(b, {}).get("text", "")
            ov = tok_overlap(ta, tb)
            if norm_tokens(ta) == norm_tokens(tb):
                uf.union(a, b)
            elif ov >= 0.6:
                key = "|".join(sorted([a, b]))
                if cache.get(key) == "yes":
                    uf.union(a, b)
                elif key not in cache:
                    merge_queue.append({"pair": [a, b], "overlap": round(ov, 2),
                                        "a": ta[:80], "b": tb[:80]})
    clusters = collections.defaultdict(list)
    for i in ids:
        clusters[uf.find(i)].append(i)
    canon, raw2canon = {}, {}
    for members in clusters.values():
        rep = sorted(members, key=span_num)[0]
        cid = slugify(byspan.get(rep, {}).get("text", rep), "INT")
        canon[cid] = {"canonical_id": cid, "type": "intervention",
                      "gloss": byspan.get(rep, {}).get("text", "")[:80], "members": sorted(members)}
        for m in members:
            raw2canon[m] = cid
    return canon, raw2canon


# ---------- Step E: eval_metric first-pass grouping ----------
def canonical_metric(consensus, byspan):
    ids = sorted({cc["eval_metric"] for cc in consensus.values() if cc.get("eval_metric")})
    canon, raw2canon = {}, {}
    for e in ids:
        text = byspan.get(e, {}).get("text", "").lower()
        evalset = "arc2" if ("arc-2" in text or "arc2" in text) else "arc1" if "arc" in text else "gen"
        metric = "passk" if "pass@" in text else "accuracy"
        cid = f"MET_{evalset}_{metric}"
        canon.setdefault(cid, {"canonical_id": cid, "type": "eval_metric", "members": []})
        canon[cid]["members"].append(e)
        raw2canon[e] = cid
    return canon, raw2canon


# ---------- link re-measure on canonical AM ----------
def link_jaccard_canonical(builds, raw2canon_am):
    import itertools
    sets = []
    for b in builds:
        amc = {c["am_id"]: [c["node"]] + list(c.get("aliases") or []) for c in b["am"]}
        pat = {c["cio_id"]: c.get("pattern") for c in b["cio"]}
        s = set()
        for e in b["links"]:
            p = pat.get(e.get("source_cio"))
            for atom in amc.get(e.get("target_am"), []):
                cc = raw2canon_am.get(atom)
                if p and cc:
                    s.add((p, cc, e.get("direction")))
        sets.append(s)
    vals = [len(a & b) / len(a | b) for a, b in itertools.combinations(sets, 2) if (a | b)]
    return round(sum(vals) / len(vals), 3) if vals else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--ensemble", default=None, help="default run-dir/ensemble/ensemble_N5.json")
    ap.add_argument("--ctx-min", type=int, default=3, help="context kept if in >= this many builds")
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    ens = load_json(args.ensemble or run_dir / "ensemble" / "ensemble_N5.json")
    builds = load_builds(run_dir, ens["builds"])
    spans = load_json(run_dir / "spans.json")
    byspan = {s["node_id"]: s for s in spans}

    out_dir = run_dir / "canonical"
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_path = out_dir / "merge_decisions.json"
    cache = load_json(cache_path) if cache_path.exists() else {}

    survivors_pat = set(ens["accepted"]["cio_patterns"])
    survivors_am = {k: v["votes"] for k, v in ens["accepted"]["am_nodes"].items()}
    link_counts = collections.Counter()
    for k in ens["accepted"]["links"]:
        link_counts[k.split("|")[1]] += 1

    cio_cons = consensus_cio(builds, survivors_pat, args.ctx_min)
    am_canon, r2c_am = canonical_am(builds, survivors_am, link_counts)
    merge_queue = []
    int_canon, r2c_int = canonical_intervention(cio_cons, byspan, cache, merge_queue)
    ctx_canon, r2c_ctx, dropped = canonical_context(cio_cons, byspan)
    met_canon, r2c_met = canonical_metric(cio_cons, byspan)

    for pat, c in cio_cons.items():
        c["canonical"] = {
            "context": [r2c_ctx.get(x, x) for x in c["context"] if x not in dropped],
            "intervention": r2c_int.get(c.get("intervention")),
            "reference": r2c_int.get(c.get("reference")),
            "eval_metric": r2c_met.get(c.get("eval_metric")),
            "observable": [r2c_met.get(c.get("eval_metric")), c.get("direction")],
        }

    registry = {"context": ctx_canon, "intervention": int_canon,
                "eval_metric": met_canon, "am": am_canon,
                "raw2canon": {**r2c_ctx, **r2c_int, **r2c_met, **r2c_am}}
    report = {
        "n_builds": len(builds),
        "before": {
            "context": len({x for cc in cio_cons.values() for x in cc["context"]}),
            "intervention": len({cc.get("intervention") for cc in cio_cons.values() if cc.get("intervention")}),
            "eval_metric": len({cc.get("eval_metric") for cc in cio_cons.values() if cc.get("eval_metric")}),
            "am_survivors": len(survivors_am),
        },
        "after": {"context": len(ctx_canon), "intervention": len(int_canon),
                  "eval_metric": len(met_canon), "am_clusters": len(am_canon)},
        "context_dropped": len(dropped),
        "merge_queue_pending": len(merge_queue),
        "link_jaccard_raw_baseline": ens["reproducibility_mean_pairwise_jaccard"].get("link_atomic"),
        "link_jaccard_on_canonical_am": link_jaccard_canonical(builds, r2c_am),
    }

    (out_dir / "cio_consensus.json").write_text(json.dumps(cio_cons, indent=2, ensure_ascii=False))
    (out_dir / "am_canonical.json").write_text(json.dumps(am_canon, indent=2, ensure_ascii=False))
    (out_dir / "registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=False))
    (out_dir / "merge_queue.json").write_text(json.dumps(merge_queue, indent=2, ensure_ascii=False))
    (out_dir / "canon_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    if not cache_path.exists():
        cache_path.write_text(json.dumps(cache, indent=2, ensure_ascii=False))

    print(json.dumps(report, indent=2, ensure_ascii=False))
    if merge_queue:
        print(f"\n{len(merge_queue)} fuzzy intervention pairs need a decision -> merge_queue.json")
        print('resolve them in merge_decisions.json as {"<idA>|<idB>": "yes"|"no"} and re-run.')


if __name__ == "__main__":
    main()
