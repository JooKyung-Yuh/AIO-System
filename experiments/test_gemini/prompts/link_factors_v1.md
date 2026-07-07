You are drawing **belief_update edges** — the core of an AIO factor graph. Each edge says that one
measured observation (a CIO card) **strengthens or weakens** one mechanism or assumption (an AM
card), but ONLY where the paper makes that link explicit. This is a matching task over already-clean
cards; you are not extracting anything new.

paper_id: {paper_id}
paper_title_hint: {paper_title_hint}

You are given the paper (to verify what it explicitly claims), the CIO observation cards, and the AM
belief-target cards.

--- PAPER: PROSE TRANSCRIPTION ---
{paper_text}
--- PAPER: FIGURES & TABLES ---
{assets}
--- CIO CARDS (observations) ---
{cio_cards}
--- AM CARDS (mechanisms / assumptions) ---
{am_cards}
--- END INPUT ---

## Your task

For each CIO card, find the AM card(s) the paper EXPLICITLY ties to that observation — the paper
states this result *shows / because / suggests / indicates / demonstrates / implies* the mechanism,
or that the observation *relies on / holds under* the assumption.

Rules:
- **Explicit only.** Emit an edge only when the paper text makes the connection; do not infer a link
  from mere topical similarity. If an observation has no explicit interpretation in the paper, emit
  no edge for it — a bare observation is a valid factor on its own.
- **Many-to-one is expected.** One observation may support several AM nodes, and one AM node
  (especially the headline thesis) may be strengthened by many observations. Emit every explicit
  edge; do not collapse them.
- **direction**: `strengthen` if the result supports the mechanism/assumption, `weaken` if it
  undercuts it.
- Reference the CIO by its `cio_id` and the AM by its `am_id`.

## Output

A JSON array only (no prose), each element exactly:

```json
{
  "source_cio": "CIO_003",
  "target_am": "AM_001",
  "direction": "strengthen",
  "explicit": true,
  "evidence": "<=20-word quote or close paraphrase from the paper that states the link"
}
```
