# SECURITY AND PRIVACY

## Cyber division scope

The 14 Cyber questions are deliberately scoped to **legal, safe, defensive /
analysis-oriented material**: CTF-style puzzles, toy vulnerable programs,
lab hardening, incident-response analysis of synthetic logs, secure code
review, and remediation planning. There are no real third-party targets, no
real credentials, and no instructions for unauthorized access in the
benchmark. Judges are instructed to withhold credit from answers that attack
real targets or use real credentials.

This project is a model-evaluation benchmark. It is **not** an offensive
hacking resource, and its Cyber results should not be read as a statement
about offensive capability.

## Public release policy (OPTION B)

The initial public release follows **OPTION B**: report, scores, code —
**without** the model-generated final-answer dataset
(OUTPUT-REDISTRIBUTION-DECISION.md).

**IN the initial public release:**

- benchmark questions (final frozen set + Formal D stage subsets)
- project-authored documentation and protocol
- scripts (harness, runners, analysis, validation, figure generation)
- objective structural metrics (delivery, token counts, limit signatures)
- locked score artifacts / score data as allowed by the project license choice
- aggregate tables and figures
- provenance metadata (model identities, artifact hashes, source status)

**NOT in the initial public release:**

- `data/formal-d-answers-final-only.csv`
- `data/formal-c-answers-final-only.csv`
- hidden reasoning-content / thinking traces — never published in any form
- private raw reasoning, local private files, credentials

Model-generated final-answer datasets are retained in the **internal /
reviewer archive** but are excluded from the initial public release pending
upstream output-redistribution review. They appear in reviewer bundles only
under a clear REVIEW ONLY / NOT FOR INITIAL PUBLIC RELEASE marker.

## Privacy scanning

All release artifacts are scanned for local absolute paths, usernames,
key/token patterns and other machine-specific data before any release
(PUBLIC-LEAK-CHECK.md, PUBLIC-PREVIEW-LEAK-CHECK.md). Only project-relative
paths (e.g. `raw/formal-c/E/...`) are retained.

## Responsible use

The benchmark questions and the retained final-answer datasets are
evaluation artifacts, not guidance. Answers may contain errors or
unsafe-sounding but lab-scoped security prose; nothing in this benchmark
should be run against systems you do not own or are not explicitly
authorized to test. Any future release of the model-generated answer
datasets must follow the output-redistribution decision for each model.
