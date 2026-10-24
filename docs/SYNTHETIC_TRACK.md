# Synthetic Track: Data Statement and Use Guide

## Release contents

This is a **programmatically generated synthetic benchmark**, not a human-participant corpus. The current generated release contains:

| Split | Episodes | Questions | File |
|---|---:|---:|---|
| Synthetic pilot | 50 | 800 | `data/synthetic/pilot/episodes.jsonl` |
| Public synthetic dev | 200 | 3,200 | `data/synthetic/dev/episodes.jsonl` |
| Public synthetic test | 800 | 12,800 | `data/synthetic/test/episodes.jsonl` |
| **Synthetic total** | **1,050** | **16,800** | plus `data/synthetic/manifest.json` |

The two earlier hand-authored loader examples (four questions) remain separate under `data/dev/episodes.jsonl`. Each synthetic episode has 18 timestamped messages across six sessions and 16 questions. Every record is marked `data_origin: programmatic_synthetic`. The public synthetic test includes its labels; it is **not a hidden test set** and submissions on it are not a secure leaderboard evaluation.

## Generation method

`scripts/generate_synthetic.py` uses a fixed seed and hand-written templates with combinatorial values for project, date, participants, venues, items, schedule values, scoped format preferences, commitments, distractors, and unanswered/ambiguous facts. It does not use participant conversations or an LLM. The generator writes one JSONL per split and a manifest with per-file SHA-256 and byte counts. The default seed is `20261025`; rerunning with the same seed and counts reproduces the same files.

The conversations cover eight everyday domains: travel, home organization, learning, hobbies, community events, work planning, errands, and meal planning. Each episode includes a schedule correction, person/task binding, one-time preference, commitment, unrelated detail, an undecided assignment, a near-window-end fact, and four questions that require abstention or stating uncertainty. Question labels and evidence IDs are generated from the same structured scenario variables as the dialogue.

Pilot, dev, and test use separate lexical pools and distinct surface-realization families. Episode IDs and event dates are unique. The exact-overlap audit is still only a triage tool; distinct strings do not guarantee semantic independence. The underlying interaction structure is intentionally controlled and remains highly templated across splits.

## What this data can and cannot establish

The synthetic set can test data adapters, cutoff/evidence handling, state-update logic, abstention behavior, and controlled system comparisons within this generator's distribution. It can reveal regressions under known scenarios.

It cannot establish how real people converse, how real users phrase corrections or preferences, population-level memory needs, product readiness, or real-world system rankings. Fixed structures and generated answer patterns may create shortcuts. Public labels allow tuning and contamination. Do not describe synthetic scores as real-user performance or as a validated benchmark result. A future consented prospective track must be separately collected, reviewed, scored, and reported.

No human annotation, human naturalness review, annotator-agreement study, model baseline, or statistical power study has been completed for this synthetic release. Automated checks confirm structure, timestamps, evidence prefixes, target counts, and exact-overlap results only.

## Reproduce and validate

From the repository root (Python 3.7+):

```bash
python scripts/generate_synthetic.py
python scripts/validate_dataset.py --expect-synthetic-release \
  data/synthetic/pilot/episodes.jsonl \
  data/synthetic/dev/episodes.jsonl \
  data/synthetic/test/episodes.jsonl
python scripts/audit_leakage.py data/synthetic/pilot/episodes.jsonl \
  data/synthetic/dev/episodes.jsonl \
  data/synthetic/test/episodes.jsonl --strict
```

The final command checks exact normalized question/message reuse across splits; passing it is not a semantic leakage guarantee. Keep and publish the generated manifest/checksums with each release.

## Loading

```python
from datasets import load_dataset

base = "https://huggingface.co/datasets/MANMEET75/SaptahMem-Bench/resolve/main/data/synthetic"
ds = load_dataset("json", data_files={
    "pilot": f"{base}/pilot/episodes.jsonl",
    "dev": f"{base}/dev/episodes.jsonl",
    "test": f"{base}/test/episodes.jsonl",
})
print(len(ds["test"]))  # 800 synthetic episodes
```

The `test` split is public synthetic data. For system evaluation, replay only the messages strictly before each question cutoff; keep gold answers/evidence out of the system input. Report results as synthetic-track results.
