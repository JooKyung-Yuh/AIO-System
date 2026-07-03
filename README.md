# AIO-System

**AIO PoC - Diagnostic World Model from Papers**

Proof-of-concept for **AIO** (Assumption-Intervention-Observable): compiling ML papers
into a factor graph that a reasoning agent can later query - not a RAG index, but a
world model that records *what was done, what was observed, why the authors think so,
and which beliefs each observation supports or weakens*.

## Core ideas

- **Words vs. sentences.** Canonical nodes (A/I/O/M/C) are the vocabulary; a *factor*
  is a sentence written with them. Vocabulary alone is retrieval - sentences make it a
  world model.
- **Votes are stored, beliefs are derived.** Each factor casts votes
  (`belief_update`: strengthen/weaken) at mechanism/assumption nodes. The
  supported / contested / weakened label lives only in the registry and is recomputed
  from the full record log - never edited by hand or by an LLM.
- **Append-only.** Records are immutable. New evidence (e.g., a 2018 rebuttal) is a new
  card; `git diff registry.json` then shows beliefs flipping while no card changed.
- **Observable = metric + pattern.** `O[E_xxx, P_xxx]` - results measured with
  different metrics are *incomparable*, not contradictory.
- **Expected outcomes are quoted-only.** Branch predictions enter a card only when the
  paper states them verbatim; otherwise `null`. No invented implications.

## Status

Bootstrap (base 0). Pilot paper: Batch Normalization (arXiv:1502.03167).
Current scope: Layer 1 (node extraction) -> Layer 2 (canonicalize, table-first factor
assembly, first graph) -> belief tally -> static world-model SVG. Query mode comes later.

## Layout

- `data/papers/`: source texts
- `data/records/`: factor cards (append-only)
- `registry/`: vocabulary + derived beliefs
- `schema/`: versioned factor card schema
- `prompts/`: versioned extraction prompts
- `scripts/`: validate / belief / viz
- `docs/`: key ideas & decision log

## Pipeline

extract (LLM, refs required, ambiguity flagged) -> **human check** -> canonicalize ->
**human check** -> fill C/I/O from tables -> attach A/M + votes -> **human check** ->
tally beliefs -> render graph -> **human check**

Every stage gates on researcher review (PR approval). CI grows with the repo:
JSON sanity -> schema validation -> registry freshness -> viz artifact.
