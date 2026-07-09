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

STATUS_MIN_BUILDS = 2   # link Jaccard ~0.29, so a 1-build belief edge is noise. An edge only counts
                        # toward tested/contested if it recurs in >= this many builds. 'assumed' is
                        # judged separately on ref_count==0 (a true orphan), per the "narrow" choice.


def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def load_builds(builds_dir, build_names):
    out = []
    for name in build_names:
        d = builds_dir / name
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


def band(conf):
    """View-level confidence band (mirror of aggregate_ensemble.band). Nothing is dropped."""
    if conf >= 0.8:
        return "observed"
    if conf >= 0.4:
        return "supported"
    return "uncertain"


# ---------- Step B: AM canonical (union clustering; merge-then-count confidence) ----------
def canonical_am(builds, am_votes, link_counts, n):
    """Cluster EVERY AM atom (union, no vote filter). A cluster's confidence is recomputed
    merge-then-count: how many of the N builds contained ANY of the cluster's member atoms --
    so a concept scattered across builds under different aliases regains its true support."""
    uf = UF()
    text = {}
    build_atoms = []
    for b in builds:
        present = set()
        for card in b["am"]:
            atoms = [card["node"]] + list(card.get("aliases") or [])
            present.update(a for a in atoms if a)
            for x in atoms:
                text.setdefault(x, card.get("gloss") or "")
            for x in atoms[1:]:
                uf.union(atoms[0], x)
        build_atoms.append(present)
    clusters = collections.defaultdict(list)
    for node in am_votes:
        clusters[uf.find(node)].append(node)
    am_canon, raw2canon = {}, {}
    for members in clusters.values():
        rep = sorted(members, key=lambda x: (-am_votes.get(x, 0),
                                             -link_counts.get(x, 0), span_num(x)))[0]
        kind = "assumption" if rep.startswith("A") else "mechanism"
        cid = slugify(text.get(rep, rep), "ASM" if kind == "assumption" else "MECH")
        mset = set(members)
        cluster_votes = sum(1 for present in build_atoms if present & mset)
        conf = round(cluster_votes / n, 3)
        am_canon[cid] = {"canonical_id": cid, "type": kind, "gloss": text.get(rep, ""),
                         "representative": rep, "members": sorted(members), "n_members": len(members),
                         "votes": cluster_votes, "confidence": conf, "band": band(conf)}
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
            "provenance": {"location": mode([(c.get("provenance") or {}).get("location") for c in cards])},
            "field_support": {"n_cards": len(cards)},
        }
    return out


# ---------- Phase A': field category discipline WITHOUT discarding info ----------
FIELD_PREFIX = {
    "intervention": ("I",),        # an intervention id only
    "reference":    ("I", "C"),    # baseline arm: another intervention, or a contrasting context
    "eval_metric":  ("E",),        # a metric id only
}
# verbs that betray a real manipulation that Layer-1 mislabeled as context/metric
MANIP_RE = re.compile(
    r"\b(vary|varying|ablat|ensembl|scal|swap|replace|remov|add|combin|"
    r"increase|decrease|with vs|independent|joint|augment)\w*", re.I)

# Generic category hygiene (NOT VARC-figure-specific): a node LABELED eval_metric that names a
# comparison TARGET / CONDITION (ground truth, correct/reference/target output) and carries NO
# metric keyword is not a measurement — it is a context/condition, so it may legally sit in a
# reference or context slot (both accept a C-node). Deliberately narrow: pass@k protocols,
# scaling axes, and everything else keep their eval_metric label.
CONDITION_RE = re.compile(r"ground[\s-]*truth|correct output|reference output|target output", re.I)
METRIC_KW = re.compile(r"accuracy|acc\.|pass\s*@|\bscore\b|\brate\b|%|\bloss\b|\berror\b|\bf1\b|\bauc\b", re.I)


def eval_reads_as_context(nid, byspan):
    if not str(nid).startswith("E"):
        return False
    s = byspan.get(nid, {})
    blob = f"{s.get('text','')} {s.get('note','')}"
    return bool(CONDITION_RE.search(blob)) and not METRIC_KW.search(blob)


def validate_cio_fields(consensus, byspan):
    """Enforce field-prefix discipline on each surviving CIO card. A violating value is NOT
    deleted: it is stashed in card['field_mismatch'][field] with its Layer-1 label + text, and
    the working slot is cleared to None so the graph never builds a wrong-category edge.
    promote_mislabeled_intervention() can pull genuine-but-mislabeled ones back."""
    errors = []
    for pat, c in consensus.items():
        mism = {}
        for field, allowed in FIELD_PREFIX.items():
            v = c.get(field)
            if v and not str(v).startswith(allowed) and not ("C" in allowed and eval_reads_as_context(v, byspan)):
                s = byspan.get(v, {})
                mism[field] = {"raw": v, "layer1_label": s.get("assigned_label"),
                               "text": s.get("text", "")}
                c[field] = None
                errors.append({"pattern": pat, "field": field, "bad_value": v,
                               "layer1_label": s.get("assigned_label"),
                               "text": (s.get("text") or "")[:100]})
        ctx = c.get("context") or []
        bad = [x for x in ctx if not (str(x).startswith("C") or eval_reads_as_context(x, byspan))]
        if bad:
            mism["context"] = [{"raw": x, "layer1_label": byspan.get(x, {}).get("assigned_label"),
                                "text": byspan.get(x, {}).get("text", "")} for x in bad]
            c["context"] = [x for x in ctx if str(x).startswith("C")]
            errors.append({"pattern": pat, "field": "context", "bad_value": bad})
        if not str(c.get("pattern") or "").startswith("P"):
            errors.append({"pattern": pat, "field": "pattern", "bad_value": c.get("pattern"),
                           "note": "anchor not a P-id"})
        if mism:
            c["field_mismatch"] = mism
    return errors


def promote_mislabeled_intervention(consensus, byspan):
    """A value stashed in field_mismatch['intervention'] that came from a context/metric node but
    reads like a real manipulation (MANIP_RE) is promoted back into the empty intervention slot.
    The raw id is kept (still C../E..) and tagged 'promoted' so provenance stays honest."""
    promoted = []
    for pat, c in consensus.items():
        mm = (c.get("field_mismatch") or {}).get("intervention")
        if not mm or c.get("intervention"):
            continue
        if MANIP_RE.search(mm.get("text", "")):
            c["intervention"] = mm["raw"]
            c.setdefault("promoted", {})["intervention"] = mm["raw"]
            promoted.append({"pattern": pat, "node": mm["raw"],
                             "layer1_label": mm.get("layer1_label"), "text": mm.get("text", "")[:90]})
    return promoted


# ---------- Step D: context facet classify + drop pure fragments ----------
FACET_RULES = [
    ("dataset", r"arc-?1|arc-?2|re-?arc"),
    ("model", r"vit|u-?net|\d+\s?m\b|param|width|depth"),
    ("training", r"test-?time|ttt|offline|scratch|augment"),
    ("eval", r"pass@|single-?view|multi-?view|accuracy|ensemble"),
]
DROP_RE = re.compile(r"modifies the one above|circle areas|denote|entries?\s*\(", re.I)


def spec_sig(note):
    """A context node's distinguishing spec (width / #params / Gflops ...) usually lives in
    `note`, not `text`: text="ViT", note="width 512, 18M". Merging on text alone collapses
    ViT-6M/18M/66M into one node. This returns the note's numeric tokens joined, so nodes that
    share text but differ in ANY spec number stay SEPARATE. Empty note -> "" -> text-only merge
    (true duplicate contexts, e.g. two bare "ARC-1", still merge as before)."""
    nums = [t for t in re.findall(r"[a-z0-9]+", (note or "").lower()) if any(ch.isdigit() for ch in t)]
    return "_".join(nums)


def canonical_context(consensus, byspan):
    """Cluster context C-nodes by facet + text slug, BUT keep spec-distinct nodes apart via
    spec_sig(note): ViT-6M/18M/66M -> three canonical contexts instead of one. Nodes with no
    distinguishing spec (empty note) still merge on text. Pure layout fragments (DROP_RE) are
    dropped. Deterministic: no LLM, no randomness."""
    ctx_canon, raw2canon, dropped = {}, {}, []
    seen = {c for cc in consensus.values() for c in cc["context"]}
    for cid in sorted(seen):
        s = byspan.get(cid, {})
        text = s.get("text", "")
        note = s.get("note", "") or ""
        if DROP_RE.search(text):
            dropped.append(cid)
            continue
        facet = next((f for f, rx in FACET_RULES if re.search(rx, text, re.I)), "other")
        base = slugify(text, f"CTX_{facet}")
        sig = spec_sig(note)
        canon = f"{base}_{sig}" if sig else base            # spec-distinct -> distinct canonical id
        gloss = (text + (f" — {note}" if note else "")).strip()[:80]
        ctx_canon.setdefault(canon, {"canonical_id": canon, "type": "context",
                                     "facet": facet, "gloss": gloss, "members": []})
        ctx_canon[canon]["members"].append(cid)
        raw2canon[cid] = canon
    for rec in ctx_canon.values():
        rec["members"] = sorted(rec["members"])
        rec["representative"] = sorted(rec["members"], key=span_num)[0]
        rec["n_members"] = len(rec["members"])
    return ctx_canon, raw2canon, dropped


# ---------- Step C: intervention / reference (rule + cached confirm) ----------
CAND_OVERLAP = 0.4   # was 0.6 — lower so more near-dupes reach the LLM judge (recall up); only an
                     # EXACT token-set match still auto-merges without asking. Non-exact pairs at
                     # or above this go to merge_queue -> canon_pair_judge decides yes/no (cached).


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
                uf.union(a, b)                       # exact token-set match: deterministic auto-merge
            elif ov >= CAND_OVERLAP:
                key = "|".join(sorted([a, b]))
                decision = cache.get(key)
                if decision == "yes":
                    uf.union(a, b)                   # judged same (cached)
                elif decision == "no":
                    pass                             # judged different (cached) -> keep split
                else:
                    merge_queue.append({"pair": [a, b], "overlap": round(ov, 2),
                                        "a": ta[:240], "b": tb[:240]})   # -> canon_pair_judge
    clusters = collections.defaultdict(list)
    for i in ids:
        clusters[uf.find(i)].append(i)
    canon, raw2canon = {}, {}
    for members in clusters.values():
        rep = sorted(members, key=span_num)[0]
        cid = slugify(byspan.get(rep, {}).get("text", rep), "INT")
        canon[cid] = {"canonical_id": cid, "type": "intervention",
                      "gloss": byspan.get(rep, {}).get("text", "")[:80],
                      "representative": rep, "members": sorted(members), "n_members": len(members)}
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
        m = re.search(r"pass\s*@?\s*(\d+)", text)
        if m:
            metric = f"pass{m.group(1)}"            # keep pass@1 vs pass@2 distinct (headline is pass@2)
        elif "pass@" in text:
            metric = "passk"
        elif "loss" in text or "cross-entropy" in text or "cross entropy" in text:
            metric = "loss"                         # a loss is not an accuracy -- do not merge them
        else:
            metric = "accuracy"
        cid = f"MET_{evalset}_{metric}"
        canon.setdefault(cid, {"canonical_id": cid, "type": "eval_metric", "members": []})
        canon[cid]["members"].append(e)
        raw2canon[e] = cid
    for rec in canon.values():
        rec["members"] = sorted(rec["members"])
        rec["representative"] = sorted(rec["members"], key=span_num)[0]
        rec["n_members"] = len(rec["members"])
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


def derive_am_status(rec, edges, min_builds):
    """Deterministic belief status for one canonical AM node (no LLM). `edges` maps
    (pattern_id, direction) -> set of build names that produced it, so an edge only counts once it
    recurs in >= min_builds builds. Status ladder:
      assumed        ref_count == 0 — a genuine orphan asserted with no observation -> propose_test
      contested      >=1 reproduced weaken edge — the paper's own results push back
      tested         >=1 reproduced strengthen edge AND an 'observed' confidence band
      weakly-tested  has edges, but none reproduce enough / band too low to call it tested
    strengthened_by / weakened_by carry the pattern ids so the status stays auditable."""
    strengthen = sorted({p for (p, d), bs in edges.items()
                         if d == "strengthen" and len(bs) >= min_builds})
    weaken = sorted({p for (p, d), bs in edges.items()
                     if d == "weaken" and len(bs) >= min_builds})
    if rec.get("ref_count", 0) == 0:
        return "assumed", strengthen, weaken, True
    if weaken:
        return "contested", strengthen, weaken, False
    if strengthen and rec.get("band") == "observed":
        return "tested", strengthen, weaken, False
    return "weakly-tested", strengthen, weaken, False


# --- AM ontology v0.1 typing (docs/am-ontology-v0.1/2026-07-09-am-ontology-migration-spec.md) ---
# §1 GENERAL rules live here as paper-agnostic code. §2 VARC-tuned assignments come from a
# per-paper overrides file (run-dir/am_ontology_overrides.json), so no paper-specific string leaks
# into the system core. link_policy is derived deterministically from ontology_type.
OBS_LEAKY_RE = re.compile(r"\b(shows?|reveal(?:s|ed)?|suggests?|visuali[sz]ation|illustrat)", re.I)
ONTOLOGY_LINK_POLICY = {
    "mechanism": "direct_link_allowed", "aggregate_claim": "direct_link_allowed",
    "paper_thesis": "rolls_up_only",
    "assumption": "qualifier_only", "scope_condition": "qualifier_only",
    "precondition": "qualifier_only", "limitation": "qualifier_only",
    "qualitative_observation": "no_direct_link",
}


def general_ontology_type(gloss, kind):
    """Paper-agnostic ontology_type (spec §1): an observation-leaky belief
    ('shows/reveals/suggests/visualization') is really a qualitative observation; an L1 assumption
    defaults to a QualifierCard; everything else is a mechanism. paper_thesis / scope_condition /
    limitation / aggregate_claim are paper-specific and arrive via per-paper overrides (§2)."""
    if OBS_LEAKY_RE.search(gloss or ""):
        return "qualitative_observation"
    if kind == "assumption":
        return "assumption"
    return "mechanism"


def assign_ontology_types(am_canon, overrides):
    """Attach ontology_type + link_policy to every canonical AM. General rule first, then the
    per-paper overrides — keyed by GLOSS substring (a canonical_id is per-cohort, a gloss is
    stable), mapping {ontology_type: [gloss substrings]}."""
    for rec in am_canon.values():
        rec["ontology_type"] = general_ontology_type(rec.get("gloss"), rec.get("type"))
    for otype, subs in (overrides or {}).items():
        if otype.startswith("_") or not isinstance(subs, list):
            continue                                 # skip config metadata (e.g. "_note")
        for rec in am_canon.values():
            g = (rec.get("gloss") or "").lower()
            if any(str(s).lower() in g for s in subs):
                rec["ontology_type"] = otype
    for rec in am_canon.values():
        ot = rec["ontology_type"]
        if ot not in ONTOLOGY_LINK_POLICY:           # fail-fast: an override typo must not silently fall to direct
            raise ValueError(f"unknown ontology_type {ot!r} for {rec.get('canonical_id')} "
                             f"(override typo?); known: {sorted(ONTOLOGY_LINK_POLICY)}")
        rec["link_policy"] = ONTOLOGY_LINK_POLICY[ot]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--ensemble", default=None, help="default run-dir/ensemble/ensemble_N5.json")
    ap.add_argument("--builds-dir", default=None,
                    help="directory holding the build folders named in the ensemble (default: <run-dir>/factors)")
    ap.add_argument("--out-dir", default=None, help="where to write canonical/ output (default: <run-dir>/canonical)")
    ap.add_argument("--ctx-min", type=int, default=3, help="context kept if in >= this many builds")
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    ens = load_json(args.ensemble or run_dir / "ensemble" / "ensemble_N5.json")
    builds_dir = Path(args.builds_dir) if args.builds_dir else run_dir / "factors"
    builds = load_builds(builds_dir, ens["builds"])
    spans = load_json(run_dir / "spans.json")
    byspan = {s["node_id"]: s for s in spans}

    out_dir = Path(args.out_dir) if args.out_dir else run_dir / "canonical"
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_path = out_dir / "merge_decisions.json"
    cache = load_json(cache_path) if cache_path.exists() else {}

    # KEEP-ALL union: canonicalize EVERY node seen in >=1 build, not just vote-survivors.
    n = len(builds)
    all_pat = set(ens["nodes"]["cio_patterns"])
    am_votes = {k: v["votes"] for k, v in ens["nodes"]["am_nodes"].items()}
    link_counts = collections.Counter()
    for k in ens["nodes"]["links"]:
        link_counts[k.split("|")[1]] += 1

    cio_cons = consensus_cio(builds, all_pat, args.ctx_min)
    field_errors = validate_cio_fields(cio_cons, byspan)                 # Phase A'
    promoted = promote_mislabeled_intervention(cio_cons, byspan)         # Phase C-1
    am_canon, r2c_am = canonical_am(builds, am_votes, link_counts, n)
    merge_queue = []
    int_canon, r2c_int = canonical_intervention(cio_cons, byspan, cache, merge_queue)
    ctx_canon, r2c_ctx, dropped = canonical_context(cio_cons, byspan)
    met_canon, r2c_met = canonical_metric(cio_cons, byspan)

    for pat, c in cio_cons.items():
        c["canonical"] = {
            "context": sorted(set(r2c_ctx.get(x, x) for x in c["context"] if x not in dropped)),
            "intervention": r2c_int.get(c.get("intervention")),
            "reference": r2c_int.get(c.get("reference")),
            "eval_metric": r2c_met.get(c.get("eval_metric")),
            "observable": [r2c_met.get(c.get("eval_metric")), c.get("direction")],
        }

    registry = {"context": ctx_canon, "intervention": int_canon,
                "eval_metric": met_canon, "am": am_canon,
                "raw2canon": {**r2c_ctx, **r2c_int, **r2c_met, **r2c_am}}

    # reverse index: which surviving patterns reference each canonical node. CIO-layer nodes
    # (context/intervention/eval_metric) are referenced by card slots; AM clusters by belief
    # links. ref_count surfaces hub concepts (the interventions/metrics many factors lean on).
    ref_index = collections.defaultdict(set)
    for pat, c in cio_cons.items():
        cn = c.get("canonical", {})
        for cc in (cn.get("context") or []):
            ref_index[cc].add(pat)
        for slot in ("intervention", "reference", "eval_metric"):
            if cn.get(slot):
                ref_index[cn[slot]].add(pat)
    for b in builds:
        pat_of = {c["cio_id"]: c.get("pattern") for c in b["cio"]}
        amc = {c["am_id"]: [c["node"]] + list(c.get("aliases") or []) for c in b["am"]}
        for e in b["links"]:
            p = pat_of.get(e.get("source_cio"))
            if not p or p not in cio_cons:
                continue
            for atom in amc.get(e.get("target_am"), []):
                cc = r2c_am.get(atom)
                if cc:
                    ref_index[cc].add(p)
    for kind in ("context", "intervention", "eval_metric", "am"):
        for cid, rec in registry[kind].items():
            rec["referenced_by"] = sorted(ref_index.get(cid, []))
            rec["ref_count"] = len(rec["referenced_by"])

    # ---- C1: deterministic belief status per canonical AM (no LLM). Collect each cluster's
    # (pattern, direction) belief edges with the set of builds that produced them, so status can
    # require build reproducibility (see derive_am_status). ref_count (set above) drives 'assumed'.
    am_edges = collections.defaultdict(lambda: collections.defaultdict(set))
    for b in builds:
        pat_of = {c["cio_id"]: c.get("pattern") for c in b["cio"]}
        amc = {c["am_id"]: [c["node"]] + list(c.get("aliases") or []) for c in b["am"]}
        for e in b["links"]:
            p = pat_of.get(e.get("source_cio"))
            if not p or p not in cio_cons:
                continue
            d = e.get("direction")
            for atom in amc.get(e.get("target_am"), []):
                cid = r2c_am.get(atom)
                if cid in am_canon:
                    am_edges[cid][(p, d)].add(b["name"])
    # AM ontology v0.1 typing FIRST (general rules code §1 + per-paper overrides config §2), so the
    # belief-edge routing below can gate each edge on its target's link_policy.
    onto_path = run_dir / "am_ontology_overrides.json"
    assign_ontology_types(am_canon, load_json(onto_path) if onto_path.exists() else {})

    # ---- L2: enforce link_policy on belief edges (migration spec §3 + §4 success criteria). A direct
    # belief_update (strengthen/weaken) may target a direct_link_allowed AM (mechanism | aggregate_claim)
    # ONLY. Edges whose target is a paper_thesis / qualifier / demoted observation are re-routed to
    # explicit buckets (rolls_up / qualifier / demoted) so the direct graph carries only genuine
    # Observation->mechanism belief; strengthened_by/weakened_by stay empty for non-direct targets. The
    # STATUS_MIN_BUILDS reproducibility gate is applied uniformly, so every reported edge recurs. No LLM.
    POLICY_BUCKET = {"rolls_up_only": "rolls_up", "qualifier_only": "qualifier", "no_direct_link": "demoted"}
    POLICY_EDGE = {"rolls_up": "rolls_up", "qualifier": "qualifies", "demoted": "demoted"}
    POLICY_STATUS = {"rolls_up_only": "rollup_target", "qualifier_only": "qualifier",
                     "no_direct_link": "demoted_observation"}
    belief_edges = {"direct": [], "rolls_up": [], "qualifier": [], "demoted": []}
    for cid, rec in am_canon.items():
        edges = am_edges.get(cid, {})
        repro = {(p, d): len(bs) for (p, d), bs in edges.items() if len(bs) >= STATUS_MIN_BUILDS}
        if rec["link_policy"] == "direct_link_allowed":
            st, s_obs, w_obs, propose = derive_am_status(rec, edges, STATUS_MIN_BUILDS)
            rec["status"], rec["strengthened_by"], rec["weakened_by"], rec["propose_test"] = st, s_obs, w_obs, propose
            rec["unobserved_qualifier"] = False          # a direct claim is a propose_test target, not a qualifier
            for (p, d), nb in repro.items():
                belief_edges["direct"].append({"observation": p, "target": cid, "direction": d,
                                               "edge_type": d, "n_builds": nb})
        else:                                            # policy forbids direct belief edges -> reroute
            st, _, _, _ = derive_am_status(rec, {}, STATUS_MIN_BUILDS)  # orphan/'assumed' logic still applies
            rec["status"] = st if rec.get("ref_count", 0) == 0 else POLICY_STATUS[rec["link_policy"]]
            rec["strengthened_by"], rec["weakened_by"], rec["propose_test"] = [], [], False
            # an unobserved qualifier (assumption/scope/limitation with no observation) is flagged separately;
            # it is NOT a propose_test target — that differentiator is for untested direct claims/mechanisms.
            rec["unobserved_qualifier"] = rec["link_policy"] == "qualifier_only" and rec.get("ref_count", 0) == 0
            bucket = POLICY_BUCKET[rec["link_policy"]]
            for (p, d), nb in repro.items():
                belief_edges[bucket].append({"observation": p, "target": cid, "direction": d,
                                             "edge_type": POLICY_EDGE[bucket], "n_builds": nb})
    for k in belief_edges:
        belief_edges[k].sort(key=lambda e: (e["target"], e["observation"], e["direction"]))
    # success criteria (spec §4): direct edges only to direct_link_allowed AMs; paper_thesis direct = 0.
    assert all(am_canon[e["target"]]["link_policy"] == "direct_link_allowed" for e in belief_edges["direct"]), \
        "link_policy violation: a direct belief edge targets a non-direct AM"
    thesis_direct = sum(1 for e in belief_edges["direct"]
                        if am_canon[e["target"]]["ontology_type"] == "paper_thesis")
    assert thesis_direct == 0, f"paper_thesis direct edges must be 0, got {thesis_direct}"

    am_band = collections.Counter(v["band"] for v in am_canon.values())
    report = {
        "n_builds": n,
        "before": {
            "context": len({x for cc in cio_cons.values() for x in cc["context"]}),
            "intervention": len({cc.get("intervention") for cc in cio_cons.values() if cc.get("intervention")}),
            "eval_metric": len({cc.get("eval_metric") for cc in cio_cons.values() if cc.get("eval_metric")}),
            "am_atoms_union": len(am_votes),
        },
        "after": {"context": len(ctx_canon), "intervention": len(int_canon),
                  "eval_metric": len(met_canon), "am_clusters": len(am_canon)},
        "am_cluster_bands": {b: am_band.get(b, 0) for b in ("observed", "supported", "uncertain")},
        "am_status": dict(collections.Counter(v["status"] for v in am_canon.values())),
        "am_ontology_types": dict(collections.Counter(v.get("ontology_type") for v in am_canon.values())),
        "am_link_policies": dict(collections.Counter(v.get("link_policy") for v in am_canon.values())),
        "belief_edges_by_policy": {k: len(v) for k, v in belief_edges.items()},
        "propose_test_direct_claims": sorted(cid for cid, v in am_canon.items() if v.get("propose_test")),
        "unobserved_qualifiers": sorted(cid for cid, v in am_canon.items() if v.get("unobserved_qualifier")),
        "context_dropped": len(dropped),
        "merge_queue_pending": len(merge_queue),
        "cio_field_errors": len(field_errors),
        "promoted_interventions": len(promoted),
        "link_jaccard_raw_baseline": ens["reproducibility_mean_pairwise_jaccard"].get("link_atomic"),
        "link_jaccard_on_canonical_am": link_jaccard_canonical(builds, r2c_am),
    }

    (out_dir / "cio_consensus.json").write_text(json.dumps(cio_cons, indent=2, ensure_ascii=False))
    (out_dir / "am_canonical.json").write_text(json.dumps(am_canon, indent=2, ensure_ascii=False))
    (out_dir / "belief_edges.json").write_text(json.dumps(belief_edges, indent=2, ensure_ascii=False))
    (out_dir / "registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=False))
    (out_dir / "merge_queue.json").write_text(json.dumps(merge_queue, indent=2, ensure_ascii=False))
    (out_dir / "cio_field_errors.json").write_text(json.dumps(field_errors, indent=2, ensure_ascii=False))
    (out_dir / "promoted_interventions.json").write_text(json.dumps(promoted, indent=2, ensure_ascii=False))
    (out_dir / "canon_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    if not cache_path.exists():
        cache_path.write_text(json.dumps(cache, indent=2, ensure_ascii=False))

    print(json.dumps(report, indent=2, ensure_ascii=False))
    if merge_queue:
        print(f"\n{len(merge_queue)} fuzzy intervention pairs need a decision -> merge_queue.json")
        print('resolve them in merge_decisions.json as {"<idA>|<idB>": "yes"|"no"} and re-run.')


if __name__ == "__main__":
    main()
