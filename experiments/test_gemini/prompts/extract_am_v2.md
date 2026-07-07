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

Emit an AM card ONLY for a node that is a genuine belief target. Be strict.

### mechanism = a causal explanation for WHY an intervention produces its effect
(e.g. "visual priors let the model generalize from few examples").
REJECT — do not card — nodes that are merely:
- a purpose / goal fragment ("to improve accuracy", "to incorporate visual priors"),
- background motivation or a general aim ("draw inspiration from language modeling"),
- a restatement of the result itself.

### assumption — accept ONLY a load-bearing precondition (be much stricter than for mechanism)

An assumption is worth carding ONLY if it is a **load-bearing precondition whose truth would change
the interpretation of one or more concrete observations in THIS paper**. Sort every candidate into
one of three buckets and card only the first:

- **(A) Load-bearing precondition — CARD IT.** A concrete observation's interpretation would become
  invalid if this statement were false, OR the paper explicitly frames it as an assumption /
  requirement / limitation / scope condition / necessary condition, OR a concrete observation in this
  paper could directly strengthen or weaken it.
  (e.g. "ARC tasks are visual enough that visual priors help" — the visual-prior ablations directly
  bear on it; "most ARC tasks are unambiguous" — multi-view/voting results bear on it.)

- **(B) Evaluation / scope / task-setup condition — DO NOT CARD (leave for context).** A description
  of the experimental setting or benchmark protocol, not a belief the results test.
  (e.g. "the model predicts each unseen task given a few examples", "evaluation uses pass@2".)

- **(C) Background / world statement — DO NOT CARD.** Paper background or general motivation that no
  observation in this paper could plausibly support or weaken.
  (e.g. "humans solve ARC using common sense".)

Explicit reject list for assumptions — never card:
- task definitions or benchmark protocol descriptions;
- generic background or broad motivation statements;
- statements that merely restate the dataset / problem setup;
- any statement that no concrete observation in this paper could plausibly support or weaken.

**If you are unsure whether a node is a load-bearing assumption or just context/background, REJECT
it as an AM card** and leave it for the context / canonicalization stage. Missing a borderline
assumption is cheaper than admitting an unstable one — do not card on the benefit of the doubt.

### DEDUPLICATE
When several nodes state the SAME mechanism or assumption — most importantly the paper's headline
thesis repeated in many places — emit ONE card and list the other node_ids as `aliases`. Do not
create near-duplicate cards. Use the paper text to decide both genuineness and which nodes are the
same claim.

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
