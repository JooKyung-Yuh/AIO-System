Below is a Layer-1 AIO extraction for a paper: evidence spans pulled from the paper, each already
labeled with one category among assumption / mechanism / context / intervention / observable
(or "unresolved"), each with a unique span_id, plus classification reasoning and ambiguity notes.

paper_id: {paper_id}
paper_title_hint: {paper_title_hint}

--- LAYER 1 EXTRACTION START ---
{layer1_extraction}
--- LAYER 1 EXTRACTION END ---

Your task: ASSEMBLE "factor" units by SELECTING spans. A factor is one single testable claim —
roughly: one mechanism, tested under one intervention (against one reference arm), in one
context, with one observed result, resting on one assumption.

THE CORE RULE — SELECT, DO NOT SUMMARIZE:
- Each of the five fields below must be filled with the text of EXACTLY ONE span from the
  extraction above — copied as-is (you may lightly trim length or fix obvious grammar, but you
  must NOT add claims, and you must NOT combine content from two or more spans into one field).
- NEVER merge several mechanism spans into one summarizing sentence. NEVER paraphrase multiple
  spans together. One field = one span's text.
- If no span fits a field, set that field to null. Do not invent one.

HOW TO GROUP SPANS INTO A FACTOR:
- Group spans that describe the SAME single experiment / comparison / claim, then pick ONE span
  per role (assumption / mechanism / context / intervention / observable) from that group.
- COMPETING OR DISTINCT MECHANISMS -> SEPARATE FACTORS. If a group of spans contains two or more
  different mechanisms (different causal explanations), output one factor PER mechanism. These
  sibling factors may share the same context / intervention / observable / assumption spans, but
  each carries its own single mechanism span.
- If two spans state the SAME mechanism (mere restatement/duplication), pick only one; do not
  create duplicate factors and do not merge their text.
- One factor = one intervention axis x one condition. Do not fold two different comparisons into
  one factor just because they share a mechanism.

For each factor, output exactly ONE value per key (never a list):
- "assumption": the text of one assumption span, or null
- "mechanism": the text of one mechanism span, or null
- "context": the text of one context span, or null
- "intervention": the text of one intervention span, or null (null is correct for a purely
  observational factor with no manipulation/comparison)
- "observable": the text of one observable span, or null
- "source_spans": an object giving the span_id chosen for each field above, e.g.
  {"assumption": "S12", "mechanism": "S7", "context": "S3", "intervention": "S20", "observable": "S31"}
  Use null for any field you set to null. Every non-null field MUST have a matching span_id here.
- "status": "observed" if the observable span reports a result the paper actually measured,
  "inferred" if the factor rests on inference rather than a directly reported result
- "provenance": the single most grounding span text for this factor (usually the observable or
  mechanism span you selected)

Output ONLY a JSON array, no prose before or after, in exactly this shape:

[
  {
    "assumption": "...",
    "mechanism": "...",
    "context": "...",
    "intervention": "...",
    "observable": "...",
    "source_spans": {
      "assumption": "S12",
      "mechanism": "S7",
      "context": "S3",
      "intervention": "S20",
      "observable": "S31"
    },
    "status": "observed",
    "provenance": "..."
  }
]
