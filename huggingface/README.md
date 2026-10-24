---
license: mit
language:
  - en
task_categories:
  - question-answering
pretty_name: SaptahMem-Bench Synthetic Track
tags:
  - conversational-memory
  - short-term-memory
  - benchmark
  - synthetic-data
size_categories:
  - 1K<n<10K
---

# SaptahMem-Bench

**A seven-day conversational-memory benchmark with a public synthetic track and a separate proposed human-study track.**

> **Current data status:** 50 synthetic pilot episodes, 200 synthetic dev episodes, and 800 synthetic test episodes; 16 questions per episode (16,800 synthetic questions total). The original hand-authored loader fixture remains separate: two episodes/four questions. **No participant study or real-world conversational data has been collected.** Synthetic dialogue is template-driven and does not establish real-user performance or product readiness.

SaptahMem-Bench tests memory over a bounded **168-hour** window: recall, cross-session binding, updates, recency, temporary preference scope, commitments, entity binding, distraction resistance, and grounded abstention. It is designed as a short-horizon complement to long-horizon conversation-memory evaluations.

## Files and splits

- `data/synthetic/pilot/episodes.jsonl`: 50 synthetic pilot episodes / 800 questions.
- `data/synthetic/dev/episodes.jsonl`: 200 public synthetic development episodes / 3,200 questions.
- `data/synthetic/test/episodes.jsonl`: 800 public synthetic test episodes / 12,800 questions. Test labels are public; this is **not** a hidden or leakage-resistant leaderboard split.
- `data/synthetic/manifest.json`: generation seed, split counts, byte sizes, and SHA-256 checksums.
- `data/dev/episodes.jsonl`: two separate hand-authored fictional loader examples / four questions.
- `schemas/episode.schema.json`: schema, including the required `data_origin` field.
- `scripts/`: deterministic generator, validator, overlap audit, and scorer.
- `docs/`: synthetic data statement, study/consent drafts, annotation/evaluation manuals, plan, and baseline status.
- [GitHub source](https://github.com/MANMEET75/SaptahMem-Bench): full source, tests, and release history.

## Synthetic data construction

The corpus is generated deterministically by `scripts/generate_synthetic.py`, default seed `20261025`. It uses hand-written templates and controlled fictional values; it does not use user chat logs, participants, or LLM-generated dialogue. The eight scenario domains are travel, home organization, learning, hobbies, community events, work planning, errands, and meal planning. Split-specific lexical pools and wording families are used, but all splits share a controlled scenario structure and remain highly templated.

Episodes contain timestamped messages over six sessions and 16 labeled questions. The questions cover ten primary categories, including current versus superseded values, one-time preferences, commitments, multi-turn entity binding, distractions, late-window recall, and unanswerable/ambiguous requests. Gold evidence IDs must refer to messages strictly before the query cutoff. Every synthetic row is marked `data_origin: programmatic_synthetic`.

## Use and limits

The synthetic data can support adapter checks, deterministic regression tests, and controlled comparisons on this generator's distribution. Because all splits and labels are public, systems may be tuned to them. Exact string-overlap checks do not prove semantic independence, and template variation does not make the dialogue naturalistic. Report results explicitly as **synthetic-track scores**; do not infer real-user behavior, population needs, deployment readiness, or real-world system rankings from them.

No human naturalness review, annotator-agreement study, power analysis, or model baseline has been completed. A deterministic always-abstain metric sanity check (0.10 category-macro accuracy and 0.25 micro accuracy on synthetic test) is documented in `docs/BASELINE_RESULTS.md`; no memory model was tested.

## Load the public synthetic splits

```python
from datasets import load_dataset

base = "https://huggingface.co/datasets/MANMEET75/SaptahMem-Bench/resolve/main/data/synthetic"
ds = load_dataset("json", data_files={
    "pilot": f"{base}/pilot/episodes.jsonl",
    "dev": f"{base}/dev/episodes.jsonl",
    "test": f"{base}/test/episodes.jsonl",
})
print(len(ds["test"]))  # 800 public synthetic episodes
```

For evaluation, replay each message once in timestamp order and answer using only the system state built from messages strictly before each cutoff. Never provide gold answers, evidence IDs, rubrics, or future turns to the evaluated system. The scorer, exact-match normalization, abstention policy, and confidence-interval method are documented in `docs/EVALUATION_PROTOCOL.md`.

To regenerate from the source repository, run `python scripts/generate_synthetic.py`; compare the resulting manifest checksums. Validate the three files with `scripts/validate_dataset.py --expect-synthetic-release` and run `scripts/audit_leakage.py` across all splits. An audit pass detects exact normalized reuse only, not semantic/template leakage.

## Separate prospective human track (planned, not collected)

A future track is planned from prospective, consented English use of a frozen text assistant for ordinary self-chosen needs over seven days. Its targets are a separate 50-person pilot and 1,000 main episodes (200 public dev, 800 hidden test), with a pilot-based preregistered power analysis and possible expansion to 1,500 total. These targets are not the synthetic episodes above.

Human collection requires applicable ethics/IRB and privacy/security review before recruitment. Participation consent and public transcript-release consent must be separate; public release also requires redaction, independent privacy and re-identification review, and rights approval. The current repository contains only draft materials. Do not mix or relabel synthetic data as participant data. Full procedures are in `docs/STUDY_PROTOCOL.md` and `docs/CONSENT_TEMPLATE.md`.

## License, citation, and status

The repository MIT license applies to the current generator, synthetic data, fictional fixtures, documentation, and tools. No participant records are included. No validated real-world benchmark paper exists; cite the repository and immutable revision, and state that results are from the public synthetic track.

```bibtex
@software{saptahmem_bench_synthetic,
  title = {SaptahMem-Bench: A Synthetic Benchmark Track for Seven-Day Conversational Memory},
  author = {MANMEET75},
  year = {2026},
  version = {0.3.0-synthetic-prep},
  url = {https://github.com/MANMEET75/SaptahMem-Bench}
}
```
