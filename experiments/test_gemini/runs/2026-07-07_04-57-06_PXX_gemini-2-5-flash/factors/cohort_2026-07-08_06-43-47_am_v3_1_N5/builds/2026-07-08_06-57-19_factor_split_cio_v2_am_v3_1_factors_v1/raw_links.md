```json
[
  {
    "source_cio": "CIO_004",
    "target_am": "AM_008",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Our VARC with 18M parameters is ~10 points better than TRM on ARC-1, a >20% relative improvement."
  },
  {
    "source_cio": "CIO_008",
    "target_am": "AM_006",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Extending from 1D positional embedding to its 2D counterpart is beneficial: see Fig. 7(b)(c)."
  },
  {
    "source_cio": "CIO_009",
    "target_am": "AM_006",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Extending from 1D positional embedding to its 2D counterpart is beneficial: see Fig. 7(b)(c)."
  },
  {
    "source_cio": "CIO_010",
    "target_am": "AM_006",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "we replace the 2D ROPE... with a 1D ROPE and observe a degradation of 3.5 points."
  },
  {
    "source_cio": "CIO_011",
    "target_am": "AM_002",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "each patch can cover multiple colors... which substantially enriches the data space for learning."
  },
  {
    "source_cio": "CIO_012",
    "target_am": "AM_003",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "In Fig. 7(e), we apply fully flexible translation augmentation on the canvas... yields an additional gain of 2.9 points."
  },
  {
    "source_cio": "CIO_012",
    "target_am": "AM_004",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Theses data augmentations encourage the model to learn underlying mappings invariant to geometric transformations."
  },
  {
    "source_cio": "CIO_013",
    "target_am": "AM_003",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "we further apply the scale augmentation enabled by the concept of canvas. Scale augmentation yields a substantial gain."
  },
  {
    "source_cio": "CIO_013",
    "target_am": "AM_004",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Theses data augmentations encourage the model to learn underlying mappings invariant to geometric transformations."
  },
  {
    "source_cio": "CIO_013",
    "target_am": "AM_007",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Scale augmentation yields a substantial gain... ViT architecture has little to no inductive bias about scale invariance."
  },
  {
    "source_cio": "CIO_015",
    "target_am": "AM_009",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "offline training greatly improves the performance of TTT, suggesting that common sense... can be learned."
  },
  {
    "source_cio": "CIO_016",
    "target_am": "AM_010",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "even without offline training, our TTT strategy can achieve nontrivial accuracy... suggesting that some tasks... can be solved tabula rasa."
  },
  {
    "source_cio": "CIO_017",
    "target_am": "AM_018",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "performing TTT independently... yields substantially better performance... than doing so jointly... which relies on a stronger assumption."
  },
  {
    "source_cio": "CIO_018",
    "target_am": "AM_017",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Going beyond this regime can lead to overfitting in our current setting, as shown in Tab. 1 for the 66M ViT model."
  },
  {
    "source_cio": "CIO_021",
    "target_am": "AM_019",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "in ARC, a mistake on even a single pixel renders the entire prediction incorrect."
  },
  {
    "source_cio": "CIO_022",
    "target_am": "AM_019",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "a mistake on even a single pixel renders the entire prediction incorrect. This may explain the large gain seen here."
  },
  {
    "source_cio": "CIO_025",
    "target_am": "AM_008",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "our method substantially outperforms the recurrent models: HRM [53] and TRM [27]."
  },
  {
    "source_cio": "CIO_030",
    "target_am": "AM_011",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "These attention maps show that our model can correctly reason about the relationship between a source pixel and its target pixel."
  },
  {
    "source_cio": "CIO_031",
    "target_am": "AM_015",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "In this task, different layers exhibit different specialties: some layers attend to the pixels that are to be copied..."
  },
  {
    "source_cio": "CIO_032",
    "target_am": "AM_012",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "This visualization suggests that our method attempts to learn the relations between different tasks, which is an essential ability."
  },
  {
    "source_cio": "CIO_040",
    "target_am": "AM_014",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "our method uncovers different solutions that are plausible."
  },
  {
    "source_cio": "CIO_040",
    "target_am": "AM_020",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Although most ARC tasks are unambiguous, some may admit multiple plausible explanations or rules."
  },
  {
    "source_cio": "CIO_045",
    "target_am": "AM_015",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Layers at different depths tend to focus on different structures. Early layers tend to focus on local transformations..."
  },
  {
    "source_cio": "CIO_046",
    "target_am": "AM_015",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "The figure visually represents how attention is distributed across different layers... with varying patterns of activation visible."
  },
  {
    "source_cio": "CIO_048",
    "target_am": "AM_013",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "we apply attention masks... to encourage the model to focus on the foreground pixels."
  },
  {
    "source_cio": "CIO_049",
    "target_am": "AM_013",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "These designs encourage the model to pay more attention to foregrounds and therefore improve accuracy."
  }
]
```