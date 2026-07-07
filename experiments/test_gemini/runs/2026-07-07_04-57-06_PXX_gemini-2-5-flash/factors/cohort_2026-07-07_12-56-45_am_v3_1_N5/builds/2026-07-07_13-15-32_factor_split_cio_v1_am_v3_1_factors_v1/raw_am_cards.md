```json
[
  {
    "am_id": "AM_001",
    "kind": "mechanism",
    "node": "M7",
    "aliases": ["M50"],
    "gloss": "Visual learning directly enables abstraction and inference without language.",
    "provenance": { "location": "Section 1" }
  },
  {
    "am_id": "AM_002",
    "kind": "mechanism",
    "node": "M10",
    "aliases": ["M17", "M23", "M34", "M36"],
    "gloss": "Canvas patchification enriches data space, reduces overfitting, learns spatial priors.",
    "provenance": { "location": "Section 1" }
  },
  {
    "am_id": "AM_003",
    "kind": "mechanism",
    "node": "M15",
    "aliases": [],
    "gloss": "Demo pairs at inference enable test-time training.",
    "provenance": { "location": "Section 3.1" }
  },
  {
    "am_id": "AM_004",
    "kind": "mechanism",
    "node": "M16",
    "aliases": ["M19", "M20"],
    "gloss": "Canvas enables augmentations to learn geometric transformation invariance.",
    "provenance": { "location": "Section 3.3" }
  },
  {
    "am_id": "AM_005",
    "kind": "mechanism",
    "node": "M27",
    "aliases": ["M28", "M33", "M42"],
    "gloss": "Majority voting consolidates multi-view predictions to improve accuracy.",
    "provenance": { "location": "Section 3.5" }
  },
  {
    "am_id": "AM_006",
    "kind": "mechanism",
    "node": "M29",
    "aliases": [],
    "gloss": "Average pooling aggregates multi-pixel predictions for single output location.",
    "provenance": { "location": "Section 3.5" }
  },
  {
    "am_id": "AM_007",
    "kind": "mechanism",
    "node": "M40",
    "aliases": [],
    "gloss": "Offline training learns visual common sense from the training set.",
    "provenance": { "location": "Section 5.2" }
  },
  {
    "am_id": "AM_008",
    "kind": "mechanism",
    "node": "M44",
    "aliases": [],
    "gloss": "Attention maps reveal correct pixel-to-pixel reasoning.",
    "provenance": { "location": "Section 6" }
  },
  {
    "am_id": "AM_009",
    "kind": "mechanism",
    "node": "M46",
    "aliases": ["M47", "M59", "M60", "M61", "M62"],
    "gloss": "Different layers focus on distinct structures and task-specific patterns.",
    "provenance": { "location": "Section 6" }
  },
  {
    "am_id": "AM_010",
    "kind": "mechanism",
    "node": "M48",
    "aliases": [],
    "gloss": "Task embedding visualization suggests learning relations between tasks.",
    "provenance": { "location": "Section 6" }
  },
  {
    "am_id": "AM_011",
    "kind": "mechanism",
    "node": "M69",
    "aliases": ["M70"],
    "gloss": "Test-time training refines color and spatial arrangement, adapting to tasks.",
    "provenance": { "location": "Figure 22 caption" }
  },
  {
    "am_id": "AM_012",
    "kind": "assumption",
    "node": "A6",
    "aliases": [],
    "gloss": "ARC colors are not real-world, making bilinear interpolation meaningless.",
    "provenance": { "location": "Section 3.3" }
  },
  {
    "am_id": "AM_013",
    "kind": "assumption",
    "node": "A15",
    "aliases": [],
    "gloss": "Larger models can overfit, hindering generalization in current settings.",
    "provenance": { "location": "Section 5.2" }
  },
  {
    "am_id": "AM_014",
    "kind": "assumption",
    "node": "A16",
    "aliases": ["A19"],
    "gloss": "Joint TTT assumes multiple test tasks available simultaneously.",
    "provenance": { "location": "Section 5.2" }
  },
  {
    "am_id": "AM_015",
    "kind": "assumption",
    "node": "A18",
    "aliases": [],
    "gloss": "Single pixel errors invalidate entire ARC predictions.",
    "provenance": { "location": "Section 5.2" }
  },
  {
    "am_id": "AM_016",
    "kind": "assumption",
    "node": "A20",
    "aliases": ["A21", "A22"],
    "gloss": "Some ARC tasks are ambiguous, admitting multiple plausible rules.",
    "provenance": { "location": "Section C.2" }
  }
]
```