"""Deterministic tests for the claim-graph builder (migration spec §3). No LLM, no cohort I/O — pure
fixtures. Covers the fail-fast cases the reviewer flagged (zero-match / duplicate / id-collision /
thesis-cardinality / bad-rollup) and the exact VARC P-ID re-routing + P24/P25 preservation.
Run: .venv/bin/python test_claim_graph.py    (exit 0 = pass, 1 = fail)"""
import collections
from canonicalize_v0 import build_claim_graph


def fresh():
    """Tiny canonical graph: 1 thesis, 2 mechanisms; MECH_a holds P20-P23/P26, MECH_b holds P24/P25."""
    am = {
        "THESIS": {"canonical_id": "THESIS", "ontology_type": "paper_thesis",
                   "link_policy": "rolls_up_only", "gloss": "t", "ref_count": 0},
        "MECH_a": {"canonical_id": "MECH_a", "ontology_type": "mechanism",
                   "link_policy": "direct_link_allowed", "gloss": "a", "ref_count": 5},
        "MECH_b": {"canonical_id": "MECH_b", "ontology_type": "mechanism",
                   "link_policy": "direct_link_allowed", "gloss": "b", "ref_count": 2},
    }
    edges = collections.defaultdict(lambda: collections.defaultdict(set))
    for p in ("P20", "P22", "P26", "P21", "P23"):
        edges["MECH_a"][(p, "strengthen")] = {"b1", "b2"}
    for p in ("P24", "P25"):
        edges["MECH_b"][(p, "strengthen")] = {"b1", "b2"}
    return am, edges


CFG_OK = {
    "aggregate_claims": [
        {"id": "AGG_v", "gloss": "vision", "observation_ids": ["P20", "P22", "P26"]},
        {"id": "AGG_c", "gloss": "canvas", "observation_ids": ["P21", "P23"]},
    ],
    "claims_roll_up_to_thesis": ["MECH_a", "MECH_b", "AGG_v", "AGG_c"],
    "reported_as_main_result_observations": ["P99"],
}

results = []


def check(cond, msg):
    results.append(None if cond else f"FAIL: {msg}")


def expect_error(fn, needle):
    try:
        fn()
        return f"FAIL: expected ValueError containing {needle!r}, none raised"
    except ValueError as e:
        return None if needle in str(e) else f"FAIL: wrong ValueError for {needle!r}: {e}"
    except Exception as e:                                # noqa: BLE001 — any non-ValueError is a failure
        return f"FAIL: non-ValueError for {needle!r}: {type(e).__name__}: {e}"


# --- happy path: exact re-routing + preservation + schema ---
am, edges = fresh()
rolls, main_obs, tid = build_claim_graph(am, edges, CFG_OK)
check(tid == "THESIS", "resolves the single thesis")
check(set(edges["AGG_v"]) == {("P20", "strengthen"), ("P22", "strengthen"), ("P26", "strengthen")},
      "AGG_v absorbs exactly P20/P22/P26")
check(set(edges["AGG_c"]) == {("P21", "strengthen"), ("P23", "strengthen")},
      "AGG_c absorbs exactly P21/P23")
check(set(edges["MECH_b"]) == {("P24", "strengthen"), ("P25", "strengthen")},
      "P24/P25 preserved on MECH_b (NOT aggregated)")
check(not any(p in ("P20", "P21", "P22", "P23", "P26") for (p, d) in edges["MECH_a"]),
      "MECH_a lost every re-routed pattern")
check(am["AGG_v"]["n_members"] == 0 and am["AGG_v"]["members"] == [],
      "aggregate keeps schema invariant n_members == len(members) == 0")
check(am["AGG_v"]["n_supporting_observations"] == 3, "AGG_v n_supporting_observations == 3")
check(am["AGG_v"]["ontology_type"] == "aggregate_claim" and am["AGG_v"]["link_policy"] == "direct_link_allowed",
      "aggregate typed as aggregate_claim / direct")
check(main_obs == {"P99"}, "main_result audit set passes through")
check(len(rolls) == 4 and all(t == "THESIS" for _, t in rolls), "4 claims roll up to the thesis")

# --- fail-fast cases (reviewer-flagged silent failures) ---
def dup():
    am, e = fresh()
    build_claim_graph(am, e, {"aggregate_claims": [
        {"id": "AGG_v", "gloss": "v", "observation_ids": ["P20", "P22"]},
        {"id": "AGG_c", "gloss": "c", "observation_ids": ["P22", "P23"]}]})
results.append(expect_error(dup, "assigned to two aggregates"))

def zero():
    am, e = fresh()
    build_claim_graph(am, e, {"aggregate_claims": [{"id": "AGG_z", "gloss": "z", "observation_ids": ["P77"]}]})
results.append(expect_error(zero, "zero belief edges"))

def collide():
    am, e = fresh()
    build_claim_graph(am, e, {"aggregate_claims": [{"id": "MECH_a", "gloss": "x", "observation_ids": ["P20"]}]})
results.append(expect_error(collide, "collides"))

def two_thesis():
    am, e = fresh()
    am["THESIS2"] = {"canonical_id": "THESIS2", "ontology_type": "paper_thesis",
                     "link_policy": "rolls_up_only", "gloss": "t2"}
    build_claim_graph(am, e, {"aggregate_claims": [{"id": "AGG_v", "gloss": "v", "observation_ids": ["P20"]}]})
results.append(expect_error(two_thesis, "exactly 1 paper_thesis"))

def self_rollup():
    am, e = fresh()
    build_claim_graph(am, e, {"claims_roll_up_to_thesis": ["THESIS"]})
results.append(expect_error(self_rollup, "roll up into itself"))

def rollup_nonclaim():
    am, e = fresh()
    am["QUAL"] = {"canonical_id": "QUAL", "ontology_type": "assumption",
                  "link_policy": "qualifier_only", "gloss": "q"}
    build_claim_graph(am, e, {"claims_roll_up_to_thesis": ["QUAL"]})
results.append(expect_error(rollup_nonclaim, "not a direct_link_allowed claim"))

def partial_miss():
    am, e = fresh()
    build_claim_graph(am, e, {"aggregate_claims": [
        {"id": "AGG_v", "gloss": "v", "observation_ids": ["P20", "P77"]}]})     # P20 matches, P77 does not
results.append(expect_error(partial_miss, "no re-routable belief edge"))

def dup_agg_id():
    am, e = fresh()
    build_claim_graph(am, e, {"aggregate_claims": [
        {"id": "AGG_v", "gloss": "v", "observation_ids": ["P20"]},
        {"id": "AGG_v", "gloss": "v2", "observation_ids": ["P22"]}]})           # same id declared twice
results.append(expect_error(dup_agg_id, "duplicate aggregate id"))

def two_thesis_explicit():                                                      # explicit id must NOT bypass cardinality
    am, e = fresh()
    am["THESIS2"] = {"canonical_id": "THESIS2", "ontology_type": "paper_thesis",
                     "link_policy": "rolls_up_only", "gloss": "t2"}
    build_claim_graph(am, e, {"paper_thesis_id": "THESIS",
                              "aggregate_claims": [{"id": "AGG_v", "gloss": "v", "observation_ids": ["P20"]}]})
results.append(expect_error(two_thesis_explicit, "exactly 1 paper_thesis"))

def thesis_id_mismatch():
    am, e = fresh()
    build_claim_graph(am, e, {"paper_thesis_id": "MECH_a",                      # names a non-thesis node
                              "aggregate_claims": [{"id": "AGG_v", "gloss": "v", "observation_ids": ["P20"]}]})
results.append(expect_error(thesis_id_mismatch, "does not match the sole paper_thesis"))

# validate-then-mutate: a config that fails a LATE check must leave am_canon / am_edges untouched
am, e = fresh()
before_nodes = set(am)
before_edges = {c: {k: set(v) for k, v in e[c].items()} for c in list(e)}
results.append(expect_error(
    lambda: build_claim_graph(am, e, {
        "aggregate_claims": [{"id": "AGG_v", "gloss": "v", "observation_ids": ["P20", "P22", "P26"]}],
        "claims_roll_up_to_thesis": ["NOPE_not_a_node"]}),                      # aggregates valid, rollup bad
    "not a canonical node"))
check(set(am) == before_nodes, "no aggregate node added after a rejected config (no partial mutation)")
check({c: {k: set(v) for k, v in e[c].items()} for c in list(e)} == before_edges,
      "am_edges unchanged after a rejected config (no partial mutation)")

# a missing-gloss aggregate must be rejected in phase 1 (schema) BEFORE any edge is moved
am, e = fresh()
mg_nodes = set(am)
mg_edges = {c: {k: set(v) for k, v in e[c].items()} for c in list(e)}
results.append(expect_error(
    lambda: build_claim_graph(am, e, {"aggregate_claims": [{"id": "AGG_x", "observation_ids": ["P20"]}]}),
    "missing required field"))
check(set(am) == mg_nodes, "missing-gloss: no aggregate node added (rejected before mutation)")
check({c: {k: set(v) for k, v in e[c].items()} for c in list(e)} == mg_edges,
      "missing-gloss: am_edges unchanged (rejected before mutation)")

def empty_oids():
    am, e = fresh()
    build_claim_graph(am, e, {"aggregate_claims": [{"id": "AGG_x", "gloss": "g", "observation_ids": []}]})
results.append(expect_error(empty_oids, "non-empty list"))

def dup_rollup():
    am, e = fresh()
    build_claim_graph(am, e, {"claims_roll_up_to_thesis": ["MECH_a", "MECH_a"]})
results.append(expect_error(dup_rollup, "duplicate claims_roll_up_to_thesis"))

# a reported-only config must NOT be early-returned away — it still audits headlines
am, e = fresh()
rolls_r, main_r, tid_r = build_claim_graph(am, e, {"reported_as_main_result_observations": ["P12", "P49"]})
check(main_r == {"P12", "P49"}, "reported-only config returns the audited set (not silently dropped)")
check(tid_r == "THESIS", "reported-only config still resolves the thesis")
check(rolls_r == [], "reported-only config produces no rolls_up")

fails = [r for r in results if r]
if fails:
    print("\n".join(fails))
    print(f"\n{len(fails)}/{len(results)} FAILED")
    raise SystemExit(1)
print(f"all {len(results)} claim-graph tests passed")
