---
license: mit
language:
  - en
task_categories:
  - question-answering
pretty_name: SaptahMem-Bench (Protocol and Fixture)
tags:
  - conversational-memory
  - short-term-memory
  - benchmark
  - synthetic-data
size_categories:
  - n<1K
---

# SaptahMem-Bench

**A benchmark and prospective study protocol for seven-day conversational memory.**

> **Current status: protocol and development fixture only (0.2.0-prep).** This dataset repository currently contains two fictional hand-authored episodes and four questions. No human-participant study has been run; there is no real-world dataset, validated test set, leaderboard, or model-performance result. Do not use the fixture to compare systems or make statistical/generalization claims.

SaptahMem-Bench is designed to evaluate whether a system can retain and update conversational information over a bounded **168-hour** window, retrieve the right value at a query cutoff, respect the scope of temporary intent, bind facts to the right entity, and abstain when evidence is missing. It complements long-horizon conversational memory benchmarks; it does not claim a universal definition of short-term memory.

## Current contents

- `data/dev/episodes.jsonl`: two fictional loader-fixture episodes with four questions total.
- `schemas/episode.schema.json`: episode JSON Schema.
- `LICENSE`: applies to this blueprint and current fictional fixture. It does not automatically apply to future participant data.
- `docs/`: study protocol, draft consent information, annotation instructions, evaluation protocol, data card, release gates, and baseline-results status.
- `scripts/`: offline data validator, exact-overlap triage, and deterministic scorer. These are preparation tools; no baseline model has been run.
- Full protocol, study and annotation procedures, evaluator scripts, and data card: [GitHub repository](https://github.com/MANMEET75/SaptahMem-Bench).

One JSONL line is one episode. Episodes contain a UTC start time, a 168-hour duration, chronological user/assistant messages, and questions with cutoff timestamps and gold annotations. Question evidence IDs, answers, acceptable variants, and rubrics are evaluation-only; never expose them to the system being tested.

## Planned prospective study (not collected yet)

The planned real-world data source is prospective, consented, English-language use of a fixed text study assistant for participants' ordinary, self-chosen needs over seven days. Participants will not receive scripted fact-sharing tasks or question templates. The collection assistant will be frozen, have persistent cross-session memory disabled, and collect only text, UTC timestamps, and session boundaries. No audio, location, contacts, or tool/web history are planned.

The target is 50 pilot episodes, not scored, followed by 1,000 main episodes from 1,000 distinct participants: 200 public development episodes and 800 hidden-test episodes. Target 16 questions per main episode (normally 12 answerable and four unanswerable/ambiguous). A preregistered pilot-based power analysis may add hidden-test episodes in fixed blocks of 100, up to 1,500 main episodes total (200 dev and at most 1,300 hidden test). These are plans only, not current dataset contents or guarantees of statistical power.

Public development transcripts and labels will be released only if the participant explicitly consents to public data release and each episode passes redaction, independent privacy review, rights, and re-identification checks. Participation consent alone is insufficient. Hidden-test conversations, questions, and labels will remain under controlled evaluation. Episodes that do not pass public-release gates will be excluded from the public split. The full study and withdrawal procedures are in `docs/STUDY_PROTOCOL.md`; the participant information/consent file is a draft, not an approved form. Ethics/privacy/legal review and applicable institutional approval are required before recruitment.

## Skills and evaluation

The proposed taxonomy covers recent episodic recall, cross-session binding, temporal ordering/recency, state updates, ephemeral intent, preference scope, entity/speaker binding, distractor resistance, unanswerable/ambiguous questions, and separately reported window-boundary probes. Coverage is reported as observed; category quotas must not produce unnatural conversations.

The primary evaluation replays each episode chronologically. A system observes every message once and answers questions using only messages strictly earlier than the cutoff. The primary memory-only track gives no raw transcript at query time. Report bounded-transcript, recent-window, full-prefix, no-memory, and gold-evidence diagnostics separately; full-prefix and oracle-evidence are not memory leaderboard scores.

The planned headline is macro-average per-question accuracy over primary skill categories, with micro accuracy and answerable/unanswerable/ambiguous strata reported too. The included scorer currently computes exact/acceptable-answer matches and abstention correctness; it does not determine semantic equivalence. Semantic scoring requires a frozen rubric/judge calibrated against blinded human labels. Compare systems on identical episodes, use paired episode-clustered confidence intervals, and disclose counts, failures, prompts, model versions, memory budgets, latency, token use, and costs.

## Load the current fixture

```python
from datasets import load_dataset

ds = load_dataset(
    "json",
    data_files="https://huggingface.co/datasets/MANMEET75/SaptahMem-Bench/resolve/main/data/dev/episodes.jsonl",
)
print(len(ds["train"]))  # currently 2 fictional episodes
```

## Data, risks, and limitations

No participants or private chat data are represented in the current fixture. Its tiny size, fictional wording, and public labels make it unsuitable for score claims. Future data may reflect study-participation and assistant-specific effects, English-first recruitment, category imbalance, and exclusions required for privacy. This benchmark does not certify product readiness or safety and is not intended for high-stakes medical, legal, financial, or other advice.

The current blueprint, tools, and fixture carry MIT terms. Future participant releases may have distinct terms and will only be published under a license compatible with consent and rights review. **No baselines have been run and no benchmark scores are available.** Version data and code, publish checksums, and never silently overwrite a scored release. Report issues via [GitHub](https://github.com/MANMEET75/SaptahMem-Bench); do not post participant text in public issues.

## Citation

No validated benchmark paper exists yet. Until publication, cite the repository release and immutable revision. Do not describe the current fixture as a validated benchmark.

```bibtex
@software{saptahmem_bench,
  title = {SaptahMem-Bench: A Benchmark and Study Protocol for Short-Horizon Conversational Memory},
  author = {MANMEET75},
  year = {2026},
  version = {0.2.0-prep},
  url = {https://github.com/MANMEET75/SaptahMem-Bench}
}
```
