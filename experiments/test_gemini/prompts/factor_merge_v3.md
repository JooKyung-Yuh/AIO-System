Below is a Layer-1 AIO extraction for a paper: evidence nodes pulled from the paper, each already
labeled with one category among assumption / mechanism / context / intervention / eval_metric /
pattern (or "unresolved"), each with a unique per-category node_id (e.g. "A3", "M7", "C2", "I1",
"E4", "P1") plus classification reasoning and ambiguity notes. Each node also carries a
"source_span" (its original sentence index, e.g. "S12") for provenance only.

paper_id: {paper_id}
paper_title_hint: {paper_title_hint}

--- LAYER 1 EXTRACTION START ---
{layer1_extraction}
--- LAYER 1 EXTRACTION END ---

Your task: ASSEMBLE "factor" units by SELECTING nodes. A factor is one single testable claim —
roughly: one mechanism, tested under one intervention (against one reference arm), in one
context, with one measured pattern on one eval_metric, resting on one assumption.

THE CORE RULE — SELECT, DO NOT SUMMARIZE, AND DO NOT REPRODUCE TEXT:
- Each of the six fields below must be filled with the "node_id" of EXACTLY ONE node from the
  extraction above — never its text, and never a source_span (S-number). The full text for any
  node_id is already recoverable from Layer 1's output and must NOT be repeated here.
- NEVER merge several mechanism nodes into one field. NEVER paraphrase multiple nodes together.
  One field = one node's id.
- If no node fits a field, set that field to null. Do not invent one.

HOW TO GROUP NODES INTO A FACTOR:
- Group nodes that describe the SAME single experiment / comparison / claim, then pick ONE node
  id per role (assumption / mechanism / context / intervention / eval_metric / pattern) from
  that group.
- COMPETING OR DISTINCT MECHANISMS -> SEPARATE FACTORS. If a group of nodes contains two or more
  different mechanisms (different causal explanations), output one factor PER mechanism. These
  sibling factors may share the same context / intervention / eval_metric / pattern / assumption
  node ids, but each carries its own single mechanism node id.
- If two nodes state the SAME mechanism (mere restatement/duplication), pick only one; do not
  create duplicate factors.
- One factor = one intervention axis x one condition. Do not fold two different comparisons into
  one factor just because they share a mechanism.
- METRIC/PROTOCOL ROUTING: any node labeled "eval_metric" in Layer 1 must be placed in this
  factor's "eval_metric" field. It is disallowed to place an eval_metric node's id into the
  "context" field, even if it originated from a "benchmark setup" paragraph. If a group has no
  eval_metric node but has a pattern node, still set "eval_metric": null rather than
  substituting a context node.
- CROSS-CHECK: if two or more nodes in the group come from the same experimental unit (e.g. same
  figure/table) and one of them fixes an intervention node id, all factors built from that group
  must use that same intervention node id — do not leave intervention null for one factor in the
  group while filling it in for a sibling factor from the same experiment.

For each factor, output exactly ONE value per key (never a list), using node_id strings only:
- "assumption": the node_id of one assumption node (e.g. "A3"), or null
- "mechanism": the node_id of one mechanism node (e.g. "M7"), or null
- "context": the node_id of one context node (e.g. "C2"), or null
- "intervention": the node_id of one intervention node (e.g. "I1"), or null (null is correct for
  a purely observational factor with no manipulation/comparison)
- "eval_metric": the node_id of one eval_metric node (e.g. "E4"), or null
- "pattern": the node_id of one pattern node (e.g. "P1"), or null
- "status": "observed" if the pattern node reports a result the paper actually measured,
  "inferred" if the factor rests on inference rather than a directly reported result
- "provenance": the single node_id that is the most grounding node for this factor (usually the
  pattern or mechanism node id you selected)

Output ONLY a JSON array, no prose before or after, in exactly this shape:

[
  {
    "assumption": "A3",
    "mechanism": "M7",
    "context": "C2",
    "intervention": null,
    "eval_metric": "E4",
    "pattern": "P1",
    "status": "observed",
    "provenance": "P1"
  }
]
