# Data Card: SaptahMem-Bench

## Current release

- **Version/status:** 0.3.0 synthetic track preparation; no validated real-world benchmark release.
- **Synthetic data:** 50 pilot episodes, 200 dev episodes, and 800 public test episodes; 16 questions per episode; 1,050 episodes and 16,800 questions total.
- **Separate loader fixture:** two hand-authored fictional episodes and four questions under `data/dev/episodes.jsonl`.
- **Origin:** synthetic episodes are generated deterministically by `scripts/generate_synthetic.py` with seed `20261025`; no participant data, historical chat logs, or LLM-generated dialogue are used. The two loader examples are hand-authored fiction.
- **Quality work completed:** structural/timestamp/cutoff/evidence validation, exact cross-split overlap audit, deterministic scoring tests, and count/checksum manifest. No human naturalness review or annotation agreement study has been run.
- **Baselines:** no model baseline has been run. A deterministic always-abstain metric sanity check is recorded in `BASELINE_RESULTS.md`; it is not a memory-system result.
- **License:** repository MIT terms apply to the code, documentation, generator, and current fictional/synthetic data. There is no real participant data in this release.

## Synthetic dataset composition

The synthetic track contains multi-session seven-day conversations covering travel, home organization, learning, hobbies, community events, work planning, errands, and meal planning. Each episode has 18 messages over six sessions and 16 questions covering recent recall, cross-session binding, recency, updates, temporary preferences, commitments, entity binding, distraction resistance, window-boundary retrieval, and abstention/ambiguity. The manifest records per-split question counts, exact byte sizes, and SHA-256 checksums.

The data is fully public, including the test labels. Its splits use different name/venue inventories and surface phrasing families, but they share a controlled scenario structure and remain highly templated. The test is not hidden, and public labels permit tuning and contamination.

## Intended uses and limits

Use this track for evaluator/adaptor checks, controlled comparisons of memory behaviors on known synthetic cases, and regression testing. Report every score as a result on the **SaptahMem-Bench synthetic track**. Do not use it to infer real-user conversation patterns, population memory needs, product readiness, safety, or real-world system ranking. It is not a substitute for the planned prospective consented-human track.

The present data are English-only and generated from a finite template system. Correctly varied strings do not establish semantic split independence or naturalness. The generator may create cues unavailable in real dialogue and can reward systems tuned to its pattern. No participant study, human reviewer validation, judge calibration, power analysis, or deployment assessment is complete.

## Future prospective track (planned, not collected)

The separate human-data proposal is prospective, consented English use of a frozen text assistant for ordinary, self-chosen needs over 168 hours. The target is a 50-episode pilot followed by 1,000 main episodes (200 public dev, 800 hidden test), each targeting 16 questions. A preregistered power analysis may expand the main human release in 100-episode blocks to 1,500 total. These are targets only and are unrelated to the synthetic records above.

No human recruitment should occur until required ethics/IRB, privacy/security, participant-material, and preregistration gates pass. Public human transcripts require separate publication consent and per-episode privacy/re-identification review. See `STUDY_PROTOCOL.md` and the draft-only `CONSENT_TEMPLATE.md`. No participant data may be mixed with or relabeled as synthetic.

## Maintenance

Keep code, generator version, seed, data checksum, scoring code, and data version together. Do not silently replace a scored dataset. Fixes to synthetic data require regenerating and versioning the affected split/manifest; fixes to a future human dataset must follow the approved withdrawal and correction process. Report public issues on GitHub, but never post participant text. Establish a monitored private privacy/withdrawal contact before human recruitment.
