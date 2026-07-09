```json
[
  {
    "source_cio": "CIO_001",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Our framework, termed Vision ARC (VARC), achieves 60.4% accuracy... This perspective connects ARC to classical image-to-image problems... We demonstrate that incorporating visual priors is crucial."
  },
  {
    "source_cio": "CIO_002",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "VARC achieves 54.5% accuracy on the ARC-1 benchmark... This result substantially surpasses the best recurrent methods... trained from scratch."
  },
  {
    "source_cio": "CIO_003",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Combining VARC models through ensembling... further improves accuracy to 60.4%, matching the reported average human performance."
  },
  {
    "source_cio": "CIO_003",
    "target_am": "AM_007",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Combining VARC models through ensembling [29] further improves accuracy to 60.4%..."
  },
  {
    "source_cio": "CIO_004",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Our ensemble result aggregates an 18M ViT and a 55M U-Net... (ARC-2) 11.1."
  },
  {
    "source_cio": "CIO_004",
    "target_am": "AM_007",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Our ensemble result aggregates an 18M ViT and a 55M U-Net... (ARC-2) 11.1."
  },
  {
    "source_cio": "CIO_005",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Our ensemble result aggregates an 18M ViT and a 55M U-Net... (ARC-1) 60.4."
  },
  {
    "source_cio": "CIO_005",
    "target_am": "AM_007",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Our ensemble result aggregates an 18M ViT and a 55M U-Net... (ARC-1) 60.4."
  },
  {
    "source_cio": "CIO_006",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Our ensemble result aggregates an 18M ViT and a 55M U-Net... (ARC-2) 11.1."
  },
  {
    "source_cio": "CIO_006",
    "target_am": "AM_007",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Our ensemble result aggregates an 18M ViT and a 55M U-Net... (ARC-2) 11.1."
  },
  {
    "source_cio": "CIO_007",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Examples of unseen tasks solved by VARC... VARC correctly solves these challenging tasks."
  },
  {
    "source_cio": "CIO_008",
    "target_am": "AM_019",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "During test-time training, the prediction from Xinfer becomes progressively more accurate, with the model finally generating the correct prediction."
  },
  {
    "source_cio": "CIO_010",
    "target_am": "AM_006",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "To demonstrate this effect... we replace the 2D ROPE... with a 1D ROPE and observe a degradation of 3.5 points."
  },
  {
    "source_cio": "CIO_011",
    "target_am": "AM_006",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Extending from 1D positional embedding to its 2D counterpart is beneficial: see Fig. 7(b)(c)."
  },
  {
    "source_cio": "CIO_012",
    "target_am": "AM_002",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "the 2×2 patchification leads to a noticeable gain of 2.4 points... each patch can cover multiple colors... which substantially enriches the data space for learning."
  },
  {
    "source_cio": "CIO_012",
    "target_am": "AM_005",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Patchification... incorporates several critical inductive biases in vision: most notably, locality... and translation invariance."
  },
  {
    "source_cio": "CIO_013",
    "target_am": "AM_002",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "the 2×2 patchification leads to a noticeable gain of 2.4 points... each patch can cover multiple colors... which substantially enriches the data space for learning."
  },
  {
    "source_cio": "CIO_013",
    "target_am": "AM_005",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Patchification... incorporates several critical inductive biases in vision: most notably, locality... and translation invariance."
  },
  {
    "source_cio": "CIO_014",
    "target_am": "AM_002",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "These vision priors cumulatively yield 27.7 improvement... in which the canvas-based designs (c→f) contribute an 11.5 gain."
  },
  {
    "source_cio": "CIO_014",
    "target_am": "AM_003",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "These vision priors cumulatively yield 27.7 improvement... in which the canvas-based designs (c→f) contribute an 11.5 gain."
  },
  {
    "source_cio": "CIO_015",
    "target_am": "AM_006",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "To demonstrate this effect... we replace the 2D ROPE... with a 1D ROPE and observe a degradation of 3.5 points."
  },
  {
    "source_cio": "CIO_016",
    "target_am": "AM_003",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "In Fig. 7(e), we apply fully flexible translation augmen-tation on the canvas... this setting yields an additional gain of 2.9 points."
  },
  {
    "source_cio": "CIO_016",
    "target_am": "AM_004",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "These data augmentations encourage the model to learn underlying mappings invariant to geometric transformations grounded in the visual world."
  },
  {
    "source_cio": "CIO_017",
    "target_am": "AM_003",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "In Fig. 7(f), we further ap-ply the scale augmentation enabled by the concept of can-vas. Scale augmentation yields a substantial gain of 6.2 points."
  },
  {
    "source_cio": "CIO_017",
    "target_am": "AM_004",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "These data augmentations encourage the model to learn underlying mappings invariant to geometric transformations grounded in the visual world."
  },
  {
    "source_cio": "CIO_017",
    "target_am": "AM_009",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "the ViT architecture has little to no inductive bias about scale invariance. This can explain why scale augmen-tation yields a substantial gain."
  },
  {
    "source_cio": "CIO_018",
    "target_am": "AM_021",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Increasing depth and/or width leads to higher accuracy as a result of better fitting. Going beyond this regime can lead to overfitting."
  },
  {
    "source_cio": "CIO_019",
    "target_am": "AM_021",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "this larger model achieves higher training accuracy, sug-gesting that future research should focus on generalization."
  },
  {
    "source_cio": "CIO_020",
    "target_am": "AM_021",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "In this regime, our method demonstrates good scalability: increasing depth and/or width leads to higher accuracy as a result of better fitting."
  },
  {
    "source_cio": "CIO_021",
    "target_am": "AM_010",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "offline training greatly improves the per-formance of TTT, suggesting that common sense about the visual world can be learned from the training set."
  },
  {
    "source_cio": "CIO_022",
    "target_am": "AM_022",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "performing TTT independently for each test task yields substantially better performance... even though the latter relies on a stronger assumption."
  },
  {
    "source_cio": "CIO_023",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Single-view inference has a decent pass@1 accuracy of 35.9."
  },
  {
    "source_cio": "CIO_024",
    "target_am": "AM_007",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "multi-view inference further boosts to 49.8, thanks to majority voting."
  },
  {
    "source_cio": "CIO_025",
    "target_am": "AM_007",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "multi-view inference further boosts to 49.8, thanks to majority voting."
  },
  {
    "source_cio": "CIO_025",
    "target_am": "AM_023",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "a mistake on even a single pixel renders the entire prediction incorrect. This may explain the large gain seen here."
  },
  {
    "source_cio": "CIO_026",
    "target_am": "AM_007",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "multi-view inference further boosts to 49.8, thanks to majority voting."
  },
  {
    "source_cio": "CIO_028",
    "target_am": "AM_023",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "a mistake on even a single pixel renders the entire prediction incorrect. This may explain the large gain seen here."
  },
  {
    "source_cio": "CIO_029",
    "target_am": "AM_020",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "As the multi-view inference cost is negli-gible compared with test-time training cost, it is virtually nearly free to use many views."
  },
  {
    "source_cio": "CIO_030",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Our single-model result is based on ViT, with mean±std of 54.5±0.7 (ARC-1) and 8.3±0.4 (ARC-2)."
  },
  {
    "source_cio": "CIO_031",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Our ensemble result aggregates an 18M ViT and a 55M U-Net... (ARC-1) 60.4 (ARC-2) 11.1."
  },
  {
    "source_cio": "CIO_031",
    "target_am": "AM_007",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Our ensemble result aggregates an 18M ViT and a 55M U-Net... (ARC-1) 60.4 (ARC-2) 11.1."
  },
  {
    "source_cio": "CIO_032",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Our ensemble result aggregates an 18M ViT and a 55M U-Net... (ARC-1) 60.4."
  },
  {
    "source_cio": "CIO_032",
    "target_am": "AM_007",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Our ensemble result aggregates an 18M ViT and a 55M U-Net... (ARC-1) 60.4."
  },
  {
    "source_cio": "CIO_033",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Our VARC with 18M parameters is ~10 points better than TRM on ARC-1, a >20% relative improvement."
  },
  {
    "source_cio": "CIO_034",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Our model compares favorably with some of the most powerful LLMs at the time their results were reported."
  },
  {
    "source_cio": "CIO_036",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Our method does not rely on such data and uses a model that is several orders of magnitude smaller."
  },
  {
    "source_cio": "CIO_037",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Doing so boosts our result to 60.4. This result closes the gap with the re-ported average human performance."
  },
  {
    "source_cio": "CIO_037",
    "target_am": "AM_007",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Following the classical ensembling practice in vision... we ensemble one ViT and one U-Net... Doing so boosts our result to 60.4."
  },
  {
    "source_cio": "CIO_038",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "This result closes the gap with the re-ported average human performance (60.2 [31])."
  },
  {
    "source_cio": "CIO_038",
    "target_am": "AM_007",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Doing so boosts our result to 60.4. This result closes the gap with the re-ported average human performance."
  },
  {
    "source_cio": "CIO_039",
    "target_am": "AM_012",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "These attention maps show that our model can correctly reason about the relationship between a source pixel and its target pixel."
  },
  {
    "source_cio": "CIO_040",
    "target_am": "AM_012",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "different layers exhibit different specialties: some layers at-tend to the pixels that are to be copied, and some layers at-tend to the target lines."
  },
  {
    "source_cio": "CIO_040",
    "target_am": "AM_013",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "some layers exhibit strong attention to the 3 × 3 neighborhood, reflecting the influence of the pattern's core."
  },
  {
    "source_cio": "CIO_040",
    "target_am": "AM_014",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "some other layers (e.g., layers 7-9) focus on the outward-radiating rays, corresponding to the rule that extends colored pixels."
  },
  {
    "source_cio": "CIO_041",
    "target_am": "AM_015",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "This visualization suggests that our method attempts to learn the relations between different tasks, which is an essential abil-ity for abstraction and reasoning."
  },
  {
    "source_cio": "CIO_042",
    "target_am": "AM_010",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "This comparison suggests that increasing the amount of offline training data is beneficial, although the returns diminish."
  },
  {
    "source_cio": "CIO_043",
    "target_am": "AM_010",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "suggesting that the diversity of training tasks is helpful for generalization."
  },
  {
    "source_cio": "CIO_044",
    "target_am": "AM_016",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "These designs encourage the model to pay more attention to foregrounds and therefore improve accuracy."
  },
  {
    "source_cio": "CIO_045",
    "target_am": "AM_016",
    "direction": "weaken",
    "explicit": true,
    "evidence": "although we note that even without them, our method still per-forms competitively, as observed in our preliminary experiments."
  },
  {
    "source_cio": "CIO_046",
    "target_am": "AM_017",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "This result indicates that our model produces correct predictions in some of the many views, although such cor-rect cases are not sufficiently populated."
  },
  {
    "source_cio": "CIO_047",
    "target_am": "AM_017",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "This result indicates that our model produces correct predictions in some of the many views, although such cor-rect cases are not sufficiently populated."
  },
  {
    "source_cio": "CIO_048",
    "target_am": "AM_017",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "This result indicates that our model produces correct predictions in some of the many views, although such cor-rect cases are not sufficiently populated."
  },
  {
    "source_cio": "CIO_049",
    "target_am": "AM_024",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Although most ARC tasks are unambiguous, some may admit multiple plausible explanations or rules."
  },
  {
    "source_cio": "CIO_050",
    "target_am": "AM_018",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "our model attempts to interpret the rule as either 'going-through-only' (attempt 1) or 'touching' (attempt 2)."
  },
  {
    "source_cio": "CIO_050",
    "target_am": "AM_024",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "our model attempts to interpret the rule as either 'going-through-only' (attempt 1) or 'touching' (attempt 2)."
  },
  {
    "source_cio": "CIO_051",
    "target_am": "AM_018",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "our model attempts to interpret the rule as either 'going-through-only' (attempt 1) or 'touching' (attempt 2)."
  },
  {
    "source_cio": "CIO_051",
    "target_am": "AM_024",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "our model attempts to interpret the rule as either 'going-through-only' (attempt 1) or 'touching' (attempt 2)."
  },
  {
    "source_cio": "CIO_053",
    "target_am": "AM_012",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "Figure 21, Additional visualization: layer-wise attention maps."
  },
  {
    "source_cio": "CIO_053",
    "target_am": "AM_013",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "some layers exhibit strong attention to the 3 × 3 neighborhood, reflecting the influence of the pattern's core."
  },
  {
    "source_cio": "CIO_053",
    "target_am": "AM_014",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "some other layers (e.g., layers 7-9) focus on the outward-radiating rays, corresponding to the rule that extends colored pixels."
  },
  {
    "source_cio": "CIO_054",
    "target_am": "AM_019",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "This visualization illustrates the model's behavior of adapting to task-specific transformations through few-shot test-time training."
  },
  {
    "source_cio": "CIO_055",
    "target_am": "AM_019",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "In early epochs, the model produces coarse and imprecise structures; in later epochs, the model can improve the solutions... This visualization illustrates the model's behavior of adapting."
  },
  {
    "source_cio": "CIO_056",
    "target_am": "AM_019",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "This visualization illustrates the model's behavior of adapting to task-specific transformations through few-shot test-time training."
  },
  {
    "source_cio": "CIO_057",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "(Top): Examples of test tasks successfully solved by VARC."
  },
  {
    "source_cio": "CIO_059",
    "target_am": "AM_001",
    "direction": "strengthen",
    "explicit": true,
    "evidence": "(Top): Examples of test tasks successfully solved by VARC."
  }
]
```