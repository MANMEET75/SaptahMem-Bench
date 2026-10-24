# SaptahMem-Bench

**A benchmark and study protocol for short-horizon conversational memory in assistants.**

> **Status: protocol and development fixture (v0.2.0-prep).** This repository contains a prospective human-study protocol, annotation and privacy workflows, validation/scoring utilities, and two fictional examples for loader checks. No participant study has been run, no participant conversations are included, and there is no validated test set, leaderboard, or model-performance claim. The fixture is not suitable for system comparisons.

SaptahMem-Bench evaluates whether an assistant can preserve, update, retrieve, combine, and appropriately decline to answer facts across a bounded **seven-day conversational window**. The focus is short-term episodic memory: information that should remain available over several days but may later expire or be superseded.

The name combines *saptah* (Hindi for “week”) with memory. A web search on 25 October 2026 did not surface an exact benchmark name match; this is a practical naming check, not a legal, trademark, domain, or permanent uniqueness guarantee.

## Why a short-horizon benchmark?

Long-horizon suites such as BEAM and LoCoMo probe retention over very long histories. Real assistants also need to manage near-term commitments and changing details: a meeting time revised on Thursday, a shopping list that changes tomorrow, or a preference stated only for the current task. A system can be strong on long-history retrieval and still fail at freshness, recency, decay, and short-lived intent.

SaptahMem-Bench is designed to isolate those behaviors in a controlled seven-day window. It evaluates the complete memory path—what gets stored, updated, retrieved, and used in an answer—while recording enough evidence to separate memory failures from answer-generation failures.

## Benchmark at a glance

| Property | Specification |
|---|---|
| Primary horizon | 7 consecutive 24-hour periods (168 hours) |
| Interaction | Multi-session user–assistant conversations, timestamped in UTC |
| Core task | Answer questions using only information available before the query cutoff |
| Unit | One participant's seven-day conversation episode, chronological messages, query cutoffs, questions, gold answers, evidence, and scoring rubric |
| Intended systems | Memory-augmented assistants, full-history baselines, rolling-window baselines, summaries, retrieval systems, and no-memory controls |
| Planned study | 50-episode pilot followed by 1,000 main episodes (200 public dev, 800 hidden test); power analysis may expand the main release in fixed 100-episode blocks up to 1,500 total |
| Planned questions | 16 per main episode (12 answerable, 4 unanswerable or ambiguous target); approximately 16,000 total |
| Languages | English first; multilingual extensions only after language-specific review |
| Current release | Study/evaluation protocol plus two fictional dev fixture episodes; not an official scoreable test set |
| Repositories | [GitHub source](https://github.com/MANMEET75/SaptahMem-Bench) · [Hugging Face dataset](https://huggingface.co/datasets/MANMEET75/SaptahMem-Bench) |

## What it measures

The proposed question set uses a balanced taxonomy. Categories are multi-label where appropriate, but each question has one primary category for reporting.

1. **Recent episodic recall** — recover a detail from an earlier day after intervening conversation.
2. **Cross-session binding** — combine compatible facts introduced in separate sessions (for example, destination + date + constraint).
3. **Temporal ordering and recency** — identify which event or value is current at the query cutoff.
4. **State update and correction** — prefer an explicit correction over an obsolete value; preserve history when asked about the earlier value.
5. **Ephemeral intent and commitment** — remember near-term plans, deadlines, reminders, and task-specific intent without treating them as permanent profile facts.
6. **Preference scope and decay** — distinguish stable preferences from one-task or one-week preferences; do not overgeneralize a temporary request.
7. **Entity and speaker binding** — associate facts with the right person, object, project, or speaker.
8. **Distraction resistance** — ignore plausible but irrelevant neighboring facts and repeated topic noise.
9. **Unanswerable detection / abstention** — say the available evidence is insufficient rather than inventing a detail.
10. **Window boundary and expiry** — test facts just inside and outside the declared retention window in dedicated boundary probes. These probes must never silently change the primary seven-day task definition.

A strong benchmark contains answerable, ambiguous, contradicted, and genuinely unanswerable questions. It must not reward confident guessing.

## Proposed protocol

### 1. Episode timeline

- Each episode begins at `t0` and runs for exactly 168 hours. Use timezone-aware ISO-8601 UTC timestamps.
- Divide the timeline into seven 24-hour bins (`D0`…`D6`) measured from `t0`, not from local midnight. This avoids daylight-saving ambiguity.
- Preserve natural variation in session count, active days, session gaps, message volume, and question delays. Do not script facts or add turns to meet a quota; report observed distributions and retain sparse valid episodes.
- Questions are issued at explicit cutoffs within the episode. A system may only use messages with timestamps earlier than that cutoff. Future messages and gold annotations are inaccessible to the evaluated system.
- The primary test cutoff occurs before or at the 168-hour boundary. A separate boundary track may ask questions after expiry and must define the permitted memory state explicitly.
- Messages are chronologically ordered and uniquely identified. The dataset's `source_message_ids` are for evaluator/scorer use and are never shown to the answering system.

### 2. System interface

Every system must implement two conceptual operations, regardless of its internal architecture:

1. `observe(message)`: process each message once, in chronological order, without seeing future dialogue or labels.
2. `answer(question, cutoff)`: return one answer (or a declared abstention) using only the state and messages permitted by the selected track.

A benchmark adapter must record the final answer, citations/evidence if supported, input/output tokens, latency, and any external calls. The benchmark does not prescribe an internal memory representation. For the retrieval-only track, submit retrieved message IDs or spans before answer generation.

### 3. Tracks and baselines

Report results separately; do not collapse these tracks into a single ranking:

- **Memory-only (primary):** system ingests messages incrementally and answers from its own memory; raw history is not supplied at query time.
- **Memory + bounded transcript:** memory may retrieve from a declared rolling transcript buffer; report buffer size and memory budget.
- **Full-history upper bound:** all messages before cutoff are available at query time. This is a context baseline, not evidence of an external memory mechanism.
- **Recent-window baseline:** only the last N messages or a declared number of hours are available.
- **No-memory baseline:** query-only answer, useful for detecting dataset leakage and answer priors.
- **Oracle evidence diagnostic:** gold evidence is supplied. This is not a leaderboard score; it estimates answerer capability independent of memory retrieval.

For fair comparison, disclose model/provider and exact version, prompts, decoding parameters, memory write/read settings, token limits, context window, retries, tools, costs, and code revision. No system may access test labels, future turns, hidden metadata, or external web sources for benchmark answers.

### 4. Question construction and evidence

Each question has one canonical answer or an explicitly defined acceptable-answer set, an answerability label, one primary skill, difficulty, query timestamp, source evidence, and a scoring rubric. Evidence should be minimal but sufficient. Multi-hop questions cite every required message. Contradiction questions identify both the superseded and current evidence. Questions should be natural, varied in phrasing, and not copy the wording of the source turn verbatim in a way that makes retrieval trivial.

The planned source is natural conversation from consenting participants using the study assistant for self-chosen, ordinary needs. Domains may include scheduling, errands, learning, hobbies, travel, household coordination, work tasks, and event preparation. Do not prompt participants to produce distractors or benchmark facts. Annotators may select naturally occurring distractions and updates; if a category is absent, report that instead of inventing dialogue. Exclude high-stakes advice and remove sensitive or identifying incidental details before public release.

### 5. Planned prospective study

The target v1 data source is prospective, consented use of an instrumented study assistant for ordinary, self-chosen needs over seven days. Participants are not given scripted fact-sharing tasks and are not told the question templates. Freeze the assistant version and disable persistent cross-session memory during collection so each participant experiences the same collection system. Collect only the minimum text and timestamps needed for replay; do not collect audio, location, contacts, or tool/web histories. Participant-facing materials, ethics review, consent, withdrawal, retention, and incident procedures are specified in `docs/STUDY_PROTOCOL.md`. `docs/CONSENT_TEMPLATE.md` is an unapproved drafting aid and requires local ethics/privacy/legal review and completion before recruitment.

Recruit 50 pilot participants/episodes, excluded from the main score. After pilot-based power analysis, target 1,000 main episodes from 1,000 participants: 200 consented, de-identified public development episodes and 800 hidden test episodes held for controlled evaluation. If the pre-registered precision/power target is not met, add 100-episode blocks to the main release up to 1,500 total (holding the 200-episode public dev target constant and expanding hidden test). Public release requires explicit publication consent, privacy review, and successful redaction/re-identification checks; episodes that fail are excluded from public distribution. The study is English-first. Do not infer the 1,000-episode target is powered for a particular effect until the pilot variance and within-episode correlation have been measured.

Annotate 16 questions per main episode as a target, normally 12 answerable and 4 unanswerable/ambiguous, without forcing unnatural category coverage. Ensure all ten categories appear in the release and report actual counts. Every test episode receives independent second review; adjudicate and preserve a non-identifying audit trail. Freeze split assignments, questions, labels, evaluator, and checksums before comparative evaluation. Read `docs/ANNOTATION_GUIDE.md` and `docs/EVALUATION_PROTOCOL.md` for operational instructions.

### 6. Scoring

Publish every metric overall and by primary category, difficulty, answerability, and episode. Report counts and confidence intervals. Recommended metrics:

- **Exact Match (EM):** normalized exact answer match for deterministic, constrained answers.
- **Semantic answer accuracy:** blinded rubric scoring for valid paraphrases and compositional answers. Publish judge model/version, prompt, raw labels, and adjudication policy. Human scoring is the reference for a stratified audit sample.
- **Evidence precision/recall/F1:** compare cited message IDs or spans with gold evidence. Report this only when systems return evidence; a correct answer without citations should not be silently scored as grounded.
- **Abstention precision, recall, and F1:** for unanswerable or explicitly ambiguous questions; separately count false assertions.
- **Temporal/state accuracy:** accuracy on current-value versus historical-value questions.
- **Calibration:** Brier score or expected calibration error only if confidence is required and consistently collected.
- **Efficiency:** median and p95 latency, tokens stored/read/generated, memory footprint, and cost per 100 questions. State provider pricing date and calculation method.
- **Failure breakdown:** stale value, forgotten fact, wrong entity, unsupported inference, false abstention, missed abstention, and evidence mismatch.

Primary score (planned): macro-average per-question accuracy across the ten categories, with answerable and unanswerable/ambiguous items separately reported. A validated semantic rubric score is reported alongside deterministic exact match; the included scorer computes exact/acceptable-answer matches and abstention outcomes, not semantic equivalence. Also show micro accuracy and the complete per-category table. Comparative claims require a frozen human-reviewed test set and pre-registered episode-clustered paired uncertainty intervals.

## Data design and quality control

### Target composition (planned)

- Pilot: 50 prospective episodes, used only to debug recruitment, privacy, annotation, schema, scoring, and power estimates.
- Main release target: 200 public dev + 800 hidden test episodes (1,000 total); add hidden episodes in blocks of 100 to a maximum of 1,500 if the preregistered power/precision target is unmet.
- 16 questions per main episode (target 12 answerable and 4 unanswerable/ambiguous); actual category and answerability counts are published.
- Collect natural use rather than assigning benchmark scenarios; sample and report conversation volume, session gaps, active days, and domains. Do not discard sparse but valid episodes merely to meet category quotas.
- Keep pilot, dev, and hidden test participants disjoint. Split by participant and any scenario/question authoring family, not by question rows.

### Creation workflow

1. Collect and freeze consented prospective conversations under the approved study protocol; separate identity linkage from transcript data.
2. Redact identifiers and sensitive incidental details; obtain independent contextual privacy and public-release review before annotation/release.
3. Write questions from the recorded conversations without altering dialogue; annotate cutoff, answerability, accepted answers, minimal evidence, skill, and rubric.
4. Verify every question using only its visible prefix; have a second reviewer check every hidden-test episode and adjudicate disagreements.
5. Run schema, chronology, cutoff/evidence, duplicate, answer-in-question, and split-leakage checks; manually inspect semantic/template overlap.
6. Run baseline diagnostics for question-only leakage, recency shortcuts, floor/ceiling, and oracle answerability.
7. Freeze participant-level splits, labels, evaluator, privacy decisions, license, and checksums; publish the release card and change log.

### Data and privacy policy

Use fictional or consented data only. Never publish scraped private conversations, credentials, contact information, precise home/work addresses, or sensitive personal data. Synthetic examples must be identified as synthetic. Human-created data needs informed consent, clear compensation terms, withdrawal handling before release, and a license compatible with the intended distribution. The dataset card must disclose generation tools and human review. Do not claim synthetic data represents real-world prevalence.

## Files and format

- `data/dev/episodes.jsonl` — small, illustrative development fixture.
- `schemas/episode.schema.json` — JSON Schema for an episode record.
- `docs/BENCHMARK_PLAN.md` — implementation phases, governance, and release gates.
- `docs/DATA_CARD.md` — data statement template and required disclosures.
- `docs/STUDY_PROTOCOL.md` — prospective collection, privacy, withdrawal, and release workflow.
- `docs/CONSENT_TEMPLATE.md` — participant information and separate participation/publication choices (draft only; approval required).
- `docs/ANNOTATION_GUIDE.md` — blinded prefix-only authoring and review instructions.
- `docs/EVALUATION_PROTOCOL.md` — prediction interface, baselines, scoring, and reporting.
- `scripts/` — standard-library dataset validation, leakage checks, and deterministic scoring tools.
- Hugging Face dataset card — copy of the task and dataset documentation for discovery and loading.

The proposed JSONL schema contains `episode_id`, `split`, `start_time`, `duration_hours`, `scenario_domain`, `messages`, and `questions`. See the schema and examples. Use UTF-8, one complete JSON object per line, stable IDs, and no trailing comments.

## Local tooling

The preparation tools use only Python's standard library (Python 3.7+). From the repository root:

```bash
python scripts/validate_dataset.py data/dev/episodes.jsonl
python scripts/audit_leakage.py data/dev/episodes.jsonl
python -m unittest discover -s tests -v
python scripts/score_predictions.py --gold data/dev/episodes.jsonl --predictions predictions.jsonl
```

Prediction JSONL format and scorer limitations are documented in `docs/EVALUATION_PROTOCOL.md`. Use only public dev labels locally; do not place hidden test labels or participant data in Git or Hugging Face. The leakage scanner reports hashes and IDs, not matched text, and only detects exact normalized reuse; a clean scan is not proof of split independence.

## Reproducible reporting checklist

A result report must include:

- Benchmark release and split hash; code commit and evaluation timestamp.
- System architecture track and whether raw transcript retrieval is permitted.
- Answering and judging model identifiers, versions, prompts, and settings.
- Memory configuration, write/read limits, transcript buffer, and retrieval settings.
- Number of episodes/questions attempted; exclusions and failures.
- Overall, category, answerability, and difficulty scores with denominators.
- Abstention and grounding metrics, including missing citations.
- Tokens, latency, cost, and number of runs; publish per-item outputs where licensing permits.
- Any post-processing, retries, manual edits, or dropped items.

## Limitations

A seven-day window is one useful operational definition, not a universal boundary for short-term memory. The present fixture is fictional and cannot establish real-world behavior. A future prospective study may still reflect participation effects, assistant-specific interaction patterns, English-first recruitment, and privacy-related public-release exclusions. LLM judges can be inconsistent, so calibrate against human labels before leaderboard use. A memory score also reflects the answering model, prompts, and context budget. SaptahMem-Bench should complement long-term evaluations, not replace them.

## Roadmap

1. **Protocol preparation (this release):** publish study and annotation protocols, evaluator scripts, schema, and fictional fixture. No participant data or claims.
2. **Pilot:** recruit and review 50 consented episodes; estimate annotation reliability, natural category coverage, collection burden, and statistical power; revise and preregister.
3. **Public development release:** collect, review, and publish up to 200 permitted, de-identified dev episodes with evaluator and baseline outputs.
4. **Decision-grade v1:** freeze 800 or power-adjusted hidden test episodes, run paired evaluation, publish audit and confidence intervals, licenses, checksums, and controlled-submission procedure.
5. **Extensions:** multilingual tracks, multimodal short-term memory, personalized retention/forgetting, and interactive follow-up tasks—each as a separately reported track.

## Citation

No paper or official benchmark release exists yet. Until one is published, cite the repository release and commit hash. Do not cite the development fixture as a validated benchmark.

## License

The blueprint, tools, and hand-authored fixture are released under the MIT License. This does not pre-license future participant data. A future dataset may require separate terms; check the release-specific card and rights/consent review.

## References

- BEAM: [Beyond a Million Tokens: Benchmarking and Enhancing Long-Term Memory in LLMs](https://arxiv.org/abs/2510.27246) (ICLR 2026).
- LoCoMo: [Evaluating Very Long-Term Conversational Memory of LLM Agents](https://github.com/snap-research/locomo), ACL 2024.
- LongMemEval: [LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://github.com/xiaowu0162/LongMemEval), ICLR 2025.

If a reference URL or publication detail changes, update it before the v1.0 paper; citations above are orientation links, not a claim that SaptahMem-Bench is affiliated with those projects.
