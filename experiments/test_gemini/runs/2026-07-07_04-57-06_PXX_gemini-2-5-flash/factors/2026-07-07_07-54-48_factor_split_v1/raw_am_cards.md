```json
[
  {
    "am_id": "AM_001",
    "kind": "mechanism",
    "node": "M7",
    "aliases": [],
    "gloss": "Abstraction and inference arise directly from visual learning.",
    "provenance": {
      "location": "Section 1"
    }
  },
  {
    "am_id": "AM_002",
    "kind": "mechanism",
    "node": "M10",
    "aliases": [
      "M17",
      "M34",
      "M36"
    ],
    "gloss": "Canvas patchification reduces overfitting, encourages spatial priors via diverse color combinations.",
    "provenance": {
      "location": "Section 1"
    }
  },
  {
    "am_id": "AM_003",
    "kind": "assumption",
    "node": "A2",
    "aliases": [],
    "gloss": "ARC protocol requires few-shot, cross-task generalization.",
    "provenance": {
      "location": "Section 2"
    }
  },
  {
    "am_id": "AM_004",
    "kind": "mechanism",
    "node": "M15",
    "aliases": [],
    "gloss": "New demo pairs at inference enable test-time training.",
    "provenance": {
      "location": "Section 3.1"
    }
  },
  {
    "am_id": "AM_005",
    "kind": "mechanism",
    "node": "M16",
    "aliases": [
      "M19"
    ],
    "gloss": "Canvas formulation accommodates augmentations, introducing translation and scale invariance.",
    "provenance": {
      "location": "Section 3.3"
    }
  },
  {
    "am_id": "AM_006",
    "kind": "mechanism",
    "node": "M20",
    "aliases": [],
    "gloss": "Data augmentations encourage learning mappings invariant to geometric transformations.",
    "provenance": {
      "location": "Section 3.3"
    }
  },
  {
    "am_id": "AM_007",
    "kind": "assumption",
    "node": "A6",
    "aliases": [],
    "gloss": "ARC colors do not correspond to real-world colors.",
    "provenance": {
      "location": "Section 3.3"
    }
  },
  {
    "am_id": "AM_008",
    "kind": "mechanism",
    "node": "M21",
    "aliases": [],
    "gloss": "ARC's non-real-world colors make other interpolations meaningless.",
    "provenance": {
      "location": "Section 3.3"
    }
  },
  {
    "am_id": "AM_009",
    "kind": "assumption",
    "node": "A7",
    "aliases": [],
    "gloss": "All pixels must remain visible during translation augmentation.",
    "provenance": {
      "location": "Section 3.3"
    }
  },
  {
    "am_id": "AM_010",
    "kind": "mechanism",
    "node": "M23",
    "aliases": [],
    "gloss": "Patchification incorporates locality and translation invariance inductive biases.",
    "provenance": {
      "location": "Section 3.3"
    }
  },
  {
    "am_id": "AM_011",
    "kind": "assumption",
    "node": "A8",
    "aliases": [
      "A9"
    ],
    "gloss": "Few demo pairs (2-4) are available for test-time training.",
    "provenance": {
      "location": "Section 3.5"
    }
  },
  {
    "am_id": "AM_012",
    "kind": "assumption",
    "node": "A10",
    "aliases": [],
    "gloss": "Rescaling causes multiple canvas pixels to predict one raw grid location.",
    "provenance": {
      "location": "Section 3.5"
    }
  },
  {
    "am_id": "AM_013",
    "kind": "mechanism",
    "node": "M29",
    "aliases": [],
    "gloss": "Average pooling aggregates multiple canvas pixel predictions for one raw location.",
    "provenance": {
      "location": "Section 3.5"
    }
  },
  {
    "am_id": "AM_014",
    "kind": "assumption",
    "node": "A11",
    "aliases": [],
    "gloss": "Multi-view inference cost is negligible compared to test-time training.",
    "provenance": {
      "location": "Section 3.5"
    }
  },
  {
    "am_id": "AM_015",
    "kind": "assumption",
    "node": "A12",
    "aliases": [],
    "gloss": "Auxiliary tasks are assumed translation and scale invariant.",
    "provenance": {
      "location": "Section 4"
    }
  },
  {
    "am_id": "AM_016",
    "kind": "assumption",
    "node": "A13",
    "aliases": [],
    "gloss": "Majority voting requires identical grids for consistency.",
    "provenance": {
      "location": "Footnote 2"
    }
  },
  {
    "am_id": "AM_017",
    "kind": "mechanism",
    "node": "M33",
    "aliases": [],
    "gloss": "Majority voting selects grid consistent with most other outputs.",
    "provenance": {
      "location": "Footnote 2"
    }
  },
  {
    "am_id": "AM_018",
    "kind": "mechanism",
    "node": "M40",
    "aliases": [],
    "gloss": "Offline training enables learning visual common sense from data.",
    "provenance": {
      "location": "Section 5.2"
    }
  },
  {
    "am_id": "AM_019",
    "kind": "assumption",
    "node": "A18",
    "aliases": [],
    "gloss": "Single pixel error invalidates entire ARC prediction.",
    "provenance": {
      "location": "Section 5.2"
    }
  },
  {
    "am_id": "AM_020",
    "kind": "mechanism",
    "node": "M53",
    "aliases": [],
    "gloss": "Attention masks zero softmax scores for background key positions.",
    "provenance": {
      "location": "Section A.3"
    }
  },
  {
    "am_id": "AM_021",
    "kind": "mechanism",
    "node": "M54",
    "aliases": [],
    "gloss": "Attention masks encourage foreground focus, improving accuracy.",
    "provenance": {
      "location": "Section A.3"
    }
  },
  {
    "am_id": "AM_022",
    "kind": "assumption",
    "node": "A21",
    "aliases": [],
    "gloss": "Most ARC tasks are unambiguous.",
    "provenance": {
      "location": "Figure 19"
    }
  }
]
```