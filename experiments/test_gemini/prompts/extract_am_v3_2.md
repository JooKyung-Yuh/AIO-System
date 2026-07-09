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
(e.g. "a deeper network can represent more compositional functions").
REJECT — do not card — nodes that are merely:
- a purpose / goal fragment ("to improve accuracy", "to incorporate visual priors"),
- background motivation or a general aim ("draw inspiration from language modeling"),
- a restatement of the result itself ("accuracy improves").

### assumption — card ONLY a load-bearing precondition that THIS paper's results can test
An assumption is worth carding ONLY if BOTH hold:
1. **Load-bearing:** if it were false, the interpretation of at least one concrete result in this
   paper would change (or the paper explicitly frames it as an assumption / requirement /
   limitation / scope condition).
2. **Testable here (HARD GATE):** you can point to at least one concrete observation IN THIS PAPER
   — a specific table row, figure, ablation, or measured comparison — that would strengthen or
   weaken it. Name that observation to yourself before carding. If no observation in this paper
   could move it, DO NOT card it.

Sort each candidate into one bucket and card ONLY (A):
- **(A) load-bearing AND testable here — CARD IT.**
  (e.g. "the benchmark's labels are noise-free" ← a held-out re-labeling check bears on it;
   "two conditions share the same input distribution" ← a transfer / ablation result bears on it.)
- **(B) evaluation / scope / task-setup condition — DO NOT CARD** (leave for context). A description
  of the setting, protocol, or a definitional equivalence that no result is trying to test.
  (e.g. "each task provides only a few training examples"; "a single forward pass yields one
   prediction"; "disabling the augmentation recovers the baseline configuration".)
- **(C) background / world statement — DO NOT CARD.**
  (e.g. "humans acquire new skills from few demonstrations".)

Two extra rejects, on top of bucket (B)/(C):
- reject a statement that merely re-describes a method step or a definitional equivalence;
- reject any assumption you cannot tie to a specific supporting/weakening observation in this paper.

If you are unsure, REJECT. Missing a borderline assumption is cheaper than admitting an unstable
one; assumptions are the least reproducible node type, so hold this bar high — a typical paper
yields only a few genuinely testable assumptions, not a dozen.

### DEDUPLICATE — applies to mechanisms AND assumptions; do this aggressively
When several nodes state the SAME belief — especially the paper's headline thesis repeated across
abstract, intro, method, and conclusion — emit ONE card and list every other node_id in `aliases`.
Do NOT emit near-duplicate cards that differ only in wording, granularity, or which section they
came from. Example: if three nodes M4, M9, M12 all express the same idea (say "the pretraining
objective shapes the learned representation"), that is ONE card with two aliases, not three cards. A paper has only a handful of
distinct mechanisms; if you find yourself emitting many mechanism cards, you are under-merging or
carding purpose/background fragments — go back, merge the duplicates, and drop the fragments.

Use the paper text to decide both genuineness and which nodes state the same claim.

## Output

A JSON array only (no prose), each element exactly:

```json
{
  "am_id": "AM_001",
  "kind": "mechanism",
  "node": "M0aa",
  "aliases": ["M0bb", "M0cc"],
  "gloss": "<=12-word restatement of the represented belief>",
  "provenance": { "location": "Section 1" }
}
```

`gloss` is a <=12-word restatement for readability. `node` is the representative node_id; `aliases`
is every other node_id (possibly empty) that restates the same belief. Emit nothing for rejected
nodes.
