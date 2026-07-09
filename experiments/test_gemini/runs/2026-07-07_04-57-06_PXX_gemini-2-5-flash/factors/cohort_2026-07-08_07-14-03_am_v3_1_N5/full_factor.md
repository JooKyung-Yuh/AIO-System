# Full factor graph — cohort_2026-07-08_07-14-03_am_v3_1_N5

66 observations · 5 propose_test targets (asserted beliefs with no observation).

## Observations (φ) → beliefs (δ)
### F001 · P1 · primary_result · _Section 1_
- **context**: Our framework, termed Vision ARC (VARC); on the ARC-1 benchmark
- **intervention**: apply standard vision architectures, such as a vanilla Vision Transformer (ViT), to perform image-to-image mapping.
- **observed**: achieves accuracy  [60.4%]  [metric: accuracy]
    - ↑ _✓ tested_ (1.0) Visual learning enables abstraction without language
    - ↑ _~ weak_ (0.4) majority voting consolidates multi-view predictions for accuracy
    - ↑ _✓ tested_ (0.4) Canvas enables geometric augmentations for invariance
    - ↑ _✓ tested_ (0.4) Explicit 2D positional modeling is essential
    - ↑ _✓ tested_ (0.4) Visual common sense is learnable from training data

### F002 · P11 · comparison · _Section 1_
- **context**: VARC; on the ARC-1 benchmark
- **intervention**: Combining VARC models through ensembling [29]  _vs_  using a small model with only 18 million parameters.  [18 million parameters]
- **observed**: further improves accuracy  [to 60.4%] (up)  [metric: accuracy]
    - ↑ _✓ tested_ (1.0) Visual learning enables abstraction without language
    - ↑ _✓ tested_ (0.4) Explicit 2D positional modeling is essential
    - ↑ _✓ tested_ (0.4) Canvas enables geometric augmentations for invariance
    - ↑ _✓ tested_ (0.4) Visual common sense is learnable from training data

### F003 · P12 · primary_result · _Section 1_
- **context**: on the ARC-1 benchmark
- **intervention**: Combining VARC models through ensembling [29]
- **observed**: matching the reported average human performance [31] on the ARC-1 dataset. (flat)  [metric: accuracy]
    - ↑ _✓ tested_ (1.0) Visual learning enables abstraction without language
    - ↑ _✓ tested_ (0.4) Explicit 2D positional modeling is essential
    - ↑ _✓ tested_ (0.4) Canvas enables geometric augmentations for invariance
    - ↑ _✓ tested_ (0.4) Visual common sense is learnable from training data

### F004 · P7 · primary_result · _Section 1_
- **intervention**: represent the inputs on a "canvas" with flexible geometric transformations
- **observed**: shows strong performance on the ARC benchmarks (e.g., Fig. 2).
    - ↑ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F005 · P8 · primary_result · _Section 1_
- **context**: VARC; on the ARC-1 benchmark; using a small model with only 18 million parameters.  [18 million parameters]
- **intervention**: apply standard vision architectures, such as a vanilla Vision Transformer (ViT), to perform image-to-image mapping.
- **observed**: achieves accuracy  [54.5%]  [metric: accuracy]
    - ↑ _✓ tested_ (1.0) Visual learning enables abstraction without language

### F006 · P9 · primary_result · _Section 1_
- **context**: VARC; on the ARC-1 benchmark; using a small model with only 18 million parameters.  [18 million parameters]
- **intervention**: apply standard vision architectures, such as a vanilla Vision Transformer (ViT), to perform image-to-image mapping.  _vs_  recurrent models [53, 27]
- **observed**: substantially surpasses the best recurrent methods [53, 27] that are also trained from scratch on ARC. (up)  [metric: accuracy]
    - ↑ _✓ tested_ (0.4) Visual learning enables abstraction without language
    - ↑ _✓ tested_ (0.4) Canvas enables geometric augmentations for invariance
    - ↑ _✓ tested_ (0.4) Explicit 2D positional modeling is essential
    - ↑ _~ weak_ (0.2) majority voting consolidates multi-view predictions for accuracy

### F007 · P16 · primary_result · _Figure 2_
- **context**: VARC
- **observed**: correctly solves these challenging tasks.
    - ↑ _✓ tested_ (1.0) Visual learning enables abstraction without language
    - ↑ _✓ tested_ (0.4) Explicit 2D positional modeling is essential
    - ↑ _✓ tested_ (0.4) Canvas enables geometric augmentations for invariance
    - ↑ _✓ tested_ (0.4) Visual common sense is learnable from training data

### F008 · P17 · primary_result · _Figure 6_
- **context**: Test-time training (TTT).
- **intervention**: We perform test-time training for each new task T independently.
- **observed**: During test-time training, the prediction from Xinfer becomes progressively more accurate, with the model finally generating the correct prediction. (up)
    - ↑ _✓ tested_ (0.6) Visual common sense is learnable from training data
    - ↑ _~ weak_ (0.2) Some ARC tasks are solvable from scratch
    - ↑ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F009 · P19 · comparison · _Table 1_
- **context**: ViT  [width 384, depth 5, #params 6M, Gflops 10]; ViT  [width 512, depth 10, #params 18M, Gflops 28]; ViT  [width 768, depth 20, #params 66M, Gflops 99]
- **intervention**: We compare variants of ViTs and U-Nets of similar sizes.  _vs_  U-Net  [setting (a), #params 7M, Gflops 18]
- **observed**: ViT models show higher accuracy than U-Net models  [ViT accuracies: 44.4, 54.5, 53.0; U-Net accuracies: 42.8, 47.5, 48.3] (up)  [metric: acc.]
    - ↑ _✓ tested_ (0.6) Visual learning enables abstraction without language
    - ↑ _~ weak_ (0.4) Classical vision backbones can address ARC effectively
    - ↑ _✓ tested_ (0.4) Explicit 2D positional modeling is essential
    - ↑ _✓ tested_ (0.4) Canvas enables geometric augmentations for invariance

### F010 · P20 · comparison · _Figure 7_
- **context**: Effects of visual priors in VARC.; ARC-1 evaluation set.; The model used is ViT-18M.
- **intervention**: Entries (a-c) use a patch size of 1×1 on a 32×32 canvas, whereas entries (d-f) use a patch size of 2×2 on a 64×64 canvas.  _vs_  We start from a naïve baseline with components (b-f) removed.
- **observed**: These vision priors cumulatively yield improvement (a→f)  [27.7 improvement] (up)  [metric: Accuracy]
    - ↑ _✓ tested_ (1.0) Explicit 2D positional modeling is essential

### F011 · P21 · comparison · _Figure 7_
- **context**: Effects of visual priors in VARC.; ARC-1 evaluation set.; The model used is ViT-18M.
- **intervention**: Entries (a-c) use a patch size of 1×1 on a 32×32 canvas, whereas entries (d-f) use a patch size of 2×2 on a 64×64 canvas.  _vs_  This is observed in both (b) absolute and (c) relative positional embeddings.
- **observed**: the canvas-based designs (c→f) contribute an gain.  [11.5 gain] (up)  [metric: Accuracy]
    - ↑ _✓ tested_ (1.0) Explicit 2D positional modeling is essential

### F012 · P22 · comparison · _Section 5.1_
- **context**: 2D positional embedding.; Patchification.; Translation and scale augmentation.
- **intervention**: starting from a baseline (a) without the other components in this figure.  _vs_  starting from a baseline (a) without the other components in this figure.
- **observed**: These priors jointly have a gain  [27.7 points] (up)
    - ↑ _✓ tested_ (0.8) Explicit 2D positional modeling is essential
    - ↑ _✓ tested_ (0.2) Canvas enables geometric augmentations for invariance
    - ↑ _✓ tested_ (0.2) Canvas patchification enriches data space, reduces overfitting

### F013 · P23 · comparison · _Section 5.1_
- **context**: Patchification.; Translation and scale augmentation.
- **intervention**: we advance from 1×1 patches on a 32×32 canvas to 2×2 patches on a 64×64 canvas.  _vs_  This is observed in both (b) absolute and (c) relative positional embeddings.
- **observed**: the canvas-based designs (c–f) has a gain.  [11.5 points] (up)
    - ↑ _✓ tested_ (1.0) Canvas patchification enriches data space, reduces overfitting
    - ↑ _✓ tested_ (0.6) Explicit 2D positional modeling is essential
    - ↑ _✓ tested_ (0.2) Canvas enables geometric augmentations for invariance

### F014 · P24 · primary_result · _Section 5.1_
- **observed**: Extending from 1D posi-tional embedding to its 2D counterpart is beneficial (up)
    - ↑ _✓ tested_ (0.2) Canvas patchification enriches data space, reduces overfitting

### F015 · P25 · primary_result · _Section 5.1_
- **context**: 2D positional embedding.
- **intervention**: we re-place the 2D ROPE in Fig. 7(f) with a 1D ROPE  _vs_  This is observed in both (b) absolute and (c) relative positional embeddings.
- **observed**: observe a degradation  [3.5 points, from 54.5 to 51.0] (down)
    - ↑ _✓ tested_ (0.6) Canvas patchification enriches data space, reduces overfitting
    - ↑ _✓ tested_ (0.2) Explicit 2D positional modeling is essential

### F016 · P26 · primary_result · _Section 5.1_
- **intervention**: we advance from 1×1 patches on a 32×32 canvas to 2×2 patches on a 64×64 canvas.
- **observed**: The entries Fig. 7(d-f) all benefit from this design. (up)
    - ↑ _✓ tested_ (0.2) Canvas enables geometric augmentations for invariance

### F017 · P28 · comparison · _Section 5.1_
- **context**: Patchification.; the scaling ratio is fixed as 2x.; This can be interpreted as one-pixel translation augmentation on the canvas.
- **intervention**: we advance from 1×1 patches on a 32×32 canvas to 2×2 patches on a 64×64 canvas.
- **observed**: the 2×2 patchification leads to a noticeable gain  [2.4 points, improving from 43.0 to 45.4] (up)
    - ↑ _✓ tested_ (0.8) Canvas enables geometric augmentations for invariance
    - ↑ _✓ tested_ (0.2) Canvas patchification enriches data space, reduces overfitting
    - ↑ _~ weak_ (0.2) Scale augmentation yields substantial gain due to ViT bias

### F018 · P34 · comparison · _Section 5.1_
- **context**: Translation and scale augmentation.
- **intervention**: we apply fully flexible translation augmen-tation on the canvas.
- **observed**: this setting yields an additional gain  [2.9 points (from 45.4 to 48.3)] (up)
    - ↑ _✓ tested_ (0.8) Canvas enables geometric augmentations for invariance
    - ↑ _✓ tested_ (0.2) Visual common sense is learnable from training data

### F019 · P35 · comparison · _Section 5.1_
- **context**: Translation and scale augmentation.
- **intervention**: we further ap-ply the scale augmentation enabled by the concept of can-vas.
- **observed**: Scale augmentation yields a substantial gain  [6.2 points] (up)
    - ↑ _✓ tested_ (0.8) Canvas enables geometric augmentations for invariance
    - ↑ _~ weak_ (0.2) Scale augmentation yields substantial gain due to ViT bias
    - ↑ _~ weak_ (0.2) Some ARC tasks are solvable from scratch

### F020 · P29 · comparison · _Figure 8_
- **context**: The circle areas de-note model sizes.
- **intervention**: ViTs with different width (x-axis) and depth.
- **observed**: increasing depth and/or width leads to higher accuracy (up)  [metric: Accuracy (%)]
    - _(no belief edge)_

### F021 · P30 · comparison · _Figure 9_
- **intervention**: with vs. without offline train-ing, and joint vs. independent for each task.  _vs_  with vs. without offline train-ing, and joint vs. independent for each task.
- **observed**: offline training improves performance  [54.5 vs 29.1] (up)  [metric: Accuracy (%)]
    - ↑ _✓ tested_ (0.8) Visual common sense is learnable from training data
    - ↑ _~ weak_ (0.2) Multiple test tasks cannot be assumed available simultaneously

### F022 · P31 · comparison · _Figure 9_
- **intervention**: with vs. without offline train-ing, and joint vs. independent for each task.  _vs_  with vs. without offline train-ing, and joint vs. independent for each task.
- **observed**: TTT independently performs better than TTT jointly  [54.5 vs 26.4] (up)  [metric: Accuracy (%)]
    - ↑ _~ weak_ (0.2) Some ARC tasks are solvable from scratch

### F023 · P36 · comparison · _Section 5.2_
- **context**: ViT vs. U-Net.; We evaluate three model sizes for each architecture.
- **intervention**: we compare ViT with U-Nets, a type of convolutional network.  _vs_  we compare ViT with U-Nets, a type of convolutional network.
- **observed**: ViTs consistently per-form better (up)
    - ↑ _✓ tested_ (0.4) Single pixel error invalidates entire ARC prediction

### F024 · P38 · comparison · _Section 5.2_
- **context**: Scalability.
- **intervention**: we show ViTs with varying depths and widths.
- **observed**: our method demonstrates good scalability: increasing depth and/or width leads to higher accuracy (up)
    - ↑ _✓ tested_ (0.4) Single pixel error invalidates entire ARC prediction

### F025 · P39 · comparison · _Section 5.2_
- **context**: as shown in Tab. 1 for the 66M ViT model.
- **observed**: this larger model achieves higher training accuracy (up)
    - ↑ _~ weak_ (0.6) majority voting consolidates multi-view predictions for accuracy
    - ↑ _✓ tested_ (0.2) Single pixel error invalidates entire ARC prediction
    - ↑ _✓ tested_ (0.2) Visual learning enables abstraction without language
- ⚠️ field mismatch: ['intervention']

### F026 · P40 · comparison · _Section 5.2_
- **context**: Test-time training (TTT) strategies.
- **intervention**: we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.  _vs_  we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.
- **observed**: offline training greatly improves the per-formance of TTT (up)
    - ↑ _~ weak_ (0.6) majority voting consolidates multi-view predictions for accuracy
    - ↑ _✓ tested_ (0.4) Single pixel error invalidates entire ARC prediction
    - ↓ _~ weak_ (0.2) Multiple test tasks cannot be assumed available simultaneously
    - ↑ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F027 · P41 · primary_result · _Section 5.2_
- **context**: Test-time training (TTT) strategies.
- **intervention**: we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.
- **observed**: even without offline training, our TTT strategy can achieve nontrivial accuracy  [26.4]
    - ↑ _✓ tested_ (0.6) Single pixel error invalidates entire ARC prediction
    - ↑ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F028 · P42 · comparison · _Section 5.2_
- **context**: under a similar setting.
- **intervention**: we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.
- **observed**: This result outperforms that in [36] (up)
    - ↑ _✓ tested_ (0.6) Single pixel error invalidates entire ARC prediction
    - ↑ _✓ tested_ (0.2) Visual common sense is learnable from training data
    - ↑ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F029 · P43 · comparison · _Section 5.2_
- **context**: Test-time training (TTT) strategies.
- **intervention**: we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.  _vs_  we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.
- **observed**: performing TTT independently for each test task yields substantially better performance than doing so jointly across all test tasks  [by ~10 points] (up)
    - ↑ _✓ tested_ (0.4) Single pixel error invalidates entire ARC prediction
    - ↑ _~ weak_ (0.2) Some ARC tasks are solvable from scratch
    - ↑ _✓ tested_ (0.2) Visual learning enables abstraction without language
    - ↑ _~ weak_ (0.2) majority voting consolidates multi-view predictions for accuracy

### F030 · P44 · primary_result · _Section 5.2_
- **context**: Single-view vs. multi-view inference.
- **intervention**: we also examine the single-view inference accuracy.
- **observed**: Single-view inference has a decent pass@1 accuracy  [35.9]  [metric: we compare pass@1 accuracy.]
    - ↑ _✓ tested_ (0.6) Visual learning enables abstraction without language
    - ↑ _✓ tested_ (0.4) Explicit 2D positional modeling is essential
    - ↑ _✓ tested_ (0.4) Canvas enables geometric augmentations for invariance
    - ↑ _✓ tested_ (0.4) Visual common sense is learnable from training data
    - ↑ _✓ tested_ (0.2) Attention maps reveal pixel-to-pixel reasoning

### F031 · P45 · comparison · _Section 5.2_
- **context**: Single-view vs. multi-view inference.
- **observed**: multi-view inference further boosts  [to 49.8] (up)  [metric: we compare pass@1 accuracy.]
    - ↑ _✓ tested_ (0.6) Visual learning enables abstraction without language
    - ↑ _✓ tested_ (0.4) Canvas enables geometric augmentations for invariance
    - ↑ _✓ tested_ (0.4) Explicit 2D positional modeling is essential
    - ↑ _✓ tested_ (0.4) Visual common sense is learnable from training data
    - ↑ _✓ tested_ (0.2) Single pixel error invalidates entire ARC prediction
    - ↑ _✓ tested_ (0.2) Transformer layers specialize in different structures/contexts
    - ↑ _~ weak_ (0.2) majority voting consolidates multi-view predictions for accuracy
- ⚠️ field mismatch: ['intervention']

### F032 · P48 · primary_result · _Section 5.3_
- **context**: System-level Comparisons.; Our method does not rely on such data; uses a model that is several orders of magnitude smaller.
- **intervention**: we compare with leading results using LLMs or recurrent models, on ARC-1 and ARC-2.  _vs_  LLM-based results are from the ARC-AGI leader-board [18].
- **observed**: Our model compares favorably with some of the most powerful LLMs at the time their results were reported: in-cluding Deepseek, Claude, o3, and GPT-5 (up)  [metric: ARC-1]
    - ↑ _✓ tested_ (0.8) Visual learning enables abstraction without language
    - ↑ _~ weak_ (0.4) majority voting consolidates multi-view predictions for accuracy
    - ↑ _✓ tested_ (0.4) Explicit 2D positional modeling is essential
    - ↑ _✓ tested_ (0.4) Canvas enables geometric augmentations for invariance
    - ↑ _✓ tested_ (0.4) Visual common sense is learnable from training data

### F033 · P49 · comparison · _Section 5.3_
- **context**: In the controlled setting of training from scratch on ARC data
- **intervention**: we compare with leading results using LLMs or recurrent models, on ARC-1 and ARC-2.  _vs_  HRM, TRM, and our VARC are trained from scratch only on ARC data.
- **observed**: our method substantially outperforms the recur-rent models: HRM [53] and TRM [27]. (up)  [metric: ARC-1]
    - ↑ _✓ tested_ (0.8) Visual learning enables abstraction without language
    - ↑ _✓ tested_ (0.4) Canvas enables geometric augmentations for invariance
    - ↑ _✓ tested_ (0.4) Visual common sense is learnable from training data
    - ↑ _✓ tested_ (0.4) Explicit 2D positional modeling is essential
    - ↑ _✓ tested_ (0.2) Transformer layers specialize in different structures/contexts

### F034 · P50 · comparison · _Section 5.3_
- **context**: In the controlled setting of training from scratch on ARC data
- **intervention**: we compare with leading results using LLMs or recurrent models, on ARC-1 and ARC-2.  _vs_  HRM, TRM, and our VARC are trained from scratch only on ARC data.
- **observed**: Our VARC with 18M parameters is better than TRM on ARC-1  [~10 points better, a >20% relative improvement] (up)  [metric: ARC-1]
    - ↑ _✓ tested_ (0.8) Visual learning enables abstraction without language
    - ↑ _✓ tested_ (0.4) Canvas enables geometric augmentations for invariance
    - ↑ _✓ tested_ (0.4) Explicit 2D positional modeling is essential
    - ↑ _✓ tested_ (0.4) Visual common sense is learnable from training data
    - ↑ _✓ tested_ (0.2) Transformer layers specialize in different structures/contexts

### F035 · P51 · comparison · _Section 5.3_
- **context**: System-level Comparisons.
- **intervention**: we ensemble one ViT and one U-Net, each with test-time training run four times.  _vs_  Our single-model result is based on ViT, with mean±std of 54.5±0.7 (ARC-1) and 8.3±0.4 (ARC-2) over four runs.
- **observed**: Doing so boosts our result  [to 60.4] (up)  [metric: ARC-1]
    - ↑ _✓ tested_ (0.8) Visual learning enables abstraction without language
    - ↑ _✓ tested_ (0.4) Explicit 2D positional modeling is essential
    - ↑ _✓ tested_ (0.4) Canvas enables geometric augmentations for invariance
    - ↑ _✓ tested_ (0.4) Visual common sense is learnable from training data
    - ↑ _✓ tested_ (0.2) Transformer layers specialize in different structures/contexts

### F036 · P52 · comparison · _Section 5.3_
- **context**: System-level Comparisons.
- **intervention**: we ensemble one ViT and one U-Net, each with test-time training run four times.
- **observed**: This result closes the gap with the re-ported average human performance  [60.4 vs 60.2 [31]] (flat)  [metric: ARC-1]
    - ↑ _✓ tested_ (0.6) Visual learning enables abstraction without language
    - ↑ _✓ tested_ (0.6) Visual common sense is learnable from training data
    - ↑ _✓ tested_ (0.4) Canvas enables geometric augmentations for invariance
    - ↑ _✓ tested_ (0.4) Explicit 2D positional modeling is essential

### F037 · P46 · primary_result · _Table 3_
- **context**: LLM-based results are from the ARC-AGI leader-board [18].; HRM, TRM, and our VARC are trained from scratch only on ARC data.; Our ensemble result aggregates an 18M ViT and a 55M U-Net, each with test-time training performed four times.
- **intervention**: Our ensemble result aggregates an 18M ViT and a 55M U-Net, each with test-time training performed four times.
- **observed**: VARC (ensemble) achieves 60.4 on ARC-1 and 11.1 on ARC-2  [60.4, 11.1]  [metric: ARC-1]
    - ↑ _✓ tested_ (0.8) Visual learning enables abstraction without language
    - ↑ _✓ tested_ (0.4) Canvas enables geometric augmentations for invariance
    - ↑ _✓ tested_ (0.4) Explicit 2D positional modeling is essential
    - ↑ _✓ tested_ (0.4) Visual common sense is learnable from training data
    - ↑ _✓ tested_ (0.2) Task embedding visualization suggests learning task relations
- ⚠️ field mismatch: ['intervention']

### F038 · P47 · primary_result · _Table 3_
- **context**: LLM-based results are from the ARC-AGI leader-board [18].; HRM, TRM, and our VARC are trained from scratch only on ARC data.; Our ensemble result aggregates an 18M ViT and a 55M U-Net, each with test-time training performed four times.
- **intervention**: Our ensemble result aggregates an 18M ViT and a 55M U-Net, each with test-time training performed four times.
- **observed**: VARC (ensemble) is comparable to avg. human performance on ARC-1  [VARC 60.4, avg. human 60.2] (flat)  [metric: ARC-1]
    - ↑ _✓ tested_ (0.4) Visual learning enables abstraction without language
    - ↑ _✓ tested_ (0.2) Task embedding visualization suggests learning task relations
- ⚠️ field mismatch: ['intervention']

### F039 · P53 · primary_result · _Section 6_
- **context**: Figure 11 visualizes the layer-wise attention maps for an-other test task.; A layer-wise map is the softmax attention map averaged across all pixels in the layer
- **observed**: some layers exhibit strong attention to the 3 × 3 neighborhood
    - ↑ _✓ tested_ (0.8) Attention maps reveal pixel-to-pixel reasoning
    - ↑ _~ weak_ (0.2) Some ARC tasks are solvable from scratch

### F040 · P54 · primary_result · _Section 6_
- **context**: Figure 11 visualizes the layer-wise attention maps for an-other test task.; A layer-wise map is the softmax attention map averaged across all pixels in the layer
- **observed**: some other layers (e.g., layers 7-9) focus on the outward-radiating rays
    - ↑ _✓ tested_ (0.8) Transformer layers specialize in different structures/contexts
    - ↑ _✓ tested_ (0.2) Visual common sense is learnable from training data

### F041 · P57 · primary_result · _Section 6_
- **context**: t-SNE of task embeddings.; With 400 training tasks in ARC-1, our model learns 400 distinct task embeddings in offline training.; Each point corresponds to a task..
- **intervention**: We visu-alize these 400 embeddings in the 2D space by t-SNE [39]
- **observed**: the top-left corner in Fig. 12 shows two tasks related to coloring; the bottom-left corner shows two tasks related to generalized logic operations (i.e., AND/OR/XOR).
    - ↑ _✓ tested_ (0.8) Task embedding visualization suggests learning task relations
    - ↑ _✓ tested_ (0.2) Visual common sense is learnable from training data

### F042 · P59 · primary_result · _Figure 14_
- **intervention**: Offline training data scaling: effect of varying
- **observed**: Increasing the amount of offline training data is beneficial (up)
    - ↑ _✓ tested_ (0.2) Single pixel error invalidates entire ARC prediction
- ⚠️ field mismatch: ['intervention']

### F043 · P60 · primary_result · _Figure 15_
- **intervention**: Offline training task diversity scaling: effect of varying
- **observed**: Increasing task diversity is beneficial. (up)
    - ↑ _✓ tested_ (0.2) Single pixel error invalidates entire ARC prediction
- ⚠️ field mismatch: ['intervention']

### F044 · P61 · primary_result · _Section B.1_
- **context**: RE-ARC dataset [22] in our offline training
- **intervention**: Using only the original ARC training data, without any RE-ARC data
- **observed**: our method achieves a decent accuracy  [31.5%]  [metric: accuracy]
    - ↑ _✓ tested_ (0.2) Single pixel error invalidates entire ARC prediction

### F045 · P62 · primary_result · _Section B.1_
- **context**: RE-ARC dataset [22] in our offline training
- **intervention**: adding 10, 100, and 1,000 pairs per task from RE-ARC  _vs_  Using only the original ARC training data, without any RE-ARC data
- **observed**: increases  [to 38.6, 52.3, and 54.0] (up)  [metric: accuracy]
    - ↑ _✓ tested_ (0.8) Visual common sense is learnable from training data
    - ↑ _✓ tested_ (0.2) Single pixel error invalidates entire ARC prediction

### F046 · P63 · primary_result · _Section B.1_
- **intervention**: trained on 0, 16, 80, and 400 tasks
- **observed**: increases  [from 26.4 to 43.1, 49.6, and 54.5] (up)  [metric: accuracy]
    - ↑ _✓ tested_ (0.4) Visual common sense is learnable from training data
    - ↑ _✓ tested_ (0.4) Task embedding visualization suggests learning task relations
    - ↑ _✓ tested_ (0.2) Single pixel error invalidates entire ARC prediction

### F047 · P65 · primary_result · _Section B.2_
- **context**: multi-view inference with many views (510); On ARC-1
- **intervention**: as the number of proposals (k) increases
- **observed**: is  [49.8, 54.5, and 66.3, when k is 1, 2, and 300] (up)  [metric: pass@k accu-racy]
    - ↑ _~ weak_ (0.4) majority voting consolidates multi-view predictions for accuracy
    - ↑ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F048 · P66 · primary_result · _Section B.2_
- **context**: multi-view inference with many views (510); On ARC-1
- **observed**: this result reveals the upper-bound performance (66.3) of our method, even if oracle voting were applied.  [metric: pass@k accu-racy]
    - ↑ _~ weak_ (0.4) majority voting consolidates multi-view predictions for accuracy
    - ↓ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F049 · P70 · primary_result · _Figure 17_
- **context**: ARC-1
- **observed**: Successful and failed examples
    - ↑ _✓ tested_ (0.8) Visual learning enables abstraction without language
    - ↑ _✓ tested_ (0.6) Visual common sense is learnable from training data
    - ↑ _✓ tested_ (0.4) Explicit 2D positional modeling is essential
    - ↑ _✓ tested_ (0.4) Canvas enables geometric augmentations for invariance
    - ↑ _~ weak_ (0.2) Some ARC tasks are solvable from scratch

### F050 · P71 · primary_result · _Figure 17_
- **context**: test tasks
- **intervention**: solved by VARC
- **observed**: successfully solved  [metric: correct output]
    - ↓ _✓ tested_ (0.2) Visual learning enables abstraction without language
    - ↑ _✓ tested_ (0.2) Visual common sense is learnable from training data
    - ↑ _~ weak_ (0.2) Some ARC tasks are solvable from scratch
    - ↑ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F051 · P72 · primary_result · _Figure 17_
- **context**: test tasks
- **intervention**: unsolved by VARC
- **observed**: unsolved  [metric: correct output]
    - ↑ _✓ tested_ (0.6) Visual learning enables abstraction without language
    - ↑ _✓ tested_ (0.6) Visual common sense is learnable from training data
    - ↑ _✓ tested_ (0.4) Explicit 2D positional modeling is essential
    - ↑ _✓ tested_ (0.4) Canvas enables geometric augmentations for invariance
    - ↓ _✓ tested_ (0.2) Visual learning enables abstraction without language
    - ↑ _~ weak_ (0.2) Some ARC tasks are solvable from scratch

### F052 · P73 · primary_result · _Figure 17_
- **context**: Task 15663ba9; Task 981571dc; Task 15696249; Task 67c52801
- **intervention**: first and second solutions proposed by VARC
- **observed**: VARC's Attempt 1 matches the Ground Truth  [Tasks: 15663ba9, 981571dc, 15696249, 67c52801] (flat)  [metric: Vote  [109, 57, 399, 35, 456, 10, 233, 123, 9, 6, 14, 8, 13, 9, 3, 2]]
    - ↓ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F053 · P74 · primary_result · _Figure 17_
- **context**: Task 8dae5dfc; Task 67636eac; Task aa4ec2a5; Task b457fec5
- **intervention**: first and second solutions proposed by VARC
- **observed**: VARC fails to solve the task  [Tasks: 8dae5dfc, 67636eac, aa4ec2a5, b457fec5] (down)  [metric: Vote  [109, 57, 399, 35, 456, 10, 233, 123, 9, 6, 14, 8, 13, 9, 3, 2]]
    - ↓ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F054 · P75 · primary_result · _Figure 18_
- **context**: ARC-2
- **observed**: Successful and failed examples
    - ↑ _✓ tested_ (0.4) Visual learning enables abstraction without language

### F055 · P76 · primary_result · _Figure 18_
- **context**: test tasks
- **intervention**: solved by VARC
- **observed**: successfully solved  [metric: correct output]
    - ↓ _✓ tested_ (0.2) Visual learning enables abstraction without language
    - ↑ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F056 · P77 · primary_result · _Figure 18_
- **context**: test tasks
- **intervention**: unsolved by VARC
- **observed**: unsolved  [metric: correct output]
    - ↓ _✓ tested_ (0.2) Visual learning enables abstraction without language
    - ↑ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F057 · P78 · primary_result · _Figure 18_
- **context**: Task 800d221b; Task 7666fa5d; Task 221dfab4; Task 7b80bb43
- **intervention**: first and second solutions proposed by VARC
- **observed**: VARC's Attempt 1 matches the Ground Truth  [Tasks: 800d221b, 7666fa5d, 221dfab4, 7b80bb43] (flat)  [metric: Vote  [99, 82, 410, 16, 30, 17, 168, 44, 21, 20, 7, 6, 14, 12, 67, 51]]
    - ↓ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F058 · P79 · primary_result · _Figure 18_
- **context**: Task 2b83f449; Task 2d0172a1; Task 3e6067c3; Task 7ed72f31
- **intervention**: first and second solutions proposed by VARC
- **observed**: VARC fails to solve the task  [Tasks: 2b83f449, 2d0172a1, 3e6067c3, 7ed72f31] (down)  [metric: Vote  [99, 82, 410, 16, 30, 17, 168, 44, 21, 20, 7, 6, 14, 12, 67, 51]]
    - ↓ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F059 · P80 · primary_result · _Figure 19_
- **context**: an example in Fig. 19
- **observed**: Ambiguous examples
    - ↑ _✓ tested_ (0.8) Some ARC tasks have multiple plausible rules
    - ↑ _~ weak_ (0.2) Model interprets ambiguous rules with multiple plausible guesses
    - ↑ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F060 · P81 · primary_result · _Figure 19_
- **context**: an example in Fig. 19
- **observed**: some may admit multiple plausible explanations or rules
    - ↑ _✓ tested_ (0.6) Some ARC tasks have multiple plausible rules
    - ↑ _~ weak_ (0.2) Model interprets ambiguous rules with multiple plausible guesses
    - ↓ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F061 · P82 · primary_result · _Figure 19_
- **context**: inference example (bottom panel) involves this situation ("touching"); Task 09c534e7
- **intervention**: our model attempts to interpret the rule as either "going-through-only" (attempt 1) or "touching" (attempt 2)  _vs_  our model attempts to interpret the rule as either "going-through-only" (attempt 1) or "touching" (attempt 2)
- **observed**: Attempt 2 matches Ground Truth, Attempt 1 does not (up)  [metric: Ground truth]
    - ↑ _✓ tested_ (0.6) Some ARC tasks have multiple plausible rules
    - ↑ _~ weak_ (0.2) Model interprets ambiguous rules with multiple plausible guesses

### F062 · P83 · primary_result · _Figure 20_
- **context**: 4 test tasks in ARC eval; Task 09c534e7
- **observed**: task that was not correctly solved (down)  [metric: correctly solved]
    - ↑ _✓ tested_ (0.8) Transformer layers specialize in different structures/contexts

### F063 · P84 · primary_result · _Figure 21_
- **context**: layer-wise attention maps; demonstration examples (on the left) are provided for reference; Task 0607ce86; Task 0bb8deee; Task 1c56ad9f; Task 1d0a4b61
- **observed**: Attention patterns vary across layers  [metric: per-pixel softmax attention maps averaged across all pixels in that layer]
    - ↑ _✓ tested_ (0.8) Transformer layers specialize in different structures/contexts

### F064 · P85 · primary_result · _Figure 22 caption_
- **context**: the grid augmented with a given scale ratio of 2×; the full canvas is not shown for brevity
- **intervention**: test-time training progresses
- **observed**: gradually converge toward the correct output (up)  [metric: model's predictions converge toward the correct output]
    - ↑ _✓ tested_ (0.4) Transformer layers specialize in different structures/contexts
    - ↑ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F065 · P86 · primary_result · _Figure 22 caption_
- **context**: In early epochs
- **intervention**: test-time training progresses
- **observed**: model produces coarse and imprecise structures
    - ↑ _✓ tested_ (0.4) Visual common sense is learnable from training data
    - ↑ _✓ tested_ (0.2) Visual learning enables abstraction without language

### F066 · P87 · comparison · _Figure 22 caption_
- **context**: in later epochs
- **intervention**: test-time training progresses
- **observed**: model can improve the solutions (up)
    - ↑ _✓ tested_ (0.4) Visual common sense is learnable from training data
    - ↑ _✓ tested_ (0.2) Visual learning enables abstraction without language

## propose_test — asserted but untested here (AIO differentiator)

- **ASM_arc_colors_lack_real_world_semantic** — ARC colors lack real-world semantic meaning  (_assumption_, 1 raw nodes)
- **ASM_auxiliary_tasks_translation_scale_invariant** — auxiliary tasks are translation/scale invariant  (_assumption_, 1 raw nodes)
- **ASM_larger_models_current_setting_lead_overfitting** — Larger models in current setting lead to overfitting  (_assumption_, 1 raw nodes)
- **MECH_attention_masks_improve_accuracy_focusing_foregrounds** — Attention masks improve accuracy by focusing on foregrounds  (_mechanism_, 1 raw nodes)
- **MECH_average_pooling_aggregates_multi_pixel_canvas** — average pooling aggregates multi-pixel canvas predictions  (_mechanism_, 1 raw nodes)

_belief edge status tally: {'tested': 147, 'weakly-tested': 25}_