# Changelog

All entries distinguish preparation work from an actual benchmark data release.

## 0.3.0-synthetic-prep — 2026-10-25

- Added a deterministic synthetic corpus: 50 pilot, 200 dev, and 800 public test episodes; 16 questions each (16,800 total synthetic questions).
- Added a seeded generator and per-split SHA-256/size manifest. No real or participant data is included.
- Added a required `data_origin` marker so hand-authored fiction, programmatic synthetic data, and future consented data cannot be confused.
- Added synthetic-track data statement, loading instructions, and explicit limits; the public synthetic test is not a hidden leaderboard set.
- Validated all 1,050 generated episodes and audited zero exact normalized question/message overlaps across the three splits.
- Scored a deterministic always-abstain sanity check (0.10 category-macro, 0.25 micro accuracy); no model baseline has been run.
- This preparation release does not establish naturalness, real-world generalization, or statistical power.

## 0.2.0-prep — 2026-10-25

- Added a prospective consent-based seven-day data collection protocol and release gates.
- Added blinded annotation guide, replay/scoring interface, and expanded data card.
- Added standard-library dataset validation, exact-overlap triage, deterministic scoring, and unit checks.
- Updated planned scale to a 50-episode pilot and 1,000 main episodes (200 public dev, 800 hidden test), with power-based expansion up to 1,500 main episodes total.
- Clarified that the two fictional episodes/four questions are loader fixtures only.
- No participant data were collected or added. No baseline model was run and no benchmark result is available.

## 0.1.0 — blueprint fixture

- Published benchmark proposal, schema, data card, and two fictional loader examples (four questions).
- No validated data, participant study, leaderboard, or model-performance claims.
