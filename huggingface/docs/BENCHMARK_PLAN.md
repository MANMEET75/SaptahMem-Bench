# Benchmark Plan and Decision Gates

## Objective and current state

SaptahMem-Bench is intended to compare short-term conversational memory systems on natural, consented conversations spanning seven days. The current release is protocol preparation only: two fictional episodes/four questions, no human-collected data, no reviewed test set, and no performance claims. This file is a plan, not evidence that a study or release has occurred.

## Frozen design choices

- Primary horizon: 168 consecutive hours from episode start; timestamps in UTC.
- Study source: prospective English-language use of a frozen, text-only study assistant for participants' ordinary, self-chosen needs; no scripted benchmark fact tasks.
- Cohort: one participant and one episode per record. Separate 50-person pilot; 1,000 main episodes initially (200 public dev, 800 hidden test), with preregistered 100-episode expansion blocks to at most 1,500 main episodes total (200 dev plus up to 1,300 hidden test).
- Questions: target 16 per main episode (normally 12 answerable and four unanswerable/ambiguous); all ten skill categories represented across the release, without forcing unnatural episode-level quotas.
- Primary task: incremental replay, then answer at a cutoff from system memory alone. The permitted prefix is strictly earlier than the cutoff.
- Primary use: paired comparison of systems. Not a product-readiness or safety certification.
- Public release: dev transcripts/labels only after separate publication consent, redaction, privacy and rights review, and re-identification audit. Hidden test stays controlled.

## Work phases and release gates

### Phase 0 — Protocol preparation (current)

Deliver this protocol, draft participant information/consent materials, annotation guide, data card, JSON schema, fictional loader fixture, deterministic validator/scorer, and exact-overlap audit. No study recruitment, participant data, hidden-test claims, or leaderboard.

**Gate:** scripts run on current fixtures; protocol and current-data claims agree across GitHub and Hugging Face; risk and privacy limitations are explicit.

### Phase 1 — Prospective pilot (50 participants/episodes)

Obtain ethics/IRB determination and security/data-protection approval before recruitment. Freeze assistant and participant materials. Run one 168-hour episode per participant, separate participation and public-release consent, and train study staff. Test opt-in flow, pause/withdrawal, logging minimization, privacy review, annotation load, category naturalness, query difficulty, agreement, and baseline feasibility. Pilot episodes are not part of main v1 scores.

Estimate question/episode variance, within-episode correlation, missingness, human annotation reliability, and collection yield. Preregister primary comparison, 3-point target paired effect, two-sided alpha 0.05, 80% power, bootstrap procedure, sample-size re-estimation rule, exclusions, and stopping rule before the main cohort. Revise prompts/rubrics only based on pilot, then freeze them.

**Gate:** no unresolved privacy incident; collection and withdrawal work end-to-end; annotator agreement and adjudication are documented; leakage audit and baseline sanity checks pass; protocol and power calculation are preregistered.

### Phase 2 — Main data collection and public dev

Recruit 1,000 distinct participants initially, aiming to publish 200 cleared dev episodes and retain 800 test episodes. Maintain one participant per episode and disjoint participant IDs across pilot/dev/test. Preserve natural variation in active days, session gaps, message volume, and everyday domains; report these distributions. Do not induce facts or query topics to fill category quotas.

Every proposed public episode receives explicit publication consent, contextual redaction, independent privacy review, re-identification assessment, and rights/license review. Exclude records that fail any gate. The release may have fewer than 200 public episodes if consent/review excludes records; recruit additional participants under the approved protocol if needed. Never relax privacy gates to hit a count. Keep participant identity linkage and raw data outside GitHub/Hugging Face.

Annotate public dev with the same blinded protocol as test. Publish only de-identified approved records and labels, exact sample counts, data version/checksum, source/collection facts, exclusions in aggregate, annotation reliability, known bias, license, and evaluator code. The present fixture remains clearly labeled fictional and separate.

**Gate:** exact records in public release have publication consent, clean validation, resolved evidence, reviewer sign-off, passing privacy audit, documented license, and frozen hashes.

### Phase 3 — Hidden test and benchmark v1

Maintain an access-controlled test store, split manifest, labels, and audit log. Two reviewers inspect every test episode; a prefix-only verifier sees no future dialogue, author note, gold answer, or evidence. Freeze item set, evaluator version, system submission schema, and checksums before accepting official runs.

Use pilot statistics for an episode-clustered paired power calculation: 80% power at two-sided alpha 0.05 for a 3 percentage-point difference on the primary macro score. If 800 test episodes are insufficient, recruit additional hidden participants in fixed 100-episode blocks while keeping 200 dev episodes fixed, up to 1,500 main episodes total (1,300 hidden). If precision/power still misses the target, report the detectable effect and mark the comparison underpowered; do not imply a decision threshold was met.

Use a rate-limited evaluation endpoint or controlled evaluation operator for submissions. Bind every submission to system/version/configuration hashes and timestamp. Do not return item-level gold data or feedback that enables hidden-set tuning. Publish an independent report with paired clustered intervals, all denominators, baseline settings, errors, efficiency, calibration, exclusions, and deviations.

**Gate:** frozen and audited hidden set; preregistered sample size and analysis; reproducible evaluator; independent privacy/annotation audit; hashes and release terms published; no unresolved leakage; baseline report complete.

### Phase 4 — Maintenance

Use semantic versioning. Patch versions fix code/docs without changing scored data. Minor versions add compatible records. Major versions change task, schema, labels, splits, or scoring. Never silently overwrite a scored version. Publish a change log, checksums, correction/removal procedure, maintainer roles, and privacy contact. Retire or refresh hidden test if leakage is demonstrated.

## Question sampling and annotation

Use the ten categories in the README. Target 16 questions per main episode, usually 12 answerable and four unanswerable/ambiguous. This is a planning target; report realized counts and do not write artificial conversations to satisfy a quota. Query cutoffs should cover short and long evidence delays, state updates, interruptions, and late-week recall. Each question records cutoff, answerability, canonical and accepted answers, minimum evidence IDs, category, difficulty, and rubric. An answerable question needs sufficient pre-cutoff evidence; unresolved uncertainty must be explicitly labeled.

For every hidden-test episode, require an author, independent prefix-only verifier, and independent second reviewer. Adjudicate all disagreements. Report raw and chance-corrected agreement with label definitions, sample, denominators, and intervals. See `ANNOTATION_GUIDE.md` for the operating procedure.

## Baselines and statistics

Run no-memory/question-only and always-abstain controls; recent-window (including token-matched); rolling session summary; raw-message retrieval; structured fact store with update/provenance handling; full permitted prefix; and gold-evidence answerer. Use the same answer model and decoding where possible. Report full-prefix and gold-evidence as diagnostics, never memory-system leaderboard scores.

Primary planned metric: macro-average question accuracy across the ten primary skill categories. Also publish micro accuracy, each category, answerability/abstention outcomes, exact match, calibrated human-audited semantic rubric score, evidence grounding, temporal/update accuracy, and efficiency. The current included scorer implements only deterministic exact/acceptable-answer and abstention scoring. For system comparisons, use paired episode-cluster bootstrap intervals and report the interval for the paired difference; resample episodes, not questions. Predefine every primary contrast and analysis before test evaluation.

## Quality and leakage controls

- Validate record shape, JSONL, unique IDs, UTC chronology, 168-hour bounds, cutoff boundaries, and evidence references.
- Assign splits by participant, never by question. Keep pilot, public dev, and hidden test participants disjoint.
- Run exact duplicate question/message scans as triage only; review semantic paraphrase and shared-template leakage manually.
- Run question-only, no-memory, recency, full-prefix, and oracle-evidence diagnostics for leakage, floor, and ceiling behavior.
- Search for future-turn dependence, answer text in question/metadata/IDs, lexical artifacts, duplicated corrections, unsupported world knowledge, and shortcut cues.
- Have annotators solve from the exact visible prefix and log all exclusions and adjudications.
- Check rights, explicit release consent, contextual de-identification, third-party references, redaction quality, and re-identification risk for every public episode.

## Tools and commands

From repository root, using Python 3.7 or later:

```bash
python scripts/validate_dataset.py data/dev/episodes.jsonl
python scripts/audit_leakage.py data/dev/episodes.jsonl
python scripts/score_predictions.py --gold data/dev/episodes.jsonl --predictions predictions.jsonl
```

`--expect-main-release` checks exact initial target counts and 16 questions per record. It is intended for private release-preparation data, not the two-record fixture. See `EVALUATION_PROTOCOL.md` for the prediction format, assumptions, and metric limitations.
