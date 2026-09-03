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

## Public release policy (partial output release, 2026-09-03)

Historical note: the initial release followed **OPTION B** (all final answers
withheld). The 2026-09-03 Output Dataset Addendum partially supersedes it:
verbatim final answers for **C/D/E/F (256)** are now public under
`data/model-answers/` as benchmark artifacts; the **A/B answers (128)** remain
withheld pending additional upstream/output-terms review.

**IN the public release:**

- benchmark questions (final frozen set + Formal D stage subsets)
- project-authored documentation and protocol
- scripts (harness, runners, analysis, validation, figure generation,
  dataset build/verify tooling)
- objective structural metrics (delivery, token counts, limit signatures)
- locked score artifacts / score data as allowed by the project license choice
- aggregate tables and figures
- provenance metadata (model identities, artifact hashes, source status)
- per-model final-answer CSVs for C/D/E/F under `data/model-answers/`
  (verbatim benchmark artifacts; not relicensed — see
  data/model-answers/NOTICE.md)

**NOT in the public release:**

- A and B final answers (withheld pending additional
  upstream/output-terms review; never extracted into this repository)
- the combined 6-model CSVs (`formal-{d,c}-answers-final-only.csv`),
  superseded — publishing them would re-include the withheld A/B rows
- hidden reasoning-content / thinking traces — never published in any form
- private raw reasoning, local private files, credentials

Model-generated final-answer texts for A and B are retained in the
internal/reviewer archive only; they appear in reviewer bundles solely under
a clear REVIEW ONLY marker.

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
authorized to test. The released model-generated answers are evaluation
artifacts governed per model by the output-redistribution decision
(data/model-answers/NOTICE.md); the withheld A/B answers must not be
redistributed from reviewer archives.
