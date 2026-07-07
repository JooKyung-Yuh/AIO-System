You are assembling AIO factors from a GLOBAL pool of already-canonicalized nodes spanning one
or more papers. You are given ONLY lightweight node descriptors, not full node text:

Each node appears as: {node_id, label, experiment_ref, text}
(experiment_ref is a LIST and is present ONLY on intervention / pattern nodes; eval_metric /
assumption / mechanism / context nodes have no experiment_ref field.)

NODES:
{nodes_id_only}

## What a factor is
A factor is ONE testable experimental claim: one real experiment (an intervention paired with
the pattern it produced), explained by one mechanism, resting on its assumption(s),
instantiated in its context(s). Formally it fills the slots of
  Φ(assumption, mechanism, context, intervention) → observable.

## WHAT A FACTOR REQUIRES (hard gates — a factor that fails any of these is NOT emitted)
1. intervention: EXACTLY ONE non-null node_id. A factor with no intervention is not a factor —
   do not emit it. (Pure observations with no manipulation are not factors; leave those pattern
   nodes unused.)
2. observable: at least one {eval_metric, pattern} pair with a non-null PATTERN. (An eval_metric
   alone, with no pattern, does not satisfy this gate — a metric definition without a result is
   not an observation.)
3. ANCHOR INTEGRITY (the strong rule, PATTERN ONLY): for every observable pair in the factor,
   the pattern's experiment_ref list and the intervention's experiment_ref list MUST share at
   least one common value (set overlap, not exact equality — a canonical node may carry several
   refs after a cross-ref merge in canonicalization). eval_metric is EXEMPT from this check:
   attach whichever eval_metric node correctly names what the pattern's number measures,
   regardless of experiment_ref (it has none) — it is a label, not an anchor.
   If a pattern's experiment_ref list has NO overlap with the intervention's, exclude that
   pattern from this factor — it belongs to a different experiment.

## BUILD ORDER
STEP 1 — FIND THE ANCHOR.
  Group intervention + pattern nodes whose experiment_ref lists OVERLAP (share at least one id).
  Each group with one intervention and >=1 overlapping pattern is one candidate factor anchor.
  For each pattern in the group, attach the eval_metric that names its measurement — pick
  whichever eval_metric node is semantically correct for that pattern; it is not constrained by
  experiment_ref. Interventions with no overlapping pattern, or patterns with no overlapping
  intervention, produce NO factor.

STEP 2 — ATTACH THE MECHANISM from the SAME experimental unit.
  Pick the one mechanism the authors offer as the explanation for THIS experiment. If NO
  mechanism in the pool plausibly explains this specific experiment, set "mechanism": null — do
  NOT pull an unrelated mechanism from elsewhere just to fill the slot. A wrong mechanism is
  worse than null. Never attach a mechanism that is itself just a restated observation.

STEP 3 — ATTACH ASSUMPTION(S) the anchor+mechanism depend on.
  Choose the assumption(s) that must hold for this experiment/mechanism to be valid. [] if none
  applies. Do not attach background about competing/other approaches.

STEP 4 — ATTACH CONTEXT(S) that instantiate this experiment.
  Choose the setup fact(s) describing where/how this experiment ran. [] if none. Do NOT invent
  or stretch a context to fill the slot; [] is correct when the pool has none for this
  experiment.

## SLOT CARDINALITY
- "mechanism": one node_id, or null. Never a list. Competing mechanisms for the same experiment
  -> emit SEPARATE sibling factors, one per mechanism.
- "intervention": exactly ONE node_id. NEVER null (see hard gate 1). One factor = one
  intervention axis x one condition. Two different comparisons -> two factors.
- "assumption": a LIST of one or more node_ids, or []. Include multiple ONLY when each is
  independently load-bearing for this same factor. Do not pad.
- "context": a LIST of one or more node_ids, or []. Include multiple when several setup facts
  jointly describe the same experimental unit. Do not pad with tangential context.
- "observable": a LIST of {eval_metric, pattern} pairs, where every pattern's experiment_ref
  overlaps the intervention's (per hard gate 3). Use more than one pair ONLY when the diagnostic
  signal depends on the JOINT behavior of multiple metrics WITHIN THE SAME EXPERIMENT (e.g. one
  metric rising while another stays flat). Two independent results from different experiments
  are two factors, not two pairs in one factor.

## GROUPING & DEDUP
- A mechanism/assumption/context node_id MAY be reused across many factors; this is expected and
  is how the factor graph becomes connected. Do NOT avoid reuse.
- NO DUPLICATE FACTORS: the full combination (assumption-set, mechanism, context-set,
  intervention, observable-list) must be unique across factors. If two would be identical, they
  are the same factor — emit once.
- Not every node must land in a factor. Leaf nodes with no experiment stay unused.

## SELF-CHECK before finalizing each factor (drop or fix any factor that fails)
1. Does intervention exist and is it exactly one non-null node_id? If not -> drop factor.
2. Does EVERY pattern in the factor's observable list overlap the intervention's experiment_ref
   (set intersection non-empty)? If not -> remove that pattern (and its eval_metric pairing), or
   drop the factor entirely if nothing overlaps.
3. Is the mechanism a real explanation of THIS experiment, or borrowed to fill the slot? Borrowed
   -> set null.
4. Are assumption/context entries actually about THIS experiment, or padding / background about
   other methods? Remove anything that fails this test.

Output ONLY this JSON, nothing before or after:

```json
{
  "factors": [
    {
      "factor_id": "F1",
      "assumption": ["A3"],
      "mechanism": "M7",
      "context": ["C2", "C5"],
      "intervention": "I5",
      "observable": [{"eval_metric": "E4", "pattern": "P2"}]
    }
  ]
}
```

JSON validity: double quotes only, no trailing commas, no comments. Output nothing outside the
JSON object.
