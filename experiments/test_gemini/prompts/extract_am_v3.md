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

Emit an AM card ONLY for a node that is a genuine belief target, AND merge every restatement of the
same belief into a single card. Two mistakes are equally bad and equally forbidden: (1) carding
junk that is not a belief target, and (2) emitting several near-duplicate cards for one belief.
Be strict on both.

### mechanism = a causal explanation for WHY an intervention produces its effect
(e.g. "visual priors let the model generalize from few examples").
REJECT — do not card — nodes that are merely:
- a purpose / goal fragment ("to improve accuracy", "to incorporate visual priors"),
- background motivation or a general aim ("draw inspiration from language modeling"),
- a restatement of the result itself ("accuracy improves").

### assumption — card ONLY a load-bearing precondition (stricter than mechanism)
Card an assumption ONLY if its truth would change how a concrete observation in THIS paper is
interpreted. Sort each candidate into one bucket and card ONLY bucket (A):
- **(A) load-bearing precondition — CARD IT.** A concrete result's interpretation breaks if this
  were false, OR the paper explicitly frames it as an assumption / requirement / limitation / scope
  condition, OR some observation in this paper could directly strengthen or weaken it.
  (e.g. "ARC tasks are visual enough that visual priors help"; "most ARC tasks are unambiguous".)
- **(B) evaluation / scope / task-setup condition — DO NOT CARD** (leave it for context).
  (e.g. "the model predicts each unseen task from a few examples"; "evaluation uses pass@2".)
- **(C) background / world statement — DO NOT CARD.**
  (e.g. "humans solve ARC using common sense".)
If you are unsure whether a node is a load-bearing assumption or just setup/background, REJECT it.
Missing a borderline assumption is cheaper than admitting an unstable one — do not card on the
benefit of the doubt.

### DEDUPLICATE — applies to mechanisms AND assumptions; do this aggressively
When several nodes state the SAME belief — especially the paper's headline thesis repeated across
abstract, intro, method, and conclusion — emit ONE card and list every other node_id in `aliases`.
Do NOT emit near-duplicate cards that differ only in wording, granularity, or which section they
came from. Example: if M10, M17, M34, M36 all express "canvas patchification enriches the learnable
data space", that is ONE card with three aliases, not four cards. A paper has only a handful of
distinct mechanisms; if you find yourself emitting many mechanism cards, you are under-merging or
carding purpose/background fragments — go back, merge the duplicates, and drop the fragments.

Use the paper text to decide both genuineness and which nodes state the same claim.

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
