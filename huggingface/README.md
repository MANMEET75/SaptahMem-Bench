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

# SaptahMem-Bench (Blueprint Fixture)

**Status: v0.1.0 proposal and development fixture. This is not a validated benchmark release.**

This dataset contains two illustrative, hand-authored fictional seven-day conversational-memory episodes and four questions for schema and loader development. Do not use it to rank models or make performance claims.

## Task

Answer each question using only messages whose timestamp is earlier than that question's `query_time`. The episodes have a 168-hour declared window, chronological timestamped messages, updates, distractor turns, and evidence labels. For unanswerable questions, state that the visible history does not provide the requested fact. Never use future messages, labels, source IDs, or outside knowledge to answer.

The JSONL records are episode-level examples: each includes its messages and a list of questions. Fields and constraints are specified in `../schemas/episode.schema.json` and the benchmark protocol is in the GitHub README.

## Load

```python
from datasets import load_dataset

ds = load_dataset("MANMEET75/SaptahMem-Bench", data_files="data/dev/episodes.jsonl")
print(ds["train"][0]["episode_id"])
```

For raw JSONL, download `data/dev/episodes.jsonl` from the Files tab. The GitHub repository contains the canonical schema and full benchmark plan.

## Data and limitations

- Two fictional episodes and four questions; English only.
- Hand-authored for schema examples; no private chats or real-user data.
- No participant study, annotator agreement study, or human audit has been conducted.
- The sample is tiny, easy to inspect, and statistically meaningless. It cannot support model comparisons or claims about real users.
- The proposed benchmark needs a pilot, independent review, leakage testing, judge calibration, and a frozen hidden test before leaderboard use.
- Synthetic examples do not establish real-world prevalence or distribution.

## License

MIT for this blueprint fixture and its documentation. See the repository `LICENSE`. Future dataset versions may have different terms.

## Citation

No paper or official benchmark release exists yet. Cite the GitHub repository and immutable commit for this blueprint. Do not cite this fixture as a validated benchmark.

```bibtex
@software{saptahmem_bench_blueprint,
  title = {SaptahMem-Bench: A Benchmark Blueprint for Short-Horizon Conversational Memory},
  author = {MANMEET75},
  year = {2026},
  version = {0.1.0},
  url = {https://github.com/MANMEET75/SaptahMem-Bench}
}
```
