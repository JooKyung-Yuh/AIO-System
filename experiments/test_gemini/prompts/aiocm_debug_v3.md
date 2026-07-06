Attached is a scientific paper PDF.

paper_id: {paper_id}
paper_title_hint: {paper_title_hint}

Your task is to split the content of this paper into the following five categories.
Use exactly these definitions — do not redefine them in your own words:

- "assumption": The underlying assumption, precondition, or scope condition that must hold for the mechanism/claim to be valid. This is usually implicit — the author rarely states it directly. Ask yourself: "for this claim to be true, what has to be assumed about the data, the model, or the setup?"
- "mechanism": The causal explanation the authors propose for why the intervention produces the effect. This is the "why", not the "what happened". If the text proposes two competing explanations for the same result, extract them as separate objects.
- "context": The concrete experimental setting in which this claim/mechanism is tested — dataset, model architecture, domain, task type, or any condition that limits generalizability (e.g. "CIFAR-10 diffusion model", "ARC-like test-time adaptation", "matched compute budget").
- "intervention": The specific manipulation, ablation, controlled comparison, or counterfactual condition performed to test the assumption/mechanism. If the text does not report any intervention for an otherwise clear claim, still create the object and set "intervention" to null.
- "observable": The specific, measurable metric, behavior, or empirical result that is monitored or compared across conditions to validate or invalidate the claim.

Do not just output final labels. I want to see the classification process itself, including the
ambiguous cases and the reasoning you used to resolve them.

Output your answer in exactly two parts, in this order. Do not write anything before part 1 or
between part 1 and part 2.

# PART 1 — span classification (JSON)

Go through the paper and list every source span relevant to these five categories.
Output a single fenced code block containing a JSON array, one object per span, with exactly
these keys:

- "span_id": a short unique id you assign, e.g. "S1", "S2", ...
- "text": the evidence snippet (short quote or close paraphrase)
- "location": section/page/table/figure if available
- "assigned_label": your best single label — one of "assumption", "mechanism", "context", "intervention", "observable", or "unresolved" if you genuinely cannot decide
- "alternative_labels_considered": array of other labels you seriously weighed (empty array if none)
- "classification_reasoning": why you assigned this label and not the alternatives — reference the definitions above
- "ambiguity_reason": what made this hard to classify, or "none" if it was clear-cut

Example shape only (do not copy the content, only the structure):

```json
[
  {
    "span_id": "S1",
    "text": "...",
    "location": "Section 3, Table 2",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "...",
    "ambiguity_reason": "none"
  }
]
```

# PART 2 — classification process notes (prose)

After the closing fence of the JSON block, write two markdown sections in prose:

## Classification criteria you actually used
Step back from individual spans and describe, in your own words, the general rules you ended up
applying while doing PART 1 above:
- What distinguishes "assumption" from "context" in this paper specifically?
- What distinguishes "mechanism" from a plain description of "what happened"?
- How did you decide when an intervention was implicit vs. genuinely absent (null)?
- What made an "observable" count as evidence for/against a mechanism vs. just a raw number?
- Any rule of thumb you invented mid-way that isn't in the five definitions above but that you
  found yourself relying on?

## What you deliberately did NOT extract
List things that looked tempting to classify but that you excluded, and why (e.g. a claim with
no intervention that you still didn't want to force into "assumption", a method name that looked
like it could be a mechanism, etc.)

Remember:
This is an extraction-debug pass focused on the classification process, not a final database and
not a polished paper summary. "unresolved" is an acceptable assigned_label.
