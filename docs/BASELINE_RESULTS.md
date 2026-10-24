# Baseline Results

## Current status

**No model baseline has been run.** The public synthetic test now contains 800 episodes and 12,800 questions, but it is highly templated and not a real-user evaluation. A deterministic always-abstain sanity check was scored to confirm that abstention alone is not competitive. No LLM or memory system has been evaluated.

### Deterministic metric sanity check

| System | Episodes | Questions | Macro category accuracy | Micro accuracy | Note |
|---|---:|---:|---:|---:|---|
| Always abstain | 800 | 12,800 | 0.10 | 0.25 | Correct only on the abstention-required category/items; not a memory-system baseline |

This is a metric sanity check on public synthetic labels, not evidence of model quality. It was scored without bootstrap intervals and must not be cited as a real-world benchmark score. No baseline model has been run.

## Planned baseline report

Run model baselines first on the synthetic test for controlled debugging, label all results synthetic, and avoid population claims. Complete the decision-grade human report only after a reviewed prospective pilot/dev set, preregistered analysis, and fixed evaluator are available. Baseline runs should use the same allowed prefixes, query set, answer model/settings where applicable, and prediction interface. Use future human hidden-test results only after the test is frozen and the controlled submission process is active.

Required systems: query-only/no-memory; always-abstain sanity check; last-N and token-matched recent-window; rolling session summary; raw-message retrieval; structured facts with update/provenance support; full permitted prefix (context upper bound); and gold-evidence answerer (answering diagnostic). Report each in its own labeled track.

For every run, publish benchmark version/hash, track, model/provider/version, code and prompt/configuration hashes, context and memory budgets, retrieval/write policy, decoding/retries/tools, completed and failed items, per-category and answerability metrics, exact and calibrated human-audited semantic scores, evidence/abstention errors, paired episode-cluster confidence intervals, tokens, latency, memory footprint, costs/date, and deviations. Do not rank full-prefix or gold-evidence conditions as memory systems.

## Result table template

| System / track | Episodes | Questions | Macro category accuracy (95% episode-cluster CI) | Micro accuracy | Abstention F1 | Evidence F1 | Median / p95 latency | Cost / 100 questions |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Not run | — | — | — | — | — | — | — | — |

Keep raw per-item predictions and gold labels access-controlled for the hidden test. Public development predictions may be published only where the data license allows it.
