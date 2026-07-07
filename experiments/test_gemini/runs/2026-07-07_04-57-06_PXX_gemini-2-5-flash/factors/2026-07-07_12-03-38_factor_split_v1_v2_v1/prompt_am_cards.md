You are building **AM cards** — the "why the authors think so" layer of an AIO factor graph. These
are the mechanism and assumption nodes that measured observations will later vote on (strengthen /
weaken). This step does NOT touch observations; it only distills the belief-target nodes.

paper_id: PXX
paper_title_hint: unknown

You are given the paper (prose + figure/table descriptions) and ONLY the Layer-1 nodes that were
labeled `mechanism` or `assumption`. Use the paper to judge which are genuine and to merge
restatements.

--- PAPER: PROSE TRANSCRIPTION ---
===== pages 1-4 =====

ARC Is a Vision Problem!
Keya Hu Ali Cy
Runqian Wang
Linlu Qiu
Yeyin Eva Zhu
Xiaoman Delores Ding
Jacob Andreas
MIT
Kaiming He
Abstract
The Abstraction and Reasoning Corpus (ARC) is designed
to promote research on abstract reasoning, a fundamen-
tal aspect of human intelligence. Common approaches to
ARC treat it as a language-oriented problem, addressed by
large language models (LLMs) or recurrent reasoning mod-
els. However, although the puzzle-like tasks in ARC are in-
herently visual, existing research has rarely approached the
problem from a vision-centric perspective. In this work, we
formulate ARC within a vision paradigm, framing it as an
image-to-image translation problem. To incorporate visual
priors, we represent the inputs on a “canvas" that can be
processed like natural images. It is then natural for us to
apply standard vision architectures, such as a vanilla Vi-
sion Transformer (ViT), to perform image-to-image map-
ping. Our model is trained from scratch solely on ARC
data and generalizes to unseen tasks through test-time train-
ing. Our framework, termed Vision ARC (VARC), achieves
60.4% accuracy on the ARC-1 benchmark, substantially
outperforming existing methods that are also trained from
scratch. Our results are competitive with those of leading
LLMs and close the gap to average human performance.¹
1. Introduction
Learning and abstracting concepts from a small number of
demonstrations is a key feature of intelligence. The Ab-
straction and Reasoning Corpus (ARC) benchmark [12] was
designed to incentivize machine learning research aimed at
improving these capabilities. ARC consists of a collection
of puzzle-like tasks (Fig. 1, top), each containing only a
few examples governed by a unique underlying transfor-
mation rule. The model is expected to make predictions
on each unseen task given a few examples. While humans
are capable of solving various ARC tasks [25, 31, 32], the
benchmark remains highly challenging for today's leading
machine learning systems [44, 42].
The ARC problem has attracted significant attention, and
substantial progress has been made in recent years [13].
¹Project webpage: https://github.com/lillian039/VARC.
1
Training tasks
X
y
X
y
Test task
X
y
Xinfer
Xinfer
Yinfer
Xinfer
Yinfer
Xinfer
?
?
?
[TASK]
VARC network
model prediction
Figure 1. The ARC benchmark (top) consists of a collection of
many different tasks, where each task has a few (e.g., 2-4) exam-
ples. We propose the Vision ARC (VARC) framework, which ad-
dresses the ARC problem as an image-to-image translation prob-
lem, from a computer vision perspective (bottom). In this illus-
tration, the underlying concepts of the three tasks can be roughly
described by humans as: "reflection" (left), "symmetry" (middle),
and "gravity" (right). These concepts are closely related to the vi-
sual and physical world.
Among a wide variety of methods, those based on large
language models (LLMs) have proven highly competi-
tive. These methods generally convert ARC inputs into se-
quences of text tokens for language modeling. Representa-
tive methods may involve inductive reasoning [54, 7, 50, 6],
transductive reasoning [1, 19, 45], or a combination of both
[35, 8, 40]. The LLMs are pre-trained on internet-scale data,
from which they learn transferable common sense.
Most recently, research on recurrent models [53, 27]
has achieved impressive results on ARC without relying on
internet-scale data. These models are trained from scratch
on ARC data only and perform inference through recurrent,
iterative reasoning. Although they do not rely on large-scale
language pre-training, these recurrent models draw strong
inspiration from the success of language modeling.
Interestingly, although the ARC puzzles are typically
presented visually, existing research has rarely framed ARC
as a vision-centric problem. In fact, many concepts in ARC
ARC-1
ARC-2
X
y
X
y
X
y
Xinfer
model prediction
Xinfer
model prediction
Linfer
model prediction
TH
Figure 2. Examples of unseen tasks solved by VARC. Each
panel shows an unseen test task, with demonstrations on the top
and the model's prediction on the bottom. VARC correctly solves
these challenging tasks.
are inherently visual and physical: e.g., reflection, symme-
try, and gravity, as shown in Fig. 1. Humans can solve these
tasks not merely from the demonstrations, but by reason-
ing through analogy to their common sense obtained from
external experience. Such common sense can be acquired
through observing the world, particularly, the visual world.
Motivated by its visual nature, we approach ARC from
a vision-centric perspective. We frame each puzzle as an
image-to-image translation problem. Abstraction and infer-
ence can arise directly from visual learning, without explicit
linguistic intermediates. This perspective connects ARC to
classical image-to-image problems, ranging from low-level
image processing (e.g., [16, 43]) to high-level image under-
standing (e.g., [38, 46]). With this connection, we can ap-
ply standard vision models (e.g., Vision Transformers [17]
or convolutional networks [30]) to tackle the ARC problem.
We demonstrate that incorporating visual priors is cru-
cial. These priors include 2D spatial locality, translation
invariance, and scale invariance. To facilitate learning these
priors, we represent the inputs on a "canvas" with flexible
geometric transformations, allowing the inputs to be pro-
cessed as if they were natural images. A patch on the can-
vas can consist of exponentially many color combinations,
which helps reduce overfitting and encourages the model to
learn spatial priors rather than merely memorize.
With the vision-centric formulation, we train our model
from scratch using ARC-only data. At inference time, when
presented with a new, unseen task, we perform test-time
training [9, 24, 49, 1, 53, 27] to adapt the model to the task,
enabling it to generalize from only a few examples.
Our framework, termed Vision ARC (VARC), shows
strong performance on the ARC benchmarks (e.g., Fig. 2).
VARC achieves 54.5% accuracy on the ARC-1 benchmark,
using a small model with only 18 million parameters. This
result substantially surpasses the best recurrent methods
[53, 27] that are also trained from scratch on ARC. It is
also competitive with many popular LLM-based methods.
Combining VARC models through ensembling [29] further
improves accuracy to 60.4%, matching the reported average
human performance [31] on the ARC-1 dataset.
We hope our research will shed light on the ARC prob-
lem, and more broadly, on the field of abstract reasoning.
On the one hand, the design of the ARC benchmark is based
on human observations and induced rules abstracted from
the visual and physical world. It is natural to explore vision-
driven approaches for ARC. On the other hand, human rea-
soning is not confined to language or vision in isolation,
but instead should integrate information across modalities.
With our complementary vision-based perspective, we hope
the scope of abstract reasoning will be further broadened.
We invite the vision community to study the ARC problem
and to advance research on abstract reasoning.
2. Related Work
Visual reasoning. Visual reasoning is a long-standing re-
search problem. It involves not only perceiving scenes and
objects, but also inferring and abstracting the relations and
transformations among them. The advancement of ma-
chine learning methods has led to the development of a
variety of challenging protocols, such as VQA [5, 56, 20],
CLEVR [26], and Winoground [51].
The visual reasoning methods developed under these
protocols typically consist of a visual perception mod-
ule and a language-like recurrent module, e.g., within the
neuro-symbolic framework [4, 23, 3, 41]. These methods
have evolved into modern vision-language models (VLMs,
e.g., [2, 33, 37]), in which images are converted into tokens
and processed jointly with text.
Unlike ARC, classical visual reasoning protocols gener-
ally involve a training set and a test set, both of which can
be viewed as instances of the same task. In contrast, ARC
consists of a large collection of distinct tasks, each defined
by only a few examples.
Approaches to ARC. Owing to the "few-shot, many-task"
nature of ARC, LLMs have been regarded as a natural solu-
tion. A new task can be converted into a sequence of tokens,
treated as a prompt, and processed by LLMs via in-context
few-shot learning [55, 10]. We refer the reader to [13] for a
comprehensive survey.
Recently, recurrent models [53, 27] have been proven
effective for ARC, without the requirement of internet-scale
pre-training. These models aim to mimic the hierarchical
and multi-timescale processing of the human brain [53] for
reasoning. At inference time, these methods adopt test-time
training [9, 24, 49] on the few demonstration examples.
Related to our work, the ViT-ARC method [34] attempts
to address the ARC problem using vision models. How-
ever, this method has only shown the ability to fit individual
tasks in the training set; it is unable to generalize or solve
any unseen test task. As such, this method has not been
2
Training Set Ttrain
Ddemo
Task 1
Task 400
Test Set Ttest
Task 1
Task 400
y
Linfer
Xinfer
Dinfer
↓
?
?
Linfer
?
?
Figure 3. The ARC problem definition. ARC is a collection of
many different tasks. For each task, a few (e.g., 2-4) demonstration
pairs (x, y) are given, and the model is required to infer the output
from Xinfer. The training set Ttrain is a collection of 400 tasks, which
can be used for model training. The test set Ttest contains 400 new
tasks: the demo pairs of a new task are given only at inference
time, based on which the model performs inference on Xinfer.
able to satisfy the ARC protocol, whose essence lies pre-
cisely in few-shot, cross-task generalization. Unlike [34],
our framework is designed to address the "few-shot, many-
task" nature of ARC.
3. ARC as a Vision Problem
3.1. ARC Problem Definition
The ARC benchmark consists of several hundred very few-
shot (e.g., 2 to 4-shot) reasoning tasks. Each task, denoted
by T, involves a unique underlying transformation rule,
mapping from an input x to an output y. Here, x and y are
both 2D grids with maximum size 30×30, in which each
location has one of C different color indexes (e.g., C=10).
The ARC problem definition is illustrated in Fig. 3, which
we discuss next.
T
m
A task. A "task" is the basic unit in ARC. Each task in-
cludes a few demonstration examples. For a demonstration
pair (x, y), both x and y are known to the model. We denote
the demonstration set of task T as: Demo={(xi, Yi)}=1,
where m is the number of pairs (e.g., m is 2 to 4). Each
task T also contains a few inference examples, denoted as:
Dinfer={(xi, Yi)}=1 (n is 1 or 2). At inference time, only
the demo pairs Den emo and one input Xinfer ∈ Dinfer are given,
and the model is required to infer the desired output Yinfer.
Training set. The training set consists of multiple tasks
used to train the model offline (i.e., before a new task is
given). We denote the training set as: Train={T}=1, where
k is the number of tasks (400 in ARC-1). Following stan-
dard machine learning protocols, samples in Demo for any
T∈ Ttrain can be used for training. The "inference" samples
in the training set, that is, Dinfer for any task T∈ Ttrain, are
used for validating the training process only.
Test set. The test set is a collection of new tasks, which are
not seen during offline training. We denote the test set as:
Ttest={T}=1, with l different test tasks. Note that any test
task is a "complete" and new task: that is, for any T∈ Ttest,
demo'
there also exists a demo set DT. and the pairs (x, y) in
Demo are given to the model at inference time. The model
should make use of DT. demo to infer the output of the given
Xinfer for this new task.
The presence of new (x, y) pairs in Demo at inference
time allows to perform test-time training [49, 1, 9, 24],
which we adopt and will discuss.
3.2. Image-to-Image Translation
With these definitions, we formulate reasoning on each task
as an image-to-image translation problem. We frame the
problem as per-pixel classification, analogous to the seman-
tic segmentation problem [38].
Formally, we learn a neural network fe parameterized by
0. The network fe takes an image xi as input, conditioned
on a task token associated with the task T. The task token
is represented as a learnable embedding dependent on T.
The output of fe is a grid where each position represents
a categorical distribution. The overall objective function is
simply the per-pixel cross-entropy loss [38]:
L(0) = ET,i [D(yi, fo(xi | T))].
(1)
Here, D denotes the per-pixel cross-entropy loss between
the ground-truth yi and the network output.
3.3. Visual Modeling
Previous methods on ARC generally operate in the space of
discrete-valued tokens, motivated by the design of language
models. In our formulation of image-to-image translation,
we explore native designs developed for vision.
Canvas. While it is straightforward to view the raw H×W
grid as an H×W image, we propose more flexible transfor-
mations to represent it in a manner similar to natural images.
We define the concept of a "canvas". A canvas has a
predefined and sufficiently large size, e.g., 64×64. The raw
input is transformed and placed onto this canvas. This for-
mulation naturally accommodates translation and scale aug-
mentations, which are common strategies for introducing
translation and scale invariance in vision, discussed next.
We set the background of the canvas to an additional back-
ground color, i.e., the (C+1)-th color.
When applying a ViT model (discussed next), if we
naïvely treat each raw pixel as a token, there would be only
C distinct tokens. In contrast, our canvas formulation sup-
ports a much larger set of local, patch-level configurations.
For example, with a patch size of 2×2 (see Fig. 5), a single
patch can contain multiple colors and, in principle, has an
exponentially large cardinality, O(C2×2). This formulation
is important for improving generalization performance.
Translation and scale invariance. The “canvas" concept
enables us to flexibly apply translation and scale augmen-
tations, which are critical in standard vision models. The-
3
Scale
Translation
[task]
Figure 4. The raw input undergoes random scale and translation
transformations and is placed on the "canvas" (denoted in gray).
ses data augmentations encourage the model to learn un-
derlying mappings invariant to geometric transformations
grounded in the visual world. Formally, we perform:
place on canvas
patch embedding
Transformer block
• Scale augmentation: Given a raw input, we randomly
resize it by an integer scaling ratio s, duplicating each
raw pixel into sxs (see Fig. 4, left). This is analo-
gous to nearest-neighbor interpolation in natural im-
ages. However, note that “colors” in ARC do not cor-
respond to real-world colors, so it is not meaningful to
perform other interpolations (such as bilinear).
• Translation augmentation: given the scaled grid, we
randomly place it on the fixed-size canvas. We ensure
all pixels are visibile. See Fig. 4 (right).
We empirically show that these visual priors are important
for generalization to unseen tasks.
Vision Transformer. Given a canvas with an input ran-
domly placed, we perform image-to-image translation by a
standard vision model. By default, we use a ViT [17].
The principle of ViT is Transformer on patches. For-
mally, the input canvas is divided into non-overlapping
patches (e.g., 2×2), projected by a linear embedding, added
with positional embedding [52], and processed by a stack
of Transformer blocks [52]. The model has a linear projec-
tion layer as the output, which performs per-pixel classifica-
tion for each patch. Note that unlike natural images where
each raw pixel has continuous values, in our case, the raw
pixels have discrete values. Therefore, before patchifica-
tion, we first map each pixel's discrete index into a learnable
continuous-valued embedding.
Conceptually, patchification can be viewed as a special
form of convolution. Like convolution, it incorporates sev-
eral critical inductive biases in vision: most notably, local-
ity (i.e., grouping nearby pixels) and translation invariance
(i.e., weight sharing across locations).
2D positional embedding. Unlike language data, which is
generally modeled as 1D sequences, images are inherently
2D. This 2D structure can be lost if we naïvely treat the
embedded patches as a 1D sequence. We empirically show
that explicitly modeling positions in 2D is essential.
Formally, we adopt separable 2D positional embed-
dings, following [11]: with D channels for positional em-
beddings, we use the first half of the channels to embed
the horizontal coordinate and the second half to embed the
off canvas
Transformer block
predictor
Figure 5. The ViT architecture in VARC. The input is randomly
placed on a canvas, which is then treated as a natural image and
processed by a standard ViT, conditioned on the task token.
vertical coordinate. This can be applied both to additive po-
sitional embeddings for encoding absolute positions and to
the encoding of relative positions (e.g., RoPE [48]).
Alternative: convolutional networks. Beyond ViT, we
also study the more classical vision-based architecture, i.e.,
convolutional neural networks [30]. Specifically, we adopt
the U-Net model [46], a hierarchical convolutional network.
The original U-Net was proposed precisely for the image-
to-image translation problem of segmentation [46], making
it a natural candidate for the problem we consider.
3.4. Two-stage Training
We adopt a two-stage training paradigm to learn the param-
eters of the neural network.
demo
Offline training. This stage is applied on the entire train-
ing set Train. It is on all demos DTmo for any T∈ Ttrain.
We train one model fe jointly for all k training tasks (e.g.,
k=400), based on the loss in Eq. (1). All tasks share the
same parameters, only except that each task has its own
task-conditional token. We do not use the inference set
Pinfer from the training tasks (i.e., T∈ Ttrain) to train the
model. These sets are used only for validation purposes.
DT
4

===== pages 5-8 =====

nearly free to use many views. We use 510 random views
(details are in appendix). Predictions from different views
are consolidated by majority voting [1].
prediction
Pass@2 accuracy. The ARC benchmark by default adopts
the pass@2 accuracy metric: i.e., two different solutions
can be produced for evaluation, and a task is considered
correct if one is correct. To support this metric, we adopt
majority voting in multi-view inference and retain the top-2
most populated output solutions.

4. Implementation Details
We describe the major implementation choices in this sec-
tion. The configuration details can be found in appendix.
Figure 6. Effect of test-time training. (Top): Demonstration ex-
amples for the current task. (Bottom left): An inference example
Xinfer. (Bottom right): During test-time training, the prediction
from Xinfer becomes progressively more accurate, with the model
finally generating the correct prediction.

Test-time training (TTT). Given a single new, unseen
task T∈ Ttest from the test set, we perform inference
by test-time training. At inference time, we are given
Demo={(xi, Yi)}=1 with both input and output accessi-
ble; the model is required to make prediction for a given
Xinfer in this new task T. The test-time training fol-
lowed by inference can be viewed abstractly as a function
F(Xinfer | Demo)→ Yinfer.
We perform test-time training for each new task T inde-
pendently. It has a new task token whose parameters are
randomly initialized. As there are very few demo pairs in
Demo (e.g., 2 to 4), we also perform data augmentation. We
elaborate on the details in the next section and in appendix.
In summary, at inference time, the model is initialized
from offline training, fine-tuned with test-time training only
for the single new task T, and then performs inference on
Xinfer. As the new demo pairs in Demo are very few, even
with data augmentation, this test-time training process re-
mains reasonably fast (e.g., 70 seconds per task on a single
GPU). Fig. 6 visualizes the effect of test-time training.

3.5. Inference
After test-time training, we apply fe to Xinfer to obtain the
final prediction. This process is analogous to the classical
recognition problems [29, 38]. Accordingly, we adopt post-
processing strategies inspired by recognition methods.
Single-view inference. Given Xinfer and a single "view"
(i.e., with a given scale and translation), we place Xinfer on
the canvas and apply fe to predict the output. Since one
output location in the raw grid may be predicted by multi-
ple pixels on the canvas (e.g., due to rescaling; see Fig. 5),
we aggregate all predictions (from softmax outputs) at this
location by average pooling.
Multi-view inference. It was a common practice to consol-
idate the predictions from multiple views (e.g., see AlexNet
[29]). Analogously, we adopt multi-view inference to im-
prove accuracy, where the views are sampled with different
augmentations. As the multi-view inference cost is negli-
gible compared with test-time training cost, it is virtually
Canvas. In our best-performing model, the canvas size is
64×64. In the case of ViT, the patch size is 2×2, resulting
in a sequence length of 322. For scale augmentation, an in-
teger scaling ratio is randomly sampled, such that the scaled
grid is no larger than the canvas size. For translation aug-
mentation, the upper-left corner is randomly sampled under
the constraint that the placed image is fully visible.
Offline training. We use the standard ARC-1 training set
Ttrain for training: it has 400 tasks with 2-4 demo pairs each.
Following common practice on ARC, we also expand our
training set with the RE-ARC set [22], from which we sam-
ple 1,000 additional demo pairs per task. Put together, our
full training set has about 400k sample pairs. We apply
translation and scale augmentation in offline training.
Test-time training. Given an unseen task T∈ Ttest, we
have 2-4 sample pairs in Demo. To make test-time training
more feasible, we also augment the single task T into mul-
tiple auxiliary tasks. We do this by using standard augmen-
tation from existing ARC methods: flip, rotation (by 90°,
180°, or 270°), and color permutation. We treat each of
these test-time training augmentations as an auxiliary task,
each assigned a task embedding. We also apply translation
and scale augmentation in test-time training, but we do not
view them as a new auxiliary task (under the assumption
that all auxiliary tasks are translation and scale invariant).

5. Experimental Results
Our experiments are primarily conducted on the benchmark
of ARC-1 [12]. We report the pass@2 accuracy (referred
to simply as "accuracy” hereafter) in percentage (%). To
support pass@2 evaluation, we adopt multi-view inference.
We also report final results on ARC-2 [14].
We evaluate our model on the ARC-1 evaluation set (i.e.,
Teval). This set is conceptually a test set (see Fig. 3), but with
ground truth available only for computing accuracy.

2In majority voting, two output grids are considered "consistent” only
when they are identical across the entire grid. The winner is the grid that
is "consistent" with the largest number of other output grids.
5
(a) naïve baseline
26.8
(b) w/ 2D absolute pos embed
(c) w/ 2D ROPE
(d) 1x1 patch on 32x32 → 2x2 patch on 64x64
32.8
43.0
45.4
model width
depth #params Gflops acc.
384
5
6M
10
44.4
ViT
512
10
18M
28 54.5
768
20
66M
99 53.0
setting (a)
7M
18 42.8
U-Net
setting (b)
17M
33 47.5
setting (c)
55M
87 48.3
(e) w/ translation aug. on canvas
(f) w/ scale aug. on canvas
0
10
20
30
40
48.3
54.5
50
(%)
Figure 7. Effects of visual priors in VARC. Accuracy is reported
on the ARC-1 evaluation set. The model used is ViT-18M. En-
tries (a-c) use a patch size of 1×1 on a 32×32 canvas, whereas
entries (d-f) use a patch size of 2×2 on a 64×64 canvas. Each
entry modifies the one above it. We start from a naïve baseline
with components (b-f) removed. These vision priors cumulatively
yield 27.7 improvement (a→f), in which the canvas-based designs
(cf) contribute an 11.5 gain.
Table 1. Vision backbones. We compare variants of ViTs and U-
Nets of similar sizes. U-Net settings are in appendix.
Accuracy (%)
601
• Depth = 5
• Depth = 10
55
50-
Accuracy (%
80-
w/ offline training
70-
wo/ offline training
60-
54.5
54.5
50-
18M
44.8
51.6
12M
40
45
47.0
47.0
30
29.1
26.4
6M
10M
44.4
6M
20-
40- 41.0
3M
10
0
35
256
384
512
TTT jointly
TTT independently
5.1. Visual Priors
Fig. 7 summarizes the effects of visual priors, starting from
a baseline (a) without the other components in this figure.
These priors jointly have a gain of 27.7 points, where the
canvas-based designs (cf) has a gain of 11.5 points. We
discuss these components as follows.
2D positional embedding. Extending from 1D posi-
tional embedding to its 2D counterpart is beneficial: see
Fig. 7(b)(c). This is observed in both (b) absolute and (c)
relative positional embeddings.
To demonstrate this effect on a stronger baseline, we re-
place the 2D ROPE in Fig. 7(f) with a 1D ROPE and observe
a degradation of 3.5 points, from 54.5 to 51.0.
Patchification. A key design principle of our method is
to prepare the input as a natural image. This enables the
expansion of the token set from a very limited size (e.g., 10)
to an exponentially large number. The entries Fig. 7(d-f) all
benefit from this design.
In Fig. 7(d), we advance from 1×1 patches on a 32×32
canvas to 2×2 patches on a 64×64 canvas. Doing so does
not increase the computational cost of the Transformer. In
this ablation (d), the scaling ratio is fixed as 2x. As such,
if we constrain each 2×2 patch to cover only one raw pixel,
it becomes equivalent to the 1×1 patch counterpart on the
32×32 canvas. Therefore, to ensure a meaningful compar-
ison, we do not impose this constraint, allowing each 2×2
patch to cover multiple colors. This can be interpreted as
one-pixel translation augmentation on the canvas.
Even so, the 2×2 patchification leads to a noticeable gain
of 2.4 points, improving from 43.0 to 45.4; see Fig. 7(c,d).
In spite of the small one-pixel augmentation, each patch can
cover multiple colors (as in natural images), which substan-
tially enriches the data space for learning.
Figure 8. Scalability: ViTs
with different width (x-axis)
and depth. The circle areas de-
note model sizes.
Figure 9. TTT strategies:
with vs. without offline train-
ing, and joint vs. independent
for each task.
Translation and scale augmentation. In image recogni-
tion, even highly capable network architectures still benefit
greatly from translation and scale augmentations. We draw
similar observations in ARC. See Fig. 7(e,f).
In Fig. 7(e), we apply fully flexible translation augmen-
tation on the canvas. Compared with the "one-pixel" aug-
mentation in Fig. 7(d), this setting yields an additional gain
of 2.9 points (from 45.4 to 48.3). In Fig. 7(f), we further ap-
ply the scale augmentation enabled by the concept of can-
vas. Scale augmentation yields a substantial gain of 6.2
points. Unlike translation invariance, which can be partially
addressed by patchification (i.e., a special form of convo-
lution), the ViT architecture has little to no inductive bias
about scale invariance. This can explain why scale augmen-
tation yields a substantial gain.

5.2. Other Ablation Experiments
ViT vs. U-Net. In Tab. 1, we compare ViT with U-Nets,
a type of convolutional network. We evaluate three model
sizes for each architecture. Although ViTs consistently per-
form better, all U-Net variants achieve decent accuracy, sug-
gesting that this problem can also be effectively addressed
by classical vision backbones.
Scalability. In Fig. 8, we show ViTs with varying depths
and widths. In this regime, our method demonstrates good
scalability: increasing depth and/or width leads to higher
accuracy as a result of better fitting. Going beyond this
6

single-view, pass@1 multi-view, pass@1 multi-view, pass@2
35.9
49.8
54.5
Table 2. Single-view vs. multi-view inference.

regime can lead to overfitting in our current setting, as
shown in Tab. 1 for the 66M ViT model. We observe that
this larger model achieves higher training accuracy, sug-
gesting that future research should focus on generalization.
Test-time training (TTT) strategies. In Fig. 9(b), we study
TTT with and without offline training, and TTT performed
jointly on all test tasks vs. independently for each test task.
As expected, offline training greatly improves the per-
formance of TTT, suggesting that common sense about the
visual world can be learned from the training set. We also
note that even without offline training, our TTT strategy
can achieve nontrivial accuracy (26.4), suggesting that some
tasks in this benchmark can be solved tabula rasa. This re-
sult outperforms that in [36] under a similar setting.
Surprisingly, performing TTT independently for each
test task yields substantially better performance (by ~10
points) than doing so jointly across all test tasks, even
though the latter relies on a stronger assumption about the
availability of multiple test tasks at once. We hypothesize
that overtraining on the test tasks may cause the model to
forget the knowledge acquired during offline training.
Single-view vs. multi-view inference. As discussed in
Sec. 3.5, we adopt multi-view inference by default. For
completeness, we also examine the single-view inference
accuracy. Since single-view inference cannot produce mul-
tiple predictions, we compare pass@1 accuracy. See Tab. 2.
Single-view inference has a decent pass@1 accuracy of
35.9; multi-view inference further boosts to 49.8, thanks to
majority voting. Unlike typical computer vision applica-
tions such as semantic segmentation, in ARC, a mistake on
even a single pixel renders the entire prediction incorrect.
This may explain the large gain seen here.

5.3. System-level Comparisons
In Tab. 3 we compare with leading results using LLMs or
recurrent models, on ARC-1 and ARC-2.4
Our model compares favorably with some of the most
powerful LLMs at the time their results were reported: in-
cluding Deepseek, Claude, o3, and GPT-5 (we note that
given the rapid progress of LLMs, these models may have
stronger results by the time our paper is public). LLMs are
pre-trained on internet-scale data, and some may also incor-
porate multimodal data that include images. Our method
does not rely on such data and uses a model that is several

3In general, it cannot be assumed that multiple unseen tasks will be
presented all at once.

system
#params ARC-1 ARC-2
large language models (LLMs)
Deepseek R1 [21]
671B
15.8
1.3
Claude 3.7 8k [18]
N/A
21.2
0.9
o3-mini-high [18]
N/A
34.5
3.0
GPT-5 [18]
N/A
44.0
1.9
Grok-4-thinking [18]
1.7T
66.7
16.0
Bespoke (Grok-4) [8]
1.7T
79.6
29.4
recurrent models
HRM [53]
27M
40.3
5.0
TRM [27]
7M
44.6
7.8
vision models
VARC
18M
54.5
8.3
VARC (ensemble)
73M
60.4
11.1
human results
avg. human [31]
60.2
best human [18]
98.0
100.0
Table 3. System-level comparisons on the ARC-1 and ARC-2
benchmarks. LLM-based results are from the ARC-AGI leader-
board [18]. HRM, TRM, and our VARC are trained from scratch
only on ARC data. Our single-model result is based on ViT, with
mean±std of 54.5±0.7 (ARC-1) and 8.3±0.4 (ARC-2) over four
runs. Our ensemble result aggregates an 18M ViT and a 55M
U-Net, each with test-time training performed four times.

orders of magnitude smaller.
In the controlled setting of training from scratch on
ARC data, our method substantially outperforms the recur-
rent models: HRM [53] and TRM [27]. Our VARC with
18M parameters is ~10 points better than TRM on ARC-1,
a >20% relative improvement. Note that, once test-time
training is completed, our model performs fully feedfor-
ward inference, with no recurrence involved in reasoning.
Following the classical ensembling practice in vision
(e.g., AlexNet [29]), we ensemble one ViT and one U-Net,
each with test-time training run four times. Doing so boosts
our result to 60.4. This result closes the gap with the re-
ported average human performance (60.2 [31]).

6. Visualization and Analysis
Beyond numerical metrics, we provide additional qualita-
tive results that help reveal the model's behavior. We refer
readers to the appendix for more visualizations.
Attention patterns. Fig. 10 shows the attention patterns of
our ViT model in a test task. These attention maps show
that our model can correctly reason about the relationship
between a source pixel and its target pixel to copy from.
Figure 11 visualizes the layer-wise attention maps for an-
other test task. A layer-wise map is the softmax attention
map averaged across all pixels in the layer: it reveals which
pixels receive the most attention in that layer. In this task,

4Our ARC-2 models are trained only on the ARC-1 dataset, with test-
time training and inference on the ARC-2 set.

7

Ddemo
Xinfer
model prediction
Ddemo
Xinfer
model prediction
one pixel, different layers
-1
+1
Layer 0
Layer 1
Layer 2
Layer 3
Layer 4
1.0
layer 3
layer 4
layer 8
one layer, different pixels
layer 8
layer 8
layer 8
Layer 5
Layer 6
Layer 7
Layer 8
Layer 9
0.2
0.0
Figure 10. Visualization of pixel-to-pixel attention. (Top): a
test task from ARC-1 eval: showing demo pairs, inference input,
and model prediction. (Middle): attention maps for a single pixel
across different layers. With the highlighted pixel as query, we
show pre-softmax logits. Different layers exhibit different behav-
ior. (Bottom): attention maps in layer 8 with other query pixels.
All of them correctly attend to their corresponding palette pixel.

different layers exhibit different specialties: some layers at-
tend to the pixels that are to be copied, and some layers
attend to the target lines alone the eight directions.
t-SNE of task embeddings. Our model is conditioned on
a task token, with an embedding learned to represent each
task. With 400 training tasks in ARC-1, our model learns
400 distinct task embeddings in offline training. We visu-
alize these 400 embeddings in the 2D space by t-SNE [39]
(see Fig. 12). Each point corresponds to a task..
Interestingly, we observe that nearby points in the task
embedding space exhibit similar semantics. For example,
the top-left corner in Fig. 12 shows two tasks related to
coloring; the bottom-left corner shows two tasks related to
generalized logic operations (i.e., AND/OR/XOR). This vi-
sualization suggests that our method attempts to learn the
relations between different tasks, which is an essential abil-
ity for abstraction and reasoning.

7. Conclusion
Our work explores a previously overlooked perspective in
the ARC task by framing it as an image-to-image translation
problem. It naturally enables the adaptation of visual frame-
works and yields strong few-shot generalization competi-
tive with recent approaches, while remaining orders of mag-
nitude smaller than most LLM-based models. This opens up
a new possibility of treating ARC as a vision-centric prob-

Figure 11. Visualization of layer-wise attention maps. For each
layer, we compute pixel-to-pixel attention and then average the
softmax maps across all pixels to obtain a single map per layer.
This map reveals which pixels are most attended in this layer. We
show a test task from ARC-1 eval. In this task, some layers exhibit
strong attention to the 3 × 3 neighborhood, reflecting the influence
of the pattern's core. In comparison, some other layers (e.g., layers
7-9) focus on the outward-radiating rays, corresponding to the rule
that extends colored pixels along the eight directions.

"Use the blue layout in the
blue box as the blueprint,
fill its four regions with the
four corner colors"

"Use the green layout in the
blue box as the blueprint,
fill its four regions with the
small square of four colors."

"If a cell is black in both "If a cell is black in both
input grids, make it green. input grids, make it green.
Otherwise leave it black." Otherwise leave it black."

"Copy the small colored
pattern center to the gray
pixel."

+H

"Copy the small colored
pattern center to the blue
pixel."

"Expand the red pixel vertically
with blue pixels, and expand
pattern in four dimensions."

"Expand the gray pixel diagonally
with blue pixels, and expand
pattern in four dimensions."

Figure 12. t-SNE of task embeddings, on the 400 task tokens
learned from the ARC-1 training set. Each point represents a sin-
gle task. To aid the reader, we provide human-written descriptions
for the tasks (which are not used in any form by our method).

lem, emphasizing abstraction and reasoning emerging di-
rectly from image pixels.
We hope this work will encourage the community to
leverage ARC not only as a symbolic reasoning problem,
but also as a testbed for promoting the generalization ca-
pacity of visual methods. Future research may extend this
direction through more expressive architectures, richer vi-
sual priors, or larger-scale image pre-training. We envision
that vision-centric reasoning will play a key role in build-
ing AI systems capable of learning and applying abstract
concepts in a human-like manner.

8

===== pages 9-12 =====

References
[1] Ekin Akyürek, Mehul Damani, Adam Zweiger, Linlu Qiu,
Han Guo, Jyothish Pari, Yoon Kim, and Jacob Andreas.
The surprising effectiveness of test-time training for few-shot
learning. In ICML, 2025.
[2] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine
Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Men-
sch, Katherine Millican, Malcolm Reynolds, Roman Ring,
Eliza Rutherford, Serkan Cabi, Tengda Han, Zhitao Gong,
Sina Samangooei, Marianne Monteiro, Jacob L. Menick,
Sebastian Borgeaud, Andy Brock, Aida Nematzadeh, Sa-
hand Sharifzadeh, Mikolaj Binkowski, Ricardo Barreira,
Oriol Vinyals, Andrew Zisserman, and Karén Simonyan.
Flamingo: a visual language model for few-shot learning.
In NeurIPS, 2022.
[3] Jacob Andreas, Marcus Rohrbach, Trevor Darrell, and Dan
Klein. Learning to compose neural networks for question
answering. In ACL, 2016.
[4] Jacob Andreas, Marcus Rohrbach, Trevor Darrell, and Dan
Klein. Neural module networks. In CVPR, 2016.
[5] Stanislaw Antol, Aishwarya Agrawal, Jiasen Lu, Margaret
Mitchell, Dhruv Batra, C. Lawrence Zitnick, and Devi
Parikh. VQA: visual question answering. In ICCV, 2015.
[6] Jeremy Berman. How I came in first on ARC-AGI-Pub using
Sonnet 3.5 with evolutionary test-time compute. Substack,
2024. Accessed: 2025-10-13.
[7] Jeremy Berman. How I got a record 53.6% on ARC-AGI.
Substack, 2024. Accessed: 2025-10-13.
[8] Jeremy Berman. How I got the highest score on ARC-AGI
again swapping Python for English. Substack, 2025.
[9] Léon Bottou and Vladimir Vapnik. Local learning algo-
rithms. Neural Computation, 1992.
[10] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Sub-
biah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakan-
tan, Pranav Shyam, Girish Sastry, Amanda Askell, Sand-
hini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom
Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler,
Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen,
Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess,
Jack Clark, Christopher Berner, Sam McCandlish, Alec Rad-
ford, Ilya Sutskever, and Dario Amodei. Language models
are few-shot learners. In NeurIPS, 2020.
[11] Xinlei Chen, Saining Xie, and Kaiming He. An empiri-
cal study of training self-supervised vision transformers. In
ICCV, 2021.
[12] François Chollet. On the measure of intelligence.
arXiv:1911.01547, 2019.
[13] Francois Chollet, Mike Knoop, Gregory Kamradt, and
Bryan Landers. ARC Prize 2024: Technical report.
arXiv:2412.04604, 2024.
[14] Francois Chollet, Mike Knoop, Gregory Kamradt, Bryan
Landers, and Henry Pinkard. ARC-AGI-2: A new challenge
for frontier Al reasoning systems. arXiv:2505.11831, 2025.
[15] Prafulla Dhariwal and Alexander Quinn Nichol. Diffusion
models beat GANs on image synthesis. In NeurIPS, 2021.
[16] Chao Dong, Chen Change Loy, Kaiming He, and Xiaoou
Tang. Image super-resolution using deep convolutional net-
works. IEEE Transactions on Pattern Analysis and Machine
Intelligence, 2015.
[17] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov,
Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner,
Mostafa Dehghani, Matthias Minderer, Georg Heigold, Syl-
vain Gelly, Jakob Uszkoreit, and Neil Houlsby. An image is
worth 16x16 words: Transformers for image recognition at
scale. In ICLR, 2021.
[18] ARC Prize Foundation. ARC-AGI benchmarking: Leader-
board and dataset for the ARC-AGI benchmark. https:
//arcprize.org/leaderboard, 2025. Accessed:
2025-11-01.
[19] Daniel Franzen, Jan Disselhoff, and David Hartmann. Prod-
uct of experts with LLMs: Boosting performance on ARC is
a matter of perspective. arXiv:2505.07859, 2025.
[20] Yash Goyal, Tejas Khot, Douglas Summers-Stay, Dhruv Ba-
tra, and Devi Parikh. Making the V in VQA matter: El-
evating the role of image understanding in visual question
answering. In CVPR, 2017.
[21] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song,
Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi
Wang, Xiao Bi, et al. Deepseek-R1: Incentivizing rea-
soning capability in LLMs via reinforcement learning.
arXiv:2501.12948, 2025.
[22] Michael Hodel. Addressing the abstraction and rea-
soning corpus via procedural example generation.
arXiv:2404.07353, 2024.
[23] Ronghang Hu, Jacob Andreas, Marcus Rohrbach, Trevor
Darrell, and Kate Saenko. Learning to reason: End-to-end
module networks for visual question answering. In ICCV,
2017.
[24] Thorsten Joachims. Transductive inference for text classifi-
cation using support vector machines. In ICML, 1999.
[25] Aysja Johnson, Wai Keen Vong, Brenden M. Lake, and
Todd M. Gureckis. Fast and flexible: Human program induc-
tion in abstract reasoning tasks. arXiv:2103.05823, 2021.
[26] Justin Johnson, Bharath Hariharan, Laurens van der Maaten,
Li Fei-Fei, C. Lawrence Zitnick, and Ross B. Girshick.
CLEVR: A diagnostic dataset for compositional language
and elementary visual reasoning. In CVPR, 2017.
[27] Alexia Jolicoeur-Martineau. Less is more: Recursive reason-
ing with tiny networks. arXiv:2510.04871, 2025.
[28] Diederik P Kingma and Jimmy Ba. Adam: A method for
stochastic optimization. In ICLR, 2015.
[29] Alex Krizhevsky, Ilya Sutskever, and Geoffrey E. Hinton.
ImageNet classification with deep convolutional neural net-
works. In NeurIPS, 2012.
[30] Y. LeCun, B. Boser, J. S. Denker, D. Henderson, R. E.
Howard, W. Hubbard, and L. D. Jackel. Backpropagation
applied to handwritten zip code recognition. Neural Compu-
tation, 1989.
[31] Solim LeGris, Wai Keen Vong, Brenden M. Lake, and
Todd M. Gureckis. H-ARC: A robust estimate of human
performance on the abstraction and reasoning corpus bench-
mark. arXiv:2409.01374, 2024.
[32] Solim LeGris, Wai Keen Vong, Brenden M. Lake, and
Todd M. Gureckis. A comprehensive behavioral dataset for
the abstraction and reasoning corpus. Scientific Data, 2025.
9
[33] Junnan Li, Dongxu Li, Caiming Xiong, and Steven C. H.
Hoi. BLIP: bootstrapping language-image pre-training for
unified vision-language understanding and generation. In
ICML, 2022.
[34] Wenhao Li, Yudong Xu, Scott Sanner, and Elias Boutros
Khalil. Tackling the abstraction and reasoning corpus with
vision transformers: the importance of 2D representation,
positions, and objects. arXiv:2410.06405, 2024.
[35] Wen-Ding Li, Keya Hu, Carter Larsen, Yuqing Wu, Simon
Alford, Caleb Woo, Spencer M. Dunn, Hao Tang, Wei-Long
Zheng, Yewen Pu, and Kevin Ellis. Combining induction and
transduction for abstract reasoning. In ICLR, 2025.
[36] Isaac Liao and Albert Gu. ARC-AGI without pretrain-
ing.
https://iliao2345.github.io/blog_
posts/arc_agi_without_pretraining/arc_
agi_without_pretraining.html, 2025.
[37] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee.
Visual instruction tuning. NeurIPS, 2023.
[38] Jonathan Long, Evan Shelhamer, and Trevor Darrell. Fully
convolutional networks for semantic segmentation. In
CVPR, 2015.
[39] Laurens van der Maaten and Geoffrey Hinton. Visualizing
data using t-SNE. Journal of machine learning research,
2008.
[40] Matthew V Macfarlane and Clément Bonnet. Searching la-
tent program spaces. arXiv:2411.08706, 2024.
[41] Jiayuan Mao, Chuang Gan, Pushmeet Kohli, Joshua B.
Tenenbaum, and Jiajun Wu. The neuro-symbolic concept
learner: Interpreting scenes, words, and sentences from nat-
ural supervision. In ICLR, 2019.
[42] Arseny Moskvichev, Victor Vikram Odouard, and Melanie
Mitchell. The ConceptARC benchmark: Evaluating
understanding and generalization in the ARC domain.
arXiv:2305.07141, 2023.
[43] Deepak Pathak, Philipp Krähenbühl, Jeff Donahue, Trevor
Darrell, and Alexei A. Efros. Context encoders: Feature
learning by inpainting. In CVPR, 2016.
[44] Rolf Pfister and Hansueli Jud. Understanding and bench-
marking artificial intelligence: OpenAI's o3 is not AGI.
arXiv:2501.07458, 2025.
[45] Jean-Francois Puget. A 2D nGPT model for ARC Prize.
2024.
[46] Olaf Ronneberger, Philipp Fischer, and Thomas Brox. U-
net: Convolutional networks for biomedical image segmen-
tation. In International Conference on Medical image com-
puting and computer-assisted intervention. Springer, 2015.
[47] Yang Song and Stefano Ermon. Generative modeling by es-
timating gradients of the data distribution. In NeurIPS, 2019.
[48] Jianlin Su, Murtadha Ahmed, Yu Lu, Shengfeng Pan, Wen
Bo, and Yunfeng Liu. Roformer: Enhanced transformer with
rotary position embedding. Neurocomputing, 2024.
[49] Yu Sun, Xiaolong Wang, Zhuang Liu, John Miller, Alexei A.
Efros, and Moritz Hardt. Test-time training with self-
supervision for generalization under distribution shifts. In
ICML, 2020.
[50] Hao Tang, Keya Hu, Jin Zhou, Sicheng Zhong, Wei-Long
Zheng, Xujie Si, and Kevin Ellis. Code repair with LLMs
gives an exploration-exploitation tradeoff. In NeurIPS, 2024.
[51] Tristan Thrush, Ryan Jiang, Max Bartolo, Amanpreet
Singh, Adina Williams, Douwe Kiela, and Candace Ross.
Winoground: Probing vision and language models for visio-
linguistic compositionality. In CVPR, 2022.
[52] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszko-
reit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia
Polosukhin. Attention is all you need. In NeurIPS, 2017.
[53] Guan Wang, Jin Li, Yuhao Sun, Xing Chen, Changling Liu,
Yue Wu, Meng Lu, Sen Song, and Yasin Abbasi Yadkori.
Hierarchical reasoning model. arXiv:2506.21734, 2025.
[54] Ruocheng Wang, Eric Zelikman, Gabriel Poesia, Yewen Pu,
Nick Haber, and Noah D. Goodman. Hypothesis search: In-
ductive reasoning with language models. In ICLR, 2024.
[55] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le, and
Denny Zhou. Chain-of-thought prompting elicits reasoning
in large language models. In NeurIPS, 2022.
[56] Peng Zhang, Yash Goyal, Douglas Summers-Stay, Dhruv
Batra, and Devi Parikh. Yin and yang: Balancing and an-
swering binary visual questions. In CVPR, 2016.
10
offline training
epochs
warmup epochs
optimizer
batch size
learning rate
learning rate scheduler
weight decay
dropout
100
10
Adam [28], betas=(0.9, 0.999)
32
3e-4
cosine
0
0.1
test-time training
epochs
warmup epochs
optimizer
batch size
learning rate
learning rate scheduler
weight decay
dropout
100
10
Adam [28], betas=(0.9, 0.999)
8
3e-4
cosine
0
0.1
Table 4. Configurations.

offline training
GPU type
GPU number
GPU time
H100
8
4.8 hours
test-time training
GPU type
GPU number
GPU time
H100
1
0.7s per epoch
Table 5. Running time of the ViT-18M model. The reported time
is obtained with torch.compile optimization.

ViT
hidden dim
Transformer blocks
# heads
MLP block hidden dim
dropout
patch size
canvas size
6M 18M 66M
384 512 768
5
10
20
8
8
12
512
0.1
2x2
64×64
Table 6. Configuration of the ViT architecture. The 18M model
is our default setting.

A. Additional Implementation Details
A.1. Configurations
We report the training configurations in Tab. 4. The running time
under this configuration is profiled in Tab. 5.
The hyperparameters for our ViT models are listed in Tab. 6,
and those for our U-net models are shown in Tab. 7.

A.2. Test-time Training Augmentation
During test-time training, we augment the single test task T into
multiple auxiliary tasks. We use a distinct task embedding for
each auxiliary task, as not all of these augmentations correspond
to the same underlying rule (e.g., consider "gravity" under a 90°
rotation). We apply 2 flippings (horizontal and vertical) or 3 rota-
tions (in multiples of 90°), and 10 predefined color index permu-
tations, resulting in (2+3)×10=50 auxiliary tasks with the orig-
U-net
# stages
layers per stage
# channels at resolution 1
attention at resolution 1
# channels at resolution 2
attention at resolution 2
# channels at resolution 3
attention at resolution 3
mid block
7M 17M 55M
3
3
3
1
1
2
80
120 160
No
No
No
160
240 320
Yes
Yes Yes
160
240 320
Yes
Yes Yes
No
No Yes
Table 7. Configuration of the U-Net architecture. The definition
follows standard U-Nets used in generative models [47, 15].

Figure 13. Shape Handling. The gray pixels denote the back-
ground tokens [BG], which keep the canvas size fixed (64×64 by
default). The white pixels denote the border tokens [BD], which
indicate the output shape. (Left): a pair (x, y) with a scaling ratio
of 1x. (Right): a pair (x, y) with a scaling ratio of 2x.

inal task. We train for 100 epochs on these 51 tasks, covering
100 x 51 x 3 = 15.3k samples in total for test-time training for
one test task T (assuming 3 raw samples in this task).

A.3. Shape Handling
Unlike standard semantic segmentation, in ARC, the raw input and
output sizes are not always identical (e.g., see Fig. 3, Test Set, Task
1). This issue can be addressed on the canvas in a unified frame-
work. In our method, the input/output canvas always has a fixed
size and is filled with a background token [BG]. In addition, when
the raw output is placed on the canvas (serving as the ground truth
during training), we always use an extra border token, [BD], to
indicate the right and bottom edges. Specifically, the token [BD]
is filled along the one-pixel-wide edge on the right and bottom
sides. Upon inference, we locate the rightmost and bottommost
[BD] tokens and crop the output accordingly to recover the final
predicted shape. This is illustrated in Fig. 13.
Since the number of background pixels [BG] can dominate
in some examples, we apply attention masks in the self-attention
blocks to encourage the model to focus on the foreground pixels.
The attention masks are applied after the query-key dot-product
computation, adding a large negative value to the keys correspond-
ing to background inputs. The resulting softmax attention scores
are therefore zero at those key positions. Moreover, during train-
ing, the loss is computed only on locations where the inputs are not
background pixels [BG]. These designs encourage the model to
pay more attention to foregrounds and therefore improve accuracy,
although we note that even without them, our method still per-
forms competitively, as observed in our preliminary experiments.
11
60
50
40
Evaluation Accuracy (%)
30
20
10
0
0
10
100
1000
Offline Training RE-ARC Pairs Per Task (Log-scaled)
Figure 14. Offline training data scaling: effect of varying the
number of RE-ARC samples per task, evaluated on the ARC-1 eval
set. Increasing the amount of offline training data is beneficial,
although even without it, our model can achieve decent accuracy.
72.5
70.0
67.5
Pass@k (Cumulative Success Rate)
Pass@k (Cumulative Success Rate)
12.5
Pass@k Curve for ARC-1
65.0
50.0
0
50
100
150 200 250
300
Pass@k Curve for Ensemble ARC-1
Pass@k (Cumulative Success Rate)
2
1
14
15
Pass@k (Cumulative Success Rate)
Pass@k Curve for ARC-2
10.5
10.0
0
50
100
150 200 250
300
Pass@k Curve for Ensemble ARC-2
Evaluation Accuracy (%)
60
50
40
30
20
10
0
0
16
80
Offline Training Task Diversity (Log-scaled)
400
Figure 15. Offline training task diversity scaling: effect of vary-
ing the number of training tasks, evaluated on the ARC-1 eval set.
Increasing task diversity is beneficial.
B. Additional Experiments
B.1. Offline Training Data Scaling
Since we use the RE-ARC dataset [22] in our offline training, we
can examine the effect of data scale provided by RE-ARC. See
Fig. 14. Using only the original ARC training data, without any
RE-ARC data, our method achieves a decent accuracy of 31.5.
By adding 10, 100, and 1,000 pairs per task from RE-ARC, the
accuracy increases to 38.6, 52.3, and 54.0, respectively. This com-
parison suggests that increasing the amount of offline training data
is beneficial, although the returns diminish beyond a certain point.
Beyond scaling the data per task using RE-ARC, we also exam-
ine the scalability of the offline training task diversity. See Fig. 15.
When trained on 0, 16, 80, and 400 tasks, the accuracy increases
from 26.4 to 43.1, 49.6, and 54.5, respectively, suggesting that the
diversity of training tasks is helpful for generalization.

B.2. Pass@k Results
By default, the ARC protocol evaluates the pass@2 accuracy. We
further examine the pass@k accuracy, thanks to our multi-view
inference with many views (510). This metric reflects whether at
least one of the k predicted solutions is correct. It can be viewed
as a recall-like measure.
Figure 16 provides the pass@k results on ARC-1 and ARC-2
eval sets. As expected, as the number of proposals (k) increases,
the pass@k accuracy increases. On ARC-1, the pass@k accu-
racy is 49.8, 54.5, and 66.3, when k is 1, 2, and 300, respectively
(Fig. 16, top-left). This result indicates that our model produces
correct predictions in some of the many views, although such cor-
rect cases are not sufficiently populated to be retained after voting.
On the other hand, this result reveals the upper-bound performance
57.5
55.0
0
250 500 750 1000 1250 1500 1750
0
20
60 80 100 120 140
Figure 16. Pass@k results in the ARC-1 (left) and ARC-2 (right)
evaluation sets. Results are obtained with majority voting from
multi-view inference, using 510 views. (Top): using a single
model of ViT-18M. (Bottom): using an ensemble of one ViT-18M
and one U-Net-55M, each with test-time training run four times.

(66.3) of our method, even if oracle voting were applied. Beyond
voting, future efforts should focus on improving the fundamental
ability of the model on each individual view.

C. Additional Visualizations
C.1. Successful and Failed Examples
We show successful and failed examples on ARC-1 (Fig. 17) and
ARC-2 (Fig. 18). See captions for detailed descriptions. Our
method can solve some highly challenging tasks, but still makes
mistakes on some tasks that are simple for humans.

C.2. Ambiguous Examples.
Although most ARC tasks are unambiguous, some may admit
multiple plausible explanations or rules. We show an example in
Fig. 19, in which our method uncovers different solutions that are
plausible. Here, the rule can be interpreted as either "turn the red
box blue only if the extended blue lines go through the box" (our
method's first guess) or "turn the red box blue if the extended blue
lines touch the box in any form" (our method's second guess).

C.3. Attention Maps
Pixel-wise Attention Maps. In Fig. 20, we visualize the attention
maps of a single pixel specified as the query. See captions for
detailed descriptions.
Layer-wise Attention Maps. In Fig. 21, we visualize the layer-
wise attention maps averaged across all pixels. See captions for
detailed descriptions.

C.4. Test-time Training Visualization
Figure 22 illustrates the evolution of model predictions during the
test-time training process. Each row corresponds to a distinct test
task from the ARC benchmark. It shows how our method progres-
sively refines its prediction through test-time training.
12

===== pages 13-16 =====

ARC-1 Solved
Demonstration 1
15663ba9
981571dc
15696249
67c52801
ARC-1 Unsolved
Demonstration 1
8dae5dfc
67636eac
aa4ec2a5
b457fec5
Demonstration 2
Input
Attempt 1
Vote: 109
Attempt 2
Vote: 57
Ground truth
Vote: 399
Vote: 35
Vote: 456
Vote: 10
Vote: 233
Vote: 123
Demonstration 2
Input
Attempt 1
Vote: 9
Attempt 2
Vote: 6
Ground truth
Vote: 14
Vote: 8
Vote: 13
Vote: 9
Vote: 3
Vote: 2
Figure 17. Successful and failed examples on ARC-1. (Top): Examples of test tasks successfully solved by VARC. (Bottom): Examples
of test tasks unsolved by VARC. (Left): Two demonstration example pairs shown for each task (some have more demonstrations not shown
here). (Right): Inference input and the first and second solutions proposed by VARC. The green box indicates the correct output.
13
ARC-2 Solved
Demonstration 1
800d221b
7666fa5d
221dfab4
7b80bb43
ARC-2 Unsolved
Demonstration 1
2b83f449
2d0172a1
3e6067c3
7ed72f31
Demonstration 2
Input
Attempt 1
Vote: 99
Attempt 2
Vote: 82
Ground truth
Vote: 410
Vote: 16
Vote: 30
Vote: 17
Vote: 168
Vote: 44
Demonstration 2
Input
Attempt 1
Attempt 2
Ground truth
Vote: 21
Vote: 20
Vote: 7
Vote: 6
Vote: 14
Vote: 12
Vote: 67
Vote: 51
Figure 18. Successful and failed examples on ARC-2. (Top): Examples of test tasks successfully solved by VARC. (Bottom): Examples
of test tasks unsolved by VARC. (Left): Two demonstration example pairs shown for each task (some have more demonstrations not shown
here). (Right): Inference input and the first and second solutions proposed by VARC. The green box indicates the correct output.
14
Demonstration Examples
Input
Attempt 1
Attempt 2
Ground truth
Figure 19. Ambiguous examples. Although most ARC tasks are unambiguous, some may admit multiple plausible explanations or rules.
Here, in the given three demonstration examples of a test task (top panel), it is unclear whether a blue line "touching" (but not "going
through") a red rectangle should render that rectangle blue. The inference example (bottom panel) involves this situation ("touching"), and
our model attempts to interpret the rule as either "going-through-only" (attempt 1) or "touching" (attempt 2).
Task
09c534e7*
Fill in the interior of the
connected boxes with the
same color.
506d28a5
Logical OR between the
upper and lower parts
of the input.
0607ce86
Remove visual noise
from a regular, repeating
grid pattern.
070dd51e
Connect horizontal
or vertical lines, with
vertical lines being on
top.
→
→
Intermediate Heatmaps
Early
Mid
Late
Block 2
Block 4
Block 5
Block 1
Block 4
Block 5
Block 2
Block 4
Block 5
Block 3 Attention focuses on
endpoints of all lines for all
pixels.
Block 4
Block 5
Block 6 Attention
is focused within the rectangle.
Block 7 Attention focuses on
the corresponding cell in the
lower part of the grid.
Block 7 Attention focuses on
other cells in the same relative
position within the grid.
Block 7 Attention focuses on
nearby, relevant lines only,
focusing strongest on the
correct line.
Figure 20. Additional visualization: pixel-level attention maps. The maps are shown for different Transformer blocks, with a query
pixel highlighted by a red-yellow border. Here we show 4 test tasks in ARC eval. Layers at different depths tend to focus on different
structures. Early layers tend to focus on local transformations and context. Middle layers tend to perform a more non-local connection,
e.g., horizontally or vertically. The deep layers are more task-specialized. The red asterisk indicates the task that was not correctly solved.
(Here, the text descriptions are written by humans solely to help readers interpret the tasks.)
15
demonstrations
inference
Layer 0
Layer 1
0607ce86 example 0
Layer 2
Layer 3
Layer 4
1.0
demonstrations
Input
inference
Output
Input
Layer 5
Layer 6
Layer 7
Layer 8
Layer 9
0.8
0.6
0.4
0bb8deee example 0
Layer 0
Layer 1
Layer 2
Layer 3
Layer 4
0.2
Layer 5
Layer 6
Layer 7
Layer 8
Layer 9
Input
Output
Ground Truth
demonstrations
Input
inference
1c56ad9f example 0
Output
Input
Layer 0
Layer 1
Layer 2
Layer 3
Layer 4
Input
Output
Ground Truth
Layer 5
Layer 6
Layer 7
Layer 8
Layer 9
demonstrations
inference
1d0a4b61 example 0
Train Example 1
Layer 0
Layer 1
Layer 2
Layer 3
Layer 4
Layer 5
Layer 6
Layer 7
Layer 8
Layer 9
0.0
Figure 21. Additional visualization: layer-wise attention maps. Each map is the per-pixel softmax attention maps averaged across all
pixels in that layer. The corresponding demonstration examples (on the left) are provided for reference.
16

===== pages 17-17 =====

55059096
Demonstration 1
Demonstration 2
Input
TTT process
Ground truth
0c786b71
Demonstration 1
Demonstration 2
Input
TTT process
Ground truth
ac3e2b04
Demonstration 1
Demonstration 2
TTT process
Input
Ground truth
Figure 22. Visualization of the test-time training process. Here, we visualize the grid augmented with a given scale ratio of 2× (the
full canvas is not shown for brevity). As the test-time training progresses, the model's predictions gradually converge toward the correct
output. In early epochs, the model produces coarse and imprecise structures; in later epochs, the model can improve the solutions, e.g.,
by refining color and spatial arrangement. This visualization illustrates the model's behavior of adapting to task-specific transformations
through few-shot test-time training.
17

--- PAPER: FIGURES & TABLES ---
{
  "figures": [
    {
      "id": "Figure 1",
      "description": "The top part shows the ARC benchmark structure with training tasks (X, y pairs) and test tasks (X, ? pairs). The bottom part illustrates the proposed Vision ARC (VARC) framework, showing how an input task (X, y pairs for training, X, ? for inference) is processed by a VARC network to produce a model prediction. The example tasks are visually represented with grids of colored squares, demonstrating concepts like reflection, symmetry, and gravity. The VARC network takes the task as input and outputs a model prediction, indicating an image-to-image translation approach."
    },
    {
      "id": "Figure 2",
      "description": "This figure presents three examples of unseen ARC tasks solved by VARC. Each panel shows a task with a few demonstration input-output pairs (X, y) at the top, and an inference input (Xinfer) with the model's predicted output (model prediction) at the bottom. The tasks involve transforming grids of colored squares. For instance, ARC-1 shows a task where the input grid is reflected and colored, ARC-2 shows a task where objects are moved and colored based on a pattern, and the third task (unlabeled) shows a transformation involving object selection and coloring. The model's predictions accurately match the expected outputs for these challenging tasks."
    },
    {
      "id": "Figure 3",
      "description": "This figure illustrates the ARC problem definition. It shows a 'Training Set Ttrain' and a 'Test Set Ttest', each containing multiple tasks (e.g., Task 1, Task 400). For each task, there are demonstration pairs (X, y) and inference pairs (Xinfer, Yinfer). In the training set, both X and y are known for demonstrations, and Xinfer is given for inference, with Yinfer to be predicted. In the test set, only demonstration pairs (X, y) and Xinfer are given, and the model must infer Yinfer. The figure uses grids of colored squares to represent the inputs and outputs, with question marks indicating unknown outputs to be predicted."
    },
    {
      "id": "Figure 4",
      "description": "This figure demonstrates the 'canvas' concept and data augmentations used in VARC. The left panel shows 'Scale' augmentation: a raw input grid (e.g., a 2x2 pattern of colored squares) is scaled up by duplicating pixels (e.g., into a 4x4 grid). The right panel shows 'Translation' augmentation: the scaled grid is randomly placed on a larger fixed-size 'canvas' (represented by a gray background). Both transformations are applied to the raw input before it is processed by the model."
    },
    {
      "id": "Figure 5",
      "description": "This figure illustrates the Vision Transformer (ViT) architecture used in VARC. The input is first randomly placed on a 'canvas' (shown in gray). This canvas is then divided into non-overlapping 'patch embeddings'. These embeddings, along with a 'task' token, are fed into a stack of 'Transformer blocks'. The output from the Transformer blocks is then passed through a 'predictor' layer, which generates the final output grid. The 'off canvas' area is also shown, indicating the background color."
    },
    {
      "id": "Figure 6",
      "description": "The top row shows demonstration examples for a task, with input and output grids. The bottom left shows an inference example input grid. The bottom right shows a sequence of grids illustrating the test-time training process, where an initial incorrect prediction for the inference example gradually becomes more accurate through training steps, eventually leading to the correct output grid."
    },
    {
      "id": "Figure 7",
      "description": "A bar chart showing the accuracy (in percentage) of different visual priors on the ARC-1 evaluation set. It starts with a 'naïve baseline' at 26.8%, then shows cumulative improvements with 'w/ 2D absolute pos embed' (32.8%), 'w/ 2D ROPE' (43.0%), '1x1 patch on 32x32 → 2x2 patch on 64x64' (45.4%), 'w/ translation aug. on canvas' (48.3%), and finally 'w/ scale aug. on canvas' (54.5%). Each bar represents an incremental improvement over the previous one."
    },
    {
      "id": "Figure 8",
      "description": "A scatter plot showing the scalability of ViT models with varying width (x-axis, 256 to 512) and depth (indicated by different colored circles, Depth=5 and Depth=10) against accuracy (y-axis, 35% to 60%). The circle areas denote model sizes (3M to 18M). Generally, increasing width and depth leads to higher accuracy, with larger models achieving better performance."
    },
    {
      "id": "Figure 9",
      "description": "A bar chart comparing TTT strategies. It shows accuracy (y-axis, 0% to 80%) for 'TTT jointly' and 'TTT independently' strategies, both with and without offline training. 'w/ offline training' consistently yields higher accuracy (54.5% for both joint and independent) compared to 'wo/ offline training' (44.8% for joint, 29.1% for independent). The 'TTT jointly' strategy performs better than 'TTT independently' when offline training is not used, but they are equal when offline training is used."
    },
    {
      "id": "Figure 9(b)",
      "description": "This figure is referenced but not shown on the page. It is described as studying TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task."
    },
    {
      "id": "Figure 10",
      "description": "This figure visualizes pixel-to-pixel attention for an ARC-1 eval test task. The top panel shows demo pairs, inference input, and model prediction. The middle panel shows attention maps for a single pixel across different layers, with pre-softmax logits. Different layers exhibit different behaviors. The bottom panel shows attention maps in layer 8 with other query pixels, all correctly attending to their corresponding palette pixel."
    },
    {
      "id": "Figure 11",
      "description": "This figure visualizes layer-wise attention maps for an ARC-1 eval test task. For each layer, pixel-to-pixel attention is computed and then averaged across all pixels to obtain a single map per layer. Some layers exhibit strong attention to the 3x3 neighborhood, reflecting the influence of the pattern's core. Other layers (e.g., layers 7-9) focus on outward-radiating rays, corresponding to the rule that extends colored pixels along eight directions."
    },
    {
      "id": "Figure 12",
      "description": "This figure shows a t-SNE visualization of task embeddings for the 400 task tokens learned from the ARC-1 training set. Each point represents a single task. Human-written descriptions are provided for some tasks to aid understanding. The visualization shows that nearby points in the embedding space exhibit similar semantics, e.g., top-left corner shows two coloring tasks, bottom-left corner shows two generalized logic operations (AND/OR/XOR)."
    },
    {
      "id": "Figure 13",
      "description": "Two pairs of input/output grids demonstrating shape handling. The left pair shows a 1x scaling ratio, with a small input grid and a slightly larger output grid. The right pair shows a 2x scaling ratio, with a larger input grid and an even larger output grid. In both cases, gray pixels denote background tokens, and white pixels denote border tokens indicating the output shape."
    },
    {
      "id": "Figure 14",
      "description": "A line graph showing the evaluation accuracy (%) on the ARC-1 eval set as a function of the number of offline training RE-ARC pairs per task (log-scaled). Accuracy increases from around 30% with 0 pairs to over 50% with 1000 pairs, showing diminishing returns."
    },
    {
      "id": "Figure 15",
      "description": "A line graph showing the evaluation accuracy (%) on the ARC-1 eval set as a function of offline training task diversity (log-scaled). Accuracy increases from around 25% with 0 tasks to over 50% with 400 tasks, indicating that diversity is beneficial."
    },
    {
      "id": "Figure 16",
      "description": "Four line graphs showing Pass@k (Cumulative Success Rate) on ARC-1 (left) and ARC-2 (right) evaluation sets, for both a single ViT-18M model (top) and an ensemble (bottom). In all graphs, Pass@k increases with k, showing that more proposals lead to higher success rates. The ensemble generally achieves higher Pass@k values than the single model."
    },
    {
      "id": "Figure 17",
      "description": "A grid of successful and failed examples from ARC-1. Each example shows an input grid, a ground truth output grid, and the model's predicted output grid. Successful examples show the model's prediction matching the ground truth, while failed examples show discrepancies."
    },
    {
      "id": "Figure 18",
      "description": "A grid of successful and failed examples from ARC-2. Similar to Figure 17, each example shows input, ground truth, and predicted output grids, highlighting both correct and incorrect predictions."
    },
    {
      "id": "Figure 19",
      "description": "An example of an ambiguous ARC task showing an input grid, a ground truth output grid, and two plausible solutions generated by the model. The first solution interprets the rule as 'turn red box blue only if extended blue lines go through the box,' while the second interprets it as 'turn red box blue if extended blue lines touch the box in any form.'"
    },
    {
      "id": "Figure 20",
      "description": "A visualization of pixel-wise attention maps. For a specified query pixel, the map shows the attention weights across the input grid, highlighting which input regions the model focuses on."
    },
    {
      "id": "Figure 21",
      "description": "A visualization of layer-wise attention maps. For different layers of the model, the attention maps averaged across all pixels are shown, indicating the overall focus of the model at different processing stages."
    },
    {
      "id": "Figure 22",
      "description": "A visualization of test-time training evolution. Each row represents a distinct test task, showing the model's predicted output grid at different stages of test-time training, demonstrating how predictions are progressively refined."
    }
  ],
  "tables": [
    {
      "id": "Table 1",
      "description": "A table comparing different ViT and U-Net models based on their width, depth, number of parameters (#params), Gflops, and accuracy (acc.). ViT models (384 width, 5 depth; 512 width, 10 depth; 768 width, 20 depth) show increasing #params, Gflops, and accuracy (44.4% to 54.5%) with larger sizes. U-Net models (setting (a), (b), (c)) also show increasing #params, Gflops, and accuracy (42.8% to 48.3%) with larger sizes, but ViT models consistently achieve higher accuracy for comparable sizes."
    },
    {
      "id": "Table 2",
      "description": "This table compares single-view and multi-view inference accuracy (pass@1). Single-view achieves 35.9, while multi-view achieves 49.8 and 54.5 (pass@2), showing a significant boost from multi-view inference due to majority voting."
    },
    {
      "id": "Table 3",
      "description": "This table provides system-level comparisons on ARC-1 and ARC-2 benchmarks, comparing large language models (LLMs), recurrent models, and vision models (VARC) against human performance. LLMs show a wide range of performance, with Grok-4-thinking and Bespoke (Grok-4) achieving the highest ARC-1 scores (66.7 and 79.6 respectively). Recurrent models (HRM, TRM) achieve ARC-1 scores around 40-45. VARC (18M) achieves 54.5 on ARC-1 and 8.3 on ARC-2, and VARC (ensemble, 73M) achieves 60.4 on ARC-1 and 11.1 on ARC-2. The VARC ensemble result (60.4) closes the gap with average human performance (60.2). Best human performance is 98.0 on ARC-1 and 100.0 on ARC-2."
    },
    {
      "id": "Table 4",
      "description": "Compares configurations for offline training and test-time training, detailing epochs (100 for both), warmup epochs (10 for both), optimizer (Adam for both), batch size (32 for offline, 8 for test-time), learning rate (3e-4 for both), learning rate scheduler (cosine for both), weight decay (0 for both), and dropout (0.1 for both)."
    },
    {
      "id": "Table 5",
      "description": "Reports the running time of the ViT-18M model for both offline and test-time training. Offline training uses 8 H100 GPUs for 4.8 hours, while test-time training uses 1 H100 GPU for 0.7 seconds per epoch."
    },
    {
      "id": "Table 6",
      "description": "Details the configurations for three ViT architectures (6M, 18M, 66M), specifying hidden dimension (384, 512, 768), Transformer blocks (5, 10, 20), number of heads (8, 8, 12), MLP block hidden dimension (512 for all), dropout (0.1 for all), patch size (2x2 for all), and canvas size (64x64 for all)."
    },
    {
      "id": "Table 7",
      "description": "Details the configurations for three U-Net architectures (7M, 17M, 55M), specifying the number of stages (3 for all), layers per stage (1, 1, 2), channels at resolution 1 (80, 120, 160), attention at resolution 1 (No for all), channels at resolution 2 (160, 240, 320), attention at resolution 2 (Yes for all), channels at resolution 3 (160, 240, 320), attention at resolution 3 (Yes for all), and mid block (No for all)."
    }
  ]
}
--- LAYER-1 MECHANISM / ASSUMPTION NODES ---
[
  {
    "node_id": "M1",
    "assigned_label": "mechanism",
    "text": "To incorporate visual priors",
    "note": "",
    "location": "Section 1",
    "parent": null,
    "source_span": "S5"
  },
  {
    "node_id": "A1",
    "assigned_label": "assumption",
    "text": "The model is expected to make predictions on each unseen task given a few examples.",
    "note": "",
    "location": "Section 1",
    "parent": null,
    "source_span": "S11"
  },
  {
    "node_id": "M2",
    "assigned_label": "mechanism",
    "text": "from which they learn transferable common sense.",
    "note": "",
    "location": "Section 1",
    "parent": null,
    "source_span": "S15"
  },
  {
    "node_id": "M3",
    "assigned_label": "mechanism",
    "text": "these recurrent models draw strong inspiration from the success of language modeling.",
    "note": "",
    "location": "Section 1",
    "parent": null,
    "source_span": "S18"
  },
  {
    "node_id": "M4",
    "assigned_label": "mechanism",
    "text": "These concepts are closely related to the visual and physical world.",
    "note": "",
    "location": "Figure 1",
    "parent": null,
    "source_span": "S23"
  },
  {
    "node_id": "M5",
    "assigned_label": "mechanism",
    "text": "Humans can solve these tasks not merely from the demonstrations, but by reasoning through analogy to their common sense obtained from external experience.",
    "note": "",
    "location": "Section 1",
    "parent": null,
    "source_span": "S24"
  },
  {
    "node_id": "M6",
    "assigned_label": "mechanism",
    "text": "Such common sense can be acquired through observing the world, particularly, the visual world.",
    "note": "",
    "location": "Section 1",
    "parent": null,
    "source_span": "S25"
  },
  {
    "node_id": "M7",
    "assigned_label": "mechanism",
    "text": "Abstraction and inference can arise directly from visual learning, without explicit linguistic intermediates.",
    "note": "",
    "location": "Section 1",
    "parent": null,
    "source_span": "S28"
  },
  {
    "node_id": "M8",
    "assigned_label": "mechanism",
    "text": "incorporating visual priors is crucial.",
    "note": "",
    "location": "Section 1",
    "parent": null,
    "source_span": "S31"
  },
  {
    "node_id": "M9",
    "assigned_label": "mechanism",
    "text": "To facilitate learning these priors, allowing the inputs to be processed as if they were natural images.",
    "note": "",
    "location": "Section 1",
    "parent": null,
    "source_span": "S33"
  },
  {
    "node_id": "M10",
    "assigned_label": "mechanism",
    "text": "A patch on the canvas can consist of exponentially many color combinations, which helps reduce overfitting and encourages the model to learn spatial priors rather than merely memorize.",
    "note": "",
    "location": "Section 1",
    "parent": null,
    "source_span": "S34"
  },
  {
    "node_id": "M11",
    "assigned_label": "mechanism",
    "text": "enabling it to generalize from only a few examples.",
    "note": "",
    "location": "Section 1",
    "parent": null,
    "source_span": "S36"
  },
  {
    "node_id": "M12",
    "assigned_label": "mechanism",
    "text": "It is natural to explore vision-driven approaches for ARC.",
    "note": "",
    "location": "Section 1",
    "parent": null,
    "source_span": "S43"
  },
  {
    "node_id": "M13",
    "assigned_label": "mechanism",
    "text": "LLMs have been regarded as a natural solution.",
    "note": "",
    "location": "Section 2",
    "parent": null,
    "source_span": "S47"
  },
  {
    "node_id": "M14",
    "assigned_label": "mechanism",
    "text": "These models aim to mimic the hierarchical and multi-timescale processing of the human brain [53] for reasoning.",
    "note": "",
    "location": "Section 2",
    "parent": null,
    "source_span": "S50"
  },
  {
    "node_id": "A2",
    "assigned_label": "assumption",
    "text": "the ARC protocol, whose essence lies precisely in few-shot, cross-task generalization.",
    "note": "",
    "location": "Section 2",
    "parent": null,
    "source_span": "S54"
  },
  {
    "node_id": "A3",
    "assigned_label": "assumption",
    "text": "the model is required to infer the output from Xinfer.",
    "note": "",
    "location": "Figure 3",
    "parent": null,
    "source_span": "S61"
  },
  {
    "node_id": "A4",
    "assigned_label": "assumption",
    "text": "the model is required to infer the desired output Yinfer.",
    "note": "",
    "location": "Section 3.1",
    "parent": null,
    "source_span": "S68"
  },
  {
    "node_id": "A5",
    "assigned_label": "assumption",
    "text": "The model should make use of Demo to infer the output of the given Xinfer for this new task.",
    "note": "",
    "location": "Section 3.1",
    "parent": null,
    "source_span": "S76"
  },
  {
    "node_id": "M15",
    "assigned_label": "mechanism",
    "text": "The presence of new (x, y) pairs in Demo at inference time allows to perform test-time training [49, 1, 9, 24]",
    "note": "",
    "location": "Section 3.1",
    "parent": null,
    "source_span": "S77"
  },
  {
    "node_id": "M16",
    "assigned_label": "mechanism",
    "text": "This formulation naturally accommodates translation and scale augmentations, which are common strategies for introducing translation and scale invariance in vision",
    "note": "",
    "location": "Section 3.3",
    "parent": null,
    "source_span": "S92"
  },
  {
    "node_id": "M17",
    "assigned_label": "mechanism",
    "text": "our canvas formulation supports a much larger set of local, patch-level configurations.",
    "note": "",
    "location": "Section 3.3",
    "parent": null,
    "source_span": "S95"
  },
  {
    "node_id": "M18",
    "assigned_label": "mechanism",
    "text": "This formulation is important for improving generalization performance.",
    "note": "",
    "location": "Section 3.3",
    "parent": null,
    "source_span": "S97"
  },
  {
    "node_id": "M19",
    "assigned_label": "mechanism",
    "text": "The “canvas\" concept enables us to flexibly apply translation and scale augmen-tations, which are critical in standard vision models.",
    "note": "",
    "location": "Section 3.3",
    "parent": null,
    "source_span": "S98"
  },
  {
    "node_id": "M20",
    "assigned_label": "mechanism",
    "text": "These data augmentations encourage the model to learn un-derlying mappings invariant to geometric transformations grounded in the visual world.",
    "note": "",
    "location": "Section 3.3",
    "parent": null,
    "source_span": "S99"
  },
  {
    "node_id": "A6",
    "assigned_label": "assumption",
    "text": "“colors” in ARC do not cor-respond to real-world colors",
    "note": "",
    "location": "Section 3.3",
    "parent": null,
    "source_span": "S102"
  },
  {
    "node_id": "M21",
    "assigned_label": "mechanism",
    "text": "it is not meaningful to perform other interpolations (such as bilinear).",
    "note": "",
    "location": "Section 3.3",
    "parent": null,
    "source_span": "S102"
  },
  {
    "node_id": "A7",
    "assigned_label": "assumption",
    "text": "We ensure all pixels are visibile.",
    "note": "",
    "location": "Section 3.3",
    "parent": null,
    "source_span": "S104"
  },
  {
    "node_id": "M22",
    "assigned_label": "mechanism",
    "text": "these visual priors are important for generalization to unseen tasks.",
    "note": "",
    "location": "Section 3.3",
    "parent": null,
    "source_span": "S105"
  },
  {
    "node_id": "M23",
    "assigned_label": "mechanism",
    "text": "it incorporates sev-eral critical inductive biases in vision: most notably, local-ity (i.e., grouping nearby pixels) and translation invariance (i.e., weight sharing across locations).",
    "note": "",
    "location": "Section 3.3",
    "parent": null,
    "source_span": "S114"
  },
  {
    "node_id": "M24",
    "assigned_label": "mechanism",
    "text": "This 2D structure can be lost if we naïvely treat the embedded patches as a 1D sequence.",
    "note": "",
    "location": "Section 3.3",
    "parent": null,
    "source_span": "S116"
  },
  {
    "node_id": "M25",
    "assigned_label": "mechanism",
    "text": "explicitly modeling positions in 2D is essential.",
    "note": "",
    "location": "Section 3.3",
    "parent": null,
    "source_span": "S117"
  },
  {
    "node_id": "M26",
    "assigned_label": "mechanism",
    "text": "making it a natural candidate for the problem we consider.",
    "note": "",
    "location": "Section 3.3",
    "parent": null,
    "source_span": "S122"
  },
  {
    "node_id": "M27",
    "assigned_label": "mechanism",
    "text": "Predictions from different views are consolidated by majority voting [1].",
    "note": "",
    "location": "Section 3.5",
    "parent": null,
    "source_span": "S135"
  },
  {
    "node_id": "M28",
    "assigned_label": "mechanism",
    "text": "we adopt majority voting in multi-view inference and retain the top-2 most populated output solutions.",
    "note": "",
    "location": "Section 4",
    "parent": null,
    "source_span": "S138"
  },
  {
    "node_id": "A8",
    "assigned_label": "assumption",
    "text": "As there are very few demo pairs in Demo (e.g., 2 to 4)",
    "note": "",
    "location": "Section 3.5",
    "parent": "S146",
    "source_span": "S146"
  },
  {
    "node_id": "A9",
    "assigned_label": "assumption",
    "text": "As the new demo pairs in Demo are very few",
    "note": "",
    "location": "Section 3.5",
    "parent": "S148",
    "source_span": "S148"
  },
  {
    "node_id": "A10",
    "assigned_label": "assumption",
    "text": "Since one output location in the raw grid may be predicted by multi-ple pixels on the canvas (e.g., due to rescaling; see Fig. 5)",
    "note": "",
    "location": "Section 3.5",
    "parent": "S154",
    "source_span": "S154"
  },
  {
    "node_id": "M29",
    "assigned_label": "mechanism",
    "text": "we aggregate all predictions (from softmax outputs) at this location by average pooling.",
    "note": "",
    "location": "Section 3.5",
    "parent": "S154",
    "source_span": "S154"
  },
  {
    "node_id": "M30",
    "assigned_label": "mechanism",
    "text": "to im-prove accuracy",
    "note": "",
    "location": "Section 3.5",
    "parent": "S157",
    "source_span": "S157"
  },
  {
    "node_id": "A11",
    "assigned_label": "assumption",
    "text": "As the multi-view inference cost is negli-gible compared with test-time training cost",
    "note": "",
    "location": "Section 3.5",
    "parent": "S158",
    "source_span": "S158"
  },
  {
    "node_id": "M31",
    "assigned_label": "mechanism",
    "text": "To make test-time training more feasible",
    "note": "",
    "location": "Section 4",
    "parent": "S171",
    "source_span": "S171"
  },
  {
    "node_id": "A12",
    "assigned_label": "assumption",
    "text": "under the assumption that all auxiliary tasks are translation and scale invariant",
    "note": "",
    "location": "Section 4",
    "parent": "S174",
    "source_span": "S174"
  },
  {
    "node_id": "M32",
    "assigned_label": "mechanism",
    "text": "To support pass@2 evaluation",
    "note": "",
    "location": "Section 5",
    "parent": "S177",
    "source_span": "S177"
  },
  {
    "node_id": "A13",
    "assigned_label": "assumption",
    "text": "In majority voting, two output grids are considered \"consistent” only when they are identical across the entire grid.",
    "note": "",
    "location": "Footnote 2",
    "parent": null,
    "source_span": "S181"
  },
  {
    "node_id": "M33",
    "assigned_label": "mechanism",
    "text": "The winner is the grid that is \"consistent\" with the largest number of other output grids.",
    "note": "",
    "location": "Footnote 2",
    "parent": null,
    "source_span": "S182"
  },
  {
    "node_id": "M34",
    "assigned_label": "mechanism",
    "text": "This enables the expansion of the token set from a very limited size (e.g., 10) to an exponentially large number.",
    "note": "",
    "location": "Section 5.1",
    "parent": null,
    "source_span": "S207"
  },
  {
    "node_id": "A14",
    "assigned_label": "assumption",
    "text": "if we constrain each 2×2 patch to cover only one raw pixel, it becomes equivalent to the 1×1 patch counterpart on the 32×32 canvas.",
    "note": "",
    "location": "Section 5.1",
    "parent": null,
    "source_span": "S212"
  },
  {
    "node_id": "M35",
    "assigned_label": "mechanism",
    "text": "to ensure a meaningful compar-ison",
    "note": "",
    "location": "Section 5.1",
    "parent": "S213",
    "source_span": "S213"
  },
  {
    "node_id": "M36",
    "assigned_label": "mechanism",
    "text": "each patch can cover multiple colors (as in natural images), which substan-tially enriches the data space for learning.",
    "note": "",
    "location": "Section 5.1",
    "parent": null,
    "source_span": "S216"
  },
  {
    "node_id": "M37",
    "assigned_label": "mechanism",
    "text": "This can explain why scale augmen-tation yields a substantial gain.",
    "note": "",
    "location": "Section 5.1",
    "parent": null,
    "source_span": "S232"
  },
  {
    "node_id": "M38",
    "assigned_label": "mechanism",
    "text": "this problem can also be effectively addressed by classical vision backbones.",
    "note": "",
    "location": "Section 5.2",
    "parent": "S236",
    "source_span": "S236"
  },
  {
    "node_id": "M39",
    "assigned_label": "mechanism",
    "text": "as a result of better fitting.",
    "note": "",
    "location": "Section 5.2",
    "parent": "S239",
    "source_span": "S239"
  },
  {
    "node_id": "A15",
    "assigned_label": "assumption",
    "text": "Going beyond this regime can lead to overfitting in our current setting",
    "note": "",
    "location": "Section 5.2",
    "parent": "S240",
    "source_span": "S240"
  },
  {
    "node_id": "M40",
    "assigned_label": "mechanism",
    "text": "common sense about the visual world can be learned from the training set.",
    "note": "",
    "location": "Section 5.2",
    "parent": "S244",
    "source_span": "S244"
  },
  {
    "node_id": "M41",
    "assigned_label": "mechanism",
    "text": "some tasks in this benchmark can be solved tabula rasa.",
    "note": "",
    "location": "Section 5.2",
    "parent": "S245",
    "source_span": "S245"
  },
  {
    "node_id": "A16",
    "assigned_label": "assumption",
    "text": "the latter relies on a stronger assumption about the availability of multiple test tasks at once.",
    "note": "",
    "location": "Section 5.2",
    "parent": "S247",
    "source_span": "S247"
  },
  {
    "node_id": "A17",
    "assigned_label": "assumption",
    "text": "Since single-view inference cannot produce mul-tiple predictions",
    "note": "",
    "location": "Section 5.2",
    "parent": "S251",
    "source_span": "S251"
  },
  {
    "node_id": "M42",
    "assigned_label": "mechanism",
    "text": "thanks to majority voting.",
    "note": "",
    "location": "Section 5.2",
    "parent": "S255",
    "source_span": "S255"
  },
  {
    "node_id": "A18",
    "assigned_label": "assumption",
    "text": "in ARC, a mistake on even a single pixel renders the entire prediction incorrect.",
    "note": "",
    "location": "Section 5.2",
    "parent": null,
    "source_span": "S256"
  },
  {
    "node_id": "M43",
    "assigned_label": "mechanism",
    "text": "we provide additional qualita-tive results that help reveal the model's behavior.",
    "note": "",
    "location": "Section 6",
    "parent": null,
    "source_span": "S274"
  },
  {
    "node_id": "M44",
    "assigned_label": "mechanism",
    "text": "These attention maps show that our model can correctly reason about the relationship between a source pixel and its target pixel to copy from.",
    "note": "",
    "location": "Section 6",
    "parent": null,
    "source_span": "S277"
  },
  {
    "node_id": "M45",
    "assigned_label": "mechanism",
    "text": "it reveals which pixels receive the most attention in that layer.",
    "note": "",
    "location": "Section 6",
    "parent": "S279",
    "source_span": "S279"
  },
  {
    "node_id": "M46",
    "assigned_label": "mechanism",
    "text": "reflecting the influence of the pattern's core.",
    "note": "",
    "location": "Section 6",
    "parent": "S280",
    "source_span": "S280"
  },
  {
    "node_id": "M47",
    "assigned_label": "mechanism",
    "text": "corresponding to the rule that extends colored pixels along the eight directions.",
    "note": "",
    "location": "Section 6",
    "parent": "S281",
    "source_span": "S281"
  },
  {
    "node_id": "M48",
    "assigned_label": "mechanism",
    "text": "This vi-sualization suggests that our method attempts to learn the relations between different tasks",
    "note": "",
    "location": "Section 6",
    "parent": "S290",
    "source_span": "S290"
  },
  {
    "node_id": "M49",
    "assigned_label": "mechanism",
    "text": "It naturally enables the adaptation of visual frame-works",
    "note": "",
    "location": "Section 7",
    "parent": "S293",
    "source_span": "S293"
  },
  {
    "node_id": "M50",
    "assigned_label": "mechanism",
    "text": "This opens up a new possibility of treating ARC as a vision-centric prob-lem, emphasizing abstraction and reasoning emerging di-rectly from image pixels.",
    "note": "",
    "location": "Section 7",
    "parent": null,
    "source_span": "S294"
  },
  {
    "node_id": "A19",
    "assigned_label": "assumption",
    "text": "it cannot be assumed that multiple unseen tasks will be presented all at once.",
    "note": "",
    "location": "Footnote 3",
    "parent": null,
    "source_span": "S295"
  },
  {
    "node_id": "M51",
    "assigned_label": "mechanism",
    "text": "This issue can be addressed on the canvas in a unified framework.",
    "note": "",
    "location": "Section A.3",
    "parent": null,
    "source_span": "S346"
  },
  {
    "node_id": "M52",
    "assigned_label": "mechanism",
    "text": "to encourage the model to focus on the foreground pixels.",
    "note": "",
    "location": "Section A.3",
    "parent": null,
    "source_span": "S351"
  },
  {
    "node_id": "M53",
    "assigned_label": "mechanism",
    "text": "The resulting softmax attention scores are therefore zero at those key positions.",
    "note": "",
    "location": "Section A.3",
    "parent": null,
    "source_span": "S353"
  },
  {
    "node_id": "M54",
    "assigned_label": "mechanism",
    "text": "These designs encourage the model to pay more attention to foregrounds and therefore improve accuracy",
    "note": "",
    "location": "Section A.3",
    "parent": null,
    "source_span": "S355"
  },
  {
    "node_id": "M55",
    "assigned_label": "mechanism",
    "text": "increasing the amount of offline training data is beneficial, although the returns diminish beyond a certain point.",
    "note": "",
    "location": "Section B.1",
    "parent": null,
    "source_span": "S363"
  },
  {
    "node_id": "M56",
    "assigned_label": "mechanism",
    "text": "the diversity of training tasks is helpful for generalization.",
    "note": "",
    "location": "Section B.1",
    "parent": null,
    "source_span": "S365"
  },
  {
    "node_id": "M57",
    "assigned_label": "mechanism",
    "text": "our model produces correct predictions in some of the many views, although such cor-rect cases are not sufficiently populated to be retained after voting.",
    "note": "",
    "location": "Section B.2",
    "parent": null,
    "source_span": "S373"
  },
  {
    "node_id": "A20",
    "assigned_label": "assumption",
    "text": "some may admit multiple plausible explanations or rules.",
    "note": "",
    "location": "Section C.2",
    "parent": null,
    "source_span": "S377"
  },
  {
    "node_id": "M58",
    "assigned_label": "mechanism",
    "text": "the rule can be interpreted as either \"turn the red box blue only if the extended blue lines go through the box\" (our method's first guess) or \"turn the red box blue if the extended blue lines touch the box in any form\" (our method's second guess).",
    "note": "",
    "location": "Section C.2",
    "parent": null,
    "source_span": "S379"
  },
  {
    "node_id": "A21",
    "assigned_label": "assumption",
    "text": "most ARC tasks are unambiguous",
    "note": "",
    "location": "Figure 19",
    "parent": "S400",
    "source_span": "S400"
  },
  {
    "node_id": "A22",
    "assigned_label": "assumption",
    "text": "it is unclear whether a blue line \"touching\" (but not \"going through\") a red rectangle should render that rectangle blue",
    "note": "",
    "location": "Figure 19",
    "parent": "S401",
    "source_span": "S401"
  },
  {
    "node_id": "M59",
    "assigned_label": "mechanism",
    "text": "Layers at different depths tend to focus on different structures",
    "note": "",
    "location": "Figure 20",
    "parent": "S407",
    "source_span": "S407"
  },
  {
    "node_id": "M60",
    "assigned_label": "mechanism",
    "text": "Early layers tend to focus on local transformations and context",
    "note": "",
    "location": "Figure 20",
    "parent": "S408",
    "source_span": "S408"
  },
  {
    "node_id": "M61",
    "assigned_label": "mechanism",
    "text": "Middle layers tend to perform a more non-local connection, e.g., horizontally or vertically",
    "note": "",
    "location": "Figure 20",
    "parent": "S409",
    "source_span": "S409"
  },
  {
    "node_id": "M62",
    "assigned_label": "mechanism",
    "text": "The deep layers are more task-specialized",
    "note": "",
    "location": "Figure 20",
    "parent": "S410",
    "source_span": "S410"
  },
  {
    "node_id": "M63",
    "assigned_label": "mechanism",
    "text": "Attention focuses on endpoints of all lines for all pixels.",
    "note": "Block 2 heatmap description",
    "location": "Figure 20",
    "parent": "S413",
    "source_span": "S413"
  },
  {
    "node_id": "M64",
    "assigned_label": "mechanism",
    "text": "Attention is focused within the rectangle.",
    "note": "Block 6 heatmap description",
    "location": "Figure 20",
    "parent": "S413",
    "source_span": "S413"
  },
  {
    "node_id": "M65",
    "assigned_label": "mechanism",
    "text": "Attention focuses on the corresponding cell in the lower part of the grid.",
    "note": "Block 7 heatmap description",
    "location": "Figure 20",
    "parent": "S414",
    "source_span": "S414"
  },
  {
    "node_id": "M66",
    "assigned_label": "mechanism",
    "text": "Attention focuses on other cells in the same relative position within the grid.",
    "note": "Block 7 heatmap description",
    "location": "Figure 20",
    "parent": "S415",
    "source_span": "S415"
  },
  {
    "node_id": "M67",
    "assigned_label": "mechanism",
    "text": "Attention focuses on endpoints of all lines for all pixels.",
    "note": "Block 3 heatmap description",
    "location": "Figure 20",
    "parent": "S416",
    "source_span": "S416"
  },
  {
    "node_id": "M68",
    "assigned_label": "mechanism",
    "text": "Attention focuses on nearby, relevant lines only, focusing strongest on the correct line.",
    "note": "Block 7 heatmap description",
    "location": "Figure 20",
    "parent": "S416",
    "source_span": "S416"
  },
  {
    "node_id": "M69",
    "assigned_label": "mechanism",
    "text": "by refining color and spatial arrangement",
    "note": "",
    "location": "Figure 22 caption",
    "parent": "S425",
    "source_span": "S425"
  },
  {
    "node_id": "M70",
    "assigned_label": "mechanism",
    "text": "model's behavior of adapting to task-specific transformations",
    "note": "",
    "location": "Figure 22 caption",
    "parent": "S426",
    "source_span": "S426"
  }
]
--- END INPUT ---

## Your task

Emit an AM card ONLY for a node that is a genuine belief target. Be strict.

### mechanism = a causal explanation for WHY an intervention produces its effect
(e.g. "visual priors let the model generalize from few examples").
REJECT — do not card — nodes that are merely:
- a purpose / goal fragment ("to improve accuracy", "to incorporate visual priors"),
- background motivation or a general aim ("draw inspiration from language modeling"),
- a restatement of the result itself.

### assumption — accept ONLY a load-bearing precondition (be much stricter than for mechanism)

An assumption is worth carding ONLY if it is a **load-bearing precondition whose truth would change
the interpretation of one or more concrete observations in THIS paper**. Sort every candidate into
one of three buckets and card only the first:

- **(A) Load-bearing precondition — CARD IT.** A concrete observation's interpretation would become
  invalid if this statement were false, OR the paper explicitly frames it as an assumption /
  requirement / limitation / scope condition / necessary condition, OR a concrete observation in this
  paper could directly strengthen or weaken it.
  (e.g. "ARC tasks are visual enough that visual priors help" — the visual-prior ablations directly
  bear on it; "most ARC tasks are unambiguous" — multi-view/voting results bear on it.)

- **(B) Evaluation / scope / task-setup condition — DO NOT CARD (leave for context).** A description
  of the experimental setting or benchmark protocol, not a belief the results test.
  (e.g. "the model predicts each unseen task given a few examples", "evaluation uses pass@2".)

- **(C) Background / world statement — DO NOT CARD.** Paper background or general motivation that no
  observation in this paper could plausibly support or weaken.
  (e.g. "humans solve ARC using common sense".)

Explicit reject list for assumptions — never card:
- task definitions or benchmark protocol descriptions;
- generic background or broad motivation statements;
- statements that merely restate the dataset / problem setup;
- any statement that no concrete observation in this paper could plausibly support or weaken.

**If you are unsure whether a node is a load-bearing assumption or just context/background, REJECT
it as an AM card** and leave it for the context / canonicalization stage. Missing a borderline
assumption is cheaper than admitting an unstable one — do not card on the benefit of the doubt.

### DEDUPLICATE
When several nodes state the SAME mechanism or assumption — most importantly the paper's headline
thesis repeated in many places — emit ONE card and list the other node_ids as `aliases`. Do not
create near-duplicate cards. Use the paper text to decide both genuineness and which nodes are the
same claim.

## Output

A JSON array only (no prose), each element exactly:

```json
{
  "am_id": "AM_001",
  "kind": "mechanism",
  "node": "M7",
  "aliases": ["M23", "M31"],
  "gloss": "abstraction can arise from visual learning alone",
  "provenance": { "location": "Section 1" }
}
```

`gloss` is a <=12-word restatement for readability. `node` is the representative node_id; `aliases`
is every other node_id (possibly empty) that restates the same belief. Emit nothing for rejected
nodes.
