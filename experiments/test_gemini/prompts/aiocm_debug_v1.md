Attached is a scientific paper PDF.

paper_id: {paper_id}
paper_title_hint: {paper_title_hint}

Please perform an AIO-CM extraction debug pass.

Goal:
I want to see HOW A/I/O/M/C candidates are extracted and classified.
Do not output a final database schema.
Do not output a polished paper summary.
Show the classification criteria and ambiguous cases.

Please produce the following sections.

# 1. Operational one-paragraph summary
Summarize only what is needed for AIO-CM extraction:
- What phenomenon or result is the paper trying to explain?
- What experiments or ablations are most relevant?
- What mechanisms seem to be proposed or tested?

# 2. Evidence-first candidate spans
List 10-20 important source spans from the paper.
For each span, include:
- location: section/page/table/figure if available
- short evidence snippet
- why this span matters for AIO-CM extraction
- possible labels among M, A, C, I, O
Do not decide too quickly. Multi-label is allowed here.

# 3. AIO-CM candidate table
Create a table with columns:
- candidate_id
- proposed_label: M / A_substantive / A_confound_control / C / I / O
- text
- evidence_location
- source_type: extracted / author_inferred / compiler_inferred / missing
- classification_rationale
- alternative_label_considered
- ambiguity_level: low / medium / high

Important classification rules:
- Model names and method names are usually C, not M.
- Mechanisms must be abstract explanations.
- If the paper reports that a condition was set, it is C.
- If the interpretation relies on the condition successfully isolating the effect, that is A_confound_control.
- If something changes between experimental arms, it is I.
- O must be split into eval_metric and pattern.
- Raw numbers are evidence, not the O itself.

# 4. Draft experiment units, without final schema
Construct 3-7 tentative AIO-CM units.

For each unit, write in this loose format:

Unit Ux:
- What is being tested?
- M: abstract mechanism(s)
- A_substantive: substantive assumptions
- A_confound_control: control/isolation assumptions
- C: context/system/domain/benchmark/compute/evaluation setting
- I: intervention/comparison/sweep, including reference arm
- O_observed:
    eval_metric:
    pattern:
    raw evidence:
- O_expected:
    source: extracted / author_inferred / compiler_inferred
    if M holds:
    if competing M holds:
- Diagnostic implication:
    what would be strengthened?
    what would be weakened?
    what would become void if a confound-control assumption fails?
- Ambiguity:
    what is uncertain or under-specified?

# 5. What NOT to extract
List things that look tempting but should NOT become AIO-CM nodes.
Examples:
- method names mistaken as mechanisms
- raw numbers mistaken as observables
- broad claims without intervention
- conclusions without measurable signatures

# 6. Human questions
List 5-10 questions a human annotator should answer before turning this into a formal schema.
Focus on:
- A vs C ambiguity
- M vs method-name ambiguity
- whether compute/control was actually isolated
- whether expected observables are extracted or inferred
- missing ablations/tests

Remember:
This is an extraction-debug memo, not a final database.
