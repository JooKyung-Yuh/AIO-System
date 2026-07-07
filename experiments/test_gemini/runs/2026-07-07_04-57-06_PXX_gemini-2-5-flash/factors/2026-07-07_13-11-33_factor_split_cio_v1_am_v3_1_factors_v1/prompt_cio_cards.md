You are assembling **CIO observation cards** — the "what was done and what was measured" layer of
an AIO factor graph. Each card is ONE measured observation: a context (the experimental setting),
an intervention (and its reference / baseline arm when the paper compares two conditions), and an
observable (an eval_metric + the measured pattern). A CIO card carries **NO mechanism and NO
assumption** — the "why the authors think so" layer is built separately and linked later.

paper_id: PXX
paper_title_hint: unknown

You are given (1) the paper itself (prose transcription + figure/table descriptions) so you can
ground each observation, and (2) a Layer-1 span extraction already grouped into local **evidence
units** by the paper location the spans came from (a Table, a Figure, or a Section). Each node has a
per-category node_id (C.. context, I.. intervention, E.. eval_metric, P.. pattern) and a
source_span.

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
--- LAYER-1 EVIDENCE UNITS (spans grouped by location) ---
[
  {
    "unit_id": "U001",
    "location": "Section 1",
    "kind": "intro",
    "source_chunk": 1,
    "span_range": [
      1,
      44
    ],
    "node_count": 65,
    "category_counts": {
      "assumption": 1,
      "mechanism": 11,
      "context": 27,
      "intervention": 12,
      "eval_metric": 2,
      "pattern": 12
    },
    "has_pattern": true,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C1",
        "label": "context",
        "source_span": "S1",
        "parent": null,
        "note": "",
        "text": "The Abstraction and Reasoning Corpus (ARC) is designed to promote research on abstract reasoning, a fundamental aspect of human intelligence."
      },
      {
        "node_id": "C2",
        "label": "context",
        "source_span": "S2",
        "parent": null,
        "note": "",
        "text": "Common approaches to ARC treat it as a language-oriented problem, addressed by large language models (LLMs) or recurrent reasoning models."
      },
      {
        "node_id": "C3",
        "label": "context",
        "source_span": "S3",
        "parent": null,
        "note": "",
        "text": "the puzzle-like tasks in ARC are inherently visual"
      },
      {
        "node_id": "C4",
        "label": "context",
        "source_span": "S3",
        "parent": null,
        "note": "",
        "text": "existing research has rarely approached the problem from a vision-centric perspective."
      },
      {
        "node_id": "I1",
        "label": "intervention",
        "source_span": "S4",
        "parent": null,
        "note": "",
        "text": "formulate ARC within a vision paradigm, framing it as an image-to-image translation problem."
      },
      {
        "node_id": "I2",
        "label": "intervention",
        "source_span": "S5",
        "parent": null,
        "note": "",
        "text": "represent the inputs on a “canvas\" that can be processed like natural images."
      },
      {
        "node_id": "M1",
        "label": "mechanism",
        "source_span": "S5",
        "parent": null,
        "note": "",
        "text": "To incorporate visual priors"
      },
      {
        "node_id": "I3",
        "label": "intervention",
        "source_span": "S6",
        "parent": null,
        "note": "",
        "text": "apply standard vision architectures, such as a vanilla Vision Transformer (ViT), to perform image-to-image mapping."
      },
      {
        "node_id": "C5",
        "label": "context",
        "source_span": "S7",
        "parent": null,
        "note": "",
        "text": "Our model is trained from scratch solely on ARC data"
      },
      {
        "node_id": "I4",
        "label": "intervention",
        "source_span": "S7",
        "parent": null,
        "note": "",
        "text": "generalizes to unseen tasks through test-time training."
      },
      {
        "node_id": "C6",
        "label": "context",
        "source_span": "S8",
        "parent": null,
        "note": "",
        "text": "Our framework, termed Vision ARC (VARC)"
      },
      {
        "node_id": "E1",
        "label": "eval_metric",
        "source_span": "S8",
        "parent": null,
        "note": "",
        "text": "accuracy"
      },
      {
        "node_id": "C7",
        "label": "context",
        "source_span": "S8",
        "parent": null,
        "note": "",
        "text": "on the ARC-1 benchmark"
      },
      {
        "node_id": "P1",
        "label": "pattern",
        "source_span": "S8",
        "parent": null,
        "note": "60.4%",
        "text": "achieves accuracy",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "P2",
        "label": "pattern",
        "source_span": "S8",
        "parent": null,
        "note": "",
        "text": "substantially outperforming existing methods that are also trained from scratch.",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "P3",
        "label": "pattern",
        "source_span": "S9",
        "parent": null,
        "note": "",
        "text": "competitive with those of leading LLMs",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "P4",
        "label": "pattern",
        "source_span": "S9",
        "parent": null,
        "note": "",
        "text": "close the gap to average human performance",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "C8",
        "label": "context",
        "source_span": "S10",
        "parent": null,
        "note": "",
        "text": "ARC consists of a collection of puzzle-like tasks (Fig. 1, top), each containing only a few examples governed by a unique underlying transformation rule."
      },
      {
        "node_id": "A1",
        "label": "assumption",
        "source_span": "S11",
        "parent": null,
        "note": "",
        "text": "The model is expected to make predictions on each unseen task given a few examples."
      },
      {
        "node_id": "C9",
        "label": "context",
        "source_span": "S12",
        "parent": null,
        "note": "",
        "text": "humans are capable of solving various ARC tasks [25, 31, 32]"
      },
      {
        "node_id": "C10",
        "label": "context",
        "source_span": "S12",
        "parent": null,
        "note": "",
        "text": "the benchmark remains highly challenging for today's leading machine learning systems [44, 42]."
      },
      {
        "node_id": "C11",
        "label": "context",
        "source_span": "S13",
        "parent": null,
        "note": "",
        "text": "methods based on large language models (LLMs)"
      },
      {
        "node_id": "P5",
        "label": "pattern",
        "source_span": "S13",
        "parent": null,
        "note": "",
        "text": "have proven highly competitive.",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "I5",
        "label": "intervention",
        "source_span": "S14",
        "parent": null,
        "note": "",
        "text": "convert ARC inputs into sequences of text tokens for language modeling."
      },
      {
        "node_id": "C12",
        "label": "context",
        "source_span": "S15",
        "parent": null,
        "note": "",
        "text": "The LLMs are pre-trained on internet-scale data"
      },
      {
        "node_id": "M2",
        "label": "mechanism",
        "source_span": "S15",
        "parent": null,
        "note": "",
        "text": "from which they learn transferable common sense."
      },
      {
        "node_id": "C13",
        "label": "context",
        "source_span": "S16",
        "parent": null,
        "note": "",
        "text": "recurrent models [53, 27]"
      },
      {
        "node_id": "P6",
        "label": "pattern",
        "source_span": "S16",
        "parent": null,
        "note": "",
        "text": "has achieved impressive results on ARC",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "C14",
        "label": "context",
        "source_span": "S16",
        "parent": null,
        "note": "",
        "text": "without relying on internet-scale data."
      },
      {
        "node_id": "C15",
        "label": "context",
        "source_span": "S17",
        "parent": null,
        "note": "",
        "text": "These models are trained from scratch on ARC data only"
      },
      {
        "node_id": "I6",
        "label": "intervention",
        "source_span": "S17",
        "parent": null,
        "note": "",
        "text": "perform inference through recurrent, iterative reasoning."
      },
      {
        "node_id": "M3",
        "label": "mechanism",
        "source_span": "S18",
        "parent": null,
        "note": "",
        "text": "these recurrent models draw strong inspiration from the success of language modeling."
      },
      {
        "node_id": "C16",
        "label": "context",
        "source_span": "S19",
        "parent": null,
        "note": "",
        "text": "the ARC puzzles are typically presented visually"
      },
      {
        "node_id": "C17",
        "label": "context",
        "source_span": "S19",
        "parent": null,
        "note": "",
        "text": "existing research has rarely framed ARC as a vision-centric problem."
      },
      {
        "node_id": "C18",
        "label": "context",
        "source_span": "S20",
        "parent": null,
        "note": "",
        "text": "many concepts in ARC are inherently visual and physical: e.g., reflection, symmetry, and gravity, as shown in Fig. 1."
      },
      {
        "node_id": "M5",
        "label": "mechanism",
        "source_span": "S24",
        "parent": null,
        "note": "",
        "text": "Humans can solve these tasks not merely from the demonstrations, but by reasoning through analogy to their common sense obtained from external experience."
      },
      {
        "node_id": "M6",
        "label": "mechanism",
        "source_span": "S25",
        "parent": null,
        "note": "",
        "text": "Such common sense can be acquired through observing the world, particularly, the visual world."
      },
      {
        "node_id": "I8",
        "label": "intervention",
        "source_span": "S26",
        "parent": null,
        "note": "",
        "text": "approach ARC from a vision-centric perspective."
      },
      {
        "node_id": "I9",
        "label": "intervention",
        "source_span": "S27",
        "parent": null,
        "note": "",
        "text": "frame each puzzle as an image-to-image translation problem."
      },
      {
        "node_id": "M7",
        "label": "mechanism",
        "source_span": "S28",
        "parent": null,
        "note": "",
        "text": "Abstraction and inference can arise directly from visual learning, without explicit linguistic intermediates."
      },
      {
        "node_id": "C20",
        "label": "context",
        "source_span": "S29",
        "parent": null,
        "note": "",
        "text": "This perspective connects ARC to classical image-to-image problems, ranging from low-level image processing (e.g., [16, 43]) to high-level image understanding (e.g., [38, 46])."
      },
      {
        "node_id": "I10",
        "label": "intervention",
        "source_span": "S30",
        "parent": null,
        "note": "",
        "text": "apply standard vision models (e.g., Vision Transformers [17] or convolutional networks [30]) to tackle the ARC problem."
      },
      {
        "node_id": "M8",
        "label": "mechanism",
        "source_span": "S31",
        "parent": null,
        "note": "",
        "text": "incorporating visual priors is crucial."
      },
      {
        "node_id": "C21",
        "label": "context",
        "source_span": "S32",
        "parent": null,
        "note": "",
        "text": "These priors include 2D spatial locality, translation invariance, and scale invariance."
      },
      {
        "node_id": "I11",
        "label": "intervention",
        "source_span": "S33",
        "parent": null,
        "note": "",
        "text": "represent the inputs on a \"canvas\" with flexible geometric transformations"
      },
      {
        "node_id": "M9",
        "label": "mechanism",
        "source_span": "S33",
        "parent": null,
        "note": "",
        "text": "To facilitate learning these priors, allowing the inputs to be processed as if they were natural images."
      },
      {
        "node_id": "M10",
        "label": "mechanism",
        "source_span": "S34",
        "parent": null,
        "note": "",
        "text": "A patch on the canvas can consist of exponentially many color combinations, which helps reduce overfitting and encourages the model to learn spatial priors rather than merely memorize."
      },
      {
        "node_id": "C22",
        "label": "context",
        "source_span": "S35",
        "parent": null,
        "note": "",
        "text": "train our model from scratch using ARC-only data."
      },
      {
        "node_id": "I12",
        "label": "intervention",
        "source_span": "S36",
        "parent": null,
        "note": "",
        "text": "perform test-time training [9, 24, 49, 1, 53, 27] to adapt the model to the task"
      },
      {
        "node_id": "M11",
        "label": "mechanism",
        "source_span": "S36",
        "parent": null,
        "note": "",
        "text": "enabling it to generalize from only a few examples."
      },
      {
        "node_id": "C23",
        "label": "context",
        "source_span": "S37",
        "parent": null,
        "note": "",
        "text": "Our framework, termed Vision ARC (VARC)"
      },
      {
        "node_id": "P7",
        "label": "pattern",
        "source_span": "S37",
        "parent": null,
        "note": "",
        "text": "shows strong performance on the ARC benchmarks (e.g., Fig. 2).",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "C24",
        "label": "context",
        "source_span": "S38",
        "parent": null,
        "note": "",
        "text": "VARC"
      },
      {
        "node_id": "E2",
        "label": "eval_metric",
        "source_span": "S38",
        "parent": null,
        "note": "",
        "text": "accuracy"
      },
      {
        "node_id": "P8",
        "label": "pattern",
        "source_span": "S38",
        "parent": null,
        "note": "54.5%",
        "text": "achieves accuracy",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "C25",
        "label": "context",
        "source_span": "S38",
        "parent": null,
        "note": "",
        "text": "on the ARC-1 benchmark"
      },
      {
        "node_id": "C26",
        "label": "context",
        "source_span": "S38",
        "parent": null,
        "note": "18 million parameters",
        "text": "using a small model with only 18 million parameters."
      },
      {
        "node_id": "P9",
        "label": "pattern",
        "source_span": "S39",
        "parent": null,
        "note": "",
        "text": "substantially surpasses the best recurrent methods [53, 27] that are also trained from scratch on ARC.",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "P10",
        "label": "pattern",
        "source_span": "S40",
        "parent": null,
        "note": "",
        "text": "competitive with many popular LLM-based methods.",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "I13",
        "label": "intervention",
        "source_span": "S41",
        "parent": null,
        "note": "",
        "text": "Combining VARC models through ensembling [29]"
      },
      {
        "node_id": "P11",
        "label": "pattern",
        "source_span": "S41",
        "parent": null,
        "note": "to 60.4%",
        "text": "further improves accuracy",
        "pattern_class": "comparison"
      },
      {
        "node_id": "P12",
        "label": "pattern",
        "source_span": "S41",
        "parent": null,
        "note": "",
        "text": "matching the reported average human performance [31] on the ARC-1 dataset.",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "C27",
        "label": "context",
        "source_span": "S42",
        "parent": null,
        "note": "",
        "text": "the design of the ARC benchmark is based on human observations and induced rules abstracted from the visual and physical world."
      },
      {
        "node_id": "M12",
        "label": "mechanism",
        "source_span": "S43",
        "parent": null,
        "note": "",
        "text": "It is natural to explore vision-driven approaches for ARC."
      },
      {
        "node_id": "C28",
        "label": "context",
        "source_span": "S44",
        "parent": null,
        "note": "",
        "text": "human reasoning is not confined to language or vision in isolation, but instead should integrate information across modalities."
      }
    ]
  },
  {
    "unit_id": "U002",
    "location": "Figure 1",
    "kind": "table_fig",
    "source_chunk": 1,
    "span_range": [
      21,
      23
    ],
    "node_count": 3,
    "category_counts": {
      "mechanism": 1,
      "context": 1,
      "intervention": 1
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C19",
        "label": "context",
        "source_span": "S21",
        "parent": null,
        "note": "",
        "text": "The ARC benchmark (top) consists of a collection of many different tasks, where each task has a few (e.g., 2-4) examples."
      },
      {
        "node_id": "I7",
        "label": "intervention",
        "source_span": "S22",
        "parent": null,
        "note": "",
        "text": "propose the Vision ARC (VARC) framework, which addresses the ARC problem as an image-to-image translation problem, from a computer vision perspective (bottom)."
      },
      {
        "node_id": "M4",
        "label": "mechanism",
        "source_span": "S23",
        "parent": null,
        "note": "",
        "text": "These concepts are closely related to the visual and physical world."
      }
    ]
  },
  {
    "unit_id": "U003",
    "location": "Section 2",
    "kind": "section",
    "source_chunk": 1,
    "span_range": [
      45,
      56
    ],
    "node_count": 15,
    "category_counts": {
      "assumption": 1,
      "mechanism": 2,
      "context": 7,
      "intervention": 2,
      "pattern": 3
    },
    "has_pattern": true,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C29",
        "label": "context",
        "source_span": "S45",
        "parent": null,
        "note": "",
        "text": "classical visual reasoning protocols generally involve a training set and a test set, both of which can be viewed as instances of the same task."
      },
      {
        "node_id": "C30",
        "label": "context",
        "source_span": "S46",
        "parent": null,
        "note": "",
        "text": "ARC consists of a large collection of distinct tasks, each defined by only a few examples."
      },
      {
        "node_id": "C31",
        "label": "context",
        "source_span": "S47",
        "parent": null,
        "note": "",
        "text": "the \"few-shot, many-task\" nature of ARC"
      },
      {
        "node_id": "M13",
        "label": "mechanism",
        "source_span": "S47",
        "parent": null,
        "note": "",
        "text": "LLMs have been regarded as a natural solution."
      },
      {
        "node_id": "I14",
        "label": "intervention",
        "source_span": "S48",
        "parent": null,
        "note": "",
        "text": "A new task can be converted into a sequence of tokens, treated as a prompt, and processed by LLMs via in-context few-shot learning [55, 10]."
      },
      {
        "node_id": "C32",
        "label": "context",
        "source_span": "S49",
        "parent": null,
        "note": "",
        "text": "recurrent models [53, 27]"
      },
      {
        "node_id": "P13",
        "label": "pattern",
        "source_span": "S49",
        "parent": null,
        "note": "",
        "text": "have been proven effective for ARC",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "C33",
        "label": "context",
        "source_span": "S49",
        "parent": null,
        "note": "",
        "text": "without the requirement of internet-scale pre-training."
      },
      {
        "node_id": "M14",
        "label": "mechanism",
        "source_span": "S50",
        "parent": null,
        "note": "",
        "text": "These models aim to mimic the hierarchical and multi-timescale processing of the human brain [53] for reasoning."
      },
      {
        "node_id": "I15",
        "label": "intervention",
        "source_span": "S51",
        "parent": null,
        "note": "",
        "text": "adopt test-time training [9, 24, 49] on the few demonstration examples."
      },
      {
        "node_id": "C34",
        "label": "context",
        "source_span": "S52",
        "parent": null,
        "note": "",
        "text": "the ViT-ARC method [34] attempts to address the ARC problem using vision models."
      },
      {
        "node_id": "P14",
        "label": "pattern",
        "source_span": "S53",
        "parent": null,
        "note": "",
        "text": "has only shown the ability to fit individual tasks in the training set",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "P15",
        "label": "pattern",
        "source_span": "S53",
        "parent": null,
        "note": "",
        "text": "it is unable to generalize or solve any unseen test task.",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "A2",
        "label": "assumption",
        "source_span": "S54",
        "parent": null,
        "note": "",
        "text": "the ARC protocol, whose essence lies precisely in few-shot, cross-task generalization."
      },
      {
        "node_id": "C36",
        "label": "context",
        "source_span": "S56",
        "parent": null,
        "note": "",
        "text": "our framework is designed to address the \"few-shot, many-task\" nature of ARC."
      }
    ]
  },
  {
    "unit_id": "U004",
    "location": "Figure 2",
    "kind": "table_fig",
    "source_chunk": 1,
    "span_range": [
      55,
      55
    ],
    "node_count": 2,
    "category_counts": {
      "context": 1,
      "pattern": 1
    },
    "has_pattern": true,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C35",
        "label": "context",
        "source_span": "S55",
        "parent": null,
        "note": "",
        "text": "VARC"
      },
      {
        "node_id": "P16",
        "label": "pattern",
        "source_span": "S55",
        "parent": null,
        "note": "",
        "text": "correctly solves these challenging tasks.",
        "pattern_class": "primary_result"
      }
    ]
  },
  {
    "unit_id": "U005",
    "location": "Section 3.1",
    "kind": "section",
    "source_chunk": 1,
    "span_range": [
      57,
      77
    ],
    "node_count": 20,
    "category_counts": {
      "assumption": 2,
      "mechanism": 1,
      "context": 16,
      "intervention": 1
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C37",
        "label": "context",
        "source_span": "S57",
        "parent": null,
        "note": "",
        "text": "The ARC benchmark consists of several hundred very few-shot (e.g., 2 to 4-shot) reasoning tasks."
      },
      {
        "node_id": "C38",
        "label": "context",
        "source_span": "S58",
        "parent": null,
        "note": "",
        "text": "Each task, denoted by T, involves a unique underlying transformation rule, mapping from an input x to an output y."
      },
      {
        "node_id": "C39",
        "label": "context",
        "source_span": "S59",
        "parent": null,
        "note": "maximum size 30x30, C=10",
        "text": "x and y are both 2D grids with maximum size 30×30, in which each location has one of C different color indexes (e.g., C=10)."
      },
      {
        "node_id": "C45",
        "label": "context",
        "source_span": "S64",
        "parent": null,
        "note": "",
        "text": "Each task includes a few demonstration examples."
      },
      {
        "node_id": "C46",
        "label": "context",
        "source_span": "S65",
        "parent": null,
        "note": "",
        "text": "For a demonstration pair (x, y), both x and y are known to the model."
      },
      {
        "node_id": "C47",
        "label": "context",
        "source_span": "S66",
        "parent": null,
        "note": "m is 2 to 4",
        "text": "demonstration set of task T as: Demo={(xi, Yi)}=1, where m is the number of pairs (e.g., m is 2 to 4)."
      },
      {
        "node_id": "C48",
        "label": "context",
        "source_span": "S67",
        "parent": null,
        "note": "n is 1 or 2",
        "text": "Each task T also contains a few inference examples, denoted as: Dinfer={(xi, Yi)}=1 (n is 1 or 2)."
      },
      {
        "node_id": "C49",
        "label": "context",
        "source_span": "S68",
        "parent": null,
        "note": "",
        "text": "At inference time, only the demo pairs Demo and one input Xinfer ∈ Dinfer are given"
      },
      {
        "node_id": "A4",
        "label": "assumption",
        "source_span": "S68",
        "parent": null,
        "note": "",
        "text": "the model is required to infer the desired output Yinfer."
      },
      {
        "node_id": "C50",
        "label": "context",
        "source_span": "S69",
        "parent": null,
        "note": "",
        "text": "The training set consists of multiple tasks used to train the model offline (i.e., before a new task is given)."
      },
      {
        "node_id": "C51",
        "label": "context",
        "source_span": "S70",
        "parent": null,
        "note": "k is 400",
        "text": "training set as: Ttrain={T}=1, where k is the number of tasks (400 in ARC-1)."
      },
      {
        "node_id": "C52",
        "label": "context",
        "source_span": "S71",
        "parent": null,
        "note": "",
        "text": "samples in Demo for any T∈ Ttrain can be used for training."
      },
      {
        "node_id": "C53",
        "label": "context",
        "source_span": "S72",
        "parent": null,
        "note": "",
        "text": "The \"inference\" samples in the training set, that is, Dinfer for any task T∈ Ttrain, are used for validating the training process only."
      },
      {
        "node_id": "C54",
        "label": "context",
        "source_span": "S73",
        "parent": null,
        "note": "",
        "text": "The test set is a collection of new tasks, which are not seen during offline training."
      },
      {
        "node_id": "C55",
        "label": "context",
        "source_span": "S74",
        "parent": null,
        "note": "",
        "text": "test set as: Ttest={T}=1, with l different test tasks."
      },
      {
        "node_id": "C56",
        "label": "context",
        "source_span": "S75",
        "parent": null,
        "note": "",
        "text": "any test task is a \"complete\" and new task"
      },
      {
        "node_id": "C57",
        "label": "context",
        "source_span": "S75",
        "parent": null,
        "note": "",
        "text": "for any T∈ Ttest, there also exists a demo set Demo and the pairs (x, y) in Demo are given to the model at inference time."
      },
      {
        "node_id": "A5",
        "label": "assumption",
        "source_span": "S76",
        "parent": null,
        "note": "",
        "text": "The model should make use of Demo to infer the output of the given Xinfer for this new task."
      },
      {
        "node_id": "M15",
        "label": "mechanism",
        "source_span": "S77",
        "parent": null,
        "note": "",
        "text": "The presence of new (x, y) pairs in Demo at inference time allows to perform test-time training [49, 1, 9, 24]"
      },
      {
        "node_id": "I16",
        "label": "intervention",
        "source_span": "S77",
        "parent": null,
        "note": "",
        "text": "perform test-time training [49, 1, 9, 24]"
      }
    ]
  },
  {
    "unit_id": "U006",
    "location": "Figure 3",
    "kind": "table_fig",
    "source_chunk": 1,
    "span_range": [
      60,
      63
    ],
    "node_count": 6,
    "category_counts": {
      "assumption": 1,
      "context": 5
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C40",
        "label": "context",
        "source_span": "S60",
        "parent": null,
        "note": "",
        "text": "ARC is a collection of many different tasks."
      },
      {
        "node_id": "C41",
        "label": "context",
        "source_span": "S61",
        "parent": null,
        "note": "2-4 examples",
        "text": "For each task, a few (e.g., 2-4) demonstration pairs (x, y) are given"
      },
      {
        "node_id": "A3",
        "label": "assumption",
        "source_span": "S61",
        "parent": null,
        "note": "",
        "text": "the model is required to infer the output from Xinfer."
      },
      {
        "node_id": "C42",
        "label": "context",
        "source_span": "S62",
        "parent": null,
        "note": "400 tasks",
        "text": "The training set Ttrain is a collection of 400 tasks, which can be used for model training."
      },
      {
        "node_id": "C43",
        "label": "context",
        "source_span": "S63",
        "parent": null,
        "note": "400 new tasks",
        "text": "The test set Ttest contains 400 new tasks"
      },
      {
        "node_id": "C44",
        "label": "context",
        "source_span": "S63",
        "parent": null,
        "note": "",
        "text": "the demo pairs of a new task are given only at inference time, based on which the model performs inference on Xinfer."
      }
    ]
  },
  {
    "unit_id": "U007",
    "location": "Section 3.2",
    "kind": "section",
    "source_chunk": 1,
    "span_range": [
      78,
      85
    ],
    "node_count": 9,
    "category_counts": {
      "context": 4,
      "intervention": 3,
      "eval_metric": 2
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "I17",
        "label": "intervention",
        "source_span": "S78",
        "parent": null,
        "note": "",
        "text": "formulate reasoning on each task as an image-to-image translation problem."
      },
      {
        "node_id": "I18",
        "label": "intervention",
        "source_span": "S79",
        "parent": null,
        "note": "",
        "text": "frame the problem as per-pixel classification"
      },
      {
        "node_id": "C58",
        "label": "context",
        "source_span": "S79",
        "parent": null,
        "note": "",
        "text": "analogous to the semantic segmentation problem [38]."
      },
      {
        "node_id": "C59",
        "label": "context",
        "source_span": "S80",
        "parent": null,
        "note": "",
        "text": "learn a neural network fe parameterized by 0."
      },
      {
        "node_id": "C60",
        "label": "context",
        "source_span": "S81",
        "parent": null,
        "note": "",
        "text": "The network fe takes an image xi as input, conditioned on a task token associated with the task T."
      },
      {
        "node_id": "I19",
        "label": "intervention",
        "source_span": "S82",
        "parent": null,
        "note": "",
        "text": "The task token is represented as a learnable embedding dependent on T."
      },
      {
        "node_id": "C61",
        "label": "context",
        "source_span": "S83",
        "parent": null,
        "note": "",
        "text": "The output of fe is a grid where each position represents a categorical distribution."
      },
      {
        "node_id": "E3",
        "label": "eval_metric",
        "source_span": "S84",
        "parent": null,
        "note": "",
        "text": "the per-pixel cross-entropy loss [38]"
      },
      {
        "node_id": "E4",
        "label": "eval_metric",
        "source_span": "S85",
        "parent": null,
        "note": "",
        "text": "D denotes the per-pixel cross-entropy loss between the ground-truth yi and the network output."
      }
    ]
  },
  {
    "unit_id": "U008",
    "location": "Section 3.3",
    "kind": "section",
    "source_chunk": 1,
    "span_range": [
      86,
      122
    ],
    "node_count": 39,
    "category_counts": {
      "assumption": 2,
      "mechanism": 11,
      "context": 12,
      "intervention": 14
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C62",
        "label": "context",
        "source_span": "S86",
        "parent": null,
        "note": "",
        "text": "Previous methods on ARC generally operate in the space of discrete-valued tokens, motivated by the design of language models."
      },
      {
        "node_id": "I20",
        "label": "intervention",
        "source_span": "S87",
        "parent": null,
        "note": "",
        "text": "explore native designs developed for vision."
      },
      {
        "node_id": "I21",
        "label": "intervention",
        "source_span": "S88",
        "parent": null,
        "note": "",
        "text": "propose more flexible transformations to represent it in a manner similar to natural images."
      },
      {
        "node_id": "I22",
        "label": "intervention",
        "source_span": "S89",
        "parent": null,
        "note": "",
        "text": "define the concept of a \"canvas\"."
      },
      {
        "node_id": "C63",
        "label": "context",
        "source_span": "S90",
        "parent": null,
        "note": "64x64",
        "text": "A canvas has a predefined and sufficiently large size, e.g., 64×64."
      },
      {
        "node_id": "I23",
        "label": "intervention",
        "source_span": "S91",
        "parent": null,
        "note": "",
        "text": "The raw input is transformed and placed onto this canvas."
      },
      {
        "node_id": "M16",
        "label": "mechanism",
        "source_span": "S92",
        "parent": null,
        "note": "",
        "text": "This formulation naturally accommodates translation and scale augmentations, which are common strategies for introducing translation and scale invariance in vision"
      },
      {
        "node_id": "I24",
        "label": "intervention",
        "source_span": "S93",
        "parent": null,
        "note": "",
        "text": "set the background of the canvas to an additional background color, i.e., the (C+1)-th color."
      },
      {
        "node_id": "C64",
        "label": "context",
        "source_span": "S94",
        "parent": null,
        "note": "",
        "text": "if we naïvely treat each raw pixel as a token, there would be only C distinct tokens."
      },
      {
        "node_id": "M17",
        "label": "mechanism",
        "source_span": "S95",
        "parent": null,
        "note": "",
        "text": "our canvas formulation supports a much larger set of local, patch-level configurations."
      },
      {
        "node_id": "C65",
        "label": "context",
        "source_span": "S96",
        "parent": null,
        "note": "patch size 2x2, O(C^(2x2))",
        "text": "with a patch size of 2×2 (see Fig. 5), a single patch can contain multiple colors and, in principle, has an exponentially large cardinality, O(C2×2)."
      },
      {
        "node_id": "M18",
        "label": "mechanism",
        "source_span": "S97",
        "parent": null,
        "note": "",
        "text": "This formulation is important for improving generalization performance."
      },
      {
        "node_id": "M19",
        "label": "mechanism",
        "source_span": "S98",
        "parent": null,
        "note": "",
        "text": "The “canvas\" concept enables us to flexibly apply translation and scale augmen-tations, which are critical in standard vision models."
      },
      {
        "node_id": "M20",
        "label": "mechanism",
        "source_span": "S99",
        "parent": null,
        "note": "",
        "text": "These data augmentations encourage the model to learn un-derlying mappings invariant to geometric transformations grounded in the visual world."
      },
      {
        "node_id": "I25",
        "label": "intervention",
        "source_span": "S100",
        "parent": null,
        "note": "",
        "text": "randomly resize it by an integer scaling ratio s, duplicating each raw pixel into s×s (see Fig. 4, left)."
      },
      {
        "node_id": "C66",
        "label": "context",
        "source_span": "S101",
        "parent": null,
        "note": "",
        "text": "This is analogous to nearest-neighbor interpolation in natural im-ages."
      },
      {
        "node_id": "A6",
        "label": "assumption",
        "source_span": "S102",
        "parent": null,
        "note": "",
        "text": "“colors” in ARC do not cor-respond to real-world colors"
      },
      {
        "node_id": "M21",
        "label": "mechanism",
        "source_span": "S102",
        "parent": null,
        "note": "",
        "text": "it is not meaningful to perform other interpolations (such as bilinear)."
      },
      {
        "node_id": "I26",
        "label": "intervention",
        "source_span": "S103",
        "parent": null,
        "note": "",
        "text": "randomly place it on the fixed-size canvas."
      },
      {
        "node_id": "A7",
        "label": "assumption",
        "source_span": "S104",
        "parent": null,
        "note": "",
        "text": "We ensure all pixels are visibile."
      },
      {
        "node_id": "M22",
        "label": "mechanism",
        "source_span": "S105",
        "parent": null,
        "note": "",
        "text": "these visual priors are important for generalization to unseen tasks."
      },
      {
        "node_id": "I27",
        "label": "intervention",
        "source_span": "S106",
        "parent": null,
        "note": "",
        "text": "perform image-to-image translation by a standard vision model."
      },
      {
        "node_id": "C67",
        "label": "context",
        "source_span": "S107",
        "parent": null,
        "note": "",
        "text": "By default, we use a ViT [17]."
      },
      {
        "node_id": "C68",
        "label": "context",
        "source_span": "S108",
        "parent": null,
        "note": "",
        "text": "The principle of ViT is Transformer on patches."
      },
      {
        "node_id": "I28",
        "label": "intervention",
        "source_span": "S109",
        "parent": null,
        "note": "patch size 2x2",
        "text": "the input canvas is divided into non-overlapping patches (e.g., 2×2), projected by a linear embedding, added with positional embedding [52], and processed by a stack of Transformer blocks [52]."
      },
      {
        "node_id": "I29",
        "label": "intervention",
        "source_span": "S110",
        "parent": null,
        "note": "",
        "text": "The model has a linear projec-tion layer as the output, which performs per-pixel classifica-tion for each patch."
      },
      {
        "node_id": "C69",
        "label": "context",
        "source_span": "S111",
        "parent": null,
        "note": "",
        "text": "unlike natural images where each raw pixel has continuous values, in our case, the raw pixels have discrete values."
      },
      {
        "node_id": "I30",
        "label": "intervention",
        "source_span": "S112",
        "parent": null,
        "note": "",
        "text": "before patchifica-tion, we first map each pixel's discrete index into a learnable continuous-valued embedding."
      },
      {
        "node_id": "C70",
        "label": "context",
        "source_span": "S113",
        "parent": null,
        "note": "",
        "text": "patchification can be viewed as a special form of convolution."
      },
      {
        "node_id": "M23",
        "label": "mechanism",
        "source_span": "S114",
        "parent": null,
        "note": "",
        "text": "it incorporates sev-eral critical inductive biases in vision: most notably, local-ity (i.e., grouping nearby pixels) and translation invariance (i.e., weight sharing across locations)."
      },
      {
        "node_id": "C71",
        "label": "context",
        "source_span": "S115",
        "parent": null,
        "note": "",
        "text": "Unlike language data, which is generally modeled as 1D sequences, images are inherently 2D."
      },
      {
        "node_id": "M24",
        "label": "mechanism",
        "source_span": "S116",
        "parent": null,
        "note": "",
        "text": "This 2D structure can be lost if we naïvely treat the embedded patches as a 1D sequence."
      },
      {
        "node_id": "M25",
        "label": "mechanism",
        "source_span": "S117",
        "parent": null,
        "note": "",
        "text": "explicitly modeling positions in 2D is essential."
      },
      {
        "node_id": "I31",
        "label": "intervention",
        "source_span": "S118",
        "parent": null,
        "note": "",
        "text": "adopt separable 2D positional embed-dings, following [11]: with D channels for positional em-beddings, we use the first half of the channels to embed the horizontal coordinate and the second half to embed the vertical coordinate."
      },
      {
        "node_id": "C72",
        "label": "context",
        "source_span": "S119",
        "parent": null,
        "note": "",
        "text": "This can be applied both to additive po-sitional embeddings for encoding absolute positions and to the encoding of relative positions (e.g., RoPE [48])."
      },
      {
        "node_id": "I32",
        "label": "intervention",
        "source_span": "S120",
        "parent": null,
        "note": "",
        "text": "study the more classical vision-based architecture, i.e., convolutional neural networks [30]."
      },
      {
        "node_id": "I33",
        "label": "intervention",
        "source_span": "S121",
        "parent": null,
        "note": "",
        "text": "adopt the U-Net model [46], a hierarchical convolutional network."
      },
      {
        "node_id": "C73",
        "label": "context",
        "source_span": "S122",
        "parent": null,
        "note": "",
        "text": "The original U-Net was proposed precisely for the image-to-image translation problem of segmentation [46]"
      },
      {
        "node_id": "M26",
        "label": "mechanism",
        "source_span": "S122",
        "parent": null,
        "note": "",
        "text": "making it a natural candidate for the problem we consider."
      }
    ]
  },
  {
    "unit_id": "U009",
    "location": "Figure 4",
    "kind": "table_fig",
    "source_chunk": 1,
    "span_range": [
      123,
      123
    ],
    "node_count": 1,
    "category_counts": {
      "intervention": 1
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "I34",
        "label": "intervention",
        "source_span": "S123",
        "parent": null,
        "note": "",
        "text": "The raw input undergoes random scale and translation transformations and is placed on the \"canvas\" (denoted in gray)."
      }
    ]
  },
  {
    "unit_id": "U010",
    "location": "Figure 5",
    "kind": "table_fig",
    "source_chunk": 1,
    "span_range": [
      124,
      125
    ],
    "node_count": 2,
    "category_counts": {
      "context": 1,
      "intervention": 1
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C74",
        "label": "context",
        "source_span": "S124",
        "parent": null,
        "note": "",
        "text": "The ViT architecture in VARC."
      },
      {
        "node_id": "I35",
        "label": "intervention",
        "source_span": "S125",
        "parent": null,
        "note": "",
        "text": "The input is randomly placed on a canvas, which is then treated as a natural image and processed by a standard ViT, conditioned on the task token."
      }
    ]
  },
  {
    "unit_id": "U011",
    "location": "Section 3.4",
    "kind": "section",
    "source_chunk": 1,
    "span_range": [
      126,
      132
    ],
    "node_count": 7,
    "category_counts": {
      "context": 4,
      "intervention": 3
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "I36",
        "label": "intervention",
        "source_span": "S126",
        "parent": null,
        "note": "",
        "text": "adopt a two-stage training paradigm to learn the param-eters of the neural network."
      },
      {
        "node_id": "C75",
        "label": "context",
        "source_span": "S127",
        "parent": null,
        "note": "",
        "text": "This stage is applied on the entire train-ing set Ttrain."
      },
      {
        "node_id": "C76",
        "label": "context",
        "source_span": "S128",
        "parent": null,
        "note": "",
        "text": "It is on all demos Demo for any T∈ Ttrain."
      },
      {
        "node_id": "I37",
        "label": "intervention",
        "source_span": "S129",
        "parent": null,
        "note": "k=400",
        "text": "train one model fe jointly for all k training tasks (e.g., k=400), based on the loss in Eq. (1)."
      },
      {
        "node_id": "C77",
        "label": "context",
        "source_span": "S130",
        "parent": null,
        "note": "",
        "text": "All tasks share the same parameters, only except that each task has its own task-conditional token."
      },
      {
        "node_id": "I38",
        "label": "intervention",
        "source_span": "S131",
        "parent": null,
        "note": "",
        "text": "do not use the inference set Dinfer from the training tasks (i.e., T∈ Ttrain) to train the model."
      },
      {
        "node_id": "C78",
        "label": "context",
        "source_span": "S132",
        "parent": null,
        "note": "",
        "text": "These sets are used only for validation purposes."
      }
    ]
  },
  {
    "unit_id": "U012",
    "location": "Section 3.5",
    "kind": "section",
    "source_chunk": 2,
    "span_range": [
      133,
      158
    ],
    "node_count": 28,
    "category_counts": {
      "assumption": 4,
      "mechanism": 3,
      "context": 16,
      "intervention": 4,
      "pattern": 1
    },
    "has_pattern": true,
    "parent_subgroups": [
      {
        "parent": "S146",
        "node_ids": [
          "A8",
          "I40"
        ]
      },
      {
        "parent": "S148",
        "node_ids": [
          "A9",
          "P18"
        ]
      },
      {
        "parent": "S154",
        "node_ids": [
          "A10",
          "M29"
        ]
      },
      {
        "parent": "S157",
        "node_ids": [
          "I42",
          "M30",
          "C93"
        ]
      },
      {
        "parent": "S158",
        "node_ids": [
          "A11",
          "C94"
        ]
      }
    ],
    "nodes": [
      {
        "node_id": "C79",
        "label": "context",
        "source_span": "S133",
        "parent": null,
        "note": "",
        "text": "nearly free to use many views."
      },
      {
        "node_id": "C80",
        "label": "context",
        "source_span": "S134",
        "parent": null,
        "note": "",
        "text": "We use 510 random views"
      },
      {
        "node_id": "M27",
        "label": "mechanism",
        "source_span": "S135",
        "parent": null,
        "note": "",
        "text": "Predictions from different views are consolidated by majority voting [1]."
      },
      {
        "node_id": "C81",
        "label": "context",
        "source_span": "S140",
        "parent": null,
        "note": "",
        "text": "Test-time training (TTT)."
      },
      {
        "node_id": "C82",
        "label": "context",
        "source_span": "S141",
        "parent": null,
        "note": "",
        "text": "Given a single new, unseen task T∈ Ttest from the test set, we perform inference by test-time training."
      },
      {
        "node_id": "C83",
        "label": "context",
        "source_span": "S142",
        "parent": null,
        "note": "",
        "text": "At inference time, we are given Demo={(xi, Yi)}m=1 with both input and output accessible; the model is required to make prediction for a given Xinfer in this new task T."
      },
      {
        "node_id": "C84",
        "label": "context",
        "source_span": "S143",
        "parent": null,
        "note": "",
        "text": "The test-time training followed by inference can be viewed abstractly as a function F(Xinfer | Demo)→ Yinfer."
      },
      {
        "node_id": "I39",
        "label": "intervention",
        "source_span": "S144",
        "parent": null,
        "note": "",
        "text": "We perform test-time training for each new task T independently."
      },
      {
        "node_id": "C85",
        "label": "context",
        "source_span": "S145",
        "parent": null,
        "note": "",
        "text": "It has a new task token whose parameters are randomly initialized."
      },
      {
        "node_id": "A8",
        "label": "assumption",
        "source_span": "S146",
        "parent": "S146",
        "note": "",
        "text": "As there are very few demo pairs in Demo (e.g., 2 to 4)"
      },
      {
        "node_id": "I40",
        "label": "intervention",
        "source_span": "S146",
        "parent": "S146",
        "note": "",
        "text": "we also perform data augmentation."
      },
      {
        "node_id": "C86",
        "label": "context",
        "source_span": "S147",
        "parent": null,
        "note": "",
        "text": "at inference time, the model is initialized from offline training, fine-tuned with test-time training only for the single new task T, and then performs inference on Xinfer."
      },
      {
        "node_id": "A9",
        "label": "assumption",
        "source_span": "S148",
        "parent": "S148",
        "note": "",
        "text": "As the new demo pairs in Demo are very few"
      },
      {
        "node_id": "P18",
        "label": "pattern",
        "source_span": "S148",
        "parent": "S148",
        "note": "e.g., 70 seconds per task on a single GPU",
        "text": "this test-time training process remains reasonably fast",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "C87",
        "label": "context",
        "source_span": "S149",
        "parent": null,
        "note": "",
        "text": "After test-time training, we apply fe to Xinfer to obtain the final prediction."
      },
      {
        "node_id": "C88",
        "label": "context",
        "source_span": "S150",
        "parent": null,
        "note": "",
        "text": "This process is analogous to the classical recognition problems [29, 38]."
      },
      {
        "node_id": "I41",
        "label": "intervention",
        "source_span": "S151",
        "parent": null,
        "note": "",
        "text": "we adopt post-processing strategies inspired by recognition methods."
      },
      {
        "node_id": "C89",
        "label": "context",
        "source_span": "S152",
        "parent": null,
        "note": "",
        "text": "Single-view inference."
      },
      {
        "node_id": "C90",
        "label": "context",
        "source_span": "S153",
        "parent": null,
        "note": "",
        "text": "Given Xinfer and a single \"view\" (i.e., with a given scale and translation), we place Xinfer on the canvas and apply fe to predict the output."
      },
      {
        "node_id": "A10",
        "label": "assumption",
        "source_span": "S154",
        "parent": "S154",
        "note": "",
        "text": "Since one output location in the raw grid may be predicted by multi-ple pixels on the canvas (e.g., due to rescaling; see Fig. 5)"
      },
      {
        "node_id": "M29",
        "label": "mechanism",
        "source_span": "S154",
        "parent": "S154",
        "note": "",
        "text": "we aggregate all predictions (from softmax outputs) at this location by average pooling."
      },
      {
        "node_id": "C91",
        "label": "context",
        "source_span": "S155",
        "parent": null,
        "note": "",
        "text": "Multi-view inference."
      },
      {
        "node_id": "C92",
        "label": "context",
        "source_span": "S156",
        "parent": null,
        "note": "",
        "text": "It was a common practice to consolidate the predictions from multiple views (e.g., see AlexNet [29])."
      },
      {
        "node_id": "I42",
        "label": "intervention",
        "source_span": "S157",
        "parent": "S157",
        "note": "",
        "text": "we adopt multi-view inference"
      },
      {
        "node_id": "M30",
        "label": "mechanism",
        "source_span": "S157",
        "parent": "S157",
        "note": "",
        "text": "to im-prove accuracy"
      },
      {
        "node_id": "C93",
        "label": "context",
        "source_span": "S157",
        "parent": "S157",
        "note": "",
        "text": "the views are sampled with different augmentations."
      },
      {
        "node_id": "A11",
        "label": "assumption",
        "source_span": "S158",
        "parent": "S158",
        "note": "",
        "text": "As the multi-view inference cost is negli-gible compared with test-time training cost"
      },
      {
        "node_id": "C94",
        "label": "context",
        "source_span": "S158",
        "parent": "S158",
        "note": "",
        "text": "it is virtually nearly free to use many views."
      }
    ]
  },
  {
    "unit_id": "U013",
    "location": "Section 4",
    "kind": "section",
    "source_chunk": 2,
    "span_range": [
      136,
      174
    ],
    "node_count": 21,
    "category_counts": {
      "assumption": 1,
      "mechanism": 2,
      "context": 11,
      "intervention": 5,
      "eval_metric": 2
    },
    "has_pattern": false,
    "parent_subgroups": [
      {
        "parent": "S171",
        "node_ids": [
          "M31",
          "I45"
        ]
      },
      {
        "parent": "S174",
        "node_ids": [
          "I47",
          "A12"
        ]
      }
    ],
    "nodes": [
      {
        "node_id": "E5",
        "label": "eval_metric",
        "source_span": "S136",
        "parent": null,
        "note": "",
        "text": "Pass@2 accuracy."
      },
      {
        "node_id": "E6",
        "label": "eval_metric",
        "source_span": "S137",
        "parent": null,
        "note": "",
        "text": "the pass@2 accuracy metric: i.e., two different solutions can be produced for evaluation, and a task is considered correct if one is correct."
      },
      {
        "node_id": "M28",
        "label": "mechanism",
        "source_span": "S138",
        "parent": null,
        "note": "",
        "text": "we adopt majority voting in multi-view inference and retain the top-2 most populated output solutions."
      },
      {
        "node_id": "C95",
        "label": "context",
        "source_span": "S159",
        "parent": null,
        "note": "",
        "text": "Canvas."
      },
      {
        "node_id": "C96",
        "label": "context",
        "source_span": "S160",
        "parent": null,
        "note": "",
        "text": "the canvas size is 64×64."
      },
      {
        "node_id": "C97",
        "label": "context",
        "source_span": "S161",
        "parent": null,
        "note": "",
        "text": "In the case of ViT, the patch size is 2×2, resulting in a sequence length of 322."
      },
      {
        "node_id": "C98",
        "label": "context",
        "source_span": "S162",
        "parent": null,
        "note": "",
        "text": "an in-teger scaling ratio is randomly sampled, such that the scaled grid is no larger than the canvas size."
      },
      {
        "node_id": "C99",
        "label": "context",
        "source_span": "S163",
        "parent": null,
        "note": "",
        "text": "the upper-left corner is randomly sampled under the constraint that the placed image is fully visible."
      },
      {
        "node_id": "C100",
        "label": "context",
        "source_span": "S164",
        "parent": null,
        "note": "",
        "text": "Offline training."
      },
      {
        "node_id": "C101",
        "label": "context",
        "source_span": "S165",
        "parent": null,
        "note": "",
        "text": "We use the standard ARC-1 training set Ttrain for training: it has 400 tasks with 2-4 demo pairs each."
      },
      {
        "node_id": "I43",
        "label": "intervention",
        "source_span": "S166",
        "parent": null,
        "note": "",
        "text": "we also expand our training set with the RE-ARC set [22], from which we sam-ple 1,000 additional demo pairs per task."
      },
      {
        "node_id": "C102",
        "label": "context",
        "source_span": "S167",
        "parent": null,
        "note": "",
        "text": "our full training set has about 400k sample pairs."
      },
      {
        "node_id": "I44",
        "label": "intervention",
        "source_span": "S168",
        "parent": null,
        "note": "",
        "text": "We apply translation and scale augmentation in offline training."
      },
      {
        "node_id": "C103",
        "label": "context",
        "source_span": "S169",
        "parent": null,
        "note": "",
        "text": "Test-time training."
      },
      {
        "node_id": "C104",
        "label": "context",
        "source_span": "S170",
        "parent": null,
        "note": "",
        "text": "Given an unseen task T∈ Ttest, we have 2-4 sample pairs in Demo."
      },
      {
        "node_id": "M31",
        "label": "mechanism",
        "source_span": "S171",
        "parent": "S171",
        "note": "",
        "text": "To make test-time training more feasible"
      },
      {
        "node_id": "I45",
        "label": "intervention",
        "source_span": "S171",
        "parent": "S171",
        "note": "",
        "text": "we also augment the single task T into mul-tiple auxiliary tasks."
      },
      {
        "node_id": "I46",
        "label": "intervention",
        "source_span": "S172",
        "parent": null,
        "note": "",
        "text": "We do this by using standard augmen-tation from existing ARC methods: flip, rotation (by 90°, 180°, or 270°), and color permutation."
      },
      {
        "node_id": "C105",
        "label": "context",
        "source_span": "S173",
        "parent": null,
        "note": "",
        "text": "We treat each of these test-time training augmentations as an auxiliary task, each assigned a task embedding."
      },
      {
        "node_id": "I47",
        "label": "intervention",
        "source_span": "S174",
        "parent": "S174",
        "note": "",
        "text": "We also apply translation and scale augmentation in test-time training"
      },
      {
        "node_id": "A12",
        "label": "assumption",
        "source_span": "S174",
        "parent": "S174",
        "note": "",
        "text": "under the assumption that all auxiliary tasks are translation and scale invariant"
      }
    ]
  },
  {
    "unit_id": "U014",
    "location": "Figure 6",
    "kind": "table_fig",
    "source_chunk": 2,
    "span_range": [
      139,
      139
    ],
    "node_count": 1,
    "category_counts": {
      "pattern": 1
    },
    "has_pattern": true,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "P17",
        "label": "pattern",
        "source_span": "S139",
        "parent": null,
        "note": "",
        "text": "During test-time training, the prediction from Xinfer becomes progressively more accurate, with the model finally generating the correct prediction.",
        "pattern_class": "primary_result"
      }
    ]
  },
  {
    "unit_id": "U015",
    "location": "Section 5",
    "kind": "section",
    "source_chunk": 2,
    "span_range": [
      175,
      180
    ],
    "node_count": 7,
    "category_counts": {
      "mechanism": 1,
      "context": 4,
      "intervention": 1,
      "eval_metric": 1
    },
    "has_pattern": false,
    "parent_subgroups": [
      {
        "parent": "S177",
        "node_ids": [
          "M32",
          "I48"
        ]
      }
    ],
    "nodes": [
      {
        "node_id": "C106",
        "label": "context",
        "source_span": "S175",
        "parent": null,
        "note": "",
        "text": "Our experiments are primarily conducted on the benchmark of ARC-1 [12]."
      },
      {
        "node_id": "E7",
        "label": "eval_metric",
        "source_span": "S176",
        "parent": null,
        "note": "",
        "text": "the pass@2 accuracy (referred to simply as \"accuracy” hereafter) in percentage (%)."
      },
      {
        "node_id": "M32",
        "label": "mechanism",
        "source_span": "S177",
        "parent": "S177",
        "note": "",
        "text": "To support pass@2 evaluation"
      },
      {
        "node_id": "I48",
        "label": "intervention",
        "source_span": "S177",
        "parent": "S177",
        "note": "",
        "text": "we adopt multi-view inference."
      },
      {
        "node_id": "C107",
        "label": "context",
        "source_span": "S178",
        "parent": null,
        "note": "",
        "text": "We also report final results on ARC-2 [14]."
      },
      {
        "node_id": "C108",
        "label": "context",
        "source_span": "S179",
        "parent": null,
        "note": "",
        "text": "We evaluate our model on the ARC-1 evaluation set (i.e., Teval)."
      },
      {
        "node_id": "C109",
        "label": "context",
        "source_span": "S180",
        "parent": null,
        "note": "",
        "text": "This set is conceptually a test set (see Fig. 3), but with ground truth available only for computing accuracy."
      }
    ]
  },
  {
    "unit_id": "U016",
    "location": "Footnote 2",
    "kind": "section",
    "source_chunk": 2,
    "span_range": [
      181,
      182
    ],
    "node_count": 2,
    "category_counts": {
      "assumption": 1,
      "mechanism": 1
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "A13",
        "label": "assumption",
        "source_span": "S181",
        "parent": null,
        "note": "",
        "text": "In majority voting, two output grids are considered \"consistent” only when they are identical across the entire grid."
      },
      {
        "node_id": "M33",
        "label": "mechanism",
        "source_span": "S182",
        "parent": null,
        "note": "",
        "text": "The winner is the grid that is \"consistent\" with the largest number of other output grids."
      }
    ]
  },
  {
    "unit_id": "U017",
    "location": "Table 1",
    "kind": "table_fig",
    "source_chunk": 2,
    "span_range": [
      183,
      191
    ],
    "node_count": 9,
    "category_counts": {
      "context": 6,
      "intervention": 1,
      "eval_metric": 1,
      "pattern": 1
    },
    "has_pattern": true,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "I49",
        "label": "intervention",
        "source_span": "S183",
        "parent": null,
        "note": "",
        "text": "We compare variants of ViTs and U-Nets of similar sizes."
      },
      {
        "node_id": "C110",
        "label": "context",
        "source_span": "S184",
        "parent": null,
        "note": "width 384, depth 5, #params 6M, Gflops 10",
        "text": "ViT"
      },
      {
        "node_id": "C111",
        "label": "context",
        "source_span": "S185",
        "parent": null,
        "note": "width 512, depth 10, #params 18M, Gflops 28",
        "text": "ViT"
      },
      {
        "node_id": "C112",
        "label": "context",
        "source_span": "S186",
        "parent": null,
        "note": "width 768, depth 20, #params 66M, Gflops 99",
        "text": "ViT"
      },
      {
        "node_id": "C113",
        "label": "context",
        "source_span": "S187",
        "parent": null,
        "note": "setting (a), #params 7M, Gflops 18",
        "text": "U-Net"
      },
      {
        "node_id": "C114",
        "label": "context",
        "source_span": "S188",
        "parent": null,
        "note": "setting (b), #params 17M, Gflops 33",
        "text": "U-Net"
      },
      {
        "node_id": "C115",
        "label": "context",
        "source_span": "S189",
        "parent": null,
        "note": "setting (c), #params 55M, Gflops 87",
        "text": "U-Net"
      },
      {
        "node_id": "E8",
        "label": "eval_metric",
        "source_span": "S190",
        "parent": null,
        "note": "",
        "text": "acc."
      },
      {
        "node_id": "P19",
        "label": "pattern",
        "source_span": "S191",
        "parent": null,
        "note": "ViT accuracies: 44.4, 54.5, 53.0; U-Net accuracies: 42.8, 47.5, 48.3",
        "text": "ViT models show higher accuracy than U-Net models",
        "pattern_class": "comparison"
      }
    ]
  },
  {
    "unit_id": "U018",
    "location": "Figure 7",
    "kind": "table_fig",
    "source_chunk": 2,
    "span_range": [
      192,
      198
    ],
    "node_count": 9,
    "category_counts": {
      "context": 4,
      "intervention": 2,
      "eval_metric": 1,
      "pattern": 2
    },
    "has_pattern": true,
    "parent_subgroups": [
      {
        "parent": "S193",
        "node_ids": [
          "E9",
          "C117"
        ]
      },
      {
        "parent": "S198",
        "node_ids": [
          "P20",
          "P21"
        ]
      }
    ],
    "nodes": [
      {
        "node_id": "C116",
        "label": "context",
        "source_span": "S192",
        "parent": null,
        "note": "",
        "text": "Effects of visual priors in VARC."
      },
      {
        "node_id": "E9",
        "label": "eval_metric",
        "source_span": "S193",
        "parent": "S193",
        "note": "",
        "text": "Accuracy"
      },
      {
        "node_id": "C117",
        "label": "context",
        "source_span": "S193",
        "parent": "S193",
        "note": "",
        "text": "ARC-1 evaluation set."
      },
      {
        "node_id": "C118",
        "label": "context",
        "source_span": "S194",
        "parent": null,
        "note": "",
        "text": "The model used is ViT-18M."
      },
      {
        "node_id": "I50",
        "label": "intervention",
        "source_span": "S195",
        "parent": null,
        "note": "",
        "text": "Entries (a-c) use a patch size of 1×1 on a 32×32 canvas, whereas entries (d-f) use a patch size of 2×2 on a 64×64 canvas."
      },
      {
        "node_id": "C119",
        "label": "context",
        "source_span": "S196",
        "parent": null,
        "note": "",
        "text": "Each entry modifies the one above it."
      },
      {
        "node_id": "I51",
        "label": "intervention",
        "source_span": "S197",
        "parent": null,
        "note": "",
        "text": "We start from a naïve baseline with components (b-f) removed."
      },
      {
        "node_id": "P20",
        "label": "pattern",
        "source_span": "S198",
        "parent": "S198",
        "note": "27.7 improvement",
        "text": "These vision priors cumulatively yield improvement (a→f)",
        "pattern_class": "comparison"
      },
      {
        "node_id": "P21",
        "label": "pattern",
        "source_span": "S198",
        "parent": "S198",
        "note": "11.5 gain",
        "text": "the canvas-based designs (c→f) contribute an gain.",
        "pattern_class": "comparison"
      }
    ]
  },
  {
    "unit_id": "U019",
    "location": "Section 5.1",
    "kind": "section",
    "source_chunk": 2,
    "span_range": [
      199,
      232
    ],
    "node_count": 30,
    "category_counts": {
      "assumption": 1,
      "mechanism": 4,
      "context": 8,
      "intervention": 6,
      "pattern": 11
    },
    "has_pattern": true,
    "parent_subgroups": [
      {
        "parent": "S200",
        "node_ids": [
          "P22",
          "P23"
        ]
      },
      {
        "parent": "S204",
        "node_ids": [
          "I53",
          "P25"
        ]
      },
      {
        "parent": "S213",
        "node_ids": [
          "M35",
          "I55"
        ]
      }
    ],
    "nodes": [
      {
        "node_id": "I52",
        "label": "intervention",
        "source_span": "S199",
        "parent": null,
        "note": "",
        "text": "starting from a baseline (a) without the other components in this figure."
      },
      {
        "node_id": "P22",
        "label": "pattern",
        "source_span": "S200",
        "parent": "S200",
        "note": "27.7 points",
        "text": "These priors jointly have a gain",
        "pattern_class": "comparison"
      },
      {
        "node_id": "P23",
        "label": "pattern",
        "source_span": "S200",
        "parent": "S200",
        "note": "11.5 points",
        "text": "the canvas-based designs (c–f) has a gain.",
        "pattern_class": "comparison"
      },
      {
        "node_id": "C120",
        "label": "context",
        "source_span": "S201",
        "parent": null,
        "note": "",
        "text": "2D positional embedding."
      },
      {
        "node_id": "P24",
        "label": "pattern",
        "source_span": "S202",
        "parent": null,
        "note": "",
        "text": "Extending from 1D posi-tional embedding to its 2D counterpart is beneficial",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "C121",
        "label": "context",
        "source_span": "S203",
        "parent": null,
        "note": "",
        "text": "This is observed in both (b) absolute and (c) relative positional embeddings."
      },
      {
        "node_id": "I53",
        "label": "intervention",
        "source_span": "S204",
        "parent": "S204",
        "note": "",
        "text": "we re-place the 2D ROPE in Fig. 7(f) with a 1D ROPE"
      },
      {
        "node_id": "P25",
        "label": "pattern",
        "source_span": "S204",
        "parent": "S204",
        "note": "3.5 points, from 54.5 to 51.0",
        "text": "observe a degradation",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "C122",
        "label": "context",
        "source_span": "S205",
        "parent": null,
        "note": "",
        "text": "Patchification."
      },
      {
        "node_id": "C123",
        "label": "context",
        "source_span": "S206",
        "parent": null,
        "note": "",
        "text": "A key design principle of our method is to prepare the input as a natural image."
      },
      {
        "node_id": "M34",
        "label": "mechanism",
        "source_span": "S207",
        "parent": null,
        "note": "",
        "text": "This enables the expansion of the token set from a very limited size (e.g., 10) to an exponentially large number."
      },
      {
        "node_id": "P26",
        "label": "pattern",
        "source_span": "S208",
        "parent": null,
        "note": "",
        "text": "The entries Fig. 7(d-f) all benefit from this design.",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "I54",
        "label": "intervention",
        "source_span": "S209",
        "parent": null,
        "note": "",
        "text": "we advance from 1×1 patches on a 32×32 canvas to 2×2 patches on a 64×64 canvas."
      },
      {
        "node_id": "P27",
        "label": "pattern",
        "source_span": "S210",
        "parent": null,
        "note": "",
        "text": "Doing so does not increase the computational cost of the Transformer.",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "C124",
        "label": "context",
        "source_span": "S211",
        "parent": null,
        "note": "",
        "text": "the scaling ratio is fixed as 2x."
      },
      {
        "node_id": "A14",
        "label": "assumption",
        "source_span": "S212",
        "parent": null,
        "note": "",
        "text": "if we constrain each 2×2 patch to cover only one raw pixel, it becomes equivalent to the 1×1 patch counterpart on the 32×32 canvas."
      },
      {
        "node_id": "M35",
        "label": "mechanism",
        "source_span": "S213",
        "parent": "S213",
        "note": "",
        "text": "to ensure a meaningful compar-ison"
      },
      {
        "node_id": "I55",
        "label": "intervention",
        "source_span": "S213",
        "parent": "S213",
        "note": "",
        "text": "we do not impose this constraint, allowing each 2×2 patch to cover multiple colors."
      },
      {
        "node_id": "C125",
        "label": "context",
        "source_span": "S214",
        "parent": null,
        "note": "",
        "text": "This can be interpreted as one-pixel translation augmentation on the canvas."
      },
      {
        "node_id": "P28",
        "label": "pattern",
        "source_span": "S215",
        "parent": null,
        "note": "2.4 points, improving from 43.0 to 45.4",
        "text": "the 2×2 patchification leads to a noticeable gain",
        "pattern_class": "comparison"
      },
      {
        "node_id": "M36",
        "label": "mechanism",
        "source_span": "S216",
        "parent": null,
        "note": "",
        "text": "each patch can cover multiple colors (as in natural images), which substan-tially enriches the data space for learning."
      },
      {
        "node_id": "C127",
        "label": "context",
        "source_span": "S224",
        "parent": null,
        "note": "",
        "text": "Translation and scale augmentation."
      },
      {
        "node_id": "P32",
        "label": "pattern",
        "source_span": "S225",
        "parent": null,
        "note": "",
        "text": "even highly capable network architectures still benefit greatly from translation and scale augmentations.",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "P33",
        "label": "pattern",
        "source_span": "S226",
        "parent": null,
        "note": "",
        "text": "We draw similar observations in ARC.",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "I58",
        "label": "intervention",
        "source_span": "S227",
        "parent": null,
        "note": "",
        "text": "we apply fully flexible translation augmen-tation on the canvas."
      },
      {
        "node_id": "P34",
        "label": "pattern",
        "source_span": "S228",
        "parent": null,
        "note": "2.9 points (from 45.4 to 48.3)",
        "text": "this setting yields an additional gain",
        "pattern_class": "comparison"
      },
      {
        "node_id": "I59",
        "label": "intervention",
        "source_span": "S229",
        "parent": null,
        "note": "",
        "text": "we further ap-ply the scale augmentation enabled by the concept of can-vas."
      },
      {
        "node_id": "P35",
        "label": "pattern",
        "source_span": "S230",
        "parent": null,
        "note": "6.2 points",
        "text": "Scale augmentation yields a substantial gain",
        "pattern_class": "comparison"
      },
      {
        "node_id": "C128",
        "label": "context",
        "source_span": "S231",
        "parent": null,
        "note": "",
        "text": "Unlike translation invariance, which can be partially addressed by patchification (i.e., a special form of convo-lution), the ViT architecture has little to no inductive bias about scale invariance."
      },
      {
        "node_id": "M37",
        "label": "mechanism",
        "source_span": "S232",
        "parent": null,
        "note": "",
        "text": "This can explain why scale augmen-tation yields a substantial gain."
      }
    ]
  },
  {
    "unit_id": "U020",
    "location": "Figure 8",
    "kind": "table_fig",
    "source_chunk": 2,
    "span_range": [
      217,
      219
    ],
    "node_count": 4,
    "category_counts": {
      "context": 1,
      "intervention": 1,
      "eval_metric": 1,
      "pattern": 1
    },
    "has_pattern": true,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "I56",
        "label": "intervention",
        "source_span": "S217",
        "parent": null,
        "note": "",
        "text": "ViTs with different width (x-axis) and depth."
      },
      {
        "node_id": "C126",
        "label": "context",
        "source_span": "S217",
        "parent": null,
        "note": "",
        "text": "The circle areas de-note model sizes."
      },
      {
        "node_id": "E10",
        "label": "eval_metric",
        "source_span": "S218",
        "parent": null,
        "note": "",
        "text": "Accuracy (%)"
      },
      {
        "node_id": "P29",
        "label": "pattern",
        "source_span": "S219",
        "parent": null,
        "note": "",
        "text": "increasing depth and/or width leads to higher accuracy",
        "pattern_class": "comparison"
      }
    ]
  },
  {
    "unit_id": "U021",
    "location": "Figure 9",
    "kind": "table_fig",
    "source_chunk": 2,
    "span_range": [
      220,
      223
    ],
    "node_count": 4,
    "category_counts": {
      "intervention": 1,
      "eval_metric": 1,
      "pattern": 2
    },
    "has_pattern": true,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "I57",
        "label": "intervention",
        "source_span": "S220",
        "parent": null,
        "note": "",
        "text": "with vs. without offline train-ing, and joint vs. independent for each task."
      },
      {
        "node_id": "E11",
        "label": "eval_metric",
        "source_span": "S221",
        "parent": null,
        "note": "",
        "text": "Accuracy (%)"
      },
      {
        "node_id": "P30",
        "label": "pattern",
        "source_span": "S222",
        "parent": null,
        "note": "54.5 vs 29.1",
        "text": "offline training improves performance",
        "pattern_class": "comparison"
      },
      {
        "node_id": "P31",
        "label": "pattern",
        "source_span": "S223",
        "parent": null,
        "note": "54.5 vs 26.4",
        "text": "TTT independently performs better than TTT jointly",
        "pattern_class": "comparison"
      }
    ]
  },
  {
    "unit_id": "U022",
    "location": "Section 5.2",
    "kind": "section",
    "source_chunk": 2,
    "span_range": [
      233,
      256
    ],
    "node_count": 32,
    "category_counts": {
      "assumption": 4,
      "mechanism": 5,
      "context": 8,
      "intervention": 4,
      "eval_metric": 1,
      "pattern": 10
    },
    "has_pattern": true,
    "parent_subgroups": [
      {
        "parent": "S236",
        "node_ids": [
          "P36",
          "P37",
          "M38"
        ]
      },
      {
        "parent": "S239",
        "node_ids": [
          "P38",
          "M39"
        ]
      },
      {
        "parent": "S240",
        "node_ids": [
          "A15",
          "C132"
        ]
      },
      {
        "parent": "S244",
        "node_ids": [
          "P40",
          "M40"
        ]
      },
      {
        "parent": "S245",
        "node_ids": [
          "P41",
          "M41"
        ]
      },
      {
        "parent": "S246",
        "node_ids": [
          "P42",
          "C134"
        ]
      },
      {
        "parent": "S247",
        "node_ids": [
          "P43",
          "A16"
        ]
      },
      {
        "parent": "S251",
        "node_ids": [
          "A17",
          "E12"
        ]
      },
      {
        "parent": "S255",
        "node_ids": [
          "P44",
          "P45",
          "M42"
        ]
      }
    ],
    "nodes": [
      {
        "node_id": "C129",
        "label": "context",
        "source_span": "S233",
        "parent": null,
        "note": "",
        "text": "ViT vs. U-Net."
      },
      {
        "node_id": "I60",
        "label": "intervention",
        "source_span": "S234",
        "parent": null,
        "note": "",
        "text": "we compare ViT with U-Nets, a type of convolutional network."
      },
      {
        "node_id": "C130",
        "label": "context",
        "source_span": "S235",
        "parent": null,
        "note": "",
        "text": "We evaluate three model sizes for each architecture."
      },
      {
        "node_id": "P36",
        "label": "pattern",
        "source_span": "S236",
        "parent": "S236",
        "note": "",
        "text": "ViTs consistently per-form better",
        "pattern_class": "comparison"
      },
      {
        "node_id": "P37",
        "label": "pattern",
        "source_span": "S236",
        "parent": "S236",
        "note": "",
        "text": "all U-Net variants achieve decent accuracy",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "M38",
        "label": "mechanism",
        "source_span": "S236",
        "parent": "S236",
        "note": "",
        "text": "this problem can also be effectively addressed by classical vision backbones."
      },
      {
        "node_id": "C131",
        "label": "context",
        "source_span": "S237",
        "parent": null,
        "note": "",
        "text": "Scalability."
      },
      {
        "node_id": "I61",
        "label": "intervention",
        "source_span": "S238",
        "parent": null,
        "note": "",
        "text": "we show ViTs with varying depths and widths."
      },
      {
        "node_id": "P38",
        "label": "pattern",
        "source_span": "S239",
        "parent": "S239",
        "note": "",
        "text": "our method demonstrates good scalability: increasing depth and/or width leads to higher accuracy",
        "pattern_class": "comparison"
      },
      {
        "node_id": "M39",
        "label": "mechanism",
        "source_span": "S239",
        "parent": "S239",
        "note": "",
        "text": "as a result of better fitting."
      },
      {
        "node_id": "A15",
        "label": "assumption",
        "source_span": "S240",
        "parent": "S240",
        "note": "",
        "text": "Going beyond this regime can lead to overfitting in our current setting"
      },
      {
        "node_id": "C132",
        "label": "context",
        "source_span": "S240",
        "parent": "S240",
        "note": "",
        "text": "as shown in Tab. 1 for the 66M ViT model."
      },
      {
        "node_id": "P39",
        "label": "pattern",
        "source_span": "S241",
        "parent": "S241",
        "note": "",
        "text": "this larger model achieves higher training accuracy",
        "pattern_class": "comparison"
      },
      {
        "node_id": "C133",
        "label": "context",
        "source_span": "S242",
        "parent": null,
        "note": "",
        "text": "Test-time training (TTT) strategies."
      },
      {
        "node_id": "I62",
        "label": "intervention",
        "source_span": "S243",
        "parent": null,
        "note": "",
        "text": "we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task."
      },
      {
        "node_id": "P40",
        "label": "pattern",
        "source_span": "S244",
        "parent": "S244",
        "note": "",
        "text": "offline training greatly improves the per-formance of TTT",
        "pattern_class": "comparison"
      },
      {
        "node_id": "M40",
        "label": "mechanism",
        "source_span": "S244",
        "parent": "S244",
        "note": "",
        "text": "common sense about the visual world can be learned from the training set."
      },
      {
        "node_id": "P41",
        "label": "pattern",
        "source_span": "S245",
        "parent": "S245",
        "note": "26.4",
        "text": "even without offline training, our TTT strategy can achieve nontrivial accuracy",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "M41",
        "label": "mechanism",
        "source_span": "S245",
        "parent": "S245",
        "note": "",
        "text": "some tasks in this benchmark can be solved tabula rasa."
      },
      {
        "node_id": "P42",
        "label": "pattern",
        "source_span": "S246",
        "parent": "S246",
        "note": "",
        "text": "This result outperforms that in [36]",
        "pattern_class": "comparison"
      },
      {
        "node_id": "C134",
        "label": "context",
        "source_span": "S246",
        "parent": "S246",
        "note": "",
        "text": "under a similar setting."
      },
      {
        "node_id": "P43",
        "label": "pattern",
        "source_span": "S247",
        "parent": "S247",
        "note": "by ~10 points",
        "text": "performing TTT independently for each test task yields substantially better performance than doing so jointly across all test tasks",
        "pattern_class": "comparison"
      },
      {
        "node_id": "A16",
        "label": "assumption",
        "source_span": "S247",
        "parent": "S247",
        "note": "",
        "text": "the latter relies on a stronger assumption about the availability of multiple test tasks at once."
      },
      {
        "node_id": "C135",
        "label": "context",
        "source_span": "S248",
        "parent": null,
        "note": "",
        "text": "Single-view vs. multi-view inference."
      },
      {
        "node_id": "C136",
        "label": "context",
        "source_span": "S249",
        "parent": null,
        "note": "",
        "text": "we adopt multi-view inference by default."
      },
      {
        "node_id": "I63",
        "label": "intervention",
        "source_span": "S250",
        "parent": null,
        "note": "",
        "text": "we also examine the single-view inference accuracy."
      },
      {
        "node_id": "A17",
        "label": "assumption",
        "source_span": "S251",
        "parent": "S251",
        "note": "",
        "text": "Since single-view inference cannot produce mul-tiple predictions"
      },
      {
        "node_id": "E12",
        "label": "eval_metric",
        "source_span": "S251",
        "parent": "S251",
        "note": "",
        "text": "we compare pass@1 accuracy."
      },
      {
        "node_id": "P44",
        "label": "pattern",
        "source_span": "S255",
        "parent": "S255",
        "note": "35.9",
        "text": "Single-view inference has a decent pass@1 accuracy",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "P45",
        "label": "pattern",
        "source_span": "S255",
        "parent": "S255",
        "note": "to 49.8",
        "text": "multi-view inference further boosts",
        "pattern_class": "comparison"
      },
      {
        "node_id": "M42",
        "label": "mechanism",
        "source_span": "S255",
        "parent": "S255",
        "note": "",
        "text": "thanks to majority voting."
      },
      {
        "node_id": "A18",
        "label": "assumption",
        "source_span": "S256",
        "parent": null,
        "note": "",
        "text": "in ARC, a mistake on even a single pixel renders the entire prediction incorrect."
      }
    ]
  },
  {
    "unit_id": "U023",
    "location": "Table 2",
    "kind": "table_fig",
    "source_chunk": 2,
    "span_range": [
      252,
      254
    ],
    "node_count": 3,
    "category_counts": {
      "eval_metric": 3
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "E13",
        "label": "eval_metric",
        "source_span": "S252",
        "parent": null,
        "note": "35.9",
        "text": "single-view, pass@1"
      },
      {
        "node_id": "E14",
        "label": "eval_metric",
        "source_span": "S253",
        "parent": null,
        "note": "49.8",
        "text": "multi-view, pass@1"
      },
      {
        "node_id": "E15",
        "label": "eval_metric",
        "source_span": "S254",
        "parent": null,
        "note": "54.5",
        "text": "multi-view, pass@2"
      }
    ]
  },
  {
    "unit_id": "U024",
    "location": "Section 5.3",
    "kind": "section",
    "source_chunk": 2,
    "span_range": [
      257,
      272
    ],
    "node_count": 13,
    "category_counts": {
      "context": 6,
      "intervention": 2,
      "pattern": 5
    },
    "has_pattern": true,
    "parent_subgroups": [
      {
        "parent": "S266",
        "node_ids": [
          "C143",
          "C144"
        ]
      },
      {
        "parent": "S267",
        "node_ids": [
          "C145",
          "P49"
        ]
      }
    ],
    "nodes": [
      {
        "node_id": "C137",
        "label": "context",
        "source_span": "S257",
        "parent": null,
        "note": "",
        "text": "System-level Comparisons."
      },
      {
        "node_id": "I64",
        "label": "intervention",
        "source_span": "S258",
        "parent": null,
        "note": "",
        "text": "we compare with leading results using LLMs or recurrent models, on ARC-1 and ARC-2."
      },
      {
        "node_id": "P48",
        "label": "pattern",
        "source_span": "S264",
        "parent": "S264",
        "note": "",
        "text": "Our model compares favorably with some of the most powerful LLMs at the time their results were reported: in-cluding Deepseek, Claude, o3, and GPT-5",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "C142",
        "label": "context",
        "source_span": "S265",
        "parent": null,
        "note": "",
        "text": "LLMs are pre-trained on internet-scale data, and some may also incor-porate multimodal data that include images."
      },
      {
        "node_id": "C143",
        "label": "context",
        "source_span": "S266",
        "parent": "S266",
        "note": "",
        "text": "Our method does not rely on such data"
      },
      {
        "node_id": "C144",
        "label": "context",
        "source_span": "S266",
        "parent": "S266",
        "note": "",
        "text": "uses a model that is several orders of magnitude smaller."
      },
      {
        "node_id": "C145",
        "label": "context",
        "source_span": "S267",
        "parent": "S267",
        "note": "",
        "text": "In the controlled setting of training from scratch on ARC data"
      },
      {
        "node_id": "P49",
        "label": "pattern",
        "source_span": "S267",
        "parent": "S267",
        "note": "",
        "text": "our method substantially outperforms the recur-rent models: HRM [53] and TRM [27].",
        "pattern_class": "comparison"
      },
      {
        "node_id": "P50",
        "label": "pattern",
        "source_span": "S268",
        "parent": null,
        "note": "~10 points better, a >20% relative improvement",
        "text": "Our VARC with 18M parameters is better than TRM on ARC-1",
        "pattern_class": "comparison"
      },
      {
        "node_id": "C146",
        "label": "context",
        "source_span": "S269",
        "parent": null,
        "note": "",
        "text": "once test-time training is completed, our model performs fully feedfor-ward inference, with no recurrence involved in reasoning."
      },
      {
        "node_id": "I65",
        "label": "intervention",
        "source_span": "S270",
        "parent": null,
        "note": "",
        "text": "we ensemble one ViT and one U-Net, each with test-time training run four times."
      },
      {
        "node_id": "P51",
        "label": "pattern",
        "source_span": "S271",
        "parent": null,
        "note": "to 60.4",
        "text": "Doing so boosts our result",
        "pattern_class": "comparison"
      },
      {
        "node_id": "P52",
        "label": "pattern",
        "source_span": "S272",
        "parent": null,
        "note": "60.4 vs 60.2 [31]",
        "text": "This result closes the gap with the re-ported average human performance",
        "pattern_class": "comparison"
      }
    ]
  },
  {
    "unit_id": "U025",
    "location": "Table 3",
    "kind": "table_fig",
    "source_chunk": 2,
    "span_range": [
      259,
      263
    ],
    "node_count": 8,
    "category_counts": {
      "context": 4,
      "eval_metric": 2,
      "pattern": 2
    },
    "has_pattern": true,
    "parent_subgroups": [
      {
        "parent": "S259",
        "node_ids": [
          "C138",
          "C139",
          "C140",
          "C141"
        ]
      }
    ],
    "nodes": [
      {
        "node_id": "C138",
        "label": "context",
        "source_span": "S259",
        "parent": "S259",
        "note": "",
        "text": "LLM-based results are from the ARC-AGI leader-board [18]."
      },
      {
        "node_id": "C139",
        "label": "context",
        "source_span": "S259",
        "parent": "S259",
        "note": "",
        "text": "HRM, TRM, and our VARC are trained from scratch only on ARC data."
      },
      {
        "node_id": "C140",
        "label": "context",
        "source_span": "S259",
        "parent": "S259",
        "note": "",
        "text": "Our single-model result is based on ViT, with mean±std of 54.5±0.7 (ARC-1) and 8.3±0.4 (ARC-2) over four runs."
      },
      {
        "node_id": "C141",
        "label": "context",
        "source_span": "S259",
        "parent": "S259",
        "note": "",
        "text": "Our ensemble result aggregates an 18M ViT and a 55M U-Net, each with test-time training performed four times."
      },
      {
        "node_id": "E16",
        "label": "eval_metric",
        "source_span": "S260",
        "parent": null,
        "note": "",
        "text": "ARC-1"
      },
      {
        "node_id": "E17",
        "label": "eval_metric",
        "source_span": "S261",
        "parent": null,
        "note": "",
        "text": "ARC-2"
      },
      {
        "node_id": "P46",
        "label": "pattern",
        "source_span": "S262",
        "parent": null,
        "note": "60.4, 11.1",
        "text": "VARC (ensemble) achieves 60.4 on ARC-1 and 11.1 on ARC-2",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "P47",
        "label": "pattern",
        "source_span": "S263",
        "parent": null,
        "note": "VARC 60.4, avg. human 60.2",
        "text": "VARC (ensemble) is comparable to avg. human performance on ARC-1",
        "pattern_class": "primary_result"
      }
    ]
  },
  {
    "unit_id": "U026",
    "location": "Section 6",
    "kind": "section",
    "source_chunk": 2,
    "span_range": [
      273,
      290
    ],
    "node_count": 22,
    "category_counts": {
      "mechanism": 6,
      "context": 10,
      "intervention": 1,
      "pattern": 5
    },
    "has_pattern": true,
    "parent_subgroups": [
      {
        "parent": "S279",
        "node_ids": [
          "C151",
          "M45"
        ]
      },
      {
        "parent": "S280",
        "node_ids": [
          "P53",
          "M46"
        ]
      },
      {
        "parent": "S281",
        "node_ids": [
          "P54",
          "M47"
        ]
      },
      {
        "parent": "S290",
        "node_ids": [
          "M48",
          "C156"
        ]
      }
    ],
    "nodes": [
      {
        "node_id": "C147",
        "label": "context",
        "source_span": "S273",
        "parent": null,
        "note": "",
        "text": "Visualization and Analysis."
      },
      {
        "node_id": "M43",
        "label": "mechanism",
        "source_span": "S274",
        "parent": null,
        "note": "",
        "text": "we provide additional qualita-tive results that help reveal the model's behavior."
      },
      {
        "node_id": "C148",
        "label": "context",
        "source_span": "S275",
        "parent": null,
        "note": "",
        "text": "Attention patterns."
      },
      {
        "node_id": "C149",
        "label": "context",
        "source_span": "S276",
        "parent": null,
        "note": "",
        "text": "Fig. 10 shows the attention patterns of our ViT model in a test task."
      },
      {
        "node_id": "M44",
        "label": "mechanism",
        "source_span": "S277",
        "parent": null,
        "note": "",
        "text": "These attention maps show that our model can correctly reason about the relationship between a source pixel and its target pixel to copy from."
      },
      {
        "node_id": "C150",
        "label": "context",
        "source_span": "S278",
        "parent": null,
        "note": "",
        "text": "Figure 11 visualizes the layer-wise attention maps for an-other test task."
      },
      {
        "node_id": "C151",
        "label": "context",
        "source_span": "S279",
        "parent": "S279",
        "note": "",
        "text": "A layer-wise map is the softmax attention map averaged across all pixels in the layer"
      },
      {
        "node_id": "M45",
        "label": "mechanism",
        "source_span": "S279",
        "parent": "S279",
        "note": "",
        "text": "it reveals which pixels receive the most attention in that layer."
      },
      {
        "node_id": "P53",
        "label": "pattern",
        "source_span": "S280",
        "parent": "S280",
        "note": "",
        "text": "some layers exhibit strong attention to the 3 × 3 neighborhood",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "M46",
        "label": "mechanism",
        "source_span": "S280",
        "parent": "S280",
        "note": "",
        "text": "reflecting the influence of the pattern's core."
      },
      {
        "node_id": "P54",
        "label": "pattern",
        "source_span": "S281",
        "parent": "S281",
        "note": "",
        "text": "some other layers (e.g., layers 7-9) focus on the outward-radiating rays",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "M47",
        "label": "mechanism",
        "source_span": "S281",
        "parent": "S281",
        "note": "",
        "text": "corresponding to the rule that extends colored pixels along the eight directions."
      },
      {
        "node_id": "P55",
        "label": "pattern",
        "source_span": "S282",
        "parent": null,
        "note": "",
        "text": "different layers exhibit different specialties: some layers at-tend to the pixels that are to be copied, and some layers attend to the target lines alone the eight directions.",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "C152",
        "label": "context",
        "source_span": "S283",
        "parent": null,
        "note": "",
        "text": "t-SNE of task embeddings."
      },
      {
        "node_id": "C153",
        "label": "context",
        "source_span": "S284",
        "parent": null,
        "note": "",
        "text": "Our model is conditioned on a task token, with an embedding learned to represent each task."
      },
      {
        "node_id": "C154",
        "label": "context",
        "source_span": "S285",
        "parent": null,
        "note": "",
        "text": "With 400 training tasks in ARC-1, our model learns 400 distinct task embeddings in offline training."
      },
      {
        "node_id": "I66",
        "label": "intervention",
        "source_span": "S286",
        "parent": null,
        "note": "",
        "text": "We visu-alize these 400 embeddings in the 2D space by t-SNE [39]"
      },
      {
        "node_id": "C155",
        "label": "context",
        "source_span": "S287",
        "parent": null,
        "note": "",
        "text": "Each point corresponds to a task.."
      },
      {
        "node_id": "P56",
        "label": "pattern",
        "source_span": "S288",
        "parent": null,
        "note": "",
        "text": "nearby points in the task embedding space exhibit similar semantics.",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "P57",
        "label": "pattern",
        "source_span": "S289",
        "parent": null,
        "note": "",
        "text": "the top-left corner in Fig. 12 shows two tasks related to coloring; the bottom-left corner shows two tasks related to generalized logic operations (i.e., AND/OR/XOR).",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "M48",
        "label": "mechanism",
        "source_span": "S290",
        "parent": "S290",
        "note": "",
        "text": "This vi-sualization suggests that our method attempts to learn the relations between different tasks"
      },
      {
        "node_id": "C156",
        "label": "context",
        "source_span": "S290",
        "parent": "S290",
        "note": "",
        "text": "which is an essential abil-ity for abstraction and reasoning."
      }
    ]
  },
  {
    "unit_id": "U027",
    "location": "Section 7",
    "kind": "section",
    "source_chunk": 2,
    "span_range": [
      291,
      294
    ],
    "node_count": 6,
    "category_counts": {
      "mechanism": 2,
      "context": 3,
      "pattern": 1
    },
    "has_pattern": true,
    "parent_subgroups": [
      {
        "parent": "S293",
        "node_ids": [
          "M49",
          "P58",
          "C159"
        ]
      }
    ],
    "nodes": [
      {
        "node_id": "C157",
        "label": "context",
        "source_span": "S291",
        "parent": null,
        "note": "",
        "text": "Conclusion."
      },
      {
        "node_id": "C158",
        "label": "context",
        "source_span": "S292",
        "parent": null,
        "note": "",
        "text": "Our work explores a previously overlooked perspective in the ARC task by framing it as an image-to-image translation problem."
      },
      {
        "node_id": "M49",
        "label": "mechanism",
        "source_span": "S293",
        "parent": "S293",
        "note": "",
        "text": "It naturally enables the adaptation of visual frame-works"
      },
      {
        "node_id": "P58",
        "label": "pattern",
        "source_span": "S293",
        "parent": "S293",
        "note": "",
        "text": "yields strong few-shot generalization competi-tive with recent approaches",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "C159",
        "label": "context",
        "source_span": "S293",
        "parent": "S293",
        "note": "",
        "text": "while remaining orders of mag-nitude smaller than most LLM-based models."
      },
      {
        "node_id": "M50",
        "label": "mechanism",
        "source_span": "S294",
        "parent": null,
        "note": "",
        "text": "This opens up a new possibility of treating ARC as a vision-centric prob-lem, emphasizing abstraction and reasoning emerging di-rectly from image pixels."
      }
    ]
  },
  {
    "unit_id": "U028",
    "location": "Footnote 3",
    "kind": "section",
    "source_chunk": 2,
    "span_range": [
      295,
      295
    ],
    "node_count": 1,
    "category_counts": {
      "assumption": 1
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "A19",
        "label": "assumption",
        "source_span": "S295",
        "parent": null,
        "note": "",
        "text": "it cannot be assumed that multiple unseen tasks will be presented all at once."
      }
    ]
  },
  {
    "unit_id": "U029",
    "location": "Footnote 4",
    "kind": "section",
    "source_chunk": 2,
    "span_range": [
      296,
      296
    ],
    "node_count": 1,
    "category_counts": {
      "context": 1
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C160",
        "label": "context",
        "source_span": "S296",
        "parent": null,
        "note": "",
        "text": "Our ARC-2 models are trained only on the ARC-1 dataset, with test-time training and inference on the ARC-2 set."
      }
    ]
  },
  {
    "unit_id": "U030",
    "location": "Table 4",
    "kind": "table_fig",
    "source_chunk": 3,
    "span_range": [
      297,
      310
    ],
    "node_count": 14,
    "category_counts": {
      "context": 14
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C161",
        "label": "context",
        "source_span": "S297",
        "parent": null,
        "note": "",
        "text": "optimizer Adam [28], betas=(0.9, 0.999)"
      },
      {
        "node_id": "C162",
        "label": "context",
        "source_span": "S298",
        "parent": null,
        "note": "",
        "text": "batch size 32"
      },
      {
        "node_id": "C163",
        "label": "context",
        "source_span": "S299",
        "parent": null,
        "note": "",
        "text": "learning rate 3e-4"
      },
      {
        "node_id": "C164",
        "label": "context",
        "source_span": "S300",
        "parent": null,
        "note": "",
        "text": "learning rate scheduler cosine"
      },
      {
        "node_id": "C165",
        "label": "context",
        "source_span": "S301",
        "parent": null,
        "note": "",
        "text": "weight decay 0"
      },
      {
        "node_id": "C166",
        "label": "context",
        "source_span": "S302",
        "parent": null,
        "note": "",
        "text": "dropout 0.1"
      },
      {
        "node_id": "C167",
        "label": "context",
        "source_span": "S303",
        "parent": null,
        "note": "",
        "text": "epochs 100"
      },
      {
        "node_id": "C168",
        "label": "context",
        "source_span": "S304",
        "parent": null,
        "note": "",
        "text": "warmup epochs 10"
      },
      {
        "node_id": "C169",
        "label": "context",
        "source_span": "S305",
        "parent": null,
        "note": "",
        "text": "optimizer Adam [28], betas=(0.9, 0.999)"
      },
      {
        "node_id": "C170",
        "label": "context",
        "source_span": "S306",
        "parent": null,
        "note": "",
        "text": "batch size 8"
      },
      {
        "node_id": "C171",
        "label": "context",
        "source_span": "S307",
        "parent": null,
        "note": "",
        "text": "learning rate 3e-4"
      },
      {
        "node_id": "C172",
        "label": "context",
        "source_span": "S308",
        "parent": null,
        "note": "",
        "text": "learning rate scheduler cosine"
      },
      {
        "node_id": "C173",
        "label": "context",
        "source_span": "S309",
        "parent": null,
        "note": "",
        "text": "weight decay 0"
      },
      {
        "node_id": "C174",
        "label": "context",
        "source_span": "S310",
        "parent": null,
        "note": "",
        "text": "dropout 0.1"
      }
    ]
  },
  {
    "unit_id": "U031",
    "location": "Table 5",
    "kind": "table_fig",
    "source_chunk": 3,
    "span_range": [
      311,
      318
    ],
    "node_count": 8,
    "category_counts": {
      "context": 8
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C175",
        "label": "context",
        "source_span": "S311",
        "parent": null,
        "note": "",
        "text": "GPU type H100"
      },
      {
        "node_id": "C176",
        "label": "context",
        "source_span": "S312",
        "parent": null,
        "note": "",
        "text": "GPU number 8"
      },
      {
        "node_id": "C177",
        "label": "context",
        "source_span": "S313",
        "parent": null,
        "note": "",
        "text": "GPU time 4.8 hours"
      },
      {
        "node_id": "C178",
        "label": "context",
        "source_span": "S314",
        "parent": null,
        "note": "",
        "text": "GPU type H100"
      },
      {
        "node_id": "C179",
        "label": "context",
        "source_span": "S315",
        "parent": null,
        "note": "",
        "text": "GPU number 1"
      },
      {
        "node_id": "C180",
        "label": "context",
        "source_span": "S316",
        "parent": null,
        "note": "",
        "text": "GPU time 0.7s per epoch"
      },
      {
        "node_id": "C181",
        "label": "context",
        "source_span": "S317",
        "parent": null,
        "note": "",
        "text": "the ViT-18M model"
      },
      {
        "node_id": "C182",
        "label": "context",
        "source_span": "S318",
        "parent": null,
        "note": "",
        "text": "torch.compile optimization"
      }
    ]
  },
  {
    "unit_id": "U032",
    "location": "Table 6",
    "kind": "table_fig",
    "source_chunk": 3,
    "span_range": [
      319,
      326
    ],
    "node_count": 8,
    "category_counts": {
      "context": 8
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C183",
        "label": "context",
        "source_span": "S319",
        "parent": null,
        "note": "",
        "text": "hidden dim 384 512 768"
      },
      {
        "node_id": "C184",
        "label": "context",
        "source_span": "S320",
        "parent": null,
        "note": "",
        "text": "Transformer blocks 5 10 20"
      },
      {
        "node_id": "C185",
        "label": "context",
        "source_span": "S321",
        "parent": null,
        "note": "",
        "text": "# heads 8 8 12"
      },
      {
        "node_id": "C186",
        "label": "context",
        "source_span": "S322",
        "parent": null,
        "note": "",
        "text": "MLP block hidden dim 512"
      },
      {
        "node_id": "C187",
        "label": "context",
        "source_span": "S323",
        "parent": null,
        "note": "",
        "text": "dropout 0.1"
      },
      {
        "node_id": "C188",
        "label": "context",
        "source_span": "S324",
        "parent": null,
        "note": "",
        "text": "patch size 2x2"
      },
      {
        "node_id": "C189",
        "label": "context",
        "source_span": "S325",
        "parent": null,
        "note": "",
        "text": "canvas size 64x64"
      },
      {
        "node_id": "C190",
        "label": "context",
        "source_span": "S326",
        "parent": null,
        "note": "",
        "text": "The 18M model is our default setting."
      }
    ]
  },
  {
    "unit_id": "U033",
    "location": "Table 7",
    "kind": "table_fig",
    "source_chunk": 3,
    "span_range": [
      327,
      336
    ],
    "node_count": 10,
    "category_counts": {
      "context": 10
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C191",
        "label": "context",
        "source_span": "S327",
        "parent": null,
        "note": "",
        "text": "# stages 3 3 3"
      },
      {
        "node_id": "C192",
        "label": "context",
        "source_span": "S328",
        "parent": null,
        "note": "",
        "text": "layers per stage 1 1 2"
      },
      {
        "node_id": "C193",
        "label": "context",
        "source_span": "S329",
        "parent": null,
        "note": "",
        "text": "# channels at resolution 1 80 120 160"
      },
      {
        "node_id": "C194",
        "label": "context",
        "source_span": "S330",
        "parent": null,
        "note": "",
        "text": "attention at resolution 1 No No No"
      },
      {
        "node_id": "C195",
        "label": "context",
        "source_span": "S331",
        "parent": null,
        "note": "",
        "text": "# channels at resolution 2 160 240 320"
      },
      {
        "node_id": "C196",
        "label": "context",
        "source_span": "S332",
        "parent": null,
        "note": "",
        "text": "attention at resolution 2 Yes Yes Yes"
      },
      {
        "node_id": "C197",
        "label": "context",
        "source_span": "S333",
        "parent": null,
        "note": "",
        "text": "# channels at resolution 3 160 240 320"
      },
      {
        "node_id": "C198",
        "label": "context",
        "source_span": "S334",
        "parent": null,
        "note": "",
        "text": "attention at resolution 3 Yes Yes Yes"
      },
      {
        "node_id": "C199",
        "label": "context",
        "source_span": "S335",
        "parent": null,
        "note": "",
        "text": "mid block No No Yes"
      },
      {
        "node_id": "C200",
        "label": "context",
        "source_span": "S336",
        "parent": null,
        "note": "",
        "text": "standard U-Nets used in generative models [47, 15]"
      }
    ]
  },
  {
    "unit_id": "U034",
    "location": "Figure 13",
    "kind": "table_fig",
    "source_chunk": 3,
    "span_range": [
      337,
      340
    ],
    "node_count": 4,
    "category_counts": {
      "context": 4
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C201",
        "label": "context",
        "source_span": "S337",
        "parent": null,
        "note": "",
        "text": "The gray pixels denote the background tokens [BG], which keep the canvas size fixed (64×64 by default)."
      },
      {
        "node_id": "C202",
        "label": "context",
        "source_span": "S338",
        "parent": null,
        "note": "",
        "text": "The white pixels denote the border tokens [BD], which indicate the output shape."
      },
      {
        "node_id": "C203",
        "label": "context",
        "source_span": "S339",
        "parent": null,
        "note": "",
        "text": "a pair (x, y) with a scaling ratio of 1x"
      },
      {
        "node_id": "C204",
        "label": "context",
        "source_span": "S340",
        "parent": null,
        "note": "",
        "text": "a pair (x, y) with a scaling ratio of 2x"
      }
    ]
  },
  {
    "unit_id": "U035",
    "location": "Section A.2",
    "kind": "section",
    "source_chunk": 3,
    "span_range": [
      341,
      344
    ],
    "node_count": 7,
    "category_counts": {
      "context": 3,
      "intervention": 4
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C205",
        "label": "context",
        "source_span": "S341",
        "parent": null,
        "note": "",
        "text": "During test-time training"
      },
      {
        "node_id": "I67",
        "label": "intervention",
        "source_span": "S341",
        "parent": null,
        "note": "",
        "text": "we augment the single test task T into multiple auxiliary tasks."
      },
      {
        "node_id": "C206",
        "label": "context",
        "source_span": "S342",
        "parent": null,
        "note": "",
        "text": "not all of these augmentations correspond to the same underlying rule (e.g., consider \"gravity\" under a 90° rotation)"
      },
      {
        "node_id": "I68",
        "label": "intervention",
        "source_span": "S342",
        "parent": null,
        "note": "",
        "text": "We use a distinct task embedding for each auxiliary task"
      },
      {
        "node_id": "I69",
        "label": "intervention",
        "source_span": "S343",
        "parent": null,
        "note": "",
        "text": "We apply 2 flippings (horizontal and vertical) or 3 rotations (in multiples of 90°), and 10 predefined color index permutations, resulting in (2+3)×10=50 auxiliary tasks with the original task."
      },
      {
        "node_id": "C207",
        "label": "context",
        "source_span": "S344",
        "parent": null,
        "note": "",
        "text": "test-time training for one test task T (assuming 3 raw samples in this task)"
      },
      {
        "node_id": "I70",
        "label": "intervention",
        "source_span": "S344",
        "parent": null,
        "note": "",
        "text": "We train for 100 epochs on these 51 tasks, covering 100 x 51 x 3 = 15.3k samples in total"
      }
    ]
  },
  {
    "unit_id": "U036",
    "location": "Section A.3",
    "kind": "section",
    "source_chunk": 3,
    "span_range": [
      345,
      355
    ],
    "node_count": 16,
    "category_counts": {
      "mechanism": 4,
      "context": 6,
      "intervention": 6
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C208",
        "label": "context",
        "source_span": "S345",
        "parent": null,
        "note": "",
        "text": "Unlike standard semantic segmentation, in ARC, the raw input and output sizes are not always identical (e.g., see Fig. 3, Test Set, Task 1)."
      },
      {
        "node_id": "M51",
        "label": "mechanism",
        "source_span": "S346",
        "parent": null,
        "note": "",
        "text": "This issue can be addressed on the canvas in a unified framework."
      },
      {
        "node_id": "C209",
        "label": "context",
        "source_span": "S347",
        "parent": null,
        "note": "",
        "text": "In our method, the input/output canvas always has a fixed size and is filled with a background token [BG]."
      },
      {
        "node_id": "C210",
        "label": "context",
        "source_span": "S348",
        "parent": null,
        "note": "",
        "text": "when the raw output is placed on the canvas (serving as the ground truth during training)"
      },
      {
        "node_id": "I71",
        "label": "intervention",
        "source_span": "S348",
        "parent": null,
        "note": "",
        "text": "we always use an extra border token, [BD], to indicate the right and bottom edges."
      },
      {
        "node_id": "I72",
        "label": "intervention",
        "source_span": "S349",
        "parent": null,
        "note": "",
        "text": "the token [BD] is filled along the one-pixel-wide edge on the right and bottom sides."
      },
      {
        "node_id": "C211",
        "label": "context",
        "source_span": "S350",
        "parent": null,
        "note": "",
        "text": "During inference"
      },
      {
        "node_id": "I73",
        "label": "intervention",
        "source_span": "S350",
        "parent": null,
        "note": "",
        "text": "we locate the rightmost and bottommost [BD] tokens and crop the output accordingly to recover the final predicted shape."
      },
      {
        "node_id": "C212",
        "label": "context",
        "source_span": "S351",
        "parent": null,
        "note": "",
        "text": "the number of background pixels [BG] can dominate in some examples"
      },
      {
        "node_id": "I74",
        "label": "intervention",
        "source_span": "S351",
        "parent": null,
        "note": "",
        "text": "we apply attention masks in the self-attention blocks"
      },
      {
        "node_id": "M52",
        "label": "mechanism",
        "source_span": "S351",
        "parent": null,
        "note": "",
        "text": "to encourage the model to focus on the foreground pixels."
      },
      {
        "node_id": "I75",
        "label": "intervention",
        "source_span": "S352",
        "parent": null,
        "note": "",
        "text": "The attention masks are applied after the query-key dot-product computation, adding a large negative value to the keys corresponding to background inputs."
      },
      {
        "node_id": "M53",
        "label": "mechanism",
        "source_span": "S353",
        "parent": null,
        "note": "",
        "text": "The resulting softmax attention scores are therefore zero at those key positions."
      },
      {
        "node_id": "C213",
        "label": "context",
        "source_span": "S354",
        "parent": null,
        "note": "",
        "text": "during training"
      },
      {
        "node_id": "I76",
        "label": "intervention",
        "source_span": "S354",
        "parent": null,
        "note": "",
        "text": "the loss is computed only on locations where the inputs are not background pixels [BG]."
      },
      {
        "node_id": "M54",
        "label": "mechanism",
        "source_span": "S355",
        "parent": null,
        "note": "",
        "text": "These designs encourage the model to pay more attention to foregrounds and therefore improve accuracy"
      }
    ]
  },
  {
    "unit_id": "U037",
    "location": "Figure 14",
    "kind": "table_fig",
    "source_chunk": 3,
    "span_range": [
      356,
      357
    ],
    "node_count": 4,
    "category_counts": {
      "context": 2,
      "eval_metric": 1,
      "pattern": 1
    },
    "has_pattern": true,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C214",
        "label": "context",
        "source_span": "S356",
        "parent": null,
        "note": "",
        "text": "RE-ARC samples per task"
      },
      {
        "node_id": "C215",
        "label": "context",
        "source_span": "S356",
        "parent": null,
        "note": "",
        "text": "evaluated on the ARC-1 eval set"
      },
      {
        "node_id": "E18",
        "label": "eval_metric",
        "source_span": "S356",
        "parent": null,
        "note": "",
        "text": "Offline training data scaling: effect of varying"
      },
      {
        "node_id": "P59",
        "label": "pattern",
        "source_span": "S357",
        "parent": null,
        "note": "",
        "text": "Increasing the amount of offline training data is beneficial",
        "pattern_class": "primary_result"
      }
    ]
  },
  {
    "unit_id": "U038",
    "location": "Figure 15",
    "kind": "table_fig",
    "source_chunk": 3,
    "span_range": [
      358,
      359
    ],
    "node_count": 4,
    "category_counts": {
      "context": 2,
      "eval_metric": 1,
      "pattern": 1
    },
    "has_pattern": true,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C216",
        "label": "context",
        "source_span": "S358",
        "parent": null,
        "note": "",
        "text": "the number of training tasks"
      },
      {
        "node_id": "C217",
        "label": "context",
        "source_span": "S358",
        "parent": null,
        "note": "",
        "text": "evaluated on the ARC-1 eval set"
      },
      {
        "node_id": "E19",
        "label": "eval_metric",
        "source_span": "S358",
        "parent": null,
        "note": "",
        "text": "Offline training task diversity scaling: effect of varying"
      },
      {
        "node_id": "P60",
        "label": "pattern",
        "source_span": "S359",
        "parent": null,
        "note": "",
        "text": "Increasing task diversity is beneficial.",
        "pattern_class": "primary_result"
      }
    ]
  },
  {
    "unit_id": "U039",
    "location": "Section B.1",
    "kind": "section",
    "source_chunk": 3,
    "span_range": [
      360,
      365
    ],
    "node_count": 14,
    "category_counts": {
      "mechanism": 2,
      "context": 1,
      "intervention": 3,
      "eval_metric": 5,
      "pattern": 3
    },
    "has_pattern": true,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C218",
        "label": "context",
        "source_span": "S360",
        "parent": null,
        "note": "",
        "text": "RE-ARC dataset [22] in our offline training"
      },
      {
        "node_id": "E20",
        "label": "eval_metric",
        "source_span": "S360",
        "parent": null,
        "note": "",
        "text": "the effect of data scale provided by RE-ARC"
      },
      {
        "node_id": "I77",
        "label": "intervention",
        "source_span": "S361",
        "parent": null,
        "note": "",
        "text": "Using only the original ARC training data, without any RE-ARC data"
      },
      {
        "node_id": "E21",
        "label": "eval_metric",
        "source_span": "S361",
        "parent": null,
        "note": "",
        "text": "accuracy"
      },
      {
        "node_id": "P61",
        "label": "pattern",
        "source_span": "S361",
        "parent": null,
        "note": "31.5%",
        "text": "our method achieves a decent accuracy",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "I78",
        "label": "intervention",
        "source_span": "S362",
        "parent": null,
        "note": "",
        "text": "adding 10, 100, and 1,000 pairs per task from RE-ARC"
      },
      {
        "node_id": "E22",
        "label": "eval_metric",
        "source_span": "S362",
        "parent": null,
        "note": "",
        "text": "accuracy"
      },
      {
        "node_id": "P62",
        "label": "pattern",
        "source_span": "S362",
        "parent": null,
        "note": "to 38.6, 52.3, and 54.0",
        "text": "increases",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "M55",
        "label": "mechanism",
        "source_span": "S363",
        "parent": null,
        "note": "",
        "text": "increasing the amount of offline training data is beneficial, although the returns diminish beyond a certain point."
      },
      {
        "node_id": "E23",
        "label": "eval_metric",
        "source_span": "S364",
        "parent": null,
        "note": "",
        "text": "scalability of the offline training task diversity"
      },
      {
        "node_id": "I79",
        "label": "intervention",
        "source_span": "S365",
        "parent": null,
        "note": "",
        "text": "trained on 0, 16, 80, and 400 tasks"
      },
      {
        "node_id": "E24",
        "label": "eval_metric",
        "source_span": "S365",
        "parent": null,
        "note": "",
        "text": "accuracy"
      },
      {
        "node_id": "P63",
        "label": "pattern",
        "source_span": "S365",
        "parent": null,
        "note": "from 26.4 to 43.1, 49.6, and 54.5",
        "text": "increases",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "M56",
        "label": "mechanism",
        "source_span": "S365",
        "parent": null,
        "note": "",
        "text": "the diversity of training tasks is helpful for generalization."
      }
    ]
  },
  {
    "unit_id": "U040",
    "location": "Section B.2",
    "kind": "section",
    "source_chunk": 3,
    "span_range": [
      366,
      374
    ],
    "node_count": 14,
    "category_counts": {
      "mechanism": 1,
      "context": 3,
      "intervention": 1,
      "eval_metric": 6,
      "pattern": 3
    },
    "has_pattern": true,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C219",
        "label": "context",
        "source_span": "S366",
        "parent": null,
        "note": "",
        "text": "By default, the ARC protocol"
      },
      {
        "node_id": "E25",
        "label": "eval_metric",
        "source_span": "S366",
        "parent": null,
        "note": "",
        "text": "evaluates the pass@2 accuracy"
      },
      {
        "node_id": "C220",
        "label": "context",
        "source_span": "S367",
        "parent": null,
        "note": "",
        "text": "multi-view inference with many views (510)"
      },
      {
        "node_id": "E26",
        "label": "eval_metric",
        "source_span": "S367",
        "parent": null,
        "note": "",
        "text": "pass@k accuracy"
      },
      {
        "node_id": "E27",
        "label": "eval_metric",
        "source_span": "S368",
        "parent": null,
        "note": "",
        "text": "This metric reflects whether at least one of the k predicted solutions is correct."
      },
      {
        "node_id": "E28",
        "label": "eval_metric",
        "source_span": "S369",
        "parent": null,
        "note": "",
        "text": "It can be viewed as a recall-like measure."
      },
      {
        "node_id": "I80",
        "label": "intervention",
        "source_span": "S371",
        "parent": null,
        "note": "",
        "text": "as the number of proposals (k) increases"
      },
      {
        "node_id": "E30",
        "label": "eval_metric",
        "source_span": "S371",
        "parent": null,
        "note": "",
        "text": "pass@k accuracy"
      },
      {
        "node_id": "P64",
        "label": "pattern",
        "source_span": "S371",
        "parent": null,
        "note": "",
        "text": "increases",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "C222",
        "label": "context",
        "source_span": "S372",
        "parent": null,
        "note": "",
        "text": "On ARC-1"
      },
      {
        "node_id": "E31",
        "label": "eval_metric",
        "source_span": "S372",
        "parent": null,
        "note": "",
        "text": "pass@k accu-racy"
      },
      {
        "node_id": "P65",
        "label": "pattern",
        "source_span": "S372",
        "parent": null,
        "note": "49.8, 54.5, and 66.3, when k is 1, 2, and 300",
        "text": "is",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "M57",
        "label": "mechanism",
        "source_span": "S373",
        "parent": null,
        "note": "",
        "text": "our model produces correct predictions in some of the many views, although such cor-rect cases are not sufficiently populated to be retained after voting."
      },
      {
        "node_id": "P66",
        "label": "pattern",
        "source_span": "S374",
        "parent": null,
        "note": "",
        "text": "this result reveals the upper-bound performance (66.3) of our method, even if oracle voting were applied.",
        "pattern_class": "primary_result"
      }
    ]
  },
  {
    "unit_id": "U041",
    "location": "Figure 16, Section B.2",
    "kind": "table_fig",
    "source_chunk": 3,
    "span_range": [
      370,
      370
    ],
    "node_count": 2,
    "category_counts": {
      "context": 1,
      "eval_metric": 1
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C221",
        "label": "context",
        "source_span": "S370",
        "parent": null,
        "note": "",
        "text": "ARC-1 and ARC-2 eval sets"
      },
      {
        "node_id": "E29",
        "label": "eval_metric",
        "source_span": "S370",
        "parent": null,
        "note": "",
        "text": "pass@k results"
      }
    ]
  },
  {
    "unit_id": "U042",
    "location": "Section C.1",
    "kind": "section",
    "source_chunk": 3,
    "span_range": [
      375,
      376
    ],
    "node_count": 2,
    "category_counts": {
      "context": 1,
      "pattern": 1
    },
    "has_pattern": true,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C223",
        "label": "context",
        "source_span": "S375",
        "parent": null,
        "note": "",
        "text": "ARC-1 (Fig. 17) and ARC-2 (Fig. 18)"
      },
      {
        "node_id": "P67",
        "label": "pattern",
        "source_span": "S376",
        "parent": null,
        "note": "",
        "text": "Our method can solve some highly challenging tasks, but still makes mistakes on some tasks that are simple for humans.",
        "pattern_class": "summary_claim"
      }
    ]
  },
  {
    "unit_id": "U043",
    "location": "Section C.2",
    "kind": "section",
    "source_chunk": 3,
    "span_range": [
      377,
      379
    ],
    "node_count": 5,
    "category_counts": {
      "assumption": 1,
      "mechanism": 1,
      "context": 2,
      "pattern": 1
    },
    "has_pattern": true,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C224",
        "label": "context",
        "source_span": "S377",
        "parent": null,
        "note": "",
        "text": "most ARC tasks are unambiguous"
      },
      {
        "node_id": "A20",
        "label": "assumption",
        "source_span": "S377",
        "parent": null,
        "note": "",
        "text": "some may admit multiple plausible explanations or rules."
      },
      {
        "node_id": "C225",
        "label": "context",
        "source_span": "S378",
        "parent": null,
        "note": "",
        "text": "an example in Fig. 19"
      },
      {
        "node_id": "P68",
        "label": "pattern",
        "source_span": "S378",
        "parent": null,
        "note": "",
        "text": "our method uncovers different solutions that are plausible.",
        "pattern_class": "summary_claim"
      },
      {
        "node_id": "M58",
        "label": "mechanism",
        "source_span": "S379",
        "parent": null,
        "note": "",
        "text": "the rule can be interpreted as either \"turn the red box blue only if the extended blue lines go through the box\" (our method's first guess) or \"turn the red box blue if the extended blue lines touch the box in any form\" (our method's second guess)."
      }
    ]
  },
  {
    "unit_id": "U044",
    "location": "Section C.3",
    "kind": "section",
    "source_chunk": 3,
    "span_range": [
      380,
      381
    ],
    "node_count": 4,
    "category_counts": {
      "context": 2,
      "intervention": 2
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C226",
        "label": "context",
        "source_span": "S380",
        "parent": null,
        "note": "",
        "text": "In Fig. 20"
      },
      {
        "node_id": "I81",
        "label": "intervention",
        "source_span": "S380",
        "parent": null,
        "note": "",
        "text": "we visualize the attention maps of a single pixel specified as the query."
      },
      {
        "node_id": "C227",
        "label": "context",
        "source_span": "S381",
        "parent": null,
        "note": "",
        "text": "In Fig. 21"
      },
      {
        "node_id": "I82",
        "label": "intervention",
        "source_span": "S381",
        "parent": null,
        "note": "",
        "text": "we visualize the layer-wise attention maps averaged across all pixels."
      }
    ]
  },
  {
    "unit_id": "U045",
    "location": "Section C.4",
    "kind": "section",
    "source_chunk": 3,
    "span_range": [
      382,
      384
    ],
    "node_count": 4,
    "category_counts": {
      "context": 2,
      "intervention": 1,
      "pattern": 1
    },
    "has_pattern": true,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C228",
        "label": "context",
        "source_span": "S382",
        "parent": null,
        "note": "",
        "text": "Figure 22"
      },
      {
        "node_id": "I83",
        "label": "intervention",
        "source_span": "S382",
        "parent": null,
        "note": "",
        "text": "illustrates the evolution of model predictions during the test-time training process."
      },
      {
        "node_id": "C229",
        "label": "context",
        "source_span": "S383",
        "parent": null,
        "note": "",
        "text": "Each row corresponds to a distinct test task from the ARC benchmark."
      },
      {
        "node_id": "P69",
        "label": "pattern",
        "source_span": "S384",
        "parent": null,
        "note": "",
        "text": "our method progres-sively refines its prediction through test-time training.",
        "pattern_class": "summary_claim"
      }
    ]
  },
  {
    "unit_id": "U046",
    "location": "Figure 17",
    "kind": "table_fig",
    "source_chunk": 4,
    "span_range": [
      385,
      391
    ],
    "node_count": 23,
    "category_counts": {
      "context": 13,
      "intervention": 3,
      "eval_metric": 2,
      "pattern": 5
    },
    "has_pattern": true,
    "parent_subgroups": [
      {
        "parent": "S385",
        "node_ids": [
          "C230",
          "P70"
        ]
      },
      {
        "parent": "S386",
        "node_ids": [
          "C231",
          "I84",
          "P71"
        ]
      },
      {
        "parent": "S387",
        "node_ids": [
          "C232",
          "I85",
          "P72"
        ]
      },
      {
        "parent": "S389",
        "node_ids": [
          "C234",
          "I86"
        ]
      },
      {
        "parent": "S391",
        "node_ids": [
          "C235",
          "C236",
          "C237",
          "C238",
          "C239",
          "C240",
          "C241",
          "C242",
          "E33",
          "P73",
          "P74"
        ]
      }
    ],
    "nodes": [
      {
        "node_id": "C230",
        "label": "context",
        "source_span": "S385",
        "parent": "S385",
        "note": "",
        "text": "ARC-1"
      },
      {
        "node_id": "P70",
        "label": "pattern",
        "source_span": "S385",
        "parent": "S385",
        "note": "",
        "text": "Successful and failed examples",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "C231",
        "label": "context",
        "source_span": "S386",
        "parent": "S386",
        "note": "",
        "text": "test tasks"
      },
      {
        "node_id": "I84",
        "label": "intervention",
        "source_span": "S386",
        "parent": "S386",
        "note": "",
        "text": "solved by VARC"
      },
      {
        "node_id": "P71",
        "label": "pattern",
        "source_span": "S386",
        "parent": "S386",
        "note": "",
        "text": "successfully solved",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "C232",
        "label": "context",
        "source_span": "S387",
        "parent": "S387",
        "note": "",
        "text": "test tasks"
      },
      {
        "node_id": "I85",
        "label": "intervention",
        "source_span": "S387",
        "parent": "S387",
        "note": "",
        "text": "unsolved by VARC"
      },
      {
        "node_id": "P72",
        "label": "pattern",
        "source_span": "S387",
        "parent": "S387",
        "note": "",
        "text": "unsolved",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "C233",
        "label": "context",
        "source_span": "S388",
        "parent": "S388",
        "note": "",
        "text": "Two demonstration example pairs shown for each task (some have more demonstrations not shown here)"
      },
      {
        "node_id": "C234",
        "label": "context",
        "source_span": "S389",
        "parent": "S389",
        "note": "",
        "text": "Inference input"
      },
      {
        "node_id": "I86",
        "label": "intervention",
        "source_span": "S389",
        "parent": "S389",
        "note": "",
        "text": "first and second solutions proposed by VARC"
      },
      {
        "node_id": "E32",
        "label": "eval_metric",
        "source_span": "S390",
        "parent": "S390",
        "note": "",
        "text": "correct output"
      },
      {
        "node_id": "C235",
        "label": "context",
        "source_span": "S391",
        "parent": "S391",
        "note": "",
        "text": "Task 15663ba9"
      },
      {
        "node_id": "C236",
        "label": "context",
        "source_span": "S391",
        "parent": "S391",
        "note": "",
        "text": "Task 981571dc"
      },
      {
        "node_id": "C237",
        "label": "context",
        "source_span": "S391",
        "parent": "S391",
        "note": "",
        "text": "Task 15696249"
      },
      {
        "node_id": "C238",
        "label": "context",
        "source_span": "S391",
        "parent": "S391",
        "note": "",
        "text": "Task 67c52801"
      },
      {
        "node_id": "C239",
        "label": "context",
        "source_span": "S391",
        "parent": "S391",
        "note": "",
        "text": "Task 8dae5dfc"
      },
      {
        "node_id": "C240",
        "label": "context",
        "source_span": "S391",
        "parent": "S391",
        "note": "",
        "text": "Task 67636eac"
      },
      {
        "node_id": "C241",
        "label": "context",
        "source_span": "S391",
        "parent": "S391",
        "note": "",
        "text": "Task aa4ec2a5"
      },
      {
        "node_id": "C242",
        "label": "context",
        "source_span": "S391",
        "parent": "S391",
        "note": "",
        "text": "Task b457fec5"
      },
      {
        "node_id": "E33",
        "label": "eval_metric",
        "source_span": "S391",
        "parent": "S391",
        "note": "109, 57, 399, 35, 456, 10, 233, 123, 9, 6, 14, 8, 13, 9, 3, 2",
        "text": "Vote"
      },
      {
        "node_id": "P73",
        "label": "pattern",
        "source_span": "S391",
        "parent": "S391",
        "note": "Tasks: 15663ba9, 981571dc, 15696249, 67c52801",
        "text": "VARC's Attempt 1 matches the Ground Truth",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "P74",
        "label": "pattern",
        "source_span": "S391",
        "parent": "S391",
        "note": "Tasks: 8dae5dfc, 67636eac, aa4ec2a5, b457fec5",
        "text": "VARC fails to solve the task",
        "pattern_class": "primary_result"
      }
    ]
  },
  {
    "unit_id": "U047",
    "location": "Figure 18",
    "kind": "table_fig",
    "source_chunk": 4,
    "span_range": [
      392,
      398
    ],
    "node_count": 23,
    "category_counts": {
      "context": 13,
      "intervention": 3,
      "eval_metric": 2,
      "pattern": 5
    },
    "has_pattern": true,
    "parent_subgroups": [
      {
        "parent": "S392",
        "node_ids": [
          "C243",
          "P75"
        ]
      },
      {
        "parent": "S393",
        "node_ids": [
          "C244",
          "I87",
          "P76"
        ]
      },
      {
        "parent": "S394",
        "node_ids": [
          "C245",
          "I88",
          "P77"
        ]
      },
      {
        "parent": "S396",
        "node_ids": [
          "C247",
          "I89"
        ]
      },
      {
        "parent": "S398",
        "node_ids": [
          "C248",
          "C249",
          "C250",
          "C251",
          "C252",
          "C253",
          "C254",
          "C255",
          "E35",
          "P78",
          "P79"
        ]
      }
    ],
    "nodes": [
      {
        "node_id": "C243",
        "label": "context",
        "source_span": "S392",
        "parent": "S392",
        "note": "",
        "text": "ARC-2"
      },
      {
        "node_id": "P75",
        "label": "pattern",
        "source_span": "S392",
        "parent": "S392",
        "note": "",
        "text": "Successful and failed examples",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "C244",
        "label": "context",
        "source_span": "S393",
        "parent": "S393",
        "note": "",
        "text": "test tasks"
      },
      {
        "node_id": "I87",
        "label": "intervention",
        "source_span": "S393",
        "parent": "S393",
        "note": "",
        "text": "solved by VARC"
      },
      {
        "node_id": "P76",
        "label": "pattern",
        "source_span": "S393",
        "parent": "S393",
        "note": "",
        "text": "successfully solved",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "C245",
        "label": "context",
        "source_span": "S394",
        "parent": "S394",
        "note": "",
        "text": "test tasks"
      },
      {
        "node_id": "I88",
        "label": "intervention",
        "source_span": "S394",
        "parent": "S394",
        "note": "",
        "text": "unsolved by VARC"
      },
      {
        "node_id": "P77",
        "label": "pattern",
        "source_span": "S394",
        "parent": "S394",
        "note": "",
        "text": "unsolved",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "C246",
        "label": "context",
        "source_span": "S395",
        "parent": "S395",
        "note": "",
        "text": "Two demonstration example pairs shown for each task (some have more demonstrations not shown here)"
      },
      {
        "node_id": "C247",
        "label": "context",
        "source_span": "S396",
        "parent": "S396",
        "note": "",
        "text": "Inference input"
      },
      {
        "node_id": "I89",
        "label": "intervention",
        "source_span": "S396",
        "parent": "S396",
        "note": "",
        "text": "first and second solutions proposed by VARC"
      },
      {
        "node_id": "E34",
        "label": "eval_metric",
        "source_span": "S397",
        "parent": "S397",
        "note": "",
        "text": "correct output"
      },
      {
        "node_id": "C248",
        "label": "context",
        "source_span": "S398",
        "parent": "S398",
        "note": "",
        "text": "Task 800d221b"
      },
      {
        "node_id": "C249",
        "label": "context",
        "source_span": "S398",
        "parent": "S398",
        "note": "",
        "text": "Task 7666fa5d"
      },
      {
        "node_id": "C250",
        "label": "context",
        "source_span": "S398",
        "parent": "S398",
        "note": "",
        "text": "Task 221dfab4"
      },
      {
        "node_id": "C251",
        "label": "context",
        "source_span": "S398",
        "parent": "S398",
        "note": "",
        "text": "Task 7b80bb43"
      },
      {
        "node_id": "C252",
        "label": "context",
        "source_span": "S398",
        "parent": "S398",
        "note": "",
        "text": "Task 2b83f449"
      },
      {
        "node_id": "C253",
        "label": "context",
        "source_span": "S398",
        "parent": "S398",
        "note": "",
        "text": "Task 2d0172a1"
      },
      {
        "node_id": "C254",
        "label": "context",
        "source_span": "S398",
        "parent": "S398",
        "note": "",
        "text": "Task 3e6067c3"
      },
      {
        "node_id": "C255",
        "label": "context",
        "source_span": "S398",
        "parent": "S398",
        "note": "",
        "text": "Task 7ed72f31"
      },
      {
        "node_id": "E35",
        "label": "eval_metric",
        "source_span": "S398",
        "parent": "S398",
        "note": "99, 82, 410, 16, 30, 17, 168, 44, 21, 20, 7, 6, 14, 12, 67, 51",
        "text": "Vote"
      },
      {
        "node_id": "P78",
        "label": "pattern",
        "source_span": "S398",
        "parent": "S398",
        "note": "Tasks: 800d221b, 7666fa5d, 221dfab4, 7b80bb43",
        "text": "VARC's Attempt 1 matches the Ground Truth",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "P79",
        "label": "pattern",
        "source_span": "S398",
        "parent": "S398",
        "note": "Tasks: 2b83f449, 2d0172a1, 3e6067c3, 7ed72f31",
        "text": "VARC fails to solve the task",
        "pattern_class": "primary_result"
      }
    ]
  },
  {
    "unit_id": "U048",
    "location": "Figure 19",
    "kind": "table_fig",
    "source_chunk": 4,
    "span_range": [
      399,
      403
    ],
    "node_count": 11,
    "category_counts": {
      "assumption": 2,
      "context": 4,
      "intervention": 1,
      "eval_metric": 1,
      "pattern": 3
    },
    "has_pattern": true,
    "parent_subgroups": [
      {
        "parent": "S400",
        "node_ids": [
          "A21",
          "P81"
        ]
      },
      {
        "parent": "S401",
        "node_ids": [
          "C256",
          "C257",
          "A22"
        ]
      },
      {
        "parent": "S402",
        "node_ids": [
          "C258",
          "I90"
        ]
      },
      {
        "parent": "S403",
        "node_ids": [
          "C259",
          "E36",
          "P82"
        ]
      }
    ],
    "nodes": [
      {
        "node_id": "P80",
        "label": "pattern",
        "source_span": "S399",
        "parent": "S399",
        "note": "",
        "text": "Ambiguous examples",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "A21",
        "label": "assumption",
        "source_span": "S400",
        "parent": "S400",
        "note": "",
        "text": "most ARC tasks are unambiguous"
      },
      {
        "node_id": "P81",
        "label": "pattern",
        "source_span": "S400",
        "parent": "S400",
        "note": "",
        "text": "some may admit multiple plausible explanations or rules",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "C256",
        "label": "context",
        "source_span": "S401",
        "parent": "S401",
        "note": "",
        "text": "three demonstration examples of a test task (top panel)"
      },
      {
        "node_id": "C257",
        "label": "context",
        "source_span": "S401",
        "parent": "S401",
        "note": "",
        "text": "a blue line \"touching\" (but not \"going through\") a red rectangle"
      },
      {
        "node_id": "A22",
        "label": "assumption",
        "source_span": "S401",
        "parent": "S401",
        "note": "",
        "text": "it is unclear whether a blue line \"touching\" (but not \"going through\") a red rectangle should render that rectangle blue"
      },
      {
        "node_id": "C258",
        "label": "context",
        "source_span": "S402",
        "parent": "S402",
        "note": "",
        "text": "inference example (bottom panel) involves this situation (\"touching\")"
      },
      {
        "node_id": "I90",
        "label": "intervention",
        "source_span": "S402",
        "parent": "S402",
        "note": "",
        "text": "our model attempts to interpret the rule as either \"going-through-only\" (attempt 1) or \"touching\" (attempt 2)"
      },
      {
        "node_id": "C259",
        "label": "context",
        "source_span": "S403",
        "parent": "S403",
        "note": "",
        "text": "Task 09c534e7"
      },
      {
        "node_id": "E36",
        "label": "eval_metric",
        "source_span": "S403",
        "parent": "S403",
        "note": "",
        "text": "Ground truth"
      },
      {
        "node_id": "P82",
        "label": "pattern",
        "source_span": "S403",
        "parent": "S403",
        "note": "",
        "text": "Attempt 2 matches Ground Truth, Attempt 1 does not",
        "pattern_class": "primary_result"
      }
    ]
  },
  {
    "unit_id": "U049",
    "location": "Figure 20",
    "kind": "table_fig",
    "source_chunk": 4,
    "span_range": [
      404,
      416
    ],
    "node_count": 21,
    "category_counts": {
      "mechanism": 10,
      "context": 9,
      "eval_metric": 1,
      "pattern": 1
    },
    "has_pattern": true,
    "parent_subgroups": [
      {
        "parent": "S405",
        "node_ids": [
          "C261",
          "C262"
        ]
      },
      {
        "parent": "S411",
        "node_ids": [
          "E37",
          "P83"
        ]
      },
      {
        "parent": "S413",
        "node_ids": [
          "C265",
          "M63",
          "M64"
        ]
      },
      {
        "parent": "S414",
        "node_ids": [
          "C266",
          "M65"
        ]
      },
      {
        "parent": "S415",
        "node_ids": [
          "C267",
          "M66"
        ]
      },
      {
        "parent": "S416",
        "node_ids": [
          "C268",
          "M67",
          "M68"
        ]
      }
    ],
    "nodes": [
      {
        "node_id": "C260",
        "label": "context",
        "source_span": "S404",
        "parent": "S404",
        "note": "",
        "text": "pixel-level attention maps"
      },
      {
        "node_id": "C261",
        "label": "context",
        "source_span": "S405",
        "parent": "S405",
        "note": "",
        "text": "different Transformer blocks"
      },
      {
        "node_id": "C262",
        "label": "context",
        "source_span": "S405",
        "parent": "S405",
        "note": "",
        "text": "a query pixel highlighted by a red-yellow border"
      },
      {
        "node_id": "C263",
        "label": "context",
        "source_span": "S406",
        "parent": "S406",
        "note": "",
        "text": "4 test tasks in ARC eval"
      },
      {
        "node_id": "M59",
        "label": "mechanism",
        "source_span": "S407",
        "parent": "S407",
        "note": "",
        "text": "Layers at different depths tend to focus on different structures"
      },
      {
        "node_id": "M60",
        "label": "mechanism",
        "source_span": "S408",
        "parent": "S408",
        "note": "",
        "text": "Early layers tend to focus on local transformations and context"
      },
      {
        "node_id": "M61",
        "label": "mechanism",
        "source_span": "S409",
        "parent": "S409",
        "note": "",
        "text": "Middle layers tend to perform a more non-local connection, e.g., horizontally or vertically"
      },
      {
        "node_id": "M62",
        "label": "mechanism",
        "source_span": "S410",
        "parent": "S410",
        "note": "",
        "text": "The deep layers are more task-specialized"
      },
      {
        "node_id": "E37",
        "label": "eval_metric",
        "source_span": "S411",
        "parent": "S411",
        "note": "",
        "text": "correctly solved"
      },
      {
        "node_id": "P83",
        "label": "pattern",
        "source_span": "S411",
        "parent": "S411",
        "note": "",
        "text": "task that was not correctly solved",
        "pattern_class": "primary_result"
      },
      {
        "node_id": "C264",
        "label": "context",
        "source_span": "S412",
        "parent": "S412",
        "note": "",
        "text": "text descriptions are written by humans solely to help readers interpret the tasks"
      },
      {
        "node_id": "C265",
        "label": "context",
        "source_span": "S413",
        "parent": "S413",
        "note": "",
        "text": "Task 09c534e7"
      },
      {
        "node_id": "M63",
        "label": "mechanism",
        "source_span": "S413",
        "parent": "S413",
        "note": "Block 2 heatmap description",
        "text": "Attention focuses on endpoints of all lines for all pixels."
      },
      {
        "node_id": "M64",
        "label": "mechanism",
        "source_span": "S413",
        "parent": "S413",
        "note": "Block 6 heatmap description",
        "text": "Attention is focused within the rectangle."
      },
      {
        "node_id": "C266",
        "label": "context",
        "source_span": "S414",
        "parent": "S414",
        "note": "",
        "text": "Task 506d28a5"
      },
      {
        "node_id": "M65",
        "label": "mechanism",
        "source_span": "S414",
        "parent": "S414",
        "note": "Block 7 heatmap description",
        "text": "Attention focuses on the corresponding cell in the lower part of the grid."
      },
      {
        "node_id": "C267",
        "label": "context",
        "source_span": "S415",
        "parent": "S415",
        "note": "",
        "text": "Task 0607ce86"
      },
      {
        "node_id": "M66",
        "label": "mechanism",
        "source_span": "S415",
        "parent": "S415",
        "note": "Block 7 heatmap description",
        "text": "Attention focuses on other cells in the same relative position within the grid."
      },
      {
        "node_id": "C268",
        "label": "context",
        "source_span": "S416",
        "parent": "S416",
        "note": "",
        "text": "Task 070dd51e"
      },
      {
        "node_id": "M67",
        "label": "mechanism",
        "source_span": "S416",
        "parent": "S416",
        "note": "Block 3 heatmap description",
        "text": "Attention focuses on endpoints of all lines for all pixels."
      },
      {
        "node_id": "M68",
        "label": "mechanism",
        "source_span": "S416",
        "parent": "S416",
        "note": "Block 7 heatmap description",
        "text": "Attention focuses on nearby, relevant lines only, focusing strongest on the correct line."
      }
    ]
  },
  {
    "unit_id": "U050",
    "location": "Figure 21",
    "kind": "table_fig",
    "source_chunk": 4,
    "span_range": [
      417,
      420
    ],
    "node_count": 8,
    "category_counts": {
      "context": 6,
      "eval_metric": 1,
      "pattern": 1
    },
    "has_pattern": true,
    "parent_subgroups": [
      {
        "parent": "S420",
        "node_ids": [
          "C271",
          "C272",
          "C273",
          "C274",
          "P84"
        ]
      }
    ],
    "nodes": [
      {
        "node_id": "C269",
        "label": "context",
        "source_span": "S417",
        "parent": "S417",
        "note": "",
        "text": "layer-wise attention maps"
      },
      {
        "node_id": "E38",
        "label": "eval_metric",
        "source_span": "S418",
        "parent": "S418",
        "note": "",
        "text": "per-pixel softmax attention maps averaged across all pixels in that layer"
      },
      {
        "node_id": "C270",
        "label": "context",
        "source_span": "S419",
        "parent": "S419",
        "note": "",
        "text": "demonstration examples (on the left) are provided for reference"
      },
      {
        "node_id": "C271",
        "label": "context",
        "source_span": "S420",
        "parent": "S420",
        "note": "",
        "text": "Task 0607ce86"
      },
      {
        "node_id": "C272",
        "label": "context",
        "source_span": "S420",
        "parent": "S420",
        "note": "",
        "text": "Task 0bb8deee"
      },
      {
        "node_id": "C273",
        "label": "context",
        "source_span": "S420",
        "parent": "S420",
        "note": "",
        "text": "Task 1c56ad9f"
      },
      {
        "node_id": "C274",
        "label": "context",
        "source_span": "S420",
        "parent": "S420",
        "note": "",
        "text": "Task 1d0a4b61"
      },
      {
        "node_id": "P84",
        "label": "pattern",
        "source_span": "S420",
        "parent": "S420",
        "note": "",
        "text": "Attention patterns vary across layers",
        "pattern_class": "primary_result"
      }
    ]
  },
  {
    "unit_id": "U051",
    "location": "Figure 22 title | Figure 22 'TTT process' label",
    "kind": "table_fig",
    "source_chunk": 5,
    "span_range": [
      421,
      421
    ],
    "node_count": 1,
    "category_counts": {
      "intervention": 1
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "I91",
        "label": "intervention",
        "source_span": "S421",
        "parent": null,
        "note": "",
        "text": "test-time training process"
      }
    ]
  },
  {
    "unit_id": "U052",
    "location": "Figure 22",
    "kind": "table_fig",
    "source_chunk": 5,
    "span_range": [
      421,
      421
    ],
    "node_count": 1,
    "category_counts": {
      "context": 1
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "C275",
        "label": "context",
        "source_span": "S421",
        "parent": null,
        "note": "",
        "text": "Demonstration 1, Demonstration 2, Input, Ground truth for examples 55059096, 0c786b71, ac3e2b04 (paraphrase)"
      }
    ]
  },
  {
    "unit_id": "U053",
    "location": "Figure 22 caption",
    "kind": "table_fig",
    "source_chunk": 5,
    "span_range": [
      422,
      426
    ],
    "node_count": 9,
    "category_counts": {
      "mechanism": 2,
      "context": 5,
      "intervention": 2
    },
    "has_pattern": false,
    "parent_subgroups": [
      {
        "parent": "S425",
        "node_ids": [
          "C279",
          "M69"
        ]
      },
      {
        "parent": "S426",
        "node_ids": [
          "M70",
          "C280",
          "I93"
        ]
      }
    ],
    "nodes": [
      {
        "node_id": "C276",
        "label": "context",
        "source_span": "S422",
        "parent": null,
        "note": "",
        "text": "the grid augmented with a given scale ratio of 2×"
      },
      {
        "node_id": "C277",
        "label": "context",
        "source_span": "S422",
        "parent": null,
        "note": "",
        "text": "the full canvas is not shown for brevity"
      },
      {
        "node_id": "I92",
        "label": "intervention",
        "source_span": "S423",
        "parent": "S423",
        "note": "",
        "text": "test-time training progresses"
      },
      {
        "node_id": "C278",
        "label": "context",
        "source_span": "S424",
        "parent": "S424",
        "note": "",
        "text": "In early epochs"
      },
      {
        "node_id": "C279",
        "label": "context",
        "source_span": "S425",
        "parent": "S425",
        "note": "",
        "text": "in later epochs"
      },
      {
        "node_id": "M69",
        "label": "mechanism",
        "source_span": "S425",
        "parent": "S425",
        "note": "",
        "text": "by refining color and spatial arrangement"
      },
      {
        "node_id": "M70",
        "label": "mechanism",
        "source_span": "S426",
        "parent": "S426",
        "note": "",
        "text": "model's behavior of adapting to task-specific transformations"
      },
      {
        "node_id": "C280",
        "label": "context",
        "source_span": "S426",
        "parent": "S426",
        "note": "",
        "text": "task-specific transformations"
      },
      {
        "node_id": "I93",
        "label": "intervention",
        "source_span": "S426",
        "parent": "S426",
        "note": "",
        "text": "few-shot test-time training"
      }
    ]
  },
  {
    "unit_id": "U054",
    "location": "Figure 22 caption | Figure 22 'TTT process' and 'Ground truth' panels",
    "kind": "table_fig",
    "source_chunk": 5,
    "span_range": [
      423,
      423
    ],
    "node_count": 1,
    "category_counts": {
      "eval_metric": 1
    },
    "has_pattern": false,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "E39",
        "label": "eval_metric",
        "source_span": "S423",
        "parent": "S423",
        "note": "",
        "text": "model's predictions converge toward the correct output"
      }
    ]
  },
  {
    "unit_id": "U055",
    "location": "Figure 22 caption | Figure 22 'TTT process' panels",
    "kind": "table_fig",
    "source_chunk": 5,
    "span_range": [
      423,
      423
    ],
    "node_count": 1,
    "category_counts": {
      "pattern": 1
    },
    "has_pattern": true,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "P85",
        "label": "pattern",
        "source_span": "S423",
        "parent": "S423",
        "note": "",
        "text": "gradually converge toward the correct output",
        "pattern_class": "primary_result"
      }
    ]
  },
  {
    "unit_id": "U056",
    "location": "Figure 22 caption | Figure 22 'TTT process' panels (early stages)",
    "kind": "table_fig",
    "source_chunk": 5,
    "span_range": [
      424,
      424
    ],
    "node_count": 1,
    "category_counts": {
      "pattern": 1
    },
    "has_pattern": true,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "P86",
        "label": "pattern",
        "source_span": "S424",
        "parent": "S424",
        "note": "",
        "text": "model produces coarse and imprecise structures",
        "pattern_class": "primary_result"
      }
    ]
  },
  {
    "unit_id": "U057",
    "location": "Figure 22 caption | Figure 22 'TTT process' panels (later stages)",
    "kind": "table_fig",
    "source_chunk": 5,
    "span_range": [
      425,
      425
    ],
    "node_count": 1,
    "category_counts": {
      "pattern": 1
    },
    "has_pattern": true,
    "parent_subgroups": [],
    "nodes": [
      {
        "node_id": "P87",
        "label": "pattern",
        "source_span": "S425",
        "parent": "S425",
        "note": "",
        "text": "model can improve the solutions",
        "pattern_class": "comparison"
      }
    ]
  }
]
--- END INPUT ---

## Your task

Emit CIO cards by SELECTING node_ids. Follow these rules exactly:

**SELECT, never write text.** Every field is a node_id (or list of node_ids) drawn from the input —
never the node's text, never a source_span (S-number). If no node fits, use null.

**One card per measured result.** Anchor exactly one card on each pattern node whose
`pattern_class` is `primary_result` or `comparison`. Do **not** build cards on `summary_claim` or
`background` patterns (those are abstract/headline restatements, not a single measured result).

**Stay inside one evidence unit.** Build each card from node_ids belonging to the SAME evidence
unit as its pattern node. NEVER mix node_ids from different units into one card — the unit boundary
is the experiment boundary. (A pattern in a prose Section may pull its context/intervention from the
same Section unit only.)

**Fill each field by selecting from that unit:**
- `context`: the list of context node_ids that state this observation's setting (often several —
  e.g. the spec rows of a table). Prefer the concrete setting rows over vague background.
- `intervention`: the node_id of the manipulated / compared condition. Use null only for a purely
  observational result with no manipulation.
- `reference`: **the baseline arm.** When the pattern is a comparison ("A is better than B"), select
  the node_id of the baseline/other condition B if a distinct node exists; otherwise null. Read the
  PAPER text and figure descriptions to identify B (e.g. "U-Net" opposite "ViT", "TTT jointly"
  opposite "TTT independently").
- `eval_metric`: the node_id of the metric, or null.
- `pattern`: the node_id of the measured result (the anchor).
- `direction`: `up` / `down` / `flat` / null — the direction the pattern reports for the
  intervention relative to the reference, read from the paper/figure, not guessed.

**Ground everything in the paper.** Use the prose + figure/table descriptions to confirm the
reference arm and direction. Do not invent comparisons the paper does not make.

## Output

A JSON array only (no prose), each element exactly:

```json
{
  "cio_id": "CIO_001",
  "unit": "U017",
  "context": ["C110", "C111"],
  "intervention": "I49",
  "reference": "C113",
  "eval_metric": "E8",
  "pattern": "P19",
  "direction": "up",
  "pattern_class": "comparison",
  "provenance": { "location": "Table 1", "source_span": "S189" },
  "status": "observed"
}
```
