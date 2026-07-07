You are building **AM cards** — the "why the authors think so" layer of an AIO factor graph. These
are the mechanism and assumption nodes that measured observations will later vote on (strengthen /
weaken). This step does NOT touch observations; it only distills the belief-target nodes.

paper_id: {paper_id}
paper_title_hint: {paper_title_hint}

You are given the paper (prose + figure/table descriptions) and ONLY the Layer-1 nodes that were
labeled `mechanism` or `assumption`. Use the paper to judge which are genuine and to merge
restatements.

--- PAPER: PROSE TRANSCRIPTION ---
{paper_text}
--- PAPER: FIGURES & TABLES ---
{assets}
--- LAYER-1 MECHANISM / ASSUMPTION NODES ---
{am_spans}
--- END INPUT ---

## Your task

Emit an AM card ONLY for a node that is a genuine belief target. Be strict:

**mechanism** = a causal explanation for WHY an intervention produces its effect
  (e.g. "visual priors let the model generalize from few examples"). 
  REJECT — do not card — nodes that are merely:
  - a purpose / goal fragment ("to improve accuracy", "to incorporate visual priors"),
  - background motivation or a general aim ("draw inspiration from language modeling"),
  - a restatement of the result itself.

**assumption** = a scope or precondition the claim depends on
  (e.g. "ARC tasks are inherently visual", "the protocol tests cross-task generalization").
  REJECT a plain restatement of the task setup that carries no load-bearing precondition.

**DEDUPLICATE.** When several nodes state the SAME mechanism or assumption — most importantly the
paper's headline thesis repeated in many places — emit ONE card and list the other node_ids as
`aliases`. Do not create near-duplicate cards.

Use the paper text to decide both genuineness and which nodes are the same claim.

## Output

A JSON array only (no prose), each element exactly:

```json
{
  "am_id": "AM_001",
  "kind": "mechanism",
  "node": "M7",
  "aliases": ["M23", "M31"],
  "gloss": "abstraction can arise from visual learning alone",
  "provenance": { "location": "Section 1" }
}
```

`gloss` is a <=12-word restatement for readability. `node` is the representative node_id; `aliases`
is every other node_id (possibly empty) that restates the same belief. Emit nothing for rejected
nodes.
