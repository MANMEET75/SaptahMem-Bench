# SaptahMem-Bench Data Card

This dataset contains two illustrative, hand-authored fictional seven-day conversational-memory episodes and four questions for schema and loader development. It is a blueprint fixture, not a validated evaluation set. Do not use it to rank models or make performance claims.

The conversations contain invented everyday planning details, timestamps, explicit corrections, and distractor dialogue. There are no real-user conversations or personal data. The benchmark is English-only at this stage. The intended task is to answer each question using only messages before its query timestamp, and to abstain when the visible prefix does not contain enough evidence.

The full proposed protocol, limitations, roadmap, privacy policy, and scoring plan are in the repository README. Current sample size is too small for meaningful statistics. No annotation-agreement or human-audit study has been conducted. Licensed under MIT for this fixture; see LICENSE.

```python
from datasets import load_dataset

ds = load_dataset("MANMEET75/SaptahMem-Bench", data_files="data/dev/episodes.jsonl")
print(ds["train"][0]["episode_id"])
```

```bibtex
@software{saptahmem_bench_blueprint,
  title = {SaptahMem-Bench: A Benchmark Blueprint for Short-Horizon Conversational Memory},
  author = {MANMEET75},
  year = {2026},
  version = {0.1.0},
  url = {https://github.com/MANMEET75/SaptahMem-Bench}
}
```
