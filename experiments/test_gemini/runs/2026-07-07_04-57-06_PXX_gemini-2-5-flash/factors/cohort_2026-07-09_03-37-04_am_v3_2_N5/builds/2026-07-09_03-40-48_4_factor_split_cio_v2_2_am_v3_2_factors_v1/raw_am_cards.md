```json
[
  {
    "am_id": "AM_001",
    "kind": "mechanism",
    "node": "M7",
    "aliases": ["M50"],
    "gloss": "Visual learning enables abstraction/inference without language.",
    "provenance": { "location": "Section 1" }
  },
  {
    "am_id": "AM_002",
    "kind": "mechanism",
    "node": "M10",
    "aliases": ["M17", "M34", "M36"],
    "gloss": "Canvas patchification enriches data, reduces overfitting, encourages spatial priors.",
    "provenance": { "location": "Section 1" }
  },
  {
    "am_id": "AM_003",
    "kind": "mechanism",
    "node": "M16",
    "aliases": ["M19"],
    "gloss": "Canvas formulation enables augmentations for translation/scale invariance.",
    "provenance": { "location": "Section 3.3" }
  },
  {
    "am_id": "AM_004",
    "kind": "mechanism",
    "node": "M20",
    "aliases": [],
    "gloss": "Augmentations encourage learning mappings invariant to geometric transformations.",
    "provenance": { "location": "Section 3.3" }
  },
  {
    "am_id": "AM_005",
    "kind": "mechanism",
    "node": "M23",
    "aliases": [],
    "gloss": "Patchification provides locality and translation invariance inductive biases.",
    "provenance": { "location": "Section 3.3" }
  },
  {
    "am_id": "AM_006",
    "kind": "mechanism",
    "node": "M25",
    "aliases": ["M24"],
    "gloss": "Explicit 2D positional modeling preserves image structure.",
    "provenance": { "location": "Section 3.3" }
  },
  {
    "am_id": "AM_007",
    "kind": "mechanism",
    "node": "M27",
    "aliases": ["M28", "M33"],
    "gloss": "Majority voting consolidates predictions from different views.",
    "provenance": { "location": "Section 3.5" }
  },
  {
    "am_id": "AM_008",
    "kind": "mechanism",
    "node": "M29",
    "aliases": [],
    "gloss": "Average pooling aggregates predictions for raw grid locations.",
    "provenance": { "location": "Section 3.5" }
  },
  {
    "am_id": "AM_009",
    "kind": "mechanism",
    "node": "M37",
    "aliases": [],
    "gloss": "ViT lacks inductive bias for scale invariance.",
    "provenance": { "location": "Section 5.1" }
  },
  {
    "am_id": "AM_010",
    "kind": "mechanism",
    "node": "M40",
    "aliases": [],
    "gloss": "Visual common sense is learned from offline training data.",
    "provenance": { "location": "Section 5.2" }
  },
  {
    "am_id": "AM_011",
    "kind": "mechanism",
    "node": "M41",
    "aliases": [],
    "gloss": "Some tasks are solvable from scratch (tabula rasa).",
    "provenance": { "location": "Section 5.2" }
  },
  {
    "am_id": "AM_012",
    "kind": "mechanism",
    "node": "M44",
    "aliases": [],
    "gloss": "Attention maps reveal pixel-to-pixel reasoning relationships.",
    "provenance": { "location": "Section 6" }
  },
  {
    "am_id": "AM_013",
    "kind": "mechanism",
    "node": "M46",
    "aliases": [],
    "gloss": "Early layer attention reflects pattern core influence.",
    "provenance": { "location": "Section 6" }
  },
  {
    "am_id": "AM_014",
    "kind": "mechanism",
    "node": "M47",
    "aliases": [],
    "gloss": "Later layer attention reflects rule for extending pixels.",
    "provenance": { "location": "Section 6" }
  },
  {
    "am_id": "AM_015",
    "kind": "mechanism",
    "node": "M48",
    "aliases": [],
    "gloss": "Task embedding visualization suggests learning inter-task relations.",
    "provenance": { "location": "Section 6" }
  },
  {
    "am_id": "AM_016",
    "kind": "mechanism",
    "node": "M54",
    "aliases": [],
    "gloss": "Attention masks and loss focus improve foreground attention/accuracy.",
    "provenance": { "location": "Section A.3" }
  },
  {
    "am_id": "AM_017",
    "kind": "mechanism",
    "node": "M57",
    "aliases": [],
    "gloss": "Correct predictions exist in views but are outvoted.",
    "provenance": { "location": "Section B.2" }
  },
  {
    "am_id": "AM_018",
    "kind": "mechanism",
    "node": "M58",
    "aliases": [],
    "gloss": "Model handles ambiguity by proposing multiple rule interpretations.",
    "provenance": { "location": "Section C.2" }
  },
  {
    "am_id": "AM_019",
    "kind": "mechanism",
    "node": "M70",
    "aliases": [],
    "gloss": "TTT visualization shows model adapting to task-specific transformations.",
    "provenance": { "location": "Figure 22 caption" }
  },
  {
    "am_id": "AM_020",
    "kind": "assumption",
    "node": "A11",
    "aliases": [],
    "gloss": "Multi-view inference cost is negligible compared to TTT.",
    "provenance": { "location": "Section 3.5" }
  },
  {
    "am_id": "AM_021",
    "kind": "assumption",
    "node": "A15",
    "aliases": [],
    "gloss": "Larger models beyond current regime lead to overfitting.",
    "provenance": { "location": "Section 5.2" }
  },
  {
    "am_id": "AM_022",
    "kind": "assumption",
    "node": "A19",
    "aliases": ["A16"],
    "gloss": "Multiple unseen tasks cannot be assumed simultaneously.",
    "provenance": { "location": "Footnote 3" }
  },
  {
    "am_id": "AM_023",
    "kind": "assumption",
    "node": "A18",
    "aliases": [],
    "gloss": "Single pixel error invalidates entire ARC prediction.",
    "provenance": { "location": "Section 5.2" }
  },
  {
    "am_id": "AM_024",
    "kind": "assumption",
    "node": "A20",
    "aliases": [],
    "gloss": "Some ARC tasks admit multiple plausible rules.",
    "provenance": { "location": "Section C.2" }
  }
]
```