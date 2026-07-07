Below is a pool of Layer-1 AIO extraction nodes: evidence nodes already labeled with one
category among assumption / mechanism / context / intervention / eval_metric / pattern, each
with a unique node_id (e.g. "A3", "M7", "C2", "I1", "E4", "P2"), its exact quoted "text",
"location", "paper_id" (which paper it came from), and — for intervention / pattern nodes only —
an "experiment_ref" (a short id naming the specific experiment/ablation/comparison it belongs
to; eval_metric nodes never carry this field, since a metric definition is reusable across
experiments and papers, not owned by one). node_ids are already globally unique — never invent
a new one and never renumber an existing one.

This canonicalization runs GLOBALLY over the node pool from ALL papers and ALL page-batches at
once — never per-paper or per-batch. Two nodes from different papers that denote the same
underlying variable/claim MUST be able to merge into one canonical node. Cross-paper merging is
the whole point; do not restrict merges to within a single paper.

NODES:
{nodes}

Perform BOTH tasks below over this same node pool, at once.

## MERGING DUPLICATES

Merge two nodes when they denote the SAME underlying claim/variable/result, regardless of which
paper, section, figure, or experiment_ref they came from. Cross-paper and cross-experiment_ref
merging is EXPECTED — a differing experiment_ref is NOT a reason to refuse a merge, and a
matching experiment_ref is NOT by itself a reason to merge. experiment_ref is at most weak
supporting evidence, never the gate. The gate is CONTENT, and it is applied differently
depending on the node's category:

A) assumption / mechanism / context / eval_metric
   These are reusable definitions/premises, not facts owned by one experiment. Merge on
   semantic identity of the underlying concept — e.g. two phrasings of "pass@k accuracy", or of
   "trained from scratch on domain-specific data" — freely across papers and experiment_refs
   whenever they mean the same thing. There is no fixed similarity threshold; use judgment on
   whether two nodes denote the SAME concept (merge) versus a merely related but distinct one
   (keep separate).

B) intervention / pattern  (experiment-bound facts — merge ONLY if ALL three conditions match)
   These describe one specific manipulation and the specific result it produced, so a shallow
   textual or topical similarity is not enough. Merge two intervention nodes, or two pattern
   nodes, ONLY when all three hold:
   1. SUBJECT — the same thing is manipulated (intervention) or measured (pattern): the same
      component/axis/variable, not merely a similar-sounding one.
   2. COMPARISON TARGET — the same baseline / alternative / reference condition is being
      contrasted (or both genuinely have none).
   3. DIRECTION & ROUGH MAGNITUDE — the same side wins, and the effect size is of the same
      order. "Independent TTT beats joint TTT by ~10 points" and "accuracy increases over
      training epochs" are NOT the same result even though both could loosely be described as
      "improvement" — do not merge on a shared trend keyword alone.
   If any of the three differs, do NOT merge — even when experiment_ref is identical (a single
   table or figure can contain several distinct sub-experiments). If all three match, DO merge —
   even when experiment_ref differs (this correctly repairs a real experiment that got split
   across chunks, or unifies the same finding reported in different papers).

Never merge on a shallow cue alone: neither a shared experiment_ref, nor a shared trend keyword,
nor topical similarity, is sufficient by itself. Judge the full proposition (who/what was
acted on, against what, with what direction/size of effect).

For each duplicate cluster, pick ONE existing node's id as canonical — prefer the node whose
text is the most complete/self-contained. Never invent a new node_id.

## GENERALIZING TEXT

Almost every node's text was quoted verbatim from ONE paper, so it is more specific than it
needs to be if the node is ever reused when reading a different paper. This applies to the
canonical node of every cluster, AND to any standalone node whose text you judge would benefit
from it:

- You MAY rewrite a node's text into a shorter, more general form: drop incidental,
  paper-specific detail that is not load-bearing for the claim itself (e.g. an exact dataset
  name, a specific numeric result, a model version number), so that the same node could
  plausibly be reused as-is when reading a different paper.
- Do NOT over-compress: keep almost all of the original meaning. If a detail is actually
  essential to what the claim asserts — the claim would become false, vague, or a materially
  different claim without it — keep the detail; this is the exception, and when in doubt, keep
  it rather than cut it.
- DIRECTION PRESERVATION (mandatory for intervention / pattern nodes): when generalizing a
  comparative pattern or intervention, you MUST keep which side wins / the direction of the
  effect. Dropping the subject of a comparison — turning "independent TTT beats joint TTT by
  ~10 points" into "substantially better performance" — is a forbidden over-compression, because
  the direction and the subject are exactly what make the claim testable. Keep them.
- Never fabricate a fact that is not supported by the original text; never touch node_id.
- If you rewrote a node's text, record the new text as "canonical_text" (omit this key entirely
  if the text is unchanged).

## EXPERIMENT_REF HANDLING

- Only intervention and pattern nodes carry "experiment_ref". It is a LIST of one or more ids,
  never a bare string. assumption / mechanism / context / eval_metric nodes never get this
  field — omit the key entirely for them, do not set it to null.
- Never fabricate an experiment_ref value.
- On a straightforward rewrite (no real duplicate), the canonical entry's experiment_ref is the
  node's own original ref, wrapped as a single-item list (e.g. ["Fig7"]).
- On a merge, the canonical entry's experiment_ref becomes the UNION of every merged node's
  experiment_ref values, deduplicated. Do NOT collapse this to one value and do NOT drop any —
  every original ref must remain queryable downstream. This matters specifically because the
  content-based merge test above allows merging intervention/pattern nodes that carry DIFFERENT
  experiment_refs; when that happens, preserving the full union is how the merged node stays
  linkable to every experiment it actually came from. Also note in "reason" which original refs
  came from which merged node, for traceability.

## What to emit a node_registry entry for

- Any node that is part of a duplicate cluster (merged_node_ids has more than one member), OR
- Any node whose text you rewrote (canonical_text present), OR
- ALWAYS — every canonical (surviving) node needs an entry regardless of the above.
- In other words: emit exactly one node_registry entry per SURVIVING (canonical) node in this
  pool, plus nothing for absorbed (non-canonical, merged-away) node ids.

Output ONLY a JSON object, no prose before or after, in exactly this shape:

```json
{
  "node_registry": [
    {
      "canonical_node_id": "I5",
      "label": "intervention",
      "source_span": "S23",
      "experiment_ref": ["Fig7", "patch-size-sweep"],
      "merged_node_ids": ["I5", "I19"],
      "canonical_text": "...",
      "reason": "..."
    },
    {
      "canonical_node_id": "A3",
      "label": "assumption",
      "source_span": "S12",
      "merged_node_ids": ["A3", "A9"],
      "canonical_text": "...",
      "reason": "..."
    }
  ]
}
```

- "label": the node's own category (assumption/mechanism/context/intervention/eval_metric/
  pattern) — copy it from the input, do not reclassify it here.
- "source_span": copy the canonical node's own source_span from the input.
- "experiment_ref": a LIST, present ONLY for intervention/pattern nodes, equal to the union of
  every merged node's original experiment_ref values (or a single-item list if unchanged). Omit
  this key entirely for assumption/mechanism/context/eval_metric nodes.
- "merged_node_ids": the full list including the canonical id itself. For a rewrite-only entry
  with no real duplicates, this is just [canonical_node_id].
- "canonical_text": include this key ONLY if you rewrote the text — omit it if unchanged.
- "reason": a short note covering what you did (merged / generalized / both), why, and — if the
  merged nodes had differing experiment_refs — which ones came from where.

JSON validity requirements: double quotes only, no trailing commas, escape internal quotes and
backslashes, no comments inside the JSON. Output nothing before or after this JSON object.
