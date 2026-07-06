```json
[
  {
    "span_id": "S1",
    "text": "ARC Is a Vision Problem!",
    "location": "Page 1, Title",
    "assigned_label": "assumption",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is the fundamental premise or underlying belief that the entire paper is built upon. It's not a description of the experimental setup (context) nor a causal explanation (mechanism), but a foundational claim about the nature of the problem.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S2",
    "text": "Common approaches to ARC treat it as a language-oriented problem, addressed by large language models (LLMs) or recurrent reasoning models.",
    "location": "Page 1, Abstract",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the existing landscape and common methods used for ARC, setting the background for the authors' novel approach.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S3",
    "text": "although the puzzle-like tasks in ARC are inherently visual, existing research has rarely approached the problem from a vision-centric perspective.",
    "location": "Page 1, Abstract",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "The 'inherently visual' part is an assumption about the nature of ARC tasks. The 'existing research has rarely approached' part is context, but the core of the statement is the visual nature as a precondition for their approach.",
    "ambiguity_reason": "The span contains both an assumption and a context element. I prioritized the assumption as it's the core justification for the paper's direction."
  },
  {
    "span_id": "S4",
    "text": "we formulate ARC within a vision paradigm, framing it as an image-to-image translation problem.",
    "location": "Page 1, Abstract",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the specific problem formulation adopted by the authors, which is part of their experimental setup.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S5",
    "text": "To incorporate visual priors, we represent the inputs on a “canvas\" that can be processed like natural images.",
    "location": "Page 1, Abstract",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This explains *how* visual priors are incorporated: by using a 'canvas' that allows inputs to be processed like natural images. It describes a causal link (canvas -> natural image processing -> visual priors).",
    "ambiguity_reason": "Could be seen as context (describing a component), but the emphasis is on *how* it enables something."
  },
  {
    "span_id": "S6",
    "text": "apply standard vision architectures, such as a vanilla Vision Transformer (ViT), to perform image-to-image mapping.",
    "location": "Page 1, Abstract",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This specifies the type of model architecture used in their framework.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S7",
    "text": "Our model is trained from scratch solely on ARC data and generalizes to unseen tasks through test-time training.",
    "location": "Page 1, Abstract",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "The 'trained from scratch solely on ARC data' is context. However, 'generalizes to unseen tasks through test-time training' describes *how* the model achieves generalization, which is a causal explanation (TTT enables generalization).",
    "ambiguity_reason": "The span contains both context and mechanism. I focused on the causal explanation for generalization."
  },
  {
    "span_id": "S8",
    "text": "VARC achieves 60.4% accuracy on the ARC-1 benchmark, substantially outperforming existing methods that are also trained from scratch.",
    "location": "Page 1, Abstract",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a specific, measurable performance metric (accuracy) and a comparative result.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S9",
    "text": "Our results are competitive with those of leading LLMs and close the gap to average human performance.",
    "location": "Page 1, Abstract",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the measured performance in comparison to other systems and human benchmarks.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S10",
    "text": "ARC consists of a collection of puzzle-like tasks (Fig. 1, top), each containing only a few examples governed by a unique underlying transformation rule.",
    "location": "Page 1, Section 1",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the structure and characteristics of the ARC benchmark tasks.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S11",
    "text": "The model is expected to make predictions on each unseen task given a few examples.",
    "location": "Page 1, Section 1",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This defines the task requirement for the model within the ARC benchmark.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S12",
    "text": "The LLMs are pre-trained on internet-scale data, from which they learn transferable common sense.",
    "location": "Page 1, Section 1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This explains *how* LLMs achieve their capabilities (learning common sense from pre-training).",
    "ambiguity_reason": "Could be context (describing LLM training), but the 'learn transferable common sense' part is a causal explanation for their effectiveness."
  },
  {
    "span_id": "S13",
    "text": "recurrent models [53, 27]... perform inference through recurrent, iterative reasoning.",
    "location": "Page 1, Section 1",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the inference process of recurrent models, which is part of their operational setup.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S14",
    "text": "many concepts in ARC are inherently visual and physical: e.g., reflection, symmetry, and gravity, as shown in Fig. 1.",
    "location": "Page 1, Section 1",
    "assigned_label": "assumption",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a core belief about the nature of ARC concepts, justifying a vision-centric approach.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S15",
    "text": "Humans can solve these tasks not merely from the demonstrations, but by reasoning through analogy to their common sense obtained from external experience. Such common sense can be acquired through observing the world, particularly, the visual world.",
    "location": "Page 1, Section 1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This explains *how* humans solve ARC tasks (common sense from visual world enables reasoning). It's a causal explanation for human capability.",
    "ambiguity_reason": "Could be an assumption about human intelligence, but it describes the *process* by which humans achieve the outcome."
  },
  {
    "span_id": "S16",
    "text": "Abstraction and inference can arise directly from visual learning, without explicit linguistic intermediates.",
    "location": "Page 2, Section 1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This explains *how* abstraction and inference can be achieved (directly from visual learning). It's a causal explanation for a capability.",
    "ambiguity_reason": "Could be an assumption that this is possible, but it describes the *way* it happens."
  },
  {
    "span_id": "S17",
    "text": "incorporating visual priors is crucial. These priors include 2D spatial locality, translation invariance, and scale invariance.",
    "location": "Page 2, Section 1",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "The statement 'visual priors are crucial' is an underlying belief about what is necessary for success. The list of priors is context.",
    "ambiguity_reason": "The 'crucial' part makes it an assumption about necessity, rather than a mechanism explaining *how* they work."
  },
  {
    "span_id": "S18",
    "text": "To facilitate learning these priors, we represent the inputs on a \"canvas\" with flexible geometric transformations, allowing the inputs to be processed as if they were natural images.",
    "location": "Page 2, Section 1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This explains *how* learning visual priors is facilitated: by using a canvas with transformations that make inputs resemble natural images. It's a causal explanation for the learning process.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S19",
    "text": "A patch on the canvas can consist of exponentially many color combinations, which helps reduce overfitting and encourages the model to learn spatial priors rather than merely memorize.",
    "location": "Page 2, Section 1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains *how* the canvas patch design leads to beneficial outcomes: it reduces overfitting and encourages learning spatial priors. It describes the causal effects of the design choice.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S20",
    "text": "At inference time, when presented with a new, unseen task, we perform test-time training [9, 24, 49, 1, 53, 27] to adapt the model to the task, enabling it to generalize from only a few examples.",
    "location": "Page 2, Section 1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This explains *how* the model generalizes: test-time training adapts the model, enabling few-shot generalization. It's a causal explanation for the generalization capability.",
    "ambiguity_reason": "Could be context (describing TTT), but the 'enabling it to generalize' part is a clear causal explanation."
  },
  {
    "span_id": "S21",
    "text": "VARC achieves 54.5% accuracy on the ARC-1 benchmark, using a small model with only 18 million parameters.",
    "location": "Page 2, Section 1",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a specific, measurable performance metric and model size.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S22",
    "text": "This result substantially surpasses the best recurrent methods [53, 27] that are also trained from scratch on ARC.",
    "location": "Page 2, Section 1",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a comparative performance result.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S23",
    "text": "Combining VARC models through ensembling [29] further improves accuracy to 60.4%, matching the reported average human performance [31] on the ARC-1 dataset.",
    "location": "Page 2, Section 1",
    "assigned_label": "observable",
    "alternative_labels_considered": ["intervention"],
    "classification_reasoning": "The act of ensembling is an intervention, but the span primarily reports the *result* of that intervention (improved accuracy, matching human performance).",
    "ambiguity_reason": "The span describes both an intervention ('Combining VARC models through ensembling') and its observable outcome. I prioritized the outcome as the primary information conveyed."
  },
  {
    "span_id": "S24",
    "text": "the design of the ARC benchmark is based on human observations and induced rules abstracted from the visual and physical world. It is natural to explore vision-driven approaches for ARC.",
    "location": "Page 2, Section 1",
    "assigned_label": "assumption",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is an underlying belief about the origin and nature of ARC tasks, which makes vision-driven approaches a natural fit.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S25",
    "text": "human reasoning is not confined to language or vision in isolation, but instead should integrate information across modalities.",
    "location": "Page 2, Section 1",
    "assigned_label": "assumption",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a general belief about the nature of human reasoning, setting a broader context for abstract reasoning research.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S26",
    "text": "recurrent models [53, 27]... aim to mimic the hierarchical and multi-timescale processing of the human brain [53] for reasoning.",
    "location": "Page 2, Section 2",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This explains *how* recurrent models achieve reasoning (by mimicking human brain processing).",
    "ambiguity_reason": "Could be context (describing recurrent models), but the 'aim to mimic... for reasoning' part is a causal explanation."
  },
  {
    "span_id": "S27",
    "text": "the ARC protocol, whose essence lies precisely in few-shot, cross-task generalization.",
    "location": "Page 2, Section 2",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This defines the core challenge and requirement of the ARC protocol, which must be met for a solution to be valid.",
    "ambiguity_reason": "Could be context (describing ARC), but 'essence lies precisely in' makes it a fundamental condition for success."
  },
  {
    "span_id": "S28",
    "text": "ARC is a collection of many different tasks. For each task, a few (e.g., 2-4) demonstration pairs (x, y) are given, and the model is required to infer the output from Xinfer.",
    "location": "Page 3, Figure 3 caption",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the general structure and requirements of the ARC benchmark.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S29",
    "text": "The training set Ttrain is a collection of 400 tasks, which can be used for model training. The test set Ttest contains 400 new tasks: the demo pairs of a new task are given only at inference time, based on which the model performs inference on Xinfer.",
    "location": "Page 3, Figure 3 caption",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This specifies the datasets (training and test sets) and their characteristics.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S30",
    "text": "The presence of new (x, y) pairs in Ddemo at inference time allows to perform test-time training [49, 1, 9, 24], which we adopt and will discuss.",
    "location": "Page 3, Section 3.1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This explains *how* test-time training is enabled (by the availability of new demo pairs at inference time).",
    "ambiguity_reason": "Could be context (describing TTT setup), but 'allows to perform' indicates a causal enabler."
  },
  {
    "span_id": "S31",
    "text": "We frame the problem as per-pixel classification, analogous to the semantic segmentation problem [38].",
    "location": "Page 3, Section 3.2",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the specific type of machine learning problem they are solving.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S32",
    "text": "We learn a neural network fθ parameterized by θ. The network fθ takes an image xi as input, conditioned on a task token associated with the task T. The task token is represented as a learnable embedding dependent on T. The output of fθ is a grid where each position represents a categorical distribution.",
    "location": "Page 3, Section 3.2",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the model architecture, inputs, and outputs.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S33",
    "text": "The overall objective function is simply the per-pixel cross-entropy loss [38]: L(θ) = ET,i [D(yi, fθ(xi | T))].",
    "location": "Page 3, Section 3.2",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This specifies the loss function used for training.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S34",
    "text": "We define the concept of a \"canvas\". A canvas has a predefined and sufficiently large size, e.g., 64×64. The raw input is transformed and placed onto this canvas.",
    "location": "Page 3, Section 3.3",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This introduces and describes a key component of their system (the canvas) and its properties.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S35",
    "text": "This formulation naturally accommodates translation and scale augmentations, which are common strategies for introducing translation and scale invariance in vision",
    "location": "Page 3, Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This explains *how* the canvas formulation is beneficial: it accommodates augmentations that introduce invariance. It describes a causal effect of the design.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S36",
    "text": "We set the background of the canvas to an additional background color, i.e., the (C+1)-th color.",
    "location": "Page 3, Section 3.3",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a specific detail of the canvas setup.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S37",
    "text": "if we naïvely treat each raw pixel as a token, there would be only C distinct tokens. In contrast, our canvas formulation supports a much larger set of local, patch-level configurations... This formulation is important for improving generalization performance.",
    "location": "Page 3, Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This explains *why* the canvas formulation is beneficial: it increases the diversity of patch configurations, which in turn improves generalization performance. The 'if we naïvely treat...' part sets up the problem that the canvas solves.",
    "ambiguity_reason": "The 'if' clause could be an assumption, but the overall span explains the causal benefit of the canvas."
  },
  {
    "span_id": "S38",
    "text": "The “canvas\" concept enables us to flexibly apply translation and scale augmentations, which are critical in standard vision models.",
    "location": "Page 3, Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This explains *how* the canvas is useful: it enables flexible augmentations, which are critical for vision models. It describes a causal capability.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S39",
    "text": "These data augmentations encourage the model to learn underlying mappings invariant to geometric transformations grounded in the visual world.",
    "location": "Page 4, Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains *how* data augmentations are beneficial: they encourage learning invariant mappings. It's a causal explanation for the learning process.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S40",
    "text": "Scale augmentation: Given a raw input, we randomly resize it by an integer scaling ratio s, duplicating each raw pixel into s×s (see Fig. 4, left).",
    "location": "Page 4, Section 3.3",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes a specific manipulation performed on the input data.",
    "ambiguity_reason": "Could be context (describing the augmentation), but it's a deliberate manipulation for experimental purposes."
  },
  {
    "span_id": "S41",
    "text": "“colors” in ARC do not correspond to real-world colors, so it is not meaningful to perform other interpolations (such as bilinear).",
    "location": "Page 4, Section 3.3",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This is a condition about the nature of ARC colors that dictates what interpolation methods are meaningful.",
    "ambiguity_reason": "Could be context (describing ARC colors), but the 'not meaningful' part implies a constraint or precondition for valid operations."
  },
  {
    "span_id": "S42",
    "text": "Translation augmentation: given the scaled grid, we randomly place it on the fixed-size canvas. We ensure all pixels are visibile. See Fig. 4 (right).",
    "location": "Page 4, Section 3.3",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes a specific manipulation performed on the input data.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S43",
    "text": "We empirically show that these visual priors are important for generalization to unseen tasks.",
    "location": "Page 4, Section 3.3",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "The statement 'visual priors are important for generalization' is an underlying belief about their necessity for the desired outcome. The 'empirically show' refers to the observable evidence.",
    "ambiguity_reason": "The word 'important' suggests a necessary condition (assumption) rather than a direct causal explanation of *how* they work (mechanism)."
  },
  {
    "span_id": "S44",
    "text": "By default, we use a ViT [17].",
    "location": "Page 4, Section 3.3",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This specifies the default model architecture used.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S45",
    "text": "the input canvas is divided into non-overlapping patches (e.g., 2×2), projected by a linear embedding, added with positional embedding [52], and processed by a stack of Transformer blocks [52].",
    "location": "Page 4, Section 3.3",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the internal processing steps of the ViT model.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S46",
    "text": "before patchification, we first map each pixel's discrete index into a learnable continuous-valued embedding.",
    "location": "Page 4, Section 3.3",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes a specific processing step applied to the pixels before they are patchified.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S47",
    "text": "patchification can be viewed as a special form of convolution. Like convolution, it incorporates several critical inductive biases in vision: most notably, locality (i.e., grouping nearby pixels) and translation invariance (i.e., weight sharing across locations).",
    "location": "Page 4, Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This explains *how* patchification is beneficial: it incorporates inductive biases like locality and translation invariance. It describes the causal effect of patchification.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S48",
    "text": "Unlike language data, which is generally modeled as 1D sequences, images are inherently 2D. This 2D structure can be lost if we naïvely treat the embedded patches as a 1D sequence.",
    "location": "Page 4, Section 3.3",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "The statement 'images are inherently 2D' is an assumption about image data. The '2D structure can be lost' explains *why* naive 1D treatment is problematic, which is a causal explanation for a potential failure mode.",
    "ambiguity_reason": "The span contains both an assumption about image data and a mechanism explaining a potential issue. I prioritized the assumption as the foundational statement."
  },
  {
    "span_id": "S49",
    "text": "We empirically show that explicitly modeling positions in 2D is essential.",
    "location": "Page 4, Section 3.3",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "Similar to S43, 'essential' implies a necessary condition for good performance.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S50",
    "text": "Formally, we adopt separable 2D positional embeddings, following [11]: with D channels for positional embeddings, we use the first half of the channels to embed the horizontal coordinate and the second half to embed the vertical coordinate.",
    "location": "Page 4, Section 3.3",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes a specific design choice and its implementation details for positional embeddings.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S51",
    "text": "Beyond ViT, we also study the more classical vision-based architecture, i.e., convolutional neural networks [30]. Specifically, we adopt the U-Net model [46], a hierarchical convolutional network.",
    "location": "Page 4, Section 3.3",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes the comparison of ViT with another architecture (U-Net), which is a controlled comparison.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S52",
    "text": "The original U-Net was proposed precisely for the image-to-image translation problem of segmentation [46], making it a natural candidate for the problem we consider.",
    "location": "Page 4, Section 3.3",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This is an underlying belief about why U-Net is suitable for the problem (its original purpose aligns with the current task).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S53",
    "text": "We adopt a two-stage training paradigm to learn the parameters of the neural network. Offline training... Test-time training...",
    "location": "Page 4, Section 3.4",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the overall training methodology.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S54",
    "text": "We train one model fθ jointly for all k training tasks (e.g., k=400), based on the loss in Eq. (1). All tasks share the same parameters, only except that each task has its own task-conditional token.",
    "location": "Page 4, Section 3.4",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the specifics of the offline training setup.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S55",
    "text": "At inference time, we are given Ddemo={(xi, Yi)}m i=1 with both input and output accessible; the model is required to make prediction for a given Xinfer in this new task T.",
    "location": "Page 5, Section 3.5",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the setup for test-time training and inference.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S56",
    "text": "We perform test-time training for each new task T independently.",
    "location": "Page 5, Section 3.5",
    "assigned_label": "context",
    "alternative_labels_considered": ["intervention"],
    "classification_reasoning": "This describes a characteristic of how TTT is applied, which is part of the experimental setup.",
    "ambiguity_reason": "Could be an intervention if compared to 'jointly', but here it's stated as a fact of their method."
  },
  {
    "span_id": "S57",
    "text": "As there are very few demo pairs in Ddemo (e.g., 2 to 4), we also perform data augmentation.",
    "location": "Page 5, Section 3.5",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes a specific manipulation (data augmentation) performed due to a condition (few demo pairs).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S58",
    "text": "this test-time training process remains reasonably fast (e.g., 70 seconds per task on a single GPU).",
    "location": "Page 5, Section 3.5",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a measurable performance metric (speed).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S59",
    "text": "Since one output location in the raw grid may be predicted by multiple pixels on the canvas (e.g., due to rescaling; see Fig. 5), we aggregate all predictions (from softmax outputs) at this location by average pooling.",
    "location": "Page 5, Section 3.5",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This explains *how* predictions are consolidated from the canvas to the raw grid (average pooling). It's a causal explanation for the aggregation process.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S60",
    "text": "we adopt multi-view inference to improve accuracy, where the views are sampled with different augmentations.",
    "location": "Page 5, Section 3.5",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This describes a specific manipulation (multi-view inference) performed to achieve a goal (improve accuracy). The 'improve accuracy' part is the intended effect, making the adoption of multi-view inference the intervention.",
    "ambiguity_reason": "The span states both the intervention and its intended effect. I classified it as intervention because it's the action taken."
  },
  {
    "span_id": "S61",
    "text": "As the multi-view inference cost is negligible compared with test-time training cost, it is virtually nearly free to use many views.",
    "location": "Page 5, Section 3.5",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This is a condition (negligible cost) that makes using many views feasible. It's a precondition for a certain operational choice.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S62",
    "text": "Predictions from different views are consolidated by majority voting [1].",
    "location": "Page 5, Section 3.5",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This describes a specific method used to combine predictions, which is a manipulation of the output.",
    "ambiguity_reason": "Could be mechanism (how consolidation works), but it's a specific technique applied."
  },
  {
    "span_id": "S63",
    "text": "The ARC benchmark by default adopts the pass@2 accuracy metric: i.e., two different solutions can be produced for evaluation, and a task is considered correct if one is correct.",
    "location": "Page 5, Section 3.5",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This defines the standard evaluation metric for the benchmark.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S64",
    "text": "To support this metric, we adopt majority voting in multi-view inference and retain the top-2 most populated output solutions.",
    "location": "Page 5, Section 3.5",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This describes a specific strategy (majority voting, retaining top-2) adopted to align with the evaluation metric.",
    "ambiguity_reason": "Similar to S62, it's a specific technique applied."
  },
  {
    "span_id": "S65",
    "text": "In our best-performing model, the canvas size is 64×64. In the case of ViT, the patch size is 2×2, resulting in a sequence length of 32^2.",
    "location": "Page 5, Section 4",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "These are specific configuration details of the model and canvas.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S66",
    "text": "For scale augmentation, an integer scaling ratio is randomly sampled, such that the scaled grid is no larger than the canvas size. For translation augmentation, the upper-left corner is randomly sampled under the constraint that the placed image is fully visible.",
    "location": "Page 5, Section 4",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "These are specific implementation details of the augmentation strategies.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S67",
    "text": "We use the standard ARC-1 training set Ttrain for training: it has 400 tasks with 2-4 demo pairs each. Following common practice on ARC, we also expand our training set with the RE-ARC set [22], from which we sample 1,000 additional demo pairs per task.",
    "location": "Page 5, Section 4",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "The expansion of the training set with RE-ARC data is a specific manipulation of the training data.",
    "ambiguity_reason": "The first part is context, but the 'expand our training set' is a clear intervention."
  },
  {
    "span_id": "S68",
    "text": "We apply translation and scale augmentation in offline training.",
    "location": "Page 5, Section 4",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes a specific manipulation (applying augmentations) during offline training.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S69",
    "text": "To make test-time training more feasible, we also augment the single task T into multiple auxiliary tasks. We do this by using standard augmentation from existing ARC methods: flip, rotation (by 90°, 180°, or 270°), and color permutation.",
    "location": "Page 5, Section 4",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes a specific manipulation (augmenting tasks into auxiliary tasks) and the methods used for it.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S70",
    "text": "We treat each of these test-time training augmentations as an auxiliary task, each assigned a task embedding.",
    "location": "Page 5, Section 4",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes how the augmented tasks are handled within the model's framework.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S71",
    "text": "We also apply translation and scale augmentation in test-time training, but we do not view them as a new auxiliary task (under the assumption that all auxiliary tasks are translation and scale invariant).",
    "location": "Page 5, Section 4",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes applying specific augmentations during TTT. The parenthetical 'under the assumption' is an assumption.",
    "ambiguity_reason": "The span contains both an intervention and an assumption. I prioritized the intervention as the main action described."
  },
  {
    "span_id": "S72",
    "text": "Our experiments are primarily conducted on the benchmark of ARC-1 [12]. We report the pass@2 accuracy (referred to simply as \"accuracy” hereafter) in percentage (%).",
    "location": "Page 5, Section 5",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This specifies the benchmark and the primary metric used for evaluation.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S73",
    "text": "To support pass@2 evaluation, we adopt multi-view inference.",
    "location": "Page 5, Section 5",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes a specific strategy adopted to meet an evaluation requirement.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S74",
    "text": "We evaluate our model on the ARC-1 evaluation set (i.e., Teval). This set is conceptually a test set (see Fig. 3), but with ground truth available only for computing accuracy.",
    "location": "Page 5, Section 5",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the specific dataset used for evaluation and its characteristics.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S75",
    "text": "ViT 384 5 6M 10 44.4\nViT 512 10 18M 28 54.5\nViT 768 20 66M 99 53.0\nU-Net setting (a) 7M 18 42.8\nU-Net setting (b) 17M 33 47.5\nU-Net setting (c) 55M 87 48.3",
    "location": "Page 6, Table 1",
    "assigned_label": "observable",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "These are specific, measurable performance metrics (accuracy, Gflops) for different model configurations. The model configurations themselves are context, but the numbers are observables.",
    "ambiguity_reason": "The table contains both context (model specs) and observables (performance). I extracted the performance numbers as observables."
  },
  {
    "span_id": "S76",
    "text": "Fig. 7 summarizes the effects of visual priors, starting from a baseline (a) without the other components in this figure. These priors jointly have a gain of 27.7 points, where the canvas-based designs (c-f) has a gain of 11.5 points.",
    "location": "Page 6, Section 5.1",
    "assigned_label": "observable",
    "alternative_labels_considered": ["intervention"],
    "classification_reasoning": "This reports the measured performance gains from applying visual priors, which is an empirical result.",
    "ambiguity_reason": "The 'effects of visual priors' implies an intervention (adding/removing priors), but the span focuses on the measured gain."
  },
  {
    "span_id": "S77",
    "text": "Extending from 1D positional embedding to its 2D counterpart is beneficial: see Fig. 7(b)(c). This is observed in both (b) absolute and (c) relative positional embeddings.",
    "location": "Page 6, Section 5.1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["observable"],
    "classification_reasoning": "The statement 'is beneficial' implies a causal effect. The 'observed' part refers to the observable evidence.",
    "ambiguity_reason": "The span states both a causal effect ('beneficial') and the observation of it. I prioritized the causal effect as the mechanism."
  },
  {
    "span_id": "S78",
    "text": "To demonstrate this effect on a stronger baseline, we replace the 2D ROPE in Fig. 7(f) with a 1D ROPE and observe a degradation of 3.5 points, from 54.5 to 51.0.",
    "location": "Page 6, Section 5.1",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a specific manipulation (replacing 2D ROPE with 1D ROPE) and its measured outcome (degradation).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S79",
    "text": "A key design principle of our method is to prepare the input as a natural image. This enables the expansion of the token set from a very limited size (e.g., 10) to an exponentially large number.",
    "location": "Page 6, Section 5.1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "The 'design principle' is an assumption. However, 'enables the expansion of the token set' explains *how* this principle leads to a beneficial outcome. I focused on the causal explanation.",
    "ambiguity_reason": "The span contains both an assumption (design principle) and a mechanism (how it enables something). I prioritized the mechanism."
  },
  {
    "span_id": "S80",
    "text": "In Fig. 7(d), we advance from 1×1 patches on a 32×32 canvas to 2×2 patches on a 64×64 canvas. Doing so does not increase the computational cost of the Transformer.",
    "location": "Page 6, Section 5.1",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a specific manipulation (changing patch and canvas size) and an observable (no increase in computational cost).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S81",
    "text": "if we constrain each 2×2 patch to cover only one raw pixel, it becomes equivalent to the 1×1 patch counterpart on the 32×32 canvas. Therefore, to ensure a meaningful comparison, we do not impose this constraint, allowing each 2×2 patch to cover multiple colors.",
    "location": "Page 6, Section 5.1",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "The 'do not impose this constraint' is a specific manipulation to ensure a meaningful comparison. The 'if we constrain' part is an assumption about equivalence.",
    "ambiguity_reason": "The span contains both an assumption and an intervention. I prioritized the intervention as the action taken for the experiment."
  },
  {
    "span_id": "S82",
    "text": "This can be interpreted as one-pixel translation augmentation on the canvas.",
    "location": "Page 6, Section 5.1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This provides a causal interpretation of the 2x2 patchification, explaining *how* it functions as an augmentation.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S83",
    "text": "Even so, the 2×2 patchification leads to a noticeable gain of 2.4 points, improving from 43.0 to 45.4; see Fig. 7(c,d).",
    "location": "Page 6, Section 5.1",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a specific, measurable performance gain.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S84",
    "text": "each patch can cover multiple colors (as in natural images), which substantially enriches the data space for learning.",
    "location": "Page 6, Section 5.1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains *how* the multi-color patches are beneficial: they enrich the data space for learning. It's a causal explanation for improved learning.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S85",
    "text": "In image recognition, even highly capable network architectures still benefit greatly from translation and scale augmentations.",
    "location": "Page 6, Section 5.1",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This is a general belief or principle about the effectiveness of augmentations in vision, serving as a justification for their use.",
    "ambiguity_reason": "Could be mechanism (how augmentations work), but it's stated as a general truth or precondition for benefit."
  },
  {
    "span_id": "S86",
    "text": "In Fig. 7(e), we apply fully flexible translation augmentation on the canvas. Compared with the \"one-pixel\" augmentation in Fig. 7(d), this setting yields an additional gain of 2.9 points (from 45.4 to 48.3).",
    "location": "Page 6, Section 5.1",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a specific manipulation (applying flexible translation augmentation) and its measured outcome (gain).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S87",
    "text": "In Fig. 7(f), we further apply the scale augmentation enabled by the concept of canvas. Scale augmentation yields a substantial gain of 6.2 points.",
    "location": "Page 6, Section 5.1",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a specific manipulation (applying scale augmentation) and its measured outcome (gain).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S88",
    "text": "Unlike translation invariance, which can be partially addressed by patchification (i.e., a special form of convolution), the ViT architecture has little to no inductive bias about scale invariance. This can explain why scale augmentation yields a substantial gain.",
    "location": "Page 6, Section 5.1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This explains *why* scale augmentation is effective: because ViT lacks inherent scale invariance bias, the augmentation provides this. It's a causal explanation for the observed gain.",
    "ambiguity_reason": "The statement about ViT's lack of bias could be an assumption, but the overall span connects it causally to the gain."
  },
  {
    "span_id": "S89",
    "text": "In Tab. 1, we compare ViT with U-Nets, a type of convolutional network. We evaluate three model sizes for each architecture.",
    "location": "Page 6, Section 5.2",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes a controlled comparison between two different model architectures.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S90",
    "text": "Although ViTs consistently perform better, all U-Net variants achieve decent accuracy, suggesting that this problem can also be effectively addressed by classical vision backbones.",
    "location": "Page 6, Section 5.2",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This reports the comparative performance of ViTs and U-Nets. The 'suggesting that...' part is an interpretation of the observable, but the core is the measured performance.",
    "ambiguity_reason": "The span contains both an observable and an interpretation (mechanism). I prioritized the observable as the direct result."
  },
  {
    "span_id": "S91",
    "text": "In Fig. 8, we show ViTs with varying depths and widths. In this regime, our method demonstrates good scalability: increasing depth and/or width leads to higher accuracy as a result of better fitting.",
    "location": "Page 6, Section 5.2",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This reports the measured scalability and the observed trend of increasing accuracy. The 'as a result of better fitting' is a mechanism, but the primary information is the observed scalability.",
    "ambiguity_reason": "The span contains both an observable and a mechanism. I prioritized the observable as the direct result."
  },
  {
    "span_id": "S92",
    "text": "Going beyond this regime can lead to overfitting in our current setting, as shown in Tab. 1 for the 66M ViT model. We observe that this larger model achieves higher training accuracy, suggesting that future research should focus on generalization.",
    "location": "Page 6, Section 5.2",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This reports the observed phenomenon of overfitting and higher training accuracy for larger models. The 'suggesting that...' part is an implication, but the core is the measured behavior.",
    "ambiguity_reason": "The span contains both an observable and an implication (mechanism). I prioritized the observable as the direct result."
  },
  {
    "span_id": "S93",
    "text": "In Fig. 9(b), we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.",
    "location": "Page 7, Section 5.2",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes a controlled comparison of different TTT strategies.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S94",
    "text": "As expected, offline training greatly improves the performance of TTT, suggesting that common sense about the visual world can be learned from the training set.",
    "location": "Page 7, Section 5.2",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This reports the measured improvement in performance. The 'suggesting that...' part is an interpretation (mechanism), but the core is the observed improvement.",
    "ambiguity_reason": "The span contains both an observable and an interpretation (mechanism). I prioritized the observable as the direct result."
  },
  {
    "span_id": "S95",
    "text": "even without offline training, our TTT strategy can achieve nontrivial accuracy (26.4), suggesting that some tasks in this benchmark can be solved tabula rasa.",
    "location": "Page 7, Section 5.2",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This reports the measured accuracy. The 'suggesting that...' part is an interpretation (mechanism), but the core is the observed accuracy.",
    "ambiguity_reason": "The span contains both an observable and an interpretation (mechanism). I prioritized the observable as the direct result."
  },
  {
    "span_id": "S96",
    "text": "Surprisingly, performing TTT independently for each test task yields substantially better performance (by ~10 points) than doing so jointly across all test tasks, even though the latter relies on a stronger assumption about the availability of multiple test tasks at once.",
    "location": "Page 7, Section 5.2",
    "assigned_label": "observable",
    "alternative_labels_considered": ["intervention"],
    "classification_reasoning": "This reports the measured performance difference between independent and joint TTT. The 'relies on a stronger assumption' is an assumption about the joint TTT.",
    "ambiguity_reason": "The span contains both an observable and an assumption. I prioritized the observable as the direct result of the comparison."
  },
  {
    "span_id": "S97",
    "text": "We hypothesize that overtraining on the test tasks may cause the model to forget the knowledge acquired during offline training.",
    "location": "Page 7, Section 5.2",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This proposes a causal explanation for why joint TTT performs worse (overtraining causes forgetting).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S98",
    "text": "Single-view inference has a decent pass@1 accuracy of 35.9; multi-view inference further boosts to 49.8, thanks to majority voting.",
    "location": "Page 7, Section 5.2",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This reports the measured accuracy for single-view and the boost from multi-view. The 'thanks to majority voting' is a mechanism, but the core is the measured performance.",
    "ambiguity_reason": "The span contains both an observable and a mechanism. I prioritized the observable as the direct result."
  },
  {
    "span_id": "S99",
    "text": "Unlike typical computer vision applications such as semantic segmentation, in ARC, a mistake on even a single pixel renders the entire prediction incorrect. This may explain the large gain seen here.",
    "location": "Page 7, Section 5.2",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This explains *why* multi-view inference yields a large gain: because ARC's strict correctness criteria mean single pixel errors are critical, and multi-view helps mitigate this. It's a causal explanation for the observed gain.",
    "ambiguity_reason": "The first sentence could be an assumption about ARC's strictness, but the second sentence explicitly links it as an explanation for the gain, making it a mechanism."
  },
  {
    "span_id": "S100",
    "text": "Our model compares favorably with some of the most powerful LLMs at the time their results were reported: including Deepseek, Claude, o3, and GPT-5",
    "location": "Page 7, Section 5.3",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a comparative performance result.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S101",
    "text": "LLMs are pre-trained on internet-scale data, and some may also incorporate multimodal data that include images.",
    "location": "Page 7, Section 5.3",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the training data characteristics of LLMs.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S102",
    "text": "Our method does not rely on such data and uses a model that is several orders of magnitude smaller.",
    "location": "Page 7, Section 5.3",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the characteristics of their method (data independence, model size) in comparison to LLMs.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S103",
    "text": "In the controlled setting of training from scratch on ARC data, our method substantially outperforms the recurrent models: HRM [53] and TRM [27]. Our VARC with 18M parameters is ~10 points better than TRM on ARC-1, a >20% relative improvement.",
    "location": "Page 7, Section 5.3",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This reports specific, measurable performance improvements over recurrent models.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S104",
    "text": "once test-time training is completed, our model performs fully feedforward inference, with no recurrence involved in reasoning.",
    "location": "Page 7, Section 5.3",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the nature of the model's inference process after TTT.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S105",
    "text": "Following the classical ensembling practice in vision (e.g., AlexNet [29]), we ensemble one ViT and one U-Net, each with test-time training run four times. Doing so boosts our result to 60.4.",
    "location": "Page 7, Section 5.3",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["observable"],
    "classification_reasoning": "This describes a specific manipulation (ensembling) and its measured outcome (boosts result). I prioritized the intervention as the action taken.",
    "ambiguity_reason": "The span contains both an intervention and its observable outcome. I prioritized the intervention."
  },
  {
    "span_id": "S106",
    "text": "This result closes the gap with the reported average human performance (60.2 [31]).",
    "location": "Page 7, Section 5.3",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a comparative performance result against human benchmarks.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S107",
    "text": "Fig. 10 shows the attention patterns of our ViT model in a test task. These attention maps show that our model can correctly reason about the relationship between a source pixel and its target pixel to copy from.",
    "location": "Page 7, Section 6",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "The attention patterns are a measurable behavior of the model. The 'show that our model can correctly reason' is an interpretation of this observable, making it a mechanism, but the primary information is the visualization itself.",
    "ambiguity_reason": "The span contains both an observable (attention patterns) and an interpretation (mechanism). I prioritized the observable as the direct output."
  },
  {
    "span_id": "S108",
    "text": "A layer-wise map is the softmax attention map averaged across all pixels in the layer: it reveals which pixels receive the most attention in that layer.",
    "location": "Page 7, Section 6",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This explains *how* the layer-wise map provides insight (by revealing attention focus). It's a causal explanation for the interpretability.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S109",
    "text": "In this task, different layers exhibit different specialties: some layers attend to the pixels that are to be copied, and some layers attend to the target lines alone the eight directions.",
    "location": "Page 7, Section 6",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a specific, observed behavior of the model's layers.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S110",
    "text": "Our model is conditioned on a task token, with an embedding learned to represent each task. With 400 training tasks in ARC-1, our model learns 400 distinct task embeddings in offline training.",
    "location": "Page 8, Section 6",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the task token mechanism and the number of embeddings learned, which are part of the model's setup.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S111",
    "text": "We visualize these 400 embeddings in the 2D space by t-SNE [39] (see Fig. 12).",
    "location": "Page 8, Section 6",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a visualization of the model's internal state.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S112",
    "text": "Interestingly, we observe that nearby points in the task embedding space exhibit similar semantics. For example, the top-left corner in Fig. 12 shows two tasks related to coloring; the bottom-left corner shows two tasks related to generalized logic operations (i.e., AND/OR/XOR).",
    "location": "Page 8, Section 6",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes observed patterns in the task embeddings.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S113",
    "text": "This visualization suggests that our method attempts to learn the relations between different tasks, which is an essential ability for abstraction and reasoning.",
    "location": "Page 8, Section 6",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["observable"],
    "classification_reasoning": "This explains *how* the visualization provides insight: it suggests the model learns task relations, which is a causal explanation for a desired capability.",
    "ambiguity_reason": "The span contains both an observable (visualization) and an interpretation (mechanism). I prioritized the mechanism as the explanation for the observed pattern."
  },
  {
    "span_id": "S114",
    "text": "It naturally enables the adaptation of visual frameworks and yields strong few-shot generalization competitive with recent approaches, while remaining orders of magnitude smaller than most LLM-based models.",
    "location": "Page 8, Section 7",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["observable"],
    "classification_reasoning": "This explains *how* their problem framing leads to benefits: it enables adaptation and yields strong generalization. It's a causal explanation for the method's effectiveness.",
    "ambiguity_reason": "The 'yields strong few-shot generalization' part is an observable, but the 'enables the adaptation' is a mechanism. I prioritized the mechanism as the causal explanation."
  },
  {
    "span_id": "S115",
    "text": "This opens up a new possibility of treating ARC as a vision-centric problem, emphasizing abstraction and reasoning emerging directly from image pixels.",
    "location": "Page 8, Section 7",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This describes a new way of achieving abstraction and reasoning (directly from image pixels) enabled by their approach. It's a causal explanation for a new capability.",
    "ambiguity_reason": "Could be an assumption about the potential of vision-centric ARC, but it describes *how* abstraction emerges."
  },
  {
    "span_id": "S116",
    "text": "During test-time training, we augment the single test task T into multiple auxiliary tasks. We use a distinct task embedding for each auxiliary task, as not all of these augmentations correspond to the same underlying rule (e.g., consider \"gravity\" under a 90° rotation).",
    "location": "Page 11, Section A.2",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes a specific manipulation (augmenting tasks) and the reason for a detail (distinct embeddings due to rule variability). The reason for distinct embeddings is an assumption.",
    "ambiguity_reason": "The span contains both an intervention and an assumption. I prioritized the intervention as the main action described."
  },
  {
    "span_id": "S117",
    "text": "We train for 100 epochs on these 51 tasks, covering 100 x 51 x 3 = 15.3k samples in total for test-time training for one test task T (assuming 3 raw samples in this task).",
    "location": "Page 11, Section A.2",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This provides specific training details for TTT.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S118",
    "text": "Unlike standard semantic segmentation, in ARC, the raw input and output sizes are not always identical (e.g., see Fig. 3, Test Set, Task 1). This issue can be addressed on the canvas in a unified framework.",
    "location": "Page 11, Section A.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "The first sentence is context (describing ARC's variability). The second sentence explains *how* this issue is resolved (canvas addresses it).",
    "ambiguity_reason": "The span contains both context and mechanism. I prioritized the mechanism as the solution to the described problem."
  },
  {
    "span_id": "S119",
    "text": "In our method, the input/output canvas always has a fixed size and is filled with a background token [BG]. In addition, when the raw output is placed on the canvas (serving as the ground truth during training), we always use an extra border token, [BD], to indicate the right and bottom edges.",
    "location": "Page 11, Section A.3",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes specific design choices and components of the canvas and token usage.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S120",
    "text": "During inference, we locate the rightmost and bottommost [BD] tokens and crop the output accordingly to recover the final predicted shape.",
    "location": "Page 11, Section A.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This explains *how* the final predicted shape is recovered (by using BD tokens to crop). It's a causal explanation for shape recovery.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S121",
    "text": "Since the number of background pixels [BG] can dominate in some examples, we apply attention masks in the self-attention blocks to encourage the model to focus on the foreground pixels.",
    "location": "Page 11, Section A.3",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This describes a specific manipulation (applying attention masks) to achieve a goal (encourage focus on foreground). The 'encourage focus' is the mechanism, but the action is the intervention.",
    "ambiguity_reason": "The span contains both an intervention and its intended mechanism. I prioritized the intervention as the action taken."
  },
  {
    "span_id": "S122",
    "text": "The resulting softmax attention scores are therefore zero at those key positions.",
    "location": "Page 11, Section A.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains *how* the attention masks work (by zeroing out scores). It's a causal explanation for the effect of the masks.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S123",
    "text": "Moreover, during training, the loss is computed only on locations where the inputs are not background pixels [BG].",
    "location": "Page 11, Section A.3",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes a specific manipulation (computing loss only on foreground pixels) during training.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S124",
    "text": "These designs encourage the model to pay more attention to foregrounds and therefore improve accuracy, although we note that even without them, our method still performs competitively, as observed in our preliminary experiments.",
    "location": "Page 11, Section A.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["observable"],
    "classification_reasoning": "This explains *how* the designs are beneficial: they encourage foreground attention and improve accuracy. It's a causal explanation for the performance improvement.",
    "ambiguity_reason": "The 'improve accuracy' part is an observable, but the 'encourage... and therefore improve' is a causal explanation."
  },
  {
    "span_id": "S125",
    "text": "Using only the original ARC training data, without any RE-ARC data, our method achieves a decent accuracy of 31.5. By adding 10, 100, and 1,000 pairs per task from RE-ARC, the accuracy increases to 38.6, 52.3, and 54.0, respectively.",
    "location": "Page 12, Section B.1",
    "assigned_label": "observable",
    "alternative_labels_considered": ["intervention"],
    "classification_reasoning": "This reports specific, measurable accuracy values under different conditions (adding RE-ARC data). The act of adding data is an intervention, but the focus is on the measured outcome.",
    "ambiguity_reason": "The span describes both an intervention (adding data) and its observable outcome. I prioritized the outcome."
  },
  {
    "span_id": "S126",
    "text": "This comparison suggests that increasing the amount of offline training data is beneficial, although the returns diminish beyond a certain point.",
    "location": "Page 12, Section B.1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["observable"],
    "classification_reasoning": "This explains *why* increasing data is good (beneficial) and describes a trend (diminishing returns). It's a causal explanation for the observed performance trend.",
    "ambiguity_reason": "The 'beneficial' part is a causal effect, while the 'diminishing returns' describes a pattern in the observable."
  },
  {
    "span_id": "S127",
    "text": "When trained on 0, 16, 80, and 400 tasks, the accuracy increases from 26.4 to 43.1, 49.6, and 54.5, respectively, suggesting that the diversity of training tasks is helpful for generalization.",
    "location": "Page 12, Section B.1",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This reports specific, measurable accuracy values under different conditions (number of tasks). The 'suggesting that... helpful for generalization' is a mechanism, but the core is the measured accuracy.",
    "ambiguity_reason": "The span contains both an observable and an interpretation (mechanism). I prioritized the observable as the direct result."
  },
  {
    "span_id": "S128",
    "text": "We further examine the pass@k accuracy, thanks to our multi-view inference with many views (510). This metric reflects whether at least one of the k predicted solutions is correct. It can be viewed as a recall-like measure.",
    "location": "Page 12, Section B.2",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the pass@k metric and how it's used, which is part of the evaluation setup.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S129",
    "text": "As expected, as the number of proposals (k) increases, the pass@k accuracy increases. On ARC-1, the pass@k accuracy is 49.8, 54.5, and 66.3, when k is 1, 2, and 300, respectively (Fig. 16, top-left).",
    "location": "Page 12, Section B.2",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This reports specific, measurable pass@k accuracy values for different k.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S130",
    "text": "This result indicates that our model produces correct predictions in some of the many views, although such correct cases are not sufficiently populated to be retained after voting.",
    "location": "Page 12, Section B.2",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["observable"],
    "classification_reasoning": "This explains *why* the pass@k results are as they are: the model produces correct predictions, but voting doesn't always retain them. It's a causal explanation for the observed behavior.",
    "ambiguity_reason": "The span contains both an observable (result indicates) and an explanation (mechanism). I prioritized the mechanism."
  },
  {
    "span_id": "S131",
    "text": "Although most ARC tasks are unambiguous, some may admit multiple plausible explanations or rules.",
    "location": "Page 12, Section C.2",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This is a condition about the nature of ARC tasks (some are ambiguous) that affects how solutions are interpreted.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S132",
    "text": "We show an example in Fig. 19, in which our method uncovers different solutions that are plausible.",
    "location": "Page 12, Section C.2",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes an observed behavior of the model (uncovering plausible solutions).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S133",
    "text": "This visualization suggests that our method attempts to learn the relations between different tasks, which is an essential ability for abstraction and reasoning.",
    "location": "Page 8, Section 6",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["observable"],
    "classification_reasoning": "This explains *how* the visualization provides insight: it suggests the model learns task relations, which is a causal explanation for a desired capability.",
    "ambiguity_reason": "The span contains both an observable (visualization) and an interpretation (mechanism). I prioritized the mechanism as the explanation for the observed pattern."
  }
]
```

## Classification criteria you actually used

Here's how I applied the definitions and resolved ambiguities during the classification process:

*   **Assumption vs. Context**:
    *   **Assumption**: I classified statements as "assumption" when they described a fundamental belief, a necessary precondition, or an inherent property that *must be true* for a claim or method to be valid or effective. These are often implicit and justify *why* a certain approach is taken or *why* a problem is hard/easy. Keywords like "crucial," "essential," "inherently," or statements about what "makes sense" or "is natural" often signaled an assumption. For example, "ARC Is a Vision Problem!" (S1) is an assumption because it's the core premise. "explicitly modeling positions in 2D is essential" (S49) is an assumption because it states a necessary condition for good performance.
    *   **Context**: I classified statements as "context" when they described the concrete experimental setup, the characteristics of the data, the model architecture, the training paradigm, or the evaluation metrics. These are factual descriptions of "what is" in the experiment. For example, "ARC consists of a collection of puzzle-like tasks" (S10) or "We use a ViT [17]" (S44) are clear contexts. The distinction often came down to whether the statement was a *justification* (assumption) or a *description* (context).

*   **Mechanism vs. a plain description of "what happened"**:
    *   **Mechanism**: I looked for causal explanations – statements that explain *why* an intervention produces an effect, or *how* a component contributes to a desired outcome. Keywords like "enables," "allows," "helps," "reduces," "improves by," "because," "due to," or phrases explaining "how X works" were strong indicators. For example, "represent the inputs on a “canvas\" that can be processed like natural images" (S5) is a mechanism because it explains *how* visual priors are incorporated. "patchification... incorporates... locality and translation invariance" (S47) explains *how* patchification is beneficial.
    *   **Plain description of "what happened"**: These were classified as "observable." If a statement merely reported a result or a behavior without explaining the underlying cause, it was an observable. For example, "VARC achieves 60.4% accuracy" (S8) is an observable. If a span contained both a result and an explanation, I tried to prioritize the core message. If the explanation was brief and directly tied to the result, I might classify the whole span as observable, but if the explanation was detailed and causal, I'd lean towards mechanism.

*   **Deciding when an intervention was implicit vs. genuinely absent (null)**:
    *   **Implicit Intervention**: In ablation studies or comparative statements (e.g., "X improves Y"), even if the text didn't explicitly say "we compared X to not-X," the comparison was implied by the structure of the experiment. For example, "we adopt multi-view inference to improve accuracy" (S60) implies a comparison to single-view inference.
    *   **Genuinely Absent (null)**: I would have used "null" if a claim was made (e.g., "X is good") but there was no mention or implication of any manipulation or comparison to test that claim within the provided text. In this paper, most claims about effectiveness or benefit were tied to an explicit or clearly implied intervention (e.g., "by adding X, accuracy increased"). Therefore, I did not use "null" for any intervention in this paper.

*   **What made an "observable" count as evidence for/against a mechanism vs. just a raw number?**:
    *   **Observable as evidence**: An observable is the raw, measurable outcome. When the text explicitly stated that an observable *suggests*, *indicates*, or *shows* something about a mechanism, the observable itself was the evidence. For example, "offline training greatly improves the performance of TTT, suggesting that common sense... can be learned" (S94). Here, the performance improvement is the observable, and the learning of common sense is the mechanism it provides evidence for.
    *   **Raw number**: Any specific metric, percentage, or measured behavior was an observable. "VARC achieves 54.5% accuracy" (S21) is a raw number. Visualizations (attention maps, t-SNE) were also classified as observables because they are direct outputs or behaviors of the model that are monitored.

*   **Rule of thumb invented mid-way**:
    *   **Prioritizing the core message in mixed spans**: Many spans contained elements of multiple categories. My rule of thumb was to identify the *primary intent* or *core information* being conveyed. If a span described an action and its direct result, I often classified it as "intervention" if the action was the focus, or "observable" if the result was the focus. If it described a component and *how* it worked, I leaned towards "mechanism." If it described a component and its properties, I leaned towards "context." This helped resolve ambiguities where a single sentence could technically touch upon two categories. For example, "Combining VARC models through ensembling [29] further improves accuracy to 60.4%" (S23) describes an intervention (ensembling) and an observable (improved accuracy). I classified it as "observable" because the primary information conveyed is the *result* of the ensembling, not just the act itself.

## What you deliberately did NOT extract

I deliberately excluded the following types of spans:

1.  **General introductory or concluding remarks**: Sentences that set a broad stage, express hopes for future research, or summarize the paper's contribution without detailing specific mechanisms, contexts, interventions, or observables. For example, "Learning and abstracting concepts from a small number of demonstrations is a key feature of intelligence" (Page 1, Section 1) or "We hope this work will encourage the community to leverage ARC..." (Page 8, Section 7). These are too high-level and don't fit the specific definitions.
2.  **Citations without specific claims**: While citations often point to sources of context or mechanisms, I only extracted the text *around* the citation if it contained a specific claim relevant to the categories. The citation itself (e.g., "[12]") was not extracted as a span.
3.  **Definitions of general concepts**: Descriptions of what "visual reasoning" or "ARC" generally entails, if not directly tied to the authors' specific experimental setup or claims. For example, "Visual reasoning is a long-standing research problem. It involves not only perceiving scenes and objects, but also inferring and abstracting the relations and transformations among them" (Page 2, Section 2). This is a general definition, not specific to their work's context, mechanism, etc.
4.  **Future work suggestions**: Statements about what *could* be done in the future, as these are not about the current paper's findings or methods. For example, "Future research may extend this direction through more expressive architectures..." (Page 8, Section 7).
5.  **Redundant information**: If a concept was introduced and described in detail (e.g., the canvas) and then later briefly mentioned again without new information or a new causal link, I generally only extracted the most comprehensive description.
6.  **Method names alone**: A method name like "Vision Transformer" or "U-Net" by itself was not extracted unless it was part of a sentence describing its use as an intervention, its properties as context, or its causal role as a mechanism. For example, "By default, we use a ViT [17]" (S44) was extracted as context.