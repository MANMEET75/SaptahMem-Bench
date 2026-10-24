# Data Card: SaptahMem-Bench (Blueprint)

## Summary

SaptahMem-Bench is a proposed benchmark for short-horizon conversational memory over a bounded seven-day (168-hour) interaction window. This repository currently contains a benchmark specification and two small, hand-authored development examples intended to validate schema and loader behavior. It does not yet contain a validated test set or performance leaderboard.

## Dataset status

- **Release:** 0.1.0 blueprint / development fixture
- **Task:** conversational memory question answering at explicit timestamps
- **Unit:** one fictional conversation episode plus queries, labels, and evidence
- **Current size:** 2 illustrative episodes; 4 illustrative questions
- **Intended future size:** 60 public development episodes and 300 hidden test episodes, subject to pilot quality and resources
- **Current use:** software/schema prototyping and discussion of the proposed protocol only
- **Not suitable for:** model ranking, generalization claims, deployment safety claims, or comparison of published systems

## Motivation

Short-term conversational memory includes recent facts, temporary plans, evolving state, and scoped preferences. The benchmark aims to measure whether systems retain and update these details across sessions while avoiding stale answers and unsupported guesses.

## Source and construction

The included records are hand-authored fictional examples. They do not represent actual people and contain no copied private conversations. Future releases may include synthetic, human-authored, or consented conversational data; every release must state the exact source mix and review process. The proposed target workflow includes scenario planning, conversation authoring, question writing, prefix-only verification, independent review, leakage checks, and adjudication.

## Collection and annotation

No participant data was collected for this blueprint fixture. No annotator agreement study has been conducted. The future benchmark must document annotator instructions, reviewer count, compensation, adjudication, and agreement for answerability, evidence, and semantic scoring.

## Intended uses

- Prototyping data loaders and evaluation adapters.
- Designing research on short-horizon memory and retention.
- Evaluating answerability, updates, recency, evidence grounding, and efficiency after a validated release.

## Out-of-scope uses

- Treating scores on this two-episode fixture as evidence of product quality.
- Inferring how real users behave from fictional examples.
- Testing medical, legal, financial, or other high-stakes advice.
- Re-identifying real people; the current fixture has no real-person data.

## Biases and limitations

The current sample is tiny, English-only, and authored by one person. It cannot represent dialogue diversity, real-world noise, cultural variation, natural rates of forgetting, or population-level preferences. Its facts and question patterns are easy to inspect and may be memorized. It is not suitable for statistical analysis. LLM-as-judge scoring is only a proposal pending calibration and human audit.

## Privacy and risk

Current examples use fictional names and ordinary low-risk logistics. Future data releases must prevent disclosure of sensitive personal information, define consent and withdrawal procedures, and review synthetic outputs for accidental real-person references. A seven-day benchmark captures one operational window and does not establish a universal definition of short-term memory.

## License and terms

The current benchmark documentation and examples use MIT terms (see repository `LICENSE`). A future dataset may use a distinct license; the release-specific terms take precedence and must be reviewed before redistribution.

## Maintenance

Report errors through the repository issue tracker. Corrections will be documented in the changelog and released with versioned checksums. Scored releases will not be silently overwritten.
