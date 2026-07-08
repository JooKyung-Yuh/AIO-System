```json
[
  {
    "am_id": "AM_001",
    "kind": "mechanism",
    "node": "M7",
    "aliases": ["M50"],
    "gloss": "abstraction/inference from visual learning without language",
    "provenance": { "location": "Section 1" }
  },
  {
    "am_id": "AM_002",
    "kind": "mechanism",
    "node": "M10",
    "aliases": ["M17", "M18", "M34", "M36"],
    "gloss": "canvas patchification enriches data, reduces overfitting, learns spatial priors",
    "provenance": { "location": "Section 1" }
  },
  {
    "am_id": "AM_003",
    "kind": "mechanism",
    "node": "M16",
    "aliases": ["M19", "M20", "M22"],
    "gloss": "canvas/augmentations introduce translation/scale invariance for generalization",
    "provenance": { "location": "Section 3.3" }
  },
  {
    "am_id": "AM_004",
    "kind": "mechanism",
    "node": "M23",
    "aliases": ["M24", "M25"],
    "gloss": "patchification/2D pos embed incorporate visual inductive biases",
    "provenance": { "location": "Section 3.3" }
  },
  {
    "am_id": "AM_005",
    "kind": "mechanism",
    "node": "M27",
    "aliases": ["M28", "M32", "M33", "M42"],
    "gloss": "majority voting consolidates multi-view predictions for accuracy",
    "provenance": { "location": "Section 3.5" }
  },
  {
    "am_id": "AM_006",
    "kind": "mechanism",
    "node": "M29",
    "aliases": [],
    "gloss": "average pooling aggregates multi-pixel canvas predictions",
    "provenance": { "location": "Section 3.5" }
  },
  {
    "am_id": "AM_007",
    "kind": "mechanism",
    "node": "M40",
    "aliases": [],
    "gloss": "visual common sense learned from training data",
    "provenance": { "location": "Section 5.2" }
  },
  {
    "am_id": "AM_008",
    "kind": "mechanism",
    "node": "M44",
    "aliases": [],
    "gloss": "model reasons by attending to source-target pixel relationships",
    "provenance": { "location": "Section 6" }
  },
  {
    "am_id": "AM_009",
    "kind": "mechanism",
    "node": "M48",
    "aliases": [],
    "gloss": "method learns relations between different tasks",
    "provenance": { "location": "Section 6" }
  },
  {
    "am_id": "AM_010",
    "kind": "mechanism",
    "node": "M54",
    "aliases": [],
    "gloss": "attention masks encourage foreground focus, improving accuracy",
    "provenance": { "location": "Section A.3" }
  },
  {
    "am_id": "AM_011",
    "kind": "mechanism",
    "node": "M59",
    "aliases": ["M60", "M61", "M62", "M63", "M64", "M65", "M66", "M67", "M68"],
    "gloss": "Transformer layers focus on different structures by depth",
    "provenance": { "location": "Figure 20" }
  },
  {
    "am_id": "AM_012",
    "kind": "assumption",
    "node": "A6",
    "aliases": [],
    "gloss": "ARC colors are not real-world colors",
    "provenance": { "location": "Section 3.3" }
  },
  {
    "am_id": "AM_013",
    "kind": "assumption",
    "node": "A12",
    "aliases": [],
    "gloss": "auxiliary tasks are translation/scale invariant",
    "provenance": { "location": "Section 4" }
  },
  {
    "am_id": "AM_014",
    "kind": "assumption",
    "node": "A15",
    "aliases": [],
    "gloss": "larger models in current setting lead to overfitting",
    "provenance": { "location": "Section 5.2" }
  },
  {
    "am_id": "AM_015",
    "kind": "assumption",
    "node": "A18",
    "aliases": [],
    "gloss": "single pixel error makes ARC prediction incorrect",
    "provenance": { "location": "Section 5.2" }
  },
  {
    "am_id": "AM_016",
    "kind": "assumption",
    "node": "A21",
    "aliases": ["A20"],
    "gloss": "most ARC tasks unambiguous, some have multiple plausible rules",
    "provenance": { "location": "Figure 19" }
  }
]
```