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

Do not just output final labels. I want to see the classification process itself, including
the ambiguous cases and the reasoning you used to resolve them.

Please produce the following sections.

# 1. Evidence spans
Go through the paper and list the source spans relevant to these five categories.
For each span, include:
- location: section/page/table/figure if available
- evidence snippet (short quote or close paraphrase)
- candidate label(s): one or more of assumption / mechanism / context / intervention / observable
  (a span may only fit one category, but if it plausibly fits more than one, list all candidates —
  do not force a single label prematurely)

# 2. Classification table
Create a table with columns:
- span_id
- text
- assigned_label: assumption / mechanism / context / intervention / observable
- evidence_location
- classification_reasoning: why this label and not another — reference the definition above
- alternative_label_considered: which other label(s) you weighed, or "none"
- ambiguity_reason: what made this hard to classify, or "none" if it was clear-cut

# 3. Classification criteria you actually used
This is the most important section. Step back from individual spans and describe, in your own
words, the general rules you ended up applying while doing section 1-2 above:
- What distinguishes "assumption" from "context" in this paper specifically?
- What distinguishes "mechanism" from a plain description of "what happened"?
- How did you decide when an intervention was implicit vs. genuinely absent (null)?
- What made an "observable" count as evidence for/against a mechanism vs. just a raw number?
- Any rule of thumb you invented mid-way that isn't in the five definitions above but that you
  found yourself relying on?

# 4. Ambiguous / contested cases
List every span where you seriously considered two different labels, or where you are not
confident in the label you picked. For each:
- span_id (reference section 2)
- the competing labels
- the deciding factor that tipped you one way (or "unresolved" if it's still a toss-up)

# 5. What you deliberately did NOT extract
List things that looked tempting to classify but that you excluded, and why (e.g. a claim with
no intervention that you still didn't want to force into "assumption", a method name that looked
like it could be a mechanism, etc.)

Remember:
This is an extraction-debug memo focused on the classification process, not a final database
and not a polished paper summary. Multi-label and "unresolved" are acceptable answers.
