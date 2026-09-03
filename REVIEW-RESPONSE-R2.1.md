# Response to Final Release-Gate Review — R2.1 hotfix

> **Historical record.** This review response documents the state at its
> time, when all final answers were withheld (Option B). The 2026-09-03
> Output Dataset Addendum partially supersedes that decision — C/D/E/F
> final answers are now released under `data/model-answers/`; A/B remain
> withheld. The text below is preserved unmodified.


Final-gate verdict: **NOT READY TO PUBLISH**, with P0 = 0 and three explicit
P1s. This document responds to those three P1s and records the non-blocking
P3 stale-metadata cleanup. No inference was re-run; no locked score, mapping,
or raw artifact changed; R2 is preserved unmodified in
`release-candidate-r2/`.

## P1-1 — public-release-preview / PUBLIC-RELEASE-CONTENTS.md not in the reviewer bundle

- **FINDING:** Option B could not be verified because the actual preview tree
  and its contents manifest were absent from the reviewer bundle.
- **ROOT CAUSE:** the preview existed only as a claim in RELEASE-READINESS; it
  was not built into the bundle.
- **FIX:** built the **real** `public-release-preview/` directory (mirrors
  `release-candidate-r2.1/` minus the two model-answer datasets), with
  `PUBLIC-RELEASE-CONTENTS.md` (INCLUDED table with relative path + artifact
  class + reason; EXCLUDED table; RELEASE POLICY = Option B). Added
  `scripts/validate_public_release_preview.py` (programmatic: every INCLUDED
  path exists; EXCLUDED absent by filename AND content signature; hard-fail on
  answer-CSV names; reasoning/private/credential scan; file count) and a
  dedicated `PUBLIC-PREVIEW-LEAK-CHECK.md` (PASS, 0 answer files, 0 real
  leaks). The preview and both files are now physically inside the reviewer
  bundle and the ZIP.
- **VALIDATION:** `validate_public_release_preview.py` → PUBLIC RELEASE
  PREVIEW: VALID (63 listed INCLUDED, all exist, EXCLUDED absent, 0 answer
  signatures); preview leak check PASS.
- **ARTIFACT:** `public-release-preview/`, `PUBLIC-RELEASE-CONTENTS.md`,
  `PUBLIC-PREVIEW-LEAK-CHECK.md`, `scripts/validate_public_release_preview.py`,
  `review-bundle-r2.1/`, R2.1 ZIP.
- **STATUS:** CLOSED.

## P1-2 — formal_d_objective.py overwrote the manual loop audit

- **FINDING:** the script generated candidate rows, unconditionally set
  `confirmed_loop=no`, overwrote the audit CSV, then read back its own
  verdicts — making the "manual" verdicts machine-generated.
- **ROOT CAUSE:** candidate generation and manual-verdict consumption were the
  same code path; the audit file was treated as writable output.
- **FIX:** separated the two stages:
  - `--init-audit` (STAGE A): generates a candidate template only when the
    audit file is missing; verdicts are `UNREVIEWED`; refuses to overwrite an
    existing audit unless `--force-init-audit` is given.
  - normal run (STAGE B): **reads** the existing manual audit and **fails
    closed** on any candidate whose verdict is missing, duplicated, or not
    `yes`/`no`. The normal run **never writes** the audit file.
  - `clean_final = has_final AND not confirmed_loop AND not context_exhausted`
    with `confirmed_loop` taken only from the manual audit.
- **VALIDATION:** `test_formal_d_manual_audit.py` (production functions,
  synthetic JSONL): verdict `yes` preserved and clean_final subtracted (A),
  verdict `no` preserved (B), UNREVIEWED fails closed (C), missing row fails
  closed (D), duplicate row fails closed (E), **audit bytes unchanged after
  two aggregations (F)** — all PASS. Real run: 192 / 119 / 77 / 0 / 115 with
  the audit's SHA256 unchanged from the R2 source.
- **ARTIFACT:** `scripts/formal_d_objective.py`, `scripts/test_formal_d_manual_audit.py`,
  METHODOLOGY.md / REPRODUCIBILITY.md / DATA-DICTIONARY.md (audit workflow).
- **STATUS:** CLOSED.

## P1-3 — SECURITY-AND-PRIVACY.md contradicted Option B

- **FINDING:** the file claimed model-generated final answers are "published
  verbatim" in the initial release.
- **ROOT CAUSE:** stale full-data release language from the pre-Option-B
  drafts.
- **FIX:** rewrote the "Public release policy (OPTION B)" section: PUBLIC list
  (questions, docs, scripts, objective metrics, locked score artifacts/score
  data as allowed, aggregates, figures, provenance metadata) vs NOT IN INITIAL
  PUBLIC RELEASE (the two answer CSVs, reasoning content, private raw,
  credentials). The retained-answer datasets are described as internal /
  reviewer-archive only. Full-tree Option-B language audit: **0 stale
  full-data claims** (the only remaining "final answers only" hits are the
  blind-judge protocol wording, which is correct).
- **ARTIFACT:** SECURITY-AND-PRIVACY.md.
- **STATUS:** CLOSED.

## P3 — stale release metadata cleanup

- Removed "REVISION 1" marketing from README; REPORT status now lists the
  actual remaining items (maintainer project-license decision, documented F
  model-source limitation, final human review). F remains documented as a
  P2 reproducibility limitation, not a release blocker.
- RELEASE-READINESS.md regenerated to be evidence-based: preview-related
  statuses are PASS only because the directory, manifest, validator (PASS) and
  leak check (PASS) physically exist and ran.

## Residual (not blockers)

- PROJECT LICENSE: HUMAN DECISION REQUIRED (classes A/B/D).
- F acquisition source: NOT RECOVERED — documented P2.
- Final human review of R2.1 (including this response).
