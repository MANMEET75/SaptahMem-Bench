---
license: mit
language:
  - en
task_categories:
  - question-answering
pretty_name: SaptahMem-Bench (Blueprint Fixture)
tags:
  - conversational-memory
  - short-term-memory
  - benchmark
  - synthetic-data
size_categories:
  - n<1K
---

# SaptahMem-Bench

**A benchmark blueprint for short-horizon conversational memory in assistants.**

> **Release status: v0.1.0 blueprint and development fixture.** This is a proposal, not a completed or human-validated benchmark. It has no leaderboard or model-performance claims.

SaptahMem-Bench evaluates whether an assistant can retain, update, retrieve, combine, and appropriately abstain on facts across a bounded **seven-day (168-hour) conversational window**. It is designed to complement long-horizon evaluations such as BEAM and LoCoMo by focusing on freshness, temporary intent, scope, and near-term state changes.

## Current dataset contents

This release contains **two fictional hand-authored episodes and four questions**. The examples are provided to help validate loaders and discuss the schema. They are not suitable for model ranking, statistical analysis, or claims about real-world users.

Files:
- data/dev/episodes.jsonl — episode-level records with messages and questions.
- schemas/episode.schema.json — JSON Schema for validating episode records.
- GitHub repository — full benchmark plan, annotation instructions, and release checklist: https://github.com/MANMEET75/SaptahMem-Bench

## Task and episode format

Each episode declares a UTC start time and 168-hour duration. Its chronologically ordered user/assistant messages have stable message IDs, timestamps, and session IDs. Each question has an explicit query cutoff. Answer using only messages timestamped before that cutoff; future dialogue and gold labels are evaluator-only. `source_message_ids` identify the supporting evidence and must not be shown to the evaluated answerer.

Question fields include the question text, primary and secondary skills, answerability label, canonical answer, acceptable variants, evidence IDs, difficulty, and a grading rubric. Unanswerable questions use a null gold answer and require a grounded abstention.

## Proposed skill taxonomy

1. Recent episodic recall.
2. Cross-session fact binding and multi-hop composition.
3. Temporal order and recency.
4. State updates and corrections, including current versus historical values.
5. Ephemeral plans, reminders, deadlines, and commitments.
6. Preference scope: stable versus task- or week-specific.
7. Entity and speaker binding.
8. Distractor resistance.
9. Unanswerable and ambiguous query handling.
10. Retention-window boundary probes, reported as a separate track.

## Seven-day evaluation protocol

- Observe every message exactly once in timestamp order; no future turns, question labels, or evidence metadata during ingestion.
- Use UTC timestamps and seven 24-hour bins measured from the episode start, not local calendar midnights.
- Answer questions only from the permitted prefix and selected track. The primary cutoff is within the 168-hour horizon.
- Return a final answer and, where supported, cited message IDs or spans. Record model versions, prompts, token usage, latency, retries, external calls, and memory settings.
- Do not use web search or test labels to answer benchmark questions.

### Report separate tracks

- Memory-only (primary): incremental memory is available; raw transcript is not passed at query time.
- Memory plus bounded transcript: disclose the buffer size and memory budget.
- Recent-window baseline: disclose last-N-message or time-window limit.
- Full-history context upper bound: all pre-cutoff messages are supplied; this does not demonstrate external memory.
- No-memory baseline: question-only answering to detect leakage or answer priors.
- Oracle-evidence diagnostic: supply gold evidence to measure answer-generation ability; do not rank as a memory score.

Never combine these tracks into one leaderboard score. Disclose model/provider versions, prompts, decoding, context and memory budgets, retrieval settings, costs, code revision, and all retries.

## Scoring

Report results overall and by skill, answerability, difficulty, and episode, including denominators and episode-clustered confidence intervals.

- Exact match for constrained answers using documented normalization that preserves dates, negation, units, and entity distinctions.
- Semantic answer accuracy using a fixed rubric/judge, with judge model, prompt, raw labels, and human audit sample disclosed.
- Evidence precision, recall, and F1 when systems return evidence; do not treat an uncited answer as grounded.
- Abstention precision, recall, and F1; separately count missed abstentions and false assertions.
- Temporal/state accuracy for current-value and historical-value questions.
- Efficiency: median/p95 latency, stored/read/generated tokens, memory footprint, and cost per 100 questions.
- Error types: stale value, forgotten fact, wrong entity, unsupported inference, false abstention, missed abstention, and evidence mismatch.

Proposed headline: macro-average semantic accuracy over the ten primary skills, while showing answerable and unanswerable strata separately. Also publish micro accuracy and every category score. Do not publish leaderboard rankings until a reviewed test set and calibrated evaluator exist.

## Planned scale and curation

The proposed v1 target is a 30-episode pilot, 60 public development episodes, and 300 hidden test episodes, with about 12 questions per episode. These are planning targets and may change after the pilot. Split entire scenario plans, entity inventories, and template families to reduce leakage. Aim for at least 25% unanswerable/ambiguous and 25% update/recency questions if natural coverage and pilot quality support those proportions.

Creation workflow: author a seven-day scenario plan; write varied sessions and distractors; annotate canonical answers, answerability, minimal evidence, skill, and rubric; independently answer from each visible prefix; run chronology, schema, evidence, duplicate, and leakage checks; adjudicate disagreements; publish a data statement and versioned checksums. A prefix-only annotator must never see future turns or author notes.

## Data statement, intended use, and limits

The current records are fictional and hand-authored. No private chat, participant data, sensitive personal data, or real-user conversation is included. The fixture is English-only and tiny; it cannot represent natural dialogue diversity or real-world memory needs. No annotation-agreement study or human audit has been conducted. Do not use this fixture to compare systems or make safety/product claims. Future releases must document source provenance, generation tools, consent, compensation, licenses, review, and known limitations; never distribute scraped private chats or personal identifiers.

Intended now: schema/load testing and methodology discussion. Intended after validation: research evaluation of short-horizon conversational-memory systems. Not intended for high-stakes medical, legal, or financial evaluation.

## Load the JSONL

    from datasets import load_dataset
    ds = load_dataset("json", data_files="https://huggingface.co/datasets/MANMEET75/SaptahMem-Bench/resolve/main/data/dev/episodes.jsonl")
    print(ds["train"][0]["episode_id"])

For local use, pass the downloaded JSONL path to `load_dataset("json", data_files=...)`. Each row is one complete episode; questions are nested within the episode record.

## License, citation, and status

MIT for this blueprint fixture and its documentation. A future benchmark release may use different terms. No paper or official validated benchmark release exists yet; cite the repository and immutable revision, and do not describe this fixture as a validated benchmark.

```bibtex
@software{saptahmem_bench_blueprint,
  title = {SaptahMem-Bench: A Benchmark Blueprint for Short-Horizon Conversational Memory},
  author = {MANMEET75},
  year = {2026},
  version = {0.1.0},
  url = {https://github.com/MANMEET75/SaptahMem-Bench}
}
```