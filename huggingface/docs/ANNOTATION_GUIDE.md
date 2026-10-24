# Annotation Guide

## Purpose and separation of roles

Create natural questions that test what a system could know at a timestamp in a seven-day conversation. Annotators must receive only the materials needed for their role. A prefix-only answering annotator must never see later messages, author plans, gold evidence, or the intended answer. Keep the private authoring/participant link file outside the benchmark repository and delete it according to the approved study retention plan.

For every hidden-test episode, assign (1) a question author, (2) an independent prefix-only verifier, and (3) a second reviewer who inspects all questions and evidence. The second reviewer must not be the author. Adjudicate disagreements and preserve decisions in a non-identifying audit log. Pilot and dev records use the same process; report actual coverage.

## Episode preparation

1. Confirm the record is consented for its intended split and has passed privacy review before annotation.
2. Redact direct identifiers and sensitive incidental content. Preserve stable within-episode aliases only when needed to distinguish entities. Do not invent facts during redaction.
3. Convert timestamps to UTC, verify chronological order and session boundaries, and assign random non-semantic episode/message IDs. Keep participant IDs out of all public artifacts.
4. Record broad non-sensitive domain and language only. Do not infer or label personality, health status, protected traits, or demographic information from dialogue.

## Question writing

Target 16 questions per main episode, normally 12 answerable and 4 unanswerable/ambiguous. Treat these as sampling targets, not quotas that justify unnatural questions. Sample query cutoffs across the week, including short and long delays after evidence, updates, and near-boundary moments. Across the release, include all ten primary skill categories and report the actual counts. Avoid multiple questions that test the same single fact unless they deliberately distinguish current from historical state.

Write questions in varied, natural language that does not copy distinctive source wording. Do not include an answer in the question, IDs, filenames, metadata, or rubric. Avoid cues that make a question-only model succeed. Include distractors and competing entities only when the visible dialogue supports an unambiguous intended distinction. Do not ask high-stakes advice questions.

For each question, annotate:

- `question_id`, exact `query_time` (UTC), and question text.
- `answerability`: `answerable`, `unanswerable`, or `ambiguous` using only the prefix strictly before the cutoff.
- `gold_answer`: concise canonical answer for answerable items; null for the other labels.
- `acceptable_answers`: a short list of equivalent concise variants; never include unsupported guesses.
- `source_message_ids`: minimal sufficient evidence. For unanswerable items, use an empty list. For ambiguous items, cite the messages that create unresolved ambiguity.
- `primary_category`, any justified secondary categories, `difficulty`, and a rubric specifying required content and common errors.

For update questions, cite both the superseded and current evidence when the query asks for current state. If asked for historical state, cite the earlier value. For multi-hop questions, cite every fact needed. Evidence messages must occur before `query_time`. An assistant message that merely repeats a user fact may support retrieval, but prefer the original user statement and the correction when those are the actual provenance.

## Prefix-only verification

The verifier receives only the transcript prefix and question, with no answer, category, author notes, or future messages. They independently answer or mark the item unanswerable/ambiguous and list evidence IDs. The question is retained only if the verifier can recover the intended answer and evidence, or correctly identifies the intended uncertainty from that prefix. Revise or remove items that depend on future turns, unstated world knowledge, a writer's intent, or private information.

## Review and adjudication

The second reviewer checks all hidden-test items and a stratified sample of dev items. Check evidence sufficiency, cutoff correctness, answer variants, category, privacy, naturalness, ambiguity, and answer leakage. Disagreements are adjudicated by a named lead annotator. Log anonymized item ID, issue type, decision, and rubric change; do not expose participant data in public issue trackers. Report raw agreement and a chance-corrected statistic for answerability and evidence sufficiency, with denominator and confidence interval. Never report an agreement value without explaining the unit and label scheme.

## Rejection and repair rules

Reject or rewrite a question if: evidence is absent or after the cutoff; multiple answers are equally valid but the item is labeled answerable; the question paraphrases a unique phrase too closely; the answer can be guessed from the question alone; a redaction made the evidence unclear; it requires external facts; it tests a sensitive inference; or its rubric cannot distinguish a correct answer from a stale, wrong-entity, or unsupported answer. Repair by changing the item or transcript only with an auditable, consent-compatible correction; never silently edit a public scored release.
