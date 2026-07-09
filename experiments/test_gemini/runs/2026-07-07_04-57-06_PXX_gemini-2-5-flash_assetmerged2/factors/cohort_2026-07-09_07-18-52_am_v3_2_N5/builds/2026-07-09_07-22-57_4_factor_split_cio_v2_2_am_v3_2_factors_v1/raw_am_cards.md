```json
[
  {
    "am_id": "AM_001",
    "kind": "mechanism",
    "node": "M7",
    "aliases": ["M50"],
    "gloss": "Visual learning directly yields abstraction/inference, no language needed.",
    "provenance": { "location": "Section 1" }
  },
  {
    "am_id": "AM_002",
    "kind": "mechanism",
    "node": "M10",
    "aliases": ["M17", "M18", "M34", "M36"],
    "gloss": "Canvas patchification increases input diversity, reducing overfitting and encouraging spatial prior learning.",
    "provenance": { "location": "Section 1" }
  },
  {
    "am_id": "AM_003",
    "kind": "mechanism",
    "node": "M16",
    "aliases": ["M19", "M20", "M22", "M37"],
    "gloss": "Canvas enables augmentations, fostering translation/scale invariance for generalization.",
    "provenance": { "location": "Section 3.3" }
  },
  {
    "am_id": "AM_004",
    "kind": "mechanism",
    "node": "M23",
    "aliases": [],
    "gloss": "Patchification/convolution introduces locality and translation invariance inductive biases.",
    "provenance": { "location": "Section 3.3" }
  },
  {
    "am_id": "AM_005",
    "kind": "mechanism",
    "node": "M24",
    "aliases": ["M25"],
    "gloss": "Naïve 1D patch sequencing loses 2D structure, necessitating 2D positional embeddings.",
    "provenance": { "location": "Section 3.3" }
  },
  {
    "am_id": "AM_006",
    "kind": "mechanism",
    "node": "M39",
    "aliases": [],
    "gloss": "Increasing model size improves accuracy by enabling better fitting.",
    "provenance": { "location": "Section 5.2" }
  },
  {
    "am_id": "AM_007",
    "kind": "assumption",
    "node": "A15",
    "aliases": [],
    "gloss": "Excessively large models in current settings lead to overfitting.",
    "provenance": { "location": "Section 5.2" }
  },
  {
    "am_id": "AM_008",
    "kind": "mechanism",
    "node": "M40",
    "aliases": [],
    "gloss": "Offline training enables learning visual common sense, improving TTT.",
    "provenance": { "location": "Section 5.2" }
  },
  {
    "am_id": "AM_009",
    "kind": "mechanism",
    "node": "M54",
    "aliases": [],
    "gloss": "Attention masks encourage foreground focus, improving accuracy.",
    "provenance": { "location": "Section A.3" }
  },
  {
    "am_id": "AM_010",
    "kind": "assumption",
    "node": "A20",
    "aliases": ["A22"],
    "gloss": "Some ARC tasks have multiple plausible explanations/rules.",
    "provenance": { "location": "Section C.2" }
  },
  {
    "am_id": "AM_011",
    "kind": "mechanism",
    "node": "M69",
    "aliases": ["M70"],
    "gloss": "Test-time training refines color and spatial arrangement, adapting to task transformations.",
    "provenance": { "location": "Figure 22 caption" }
  }
]
```