You are assembling **CIO observation cards** — the "what was done and what was measured" layer of
an AIO factor graph. Each card is ONE measured observation: a context (the experimental setting),
an intervention (and its reference / baseline arm when the paper compares two conditions), and an
observable (an eval_metric + the measured pattern). A CIO card carries **NO mechanism and NO
assumption** — the "why the authors think so" layer is built separately and linked later.

paper_id: {paper_id}
paper_title_hint: {paper_title_hint}

You are given (1) the paper itself (prose transcription + figure/table descriptions) so you can
ground each observation, and (2) a Layer-1 span extraction already grouped into local **evidence
units** by the paper location the spans came from (a Table, a Figure, or a Section). Each node has a
per-category node_id (C.. context, I.. intervention, E.. eval_metric, P.. pattern) and a
source_span.

--- PAPER: PROSE TRANSCRIPTION ---
{paper_text}
--- PAPER: FIGURES & TABLES ---
{assets}
--- LAYER-1 EVIDENCE UNITS (spans grouped by location) ---
{evidence_units}
--- END INPUT ---

## Your task

Emit CIO cards by SELECTING node_ids. Follow these rules exactly:

**SELECT, never write text.** Every field is a node_id (or list of node_ids) drawn from the input —
never the node's text, never a source_span (S-number). If no node fits, use null.

**One card per measured result.** Anchor exactly one card on each pattern node whose
`pattern_class` is `primary_result` or `comparison`. Do **not** build cards on `summary_claim` or
`background` patterns (those are abstract/headline restatements, not a single measured result).

**Stay inside one evidence unit.** Build each card from node_ids belonging to the SAME evidence
unit as its pattern node. NEVER mix node_ids from different units into one card — the unit boundary
is the experiment boundary. (A pattern in a prose Section may pull its context/intervention from the
same Section unit only.)

**Fill each field by selecting from that unit:**
- `context`: the list of context node_ids that state this observation's setting (often several —
  e.g. the spec rows of a table). Prefer the concrete setting rows over vague background.
- `intervention`: the node_id of the manipulated / compared condition. Use null only for a purely
  observational result with no manipulation.
- `reference`: **the baseline arm.** When the pattern is a comparison ("A is better than B"), select
  the node_id of the baseline/other condition B if a distinct node exists; otherwise null. Read the
  PAPER text and figure descriptions to identify B (e.g. "U-Net" opposite "ViT", "TTT jointly"
  opposite "TTT independently").
- `eval_metric`: the node_id of the metric, or null.
- `pattern`: the node_id of the measured result (the anchor).
- `direction`: `up` / `down` / `flat` / null — the direction the pattern reports for the
  intervention relative to the reference, read from the paper/figure, not guessed.

**Ground everything in the paper.** Use the prose + figure/table descriptions to confirm the
reference arm and direction. Do not invent comparisons the paper does not make.

## Output

A JSON array only (no prose), each element exactly:

```json
{
  "cio_id": "CIO_001",
  "unit": "U017",
  "context": ["C110", "C111"],
  "intervention": "I49",
  "reference": "C113",
  "eval_metric": "E8",
  "pattern": "P19",
  "direction": "up",
  "pattern_class": "comparison",
  "provenance": { "location": "Table 1", "source_span": "S189" },
  "status": "observed"
}
```
