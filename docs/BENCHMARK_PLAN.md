# Benchmark Plan and Release Gates

## Objective

Create a reproducible, independently reviewable evaluation of short-horizon conversational memory over seven consecutive 24-hour periods. The benchmark should distinguish retaining information from updating it, retrieving the right version, honoring scope, and abstaining when evidence is missing.

## Decision principles

- Fix the primary horizon to 168 hours from episode start; treat other horizons as separate tracks.
- Keep the benchmark architecture-neutral: incremental observation and answer-at-cutoff are the required interface, not a prescribed database or prompt.
- Keep memory-only, bounded-history, full-history, and oracle diagnostics in separate tables.
- Make temporal evidence, answerability, and source-turn provenance explicit.
- Use fictional or consented data; do not use private chat dumps.
- Release only after evidence, labels, split integrity, scoring, and licenses pass review.

## Work plan

### Phase 0 — Specification and fixture (current)

Deliver: README, JSON schema, a tiny hand-authored dev fixture, data card, and clear status label. The fixture validates representation only. It is not a performance test set.

Exit gate: all records parse, schema passes, message timestamps are chronological, every evidence reference resolves, and no future message is required to answer a question.

### Phase 1 — Pilot (30 episodes, approximately 300–360 questions)

- Author 30 distinct seven-day plans in at least six domains.
- Include all skill types, with update, temporary intent, and abstention cases represented.
- Obtain independent question answering from a visible prefix; remove ambiguous gold labels.
- Have a second reviewer audit 20% of episodes and all disputed items.
- Run simple lexical, recency, full-history, and no-memory baselines to find shortcuts and floor/ceiling effects. These are diagnostics, not leaderboard claims.
- Evaluate human agreement on answerability, evidence sufficiency, and answer quality. Revise rubrics if agreement is weak.

Exit gate: pre-registered acceptance thresholds, no unresolved leakage, documented agreement, stable scoring on paraphrase/edge cases, and a pilot report. Thresholds should be set before observing final model comparisons.

### Phase 2 — Public development set (60 episodes, approximately 720 questions)

- Use scenario-plan and template families absent from pilot evaluation templates where practical.
- Publish labels, evidence, source messages, prompt instructions, and license.
- Publish evaluator code and baseline outputs with exact versions/settings.
- Add starter adapters and schema validation; ensure a developer can run the evaluation offline.

Exit gate: reproducible results from a clean environment, versioned hashes, documented costs, and a clear path to submit predictions.

### Phase 3 — Hidden test set (target 300 episodes, approximately 3,600 questions)

- Generate from disjoint plans, entity inventories, and template families.
- Keep hidden questions/labels on a controlled evaluation service or release them only after a version is retired.
- Reserve whole episodes, not question rows, for test. Do not tune prompts against test feedback.
- Stratify domains, question categories, answerability, difficulty, session density, and query offset. Publish exact counts after freeze.
- Establish a submission policy: one official submission per system version per release window, or another clearly justified rate limit; log immutable system and evaluator versions.

Exit gate: blind review by at least two independent reviewers; source data rights confirmed; automated and manual leakage audit; frozen evaluator and judge; benchmark card approved; data checksum published.

### Phase 4 — v1.0 release and maintenance

Release benchmark card, data statement, code, baseline report, scoring artifacts, and a paper or technical report. Assign a version and checksum. Use semantic versioning: patch for documentation/bug fixes without changing examples or scores; minor for additive non-breaking data; major for changes to task definition, labels, splits, or scoring. Never overwrite a scored release silently.

## Sampling and balancing plan

Initial target test size is a proposal, not a fixed quota until a pilot verifies annotation capacity and question quality. Aim for 12 questions per episode:

- 2 recent episodic recall
- 2 cross-session binding
- 2 temporal/state-update
- 1 ephemeral intent/commitment
- 1 preference scope/decay
- 1 entity/speaker binding
- 1 distraction resistance
- 2 unanswerable/ambiguous abstention

Some questions can have secondary tags. Over the whole test set, maintain diversity in domain, dialogue style, daily message volume, time gaps, question phrasing, answer length, and evidence distance. Do not force category quotas that produce unnatural dialogue. Track all deviations.

## Annotation manual requirements

For every episode, keep a private authoring plan linking planted facts and updates to source turns. For each question, annotators must provide:

- Question and exact query timestamp.
- Answerability: answerable, unanswerable, or ambiguous under the visible prefix.
- Canonical answer plus acceptable variants or a rubric for multi-part answers.
- Minimal sufficient evidence message IDs, with optional exact spans.
- Primary and secondary skills; difficulty; update/scope/recency tags.
- For changed facts, explicit `current_value`, `previous_value`, and validity interval when relevant.
- A short rationale for ambiguous and abstention cases.

The prefix-only annotator must not see future turns or writer notes. If a competent annotator cannot answer confidently using only the prefix, either revise the episode/question or label it as unanswerable/ambiguous with an explicit rubric.

## Baseline suite

Minimum baselines:

1. Query-only / no memory.
2. Last N messages (include at least one token-matched setting).
3. Rolling summary updated after each session.
4. Retrieval over raw message chunks.
5. Structured fact store with explicit update handling.
6. Memory system under evaluation.
7. Full allowed transcript at query time.
8. Gold-evidence answerer diagnostic.

Use the same answer model and decoding settings where possible. If not, clearly label the comparison and avoid causal claims. Include at least one strong model that can solve answer generation from supplied gold evidence.

## Statistical and scoring protocol

- Predefine deterministic normalization for Exact Match: Unicode NFKC, lowercase where language permits, trim, collapse whitespace, and narrowly specified punctuation handling. Never normalize away dates, negation, units, or entity distinctions.
- Score each question once per run. If sampling is stochastic, run at least three seeds or disclose a single run and report uncertainty accordingly.
- Use episode-clustered bootstrap confidence intervals (episodes, not individual questions, are resampled) for overall and category metrics.
- Keep semantic judge outputs per item and raw judge rationale private if they contain sensitive material; for synthetic benchmark data, release item labels and a safe audit trail.
- Human-audit a stratified sample of judge decisions, all ambiguous cases, and a sample of false positives/negatives.
- Report question counts and denominators; do not average only categories that a system attempted.
- Report abstention separately from answer accuracy; an always-abstain system must not obtain a competitive overall score.

## Threats to validity and mitigations

| Threat | Mitigation |
|---|---|
| Benchmark-specific wording/template memorization | Disjoint plan and template splits; periodic refreshed hidden test; paraphrase diversity |
| Answer leakage from question or metadata | Random IDs; remove author notes; question-only baseline; leakage scans |
| Future-context leakage | Strict cutoff adapters; prefix-only answers; automated future-turn tests |
| LLM judge preference or inconsistency | Fixed prompts/model version; human calibration and audit; release labels |
| Synthetic dialogue unnaturalness | Human edit/review; disclose origin; later consented real-data extension |
| Answer model dominates memory differences | Same answer model across tracks; oracle-evidence diagnostic; publish memory-only retrieval evidence |
| Short window is confused with long-term persistence | State explicit horizon and window-boundary task; position as complement to long-term suites |
| Repeated facts make task trivial | Include updates, scoped preferences, distractors, omissions, and near-miss values |
| Overfitting to leaderboard | Rate-limit submissions, separate public dev from hidden test, retire versions on leakage |

## Governance and release responsibilities

Before v1, identify named owners for data curation, annotation, evaluator maintenance, and leaderboard operations. Maintain a public issue template for errors, a versioned correction policy, and a privacy contact. Each release must include contributor roles, data sources, generation tools, annotation compensation, licenses, and known risks. A benchmark maintainer should not certify their own system's score without a reproducible external audit.

## Go / no-go release checklist

- [ ] Every included episode is synthetic or consented and has a compatible license.
- [ ] Seven-day bounds and cutoff semantics are explicit and machine-checkable.
- [ ] No answer depends on future dialogue or private writer notes.
- [ ] All message IDs, question IDs, evidence IDs, and timestamps are valid.
- [ ] Questions are answerable from the prefix or explicitly marked otherwise.
- [ ] Independent reviewers check a stratified sample and disagreements are resolved.
- [ ] Question-only, no-memory, recency, and full-history diagnostics are run.
- [ ] Split leakage and near-duplicate scans pass.
- [ ] Metrics, confidence intervals, judge versions, and costs are documented.
- [ ] Dataset card, benchmark card, citation, license, and checksum are published.
- [ ] Public examples contain no personal data or unsafe advice.
- [ ] Release status accurately distinguishes proposal, pilot, and validated benchmark.
