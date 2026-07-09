You are drawing **belief_update edges** — the core of an AIO factor graph. Each edge says that one
measured observation (a CIO card) **strengthens or weakens** one mechanism or assumption (an AM
card), but ONLY where the paper makes that link explicit. This is a matching task over already-clean
cards; you are not extracting anything new.

paper_id: PXX
paper_title_hint: unknown

You are given the paper (to verify what it explicitly claims), the CIO observation cards, and the AM
belief-target cards.

--- PAPER: PROSE TRANSCRIPTION ---
===== pages 1-4 =====

arXiv:2511.14761v1 [cs.CV] 18 Nov 2025
ARC Is a Vision Problem!
Keya Hu Ali Cy Linlu Qiu Xiaoman Delores Ding
Runqian Wang Yeyin Eva Zhu Jacob Andreas Kaiming He
MIT

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
Test Set Ttest
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
A task. A "task" is the basic unit in ARC. Each task in-
cludes a few demonstration examples. For a demonstration
pair (x, y), both x and y are known to the model. We denote
the demonstration set of task T as: Demo={(xi, Yi)}=1,
where m is the number of pairs (e.g., m is 2 to 4). Each
task T also contains a few inference examples, denoted as:
Dinfer={(xi, Yi)}=1 (n is 1 or 2). At inference time, only
the demo pairs Den emo and one input Xinfer ∈ Dinfer are given,
and the model is required to infer the desired output Yinfer.
m
T
Training set. The training set consists of multiple tasks
used to train the model offline (i.e., before a new task is
given). We denote the training set as: Train={T}=1, where
k is the number of tasks (400 in ARC-1). Following stan-
dard machine learning protocols, samples in Demo for any
T∈ Ttrain can be used for training. The “inference" samples
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

L(0) = ET,i [D(yi, fo(xi | T))]. (1)

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
Figure 4. The raw input undergoes random scale and translation
transformations and is placed on the "canvas" (denoted in gray).
ses data augmentations encourage the model to learn un-
derlying mappings invariant to geometric transformations
grounded in the visual world. Formally, we perform:
• Scale augmentation: Given a raw input, we randomly
resize it by an integer scaling ratio s, duplicating each
raw pixel into sxs (see Fig. 4, left). This is analo-
gous to nearest-neighbor interpolation in natural im-
ages. However, note that "colors" in ARC do not cor-
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
[task]
place on canvas
patch embedding
Transformer block
Transformer block
predictor
off canvas
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
Offline training. This stage is applied on the entire train-
ing set Ttrain. It is on all demos DT demo for any T∈ Ttrain.
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
are consolidated by majority voting [1].2

Pass@2 accuracy. The ARC benchmark by default adopts
the pass@2 accuracy metric: i.e., two different solutions
can be produced for evaluation, and a task is considered
correct if one is correct. To support this metric, we adopt
majority voting in multi-view inference and retain the top-2
most populated output solutions.

4. Implementation Details
We describe the major implementation choices in this sec-
tion. The configuration details can be found in appendix.

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

Figure 6. Effect of test-time training. (Top): Demonstration ex-
amples for the current task. (Bottom left): An inference example
Xinfer. (Bottom right): During test-time training, the prediction
from Xinfer becomes progressively more accurate, with the model
finally generating the correct prediction.

Test-time training (TTT). Given a single new, unseen
task T∈ Ttest from the test set, we perform inference
by test-time training. At inference time, we are given
Demo={(xi, Yi)}m
i=1, with both input and output accessi-
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
5
Table 1. Vision backbones. We compare variants of ViTs and U-
Nets of similar sizes. U-Net settings are in appendix.

Figure 7. Effects of visual priors in VARC. Accuracy is reported
on the ARC-1 evaluation set. The model used is ViT-18M. En-
tries (a-c) use a patch size of 1×1 on a 32×32 canvas, whereas
entries (d-f) use a patch size of 2×2 on a 64×64 canvas. Each
entry modifies the one above it. We start from a naïve baseline
with components (b-f) removed. These vision priors cumulatively
yield 27.7 improvement (a→f), in which the canvas-based designs
(c→f) contribute an 11.5 gain.

5.1. Visual Priors
Fig. 7 summarizes the effects of visual priors, starting from
a baseline (a) without the other components in this figure.
These priors jointly have a gain of 27.7 points, where the
canvas-based designs (c-f) has a gain of 11.5 points. We
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
for frontier AI reasoning systems. arXiv:2505.11831, 2025.
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
sides. This is illustrated in Fig. 13.
Inference, we locate the rightmost and bottommost
[BD] tokens and crop the output accordingly to recover the final
predicted shape.
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
00
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
72.5-
70.0
67.5
Pass@k (Cumulative Success Rate)
Pass@k (Cumulative Success Rate)
12.5
Pass@k Curve for ARC-1
65.0-
50.0
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
50
100
150 200 250
300
Pass@k Curve for Ensemble ARC-2
Evaluation Accuracy (%)
60
50
40
30 20 10
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
250 500 750 1000 1250 1500 1750
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
aa4ec2a5
Vote: 13
Vote: 9
b457fec5
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
Vote: 21
Attempt 2
Vote: 20
Ground truth
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
Π
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
Π
Π
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
Π
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
+
TTT process
Input
Ground truth
Figure 22. Visualization of the test-time training process. Here, we visualize the grid augmented with a given scale ratio of 2× (the full canvas is not shown for brevity). As the test-time training progresses, the model's predictions gradually converge toward the correct output. In early epochs, the model produces coarse and imprecise structures; in later epochs, the model can improve the solutions, e.g., by refining color and spatial arrangement. This visualization illustrates the model's behavior of adapting to task-specific transformations through few-shot test-time training.
17

--- PAPER: FIGURES & TABLES ---
{
  "figures": [
    {
      "id": "Figure 1",
      "caption": "The ARC benchmark (top) consists of a collection of many different tasks, where each task has a few (e.g., 2-4) examples. We propose the Vision ARC (VARC) framework, which addresses the ARC problem as an image-to-image translation problem, from a computer vision perspective (bottom). In this illustration, the underlying concepts of the three tasks can be roughly described by humans as: \"reflection\" (left), \"symmetry\" (middle), and \"gravity\" (right). These concepts are closely related to the visual and physical world.",
      "description": "The figure is divided into a top section showing the ARC benchmark and a bottom section illustrating the VARC framework. The top section, labeled \"Training tasks\" and \"Test task\", shows small grids of colored squares. Under \"Training tasks\", two pairs of (X, y) grids are shown as examples. Under \"Test task\", one X grid is shown with a '?' for the y grid, indicating a prediction is needed. The bottom section, illustrating the VARC framework, shows three examples of \"Xinfer\" (input) and \"Yinfer\" (output) pairs, with a \"VARC network\" in the middle, leading to \"model prediction\". The first example (left) shows a 3x3 grid with a red square in the top-left transforming to a 3x3 grid with a red square in the bottom-right, representing reflection. The second example (middle) shows a 5x5 grid with a blue square in the center and a yellow square in the top-left transforming to a 5x5 grid with a blue square in the center and a yellow square in the bottom-right, representing symmetry. The third example (right) shows a 5x5 grid with a red square at the top and a blue square below it transforming to a 5x5 grid with the red square at the bottom and the blue square above it, representing gravity. Below these examples, a generic \"[TASK]\" input feeds into the \"VARC network\", which produces a \"model prediction\" output, showing the predicted outputs for the three example tasks: a 3x3 grid with a red square in the bottom-right, a 5x5 grid with a yellow square in the bottom-right, and a 5x5 grid with a red square at the bottom. The figure demonstrates how ARC tasks are framed as image-to-image translation problems within VARC."
    },
    {
      "id": "Figure 2",
      "caption": "Examples of unseen tasks solved by VARC. Each panel shows an unseen test task, with demonstrations on the top and the model's prediction on the bottom. VARC correctly solves these challenging tasks.",
      "description": "The figure displays three panels, each showing an unseen ARC task solved by VARC. Each panel consists of two demonstration pairs (X, y) at the top and an inference input (Xinfer) with the model's prediction at the bottom. The grids are composed of colored squares. The first panel, labeled \"ARC-1\" (left), shows: X (3x3, red top-left) -> y (3x3, red bottom-right); X (3x3, blue top-right) -> y (3x3, blue bottom-left). For Xinfer (3x3, yellow bottom-left), the model predicts a 3x3 grid with a yellow square in the top-right. The second panel, labeled \"ARC-2\" (middle), shows: X (3x3, red top-left, blue top-right) -> y (3x3, red bottom-left, blue bottom-right); X (3x3, yellow top-left, green top-right) -> y (3x3, yellow bottom-left, green bottom-right). For Xinfer (3x3, orange top-left, purple top-right), the model predicts a 3x3 grid with an orange square in the bottom-left and a purple square in the bottom-right. The third panel (right) shows: X (3x3, red top-left, blue middle-right) -> y (3x3, red top-left, blue middle-right); X (3x3, yellow top-left, green middle-right) -> y (3x3, yellow top-left, green middle-right). For Xinfer (3x3, orange top-left, purple middle-right), the model predicts a 3x3 grid with an orange square in the top-left and a purple square in the middle-right. The figure demonstrates VARC's ability to generalize to and correctly solve new, unseen tasks."
    },
    {
      "id": "Figure 3",
      "caption": "The ARC problem definition. ARC is a collection of many different tasks. For each task, a few (e.g., 2-4) demonstration pairs (x, y) are given, and the model is required to infer the output from Xinfer. The training set Ttrain is a collection of 400 tasks, which can be used for model training. The test set Ttest contains 400 new tasks: the demo pairs of a new task are given only at inference time, based on which the model performs inference on Xinfer.",
      "description": "The figure illustrates the ARC problem definition, distinguishing between training and test sets. The top-left section, \"Training Set Ttrain\", shows two example tasks: \"Task 1\" and \"Task 400\". For Task 1, two (X, y) pairs are shown: X (3x3 grid with green cross) -> y (3x3 grid with green square); X (3x3 grid with red cross) -> y (3x3 grid with red square). For Task 400, two (X, y) pairs are shown: X (3x3 grid with blue square) -> y (3x3 grid with blue square); X (3x3 grid with red square) -> y (3x3 grid with red square). The top-right section, \"Test Set Ttest\", also shows \"Task 1\" and \"Task 400\". For Test Task 1, the same two (X, y) demonstration pairs as in training are provided, followed by an \"Xinfer\" (3x3 grid with yellow cross) and a '?' for the unknown \"Yinfer\". Similarly, for Test Task 400, the same two (X, y) demonstration pairs are provided, followed by an \"Xinfer\" (3x3 grid with yellow square) and a '?' for the unknown \"Yinfer\". Arrows indicate that for training, all X and y are known, while for testing, only demo X,y pairs and Xinfer are known, and Yinfer must be inferred. The figure clarifies the setup where models learn from known (X,y) pairs in training and then predict y for unseen Xinfer in test tasks, using only a few demo pairs."
    },
    {
      "id": "Figure 4",
      "caption": "The raw input undergoes random scale and translation transformations and is placed on the \"canvas\" (denoted in gray).",
      "description": "The figure illustrates two data augmentation steps: Scale and Translation. The left panel, labeled \"Scale\", shows a \"Raw input\" which is a 3x3 grid containing a red L-shape, a yellow square, and a blue square. This is transformed into a \"Scaled input\", which is a 6x6 grid where each pixel of the raw input is duplicated into a 2x2 block, effectively scaling the original pattern by a factor of 2. The right panel, labeled \"Translation\", takes the \"Scaled input\" (the 6x6 grid from the previous step) and places it onto a larger gray \"canvas\". The scaled input is positioned within the canvas, not necessarily at the top-left corner, with the surrounding area filled by the gray canvas background. The figure demonstrates how raw input grids are first scaled up and then randomly translated onto a larger canvas for processing."
    },
    {
      "id": "Figure 5",
      "caption": "The ViT architecture in VARC. The input is randomly placed on a canvas, which is then treated as a natural image and processed by a standard ViT, conditioned on the task token.",
      "description": "The figure illustrates the Vision Transformer (ViT) architecture used in VARC. At the top, a small colored block represents the \"[task]\" token. Below this, a grid of colored squares, labeled \"place on canvas\", represents the input image after being randomly placed on a larger canvas. This canvas input is fed into a \"patch embedding\" module, which transforms the input into a sequence of embedded patches. The output of the \"patch embedding\" then passes through a stack of \"Transformer block\"s. The \"[task]\" token is shown feeding into both the \"patch embedding\" and each \"Transformer block\", indicating that the ViT is conditioned on this task-specific information. Finally, the output of the last \"Transformer block\" is fed into a \"predictor\" module, which generates the \"off canvas\" output, a grid of colored squares representing the model's prediction. The overall flow is: task token and canvas input are processed by patch embedding, then Transformer blocks, and finally a predictor to produce the output."
    },
    {
      "id": "Figure 6",
      "caption": "Effect of test-time training. (Top): Demonstration examples for the current task. (Bottom left): An inference example Xinfer. (Bottom right): During test-time training, the prediction from Xinfer becomes progressively more accurate, with the model finally generating the correct prediction.",
      "description": "The figure shows three panels related to test-time training. The top panel, labeled \"Ddemo\", shows 6 demonstration examples for a task, each with an input grid and an output grid. The bottom left panel, labeled \"Xinfer\", shows an inference example with an input grid. The bottom right panel, labeled \"prediction\", shows the progression of prediction from Xinfer during test-time training. It starts with an incorrect prediction, then shows an intermediate prediction that is closer, and finally the correct prediction. The qualitative trend is that test-time training improves prediction accuracy over time."
    },
    {
      "id": "Figure 7",
      "caption": "Effects of visual priors in VARC. Accuracy is reported on the ARC-1 evaluation set. The model used is ViT-18M. En- tries (a-c) use a patch size of 1×1 on a 32×32 canvas, whereas entries (d-f) use a patch size of 2×2 on a 64×64 canvas. Each entry modifies the one above it. We start from a naïve baseline with components (b-f) removed. These vision priors cumulatively yield 27.7 improvement (a→f), in which the canvas-based designs (c→f) contribute an 11.5 gain.",
      "description": "The figure is a horizontal bar chart showing accuracy (%) on the x-axis from 0 to 50, and different visual prior settings on the y-axis. There are 6 settings: (a) naïve baseline at 26.8%, (b) w/ 2D absolute pos embed at 32.8%, (c) w/ 2D ROPE at 43.0%, (d) 1x1 patch on 32x32 → 2x2 patch on 64x64 at 45.4%, (e) w/ translation aug. on canvas at 48.3%, and (f) w/ scale aug. on canvas at 54.5%. The qualitative trend is that adding visual priors progressively increases accuracy."
    },
    {
      "id": "Figure 8",
      "caption": "Scalability: ViTs with different width (x-axis) and depth. The circle areas de- note model sizes.",
      "description": "The figure is a scatter plot showing Accuracy (%) on the y-axis from 35 to 60, and width on the x-axis with values 256, 384, 512. There are two series: Depth = 5 and Depth = 10. For Depth = 5: width 256 has accuracy 41.0% (3M model size), width 384 has accuracy 44.4% (6M model size), width 512 has accuracy 47.0% (10M model size). For Depth = 10: width 256 has accuracy 47.0% (6M model size), width 384 has accuracy 51.6% (12M model size), width 512 has accuracy 54.5% (18M model size). The circle areas increase with model size. The qualitative trend is that increasing width and depth generally leads to higher accuracy."
    },
    {
      "id": "Figure 9",
      "caption": "TTT strategies: with vs. without offline train- ing, and joint vs. independent for each task.",
      "description": "The figure is a bar chart showing Accuracy (%) on the y-axis from 0 to 80, and four TTT strategies on the x-axis: TTT jointly and TTT independently, each with 'w/ offline training' and 'wo/ offline training' bars. For 'TTT jointly': 'wo/ offline training' is 26.4%, 'w/ offline training' is 44.8%. For 'TTT independently': 'wo/ offline training' is 29.1%, 'w/ offline training' is 54.5%. The qualitative trend is that offline training significantly improves accuracy, and independent TTT performs better than joint TTT."
    },
    {
      "id": "Figure 10",
      "caption": "Visualization of pixel-to-pixel attention. (Top): a test task from ARC-1 eval: showing demo pairs, inference input, and model prediction. (Middle): attention maps for a single pixel across different layers. With the highlighted pixel as query, we show pre-softmax logits. Different layers exhibit different behav- ior. (Bottom): attention maps in layer 8 with other query pixels. All of them correctly attend to their corresponding palette pixel.",
      "description": "The figure shows three main sections. The top section displays a test task from ARC-1 eval, including \"Ddemo\" (two input-output pairs), \"Xinfer\" (input for inference), and \"model prediction\" (the predicted output). The middle section shows attention maps for a single query pixel across different layers (Layer 0, Layer 1, Layer 2, Layer 3, Layer 4, Layer 5, Layer 6, Layer 7, Layer 8, Layer 9). Each layer's map shows pre-softmax logits, with values ranging from -1 to +1, indicating different attention patterns. For example, Layer 0 shows attention to the query pixel itself, Layer 3 shows attention to a horizontal line, Layer 4 shows attention to a vertical line, and Layer 8 shows attention to a diagonal line. The bottom section shows attention maps in Layer 8 for multiple query pixels, demonstrating that each query pixel correctly attends to its corresponding palette pixel. The qualitative trend is that different layers learn to attend to different features or relationships within the input grid."
    },
    {
      "id": "Figure 11",
      "caption": "Visualization of layer-wise attention maps. For each layer, we compute pixel-to-pixel attention and then average the softmax maps across all pixels to obtain a single map per layer. This map reveals which pixels are most attended in this layer. We show a test task from ARC-1 eval. In this task, some layers exhibit strong attention to the 3 × 3 neighborhood, reflecting the influence of the pattern's core. In comparison, some other layers (e.g., layers 7-9) focus on the outward-radiating rays, corresponding to the rule that extends colored pixels along the eight directions.",
      "description": "The figure shows a test task from ARC-1 eval, including \"Ddemo\" (two input-output pairs), \"Xinfer\" (input for inference), and \"model prediction\" (the predicted output). Below this, there are 10 layer-wise attention maps, from Layer 0 to Layer 9. Each map is an averaged softmax attention map across all pixels in that layer, with values ranging from 0.0 to 1.0. Layers 0-6 show strong attention to the central 3x3 neighborhood, with Layer 0 having a central peak and subsequent layers showing more diffuse attention within this region. Layers 7-9 show attention patterns that radiate outwards from the center, with Layer 7 showing a cross pattern, Layer 8 showing a diagonal cross pattern, and Layer 9 showing a more diffuse outward radiation. The qualitative trend is that early layers focus on local patterns (e.g., 3x3 neighborhood), while later layers capture more global, radiating patterns."
    },
    {
      "id": "Figure 12",
      "caption": "t-SNE of task embeddings, on the 400 task tokens learned from the ARC-1 training set. Each point represents a sin- gle task. To aid the reader, we provide human-written descriptions for the tasks (which are not used in any form by our method).",
      "description": "The figure displays a 2D t-SNE plot of 400 task embeddings. Each point on the plot represents a single task. Several clusters of tasks are highlighted with human-written descriptions. In the top-left, a cluster is labeled \"Use the blue layout in the blue box as the blueprint, fill its four regions with the four corner colors\" and \"Use the green layout in the blue box as the blueprint, fill its four regions with the small square of four colors.\" In the bottom-left, a cluster is labeled \"If a cell is black in both input grids, make it green. Otherwise leave it black.\" (repeated twice). In the top-right, a cluster is labeled \"Copy the small colored pattern center to the gray pixel.\" and \"Copy the small colored pattern center to the blue pixel.\" In the bottom-right, a cluster is labeled \"Expand the red pixel vertically with blue pixels, and expand pattern in four dimensions.\" and \"Expand the gray pixel diagonally with blue pixels, and expand pattern in four dimensions.\" The qualitative trend is that tasks with similar semantics cluster together in the embedding space."
    },
    {
      "id": "Figure 13",
      "caption": "Shape Handling. The gray pixels denote the back-ground tokens [BG], which keep the canvas size fixed (64×64 by default). The white pixels denote the border tokens [BD], which indicate the output shape. (Left): a pair (x, y) with a scaling ratio of 1x. (Right): a pair (x, y) with a scaling ratio of 2x.",
      "description": "The figure shows two examples of shape handling on a 64x64 pixel canvas. Both examples have a gray background, representing background tokens [BG]. The output shape is indicated by white pixels, representing border tokens [BD]. The left panel shows a 1x scaling ratio, where the output shape is a 16x16 square of white pixels in the top-left corner, with a one-pixel-wide border of white pixels along its right and bottom edges. The right panel shows a 2x scaling ratio, where the output shape is a 32x32 square of white pixels in the top-left corner, with a one-pixel-wide border of white pixels along its right and bottom edges. The figure illustrates how different scaling ratios affect the size of the output shape on a fixed canvas."
    },
    {
      "id": "Figure 14",
      "caption": "Offline training data scaling: effect of varying the number of RE-ARC samples per task, evaluated on the ARC-1 eval set. Increasing the amount of offline training data is beneficial, although even without it, our model can achieve decent accuracy.",
      "description": "The plot shows Evaluation Accuracy (%) on the y-axis, ranging from 0 to 60, and Offline Training RE-ARC Pairs Per Task (Log-scaled) on the x-axis, ranging from 0 to 1000. A single curve shows accuracy increasing with more training data. At 0 pairs per task, accuracy is 31.5%. At 10 pairs per task, accuracy is 38.6%. At 100 pairs per task, accuracy is 52.3%. At 1000 pairs per task, accuracy is 54.0%. The curve rises sharply initially and then flattens out. Increasing the number of RE-ARC samples per task improves evaluation accuracy, with diminishing returns."
    },
    {
      "id": "Figure 15",
      "caption": "Offline training task diversity scaling: effect of vary-ing the number of training tasks, evaluated on the ARC-1 eval set. Increasing task diversity is beneficial.",
      "description": "The plot shows Evaluation Accuracy (%) on the y-axis, ranging from 0 to 60, and Offline Training Task Diversity (Log-scaled) on the x-axis, ranging from 0 to 400. A single curve shows accuracy increasing with more training tasks. At 0 tasks, accuracy is 26.4%. At 16 tasks, accuracy is 43.1%. At 80 tasks, accuracy is 49.6%. At 400 tasks, accuracy is 54.5%. The curve rises sharply initially and then flattens out. Increasing the diversity of training tasks improves evaluation accuracy, with diminishing returns."
    },
    {
      "id": "Figure 16",
      "caption": "Pass@k results in the ARC-1 (left) and ARC-2 (right) evaluation sets. Results are obtained with majority voting from multi-view inference, using 510 views. (Top): using a single model of ViT-18M. (Bottom): using an ensemble of one ViT-18M and one U-Net-55M, each with test-time training run four times.",
      "description": "The figure displays four plots showing Pass@k (Cumulative Success Rate) on the y-axis against k (number of proposals) on the x-axis. The x-axis ranges from 0 to 300 for the top plots and 0 to 1750 for the bottom plots. The y-axis ranges from 0 to 72.5 for ARC-1 plots and 0 to 15 for ARC-2 plots. The top-left plot, 'Pass@k Curve for ARC-1' (single model), shows Pass@k increasing from 49.8 at k=1, to 54.5 at k=2, and to 66.3 at k=300. The top-right plot, 'Pass@k Curve for ARC-2' (single model), shows Pass@k increasing from 10.5 at k=1, to 10.0 at k=2, and to 14.0 at k=300. The bottom-left plot, 'Pass@k Curve for Ensemble ARC-1', shows Pass@k increasing from 55.0 at k=1, to 57.5 at k=2, and to 70.0 at k=1750. The bottom-right plot, 'Pass@k Curve for Ensemble ARC-2', shows Pass@k increasing from 12.5 at k=1, to 14.0 at k=2, and to 20.0 at k=1750. In all plots, Pass@k generally increases with k, indicating that more proposals lead to higher success rates."
    },
    {
      "id": "Figure 17",
      "caption": "Successful and failed examples on ARC-1. (Top): Examples of test tasks successfully solved by VARC. (Bottom): Examples of test tasks unsolved by VARC. (Left): Two demonstration example pairs shown for each task (some have more demonstrations not shown here). (Right): Inference input and the first and second solutions proposed by VARC. The green box indicates the correct output.",
      "description": "The figure displays successful and failed examples of ARC-1 tasks. The layout is divided into a 'Top' section for solved tasks and a 'Bottom' section for unsolved tasks. Each section contains four rows, with each row representing a distinct task identified by a hexadecimal ID. For each task, there are six columns: 'Demonstration 1' (input/output pair), 'Demonstration 2' (input/output pair), 'Input' (for inference), 'Attempt 1' (proposed solution with vote count), 'Attempt 2' (proposed solution with vote count), and 'Ground truth'.\n\nIn the 'Top' (Solved) section:\n- Task 15663ba9: Attempt 1 has Vote: 109, Attempt 2 has Vote: 57. The Ground truth is enclosed in a green box.\n- Task 981571dc: Attempt 1 has Vote: 399, Attempt 2 has Vote: 35. The Ground truth is enclosed in a green box.\n- Task 15696249: Attempt 1 has Vote: 456, Attempt 2 has Vote: 10. The Ground truth is enclosed in a green box.\n- Task 67c52801: Attempt 1 has Vote: 233, Attempt 2 has Vote: 123. The Ground truth is enclosed in a green box.\n\nIn the 'Bottom' (Unsolved) section:\n- Task 8dae5dfc: Attempt 1 has Vote: 9, Attempt 2 has Vote: 6. The Ground truth is not enclosed in a green box.\n- Task 67636eac: Attempt 1 has Vote: 14, Attempt 2 has Vote: 8. The Ground truth is not enclosed in a green box.\n- Task aa4ec2a5: Attempt 1 has Vote: 13, Attempt 2 has Vote: 9. The Ground truth is not enclosed in a green box.\n- Task b457fec5: Attempt 1 has Vote: 3, Attempt 2 has Vote: 2. The Ground truth is not enclosed in a green box.\n\nThe green box around the 'Ground truth' indicates a correct output by VARC. The figure demonstrates VARC's performance on ARC-1 tasks, showing both successful and unsuccessful attempts, along with the voting scores for the proposed solutions."
    },
    {
      "id": "Figure 18",
      "caption": "Successful and failed examples on ARC-2. (Top): Examples of test tasks successfully solved by VARC. (Bottom): Examples of test tasks unsolved by VARC. (Left): Two demonstration example pairs shown for each task (some have more demonstrations not shown here). (Right): Inference input and the first and second solutions proposed by VARC. The green box indicates the correct output.",
      "description": "The figure presents successful and failed examples of ARC-2 tasks, structured similarly to Figure 17. It is divided into a 'Top' section for solved tasks and a 'Bottom' section for unsolved tasks, each containing four rows representing distinct tasks identified by hexadecimal IDs. For each task, there are six columns: 'Demonstration 1' (input/output pair), 'Demonstration 2' (input/output pair), 'Input' (for inference), 'Attempt 1' (proposed solution with vote count), 'Attempt 2' (proposed solution with vote count), and 'Ground truth'.\n\nIn the 'Top' (Solved) section:\n- Task 800d221b: Attempt 1 has Vote: 99, Attempt 2 has Vote: 82. The Ground truth is enclosed in a green box.\n- Task 7666fa5d: Attempt 1 has Vote: 410, Attempt 2 has Vote: 16. The Ground truth is enclosed in a green box.\n- Task 221dfab4: Attempt 1 has Vote: 30, Attempt 2 has Vote: 17. The Ground truth is enclosed in a green box.\n- Task 7b80bb43: Attempt 1 has Vote: 168, Attempt 2 has Vote: 44. The Ground truth is enclosed in a green box.\n\nIn the 'Bottom' (Unsolved) section:\n- Task 2b83f449: Attempt 1 has Vote: 21, Attempt 2 has Vote: 20. The Ground truth is not enclosed in a green box.\n- Task 2d0172a1: Attempt 1 has Vote: 7, Attempt 2 has Vote: 6. The Ground truth is not enclosed in a green box.\n- Task 3e6067c3: Attempt 1 has Vote: 14, Attempt 2 has Vote: 12. The Ground truth is not enclosed in a green box.\n- Task 7ed72f31: Attempt 1 has Vote: 67, Attempt 2 has Vote: 51. The Ground truth is not enclosed in a green box.\n\nThe green box around the 'Ground truth' indicates a correct output by VARC. The figure illustrates VARC's performance on ARC-2 tasks, showing both successful and unsuccessful attempts, along with the voting scores for the proposed solutions."
    },
    {
      "id": "Figure 19",
      "caption": "Ambiguous examples. Although most ARC tasks are unambiguous, some may admit multiple plausible explanations or rules. Here, in the given three demonstration examples of a test task (top panel), it is unclear whether a blue line \"touching\" (but not \"going through\") a red rectangle should render that rectangle blue. The inference example (bottom panel) involves this situation (\"touching\"), and our model attempts to interpret the rule as either \"going-through-only\" (attempt 1) or \"touching\" (attempt 2).",
      "description": "The figure illustrates ambiguous ARC tasks. The top panel, labeled 'Demonstration Examples', shows three input-output pairs. In each pair, the input contains a red rectangle and a blue line. The output consistently shows the blue line inside the red rectangle, turning the rectangle blue.\n- Example 1: Input has a blue line touching the top edge of a red rectangle. Output shows the blue line inside the now blue rectangle.\n- Example 2: Input has a blue line touching the left edge of a red rectangle. Output shows the blue line inside the now blue rectangle.\n- Example 3: Input has a blue line passing through a red rectangle. Output shows the blue line inside the now blue rectangle.\n\nThe bottom panel shows an 'Inference' example with an 'Input', 'Attempt 1', 'Attempt 2', and 'Ground truth'.\n- Input: A red rectangle with a blue line touching its top-left corner.\n- Attempt 1: Shows the blue line inside the red rectangle, with the rectangle remaining red. This interprets the rule as 'going-through-only' for the color change.\n- Attempt 2: Shows the blue line inside the red rectangle, with the rectangle turning blue. This interprets the rule as 'touching' for the color change.\n- Ground truth: Shows the blue line inside the red rectangle, with the rectangle turning blue.\n\nThe figure highlights the ambiguity in interpreting whether a 'touching' blue line should trigger the same transformation (turning the rectangle blue) as a 'going through' blue line, and how the model provides two plausible interpretations."
    },
    {
      "id": "Figure 20",
      "caption": "Additional visualization: pixel-level attention maps. The maps are shown for different Transformer blocks, with a query pixel highlighted by a red-yellow border. Here we show 4 test tasks in ARC eval. Layers at different depths tend to focus on different structures. Early layers tend to focus on local transformations and context. Middle layers tend to perform a more non-local connection, e.g., horizontally or vertically. The deep layers are more task-specialized. The red asterisk indicates the task that was not correctly solved. (Here, the text descriptions are written by humans solely to help readers interpret the tasks.)",
      "description": "The figure displays pixel-level attention maps for four ARC tasks, showing how Transformer blocks focus at different depths. Each task includes an input-output pair and 'Intermediate Heatmaps' categorized as 'Early', 'Mid', and 'Late' stages, with specific 'Block' numbers indicated.\n\n1.  **Task 09c534e7* (Not correctly solved):** \"Fill in the interior of the connected boxes with the same color.\"\n    -   Input: A grid with connected boxes of different colors.\n    -   Output: The connected boxes filled with a uniform color.\n    -   Early Heatmaps: Blocks 2, 4, 5 are shown.\n    -   Mid Heatmaps: Blocks 2, 4, 5 are shown.\n    -   Late Heatmaps: Block 6 shows \"Attention is focused within the rectangle.\"\n\n2.  **Task 506d28a5:** \"Logical OR between the upper and lower parts of the input.\"\n    -   Input: A grid divided into upper and lower parts with colored pixels.\n    -   Output: A grid representing the logical OR of the upper and lower parts.\n    -   Early Heatmaps: Blocks 1, 4, 5 are shown.\n    -   Mid Heatmaps: Blocks 1, 4, 5 are shown.\n    -   Late Heatmaps: Block 7 shows \"Attention focuses on the corresponding cell in the lower part of the grid.\"\n\n3.  **Task 0607ce86:** \"Remove visual noise from a regular, repeating grid pattern.\"\n    -   Input: A grid with a repeating pattern and some 'noise' pixels.\n    -   Output: The grid with the noise removed, showing a clean repeating pattern.\n    -   Early Heatmaps: Blocks 2, 4, 5 are shown.\n    -   Mid Heatmaps: Blocks 2, 4, 5 are shown.\n    -   Late Heatmaps: Block 7 shows \"Attention focuses on other cells in the same relative position within the grid.\"\n\n4.  **Task 070dd51e:** \"Connect horizontal or vertical lines, with vertical lines being on top.\"\n    -   Input: A grid with disconnected horizontal and vertical line segments.\n    -   Output: A grid with connected lines, where vertical lines appear on top of horizontal ones at intersections.\n    -   Early Heatmaps: Block 3 shows \"Attention focuses on endpoints of all lines for all pixels.\", Blocks 4, 5 are also shown.\n    -   Mid Heatmaps: Blocks 3, 4, 5 are shown.\n    -   Late Heatmaps: Block 7 shows \"Attention focuses on nearby, relevant lines only, focusing strongest on the correct line.\"\n\nThe figure demonstrates that attention patterns evolve through Transformer layers, from local context in early layers to more specialized, task-specific focus in deeper layers."
    },
    {
      "id": "Figure 21",
      "caption": "Additional visualization: layer-wise attention maps. Each map is the per-pixel softmax attention maps averaged across all pixels in that layer. The corresponding demonstration examples (on the left) are provided for reference.",
      "description": "The figure presents layer-wise attention maps for four ARC tasks, illustrating the average per-pixel softmax attention across different Transformer layers. For each task, the left side shows 'demonstrations' (input-output pairs) used for reference, and the right side shows the 'inference' process, including the input, the model's output, and the ground truth.\n\nBelow the inference section for each task, a grid of attention maps is displayed, labeled 'Layer 0' through 'Layer 9'. A color bar on the far right indicates attention intensity from 0.0 (dark blue) to 1.0 (bright yellow).\n\n1.  **Task 0607ce86 example 0:** Shows two demonstration examples, followed by the inference input, output, and ground truth. Attention maps for Layers 0-9 are displayed.\n2.  **Task 0bb8deee example 0:** Shows two demonstration examples, followed by the inference input, output, and ground truth. Attention maps for Layers 0-9 are displayed.\n3.  **Task 1c56ad9f example 0:** Shows two demonstration examples, followed by the inference input, output, and ground truth. Attention maps for Layers 0-9 are displayed.\n4.  **Task 1d0a4b61 example 0:** Shows two demonstration examples (labeled 'Train Example 1' and 'Train Example 2'), followed by the inference input, output, and ground truth. Attention maps for Layers 0-9 are displayed.\n\nThe figure visually represents how attention is distributed across different layers of the Transformer model during the inference process for various ARC tasks, with varying patterns of activation visible across the layers."
    },
    {
      "id": "Figure 22",
      "caption": "Visualization of the test-time training process. Here, we visualize the grid augmented with a given scale ratio of 2× (the full canvas is not shown for brevity). As the test-time training progresses, the model's predictions gradually converge toward the correct output. In early epochs, the model produces coarse and imprecise structures; in later epochs, the model can improve the solutions, e.g., by refining color and spatial arrangement. This visualization illustrates the model's behavior of adapting to task-specific transformations through few-shot test-time training.",
      "description": "The figure displays three distinct test-time training (TTT) processes, each identified by a unique hexadecimal ID: 55059096, 0c786b71, and ac3e2b04. Each TTT process is shown across two demonstrations (Demonstration 1 and Demonstration 2) and includes four stages: Input, TTT process, and Ground truth. The 'TTT process' stage is represented by a sequence of intermediate predictions, illustrating the model's convergence.\n\nFor ID 55059096:\n- Demonstration 1: Input shows a 3x3 grid with a green cross in the center. The TTT process shows 5 intermediate steps, starting with a coarse green cross and gradually refining it. The Ground truth shows a precise green cross.\n- Demonstration 2: Input shows a 3x3 grid with a red square in the center. The TTT process shows 5 intermediate steps, starting with a coarse red square and gradually refining it. The Ground truth shows a precise red square.\n\nFor ID 0c786b71:\n- Demonstration 1: Input shows a 3x3 grid with an orange square in the center. The TTT process shows 5 intermediate steps, starting with a coarse orange square and gradually refining it. The Ground truth shows a precise orange square.\n- Demonstration 2: Input shows a 3x3 grid with a purple square in the center. The TTT process shows 5 intermediate steps, starting with a coarse purple square and gradually refining it. The Ground truth shows a precise purple square.\n\nFor ID ac3e2b04:\n- Demonstration 1: Input shows a 3x3 grid with a blue pattern (a 2x2 square in the top-left corner). The TTT process shows 5 intermediate steps, starting with a coarse blue pattern and gradually refining it. The Ground truth shows a precise blue pattern.\n- Demonstration 2: Input shows a 3x3 grid with a grid-like pattern of blue and black squares. The TTT process shows 5 intermediate steps, starting with a coarse grid pattern and gradually refining it. The Ground truth shows a precise grid pattern.\n\nAcross all examples, the 'TTT process' panels show a progression from an initial, often blurry or incomplete, prediction towards a clear and accurate representation that matches the 'Ground truth'. This illustrates that as test-time training progresses, the model's predictions gradually converge toward the correct output, refining color and spatial arrangement."
    }
  ],
  "tables": [
    {
      "id": "Table 1",
      "caption": "Vision backbones. We compare variants of ViTs and U- Nets of similar sizes. U-Net settings are in appendix.",
      "columns": [
        "model",
        "width",
        "depth",
        "#params",
        "Gflops",
        "acc."
      ],
      "rows": [
        {
          "model": "ViT",
          "width": "384",
          "depth": "5",
          "#params": "6M",
          "Gflops": "10",
          "acc.": "44.4"
        },
        {
          "model": "ViT",
          "width": "512",
          "depth": "10",
          "#params": "18M",
          "Gflops": "28",
          "acc.": "54.5"
        },
        {
          "model": "ViT",
          "width": "768",
          "depth": "20",
          "#params": "66M",
          "Gflops": "99",
          "acc.": "53.0"
        },
        {
          "model": "U-Net",
          "width": "setting (a)",
          "depth": "",
          "#params": "7M",
          "Gflops": "18",
          "acc.": "42.8"
        },
        {
          "model": "U-Net",
          "width": "setting (b)",
          "depth": "",
          "#params": "17M",
          "Gflops": "33",
          "acc.": "47.5"
        },
        {
          "model": "U-Net",
          "width": "setting (c)",
          "depth": "",
          "#params": "55M",
          "Gflops": "87",
          "acc.": "48.3"
        }
      ],
      "reads": "This table compares different vision backbones (ViT and U-Net) across various sizes, showing that ViT models generally achieve higher accuracy than U-Net models for similar parameter counts and Gflops."
    },
    {
      "id": "Table 2",
      "caption": "Single-view vs. multi-view inference.",
      "columns": [
        "",
        "single-view, pass@1",
        "multi-view, pass@1",
        "multi-view, pass@2"
      ],
      "rows": [
        {
          "col": "",
          "single-view, pass@1": "35.9",
          "multi-view, pass@1": "49.8",
          "multi-view, pass@2": "54.5"
        }
      ],
      "reads": "This table compares different inference strategies, showing that multi-view inference significantly improves accuracy over single-view inference, and pass@2 further boosts performance."
    },
    {
      "id": "Table 3",
      "caption": "System-level comparisons on the ARC-1 and ARC-2 benchmarks. LLM-based results are from the ARC-AGI leader- board [18]. HRM, TRM, and our VARC are trained from scratch only on ARC data. Our single-model result is based on ViT, with mean±std of 54.5±0.7 (ARC-1) and 8.3±0.4 (ARC-2) over four runs. Our ensemble result aggregates an 18M ViT and a 55M U-Net, each with test-time training performed four times.",
      "columns": [
        "system",
        "#params",
        "ARC-1",
        "ARC-2"
      ],
      "rows": [
        {
          "system": "large language models (LLMs)",
          "#params": "",
          "ARC-1": "",
          "ARC-2": ""
        },
        {
          "system": "Deepseek R1 [21]",
          "#params": "671B",
          "ARC-1": "15.8",
          "ARC-2": "1.3"
        },
        {
          "system": "Claude 3.7 8k [18]",
          "#params": "N/A",
          "ARC-1": "21.2",
          "ARC-2": "0.9"
        },
        {
          "system": "o3-mini-high [18]",
          "#params": "N/A",
          "ARC-1": "34.5",
          "ARC-2": "3.0"
        },
        {
          "system": "GPT-5 [18]",
          "#params": "N/A",
          "ARC-1": "44.0",
          "ARC-2": "1.9"
        },
        {
          "system": "Grok-4-thinking [18]",
          "#params": "1.7T",
          "ARC-1": "66.7",
          "ARC-2": "16.0"
        },
        {
          "system": "Bespoke (Grok-4) [8]",
          "#params": "1.7T",
          "ARC-1": "79.6",
          "ARC-2": "29.4"
        },
        {
          "system": "recurrent models",
          "#params": "",
          "ARC-1": "",
          "ARC-2": ""
        },
        {
          "system": "HRM [53]",
          "#params": "27M",
          "ARC-1": "40.3",
          "ARC-2": "5.0"
        },
        {
          "system": "TRM [27]",
          "#params": "7M",
          "ARC-1": "44.6",
          "ARC-2": "7.8"
        },
        {
          "system": "vision models",
          "#params": "",
          "ARC-1": "",
          "ARC-2": ""
        },
        {
          "system": "VARC",
          "#params": "18M",
          "ARC-1": "54.5",
          "ARC-2": "8.3"
        },
        {
          "system": "VARC (ensemble)",
          "#params": "73M",
          "ARC-1": "60.4",
          "ARC-2": "11.1"
        },
        {
          "system": "human results",
          "#params": "",
          "ARC-1": "",
          "ARC-2": ""
        },
        {
          "system": "avg. human [31]",
          "#params": "-",
          "ARC-1": "60.2",
          "ARC-2": ""
        },
        {
          "system": "best human [18]",
          "#params": "-",
          "ARC-1": "98.0",
          "ARC-2": "100.0"
        }
      ],
      "reads": "This table compares various systems (LLMs, recurrent models, vision models, and human results) on ARC-1 and ARC-2 benchmarks, showing that VARC (ensemble) achieves competitive performance with average human results on ARC-1, and outperforms other models trained from scratch on ARC data."
    },
    {
      "id": "Table 4",
      "caption": "Configurations.",
      "columns": [
        "",
        "offline training",
        "test-time training"
      ],
      "rows": [
        {
          "": "epochs",
          "offline training": "100",
          "test-time training": "100"
        },
        {
          "": "warmup epochs",
          "offline training": "10",
          "test-time training": "10"
        },
        {
          "": "optimizer",
          "offline training": "Adam [28], betas=(0.9, 0.999)",
          "test-time training": "Adam [28], betas=(0.9, 0.999)"
        },
        {
          "": "batch size",
          "offline training": "32",
          "test-time training": "8"
        },
        {
          "": "learning rate",
          "offline training": "3e-4",
          "test-time training": "3e-4"
        },
        {
          "": "learning rate scheduler",
          "offline training": "cosine",
          "test-time training": "cosine"
        },
        {
          "": "weight decay",
          "offline training": "0",
          "test-time training": "0"
        },
        {
          "": "dropout",
          "offline training": "0.1",
          "test-time training": "0.1"
        }
      ],
      "reads": "This table compares the configurations for offline and test-time training, showing that most hyperparameters are kept consistent, with differences in batch size and epochs."
    },
    {
      "id": "Table 5",
      "caption": "Running time of the ViT-18M model. The reported time is obtained with torch.compile optimization.",
      "columns": [
        "",
        "offline training",
        "test-time training"
      ],
      "rows": [
        {
          "": "GPU type",
          "offline training": "H100",
          "test-time training": "H100"
        },
        {
          "": "GPU number",
          "offline training": "8",
          "test-time training": "1"
        },
        {
          "": "GPU time",
          "offline training": "4.8 hours",
          "test-time training": "0.7s per epoch"
        }
      ],
      "reads": "This table compares the GPU type, number, and time for offline and test-time training, showing that offline training uses more GPUs and takes significantly longer."
    },
    {
      "id": "Table 6",
      "caption": "Configuration of the ViT architecture. The 18M model is our default setting.",
      "columns": [
        "",
        "6M",
        "18M",
        "66M"
      ],
      "rows": [
        {
          "": "hidden dim",
          "6M": "384",
          "18M": "512",
          "66M": "768"
        },
        {
          "": "Transformer blocks",
          "6M": "5",
          "18M": "10",
          "66M": "20"
        },
        {
          "": "# heads",
          "6M": "8",
          "18M": "8",
          "66M": "12"
        },
        {
          "": "MLP block hidden dim",
          "6M": "512",
          "18M": "512",
          "66M": "512"
        },
        {
          "": "dropout",
          "6M": "0.1",
          "18M": "0.1",
          "66M": "0.1"
        },
        {
          "": "patch size",
          "6M": "2x2",
          "18M": "2x2",
          "66M": "2x2"
        },
        {
          "": "canvas size",
          "6M": "64x64",
          "18M": "64x64",
          "66M": "64x64"
        }
      ],
      "reads": "This table compares the configurations of three ViT models (6M, 18M, 66M), showing that larger models have increased hidden dimensions, more Transformer blocks, and more heads, while other parameters remain constant."
    },
    {
      "id": "Table 7",
      "caption": "Configuration of the U-Net architecture. The definition follows standard U-Nets used in generative models [47, 15].",
      "columns": [
        "",
        "7M",
        "17M",
        "55M"
      ],
      "rows": [
        {
          "": "# stages",
          "7M": "3",
          "17M": "3",
          "55M": "3"
        },
        {
          "": "layers per stage",
          "7M": "1",
          "17M": "1",
          "55M": "2"
        },
        {
          "": "# channels at resolution 1",
          "7M": "80",
          "17M": "120",
          "55M": "160"
        },
        {
          "": "attention at resolution 1",
          "7M": "No",
          "17M": "No",
          "55M": "No"
        },
        {
          "": "# channels at resolution 2",
          "7M": "160",
          "17M": "240",
          "55M": "320"
        },
        {
          "": "attention at resolution 2",
          "7M": "Yes",
          "17M": "Yes",
          "55M": "Yes"
        },
        {
          "": "# channels at resolution 3",
          "7M": "160",
          "17M": "240",
          "55M": "320"
        },
        {
          "": "attention at resolution 3",
          "7M": "Yes",
          "17M": "Yes",
          "55M": "Yes"
        },
        {
          "": "mid block",
          "7M": "No",
          "17M": "No",
          "55M": "Yes"
        }
      ],
      "reads": "This table compares the configurations of three U-Net models (7M, 17M, 55M), showing that larger models have more layers per stage, more channels at each resolution, and attention at resolution 3 and a mid block."
    }
  ]
}
--- CIO CARDS (observations) ---
[
  {
    "cio_id": "CIO_001",
    "unit": "U001",
    "context": [
      "C24",
      "C25",
      "C26"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": "E2",
    "pattern": "P8",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Section 1",
      "source_span": "S38"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_002",
    "unit": "U001",
    "context": [
      "C24",
      "C26"
    ],
    "intervention": "C24",
    "reference": "C13",
    "eval_metric": "E2",
    "pattern": "P9",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Section 1",
      "source_span": "S39"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_003",
    "unit": "U001",
    "context": [
      "C24"
    ],
    "intervention": "I13",
    "reference": "C24",
    "eval_metric": "E2",
    "pattern": "P11",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Section 1",
      "source_span": "S41"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_004",
    "unit": "U001",
    "context": [
      "C23"
    ],
    "intervention": "I13",
    "reference": null,
    "eval_metric": "E2",
    "pattern": "P12",
    "direction": "flat",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Section 1",
      "source_span": "S41"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_005",
    "unit": "U004",
    "context": [
      "C35"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P16",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 2",
      "source_span": "S55"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_006",
    "unit": "U014",
    "context": [],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P17",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 6",
      "source_span": "S139"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_007",
    "unit": "U017",
    "context": [
      "C281"
    ],
    "intervention": "C281",
    "reference": null,
    "eval_metric": "E40",
    "pattern": "P88",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 1",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_008",
    "unit": "U017",
    "context": [
      "C282"
    ],
    "intervention": "C282",
    "reference": null,
    "eval_metric": "E40",
    "pattern": "P89",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 1",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_009",
    "unit": "U017",
    "context": [
      "C283"
    ],
    "intervention": "C283",
    "reference": null,
    "eval_metric": "E40",
    "pattern": "P90",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 1",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_010",
    "unit": "U017",
    "context": [
      "C284"
    ],
    "intervention": "C284",
    "reference": null,
    "eval_metric": "E40",
    "pattern": "P91",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 1",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_011",
    "unit": "U017",
    "context": [
      "C285"
    ],
    "intervention": "C285",
    "reference": null,
    "eval_metric": "E40",
    "pattern": "P92",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 1",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_012",
    "unit": "U017",
    "context": [
      "C286"
    ],
    "intervention": "C286",
    "reference": null,
    "eval_metric": "E40",
    "pattern": "P93",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 1",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_013",
    "unit": "U017",
    "context": [
      "I49"
    ],
    "intervention": "C110",
    "reference": "C113",
    "eval_metric": "E8",
    "pattern": "P19",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Table 1",
      "source_span": "S191"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_014",
    "unit": "U018",
    "context": [
      "C116",
      "C118",
      "I51"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": "E9",
    "pattern": "P20",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Figure 7",
      "source_span": "S198"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_015",
    "unit": "U018",
    "context": [
      "C116",
      "C118"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": "E9",
    "pattern": "P21",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Figure 7",
      "source_span": "S198"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_016",
    "unit": "U019",
    "context": [],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P22",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Section 5.1",
      "source_span": "S200"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_017",
    "unit": "U019",
    "context": [],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P23",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Section 5.1",
      "source_span": "S200"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_018",
    "unit": "U019",
    "context": [
      "C120"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P24",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Section 5.1",
      "source_span": "S202"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_019",
    "unit": "U019",
    "context": [
      "C121"
    ],
    "intervention": "I53",
    "reference": null,
    "eval_metric": null,
    "pattern": "P25",
    "direction": "down",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Section 5.1",
      "source_span": "S204"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_020",
    "unit": "U019",
    "context": [
      "C122",
      "C123"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P26",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Section 5.1",
      "source_span": "S208"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_021",
    "unit": "U019",
    "context": [
      "I54",
      "C124",
      "C125"
    ],
    "intervention": "I55",
    "reference": null,
    "eval_metric": null,
    "pattern": "P28",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Section 5.1",
      "source_span": "S215"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_022",
    "unit": "U019",
    "context": [
      "C127"
    ],
    "intervention": "I58",
    "reference": null,
    "eval_metric": null,
    "pattern": "P34",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Section 5.1",
      "source_span": "S228"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_023",
    "unit": "U019",
    "context": [
      "C127"
    ],
    "intervention": "I59",
    "reference": null,
    "eval_metric": null,
    "pattern": "P35",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Section 5.1",
      "source_span": "S230"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_024",
    "unit": "U020",
    "context": [
      "C126"
    ],
    "intervention": "I56",
    "reference": null,
    "eval_metric": "E10",
    "pattern": "P29",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Figure 8",
      "source_span": "S219"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_025",
    "unit": "U021",
    "context": [],
    "intervention": null,
    "reference": null,
    "eval_metric": "E11",
    "pattern": "P30",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Figure 9",
      "source_span": "S222"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_026",
    "unit": "U021",
    "context": [],
    "intervention": null,
    "reference": null,
    "eval_metric": "E11",
    "pattern": "P31",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Figure 9",
      "source_span": "S223"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_027",
    "unit": "U022",
    "context": [
      "C129",
      "I60",
      "C130"
    ],
    "intervention": "I60",
    "reference": "I60",
    "eval_metric": null,
    "pattern": "P36",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Section 5.2",
      "source_span": "S236"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_028",
    "unit": "U022",
    "context": [
      "C131",
      "I61"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P38",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Section 5.2",
      "source_span": "S239"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_029",
    "unit": "U022",
    "context": [
      "C132"
    ],
    "intervention": "C132",
    "reference": null,
    "eval_metric": null,
    "pattern": "P39",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Section 5.2",
      "source_span": "S241"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_030",
    "unit": "U022",
    "context": [
      "C133",
      "I62"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P40",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Section 5.2",
      "source_span": "S244"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_031",
    "unit": "U022",
    "context": [
      "C133",
      "I62"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P41",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Section 5.2",
      "source_span": "S245"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_032",
    "unit": "U022",
    "context": [
      "C134"
    ],
    "intervention": null,
    "reference": "C134",
    "eval_metric": null,
    "pattern": "P42",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Section 5.2",
      "source_span": "S246"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_033",
    "unit": "U022",
    "context": [
      "C133",
      "I62"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P43",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Section 5.2",
      "source_span": "S247"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_034",
    "unit": "U022",
    "context": [
      "C135",
      "I63"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": "E12",
    "pattern": "P44",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Section 5.2",
      "source_span": "S255"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_035",
    "unit": "U022",
    "context": [
      "C135",
      "C136"
    ],
    "intervention": "C136",
    "reference": null,
    "eval_metric": "E12",
    "pattern": "P45",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Section 5.2",
      "source_span": "S255"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_036",
    "unit": "U023",
    "context": [
      "C287"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": "E41",
    "pattern": "P94",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 2",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_037",
    "unit": "U023",
    "context": [
      "C287"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": "E42",
    "pattern": "P95",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 2",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_038",
    "unit": "U023",
    "context": [
      "C287"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": "E43",
    "pattern": "P96",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 2",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_039",
    "unit": "U025",
    "context": [
      "C141"
    ],
    "intervention": "C297",
    "reference": null,
    "eval_metric": "E16",
    "pattern": "P46",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": "S262"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_040",
    "unit": "U025",
    "context": [
      "C141"
    ],
    "intervention": "C297",
    "reference": null,
    "eval_metric": "E16",
    "pattern": "P47",
    "direction": "flat",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": "S263"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_041",
    "unit": "U024",
    "context": [
      "C143",
      "C144"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P48",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Section 5.3",
      "source_span": "S264"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_042",
    "unit": "U024",
    "context": [
      "C145"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P49",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Section 5.3",
      "source_span": "S267"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_043",
    "unit": "U024",
    "context": [
      "C145"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": "E16",
    "pattern": "P50",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Section 5.3",
      "source_span": "S268"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_044",
    "unit": "U024",
    "context": [],
    "intervention": "I65",
    "reference": null,
    "eval_metric": null,
    "pattern": "P51",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Section 5.3",
      "source_span": "S271"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_045",
    "unit": "U024",
    "context": [],
    "intervention": "I65",
    "reference": null,
    "eval_metric": null,
    "pattern": "P52",
    "direction": "flat",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Section 5.3",
      "source_span": "S272"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_046",
    "unit": "U025",
    "context": [
      "C288"
    ],
    "intervention": "C288",
    "reference": null,
    "eval_metric": "E44",
    "pattern": "P97",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_047",
    "unit": "U025",
    "context": [
      "C288"
    ],
    "intervention": "C288",
    "reference": null,
    "eval_metric": "E45",
    "pattern": "P98",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_048",
    "unit": "U025",
    "context": [
      "C289"
    ],
    "intervention": "C289",
    "reference": null,
    "eval_metric": "E44",
    "pattern": "P99",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_049",
    "unit": "U025",
    "context": [
      "C289"
    ],
    "intervention": "C289",
    "reference": null,
    "eval_metric": "E45",
    "pattern": "P100",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_050",
    "unit": "U025",
    "context": [
      "C290"
    ],
    "intervention": "C290",
    "reference": null,
    "eval_metric": "E44",
    "pattern": "P101",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_051",
    "unit": "U025",
    "context": [
      "C290"
    ],
    "intervention": "C290",
    "reference": null,
    "eval_metric": "E45",
    "pattern": "P102",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_052",
    "unit": "U025",
    "context": [
      "C291"
    ],
    "intervention": "C291",
    "reference": null,
    "eval_metric": "E44",
    "pattern": "P103",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_053",
    "unit": "U025",
    "context": [
      "C291"
    ],
    "intervention": "C291",
    "reference": null,
    "eval_metric": "E45",
    "pattern": "P104",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_054",
    "unit": "U025",
    "context": [
      "C292"
    ],
    "intervention": "C292",
    "reference": null,
    "eval_metric": "E44",
    "pattern": "P105",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_055",
    "unit": "U025",
    "context": [
      "C292"
    ],
    "intervention": "C292",
    "reference": null,
    "eval_metric": "E45",
    "pattern": "P106",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_056",
    "unit": "U025",
    "context": [
      "C293"
    ],
    "intervention": "C293",
    "reference": null,
    "eval_metric": "E44",
    "pattern": "P107",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_057",
    "unit": "U025",
    "context": [
      "C293"
    ],
    "intervention": "C293",
    "reference": null,
    "eval_metric": "E45",
    "pattern": "P108",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_058",
    "unit": "U025",
    "context": [
      "C294"
    ],
    "intervention": "C294",
    "reference": null,
    "eval_metric": "E44",
    "pattern": "P109",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_059",
    "unit": "U025",
    "context": [
      "C294"
    ],
    "intervention": "C294",
    "reference": null,
    "eval_metric": "E45",
    "pattern": "P110",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_060",
    "unit": "U025",
    "context": [
      "C295"
    ],
    "intervention": "C295",
    "reference": null,
    "eval_metric": "E44",
    "pattern": "P111",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_061",
    "unit": "U025",
    "context": [
      "C295"
    ],
    "intervention": "C295",
    "reference": null,
    "eval_metric": "E45",
    "pattern": "P112",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_062",
    "unit": "U025",
    "context": [
      "C296"
    ],
    "intervention": "C296",
    "reference": null,
    "eval_metric": "E44",
    "pattern": "P113",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_063",
    "unit": "U025",
    "context": [
      "C296"
    ],
    "intervention": "C296",
    "reference": null,
    "eval_metric": "E45",
    "pattern": "P114",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_064",
    "unit": "U025",
    "context": [
      "C297"
    ],
    "intervention": "C297",
    "reference": null,
    "eval_metric": "E44",
    "pattern": "P115",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_065",
    "unit": "U025",
    "context": [
      "C297"
    ],
    "intervention": "C297",
    "reference": null,
    "eval_metric": "E45",
    "pattern": "P116",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_066",
    "unit": "U025",
    "context": [
      "C298"
    ],
    "intervention": "C298",
    "reference": null,
    "eval_metric": "E44",
    "pattern": "P117",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_067",
    "unit": "U025",
    "context": [
      "C299"
    ],
    "intervention": "C299",
    "reference": null,
    "eval_metric": "E44",
    "pattern": "P118",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_068",
    "unit": "U025",
    "context": [
      "C299"
    ],
    "intervention": "C299",
    "reference": null,
    "eval_metric": "E45",
    "pattern": "P119",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Table 3",
      "source_span": null
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_069",
    "unit": "U026",
    "context": [
      "C150",
      "C151"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P53",
    "direction": null,
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Section 6",
      "source_span": "S280"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_070",
    "unit": "U026",
    "context": [
      "C150",
      "C151"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P54",
    "direction": null,
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Section 6",
      "source_span": "S281"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_071",
    "unit": "U026",
    "context": [
      "C154",
      "I66",
      "C155"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P57",
    "direction": null,
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Section 6",
      "source_span": "S289"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_072",
    "unit": "U037",
    "context": [
      "C214",
      "C215"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": "E18",
    "pattern": "P59",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 14",
      "source_span": "S357"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_073",
    "unit": "U038",
    "context": [
      "C216",
      "C217"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": "E19",
    "pattern": "P60",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 15",
      "source_span": "S359"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_074",
    "unit": "U039",
    "context": [
      "C218"
    ],
    "intervention": "I77",
    "reference": null,
    "eval_metric": "E21",
    "pattern": "P61",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Section B.1",
      "source_span": "S361"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_075",
    "unit": "U039",
    "context": [
      "C218"
    ],
    "intervention": "I78",
    "reference": "I77",
    "eval_metric": "E22",
    "pattern": "P62",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Section B.1",
      "source_span": "S362"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_076",
    "unit": "U039",
    "context": [],
    "intervention": "I79",
    "reference": null,
    "eval_metric": "E24",
    "pattern": "P63",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Section B.1",
      "source_span": "S365"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_077",
    "unit": "U040",
    "context": [
      "C222",
      "I80"
    ],
    "intervention": "I80",
    "reference": null,
    "eval_metric": "E31",
    "pattern": "P65",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Section B.2",
      "source_span": "S372"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_078",
    "unit": "U040",
    "context": [
      "C220"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P66",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Section B.2",
      "source_span": "S374"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_079",
    "unit": "U046",
    "context": [
      "C230"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P70",
    "direction": null,
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 17",
      "source_span": "S385"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_080",
    "unit": "U046",
    "context": [
      "C231"
    ],
    "intervention": "I84",
    "reference": null,
    "eval_metric": null,
    "pattern": "P71",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 17",
      "source_span": "S386"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_081",
    "unit": "U046",
    "context": [
      "C232"
    ],
    "intervention": "I85",
    "reference": null,
    "eval_metric": null,
    "pattern": "P72",
    "direction": "down",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 17",
      "source_span": "S387"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_082",
    "unit": "U046",
    "context": [
      "C235",
      "C236",
      "C237",
      "C238",
      "I86"
    ],
    "intervention": "I86",
    "reference": "E32",
    "eval_metric": "E33",
    "pattern": "P73",
    "direction": "flat",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 17",
      "source_span": "S391"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_083",
    "unit": "U046",
    "context": [
      "C239",
      "C240",
      "C241",
      "C242",
      "I86"
    ],
    "intervention": "I86",
    "reference": "E32",
    "eval_metric": "E33",
    "pattern": "P74",
    "direction": "down",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 17",
      "source_span": "S391"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_084",
    "unit": "U047",
    "context": [
      "C243"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P75",
    "direction": null,
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 18",
      "source_span": "S392"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_085",
    "unit": "U047",
    "context": [
      "C244"
    ],
    "intervention": "I87",
    "reference": null,
    "eval_metric": null,
    "pattern": "P76",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 18",
      "source_span": "S393"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_086",
    "unit": "U047",
    "context": [
      "C245"
    ],
    "intervention": "I88",
    "reference": null,
    "eval_metric": null,
    "pattern": "P77",
    "direction": "down",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 18",
      "source_span": "S394"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_087",
    "unit": "U047",
    "context": [
      "C248",
      "C249",
      "C250",
      "C251",
      "I89"
    ],
    "intervention": "I89",
    "reference": "E34",
    "eval_metric": "E35",
    "pattern": "P78",
    "direction": "flat",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 18",
      "source_span": "S398"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_088",
    "unit": "U047",
    "context": [
      "C252",
      "C253",
      "C254",
      "C255",
      "I89"
    ],
    "intervention": "I89",
    "reference": "E34",
    "eval_metric": "E35",
    "pattern": "P79",
    "direction": "down",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 18",
      "source_span": "S398"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_089",
    "unit": "U048",
    "context": [],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P80",
    "direction": null,
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 19",
      "source_span": "S399"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_090",
    "unit": "U048",
    "context": [
      "A21"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P81",
    "direction": null,
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 19",
      "source_span": "S400"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_091",
    "unit": "U048",
    "context": [
      "C256",
      "C257",
      "C258"
    ],
    "intervention": "I90",
    "reference": "E36",
    "eval_metric": null,
    "pattern": "P82",
    "direction": "flat",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 19",
      "source_span": "S403"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_092",
    "unit": "U050",
    "context": [
      "C269",
      "C270",
      "C271",
      "C272",
      "C273",
      "C274"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": "E38",
    "pattern": "P84",
    "direction": null,
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 21",
      "source_span": "S420"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_093",
    "unit": "U055",
    "context": [
      "I92"
    ],
    "intervention": "I92",
    "reference": null,
    "eval_metric": "E39",
    "pattern": "P85",
    "direction": "up",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 22",
      "source_span": "S423"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_094",
    "unit": "U056",
    "context": [
      "C278"
    ],
    "intervention": null,
    "reference": null,
    "eval_metric": null,
    "pattern": "P86",
    "direction": "down",
    "pattern_class": "primary_result",
    "provenance": {
      "location": "Figure 22",
      "source_span": "S424"
    },
    "status": "observed"
  },
  {
    "cio_id": "CIO_095",
    "unit": "U057",
    "context": [
      "C279"
    ],
    "intervention": "I93",
    "reference": null,
    "eval_metric": null,
    "pattern": "P87",
    "direction": "up",
    "pattern_class": "comparison",
    "provenance": {
      "location": "Figure 22",
      "source_span": "S425"
    },
    "status": "observed"
  }
]
--- AM CARDS (mechanisms / assumptions) ---
[
  {
    "am_id": "AM_001",
    "kind": "mechanism",
    "node": "M7",
    "aliases": [
      "M50"
    ],
    "gloss": "Visual learning directly yields abstraction/inference, no language needed.",
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
      "M18",
      "M34",
      "M36"
    ],
    "gloss": "Canvas patchification increases input diversity, reducing overfitting and encouraging spatial prior learning.",
    "provenance": {
      "location": "Section 1"
    }
  },
  {
    "am_id": "AM_003",
    "kind": "mechanism",
    "node": "M16",
    "aliases": [
      "M19",
      "M20",
      "M22",
      "M37"
    ],
    "gloss": "Canvas enables augmentations, fostering translation/scale invariance for generalization.",
    "provenance": {
      "location": "Section 3.3"
    }
  },
  {
    "am_id": "AM_004",
    "kind": "mechanism",
    "node": "M23",
    "aliases": [],
    "gloss": "Patchification/convolution introduces locality and translation invariance inductive biases.",
    "provenance": {
      "location": "Section 3.3"
    }
  },
  {
    "am_id": "AM_005",
    "kind": "mechanism",
    "node": "M24",
    "aliases": [
      "M25"
    ],
    "gloss": "Naïve 1D patch sequencing loses 2D structure, necessitating 2D positional embeddings.",
    "provenance": {
      "location": "Section 3.3"
    }
  },
  {
    "am_id": "AM_006",
    "kind": "mechanism",
    "node": "M39",
    "aliases": [],
    "gloss": "Increasing model size improves accuracy by enabling better fitting.",
    "provenance": {
      "location": "Section 5.2"
    }
  },
  {
    "am_id": "AM_007",
    "kind": "assumption",
    "node": "A15",
    "aliases": [],
    "gloss": "Excessively large models in current settings lead to overfitting.",
    "provenance": {
      "location": "Section 5.2"
    }
  },
  {
    "am_id": "AM_008",
    "kind": "mechanism",
    "node": "M40",
    "aliases": [],
    "gloss": "Offline training enables learning visual common sense, improving TTT.",
    "provenance": {
      "location": "Section 5.2"
    }
  },
  {
    "am_id": "AM_009",
    "kind": "mechanism",
    "node": "M54",
    "aliases": [],
    "gloss": "Attention masks encourage foreground focus, improving accuracy.",
    "provenance": {
      "location": "Section A.3"
    }
  },
  {
    "am_id": "AM_010",
    "kind": "assumption",
    "node": "A20",
    "aliases": [
      "A22"
    ],
    "gloss": "Some ARC tasks have multiple plausible explanations/rules.",
    "provenance": {
      "location": "Section C.2"
    }
  },
  {
    "am_id": "AM_011",
    "kind": "mechanism",
    "node": "M69",
    "aliases": [
      "M70"
    ],
    "gloss": "Test-time training refines color and spatial arrangement, adapting to task transformations.",
    "provenance": {
      "location": "Figure 22 caption"
    }
  }
]
--- END INPUT ---

## Your task

For each CIO card, find the AM card(s) the paper EXPLICITLY ties to that observation — the paper
states this result *shows / because / suggests / indicates / demonstrates / implies* the mechanism,
or that the observation *relies on / holds under* the assumption.

Rules:
- **Explicit only.** Emit an edge only when the paper text makes the connection; do not infer a link
  from mere topical similarity. If an observation has no explicit interpretation in the paper, emit
  no edge for it — a bare observation is a valid factor on its own.
- **Many-to-one is expected.** One observation may support several AM nodes, and one AM node
  (especially the headline thesis) may be strengthened by many observations. Emit every explicit
  edge; do not collapse them.
- **direction**: `strengthen` if the result supports the mechanism/assumption, `weaken` if it
  undercuts it.
- Reference the CIO by its `cio_id` and the AM by its `am_id`.

## Output

A JSON array only (no prose), each element exactly:

```json
{
  "source_cio": "CIO_003",
  "target_am": "AM_001",
  "direction": "strengthen",
  "explicit": true,
  "evidence": "<=20-word quote or close paraphrase from the paper that states the link"
}
```
