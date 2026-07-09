# Full factor graph — cohort_2026-07-09_08-44-36_am_v3_2_N5

100 observations · 2 propose_test (untested direct claims) · 3 unobserved qualifiers.
Belief edges are link_policy-enforced: only **direct** edges (↑/↓) are genuine Observation→mechanism belief_update; rolls_up / qualifier / demoted are re-routed and are **not** belief_update.

## Observations (φ) → beliefs (δ)
### F001 · P1 · primary_result · _Section 1_
- **context**: Our framework, termed Vision ARC (VARC); on the ARC-1 benchmark
- **intervention**: Combining VARC models through ensembling [29]  _vs_  VARC
- **observed**: achieves accuracy  [60.4%] (up)  [metric: accuracy]
    - _(no direct belief edge)_

### F002 · P11 · comparison · _Section 1_
- **context**: on the ARC-1 benchmark
- **intervention**: Combining VARC models through ensembling [29]  _vs_  VARC
- **observed**: further improves accuracy  [to 60.4%] (up)  [metric: accuracy]
    - _(no direct belief edge)_

### F003 · P12 · primary_result · _Section 1_
- **context**: on the ARC-1 benchmark
- **intervention**: Combining VARC models through ensembling [29]
- **observed**: matching the reported average human performance [31] on the ARC-1 dataset. (flat)  [metric: accuracy]
    - _(no direct belief edge)_
    - ⤴ _rolls_up→thesis_ (n2) Visual learning enables abstraction/inference without language.

### F004 · P7 · primary_result · _Section 1_
- **context**: Our framework, termed Vision ARC (VARC)
- **intervention**: formulate ARC within a vision paradigm, framing it as an image-to-image translation problem.
- **observed**: shows strong performance on the ARC benchmarks (e.g., Fig. 2). (up)
    - _(no direct belief edge)_

### F005 · P8 · primary_result · _Section 1_
- **context**: VARC; on the ARC-1 benchmark; using a small model with only 18 million parameters.  [18 million parameters]
- **intervention**: apply standard vision architectures, such as a vanilla Vision Transformer (ViT), to perform image-to-image mapping.
- **observed**: achieves accuracy  [54.5%] (up)  [metric: accuracy]
    - _(no direct belief edge)_

### F006 · P9 · primary_result · _Section 1_
- **context**: VARC; on the ARC-1 benchmark; using a small model with only 18 million parameters.  [18 million parameters]
- **intervention**: apply standard vision architectures, such as a vanilla Vision Transformer (ViT), to perform image-to-image mapping.  _vs_  recurrent models [53, 27]
- **observed**: substantially surpasses the best recurrent methods [53, 27] that are also trained from scratch on ARC. (up)  [metric: accuracy]
    - _(no direct belief edge)_

### F007 · P16 · primary_result · _Figure 2_
- **context**: VARC
- **observed**: correctly solves these challenging tasks. (up)
    - _(no direct belief edge)_
    - ⤴ _rolls_up→thesis_ (n2) Visual learning enables abstraction/inference without language.

### F008 · P18 · primary_result · _Section 3.5_
- **context**: Test-time training (TTT).; Given a single new, unseen task T∈ Ttest from the test set, we perform inference by test-time training.; At inference time, we are given Demo={(xi, Yi)}m=1 with both input and output accessible; the model is required to make prediction for a given Xinfer in this new task T.; The test-time training followed by inference can be viewed abstractly as a function F(Xinfer | Demo)→ Yinfer.
- **intervention**: We perform test-time training for each new task T independently.
- **observed**: this test-time training process remains reasonably fast  [e.g., 70 seconds per task on a single GPU]
    - _(no direct belief edge)_
    - ∅ _demoted-observation (not belief)_ (n2) Attention maps reveal pixel-to-pixel reasoning relationships
- ⚠️ field mismatch: ['context']

### F009 · P17 · primary_result · _Figure 6_
- **observed**: During test-time training, the prediction from Xinfer becomes progressively more accurate, with the model finally generating the correct prediction. (up)
    - _(no direct belief edge)_
    - ∅ _demoted-observation (not belief)_ (n2) TTT visualization shows model adapting to task-specific tran

### F010 · P19 · comparison · _Table 1_
- **context**: ViT  [width 384, depth 5, #params 6M, Gflops 10]; ViT  [width 512, depth 10, #params 18M, Gflops 28]; ViT  [width 768, depth 20, #params 66M, Gflops 99]; U-Net  [setting (a), #params 7M, Gflops 18]; U-Net  [setting (b), #params 17M, Gflops 33]; U-Net  [setting (c), #params 55M, Gflops 87]
- **intervention**: ViT  _vs_  U-Net
- **observed**: ViT models show higher accuracy than U-Net models  [ViT accuracies: 44.4, 54.5, 53.0; U-Net accuracies: 42.8, 47.5, 48.3] (up)  [metric: acc.]
    - _(no direct belief edge)_

### F011 · P88 · primary_result · _Table 1_
- **context**: ViT  [width 384, depth 5, #params 6M, Gflops 10]
- **intervention**: ViT
- **observed**: ViT — acc. = 44.4  [cell: acc. = 44.4; width 384; depth 5; #params 6M; Gflops 10]  [metric: acc.]
    - _(no direct belief edge)_

### F012 · P89 · primary_result · _Table 1_
- **context**: ViT  [width 512, depth 10, #params 18M, Gflops 28]
- **intervention**: ViT
- **observed**: ViT — acc. = 54.5  [cell: acc. = 54.5; width 512; depth 10; #params 18M; Gflops 28]  [metric: acc.]
    - _(no direct belief edge)_

### F013 · P90 · primary_result · _Table 1_
- **context**: ViT  [width 768, depth 20, #params 66M, Gflops 99]
- **intervention**: ViT
- **observed**: ViT — acc. = 53.0  [cell: acc. = 53.0; width 768; depth 20; #params 66M; Gflops 99]  [metric: acc.]
    - _(no direct belief edge)_

### F014 · P91 · primary_result · _Table 1_
- **context**: U-Net  [setting (a), #params 7M, Gflops 18]
- **intervention**: U-Net
- **observed**: U-Net — acc. = 42.8  [cell: acc. = 42.8; width setting (a); #params 7M; Gflops 18]  [metric: acc.]
    - _(no direct belief edge)_

### F015 · P92 · primary_result · _Table 1_
- **context**: U-Net  [setting (b), #params 17M, Gflops 33]
- **intervention**: U-Net
- **observed**: U-Net — acc. = 47.5  [cell: acc. = 47.5; width setting (b); #params 17M; Gflops 33]  [metric: acc.]
    - _(no direct belief edge)_

### F016 · P93 · primary_result · _Table 1_
- **context**: U-Net  [setting (c), #params 55M, Gflops 87]
- **intervention**: U-Net
- **observed**: U-Net — acc. = 48.3  [cell: acc. = 48.3; width setting (c); #params 55M; Gflops 87]  [metric: acc.]
    - _(no direct belief edge)_

### F017 · P20 · comparison · _Figure 7_
- **context**: ARC-1 evaluation set.; The model used is ViT-18M.
- **intervention**: Entries (a-c) use a patch size of 1×1 on a 32×32 canvas, whereas entries (d-f) use a patch size of 2×2 on a 64×64 canvas.  _vs_  We start from a naïve baseline with components (b-f) removed.
- **observed**: These vision priors cumulatively yield improvement (a→f)  [27.7 improvement] (up)  [metric: Accuracy]
    - ↑ _✓ tested_ (n4) Explicit 2D positional modeling preserves image structure.
- ⚠️ field mismatch: ['context']

### F018 · P21 · comparison · _Figure 7_
- **context**: ARC-1 evaluation set.; The model used is ViT-18M.
- **intervention**: Entries (a-c) use a patch size of 1×1 on a 32×32 canvas, whereas entries (d-f) use a patch size of 2×2 on a 64×64 canvas.
- **observed**: the canvas-based designs (c→f) contribute an gain.  [11.5 gain] (up)  [metric: Accuracy]
    - ↑ _✓ tested_ (n5) Explicit 2D positional modeling preserves image structure.

### F019 · P22 · comparison · _Section 5.1_
- **observed**: These priors jointly have a gain  [27.7 points] (up)
    - ↑ _✓ tested_ (n5) Explicit 2D positional modeling preserves image structure.
- ⚠️ field mismatch: ['context']

### F020 · P23 · comparison · _Section 5.1_
- **observed**: the canvas-based designs (c–f) has a gain.  [11.5 points] (up)
    - ↑ _✓ tested_ (n2) Explicit 2D positional modeling preserves image structure.

### F021 · P24 · primary_result · _Section 5.1_
- **context**: 2D positional embedding.; This is observed in both (b) absolute and (c) relative positional embeddings.
- **observed**: Extending from 1D posi-tional embedding to its 2D counterpart is beneficial (up)
    - ↑ _✓ tested_ (n4) Canvas patchification enriches data, reduces overfitting, encourages s

### F022 · P25 · primary_result · _Section 5.1_
- **intervention**: we re-place the 2D ROPE in Fig. 7(f) with a 1D ROPE
- **observed**: observe a degradation  [3.5 points, from 54.5 to 51.0] (down)
    - ↑ _✓ tested_ (n3) Canvas patchification enriches data, reduces overfitting, encourages s

### F023 · P26 · primary_result · _Section 5.1_
- **context**: Patchification.; A key design principle of our method is to prepare the input as a natural image.
- **intervention**: we advance from 1×1 patches on a 32×32 canvas to 2×2 patches on a 64×64 canvas.
- **observed**: The entries Fig. 7(d-f) all benefit from this design. (up)
    - ↑ _✓ tested_ (n3) Canvas patchification enriches data, reduces overfitting, encourages s

### F024 · P27 · primary_result · _Section 5.1_
- **intervention**: we advance from 1×1 patches on a 32×32 canvas to 2×2 patches on a 64×64 canvas.
- **observed**: Doing so does not increase the computational cost of the Transformer. (flat)
    - _(no direct belief edge)_

### F025 · P28 · comparison · _Section 5.1_
- **context**: the scaling ratio is fixed as 2x.
- **intervention**: we advance from 1×1 patches on a 32×32 canvas to 2×2 patches on a 64×64 canvas.
- **observed**: the 2×2 patchification leads to a noticeable gain  [2.4 points, improving from 43.0 to 45.4] (up)
    - ↑ _✓ tested_ (n2) Canvas formulation enables augmentations for translation/scale invaria
    - ↑ _✓ tested_ (n2) Canvas patchification enriches data, reduces overfitting, encourages s
- ⚠️ field mismatch: ['context']

### F026 · P34 · comparison · _Section 5.1_
- **context**: Translation and scale augmentation.
- **intervention**: we apply fully flexible translation augmen-tation on the canvas.
- **observed**: this setting yields an additional gain  [2.9 points (from 45.4 to 48.3)] (up)
    - ↑ _✓ tested_ (n5) Canvas formulation enables augmentations for translation/scale invaria

### F027 · P35 · comparison · _Section 5.1_
- **context**: Translation and scale augmentation.
- **intervention**: we further ap-ply the scale augmentation enabled by the concept of can-vas.
- **observed**: Scale augmentation yields a substantial gain  [6.2 points] (up)
    - ↑ _✓ tested_ (n5) Canvas formulation enables augmentations for translation/scale invaria

### F028 · P29 · comparison · _Figure 8_
- **context**: The circle areas de-note model sizes.
- **intervention**: ViTs with different width (x-axis) and depth.
- **observed**: increasing depth and/or width leads to higher accuracy (up)  [metric: Accuracy (%)]
    - ↑ _~ weak_ (n3) Increasing model size improves accuracy by enabling better fitting.

### F029 · P30 · comparison · _Figure 9_
- **intervention**: with vs. without offline train-ing, and joint vs. independent for each task.  _vs_  with vs. without offline train-ing, and joint vs. independent for each task.
- **observed**: offline training improves performance  [54.5 vs 29.1] (up)  [metric: Accuracy (%)]
    - ↑ _✓ tested_ (n5) Visual common sense is learned from offline training data.

### F030 · P31 · comparison · _Figure 9_
- **intervention**: with vs. without offline train-ing, and joint vs. independent for each task.  _vs_  with vs. without offline train-ing, and joint vs. independent for each task.
- **observed**: TTT independently performs better than TTT jointly  [54.5 vs 26.4] (up)  [metric: Accuracy (%)]
    - _(no direct belief edge)_
    - ◇ _qualifier (not belief)_ (n2) Some tasks are solvable from scratch (tabula rasa).

### F031 · P36 · comparison · _Section 5.2_
- **context**: ViT vs. U-Net.; We evaluate three model sizes for each architecture.
- **intervention**: we compare ViT with U-Nets, a type of convolutional network.  _vs_  we compare ViT with U-Nets, a type of convolutional network.
- **observed**: ViTs consistently per-form better (up)
    - _(no direct belief edge)_

### F032 · P38 · comparison · _Section 5.2_
- **context**: Scalability.
- **intervention**: we show ViTs with varying depths and widths.
- **observed**: our method demonstrates good scalability: increasing depth and/or width leads to higher accuracy (up)
    - _(no direct belief edge)_

### F033 · P39 · comparison · _Section 5.2_
- **context**: as shown in Tab. 1 for the 66M ViT model.
- **observed**: this larger model achieves higher training accuracy (up)
    - ↑ _~ weak_ (n2) Majority voting consolidates predictions from different views.
- ⚠️ field mismatch: ['intervention']

### F034 · P40 · comparison · _Section 5.2_
- **context**: Test-time training (TTT) strategies.
- **intervention**: we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.  _vs_  we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.
- **observed**: offline training greatly improves the per-formance of TTT (up)
    - _(no direct belief edge)_

### F035 · P41 · primary_result · _Section 5.2_
- **context**: Test-time training (TTT) strategies.
- **intervention**: we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.
- **observed**: even without offline training, our TTT strategy can achieve nontrivial accuracy  [26.4] (up)
    - _(no direct belief edge)_
    - ◇ _qualifier (not belief)_ (n2) Single pixel error invalidates entire ARC prediction.

### F036 · P42 · comparison · _Section 5.2_
- **context**: under a similar setting.
- **observed**: This result outperforms that in [36] (up)
    - _(no direct belief edge)_
    - ◇ _qualifier (not belief)_ (n2) Single pixel error invalidates entire ARC prediction.
- ⚠️ field mismatch: ['intervention']

### F037 · P43 · comparison · _Section 5.2_
- **context**: Test-time training (TTT) strategies.
- **intervention**: we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.  _vs_  we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.
- **observed**: performing TTT independently for each test task yields substantially better performance than doing so jointly across all test tasks  [by ~10 points] (up)
    - _(no direct belief edge)_

### F038 · P44 · primary_result · _Section 5.2_
- **context**: Single-view vs. multi-view inference.
- **intervention**: we also examine the single-view inference accuracy.
- **observed**: Single-view inference has a decent pass@1 accuracy  [35.9]  [metric: we compare pass@1 accuracy.]
    - _(no direct belief edge)_

### F039 · P45 · comparison · _Section 5.2_
- **context**: Single-view vs. multi-view inference.
- **observed**: multi-view inference further boosts  [to 49.8] (up)  [metric: we compare pass@1 accuracy.]
    - _(no direct belief edge)_
- ⚠️ field mismatch: ['intervention']

### F040 · P94 · primary_result · _Table 2_
- **intervention**: single-view
- **observed**: single-view — pass@1 = 35.9  [cell: single-view, pass@1 = 35.9]  [metric: pass@1]
    - _(no direct belief edge)_

### F041 · P95 · primary_result · _Table 2_
- **intervention**: multi-view
- **observed**: multi-view — pass@1 = 49.8  [cell: multi-view, pass@1 = 49.8]  [metric: pass@1]
    - ↑ _~ weak_ (n2) Majority voting consolidates predictions from different views.

### F042 · P96 · primary_result · _Table 2_
- **intervention**: multi-view
- **observed**: multi-view — pass@2 = 54.5  [cell: multi-view, pass@2 = 54.5]  [metric: pass@2]
    - _(no direct belief edge)_

### F043 · P48 · primary_result · _Section 5.3_
- **context**: System-level Comparisons.; LLMs are pre-trained on internet-scale data, and some may also incor-porate multimodal data that include images.; Our method does not rely on such data; uses a model that is several orders of magnitude smaller.
- **intervention**: we compare with leading results using LLMs or recurrent models, on ARC-1 and ARC-2.
- **observed**: Our model compares favorably with some of the most powerful LLMs at the time their results were reported: in-cluding Deepseek, Claude, o3, and GPT-5 (up)
    - _(no direct belief edge)_
    - ⤴ _rolls_up→thesis_ (n2) Visual learning enables abstraction/inference without language.

### F044 · P49 · comparison · _Section 5.3_
- **context**: In the controlled setting of training from scratch on ARC data
- **intervention**: we compare with leading results using LLMs or recurrent models, on ARC-1 and ARC-2.
- **observed**: our method substantially outperforms the recur-rent models: HRM [53] and TRM [27]. (up)
    - _(no direct belief edge)_
    - ⤴ _rolls_up→thesis_ (n2) Visual learning enables abstraction/inference without language.

### F045 · P50 · comparison · _Section 5.3_
- **context**: In the controlled setting of training from scratch on ARC data
- **intervention**: we compare with leading results using LLMs or recurrent models, on ARC-1 and ARC-2.
- **observed**: Our VARC with 18M parameters is better than TRM on ARC-1  [~10 points better, a >20% relative improvement] (up)
    - _(no direct belief edge)_

### F046 · P51 · comparison · _Section 5.3_
- **intervention**: we ensemble one ViT and one U-Net, each with test-time training run four times.
- **observed**: Doing so boosts our result  [to 60.4] (up)
    - _(no direct belief edge)_

### F047 · P52 · comparison · _Section 5.3_
- **intervention**: we ensemble one ViT and one U-Net, each with test-time training run four times.
- **observed**: This result closes the gap with the re-ported average human performance  [60.4 vs 60.2 [31]] (flat)
    - _(no direct belief edge)_

### F048 · P100 · primary_result · _Table 3_
- **context**: Claude 3.7 8k [18]  [#params N/A]
- **intervention**: Claude 3.7 8k [18]
- **observed**: Claude 3.7 8k [18] — ARC-2 = 0.9  [cell: ARC-2 = 0.9; #params N/A]  [metric: ARC-2]
    - _(no direct belief edge)_

### F049 · P101 · primary_result · _Table 3_
- **context**: o3-mini-high [18]  [#params N/A]
- **intervention**: o3-mini-high [18]
- **observed**: o3-mini-high [18] — ARC-1 = 34.5  [cell: ARC-1 = 34.5; #params N/A]  [metric: ARC-1]
    - _(no direct belief edge)_

### F050 · P102 · primary_result · _Table 3_
- **context**: o3-mini-high [18]  [#params N/A]
- **intervention**: o3-mini-high [18]
- **observed**: o3-mini-high [18] — ARC-2 = 3.0  [cell: ARC-2 = 3.0; #params N/A]  [metric: ARC-2]
    - _(no direct belief edge)_

### F051 · P103 · primary_result · _Table 3_
- **context**: GPT-5 [18]  [#params N/A]
- **intervention**: GPT-5 [18]
- **observed**: GPT-5 [18] — ARC-1 = 44.0  [cell: ARC-1 = 44.0; #params N/A]  [metric: ARC-1]
    - _(no direct belief edge)_

### F052 · P104 · primary_result · _Table 3_
- **context**: GPT-5 [18]  [#params N/A]
- **intervention**: GPT-5 [18]
- **observed**: GPT-5 [18] — ARC-2 = 1.9  [cell: ARC-2 = 1.9; #params N/A]  [metric: ARC-2]
    - _(no direct belief edge)_

### F053 · P105 · primary_result · _Table 3_
- **context**: Grok-4-thinking [18]  [#params 1.7T]
- **intervention**: Grok-4-thinking [18]
- **observed**: Grok-4-thinking [18] — ARC-1 = 66.7  [cell: ARC-1 = 66.7; #params 1.7T]  [metric: ARC-1]
    - _(no direct belief edge)_

### F054 · P106 · primary_result · _Table 3_
- **context**: Grok-4-thinking [18]  [#params 1.7T]
- **intervention**: Grok-4-thinking [18]
- **observed**: Grok-4-thinking [18] — ARC-2 = 16.0  [cell: ARC-2 = 16.0; #params 1.7T]  [metric: ARC-2]
    - _(no direct belief edge)_

### F055 · P107 · primary_result · _Table 3_
- **context**: Bespoke (Grok-4) [8]  [#params 1.7T]
- **intervention**: Bespoke (Grok-4) [8]
- **observed**: Bespoke (Grok-4) [8] — ARC-1 = 79.6  [cell: ARC-1 = 79.6; #params 1.7T]  [metric: ARC-1]
    - _(no direct belief edge)_

### F056 · P108 · primary_result · _Table 3_
- **context**: Bespoke (Grok-4) [8]  [#params 1.7T]
- **intervention**: Bespoke (Grok-4) [8]
- **observed**: Bespoke (Grok-4) [8] — ARC-2 = 29.4  [cell: ARC-2 = 29.4; #params 1.7T]  [metric: ARC-2]
    - _(no direct belief edge)_

### F057 · P109 · primary_result · _Table 3_
- **context**: HRM [53]  [#params 27M]
- **intervention**: HRM [53]
- **observed**: HRM [53] — ARC-1 = 40.3  [cell: ARC-1 = 40.3; #params 27M]  [metric: ARC-1]
    - _(no direct belief edge)_

### F058 · P110 · primary_result · _Table 3_
- **context**: HRM [53]  [#params 27M]
- **intervention**: HRM [53]
- **observed**: HRM [53] — ARC-2 = 5.0  [cell: ARC-2 = 5.0; #params 27M]  [metric: ARC-2]
    - _(no direct belief edge)_

### F059 · P111 · primary_result · _Table 3_
- **context**: TRM [27]  [#params 7M]
- **intervention**: TRM [27]
- **observed**: TRM [27] — ARC-1 = 44.6  [cell: ARC-1 = 44.6; #params 7M]  [metric: ARC-1]
    - _(no direct belief edge)_

### F060 · P112 · primary_result · _Table 3_
- **context**: TRM [27]  [#params 7M]
- **intervention**: TRM [27]
- **observed**: TRM [27] — ARC-2 = 7.8  [cell: ARC-2 = 7.8; #params 7M]  [metric: ARC-2]
    - _(no direct belief edge)_

### F061 · P113 · primary_result · _Table 3_
- **context**: VARC  [#params 18M]
- **intervention**: VARC
- **observed**: VARC — ARC-1 = 54.5  [cell: ARC-1 = 54.5; #params 18M]  [metric: ARC-1]
    - _(no direct belief edge)_

### F062 · P114 · primary_result · _Table 3_
- **context**: VARC  [#params 18M]
- **intervention**: VARC
- **observed**: VARC — ARC-2 = 8.3  [cell: ARC-2 = 8.3; #params 18M]  [metric: ARC-2]
    - _(no direct belief edge)_

### F063 · P115 · primary_result · _Table 3_
- **context**: VARC (ensemble)  [#params 73M]
- **intervention**: VARC (ensemble)
- **observed**: VARC (ensemble) — ARC-1 = 60.4  [cell: ARC-1 = 60.4; #params 73M]  [metric: ARC-1]
    - _(no direct belief edge)_

### F064 · P116 · primary_result · _Table 3_
- **context**: VARC (ensemble)  [#params 73M]
- **intervention**: VARC (ensemble)
- **observed**: VARC (ensemble) — ARC-2 = 11.1  [cell: ARC-2 = 11.1; #params 73M]  [metric: ARC-2]
    - _(no direct belief edge)_

### F065 · P117 · primary_result · _Table 3_
- **context**: avg. human [31]  [#params -]
- **intervention**: avg. human [31]
- **observed**: avg. human [31] — ARC-1 = 60.2  [cell: ARC-1 = 60.2; #params -]  [metric: ARC-1]
    - _(no direct belief edge)_

### F066 · P118 · primary_result · _Table 3_
- **context**: best human [18]  [#params -]
- **intervention**: best human [18]
- **observed**: best human [18] — ARC-1 = 98.0  [cell: ARC-1 = 98.0; #params -]  [metric: ARC-1]
    - _(no direct belief edge)_

### F067 · P119 · primary_result · _Table 3_
- **context**: best human [18]  [#params -]
- **intervention**: best human [18]
- **observed**: best human [18] — ARC-2 = 100.0  [cell: ARC-2 = 100.0; #params -]  [metric: ARC-2]
    - _(no direct belief edge)_

### F068 · P46 · primary_result · _Table 3_
- **context**: LLM-based results are from the ARC-AGI leader-board [18].; HRM, TRM, and our VARC are trained from scratch only on ARC data.; Our single-model result is based on ViT, with mean±std of 54.5±0.7 (ARC-1) and 8.3±0.4 (ARC-2) over four runs.; Our ensemble result aggregates an 18M ViT and a 55M U-Net, each with test-time training performed four times.
- **intervention**: VARC (ensemble)
- **observed**: VARC (ensemble) achieves 60.4 on ARC-1 and 11.1 on ARC-2  [60.4, 11.1]  [metric: ARC-1]
    - _(no direct belief edge)_

### F069 · P47 · primary_result · _Table 3_
- **context**: LLM-based results are from the ARC-AGI leader-board [18].; HRM, TRM, and our VARC are trained from scratch only on ARC data.; Our single-model result is based on ViT, with mean±std of 54.5±0.7 (ARC-1) and 8.3±0.4 (ARC-2) over four runs.; Our ensemble result aggregates an 18M ViT and a 55M U-Net, each with test-time training performed four times.
- **intervention**: VARC (ensemble)  _vs_  avg. human [31]
- **observed**: VARC (ensemble) is comparable to avg. human performance on ARC-1  [VARC 60.4, avg. human 60.2] (flat)  [metric: ARC-1]
    - _(no direct belief edge)_

### F070 · P97 · primary_result · _Table 3_
- **context**: Deepseek R1 [21]  [#params 671B]
- **intervention**: Deepseek R1 [21]
- **observed**: Deepseek R1 [21] — ARC-1 = 15.8  [cell: ARC-1 = 15.8; #params 671B]  [metric: ARC-1]
    - _(no direct belief edge)_

### F071 · P98 · primary_result · _Table 3_
- **context**: Deepseek R1 [21]  [#params 671B]
- **intervention**: Deepseek R1 [21]
- **observed**: Deepseek R1 [21] — ARC-2 = 1.3  [cell: ARC-2 = 1.3; #params 671B]  [metric: ARC-2]
    - _(no direct belief edge)_

### F072 · P99 · primary_result · _Table 3_
- **context**: Claude 3.7 8k [18]  [#params N/A]
- **intervention**: Claude 3.7 8k [18]
- **observed**: Claude 3.7 8k [18] — ARC-1 = 21.2  [cell: ARC-1 = 21.2; #params N/A]  [metric: ARC-1]
    - _(no direct belief edge)_

### F073 · P53 · primary_result · _Section 6_
- **context**: Figure 11 visualizes the layer-wise attention maps for an-other test task.; A layer-wise map is the softmax attention map averaged across all pixels in the layer
- **observed**: some layers exhibit strong attention to the 3 × 3 neighborhood
    - _(no direct belief edge)_
    - ∅ _demoted-observation (not belief)_ (n2) Attention maps reveal pixel-to-pixel reasoning relationships

### F074 · P54 · primary_result · _Section 6_
- **context**: Figure 11 visualizes the layer-wise attention maps for an-other test task.; A layer-wise map is the softmax attention map averaged across all pixels in the layer
- **observed**: some other layers (e.g., layers 7-9) focus on the outward-radiating rays
    - _(no direct belief edge)_

### F075 · P57 · primary_result · _Section 6_
- **context**: t-SNE of task embeddings.; Our model is conditioned on a task token, with an embedding learned to represent each task.; With 400 training tasks in ARC-1, our model learns 400 distinct task embeddings in offline training.; Each point corresponds to a task..
- **intervention**: We visu-alize these 400 embeddings in the 2D space by t-SNE [39]
- **observed**: the top-left corner in Fig. 12 shows two tasks related to coloring; the bottom-left corner shows two tasks related to generalized logic operations (i.e., AND/OR/XOR).
    - _(no direct belief edge)_

### F076 · P59 · primary_result · _Figure 14_
- **context**: RE-ARC samples per task; evaluated on the ARC-1 eval set
- **intervention**: Offline training data scaling: effect of varying
- **observed**: Increasing the amount of offline training data is beneficial (up)
    - _(no direct belief edge)_
- ⚠️ field mismatch: ['intervention']

### F077 · P60 · primary_result · _Figure 15_
- **context**: the number of training tasks; evaluated on the ARC-1 eval set
- **intervention**: Offline training task diversity scaling: effect of varying
- **observed**: Increasing task diversity is beneficial. (up)
    - _(no direct belief edge)_
- ⚠️ field mismatch: ['intervention']

### F078 · P61 · primary_result · _Section B.1_
- **context**: RE-ARC dataset [22] in our offline training
- **intervention**: Using only the original ARC training data, without any RE-ARC data
- **observed**: our method achieves a decent accuracy  [31.5%]  [metric: accuracy]
    - _(no direct belief edge)_

### F079 · P62 · primary_result · _Section B.1_
- **context**: RE-ARC dataset [22] in our offline training
- **intervention**: adding 10, 100, and 1,000 pairs per task from RE-ARC  _vs_  Using only the original ARC training data, without any RE-ARC data
- **observed**: increases  [to 38.6, 52.3, and 54.0] (up)  [metric: accuracy]
    - _(no direct belief edge)_

### F080 · P63 · primary_result · _Section B.1_
- **intervention**: trained on 0, 16, 80, and 400 tasks
- **observed**: increases  [from 26.4 to 43.1, 49.6, and 54.5] (up)  [metric: accuracy]
    - _(no direct belief edge)_

### F081 · P65 · primary_result · _Section B.2_
- **context**: multi-view inference with many views (510); On ARC-1
- **intervention**: as the number of proposals (k) increases
- **observed**: is  [49.8, 54.5, and 66.3, when k is 1, 2, and 300] (up)  [metric: pass@k accu-racy]
    - _(no direct belief edge)_

### F082 · P66 · primary_result · _Section B.2_
- **context**: multi-view inference with many views (510); On ARC-1
- **observed**: this result reveals the upper-bound performance (66.3) of our method, even if oracle voting were applied.  [metric: pass@k accu-racy]
    - _(no direct belief edge)_
    - ◇ _qualifier (not belief)_ (n2) Correct predictions exist in views but are outvoted.

### F083 · P70 · primary_result · _Figure 17_
- **context**: ARC-1
- **observed**: Successful and failed examples
    - _(no direct belief edge)_

### F084 · P71 · primary_result · _Figure 17_
- **context**: ARC-1; test tasks
- **intervention**: solved by VARC
- **observed**: successfully solved (up)  [metric: correct output]
    - _(no direct belief edge)_

### F085 · P72 · primary_result · _Figure 17_
- **context**: ARC-1; test tasks
- **intervention**: unsolved by VARC
- **observed**: unsolved (down)  [metric: correct output]
    - _(no direct belief edge)_

### F086 · P73 · primary_result · _Figure 17_
- **context**: Two demonstration example pairs shown for each task (some have more demonstrations not shown here); Inference input; Task 15663ba9; Task 981571dc; Task 15696249; Task 67c52801
- **intervention**: first and second solutions proposed by VARC  _vs_  correct output
- **observed**: VARC's Attempt 1 matches the Ground Truth  [Tasks: 15663ba9, 981571dc, 15696249, 67c52801] (up)  [metric: Vote  [109, 57, 399, 35, 456, 10, 233, 123, 9, 6, 14, 8, 13, 9, 3, 2]]
    - _(no direct belief edge)_

### F087 · P74 · primary_result · _Figure 17_
- **context**: Two demonstration example pairs shown for each task (some have more demonstrations not shown here); Inference input; Task 8dae5dfc; Task 67636eac; Task aa4ec2a5; Task b457fec5
- **intervention**: first and second solutions proposed by VARC  _vs_  correct output
- **observed**: VARC fails to solve the task  [Tasks: 8dae5dfc, 67636eac, aa4ec2a5, b457fec5] (down)  [metric: Vote  [109, 57, 399, 35, 456, 10, 233, 123, 9, 6, 14, 8, 13, 9, 3, 2]]
    - _(no direct belief edge)_

### F088 · P75 · primary_result · _Figure 18_
- **context**: ARC-2
- **observed**: Successful and failed examples
    - _(no direct belief edge)_

### F089 · P76 · primary_result · _Figure 18_
- **context**: ARC-2; test tasks
- **intervention**: solved by VARC
- **observed**: successfully solved (up)  [metric: correct output]
    - _(no direct belief edge)_

### F090 · P77 · primary_result · _Figure 18_
- **context**: ARC-2; test tasks
- **intervention**: unsolved by VARC
- **observed**: unsolved (down)  [metric: correct output]
    - _(no direct belief edge)_

### F091 · P78 · primary_result · _Figure 18_
- **context**: Two demonstration example pairs shown for each task (some have more demonstrations not shown here); Inference input; Task 800d221b; Task 7666fa5d; Task 221dfab4; Task 7b80bb43
- **intervention**: first and second solutions proposed by VARC  _vs_  correct output
- **observed**: VARC's Attempt 1 matches the Ground Truth  [Tasks: 800d221b, 7666fa5d, 221dfab4, 7b80bb43] (up)  [metric: Vote  [99, 82, 410, 16, 30, 17, 168, 44, 21, 20, 7, 6, 14, 12, 67, 51]]
    - _(no direct belief edge)_

### F092 · P79 · primary_result · _Figure 18_
- **context**: Two demonstration example pairs shown for each task (some have more demonstrations not shown here); Inference input; Task 2b83f449; Task 2d0172a1; Task 3e6067c3; Task 7ed72f31
- **intervention**: first and second solutions proposed by VARC  _vs_  correct output
- **observed**: VARC fails to solve the task  [Tasks: 2b83f449, 2d0172a1, 3e6067c3, 7ed72f31] (down)  [metric: Vote  [99, 82, 410, 16, 30, 17, 168, 44, 21, 20, 7, 6, 14, 12, 67, 51]]
    - _(no direct belief edge)_

### F093 · P80 · primary_result · _Figure 19_
- **observed**: Ambiguous examples
    - ↑ _~ weak_ (n2) Model handles ambiguity by proposing multiple rule interpretations.
    - ◇ _qualifier (not belief)_ (n2) Some ARC tasks admit multiple plausible rules.

### F094 · P81 · primary_result · _Figure 19_
- **observed**: some may admit multiple plausible explanations or rules
    - _(no direct belief edge)_
    - ◇ _qualifier (not belief)_ (n4) Some ARC tasks admit multiple plausible rules.
- ⚠️ field mismatch: ['context']

### F095 · P82 · primary_result · _Figure 19_
- **context**: three demonstration examples of a test task (top panel); a blue line "touching" (but not "going through") a red rectangle; inference example (bottom panel) involves this situation ("touching"); Task 09c534e7
- **intervention**: our model attempts to interpret the rule as either "going-through-only" (attempt 1) or "touching" (attempt 2)  _vs_  Ground truth
- **observed**: Attempt 2 matches Ground Truth, Attempt 1 does not (up)  [metric: Ground truth]
    - ↑ _~ weak_ (n2) Model handles ambiguity by proposing multiple rule interpretations.
    - ◇ _qualifier (not belief)_ (n3) Some ARC tasks admit multiple plausible rules.
- ⚠️ field mismatch: ['context']

### F096 · P83 · primary_result · _Figure 20_
- **context**: pixel-level attention maps; 4 test tasks in ARC eval; Task 09c534e7
- **observed**: task that was not correctly solved (down)  [metric: correctly solved]
    - _(no direct belief edge)_

### F097 · P84 · primary_result · _Figure 21_
- **context**: layer-wise attention maps; demonstration examples (on the left) are provided for reference; Task 0607ce86; Task 0bb8deee; Task 1c56ad9f; Task 1d0a4b61
- **observed**: Attention patterns vary across layers  [metric: per-pixel softmax attention maps averaged across all pixels in that layer]
    - _(no direct belief edge)_

### F098 · P85 · primary_result · _Figure 22 caption | Figure 22 'TTT process' and 'Ground truth' panels_
- **context**: model's predictions converge toward the correct output
- **intervention**: test-time training progresses
- **observed**: gradually converge toward the correct output (up)  [metric: model's predictions converge toward the correct output]
    - _(no direct belief edge)_
    - ∅ _demoted-observation (not belief)_ (n5) TTT visualization shows model adapting to task-specific tran

### F099 · P86 · primary_result · _Figure 22 caption | Figure 22 'TTT process' panels (early stages)_
- **context**: In early epochs
- **intervention**: test-time training progresses
- **observed**: model produces coarse and imprecise structures (down)  [metric: model's predictions converge toward the correct output]
    - _(no direct belief edge)_
    - ∅ _demoted-observation (not belief)_ (n4) TTT visualization shows model adapting to task-specific tran

### F100 · P87 · comparison · _Figure 22 caption | Figure 22 'TTT process' panels (later stages)_
- **context**: in later epochs
- **intervention**: test-time training progresses  _vs_  In early epochs
- **observed**: model can improve the solutions (up)  [metric: model's predictions converge toward the correct output]
    - _(no direct belief edge)_
    - ∅ _demoted-observation (not belief)_ (n5) TTT visualization shows model adapting to task-specific tran

## propose_test — untested direct claims (AIO differentiator)
_direct_link_allowed beliefs asserted with zero observation — candidates for a test._

- **MECH_attention_masks_loss_focus_improve_foreground** — Attention masks and loss focus improve foreground attention/accuracy.  (_mechanism_, 1 raw nodes)
- **MECH_average_pooling_aggregates_predictions_raw_grid** — Average pooling aggregates predictions for raw grid locations.  (_mechanism_, 1 raw nodes)

## unobserved qualifiers — assumptions / scope / limitations with no observation
_flagged, but NOT propose_test targets: a qualifier is not a belief to strengthen._

- **ASM_larger_models_beyond_current_regime_lead** — Larger models beyond current regime lead to overfitting.  (_limitation_, 1 raw nodes)
- **ASM_multi_view_inference_cost_negligible_compared** — Multi-view inference cost is negligible compared to TTT.  (_scope_condition_, 1 raw nodes)
- **ASM_multiple_unseen_tasks_cannot_assumed_simultaneously** — Multiple unseen tasks cannot be assumed simultaneously.  (_assumption_, 2 raw nodes)

_direct belief edge status tally: {'tested': 12, 'weakly-tested': 5}_
_edges by policy: {'beliefs': 17, 'rolls_up': 4, 'qualifiers': 7, 'demoted': 6}_