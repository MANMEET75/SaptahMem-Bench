# Data Card: SaptahMem-Bench

## Current release facts

- **Version/status:** 0.2.0-prep; protocol and loader fixture, not a validated dataset release.
- **Current data:** two hand-authored fictional episodes and four questions in `data/dev/episodes.jsonl`.
- **Current source:** fictional examples authored for schema/loader testing. No participant data, chat logs, or user study is included.
- **Current validation:** scripts can validate timestamps/evidence and score deterministic exact/acceptable-answer predictions. No annotator study, human review, power analysis, model baseline, or leaderboard result has been produced.
- **Current suitability:** schema and adapter prototyping only. Not suitable for model ranking, real-world generalization claims, deployment decisions, or statistical conclusions.
- **Current license:** the existing blueprint and fictional fixture carry the repository's MIT terms. This says nothing about rights to future participant data.

## Planned study release (not yet collected)

The proposed v1 source is prospective, consented, English-language use of a fixed text study assistant for participants' ordinary, self-chosen needs over 168 hours. It is not scripted scenario completion or donated historical chat. The assistant version is frozen, persistent cross-session memory is disabled, and collection is limited to text, UTC timestamps, and session boundaries. No audio, location, contacts, or tool/web history is planned.

Plan: 50 pilot episodes, excluded from scored v1; then 1,000 main episodes from 1,000 distinct participants, initially split into 200 public development and 800 hidden test episodes. Each main episode targets 16 questions (normally 12 answerable and four unanswerable/ambiguous). A pilot-based preregistered power analysis may add hidden-test blocks of 100 episodes up to 1,500 main episodes total (200 dev and up to 1,300 hidden test). The pilot is not proof that the target size suffices; report the realized detectable effect and power.

These are targets only. Do not represent them as collected, available, or validated. Every future release must replace this section with exact counts, collection dates, participant flow and exclusions, consent choices, review/annotation process, license, checksums, and deviations.

## Task and intended use

Each record is a seven-day conversation episode with chronological messages and timestamped question cutoffs. A system observes the transcript incrementally and answers from only the prefix available before each cutoff. The primary track evaluates memory without passing the raw transcript at query time. Separate diagnostics compare bounded history, recent-window, full-prefix, query-only, and gold-evidence conditions.

After validation, intended use is research comparison of short-term conversational memory systems, including recall, cross-session binding, updates, scoped temporary intent, entity binding, distraction resistance, abstention, evidence grounding, and efficiency. This does not certify product readiness or safety and is not for high-stakes medical, legal, financial, or other advice.

## Collection, consent, and privacy

No participants have been recruited for the present release. Before any prospective study, obtain applicable ethics/IRB review, data-protection/security review, approved materials, separate explicit consent for public transcript release, and a preregistration. Participation consent alone does not authorize public release. The detailed procedures and gates are in `STUDY_PROTOCOL.md`.

The planned public development data must be de-identified, reviewed by an independent privacy reviewer, and checked for re-identification risk. Remove direct identifiers and sensitive incidental content; minimize third-party details. Episodes that fail publication consent, redaction, rights, or privacy review are excluded from the public split. Keep the hidden test transcripts/questions/labels access-controlled. Define withdrawal, retention, access logging, incident response, and deletion before collection. Do not use scraped or private chat dumps.

## Annotation and quality

The planned annotation protocol requires a question author, independent prefix-only verifier, and second reviewer for every hidden-test episode. Verifiers see no future turns, author notes, gold answer, or evidence labels. Annotate canonical and accepted answers, answerability, minimum evidence IDs, skills, difficulty, and a distinguishing rubric. Adjudicate disagreements and report agreement with counts and uncertainty. No such annotation or agreement results exist for the current four-question fixture.

## Biases and limitations

The present fixture is tiny, English-only, and fictional. It cannot support statistical analysis or represent actual user behavior. A future prospective study may still have participation effects, selection bias, assistant-specific interaction patterns, English-first coverage, and public-release exclusions. Natural occurrence of rare skill categories may be uneven; report realized distribution rather than claim balanced population prevalence. Synthetic examples must remain clearly labeled and must not be combined with participant data without release-specific provenance.

## Maintenance and contact

Version data and code separately, publish immutable checksums, and never silently replace a scored release. Report public schema or label issues in the GitHub repository. Before recruitment, establish and test a monitored private contact route for privacy, incidents, and withdrawal requests; no participant study should begin until it exists. Do not post participant text in public issues.
