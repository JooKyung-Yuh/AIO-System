You are drawing **belief_update edges** — the core of an AIO factor graph. Each edge says that one
measured observation (a CIO card) **strengthens or weakens** one mechanism or assumption (an AM
card), but ONLY where the paper makes that link explicit AND the belief is the **most specific** one
the result bears on. This is a matching task over already-clean cards; you are not extracting
anything new. **Prefer FEWER, SHARPER edges over many thematic ones** — an observation with no edge
is a valid factor.

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

For each CIO card, find the AM card(s) the paper EXPLICITLY ties to **that specific observation** —
where the paper states this particular result *shows / because / suggests / indicates / implies* the
mechanism, or that the observation *relies on / holds under* the assumption. Emit an edge only when a
precise **result → claim** connection is stated for THIS result.

Rules (apply every one before emitting an edge):

1. **Explicit only.** Emit an edge only when the paper text makes the connection for this result; do
   not infer a link from topical similarity. No explicit interpretation -> no edge.

2. **Specificity first.** Link a result to the **MOST SPECIFIC** mechanism/assumption it bears on. A
   paper-level thesis / headline claim — a sweeping conclusion (e.g. "X enables Y", "our approach
   works") that *nearly every* result in the paper could be said to support — is a link target ONLY
   when NO specific mechanism/assumption fits. Never funnel many different results into one broad
   thesis.

3. **Evidence must name THIS result.** The `evidence` quote must reference this CIO's own specific
   result — its metric, number, comparison arm, or the figure/table finding it reports — AND state
   the causal/support connection. **Do NOT reuse the same generic thesis sentence as the evidence
   for several different observations.** If the only quote you can find is a broad thesis statement
   that does not mention THIS result, emit NO edge.

4. **Local / provenance.** Draw the evidence from the SAME table / figure / section the observation
   comes from (its own explanation). Do not reach across the paper for a distant thesis sentence to
   interpret a local result.

5. **No aggregate -> component.** Do NOT attach a total / cumulative / aggregate result (e.g. "all
   priors together give +27.7") to a single component mechanism. An aggregate result supports the
   aggregate claim, not one of its parts.

6. **When ambiguous, no link.** If you cannot name a specific belief with a specific supporting
   quote, omit the edge — do not attach the result to a broad AM. A bare observation is a valid
   factor on its own.

7. **Many-to-one, but earned.** One AM may still be strengthened by several observations, and one
   observation may support more than one belief — but each edge must independently pass rules 1-6.
   Cap yourself at ~2 edges per observation unless each is independently explicit and specific.

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
  "evidence": "<=20-word quote that names THIS result and states the link (not a generic thesis line)"
}
```
