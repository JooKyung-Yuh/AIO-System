Attached is a scientific paper PDF.

paper_id: {paper_id}
paper_title_hint: {paper_title_hint}

Your task is to extract evidence spans from this paper and classify each span into exactly
one of five categories. Use exactly these definitions — do not redefine them in your own words:

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
- "intervention": The specific manipulation, ablation, controlled comparison, or counterfactual
  condition performed to test the assumption/mechanism. If the text does not report any
  intervention for an otherwise clear claim, still create the object and set "intervention"
  to null.
- "observable": The specific, measurable metric, behavior, or empirical result that is
  monitored or compared across conditions to validate or invalidate the claim.

## R1 — Clause-level extraction (the unit is a ROLE, not a sentence)
- The extraction unit is the MINIMAL clause that performs exactly ONE of the five roles.
- Papers habitually pack several roles into one sentence. The most common pattern is:
  "we do X (intervention), and observe Y (observable), suggesting Z (mechanism)".
  You MUST split such sentences into separate spans — one span per role.
- Sibling spans coming from the same source sentence share a "parent" id ("P01", "P02", ...).
  Standalone spans have "parent": null. Siblings must partition the sentence; their texts
  must not overlap.
- A span must never NEED a second label. If you are tempted to give one, split further.
- Span text: verbatim quote strongly preferred, roughly 10–40 words. Paraphrase only for
  figures/tables that cannot be quoted, and append "(paraphrase)" to the text.

## R2 — "assumption" anti-patterns
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
"span_id", "parent", "text", "location", "classification_reasoning",
"alternative_labels_considered", "ambiguity_reason", "assigned_label", "confidence"

# PART 1 — span classification (JSON)

Output a single fenced code block containing one JSON array, one object per span:

```json
[
  {
    "span_id": "S1",
    "parent": null,
    "text": "...",
    "location": "Section 3, Table 2",
    "classification_reasoning": "...",
    "alternative_labels_considered": [],
    "ambiguity_reason": "none",
    "assigned_label": "observable",
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
- What made an "observable" count as evidence for/against a mechanism vs. just a raw number?
- Any rule of thumb you invented mid-way that you found yourself relying on?

## What you deliberately did NOT extract
List things that looked tempting to classify but that you excluded, and why.

Remember: this is an extraction pass whose output feeds an automated factor-assembly stage.
"unresolved" is an acceptable label. Splitting is always the resolution for multi-role text.
