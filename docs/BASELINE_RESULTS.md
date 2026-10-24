# Baseline Results

## Current status

**No baseline has been run.** The repository currently contains only two fictional loader-fixture episodes and four questions. Their size and public labels make them unsuitable for model comparisons, confidence intervals, or performance claims. This page intentionally contains no invented scores.

## Planned baseline report

Complete this report only after a reviewed pilot/dev set and fixed evaluator are available. Baseline runs should use the same allowed prefixes, query set, answer model/settings where applicable, and prediction interface. Use hidden-test results only after the test is frozen and the controlled submission process is active.

Required systems: query-only/no-memory; always-abstain sanity check; last-N and token-matched recent-window; rolling session summary; raw-message retrieval; structured facts with update/provenance support; full permitted prefix (context upper bound); and gold-evidence answerer (answering diagnostic). Report each in its own labeled track.

For every run, publish benchmark version/hash, track, model/provider/version, code and prompt/configuration hashes, context and memory budgets, retrieval/write policy, decoding/retries/tools, completed and failed items, per-category and answerability metrics, exact and calibrated human-audited semantic scores, evidence/abstention errors, paired episode-cluster confidence intervals, tokens, latency, memory footprint, costs/date, and deviations. Do not rank full-prefix or gold-evidence conditions as memory systems.

## Result table template

| System / track | Episodes | Questions | Macro category accuracy (95% episode-cluster CI) | Micro accuracy | Abstention F1 | Evidence F1 | Median / p95 latency | Cost / 100 questions |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Not run | — | — | — | — | — | — | — | — |

Keep raw per-item predictions and gold labels access-controlled for the hidden test. Public development predictions may be published only where the data license allows it.
