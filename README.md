# SaptahMem-Bench

**A benchmark blueprint for short-horizon conversational memory in assistants.**

> **Status: proposal and development fixture (v0.1.0).** This repository defines a reproducible benchmark design and includes a tiny, hand-authored example for validating data loaders. It is not a completed, human-validated benchmark release, has no leaderboard, and makes no model-performance claims. The example is not suitable for drawing conclusions about system quality.

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
| Unit | One episode: a scenario, chronological messages, query cutoffs, questions, gold answers, evidence, and scoring rubric |
| Intended systems | Memory-augmented assistants, full-history baselines, rolling-window baselines, summaries, retrieval systems, and no-memory controls |
| Proposed initial test scale | 300 scenario episodes × 12 questions = 3,600 questions; separate dev and hidden test sets; final counts depend on annotation and pilot quality |
| Languages | English first; multilingual extensions only after language-specific review |
| Current release | Blueprint plus two illustrative dev episodes; not an official scoreable test set |

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
- Include at least four distinct conversation sessions on at least four bins. Session gaps, session lengths, and question delays should vary.
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

The source messages should contain diverse but non-sensitive, fictional everyday scenarios: scheduling, errands, learning, hobby projects, travel planning, household coordination, work tasks, event preparation, and health-adjacent logistics without diagnoses or private real-person data. Each episode should include meaningful distractor dialogue and plausible distractor facts. Avoid demographic stereotypes, unsafe advice, and excessive reliance on named entities or one cultural context.

### 5. Scoring

Publish every metric overall and by primary category, difficulty, answerability, and episode. Report counts and confidence intervals. Recommended metrics:

- **Exact Match (EM):** normalized exact answer match for deterministic, constrained answers.
- **Semantic answer accuracy:** blinded rubric scoring for valid paraphrases and compositional answers. Publish judge model/version, prompt, raw labels, and adjudication policy. Human scoring is the reference for a stratified audit sample.
- **Evidence precision/recall/F1:** compare cited message IDs or spans with gold evidence. Report this only when systems return evidence; a correct answer without citations should not be silently scored as grounded.
- **Abstention precision, recall, and F1:** for unanswerable or explicitly ambiguous questions; separately count false assertions.
- **Temporal/state accuracy:** accuracy on current-value versus historical-value questions.
- **Calibration:** Brier score or expected calibration error only if confidence is required and consistently collected.
- **Efficiency:** median and p95 latency, tokens stored/read/generated, memory footprint, and cost per 100 questions. State provider pricing date and calculation method.
- **Failure breakdown:** stale value, forgotten fact, wrong entity, unsupported inference, false abstention, missed abstention, and evidence mismatch.

Primary score (proposed): macro-average semantic answer accuracy over the ten categories, with answerable and unanswerable items reported as separate strata. Also show micro accuracy and the complete per-category table. Do not publish a leaderboard score until human-reviewed data and a fixed evaluator are released.

## Data design and quality control

### Target composition (proposal)

- Pilot: 30 episodes, used only to debug instructions, schema, and scoring.
- Public development: 60 episodes, with public labels and evidence.
- Hidden test: 300 episodes, generated from disjoint scenario plans and held-out templates; labels remain private for an evaluation service or are released after a benchmark version is retired.
- 12 questions per episode (target 3,600 test questions), balanced by skill where applicable. The pilot may use fewer.
- At least 25% unanswerable/ambiguous questions and at least 25% update/recency questions in the final test set; enforce exact proportions only after piloting shows natural coverage.
- Split by scenario plan, entity inventory, and template family, not by question rows, to reduce leakage.

### Creation workflow

1. Write a scenario plan with seven-day timeline, key facts, updates, temporary vs stable facts, distractors, and intended question coverage.
2. Generate or author conversation drafts from the plan, with multiple sessions and natural intervening turns.
3. Create questions from the plan and annotate gold answers, answerability, minimal evidence, category, and rubric.
4. Run automated schema, chronology, evidence-reference, split-leakage, duplicate, and answer-in-history checks.
5. Have an annotator who did not write the episode answer each question from the visible prefix only; reject or repair any item whose evidence is absent or ambiguous.
6. Independently review a stratified sample; adjudicate disagreements and record changes.
7. Red-team for shortcuts: lexical overlap, answer leakage in IDs/metadata, question-only solvability, future leakage, duplicate templates, and common-sense guessing.
8. Version the dataset, publish a data statement, document licenses and synthetic/human contributions, and retain a change log.

### Data and privacy policy

Use fictional or consented data only. Never publish scraped private conversations, credentials, contact information, precise home/work addresses, or sensitive personal data. Synthetic examples must be identified as synthetic. Human-created data needs informed consent, clear compensation terms, withdrawal handling before release, and a license compatible with the intended distribution. The dataset card must disclose generation tools and human review. Do not claim synthetic data represents real-world prevalence.

## Files and format

- `data/dev/episodes.jsonl` — small, illustrative development fixture.
- `schemas/episode.schema.json` — JSON Schema for an episode record.
- `docs/BENCHMARK_PLAN.md` — implementation phases, governance, and release gates.
- `docs/DATA_CARD.md` — data statement template and required disclosures.
- Hugging Face dataset card — copy of the task and dataset documentation for discovery and loading.

The proposed JSONL schema contains `episode_id`, `split`, `start_time`, `duration_hours`, `scenario_domain`, `messages`, and `questions`. See the schema and examples. Use UTF-8, one complete JSON object per line, stable IDs, and no trailing comments.

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

A seven-day window is one useful operational definition, not a universal boundary for short-term memory. Fictional, plan-driven dialogue may not capture the full ambiguity, language variation, emotional context, or sparsity of real conversations. LLM judges can be inconsistent, and the proposed benchmark needs human validation and judge calibration before leaderboard use. A memory score also reflects the answering model, prompts, and context budget. SaptahMem-Bench should complement long-term evaluations, not replace them.

## Roadmap

1. **Blueprint v0.1 (this release):** publish protocol, schema, and development fixture.
2. **Pilot v0.2:** author 30 episodes; run annotator agreement and baseline sanity checks; revise taxonomy and rubrics.
3. **Public dev v0.5:** publish 60 reviewed episodes, evaluator harness, adapters, and baseline outputs.
4. **Benchmark v1.0:** release frozen hidden test, evaluator protocol, human audit, benchmark paper, licenses, and leaderboard submission process.
5. **Extensions:** multilingual tracks, multimodal short-term memory, personalized retention/forgetting, and interactive follow-up tasks—each as a separately reported track.

## Citation

No paper or official benchmark release exists yet. Until one is published, cite the repository release and commit hash. Do not cite the development fixture as a validated benchmark.

## License

The blueprint and hand-authored fixture are released under the MIT License. Future datasets may require a separate license and dataset card; check the release-specific terms.

## References

- BEAM: [Benchmarking Long-Horizon Conversational Memory](https://github.com/VectorInstitute/BEAM) (verify the canonical project URL and paper citation when preparing a formal comparison).
- LoCoMo: [Evaluating Very Long-Term Conversational Memory of LLM Agents](https://github.com/snap-research/locomo), ACL 2024.
- LongMemEval: [LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://github.com/xiaowu0162/LongMemEval), ICLR 2025.

If a reference URL or publication detail changes, update it before the v1.0 paper; citations above are orientation links, not a claim that SaptahMem-Bench is affiliated with those projects.
