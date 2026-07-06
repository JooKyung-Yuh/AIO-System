```json
[
  {
    "span_id": "S1",
    "text": "Common approaches to ARC treat it as a language-oriented problem, addressed by large language models (LLMs) or recurrent reasoning models.",
    "location": "Abstract",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the existing landscape of ARC research, setting the stage for their novel approach. It's about 'what is currently being done'.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S2",
    "text": "although the puzzle-like tasks in ARC are inherently visual, existing research has rarely approached the problem from a vision-centric perspective.",
    "location": "Abstract",
    "assigned_label": "context",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This highlights a gap in current research (context) and implicitly states their core belief about ARC (assumption). I lean towards context as it describes the state of research, which is a factual setting.",
    "ambiguity_reason": "The 'inherently visual' part could be an assumption, but the overall sentence describes a research gap."
  },
  {
    "span_id": "S3",
    "text": "In this work, we formulate ARC within a vision paradigm, framing it as an image-to-image translation problem.",
    "location": "Abstract",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the core approach or 'how' they are tackling the problem.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S4",
    "text": "To incorporate visual priors, we represent the inputs on a “canvas\" that can be processed like natural images.",
    "location": "Abstract",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains a specific design choice ('canvas') and its purpose ('incorporate visual priors', 'processed like natural images'), detailing 'how' it works.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S5",
    "text": "It is then natural for us to apply standard vision architectures, such as a vanilla Vision Transformer (ViT), to perform image-to-image mapping.",
    "location": "Abstract",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes the specific architectural choice (ViT) as a consequence of their vision paradigm, explaining 'how' they perform the mapping. While ViT is a context, its application here is part of their proposed mechanism.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S6",
    "text": "Our model is trained from scratch solely on ARC data and generalizes to unseen tasks through test-time train-ing.",
    "location": "Abstract",
    "assigned_label": "context",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This describes the training setup ('from scratch', 'ARC data only') and the generalization strategy ('test-time training'). The training setup is context, and the generalization strategy is a mechanism. I'll split this into two if possible, but as a single sentence, the training setup is more dominant as context.",
    "ambiguity_reason": "Contains both context (training setup) and mechanism (generalization strategy)."
  },
  {
    "span_id": "S7",
    "text": "generalizes to unseen tasks through test-time train-ing.",
    "location": "Abstract",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' the model achieves generalization.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S8",
    "text": "Our framework, termed Vision ARC (VARC), achieves 60.4% accuracy on the ARC-1 benchmark, substantially outperforming existing methods that are also trained from scratch.",
    "location": "Abstract",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a specific, measurable performance metric and a comparison, making it an observable.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S9",
    "text": "Our results are competitive with those of leading LLMs and close the gap to average human performance.",
    "location": "Abstract",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a comparison of performance against other systems and human benchmarks, a measurable outcome.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S10",
    "text": "The Abstraction and Reasoning Corpus (ARC) benchmark [12] was designed to incentivize machine learning research aimed at improving these capabilities.",
    "location": "Section 1",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the purpose and background of the ARC benchmark.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S11",
    "text": "ARC consists of a collection of puzzle-like tasks (Fig. 1, top), each containing only a few examples governed by a unique underlying transfor-mation rule.",
    "location": "Section 1",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This defines the nature and structure of ARC tasks.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S12",
    "text": "The model is expected to make predictions on each unseen task given a few examples.",
    "location": "Section 1",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the task requirement for the model.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S13",
    "text": "While humans are capable of solving various ARC tasks [25, 31, 32], the benchmark remains highly challenging for today's leading machine learning systems [44, 42].",
    "location": "Section 1",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the current state of performance on ARC, highlighting its difficulty for ML systems.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S14",
    "text": "These methods generally convert ARC inputs into se-quences of text tokens for language modeling.",
    "location": "Section 1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' LLM-based methods process ARC inputs.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S15",
    "text": "The LLMs are pre-trained on internet-scale data, from which they learn transferable common sense.",
    "location": "Section 1",
    "assigned_label": "context",
    "alternative_labels_considered": ["assumption", "mechanism"],
    "classification_reasoning": "This describes the pre-training setup for LLMs (context). The 'learn transferable common sense' is a proposed mechanism for LLMs, but here it's presented as a characteristic of their pre-training, making it more context for *their* approach.",
    "ambiguity_reason": "Could be seen as a mechanism of LLMs, but in the context of this paper, it's describing the background of competing models."
  },
  {
    "span_id": "S16",
    "text": "These models are trained from scratch on ARC data only and perform inference through recurrent, iterative reasoning.",
    "location": "Section 1",
    "assigned_label": "context",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This describes the training and inference setup for recurrent models, which are competing approaches. It's 'what they do', not 'how it works' in detail for their own model.",
    "ambiguity_reason": "The 'recurrent, iterative reasoning' could be a mechanism, but it's describing *other* models' approach, making it context for the comparison."
  },
  {
    "span_id": "S17",
    "text": "many concepts in ARC are inherently visual and physical: e.g., reflection, symme-try, and gravity, as shown in Fig. 1.",
    "location": "Section 1",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This is a foundational belief or premise that motivates their entire vision-centric approach. It's 'what they assume to be true' about ARC.",
    "ambiguity_reason": "Could be context if seen as a description of ARC, but it's presented as a justification for their approach, making it an underlying assumption."
  },
  {
    "span_id": "S18",
    "text": "Humans can solve these tasks not merely from the demonstrations, but by reason-ing through analogy to their common sense obtained from external experience. Such common sense can be acquired through observing the world, particularly, the visual world.",
    "location": "Section 1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This describes 'how' humans solve ARC tasks, proposing a causal explanation (analogy, common sense from visual world). The second sentence is an assumption that supports this mechanism.",
    "ambiguity_reason": "The second sentence could be an assumption, but it's part of the overall explanation of human reasoning."
  },
  {
    "span_id": "S19",
    "text": "Motivated by its visual nature, we approach ARC from a vision-centric perspective. We frame each puzzle as an image-to-image translation problem.",
    "location": "Section 1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a restatement of their core approach, explaining 'how' they formulate the problem.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S20",
    "text": "Abstraction and infer-ence can arise directly from visual learning, without explicit linguistic intermediates.",
    "location": "Section 1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This explains 'how' abstraction and inference are achieved in their framework (directly from visual learning). It's a causal explanation.",
    "ambiguity_reason": "Could be an assumption that visual learning is sufficient, but it's presented as a proposed way for these capabilities to arise."
  },
  {
    "span_id": "S21",
    "text": "With this connection, we can ap-ply standard vision models (e.g., Vision Transformers [17] or convolutional networks [30]) to tackle the ARC problem.",
    "location": "Section 1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' they leverage standard vision models for ARC, linking their formulation to existing tools.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S22",
    "text": "We demonstrate that incorporating visual priors is cru-cial. These priors include 2D spatial locality, translation invariance, and scale invariance.",
    "location": "Section 1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["observable"],
    "classification_reasoning": "This states the importance ('crucial') of visual priors and lists them, explaining 'why' they are important for their approach. The 'demonstrate' part points to an observable, but the core claim is about the importance of priors.",
    "ambiguity_reason": "The 'demonstrate' implies an observable, but the main point is the causal role of visual priors."
  },
  {
    "span_id": "S23",
    "text": "To facilitate learning these priors, we represent the inputs on a \"canvas\" with flexible geometric transformations, allowing the inputs to be pro-cessed as if they were natural images.",
    "location": "Section 1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' they facilitate learning visual priors using the 'canvas' concept.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S24",
    "text": "A patch on the can-vas can consist of exponentially many color combinations, which helps reduce overfitting and encourages the model to learn spatial priors rather than merely memorize.",
    "location": "Section 1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'why' patchification on the canvas is beneficial (reduces overfitting, encourages learning priors).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S25",
    "text": "With the vision-centric formulation, we train our model from scratch using ARC-only data.",
    "location": "Section 1",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the specific training data and initialization strategy.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S26",
    "text": "At inference time, when presented with a new, unseen task, we perform test-time training [9, 24, 49, 1, 53, 27] to adapt the model to the task, enabling it to generalize from only a few examples.",
    "location": "Section 1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' they achieve generalization to unseen tasks (test-time training for adaptation).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S27",
    "text": "VARC achieves 54.5% accuracy on the ARC-1 benchmark, using a small model with only 18 million parameters.",
    "location": "Section 1",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a specific, measurable performance metric and model size.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S28",
    "text": "This result substantially surpasses the best recurrent methods [53, 27] that are also trained from scratch on ARC.",
    "location": "Section 1",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a comparative performance result.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S29",
    "text": "Combining VARC models through ensembling [29] further improves accuracy to 60.4%, matching the reported average human performance [31] on the ARC-1 dataset.",
    "location": "Section 1",
    "assigned_label": "observable",
    "alternative_labels_considered": ["intervention"],
    "classification_reasoning": "The act of ensembling is an intervention, but the sentence focuses on the *result* of that intervention (improved accuracy and matching human performance), making it an observable.",
    "ambiguity_reason": "Contains both an intervention (ensembling) and its observable outcome."
  },
  {
    "span_id": "S30",
    "text": "the design of the ARC benchmark is based on human observations and induced rules abstracted from the visual and physical world. It is natural to explore vision-driven approaches for ARC.",
    "location": "Section 1",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This is a foundational premise about ARC's design that justifies their vision-driven approach. It's 'what they believe to be true' about ARC's nature.",
    "ambiguity_reason": "Could be context (description of ARC), but it's used as a justification for their approach, making it an underlying assumption."
  },
  {
    "span_id": "S31",
    "text": "human rea-soning is not confined to language or vision in isolation, but instead should integrate information across modalities.",
    "location": "Section 1",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This is a general belief about human intelligence that informs their broader perspective on abstract reasoning. It's a premise about how reasoning works.",
    "ambiguity_reason": "Could be a mechanism of human reasoning, but it's presented as a general statement about its nature."
  },
  {
    "span_id": "S32",
    "text": "Visual reasoning is a long-standing re-search problem. It involves not only perceiving scenes and objects, but also inferring and abstracting the relations and transformations among them.",
    "location": "Section 2",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This provides a definition and scope of visual reasoning, which is the broader field their work contributes to.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S33",
    "text": "The visual reasoning methods developed under these protocols typically consist of a visual perception mod-ule and a language-like recurrent module, e.g., within the neuro-symbolic framework [4, 23, 3, 41].",
    "location": "Section 2",
    "assigned_label": "context",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This describes the common architecture ('what they consist of') of existing visual reasoning methods, providing background for their own approach.",
    "ambiguity_reason": "Describes the components of other methods, which could be seen as their mechanisms, but here it's presented as background context."
  },
  {
    "span_id": "S34",
    "text": "These methods have evolved into modern vision-language models (VLMs, e.g., [2, 33, 37]), in which images are converted into tokens and processed jointly with text.",
    "location": "Section 2",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This explains 'how' VLMs process images and text, describing their operational principle.",
    "ambiguity_reason": "Could be context if seen as a description of VLMs, but it explains their processing method."
  },
  {
    "span_id": "S35",
    "text": "Unlike ARC, classical visual reasoning protocols gener-ally involve a training set and a test set, both of which can be viewed as instances of the same task.",
    "location": "Section 2",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This highlights a key difference between ARC and classical visual reasoning, defining the problem space.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S36",
    "text": "ARC consists of a large collection of distinct tasks, each defined by only a few examples.",
    "location": "Section 2",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This reiterates the specific nature of ARC tasks.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S37",
    "text": "A new task can be converted into a sequence of tokens, treated as a prompt, and processed by LLMs via in-context few-shot learning [55, 10].",
    "location": "Section 2",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' LLMs approach ARC tasks.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S38",
    "text": "These models aim to mimic the hierarchical and multi-timescale processing of the human brain [53] for reasoning.",
    "location": "Section 2",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the underlying principle or 'how' recurrent models are designed to reason.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S39",
    "text": "At inference time, these methods adopt test-time training [9, 24, 49] on the few demonstration examples.",
    "location": "Section 2",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains the inference strategy ('how' they perform inference) for recurrent models.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S40",
    "text": "the ViT-ARC method [34] attempts to address the ARC problem using vision models.",
    "location": "Section 2",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a related work and its general approach, providing context for their own vision-based method.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S41",
    "text": "this method has only shown the ability to fit individual tasks in the training set; it is unable to generalize or solve any unseen test task.",
    "location": "Section 2",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is an empirical result or observed limitation of a competing method.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S42",
    "text": "the ARC protocol, whose essence lies pre-cisely in few-shot, cross-task generalization.",
    "location": "Section 2",
    "assigned_label": "context",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This defines a core requirement of the ARC benchmark, which is a characteristic of the problem setting.",
    "ambiguity_reason": "Could be an assumption if it's what they *must* achieve, but it's presented as a definition of the protocol's essence."
  },
  {
    "span_id": "S43",
    "text": "we formulate reasoning on each task as an image-to-image translation problem.",
    "location": "Section 3.2",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is the core 'how' of their approach.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S44",
    "text": "We frame the problem as per-pixel classification, analogous to the seman-tic segmentation problem [38].",
    "location": "Section 3.2",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This specifies the exact problem framing ('how' they define the output task).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S45",
    "text": "The network fe takes an image xi as input, conditioned on a task token associated with the task T.",
    "location": "Section 3.2",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the input structure and conditioning ('how' the network receives information).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S46",
    "text": "The task token is represented as a learnable embedding dependent on T.",
    "location": "Section 3.2",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' the task token is represented.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S47",
    "text": "The output of fe is a grid where each position represents a categorical distribution.",
    "location": "Section 3.2",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the output format ('what' the network produces and 'how' it's structured).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S48",
    "text": "The overall objective function is simply the per-pixel cross-entropy loss [38]: L(0) = ET,i [D(yi, fo(xi | T))].",
    "location": "Section 3.2",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This defines the loss function, which is a core part of 'how' the model learns.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S49",
    "text": "Previous methods on ARC generally operate in the space of discrete-valued tokens, motivated by the design of language models.",
    "location": "Section 3.3",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the approach of other methods, providing background for their own contrasting approach.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S50",
    "text": "In our formulation of image-to-image translation, we explore native designs developed for vision.",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This states their design philosophy ('how' they approach the problem).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S51",
    "text": "While it is straightforward to view the raw H×W grid as an H×W image, we propose more flexible transfor-mations to represent it in a manner similar to natural images.",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This introduces the 'canvas' concept and its purpose ('how' they represent inputs more flexibly).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S52",
    "text": "We define the concept of a \"canvas\". A canvas has a predefined and sufficiently large size, e.g., 64×64. The raw input is transformed and placed onto this canvas.",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This defines the 'canvas' and describes 'how' inputs are placed on it.",
    "ambiguity_reason": "Could be context (a description of a component), but it's a core part of their proposed method's operation."
  },
  {
    "span_id": "S53",
    "text": "This for-mulation naturally accommodates translation and scale aug-mentations, which are common strategies for introducing translation and scale invariance in vision, discussed next.",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This explains 'how' the canvas enables augmentations and 'why' those augmentations are used (to introduce invariance). The latter part is an assumption.",
    "ambiguity_reason": "Contains both a mechanism (canvas enables augmentations) and an assumption (augmentations introduce invariance)."
  },
  {
    "span_id": "S54",
    "text": "translation and scale invariance in vision",
    "location": "Section 3.3",
    "assigned_label": "assumption",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is an underlying belief about what is important for vision models.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S55",
    "text": "We set the background of the canvas to an additional back-ground color, i.e., the (C+1)-th color.",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes a specific design choice for the canvas, explaining 'how' it's configured.",
    "ambiguity_reason": "Could be context (a parameter), but it's part of the operational design."
  },
  {
    "span_id": "S56",
    "text": "if we naïvely treat each raw pixel as a token, there would be only C distinct tokens.",
    "location": "Section 3.3",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a baseline or alternative approach and its characteristic, providing context for why their canvas approach is better.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S57",
    "text": "our canvas formulation sup-ports a much larger set of local, patch-level configurations.",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' the canvas formulation provides a benefit (larger set of configurations).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S58",
    "text": "with a patch size of 2×2 (see Fig. 5), a single patch can contain multiple colors and, in principle, has an exponentially large cardinality, O(C2×2).",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' the patchification on canvas leads to increased cardinality.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S59",
    "text": "This formulation is important for improving generalization performance.",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["observable"],
    "classification_reasoning": "This states the causal effect ('improving generalization performance') of the canvas formulation, explaining 'why' it's important.",
    "ambiguity_reason": "Could be an observable if it were an empirical result, but it's a claim about the mechanism's benefit."
  },
  {
    "span_id": "S60",
    "text": "The “canvas\" concept enables us to flexibly apply translation and scale augmen-tations, which are critical in standard vision models.",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This explains 'how' the canvas enables augmentations. The 'critical in standard vision models' part is an assumption that justifies the use of these augmentations.",
    "ambiguity_reason": "Contains both a mechanism and an assumption."
  },
  {
    "span_id": "S61",
    "text": "These data augmentations encourage the model to learn un-derlying mappings invariant to geometric transformations grounded in the visual world.",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' data augmentations achieve their goal (learning invariant mappings).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S62",
    "text": "Scale augmentation: Given a raw input, we randomly resize it by an integer scaling ratio s, duplicating each raw pixel into s×s (see Fig. 4, left).",
    "location": "Section 3.3",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This describes a specific manipulation performed on the input data. It's a controlled change to the input.",
    "ambiguity_reason": "Could be seen as a mechanism if it explained *why* this specific resizing works, but it's describing *what* is done."
  },
  {
    "span_id": "S63",
    "text": "This is analo-gous to nearest-neighbor interpolation in natural im-ages.",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This provides an analogy, explaining 'how' to understand the scaling operation in familiar terms.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S64",
    "text": "“colors” in ARC do not cor-respond to real-world colors, so it is not meaningful to perform other interpolations (such as bilinear).",
    "location": "Section 3.3",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This is a premise about the nature of ARC colors that dictates what interpolation methods are appropriate. It's a constraint on their approach.",
    "ambiguity_reason": "Could be context (a property of ARC), but it's used to justify a specific design choice (no bilinear interpolation)."
  },
  {
    "span_id": "S65",
    "text": "Translation augmentation: given the scaled grid, we randomly place it on the fixed-size canvas. We ensure all pixels are visibile. See Fig. 4 (right).",
    "location": "Section 3.3",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This describes a specific manipulation performed on the input data.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S66",
    "text": "We empirically show that these visual priors are important for generalization to unseen tasks.",
    "location": "Section 3.3",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This is a statement about an empirical finding, a measurable result.",
    "ambiguity_reason": "The 'important for generalization' part is a mechanism, but the 'empirically show' makes it an observable."
  },
  {
    "span_id": "S67",
    "text": "Given a canvas with an input ran-domly placed, we perform image-to-image translation by a standard vision model. By default, we use a ViT [17].",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes the core operational step ('how' they perform translation) and the default architecture choice.",
    "ambiguity_reason": "The ViT choice could be context, but its application is part of the mechanism."
  },
  {
    "span_id": "S68",
    "text": "The principle of ViT is Transformer on patches. For-mally, the input canvas is divided into non-overlapping patches (e.g., 2×2), projected by a linear embedding, added with positional embedding [52], and processed by a stack of Transformer blocks [52].",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This details the architectural components and processing steps of the ViT, explaining 'how' it operates.",
    "ambiguity_reason": "Could be context (description of ViT), but it's explaining the operational details of their chosen model."
  },
  {
    "span_id": "S69",
    "text": "The model has a linear projec-tion layer as the output, which performs per-pixel classifica-tion for each patch.",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the output layer and its function ('how' the model produces predictions).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S70",
    "text": "unlike natural images where each raw pixel has continuous values, in our case, the raw pixels have discrete values.",
    "location": "Section 3.3",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a specific characteristic of ARC pixel values, setting the context for their embedding choice.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S71",
    "text": "Therefore, before patchifica-tion, we first map each pixel's discrete index into a learnable continuous-valued embedding.",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' discrete pixel values are handled before patchification.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S72",
    "text": "Conceptually, patchification can be viewed as a special form of convolution. Like convolution, it incorporates sev-eral critical inductive biases in vision: most notably, local-ity (i.e., grouping nearby pixels) and translation invariance (i.e., weight sharing across locations).",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This explains 'why' patchification is beneficial (incorporates inductive biases) and 'how' it relates to convolution.",
    "ambiguity_reason": "The inductive biases could be seen as assumptions, but here they are presented as benefits of the mechanism."
  },
  {
    "span_id": "S73",
    "text": "Unlike language data, which is generally modeled as 1D sequences, images are inherently 2D. This 2D structure can be lost if we naïvely treat the embedded patches as a 1D sequence.",
    "location": "Section 3.3",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This is a premise about the nature of images (inherently 2D) and a potential problem if this is ignored, justifying their 2D positional embedding.",
    "ambiguity_reason": "Could be context (a property of images), but it's used to justify a design choice, making it an underlying assumption."
  },
  {
    "span_id": "S74",
    "text": "We empirically show that explicitly modeling positions in 2D is essential.",
    "location": "Section 3.3",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This is a statement about an empirical finding, a measurable result.",
    "ambiguity_reason": "The 'essential' part is a mechanism, but the 'empirically show' makes it an observable."
  },
  {
    "span_id": "S75",
    "text": "Formally, we adopt separable 2D positional embed-dings, following [11]: with D channels for positional em-beddings, we use the first half of the channels to embed the horizontal coordinate and the second half to embed the vertical coordinate.",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes the specific implementation details of their 2D positional embeddings, explaining 'how' they are constructed.",
    "ambiguity_reason": "Could be context (a specific component), but it's explaining the operational details."
  },
  {
    "span_id": "S76",
    "text": "This can be applied both to additive po-sitional embeddings for encoding absolute positions and to the encoding of relative positions (e.g., RoPE [48]).",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains the applicability and function of the 2D positional embeddings ('how' they are used).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S77",
    "text": "Beyond ViT, we also study the more classical vision-based architecture, i.e., convolutional neural networks [30].",
    "location": "Section 3.3",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a deliberate action taken in their experiments (studying CNNs).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S78",
    "text": "Specifically, we adopt the U-Net model [46], a hierarchical convolutional network.",
    "location": "Section 3.3",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This specifies the particular CNN architecture chosen for comparison.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S79",
    "text": "The original U-Net was proposed precisely for the image-to-image translation problem of segmentation [46], making it a natural candidate for the problem we consider.",
    "location": "Section 3.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This explains 'why' U-Net is a suitable choice for their problem.",
    "ambiguity_reason": "Could be context (history of U-Net), but it's explaining its suitability for their problem."
  },
  {
    "span_id": "S80",
    "text": "We adopt a two-stage training paradigm to learn the param-eters of the neural network.",
    "location": "Section 3.4",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the overall training strategy ('how' they train the network).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S81",
    "text": "This stage is applied on the entire train-ing set Ttrain. It is on all demos Ddemo for any T∈ Ttrain.",
    "location": "Section 3.4",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This defines the scope and data used for the offline training stage.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S82",
    "text": "We train one model fe jointly for all k training tasks (e.g., k=400), based on the loss in Eq. (1).",
    "location": "Section 3.4",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes 'how' the offline training is performed (jointly, using the loss function).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S83",
    "text": "All tasks share the same parameters, only except that each task has its own task-conditional token.",
    "location": "Section 3.4",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes the parameter sharing strategy, explaining 'how' the model handles multiple tasks.",
    "ambiguity_reason": "Could be context (a characteristic of the model), but it's part of the training mechanism."
  },
  {
    "span_id": "S84",
    "text": "We do not use the inference set Dinfer from the training tasks (i.e., T∈ Ttrain) to train the model. These sets are used only for validation purposes.",
    "location": "Section 3.4",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This specifies how certain data subsets are used, defining the experimental setup.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S85",
    "text": "Given a single new, unseen task T∈ Ttest from the test set, we perform inference by test-time training.",
    "location": "Section 3.4",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the core inference strategy ('how' they perform inference on new tasks).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S86",
    "text": "At inference time, we are given Ddemo={(xi, Yi)}m i=1 with both input and output accessi-ble; the model is required to make prediction for a given Xinfer in this new task T.",
    "location": "Section 3.4",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the specific data available and the task requirement during test-time training.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S87",
    "text": "We perform test-time training for each new task T inde-pendently.",
    "location": "Section 3.4",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This describes a specific choice in how TTT is applied (independently per task), which is a manipulation for experimental comparison later.",
    "ambiguity_reason": "Could be a mechanism, but it's a specific choice that is later ablated against 'jointly'."
  },
  {
    "span_id": "S88",
    "text": "It has a new task token whose parameters are randomly initialized.",
    "location": "Section 3.4",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' the task token for a new task is handled.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S89",
    "text": "As there are very few demo pairs in Ddemo (e.g., 2 to 4), we also perform data augmentation.",
    "location": "Section 3.4",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This describes a deliberate action (data augmentation) taken during TTT, motivated by the context of few demo pairs.",
    "ambiguity_reason": "The motivation is a mechanism, but the action itself is an intervention."
  },
  {
    "span_id": "S90",
    "text": "at inference time, the model is initialized from offline training, fine-tuned with test-time training only for the single new task T, and then performs inference on Xinfer.",
    "location": "Section 3.4",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This summarizes the entire TTT process, explaining 'how' inference is performed.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S91",
    "text": "As the new demo pairs in Ddemo are very few, even with data augmentation, this test-time training process re-mains reasonably fast (e.g., 70 seconds per task on a single GPU).",
    "location": "Section 3.4",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a measurable characteristic of the TTT process (speed).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S92",
    "text": "After test-time training, we apply fe to Xinfer to obtain the final prediction.",
    "location": "Section 3.5",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the final step of prediction ('how' the output is generated).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S93",
    "text": "This process is analogous to the classical recognition problems [29, 38]. Accordingly, we adopt post-processing strategies inspired by recognition methods.",
    "location": "Section 3.5",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This explains 'how' they perform post-processing, drawing an analogy to classical methods.",
    "ambiguity_reason": "The analogy is context, but the adoption of strategies is a mechanism."
  },
  {
    "span_id": "S94",
    "text": "Given Xinfer and a single \"view\" (i.e., with a given scale and translation), we place Xinfer on the canvas and apply fe to predict the output.",
    "location": "Section 3.5",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This describes the setup for single-view inference, which is a specific condition for an experiment.",
    "ambiguity_reason": "Describes a specific way of doing inference, which is an intervention for comparison with multi-view."
  },
  {
    "span_id": "S95",
    "text": "Since one output location in the raw grid may be predicted by multi-ple pixels on the canvas (e.g., due to rescaling; see Fig. 5), we aggregate all predictions (from softmax outputs) at this location by average pooling.",
    "location": "Section 3.5",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' predictions are aggregated for single-view inference, addressing a specific challenge.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S96",
    "text": "we adopt multi-view inference to im-prove accuracy, where the views are sampled with different augmentations.",
    "location": "Section 3.5",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This describes a deliberate action (adopting multi-view inference) with a stated goal (improve accuracy). The action itself is the intervention.",
    "ambiguity_reason": "The goal is a mechanism, but the action is an intervention."
  },
  {
    "span_id": "S97",
    "text": "As the multi-view inference cost is negli-gible compared with test-time training cost, it is virtually nearly free to use many views.",
    "location": "Section 3.5",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This is a premise about the computational cost that allows them to use many views without significant overhead. It's a condition that must hold.",
    "ambiguity_reason": "Could be context (a characteristic of the system), but it's a justification for a design choice, making it an assumption."
  },
  {
    "span_id": "S98",
    "text": "Predictions from different views are consolidated by majority voting [1].",
    "location": "Section 3.5",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' predictions from multiple views are combined.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S99",
    "text": "The ARC benchmark by default adopts the pass@2 accuracy metric: i.e., two different solutions can be produced for evaluation, and a task is considered correct if one is correct.",
    "location": "Section 3.5",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This defines the standard evaluation metric for ARC, which is part of the experimental setup.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S100",
    "text": "To support this metric, we adopt majority voting in multi-view inference and retain the top-2 most populated output solutions.",
    "location": "Section 3.5",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' they adapt their inference to meet the pass@2 metric.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S101",
    "text": "In our best-performing model, the canvas size is 64×64.",
    "location": "Section 4",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This specifies a concrete parameter of their model.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S102",
    "text": "In the case of ViT, the patch size is 2×2, resulting in a sequence length of 322.",
    "location": "Section 4",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This specifies concrete parameters of their ViT model.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S103",
    "text": "For scale augmentation, an in-teger scaling ratio is randomly sampled, such that the scaled grid is no larger than the canvas size.",
    "location": "Section 4",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the specific parameters and constraints for scale augmentation.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S104",
    "text": "For translation aug-mentation, the upper-left corner is randomly sampled under the constraint that the placed image is fully visible.",
    "location": "Section 4",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the specific parameters and constraints for translation augmentation.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S105",
    "text": "We use the standard ARC-1 training set Ttrain for training: it has 400 tasks with 2-4 demo pairs each.",
    "location": "Section 4",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This specifies the dataset used for offline training.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S106",
    "text": "we also expand our training set with the RE-ARC set [22], from which we sam-ple 1,000 additional demo pairs per task.",
    "location": "Section 4",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a deliberate action to modify the training data.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S107",
    "text": "Put together, our full training set has about 400k sample pairs.",
    "location": "Section 4",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the total size of the training data.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S108",
    "text": "We apply translation and scale augmentation in offline training.",
    "location": "Section 4",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a deliberate action taken during offline training.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S109",
    "text": "Given an unseen task T∈ Ttest, we have 2-4 sample pairs in Ddemo.",
    "location": "Section 4",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the data available for test-time training.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S110",
    "text": "To make test-time training more feasible, we also augment the single task T into mul-tiple auxiliary tasks.",
    "location": "Section 4",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This describes a deliberate action (augmenting tasks) with a stated purpose (feasibility). The action is the intervention.",
    "ambiguity_reason": "The purpose is a mechanism, but the action is an intervention."
  },
  {
    "span_id": "S111",
    "text": "We do this by using standard augmen-tation from existing ARC methods: flip, rotation (by 90°, 180°, or 270°), and color permutation.",
    "location": "Section 4",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This lists the specific augmentations applied, which are deliberate manipulations.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S112",
    "text": "We treat each of these test-time training augmentations as an auxiliary task, each assigned a task embedding.",
    "location": "Section 4",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' the augmentations are incorporated into the TTT framework.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S113",
    "text": "We also apply translation and scale augmentation in test-time training, but we do not view them as a new auxiliary task (under the assumption that all auxiliary tasks are translation and scale invariant).",
    "location": "Section 4",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a deliberate action (applying augmentations) and a specific condition for it (not viewing as new auxiliary tasks). The condition is an assumption.",
    "ambiguity_reason": "Contains both an intervention and an assumption."
  },
  {
    "span_id": "S114",
    "text": "all auxiliary tasks are translation and scale invariant",
    "location": "Section 4",
    "assigned_label": "assumption",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a premise that justifies treating certain augmentations differently during TTT.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S115",
    "text": "Our experiments are primarily conducted on the benchmark of ARC-1 [12].",
    "location": "Section 5",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This specifies the primary experimental setting.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S116",
    "text": "We report the pass@2 accuracy (referred to simply as \"accuracy” hereafter) in percentage (%).",
    "location": "Section 5",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This defines the primary metric used for reporting results.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S117",
    "text": "To support pass@2 evaluation, we adopt multi-view inference.",
    "location": "Section 5",
    "assigned_label": "intervention",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This describes a deliberate action taken to enable a specific evaluation metric.",
    "ambiguity_reason": "The purpose is a mechanism, but the action is an intervention."
  },
  {
    "span_id": "S118",
    "text": "We also report final results on ARC-2 [14].",
    "location": "Section 5",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This specifies an additional benchmark used for evaluation.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S119",
    "text": "We evaluate our model on the ARC-1 evaluation set (i.e., Teval). This set is conceptually a test set (see Fig. 3), but with ground truth available only for computing accuracy.",
    "location": "Section 5",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the specific dataset used for evaluation and its characteristics.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S120",
    "text": "We compare variants of ViTs and U-Nets of similar sizes.",
    "location": "Table 1",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a controlled comparison between different model architectures.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S121",
    "text": "ViT ... acc. 44.4, 54.5, 53.0. U-Net ... acc. 42.8, 47.5, 48.3.",
    "location": "Table 1",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "These are specific, measurable performance results.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S122",
    "text": "Accuracy is reported on the ARC-1 evaluation set. The model used is ViT-18M.",
    "location": "Figure 7",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This specifies the experimental setup for the ablation study.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S123",
    "text": "Entries (a-c) use a patch size of 1×1 on a 32×32 canvas, whereas entries (d-f) use a patch size of 2×2 on a 64×64 canvas. Each entry modifies the one above it.",
    "location": "Figure 7",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the specific manipulations (changing patch/canvas size, adding components) performed in the ablation study.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S124",
    "text": "These vision priors cumulatively yield 27.7 improvement (a→f), in which the canvas-based designs (c→f) contribute an 11.5 gain.",
    "location": "Figure 7",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a measurable performance gain attributed to the interventions.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S125",
    "text": "Extending from 1D posi-tional embedding to its 2D counterpart is beneficial: see Fig. 7(b)(c).",
    "location": "Section 5.1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["observable"],
    "classification_reasoning": "This states a causal effect ('beneficial') of using 2D positional embedding. The 'see Fig. 7(b)(c)' points to the observable.",
    "ambiguity_reason": "States a benefit (mechanism) and points to evidence (observable)."
  },
  {
    "span_id": "S126",
    "text": "To demonstrate this effect on a stronger baseline, we re-place the 2D ROPE in Fig. 7(f) with a 1D ROPE and observe a degradation of 3.5 points, from 54.5 to 51.0.",
    "location": "Section 5.1",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a deliberate manipulation (replacing 2D ROPE with 1D ROPE) to test an effect.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S127",
    "text": "degradation of 3.5 points, from 54.5 to 51.0.",
    "location": "Section 5.1",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a specific, measurable performance drop.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S128",
    "text": "A key design principle of our method is to prepare the input as a natural image. This enables the expansion of the token set from a very limited size (e.g., 10) to an exponentially large number.",
    "location": "Section 5.1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'why' preparing input as a natural image is a key principle and 'how' it benefits (token set expansion).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S129",
    "text": "In Fig. 7(d), we advance from 1×1 patches on a 32×32 canvas to 2×2 patches on a 64×64 canvas.",
    "location": "Section 5.1",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a specific manipulation of patch and canvas size.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S130",
    "text": "Doing so does not increase the computational cost of the Transformer.",
    "location": "Section 5.1",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a characteristic of the intervention, not its effect on accuracy, but a constraint or property of the setup.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S131",
    "text": "to ensure a meaningful compar-ison, we do not impose this constraint, allowing each 2×2 patch to cover multiple colors.",
    "location": "Section 5.1",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a deliberate choice (not imposing constraint) to enable a fair comparison.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S132",
    "text": "This can be interpreted as one-pixel translation augmentation on the canvas.",
    "location": "Section 5.1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This provides an interpretation of the patchification, explaining 'how' it functions as an augmentation.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S133",
    "text": "Even so, the 2×2 patchification leads to a noticeable gain of 2.4 points, improving from 43.0 to 45.4; see Fig. 7(c,d).",
    "location": "Section 5.1",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a specific, measurable performance gain.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S134",
    "text": "In spite of the small one-pixel augmentation, each patch can cover multiple colors (as in natural images), which substan-tially enriches the data space for learning.",
    "location": "Section 5.1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'why' multi-color patches are beneficial (enriches data space).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S135",
    "text": "In image recogni-tion, even highly capable network architectures still benefit greatly from translation and scale augmentations.",
    "location": "Section 5.1",
    "assigned_label": "assumption",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This is a general belief or established fact in vision that they are applying to ARC, serving as a premise for their augmentations.",
    "ambiguity_reason": "Could be context (general knowledge), but it's used as a justification for their approach, making it an assumption."
  },
  {
    "span_id": "S136",
    "text": "In Fig. 7(e), we apply fully flexible translation augmen-tation on the canvas. Compared with the \"one-pixel\" aug-mentation in Fig. 7(d), this setting yields an additional gain of 2.9 points (from 45.4 to 48.3).",
    "location": "Section 5.1",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a specific manipulation (fully flexible translation augmentation) and its comparison.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S137",
    "text": "additional gain of 2.9 points (from 45.4 to 48.3).",
    "location": "Section 5.1",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a specific, measurable performance gain.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S138",
    "text": "In Fig. 7(f), we further ap-ply the scale augmentation enabled by the concept of can-vas. Scale augmentation yields a substantial gain of 6.2 points.",
    "location": "Section 5.1",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a specific manipulation (scale augmentation) and its result.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S139",
    "text": "substantial gain of 6.2 points.",
    "location": "Section 5.1",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a specific, measurable performance gain.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S140",
    "text": "Unlike translation invariance, which can be partially addressed by patchification (i.e., a special form of convo-lution), the ViT architecture has little to no inductive bias about scale invariance.",
    "location": "Section 5.1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This explains a characteristic of the ViT architecture ('little to no inductive bias') and contrasts it with translation invariance, explaining 'why' scale augmentation is needed.",
    "ambiguity_reason": "Could be an assumption about ViT's properties, but it's presented as an explanation for an observed effect."
  },
  {
    "span_id": "S141",
    "text": "This can explain why scale augmen-tation yields a substantial gain.",
    "location": "Section 5.1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This provides a causal explanation for the observed gain from scale augmentation.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S142",
    "text": "In Tab. 1, we compare ViT with U-Nets, a type of convolutional network.",
    "location": "Section 5.2",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a controlled comparison between two architectures.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S143",
    "text": "We evaluate three model sizes for each architecture.",
    "location": "Section 5.2",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This specifies the range of model sizes used in the comparison.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S144",
    "text": "Although ViTs consistently per-form better, all U-Net variants achieve decent accuracy, sug-gesting that this problem can also be effectively addressed by classical vision backbones.",
    "location": "Section 5.2",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This reports the comparative performance results. The 'suggesting' part is an interpretation, but the core is the observed performance.",
    "ambiguity_reason": "Contains an observable (performance) and an interpretation (mechanism)."
  },
  {
    "span_id": "S145",
    "text": "In Fig. 8, we show ViTs with varying depths and widths.",
    "location": "Section 5.2",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a manipulation of model parameters (depth and width).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S146",
    "text": "In this regime, our method demonstrates good scalability: increasing depth and/or width leads to higher accuracy as a result of better fitting.",
    "location": "Section 5.2",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This reports an observed trend (scalability, higher accuracy with increased depth/width). The 'as a result of better fitting' is a mechanism.",
    "ambiguity_reason": "Contains an observable (scalability) and a mechanism (better fitting)."
  },
  {
    "span_id": "S147",
    "text": "regime can lead to overfitting in our current setting, as shown in Tab. 1 for the 66M ViT model.",
    "location": "Section 5.2",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This describes an observed behavior (overfitting) for a specific model size.",
    "ambiguity_reason": "Overfitting is a mechanism, but here it's presented as an observed outcome."
  },
  {
    "span_id": "S148",
    "text": "We observe that this larger model achieves higher training accuracy, sug-gesting that future research should focus on generalization.",
    "location": "Section 5.2",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This reports an observed performance (higher training accuracy). The 'suggesting' part is a recommendation for future research, not a mechanism of their model.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S149",
    "text": "In Fig. 9(b), we study TTT with and without offline training, and TTT performed jointly on all test tasks vs. independently for each test task.",
    "location": "Section 5.2",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a set of controlled comparisons for TTT strategies.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S150",
    "text": "As expected, offline training greatly improves the per-formance of TTT, suggesting that common sense about the visual world can be learned from the training set.",
    "location": "Section 5.2",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This reports an observed performance improvement. The 'suggesting' part is an interpretation of *why* this happens, which is a mechanism.",
    "ambiguity_reason": "Contains both an observable (performance improvement) and a mechanism (common sense learned)."
  },
  {
    "span_id": "S151",
    "text": "even without offline training, our TTT strategy can achieve nontrivial accuracy (26.4), suggesting that some tasks in this benchmark can be solved tabula rasa.",
    "location": "Section 5.2",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This reports a specific accuracy achieved under a condition. The 'suggesting' part is an interpretation of *why* this is possible, which is a mechanism.",
    "ambiguity_reason": "Contains both an observable (accuracy) and a mechanism (tasks solvable tabula rasa)."
  },
  {
    "span_id": "S152",
    "text": "This result outperforms that in [36] under a similar setting.",
    "location": "Section 5.2",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a comparative performance result.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S153",
    "text": "Surprisingly, performing TTT independently for each test task yields substantially better performance (by ~10 points) than doing so jointly across all test tasks, even though the latter relies on a stronger assumption about the availability of multiple test tasks at once.",
    "location": "Section 5.2",
    "assigned_label": "observable",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This reports a comparative performance result. The 'stronger assumption' is a condition for the joint TTT, making it an assumption for that specific intervention.",
    "ambiguity_reason": "Contains an observable (performance difference) and an assumption (stronger assumption for joint TTT)."
  },
  {
    "span_id": "S154",
    "text": "the latter relies on a stronger assumption about the availability of multiple test tasks at once.",
    "location": "Section 5.2",
    "assigned_label": "assumption",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a premise or precondition for the 'joint TTT' intervention.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S155",
    "text": "We hypothesize that overtraining on the test tasks may cause the model to forget the knowledge acquired during offline training.",
    "location": "Section 5.2",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a proposed causal explanation ('may cause') for an observed or potential behavior.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S156",
    "text": "we adopt multi-view inference by default.",
    "location": "Section 5.2",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the standard setting for their inference.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S157",
    "text": "For completeness, we also examine the single-view inference accuracy. Since single-view inference cannot produce mul-tiple predictions, we compare pass@1 accuracy. See Tab. 2.",
    "location": "Section 5.2",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a deliberate action (examining single-view inference) for comparison.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S158",
    "text": "Single-view inference has a decent pass@1 accuracy of 35.9; multi-view inference further boosts to 49.8, thanks to majority voting.",
    "location": "Section 5.2",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This reports specific performance metrics and the improvement. The 'thanks to majority voting' is a mechanism.",
    "ambiguity_reason": "Contains an observable (accuracy) and a mechanism (majority voting)."
  },
  {
    "span_id": "S159",
    "text": "Unlike typical computer vision applica-tions such as semantic segmentation, in ARC, a mistake on even a single pixel renders the entire prediction incorrect.",
    "location": "Section 5.2",
    "assigned_label": "context",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This describes a characteristic of the ARC problem's evaluation, which is part of the problem setting.",
    "ambiguity_reason": "Could be an assumption about ARC's strictness, but it's a description of the evaluation criteria."
  },
  {
    "span_id": "S160",
    "text": "This may explain the large gain seen here.",
    "location": "Section 5.2",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This provides a causal explanation ('may explain') for an observed phenomenon.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S161",
    "text": "In Tab. 3 we compare with leading results using LLMs or recurrent models, on ARC-1 and ARC-2.",
    "location": "Section 5.3",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a controlled comparison with other state-of-the-art models.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S162",
    "text": "Our model compares favorably with some of the most powerful LLMs at the time their results were reported: in-cluding Deepseek, Claude, o3, and GPT-5",
    "location": "Section 5.3",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This reports a comparative performance result.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S163",
    "text": "LLMs are pre-trained on internet-scale data, and some may also incor-porate multimodal data that include images.",
    "location": "Section 5.3",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the pre-training data of competing models, providing background for comparison.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S164",
    "text": "Our method does not rely on such data and uses a model that is several orders of magnitude smaller.",
    "location": "Section 5.3",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes characteristics of their model and training data, highlighting differences from LLMs.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S165",
    "text": "In the controlled setting of training from scratch on ARC data, our method substantially outperforms the recur-rent models: HRM [53] and TRM [27].",
    "location": "Section 5.3",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This reports a comparative performance result under specific conditions.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S166",
    "text": "Our VARC with 18M parameters is ~10 points better than TRM on ARC-1, a >20% relative improvement.",
    "location": "Section 5.3",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This reports a specific, measurable performance gain.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S167",
    "text": "once test-time training is completed, our model performs fully feedfor-ward inference, with no recurrence involved in reasoning.",
    "location": "Section 5.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' the model operates after TTT, emphasizing the lack of recurrence.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S168",
    "text": "we ensemble one ViT and one U-Net, each with test-time training run four times.",
    "location": "Section 5.3",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a deliberate action (ensembling) and its specific setup.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S169",
    "text": "Doing so boosts our result to 60.4. This result closes the gap with the re-ported average human performance (60.2 [31]).",
    "location": "Section 5.3",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This reports the specific performance gain and its comparison to human performance.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S170",
    "text": "Attention patterns. Fig. 10 shows the attention patterns of our ViT model in a test task.",
    "location": "Section 6",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a visual output that reveals model behavior.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S171",
    "text": "These attention maps show that our model can correctly reason about the relationship between a source pixel and its target pixel to copy from.",
    "location": "Section 6",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["observable"],
    "classification_reasoning": "This interprets the attention maps, explaining 'how' the model reasons.",
    "ambiguity_reason": "It's an interpretation of an observable, explaining the underlying process."
  },
  {
    "span_id": "S172",
    "text": "Figure 11 visualizes the layer-wise attention maps for an-other test task.",
    "location": "Section 6",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a visual output that reveals model behavior.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S173",
    "text": "A layer-wise map is the softmax attention map averaged across all pixels in the layer: it reveals which pixels receive the most attention in that layer.",
    "location": "Section 6",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' the layer-wise map is constructed and 'what' it reveals about the model's focus.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S174",
    "text": "In this task, different layers exhibit different specialties: some layers at-tend to the pixels that are to be copied, and some layers attend to the target lines alone the eight directions.",
    "location": "Section 6",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["observable"],
    "classification_reasoning": "This describes a specific behavior of the model's layers, explaining 'how' they contribute to reasoning.",
    "ambiguity_reason": "It's an interpretation of an observable, explaining the underlying process."
  },
  {
    "span_id": "S175",
    "text": "Our model is conditioned on a task token, with an embedding learned to represent each task.",
    "location": "Section 6",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This explains 'how' the model is conditioned on tasks.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S176",
    "text": "With 400 training tasks in ARC-1, our model learns 400 distinct task embeddings in offline training.",
    "location": "Section 6",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the scope and data for learning task embeddings.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S177",
    "text": "We visu-alize these 400 embeddings in the 2D space by t-SNE [39] (see Fig. 12).",
    "location": "Section 6",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a deliberate action (visualization using t-SNE).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S178",
    "text": "Interestingly, we observe that nearby points in the task embedding space exhibit similar semantics.",
    "location": "Section 6",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This reports an observed property of the task embeddings.",
    "ambiguity_reason": "The 'similar semantics' is a property, but the 'observe' makes it an observable."
  },
  {
    "span_id": "S179",
    "text": "For example, the top-left corner in Fig. 12 shows two tasks related to coloring; the bottom-left corner shows two tasks related to generalized logic operations (i.e., AND/OR/XOR).",
    "location": "Section 6",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "These are specific examples of the observed semantic similarity.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S180",
    "text": "This vi-sualization suggests that our method attempts to learn the relations between different tasks, which is an essential abil-ity for abstraction and reasoning.",
    "location": "Section 6",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["observable"],
    "classification_reasoning": "This interprets the visualization, explaining 'how' the method learns and 'why' it's important for reasoning.",
    "ambiguity_reason": "It's an interpretation of an observable, explaining the underlying process and its importance."
  },
  {
    "span_id": "S181",
    "text": "During test-time training, we augment the single test task T into multiple auxiliary tasks.",
    "location": "Appendix A.2",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a deliberate action taken during TTT.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S182",
    "text": "We use a distinct task embedding for each auxiliary task, as not all of these augmentations correspond to the same underlying rule (e.g., consider \"gravity\" under a 90° rotation).",
    "location": "Appendix A.2",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["assumption"],
    "classification_reasoning": "This explains 'how' auxiliary tasks are handled and 'why' (because rules might change). The 'why' is a causal explanation.",
    "ambiguity_reason": "The 'not all augmentations correspond to the same underlying rule' could be an assumption, but it's used to justify the mechanism."
  },
  {
    "span_id": "S183",
    "text": "We apply 2 flippings (horizontal and vertical) or 3 rota-tions (in multiples of 90°), and 10 predefined color index permu-tations, resulting in (2+3)×10=50 auxiliary tasks with the orig-inal task.",
    "location": "Appendix A.2",
    "assigned_label": "context",
    "alternative_labels_considered": ["intervention"],
    "classification_reasoning": "This lists the specific types and number of augmentations, providing concrete details of the experimental setup.",
    "ambiguity_reason": "Could be an intervention as it's a manipulation, but it's more about the specific parameters of the setup rather than a controlled comparison."
  },
  {
    "span_id": "S184",
    "text": "We train for 100 epochs on these 51 tasks, covering 100 x 51 x 3 = 15.3k samples in total for test-time training for one test task T (assuming 3 raw samples in this task).",
    "location": "Appendix A.2",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This provides specific training parameters and data volume for TTT.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S185",
    "text": "in ARC, the raw input and output sizes are not always identical (e.g., see Fig. 3, Test Set, Task 1).",
    "location": "Appendix A.3",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a characteristic of the ARC problem that needs to be addressed.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S186",
    "text": "This issue can be addressed on the canvas in a unified frame-work.",
    "location": "Appendix A.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' the canvas solves the issue of varying input/output sizes.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S187",
    "text": "In our method, the input/output canvas always has a fixed size and is filled with a background token [BG].",
    "location": "Appendix A.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["context"],
    "classification_reasoning": "This describes a specific design choice for the canvas and its purpose ('how' it's structured).",
    "ambiguity_reason": "Could be context (a parameter), but it's part of the operational design to address the size variability."
  },
  {
    "span_id": "S188",
    "text": "when the raw output is placed on the canvas (serving as the ground truth during training), we always use an extra border token, [BD], to indicate the right and bottom edges.",
    "location": "Appendix A.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' the output shape is encoded on the canvas using a border token.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S189",
    "text": "Specifically, the token [BD] is filled along the one-pixel-wide edge on the right and bottom sides.",
    "location": "Appendix A.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This provides specific details on 'how' the border token is placed.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S190",
    "text": "During inference, we locate the rightmost and bottommost [BD] tokens and crop the output accordingly to recover the final predicted shape.",
    "location": "Appendix A.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' the final output shape is recovered during inference.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S191",
    "text": "Since the number of background pixels [BG] can dominate in some examples, we apply attention masks in the self-attention blocks to encourage the model to focus on the foreground pixels.",
    "location": "Appendix A.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'why' attention masks are used (BG dominance) and 'how' they work (encourage focus on foreground).",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S192",
    "text": "The attention masks are applied after the query-key dot-product computation, adding a large negative value to the keys correspond-ing to background inputs.",
    "location": "Appendix A.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This provides specific implementation details on 'how' attention masks are applied.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S193",
    "text": "The resulting softmax attention scores are therefore zero at those key positions.",
    "location": "Appendix A.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains the direct consequence ('how' the scores become zero) of applying attention masks.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S194",
    "text": "Moreover, during train-ing, the loss is computed only on locations where the inputs are not background pixels [BG].",
    "location": "Appendix A.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": [],
    "classification_reasoning": "This explains 'how' the loss computation is focused on foreground pixels.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S195",
    "text": "These designs encourage the model to pay more attention to foregrounds and therefore improve accuracy, although we note that even without them, our method still per-forms competitively, as observed in our preliminary experiments.",
    "location": "Appendix A.3",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["observable"],
    "classification_reasoning": "This explains 'why' these designs are beneficial (encourage attention, improve accuracy). The 'observed' part points to an observable, but the core is the causal explanation.",
    "ambiguity_reason": "Contains both a mechanism (causal effect) and a reference to an observable (preliminary experiments)."
  },
  {
    "span_id": "S196",
    "text": "Since we use the RE-ARC dataset [22] in our offline training, we can examine the effect of data scale provided by RE-ARC.",
    "location": "Appendix B.1",
    "assigned_label": "context",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes the dataset used and the purpose of the experiment.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S197",
    "text": "Using only the original ARC training data, without any RE-ARC data, our method achieves a decent accuracy of 31.5.",
    "location": "Appendix B.1",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "This is a specific, measurable performance result under a baseline condition.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S198",
    "text": "By adding 10, 100, and 1,000 pairs per task from RE-ARC, the accuracy increases to 38.6, 52.3, and 54.0, respectively.",
    "location": "Appendix B.1",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a deliberate manipulation (adding data) and its corresponding results.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S199",
    "text": "the accuracy increases to 38.6, 52.3, and 54.0, respectively.",
    "location": "Appendix B.1",
    "assigned_label": "observable",
    "alternative_labels_considered": [],
    "classification_reasoning": "These are specific, measurable performance results.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S200",
    "text": "This com-parison suggests that increasing the amount of offline training data is beneficial, although the returns diminish beyond a certain point.",
    "location": "Appendix B.1",
    "assigned_label": "mechanism",
    "alternative_labels_considered": ["observable"],
    "classification_reasoning": "This interprets the observed trend, explaining 'why' increasing data is beneficial and noting a diminishing return.",
    "ambiguity_reason": "It's an interpretation of an observable, explaining the underlying principle."
  },
  {
    "span_id": "S201",
    "text": "we also exam-ine the scalability of the offline training task diversity.",
    "location": "Appendix B.1",
    "assigned_label": "intervention",
    "alternative_labels_considered": [],
    "classification_reasoning": "This describes a deliberate action (examining scalability) for an experiment.",
    "ambiguity_reason": "none"
  },
  {
    "span_id": "S202",
    "text": "When trained on 0, 16, 80, and 400 tasks, the accuracy increases from 26.4 to 43.1, 49.6, and 54.5 respectively, suggesting that the diversity of training tasks is helpful for generalization.",
    "location": "Appendix B.1",
    "assigned_label": "observable",
    "alternative_labels_considered": ["mechanism"],
    "classification_reasoning": "This reports specific performance results across different conditions. The 'suggesting' part is an interpretation, which is a mechanism.",
    "ambiguity_reason": "Contains an observable (accuracy) and a mechanism (diversity helpful for generalization)."
  },
  {
    "span_