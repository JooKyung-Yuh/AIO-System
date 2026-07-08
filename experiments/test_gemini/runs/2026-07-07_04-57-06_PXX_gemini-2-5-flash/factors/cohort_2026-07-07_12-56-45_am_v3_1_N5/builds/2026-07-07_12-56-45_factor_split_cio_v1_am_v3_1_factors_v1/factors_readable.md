# Readable factors — 2026-07-07_12-56-45_factor_split_cio_v1_am_v3_1_factors_v1

67 factors, 9 with a field-category mismatch.

### F001  (primary_result, observed)
*from Section 1 (S8)*
- **context**: Our framework, termed Vision ARC (VARC); on the ARC-1 benchmark
- **intervention**: formulate ARC within a vision paradigm, framing it as an image-to-image translation problem.
- **observed**: achieves accuracy  [metric: accuracy]
- **↑ strengthens** [mechanism] Visual learning directly enables abstraction and inference without language.

### F002  (primary_result, observed)
*from Section 1 (S37)*
- **context**: Our framework, termed Vision ARC (VARC)
- **intervention**: approach ARC from a vision-centric perspective.
- **observed**: shows strong performance on the ARC benchmarks (e.g., Fig. 2).  [metric: —]
- **↑ strengthens** [mechanism] Visual learning directly enables abstraction and inference without language.

### F003  (primary_result, observed)
*from Section 1 (S38)*
- **context**: VARC; on the ARC-1 benchmark; using a small model with only 18 million parameters.
- **intervention**: approach ARC from a vision-centric perspective.
- **observed**: achieves accuracy  [metric: accuracy]
- **↑ strengthens** [mechanism] Visual learning directly enables abstraction and inference without language.

### F004  (primary_result, observed)
*from Section 1 (S39)*
- **context**: VARC; on the ARC-1 benchmark; using a small model with only 18 million parameters.
- **intervention**: approach ARC from a vision-centric perspective.  vs reference: recurrent models [53, 27]
- **observed**: substantially surpasses the best recurrent methods [53, 27] that are also trained from scratch on ARC. (up)  [metric: accuracy]
- **↑ strengthens** [mechanism] Visual learning directly enables abstraction and inference without language.

### F005  (comparison, observed)
*from Section 1 (S41)*
- **context**: VARC; on the ARC-1 benchmark
- **intervention**: Combining VARC models through ensembling [29]  vs reference: achieves accuracy
- **observed**: further improves accuracy (up)  [metric: accuracy]
- **↑ strengthens** [mechanism] Majority voting consolidates multi-view predictions to improve accuracy.
- ⚠️ **field mismatch**: `reference` holds ['P8'] (wrong category)

### F006  (primary_result, observed)
*from Section 1 (S41)*
- **context**: VARC; on the ARC-1 benchmark
- **intervention**: Combining VARC models through ensembling [29]
- **observed**: matching the reported average human performance [31] on the ARC-1 dataset. (flat)  [metric: accuracy]

### F007  (primary_result, observed)
*from Figure 2 (S55)*
- **context**: VARC
- **observed**: correctly solves these challenging tasks.  [metric: —]
- **↑ strengthens** [mechanism] Visual learning directly enables abstraction and inference without language.

### F008  (primary_result, observed)
*from Section 3.5 (S148)*
- **context**: Test-time training (TTT).; At inference time, we are given Demo={(xi, Yi)}m=1 with both input and output accessible; the model is required to make prediction for a given Xinfer in this new task T.; at inference time, the model is initialized from offline training, fine-tuned with test-time training only for the single new task T, and then performs inference on Xinfer.; As the new demo pairs in Demo are very few
- **intervention**: We perform test-time training for each new task T independently.
- **observed**: this test-time training process remains reasonably fast  [metric: —]
- **↑ strengthens** [mechanism] Majority voting consolidates multi-view predictions to improve accuracy.
- ⚠️ **field mismatch**: `context` holds ['A9'] (wrong category)

### F009  (primary_result, observed)
*from Figure 6 (S139)*
- **context**: —
- **observed**: During test-time training, the prediction from Xinfer becomes progressively more accurate, with the model finally generating the correct prediction. (up)  [metric: —]
- **↑ strengthens** [mechanism] Test-time training refines color and spatial arrangement, adapting to tasks.

### F010  (comparison, observed)
*from Table 1 (S191)*
- **context**: ViT; ViT; ViT; U-Net; U-Net; U-Net
- **intervention**: We compare variants of ViTs and U-Nets of similar sizes.  vs reference: U-Net
- **observed**: ViT models show higher accuracy than U-Net models (up)  [metric: acc.]

### F011  (comparison, observed)
*from Figure 7 (S198)*
- **context**: Effects of visual priors in VARC.; ARC-1 evaluation set.; The model used is ViT-18M.
- **intervention**: Entries (a-c) use a patch size of 1×1 on a 32×32 canvas, whereas entries (d-f) use a patch size of 2×2 on a 64×64 canvas.  vs reference: We start from a naïve baseline with components (b-f) removed.
- **observed**: These vision priors cumulatively yield improvement (a→f) (up)  [metric: Accuracy]
- **↑ strengthens** [mechanism] Canvas patchification enriches data space, reduces overfitting, learns spatial priors.
- **↑ strengthens** [mechanism] Canvas enables augmentations to learn geometric transformation invariance.

### F012  (comparison, observed)
*from Figure 7 (S198)*
- **context**: Effects of visual priors in VARC.; ARC-1 evaluation set.; The model used is ViT-18M.
- **intervention**: Entries (a-c) use a patch size of 1×1 on a 32×32 canvas, whereas entries (d-f) use a patch size of 2×2 on a 64×64 canvas.
- **observed**: the canvas-based designs (c→f) contribute an gain. (up)  [metric: Accuracy]
- **↑ strengthens** [mechanism] Canvas patchification enriches data space, reduces overfitting, learns spatial priors.
- **↑ strengthens** [mechanism] Canvas enables augmentations to learn geometric transformation invariance.

### F013  (comparison, observed)
*from Section 5.1 (S200)*
- **context**: 2D positional embedding.; Patchification.; Translation and scale augmentation.
- **intervention**: starting from a baseline (a) without the other components in this figure.  vs reference: starting from a baseline (a) without the other components in this figure.
- **observed**: These priors jointly have a gain (up)  [metric: —]

### F014  (comparison, observed)
*from Section 5.1 (S200)*
- **context**: Patchification.; Translation and scale augmentation.
- **intervention**: we advance from 1×1 patches on a 32×32 canvas to 2×2 patches on a 64×64 canvas.
- **observed**: the canvas-based designs (c–f) has a gain. (up)  [metric: —]

### F015  (primary_result, observed)
*from Section 5.1 (S202)*
- **context**: 2D positional embedding.; This is observed in both (b) absolute and (c) relative positional embeddings.
- **observed**: Extending from 1D posi-tional embedding to its 2D counterpart is beneficial (up)  [metric: —]
- **↑ strengthens** [mechanism] Canvas patchification enriches data space, reduces overfitting, learns spatial priors.

### F016  (primary_result, observed)
*from Section 5.1 (S204)*
- **context**: 2D positional embedding.
- **intervention**: we re-place the 2D ROPE in Fig. 7(f) with a 1D ROPE
- **observed**: observe a degradation (down)  [metric: —]

### F017  (primary_result, observed)
*from Section 5.1 (S208)*
- **context**: Patchification.; A key design principle of our method is to prepare the input as a natural image.
- **intervention**: we advance from 1×1 patches on a 32×32 canvas to 2×2 patches on a 64×64 canvas.
- **observed**: The entries Fig. 7(d-f) all benefit from this design. (up)  [metric: —]
- **↑ strengthens** [mechanism] Canvas enables augmentations to learn geometric transformation invariance.

### F018  (comparison, observed)
*from Section 5.1 (S215)*
- **context**: Patchification.; the scaling ratio is fixed as 2x.; This can be interpreted as one-pixel translation augmentation on the canvas.
- **intervention**: we advance from 1×1 patches on a 32×32 canvas to 2×2 patches on a 64×64 canvas.
- **observed**: the 2×2 patchification leads to a noticeable gain (up)  [metric: —]
- **↑ strengthens** [mechanism] Canvas enables augmentations to learn geometric transformation invariance.

### F019  (comparison, observed)
*from Section 5.1 (S228)*
- **context**: Translation and scale augmentation.
- **intervention**: we apply fully flexible translation augmen-tation on the canvas.
- **observed**: this setting yields an additional gain (up)  [metric: —]

### F020  (comparison, observed)
*from Section 5.1 (S230)*
- **context**: Translation and scale augmentation.
- **intervention**: we further ap-ply the scale augmentation enabled by the concept of can-vas.
- **observed**: Scale augmentation yields a substantial gain (up)  [metric: —]
- **↑ strengthens** [mechanism] Visual learning directly enables abstraction and inference without language.

### F021  (comparison, observed)
*from Figure 8 (S219)*
- **context**: The circle areas de-note model sizes.
- **intervention**: ViTs with different width (x-axis) and depth.
- **observed**: increasing depth and/or width leads to higher accuracy (up)  [metric: Accuracy (%)]

### F022  (comparison, observed)
*from Figure 9 (S222)*
- **context**: —
- **intervention**: with vs. without offline train-ing, and joint vs. independent for each task.  vs reference: with vs. without offline train-ing, and joint vs. independent for each task.
- **observed**: offline training improves performance (up)  [metric: Accuracy (%)]
- **↑ strengthens** [mechanism] Offline training learns visual common sense from the training set.

### F023  (comparison, observed)
*from Figure 9 (S223)*
- **context**: —
- **intervention**: with vs. without offline train-ing, and joint vs. independent for each task.  vs reference: with vs. without offline train-ing, and joint vs. independent for each task.
- **observed**: TTT independently performs better than TTT jointly (up)  [metric: Accuracy (%)]

### F024  (comparison, observed)
*from Section 5.2 (S236)*
- **context**: ViT vs. U-Net.; We evaluate three model sizes for each architecture.
- **intervention**: we compare ViT with U-Nets, a type of convolutional network.  vs reference: we compare ViT with U-Nets, a type of convolutional network.
- **observed**: ViTs consistently per-form better (up)  [metric: —]
- **↓ weakens** [assumption] Joint TTT assumes multiple test tasks available simultaneously.

### F025  (comparison, observed)
*from Section 5.2 (S239)*
- **context**: Scalability.
- **intervention**: we show ViTs with varying depths and widths.
- **observed**: our method demonstrates good scalability: increasing depth and/or width leads to higher accuracy (up)  [metric: —]

### F026  (comparison, observed)
*from Section 5.2 (S241)*
- **context**: as shown in Tab. 1 for the 66M ViT model.
- **intervention**: as shown in Tab. 1 for the 66M ViT model.
- **observed**: this larger model achieves higher training accuracy (up)  [metric: —]
- ⚠️ **field mismatch**: `intervention` holds ['C132'] (wrong category)

### F027  (comparison, observed)
*from Section 5.2 (S244)*
- **context**: Test-time training (TTT) strategies.
- **intervention**: we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.  vs reference: we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.
- **observed**: offline training greatly improves the per-formance of TTT (up)  [metric: —]

### F028  (primary_result, observed)
*from Section 5.2 (S245)*
- **context**: Test-time training (TTT) strategies.
- **intervention**: we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.
- **observed**: even without offline training, our TTT strategy can achieve nontrivial accuracy  [metric: —]
- **↑ strengthens** [mechanism] Majority voting consolidates multi-view predictions to improve accuracy.
- **↑ strengthens** [assumption] Single pixel errors invalidate entire ARC predictions.

### F029  (comparison, observed)
*from Section 5.2 (S246)*
- **context**: under a similar setting.
- **intervention**: even without offline training, our TTT strategy can achieve nontrivial accuracy
- **observed**: This result outperforms that in [36] (up)  [metric: —]
- ⚠️ **field mismatch**: `intervention` holds ['P41'] (wrong category)

### F030  (comparison, observed)
*from Section 5.2 (S247)*
- **context**: Test-time training (TTT) strategies.
- **intervention**: we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.  vs reference: we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.
- **observed**: performing TTT independently for each test task yields substantially better performance than doing so jointly across all test tasks (up)  [metric: —]

### F031  (primary_result, observed)
*from Section 5.2 (S255)*
- **context**: Single-view vs. multi-view inference.; we adopt multi-view inference by default.
- **intervention**: we also examine the single-view inference accuracy.
- **observed**: Single-view inference has a decent pass@1 accuracy  [metric: we compare pass@1 accuracy.]
- **↑ strengthens** [mechanism] Visual learning directly enables abstraction and inference without language.

### F032  (comparison, observed)
*from Section 5.2 (S255)*
- **context**: Single-view vs. multi-view inference.
- **intervention**: we adopt multi-view inference by default.  vs reference: Single-view inference has a decent pass@1 accuracy
- **observed**: multi-view inference further boosts (up)  [metric: we compare pass@1 accuracy.]
- **↑ strengthens** [mechanism] Visual learning directly enables abstraction and inference without language.
- ⚠️ **field mismatch**: `intervention` holds ['C136'] (wrong category)
- ⚠️ **field mismatch**: `reference` holds ['P44'] (wrong category)

### F033  (primary_result, observed)
*from Section 5.3 (S264)*
- **context**: System-level Comparisons.; LLMs are pre-trained on internet-scale data, and some may also incor-porate multimodal data that include images.; Our method does not rely on such data; uses a model that is several orders of magnitude smaller.
- **intervention**: we compare with leading results using LLMs or recurrent models, on ARC-1 and ARC-2.
- **observed**: Our model compares favorably with some of the most powerful LLMs at the time their results were reported: in-cluding Deepseek, Claude, o3, and GPT-5 (up)  [metric: —]
- **↑ strengthens** [mechanism] Visual learning directly enables abstraction and inference without language.

### F034  (comparison, observed)
*from Section 5.3 (S267)*
- **context**: System-level Comparisons.; In the controlled setting of training from scratch on ARC data
- **intervention**: we compare with leading results using LLMs or recurrent models, on ARC-1 and ARC-2.
- **observed**: our method substantially outperforms the recur-rent models: HRM [53] and TRM [27]. (up)  [metric: —]
- **↑ strengthens** [mechanism] Visual learning directly enables abstraction and inference without language.

### F035  (comparison, observed)
*from Section 5.3 (S268)*
- **context**: System-level Comparisons.; In the controlled setting of training from scratch on ARC data
- **intervention**: we compare with leading results using LLMs or recurrent models, on ARC-1 and ARC-2.
- **observed**: Our VARC with 18M parameters is better than TRM on ARC-1 (up)  [metric: —]
- **↑ strengthens** [mechanism] Visual learning directly enables abstraction and inference without language.

### F036  (comparison, observed)
*from Section 5.3 (S271)*
- **context**: System-level Comparisons.
- **intervention**: we ensemble one ViT and one U-Net, each with test-time training run four times.
- **observed**: Doing so boosts our result (up)  [metric: —]

### F037  (comparison, observed)
*from Section 5.3 (S272)*
- **context**: System-level Comparisons.
- **intervention**: we ensemble one ViT and one U-Net, each with test-time training run four times.
- **observed**: This result closes the gap with the re-ported average human performance (flat)  [metric: —]

### F038  (primary_result, observed)
*from Table 3 (S262)*
- **context**: LLM-based results are from the ARC-AGI leader-board [18].; HRM, TRM, and our VARC are trained from scratch only on ARC data.; Our single-model result is based on ViT, with mean±std of 54.5±0.7 (ARC-1) and 8.3±0.4 (ARC-2) over four runs.; Our ensemble result aggregates an 18M ViT and a 55M U-Net, each with test-time training performed four times.
- **intervention**: Our ensemble result aggregates an 18M ViT and a 55M U-Net, each with test-time training performed four times.
- **observed**: VARC (ensemble) achieves 60.4 on ARC-1 and 11.1 on ARC-2  [metric: ARC-1]
- ⚠️ **field mismatch**: `intervention` holds ['C141'] (wrong category)

### F039  (primary_result, observed)
*from Table 3 (S263)*
- **context**: LLM-based results are from the ARC-AGI leader-board [18].; HRM, TRM, and our VARC are trained from scratch only on ARC data.; Our single-model result is based on ViT, with mean±std of 54.5±0.7 (ARC-1) and 8.3±0.4 (ARC-2) over four runs.; Our ensemble result aggregates an 18M ViT and a 55M U-Net, each with test-time training performed four times.
- **intervention**: Our ensemble result aggregates an 18M ViT and a 55M U-Net, each with test-time training performed four times.
- **observed**: VARC (ensemble) is comparable to avg. human performance on ARC-1 (flat)  [metric: ARC-1]
- ⚠️ **field mismatch**: `intervention` holds ['C141'] (wrong category)

### F040  (primary_result, observed)
*from Section 6 (S280)*
- **context**: Attention patterns.; Fig. 10 shows the attention patterns of our ViT model in a test task.; Figure 11 visualizes the layer-wise attention maps for an-other test task.; A layer-wise map is the softmax attention map averaged across all pixels in the layer
- **observed**: some layers exhibit strong attention to the 3 × 3 neighborhood  [metric: —]
- **↑ strengthens** [mechanism] Attention maps reveal correct pixel-to-pixel reasoning.

### F041  (primary_result, observed)
*from Section 6 (S281)*
- **context**: Attention patterns.; Fig. 10 shows the attention patterns of our ViT model in a test task.; Figure 11 visualizes the layer-wise attention maps for an-other test task.; A layer-wise map is the softmax attention map averaged across all pixels in the layer
- **observed**: some other layers (e.g., layers 7-9) focus on the outward-radiating rays  [metric: —]
- **↑ strengthens** [mechanism] Different layers focus on distinct structures and task-specific patterns.

### F042  (primary_result, observed)
*from Section 6 (S289)*
- **context**: t-SNE of task embeddings.; Our model is conditioned on a task token, with an embedding learned to represent each task.; With 400 training tasks in ARC-1, our model learns 400 distinct task embeddings in offline training.; Each point corresponds to a task..
- **intervention**: We visu-alize these 400 embeddings in the 2D space by t-SNE [39]
- **observed**: the top-left corner in Fig. 12 shows two tasks related to coloring; the bottom-left corner shows two tasks related to generalized logic operations (i.e., AND/OR/XOR).  [metric: —]
- **↑ strengthens** [mechanism] Task embedding visualization suggests learning relations between tasks.

### F043  (primary_result, observed)
*from Figure 14 (S357)*
- **context**: RE-ARC samples per task; evaluated on the ARC-1 eval set
- **intervention**: Offline training data scaling: effect of varying
- **observed**: Increasing the amount of offline training data is beneficial (up)  [metric: —]
- ⚠️ **field mismatch**: `intervention` holds ['E18'] (wrong category)

### F044  (primary_result, observed)
*from Figure 15 (S359)*
- **context**: the number of training tasks; evaluated on the ARC-1 eval set
- **intervention**: Offline training task diversity scaling: effect of varying
- **observed**: Increasing task diversity is beneficial. (up)  [metric: —]
- ⚠️ **field mismatch**: `intervention` holds ['E19'] (wrong category)

### F045  (primary_result, observed)
*from Section B.1 (S361)*
- **context**: RE-ARC dataset [22] in our offline training
- **intervention**: Using only the original ARC training data, without any RE-ARC data
- **observed**: our method achieves a decent accuracy  [metric: accuracy]

### F046  (primary_result, observed)
*from Section B.1 (S362)*
- **context**: RE-ARC dataset [22] in our offline training
- **intervention**: adding 10, 100, and 1,000 pairs per task from RE-ARC  vs reference: Using only the original ARC training data, without any RE-ARC data
- **observed**: increases (up)  [metric: accuracy]
- **↑ strengthens** [mechanism] Offline training learns visual common sense from the training set.

### F047  (primary_result, observed)
*from Section B.1 (S365)*
- **context**: —
- **intervention**: trained on 0, 16, 80, and 400 tasks
- **observed**: increases (up)  [metric: accuracy]
- **↑ strengthens** [mechanism] Offline training learns visual common sense from the training set.

### F048  (primary_result, observed)
*from Section B.2 (S372)*
- **context**: By default, the ARC protocol; multi-view inference with many views (510); On ARC-1
- **intervention**: as the number of proposals (k) increases
- **observed**: is (up)  [metric: pass@k accu-racy]

### F049  (primary_result, observed)
*from Section B.2 (S374)*
- **context**: By default, the ARC protocol; multi-view inference with many views (510); On ARC-1
- **observed**: this result reveals the upper-bound performance (66.3) of our method, even if oracle voting were applied.  [metric: pass@k accu-racy]
- **↑ strengthens** [mechanism] Majority voting consolidates multi-view predictions to improve accuracy.

### F050  (primary_result, observed)
*from Figure 19 (S399)*
- **context**: —
- **observed**: Ambiguous examples  [metric: —]

### F051  (primary_result, observed)
*from Figure 19 (S400)*
- **context**: three demonstration examples of a test task (top panel); a blue line "touching" (but not "going through") a red rectangle
- **observed**: some may admit multiple plausible explanations or rules  [metric: —]
- **↑ strengthens** [assumption] Some ARC tasks are ambiguous, admitting multiple plausible rules.

### F052  (primary_result, observed)
*from Figure 19 (S403)*
- **context**: inference example (bottom panel) involves this situation ("touching"); Task 09c534e7
- **intervention**: our model attempts to interpret the rule as either "going-through-only" (attempt 1) or "touching" (attempt 2)
- **observed**: Attempt 2 matches Ground Truth, Attempt 1 does not  [metric: Ground truth]
- **↑ strengthens** [assumption] Some ARC tasks are ambiguous, admitting multiple plausible rules.

### F053  (primary_result, observed)
*from Figure 17 (S385)*
- **context**: ARC-1
- **observed**: Successful and failed examples  [metric: —]
- **↑ strengthens** [mechanism] Visual learning directly enables abstraction and inference without language.

### F054  (primary_result, observed)
*from Figure 17 (S386)*
- **context**: ARC-1; test tasks
- **intervention**: solved by VARC
- **observed**: successfully solved  [metric: —]
- **↑ strengthens** [mechanism] Visual learning directly enables abstraction and inference without language.

### F055  (primary_result, observed)
*from Figure 17 (S387)*
- **context**: ARC-1; test tasks
- **intervention**: unsolved by VARC
- **observed**: unsolved  [metric: —]
- **↑ strengthens** [mechanism] Visual learning directly enables abstraction and inference without language.

### F056  (primary_result, observed)
*from Figure 17 (S391)*
- **context**: Task 15663ba9; Task 981571dc; Task 15696249; Task 67c52801; Inference input
- **intervention**: first and second solutions proposed by VARC
- **observed**: VARC's Attempt 1 matches the Ground Truth  [metric: correct output]

### F057  (primary_result, observed)
*from Figure 17 (S391)*
- **context**: Task 8dae5dfc; Task 67636eac; Task aa4ec2a5; Task b457fec5; Inference input
- **intervention**: first and second solutions proposed by VARC
- **observed**: VARC fails to solve the task  [metric: correct output]

### F058  (primary_result, observed)
*from Figure 18 (S392)*
- **context**: ARC-2
- **observed**: Successful and failed examples  [metric: —]
- **↑ strengthens** [mechanism] Visual learning directly enables abstraction and inference without language.

### F059  (primary_result, observed)
*from Figure 18 (S393)*
- **context**: ARC-2; test tasks
- **intervention**: solved by VARC
- **observed**: successfully solved  [metric: —]
- **↑ strengthens** [mechanism] Visual learning directly enables abstraction and inference without language.

### F060  (primary_result, observed)
*from Figure 18 (S394)*
- **context**: ARC-2; test tasks
- **intervention**: unsolved by VARC
- **observed**: unsolved  [metric: —]
- **↑ strengthens** [mechanism] Visual learning directly enables abstraction and inference without language.

### F061  (primary_result, observed)
*from Figure 18 (S398)*
- **context**: Task 800d221b; Task 7666fa5d; Task 221dfab4; Task 7b80bb43; Inference input
- **intervention**: first and second solutions proposed by VARC
- **observed**: VARC's Attempt 1 matches the Ground Truth  [metric: correct output]

### F062  (primary_result, observed)
*from Figure 18 (S398)*
- **context**: Task 2b83f449; Task 2d0172a1; Task 3e6067c3; Task 7ed72f31; Inference input
- **intervention**: first and second solutions proposed by VARC
- **observed**: VARC fails to solve the task  [metric: correct output]

### F063  (primary_result, observed)
*from Figure 20 (S411)*
- **context**: pixel-level attention maps; 4 test tasks in ARC eval; Task 09c534e7
- **observed**: task that was not correctly solved  [metric: correctly solved]
- **↑ strengthens** [mechanism] Different layers focus on distinct structures and task-specific patterns.

### F064  (primary_result, observed)
*from Figure 21 (S420)*
- **context**: layer-wise attention maps; demonstration examples (on the left) are provided for reference; Task 0607ce86; Task 0bb8deee; Task 1c56ad9f; Task 1d0a4b61
- **observed**: Attention patterns vary across layers  [metric: per-pixel softmax attention maps averaged across all pixels in that layer]
- **↑ strengthens** [mechanism] Different layers focus on distinct structures and task-specific patterns.

### F065  (primary_result, observed)
*from Figure 22 caption | Figure 22 'TTT process' panels (S423)*
- **context**: the grid augmented with a given scale ratio of 2×; the full canvas is not shown for brevity
- **intervention**: test-time training progresses
- **observed**: gradually converge toward the correct output (up)  [metric: model's predictions converge toward the correct output]
- **↑ strengthens** [mechanism] Test-time training refines color and spatial arrangement, adapting to tasks.

### F066  (primary_result, observed)
*from Figure 22 caption | Figure 22 'TTT process' panels (early stages) (S424)*
- **context**: In early epochs
- **intervention**: test-time training progresses
- **observed**: model produces coarse and imprecise structures  [metric: —]
- **↑ strengthens** [mechanism] Test-time training refines color and spatial arrangement, adapting to tasks.

### F067  (comparison, observed)
*from Figure 22 caption | Figure 22 'TTT process' panels (later stages) (S425)*
- **context**: in later epochs
- **intervention**: test-time training progresses  vs reference: In early epochs
- **observed**: model can improve the solutions (up)  [metric: —]
- **↑ strengthens** [mechanism] Test-time training refines color and spatial arrangement, adapting to tasks.