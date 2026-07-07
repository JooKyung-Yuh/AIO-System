```json
[
  {
    "am_id": "AM_001",
    "kind": "mechanism",
    "node": "M7",
    "aliases": [],
    "gloss": "Abstraction can arise directly from visual learning alone.",
    "provenance": {
      "location": "Section 1"
    }
  },
  {
    "am_id": "AM_002",
    "kind": "mechanism",
    "node": "M10",
    "aliases": ["M17", "M34", "M36"],
    "gloss": "Canvas patchification enriches data space, reducing overfitting and encouraging spatial priors.",
    "provenance": {
      "location": "Section 1"
    }
  },
  {
    "am_id": "AM_003",
    "kind": "mechanism",
    "node": "M15",
    "aliases": [],
    "gloss": "ARC's demo pairs at inference enable test-time training.",
    "provenance": {
      "location": "Section 3.1"
    }
  },
  {
    "am_id": "AM_004",
    "kind": "mechanism",
    "node": "M20",
    "aliases": ["M16", "M19", "M22"],
    "gloss": "Data augmentations encourage learning geometric transformation invariants, crucial for generalization.",
    "provenance": {
      "location": "Section 3.3"
    }
  },
  {
    "am_id": "AM_005",
    "kind": "mechanism",
    "node": "M21",
    "aliases": [],
    "gloss": "ARC's non-real-world colors make bilinear interpolation meaningless.",
    "provenance": {
      "location": "Section 3.3"
    }
  },
  {
    "am_id": "AM_006",
    "kind": "mechanism",
    "node": "M23",
    "aliases": [],
    "gloss": "Patchification incorporates locality and translation invariance inductive biases.",
    "provenance": {
      "location": "Section 3.3"
    }
  },
  {
    "am_id": "AM_007",
    "kind": "mechanism",
    "node": "M27",
    "aliases": ["M28", "M33", "M42"],
    "gloss": "Multi-view predictions are consolidated by majority voting.",
    "provenance": {
      "location": "Section 3.5"
    }
  },
  {
    "am_id": "AM_008",
    "kind": "mechanism",
    "node": "M29",
    "aliases": [],
    "gloss": "Predictions from multiple canvas pixels are aggregated by average pooling.",
    "provenance": {
      "location": "Section 3.5"
    }
  },
  {
    "am_id": "AM_009",
    "kind": "mechanism",
    "node": "M37",
    "aliases": [],
    "gloss": "ViT's lack of scale invariance inductive bias explains scale augmentation gain.",
    "provenance": {
      "location": "Section 5.1"
    }
  },
  {
    "am_id": "AM_010",
    "kind": "mechanism",
    "node": "M53",
    "aliases": [],
    "gloss": "Attention masks set softmax scores to zero for background pixels.",
    "provenance": {
      "location": "Section A.3"
    }
  },
  {
    "am_id": "AM_011",
    "kind": "mechanism",
    "node": "M54",
    "aliases": [],
    "gloss": "Designs encourage foreground attention, improving accuracy.",
    "provenance": {
      "location": "Section A.3"
    }
  },
  {
    "am_id": "AM_012",
    "kind": "mechanism",
    "node": "M58",
    "aliases": [],
    "gloss": "Model produces multiple rule interpretations for ambiguous tasks.",
    "provenance": {
      "location": "Section C.2"
    }
  },
  {
    "am_id": "AM_013",
    "kind": "mechanism",
    "node": "M59",
    "aliases": ["M60", "M61", "M62"],
    "gloss": "Different layers specialize in focusing on different structures and contexts.",
    "provenance": {
      "location": "Figure 20"
    }
  },
  {
    "am_id": "AM_014",
    "kind": "mechanism",
    "node": "M70",
    "aliases": ["M69"],
    "gloss": "Test-time training adapts to task-specific transformations by refining predictions.",
    "provenance": {
      "location": "Figure 22 caption"
    }
  },
  {
    "am_id": "AM_015",
    "kind": "assumption",
    "node": "A6",
    "aliases": [],
    "gloss": "ARC colors do not correspond to real-world colors.",
    "provenance": {
      "location": "Section 3.3"
    }
  },
  {
    "am_id": "AM_016",
    "kind": "assumption",
    "node": "A8",
    "aliases": ["A9"],
    "gloss": "ARC tasks have very few demonstration pairs.",
    "provenance": {
      "location": "Section 3.5"
    }
  },
  {
    "am_id": "AM_017",
    "kind": "assumption",
    "node": "A10",
    "aliases": [],
    "gloss": "Rescaling on canvas causes multiple pixels to predict one output location.",
    "provenance": {
      "location": "Section 3.5"
    }
  },
  {
    "am_id": "AM_018",
    "kind": "assumption",
    "node": "A11",
    "aliases": [],
    "gloss": "Multi-view inference cost is negligible compared to test-time training.",
    "provenance": {
      "location": "Section 3.5"
    }
  },
  {
    "am_id": "AM_019",
    "kind": "assumption",
    "node": "A12",
    "aliases": [],
    "gloss": "Auxiliary tasks are assumed translation and scale invariant.",
    "provenance": {
      "location": "Section 4"
    }
  },
  {
    "am_id": "AM_020",
    "kind": "assumption",
    "node": "A13",
    "aliases": [],
    "gloss": "Majority voting consistency requires identical output grids.",
    "provenance": {
      "location": "Footnote 2"
    }
  },
  {
    "am_id": "AM_021",
    "kind": "assumption",
    "node": "A14",
    "aliases": [],
    "gloss": "Constraining 2x2 patches to one raw pixel equals 1x1 patches on smaller canvas.",
    "provenance": {
      "location": "Section 5.1"
    }
  },
  {
    "am_id": "AM_022",
    "kind": "assumption",
    "node": "A16",
    "aliases": [],
    "gloss": "Joint TTT assumes multiple test tasks available simultaneously.",
    "provenance": {
      "location": "Section 5.2"
    }
  },
  {
    "am_id": "AM_023",
    "kind": "assumption",
    "node": "A17",
    "aliases": [],
    "gloss": "Single-view inference cannot produce multiple predictions.",
    "provenance": {
      "location": "Section 5.2"
    }
  },
  {
    "am_id": "AM_024",
    "kind": "assumption",
    "node": "A18",
    "aliases": [],
    "gloss": "A single pixel mistake in ARC renders the entire prediction incorrect.",
    "provenance": {
      "location": "Section 5.2"
    }
  },
  {
    "am_id": "AM_025",
    "kind": "assumption",
    "node": "A19",
    "aliases": [],
    "gloss": "Multiple unseen tasks cannot be assumed available simultaneously.",
    "provenance": {
      "location": "Footnote 3"
    }
  },
  {
    "am_id": "AM_026",
    "kind": "assumption",
    "node": "A20",
    "aliases": ["A21"],
    "gloss": "Some ARC tasks admit multiple plausible explanations or rules.",
    "provenance": {
      "location": "Section C.2"
    }
  },
  {
    "am_id": "AM_027",
    "kind": "assumption",
    "node": "A22",
    "aliases": [],
    "gloss": "Ambiguity exists in specific task rules, e.g., 'touching' vs 'going through'.",
    "provenance": {
      "location": "Figure 19"
    }
  }
]
```