# Prospective Study Protocol (Pre-registration Draft)

## Status and approval gate

This document is a research protocol draft, not an ethics approval, legal opinion, or participant consent form. No participant recruitment or data collection is authorized by publishing this repository. Before recruitment, the study owner must obtain the ethics/IRB determination required by the applicable institution and jurisdiction, finalize data-protection and security reviews, approve participant-facing materials, and preregister the protocol and analysis plan. The benchmark maintainers must publish the approval/oversight type and protocol version without exposing participant identities.

## Study objective

Collect consented, naturalistic English conversations over seven days to create a replayable evaluation set for short-term conversational memory. The primary estimand is paired performance difference between memory systems answering the same held-out queries over the same permitted transcript prefixes. The study does not test clinical, legal, financial, or safety advice and must not be represented as certifying a deployed product.

## Design at a glance

| Stage | Episodes / participants | Use | Release |
|---|---:|---|---|
| Pilot | 50 / 50 | Feasibility, annotation reliability, category coverage, variance and power estimates | Not part of scored v1; publish only aggregate protocol findings |
| Main development | 200 / 200 | Public development set, only for episodes cleared for open release | De-identified transcripts and labels on Hugging Face after explicit publication consent and review |
| Main test | 800 / 800 initial target | Frozen hidden test and controlled evaluation | Transcripts, questions, and labels remain access-controlled |
| Power extension | +100 main episodes at a time, up to 1,500 main episodes total (200 dev plus at most 1,300 test) | Only if the preregistered precision/power rule requires it | Hidden additions; final total and reason reported |

One participant contributes one episode. Pilot and main cohorts are disjoint. Target one 168-hour window per participant. Episodes with naturally sparse use remain eligible if they provide enough context for at least one valid question; publish conversation-volume strata and do not pad conversations with scripted facts. A power analysis based on pilot variance and within-episode correlation must be completed before the main cohort. The target is 80% power at two-sided alpha 0.05 for a preregistered 3 percentage-point paired difference on the primary score; if the pilot indicates the initial 800-episode test target is insufficient, add 100-episode blocks while keeping the 200-episode dev target fixed, up to 1,500 main episodes total (1,300 hidden test). If the cap still cannot meet the target, report the detectable effect and label comparisons underpowered.

## Collection procedure

1. Recruit adults able to provide informed consent and use English. Apply eligibility and compensation consistently. Recruitment must aim for varied ages, regions, occupations, and everyday use patterns without collecting unnecessary demographic detail. Any demographic subgroup analysis requires a separate pre-specified rationale and adequate sample size.
2. Explain that the assistant interaction is recorded for research, that users should not share secrets or sensitive personal information, what is retained, the publication choices, withdrawal deadline, risks, contacts, and compensation. Consent to participate and consent to public transcript release are separate choices.
3. Use a frozen, text-only study assistant with persistent cross-session memory disabled and no external web/tools. Give a brief onboarding for privacy and technical use, but do not assign tasks, seed facts, name benchmark categories, or reveal future questions. Participants use it for their own ordinary, self-selected needs during the seven days.
4. Record only message text, speaker role, UTC timestamp, and session boundary required for chronological replay. Do not collect audio, location, contacts, uploaded files, web/tool traces, or unrelated app telemetry. Keep study identifiers separate from transcript records; do not put names, email, or recruitment IDs in released JSONL.
5. Give participants a clear pause/stop control and a contact route to request withdrawal. Do not add reminders that pressure participants to use the assistant. At the end, confirm whether public release consent still applies and provide the withdrawal deadline.
6. Freeze a collection manifest and model/software versions. Log data access and transformations. Store raw records encrypted with role-based access; only approved curators may access them.

The collection assistant must be version-pinned across participants, use the same system prompt and model configuration, and avoid durable memory. Changes required for safety or reliability must be documented; if they affect dialogue behavior, start a new cohort or report the cohort as a separate stratum.

## Privacy, consent, and release

- Collect only the information necessary for the evaluation. Tell participants not to share passwords, account numbers, exact addresses, medical details, or information that identifies other people.
- Before annotation, redact direct identifiers and sensitive incidental content. Replace names consistently within an episode with neutral aliases only when entity continuity is needed. Remove or rewrite third-party identifying details; do not assume participant consent covers people they mention.
- A privacy reviewer who did not author the dialogue reviews every proposed public episode. Run automated detectors as aids, then conduct manual contextual review. Automated redaction alone is not sufficient.
- Explicitly obtain permission for public release of the de-identified transcript and labels. Participation consent without data-publication consent permits no public transcript release.
- Conduct and document a motivated intruder/re-identification review. Exclude records that are recognizable, contain rare identifying combinations, cannot be safely redacted without destroying meaning, or have unclear rights. Do not publish raw-to-redacted linkage tables.
- Publish only the approved 200 development episodes and aggregate study documentation. Keep hidden-test transcripts, questions, and gold labels in controlled storage; define named access roles, access logs, encryption, backup, retention, and incident response before collection.
- Define withdrawal handling before recruitment. Remove a participant's unreleased record on a valid request through the stated cutoff. After public release, explain the practical limits of withdrawing copied public data before consent is given; offer a maintainer contact and documented correction/removal procedure.
- Use a dataset license only after rights review confirms that participant consent and local law allow that license. Do not imply that MIT applies to participant data merely because it applies to code or the current fixture.

## Exclusions and quality handling

Exclude from public release, while retaining only as permitted by the approved protocol, an episode with missing publication consent, a privacy-review failure, corrupted chronology, unresolved identity linkage, or insufficient rights. A participant may withdraw without penalty as described in approved materials. Do not exclude an episode solely because it is sparse, contains no example of a desired skill, or is difficult to annotate; report those properties and use natural-category coverage during question sampling. Never modify a transcript to plant a benchmark answer.

## Research documentation and go/no-go

Before pilot: approved protocol/materials, security plan, frozen assistant, trained staff, incident/withdrawal process, and preregistration. Before public dev: explicit publication consent, per-record redaction review, privacy sign-off, data license, annotation quality report, and checksums. Before hidden evaluation: frozen split, labels, scoring code, power/precision statement, blinded test handling, and independent audit. Publish recruitment flow, exclusions by reason, compensation method, source provenance, collection dates, assistant versions, and limitations in aggregate only.

## Consent-information template outline

The approved participant document should explain: study purpose; seven-day activity; exact data fields; intended publication and separate opt-in; foreseeable privacy risks; data access, retention, and security; withdrawal deadline and post-release limits; voluntary participation and compensation; eligibility; researcher/ethics contacts; and how to report an incident. This outline is not itself consent language and must be adapted and approved locally.
