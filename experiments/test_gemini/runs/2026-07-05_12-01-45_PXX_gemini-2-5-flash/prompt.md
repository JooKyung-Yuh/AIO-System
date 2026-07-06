Attached is a scientific paper PDF.

paper_id: PXX
paper_title_hint: unknown

Your task is to extract evidence spans from this paper and classify each span into exactly
one of six categories. Use exactly these definitions — do not redefine them in your own words:

- "assumption": The underlying assumption, precondition, or scope condition that must hold for
  the mechanism/claim to be valid. This is usually implicit — the author rarely states it
  directly. Ask yourself: "for this claim to be true, what has to be assumed about the data,
  the model, or the setup?"
- "mechanism": The causal explanation the authors propose for why the intervention produces
  the effect. This is the "why", not the "what happened". If the text proposes two competing
  explanations for the same result, extract them as separate objects.
- "context": The concrete experimental setting in which this claim/mechanism is tested —
  dataset, model architecture, domain, task type, or any condition that limits generalizability
  (e.g. "CIFAR-10 diffusion model", "ARC-like test-time adaptation", "matched compute budget").
  Context must NOT contain metric/protocol definitions — see "eval_metric" below.
- "intervention": The specific manipulation, ablation, controlled comparison, or counterfactual
  condition performed to test the assumption/mechanism. If the text does not report any
  intervention for an otherwise clear claim, still create the object and set "intervention"
  to null.
- "eval_metric": The concrete measurement method, unit, or evaluation protocol used to quantify
  results — e.g. "top-1 accuracy", "pass@2", "FID score", or a full protocol definition such as
  "pass@2 accuracy: two solutions may be produced, correct if either is correct". This is the
  measurement instrument itself, not the trend it produced. A metric/protocol definition ALWAYS
  goes here, even if it is described inside a "benchmark setup" paragraph — never file it under
  "context".
- "pattern": The shape or trend the measurements took across conditions — e.g. "monotonic
  increase", "gain of X points", "degradation from A to B", "FID dropped sharply after 10k
  steps". This is the "what happened to the numbers", separate from the metric name itself and
  separate from the causal "why" (mechanism).

## R1 — Clause-level extraction (the unit is a ROLE, not a sentence)
- The extraction unit is the MINIMAL clause that performs exactly ONE of the six roles.
- Papers habitually pack several roles into one sentence. The most common pattern is:
  "we do X (intervention), and observe Y (pattern) on metric Z (eval_metric), suggesting
  W (mechanism)". You MUST split such sentences into separate spans — one span per role.
- Sibling spans coming from the same source sentence share a "parent" id. Parent ids use the
  source-sentence index (see "Per-category indexing" below), e.g. "S07". Standalone spans have
  "parent": null. Siblings must partition the sentence; their texts must not overlap.
- A span must never NEED a second label. If you are tempted to give one, split further.
- Span text: verbatim quote strongly preferred, roughly 10–40 words. Paraphrase only for
  figures/tables that cannot be quoted, and append "(paraphrase)" to the text.

## R1b — Per-category indexing
- Every candidate sentence in the paper is first assigned a sequential source-span index
  S1, S2, S3, ... in reading order (abstract -> body -> figures/tables -> appendix). This
  S-number is ONLY a source-span reference — it is never a node's own id.
- Each extracted node's real id is assigned per-category, sequentially in the order nodes of
  that category are produced:
  - assumption   -> A1, A2, A3, ...
  - context      -> C1, C2, C3, ...
  - mechanism    -> M1, M2, M3, ...
  - intervention -> I1, I2, I3, ...
  - eval_metric  -> E1, E2, E3, ...
  - pattern      -> P1, P2, P3, ...
- Every node records both ids: "node_id" (its category id, e.g. "A3") and "source_span" (the
  S-number it was extracted from, e.g. "S12"). Downstream stages (Layer 2) reference nodes by
  "node_id" only.
- If one sentence S12 is split into two nodes of different categories (e.g. an eval_metric and
  a pattern), both nodes record "source_span": "S12", but each gets its own category id
  (e.g. "E4" and "P2").

## R2 — Classification decision tree (run every candidate clause through these steps, IN ORDER)
Do not force one sentence into a single bucket, and do not duplicate the same clause into two
categories. Splitting a sentence into multiple nodes of different categories is expected and
required whenever it bundles more than one role.

STEP 1 — Is this an active action the authors performed (manipulation, ablation, comparison,
swap)?
  YES -> "intervention" (category I). If no intervention is reported for an otherwise clear
  claim, still note intervention: null on the surrounding factor — do not skip creating the
  surrounding nodes just because there is no intervention.
  NO -> go to Step 2.

STEP 2 — Is this naming the measurement instrument/unit/protocol used (e.g. "top-1 accuracy",
"pass@2", "FID score")?
  YES -> "eval_metric" (category E). eval_metric must capture the concrete measurement
  method/protocol itself (metric name, unit, direction of improvement, evaluation protocol like
  pass@2) — do NOT put this in context even if it is described as part of "the benchmark
  setup". Metric/protocol definitions always go to eval_metric, never to context.
  NO -> go to Step 3.

STEP 3 — Is this describing the shape/trend the measurements took across conditions (e.g.
"monotonic increase", "gain of X points", "degradation from A to B")?
  YES -> "pattern" (category P). If eval_metric and pattern are named in the same sentence
  ("FID dropped sharply after 10k steps"), split into two nodes: "FID" -> E, "dropped sharply
  after 10k steps" -> P. Never keep them as one merged node.
  NO -> go to Step 4.

STEP 4 — Is this the authors' causal explanation for WHY an effect happens (theory/
interpretation), as opposed to what was measured or what was done?
  YES -> "mechanism" (category M). If two competing explanations are given for the same result,
  create two separate M nodes.
  NO -> go to Step 5.

STEP 5 — Is this a validity-boundary condition — i.e., if this condition were violated, would
the specific claim become FALSE? Apply the mandatory certainty gate before accepting:
  - Check for hedging language: "may", "might", "could", "possibly", "may not hold", "it is
    unclear whether". If ANY hedge is present, DISCARD this clause entirely — do not create an
    assumption node from it.
  - Only proceed to assumption if the condition is stated as definite (e.g. "this requires X",
    "we assume Y", "this fails when Z" — no hedge words).
  YES (passes gate) -> "assumption" (category A).
  NO -> go to Step 6.

STEP 6 — Is this a descriptive fact about the experimental setup (dataset, architecture,
domain, task, compute budget) that does NOT assert what would happen if changed?
  YES -> "context" (category C).
  NO -> discard; this text is not a node for any category.

MANDATORY MIXED-SENTENCE RULE: many sentences (especially "Limitations" statements) bundle a
descriptive setup fact with a breaking/limitation claim, e.g. "we tested only on X, so results
may not hold on Y." Split such sentences at the clause boundary:
  - "we tested only on X" -> context (Step 6), always extracted regardless of what happens to
    the other clause.
  - "results may not hold on Y" -> run through Step 5's certainty gate. Since it contains "may",
    DISCARD it — do not create an assumption node.
  - Only extract the second clause as assumption if it is phrased without hedging (e.g. "this
    does not hold for Y", "this fails when Y").

DUPLICATION RULE: never write the same full sentence into two different category fields as a
shortcut. If a sentence contains distinct clauses belonging to two categories, split it into
two nodes with two different (possibly partial) source texts — one goes to each category's
index — instead of copying the whole sentence into both.

CROSS-CHECK RULE (for consistency across nodes describing the same experiment/ablation): if two
or more sentences describe the same figure/table/ablation study (e.g. same Fig. reference), and
one sentence clearly states an intervention (Step 1) for that experiment, all other nodes
referencing results from that same experiment must also be linked to that same intervention
index — do not leave intervention null for one sentence in the same experimental unit while
filling it in for another.

## R2b — "assumption" anti-patterns
- NEVER label as assumption: the paper title; contribution claims ("we show / we demonstrate
  that ..."); section headers; the authors' thesis or conclusions. Those are claims, not
  preconditions.
- Test before assigning: "If this condition were false, would the mechanism/claim break?"
  Only preconditions and scope conditions (about data, model, task, or evaluation) qualify —
  including ones stated only in passing.

## R3 — Confidence and calibration
- Every span gets "confidence": your probability from 0.00 to 1.00 that assigned_label is
  correct.
- If confidence < 0.60, set assigned_label to "unresolved" — do not guess.
- Writing a substantive ambiguity_reason while reporting confidence >= 0.95 is a
  contradiction; recheck one of the two.

## R4 — Output budget
- classification_reasoning: at most ONE short sentence. It may be "" only when the case is
  trivial AND ambiguity_reason is "none".
- alternative_labels_considered: only labels you genuinely weighed; usually an empty array.

## R5 — Coverage and deduplication
- Cover the ENTIRE paper: abstract, body, figure and table captions, and appendix.
- If the same sentence appears in more than one place (e.g., body and a figure caption),
  extract it ONCE and list all locations in "location", separated by " | ".

## Field order (decide the label LAST)
Within each JSON object, output the keys in exactly this order, so that your reasoning is
written before you commit to a label:
"node_id", "source_span", "parent", "text", "location", "classification_reasoning",
"alternative_labels_considered", "ambiguity_reason", "assigned_label", "confidence"

# PART 1 — span classification (JSON)

Output a single fenced code block containing one JSON array, one object per span. "node_id" is
assigned per-category as described in R1b (A1, C1, M1, I1, E1, P1, ...); "source_span" is the
sentence's global S-number and is never used as the node's own id:

```json
[
  {
    "node_id": "E1",
    "source_span": "S1",
    "parent": null,
    "text": "...",
    "location": "Section 3, Table 2",
    "classification_reasoning": "...",
    "alternative_labels_considered": [],
    "ambiguity_reason": "none",
    "assigned_label": "eval_metric",
    "confidence": 0.92
  }
]
```

JSON validity requirements: double quotes only, no trailing commas, escape internal quotes
and backslashes, no comments inside the JSON. Output nothing before the code block.

# PART 2 — classification process notes (prose, brief)

After the closing fence of the JSON block, write the two sections below in markdown prose.
Keep EACH section under 120 words.

## Classification criteria you actually used
Step back from individual spans and describe the general rules you ended up applying:
- What distinguishes "assumption" from "context" in this paper specifically?
- What distinguishes "mechanism" from a plain description of "what happened"?
- How did you decide when an intervention was implicit vs. genuinely absent (null)?
- What distinguished "eval_metric" (the measurement method/protocol itself) from "pattern"
  (the trend the measurements showed) when both appeared in the same sentence?
- Any rule of thumb you invented mid-way that you found yourself relying on?

## What you deliberately did NOT extract
List things that looked tempting to classify but that you excluded, and why (e.g. hedged
"may/might" clauses discarded at Step 5's certainty gate).

Remember: this is an extraction pass whose output feeds an automated factor-assembly stage.
"unresolved" is an acceptable label. Splitting is always the resolution for multi-role text.
