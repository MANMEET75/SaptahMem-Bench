# Evaluation Protocol and Prediction Interface

## Release status

The scripts and instructions here are preparation tools. Current fixture results are not benchmark scores. Do not run official hidden-test evaluations until a consented, reviewed, frozen test release and controlled submission service exist.

## Replay contract

For every episode, the adapter presents messages exactly once, in timestamp order, through `observe(message)`. At a question cutoff, present only the question and the system's allowed memory state through `answer(question, cutoff)`. A message is available only if `timestamp < query_time`; equality is excluded. The adapter must not expose `source_message_ids`, gold answers, acceptable answers, rubrics, hidden metadata, or future turns. All tracks use the same cutoff rule. Each question is answered once per run; disclose retries and use a fixed policy.

Primary track: the evaluated system receives no raw transcript at query time, only the state it created while observing the stream. Secondary tracks must be labeled and reported separately: declared bounded transcript, fixed recent window, full permitted prefix, query-only no-memory, and gold-evidence answerer. Full-history and oracle are diagnostics, not memory scores.

## Prediction JSONL

One JSON object per question, UTF-8, with these required fields:

```json
{"episode_id":"dev_trip_planning_001","question_id":"q01","answer":"By the 10:30 flight.","abstained":false,"evidence_message_ids":["m05"]}
```

`episode_id` and `question_id` must identify one gold item. `answer` is a string (use an empty string when abstaining). `abstained` is a Boolean. `evidence_message_ids` is an optional array of cited message IDs; it is not proof of a valid explanation by itself. Do not submit confidence unless a separately versioned calibration track requests it. Missing, duplicate, extra, malformed, or non-finite outputs are errors and must be reported; the evaluator never silently drops a failed question.

The public fixture is the only available gold data today. A hidden test service must accept the same prediction interface but keep gold records and detailed labels private. Submission service logs must bind predictions to a system description, code revision, prompt/configuration hash, model/version, track, run ID, and timestamp.

## Scoring

`scripts/score_predictions.py` computes deterministic exact/acceptable-answer match, correct abstention, per-question outcomes, per-episode-cluster bootstrap intervals, and category/answerability summaries. Text normalization applies Unicode NFKC, case folding, whitespace collapse, and edge punctuation trimming; it does not remove negation, dates, units, or entity distinctions. This score is an exact-match diagnostic and does not judge semantic paraphrases.

The planned primary comparison is macro-average accuracy across the ten primary categories, with category scores and answerability strata shown individually. Report micro per-question accuracy too. An item is correct if an answerable item matches an accepted answer and is not abstained on, or if an unanswerable/ambiguous item is explicitly abstained on. Ambiguous labels count as abstention-required in this deterministic metric; publish a separate sensitivity analysis if a future rubric defines another treatment. False assertions on unanswerable items and false abstentions on answerable items are always broken out.

For semantic accuracy, use the item rubric and a fixed judge only after calibrating it against blinded human labels. Freeze judge provider/model/version, prompt, decoding, and adjudication before test scoring. Human-audit a stratified sample and every disagreement class; publish judge-human agreement and confusion. Do not let an LLM judge see system identity. Evidence precision/recall/F1 is computed only when systems return evidence; disclose uncited answers separately. Efficiency uses median/p95 latency, stored/read/generated tokens, memory footprint, tool calls, and cost per 100 questions with price date and accounting method.

Use paired comparisons on identical episodes and question IDs. Resample whole episodes (not individual questions) for 95% confidence intervals and paired score differences; fix the random seed and number of bootstrap replicates in the release. Report denominators for every slice. Do not claim significance from overlapping/non-overlapping intervals alone; report the paired difference interval. Pre-register the primary comparison and 3 percentage-point target effect at two-sided alpha 0.05; use pilot data to calculate required hidden-test size for 80% power. Add hidden episodes in 100-episode blocks, keeping the 200-episode dev target fixed, up to 1,500 main episodes total (1,300 hidden) only under the predeclared rule; state detectable effect and power if capped.

## Required comparison baselines

Run all baselines on the same frozen episodes, answer model, decoding settings, and query cutoffs wherever applicable. When that is impossible, label the confound and avoid causal claims.

1. **No-memory:** question only; always-abstain is also a sanity check.
2. **Recent-window:** last 10 messages and a token-matched last-message window; disclose exact limits.
3. **Rolling summary:** update one summary after every session with a fixed token budget and no future messages.
4. **Raw retrieval:** retrieve from all observed messages using a fixed embedding/index and top-k/token limit.
5. **Structured facts:** extract subject, predicate, value, time, scope, and supersession state using a frozen extractor; retain provenance.
6. **Full-prefix:** all messages before cutoff at answer time; context upper bound only.
7. **Gold-evidence:** only cited gold evidence to the same answer model; answer-generation diagnostic only.

Publish prompts/configuration and executable baseline adapters when the required model and licensing terms permit. Do not imply a baseline ran if only its recipe is documented.

## Reporting template

Every report includes release/version and test checksum; code and evaluator revisions; system track; model/provider version; prompts/configuration hash; memory write/read policy and limits; transcript buffer; decoding, retries, tools, and external calls; submitted/completed counts and failures; all overall/category/answerability/difficulty metrics with denominators and paired episode-clustered intervals; evidence and abstention outcomes; latency/tokens/memory/cost; human/judge calibration; exclusions; and any manual intervention. Publish per-item predictions on public dev where permitted. Hidden-test per-item outputs are returned only as allowed by the service policy and must not reveal gold labels or enable direct item-level test tuning.
