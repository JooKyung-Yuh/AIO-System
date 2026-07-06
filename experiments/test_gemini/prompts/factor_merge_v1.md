Below is a Layer-1 AIO extraction for a paper: evidence spans pulled from the paper, each already
labeled with one or more candidate categories among assumption / mechanism / context /
intervention / observable, plus classification reasoning and ambiguity notes.

paper_id: {paper_id}
paper_title_hint: {paper_title_hint}

--- LAYER 1 EXTRACTION START ---
{layer1_extraction}
--- LAYER 1 EXTRACTION END ---

Your task: merge these labeled spans into "factor" units. A factor is one single testable claim
— roughly: one mechanism, tested under one intervention (against one reference arm), in one
context, with one observed result, resting on one assumption.

For each factor, output exactly ONE value per key below (never a list):
- "assumption": one sentence — the assumption merged into a single statement, or null if none
  of the spans supply one
- "mechanism": one sentence — the causal explanation being tested
- "context": one sentence — the experimental setting (dataset, model, domain, compute, etc.)
- "intervention": one sentence describing what was manipulated or compared, including the
  reference arm if there is one, or null if the underlying claim reports no manipulation
- "observable": one sentence — the measurable result that was compared or monitored

Also include:
- "status": "observed" if the observable is a result the paper actually reports, "inferred" if
  it is your own inference rather than something stated outright
- "provenance": a short verbatim quote (or close paraphrase) from the spans above that most
  directly grounds this factor

Rules:
- Do not invent anything that isn't supported by the spans above.
- If several spans clearly describe the same single comparison, merge them into ONE factor
  instead of duplicating it.
- If a factor has no clear span for one of the five keys, use null for that key rather than
  guessing or forcing an unrelated span into it.
- One factor = one intervention axis x one condition. Don't merge two different comparisons
  into a single factor just because they involve the same mechanism.
- Output ONLY a JSON array, no prose before or after, in exactly this shape:

[
  {
    "assumption": "...",
    "mechanism": "...",
    "context": "...",
    "intervention": "...",
    "observable": "...",
    "status": "observed",
    "provenance": "..."
  }
]
