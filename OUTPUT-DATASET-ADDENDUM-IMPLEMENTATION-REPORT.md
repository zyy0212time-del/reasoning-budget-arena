# OUTPUT DATASET ADDENDUM — IMPLEMENTATION REPORT

Date: 2026-09-03 · Status: **release-ready / review-ready (LOCAL ONLY — not
committed, not tagged, not pushed; awaiting the maintainer release gate)**

## Changes Made

Upgraded the repository from Option B (all 384 model final answers withheld)
to a **partial final-answer release**: C/D/E/F answers are now public under
`data/model-answers/` (256 answers); A/B remain withheld (128). No answer was
regenerated, re-scored, normalized or rewritten; no locked score, ranking,
rubric or mapping chronology was touched.

## Released Models

| key | model | answers released |
|---|---|---:|
| C | Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced | 64 |
| D | Ornith-1.5-35B-A3B-Abliterated | 64 |
| E | Nex-N2-mini | 64 |
| F | Qwen3.8-9B-abliterated-25 | 64 |

## Withheld Models

| key | model | reason (verbatim policy wording) |
|---|---|---|
| A | RavenX-CyberAgent-35B-v5.1 | withheld pending additional upstream/output-terms review (Apache-2.0 card label, but the card body adds research-purposes-only wording) |
| B | Endy-Qwen3.6-CyberSec-35B-A3B | withheld pending additional upstream/output-terms review (AGPL-3.0; card discloses proprietary-model distillation lineage) |

## Answer Counts

- Formal C released = 128 (4 × 32)
- Formal D released = 128 (4 × 32)
- Total released = **256**
- Withheld = **128**
- Original total = **384**

All counts are asserted programmatically (`scripts/build_model_answer_dataset.py
--verify-only` and the extended `scripts/validate_public_release_preview.py`).

## Provenance Verification

Method: HF `x-linked` LFS OIDs are SHA-256 of file content, so an OID match
against the frozen local artifact SHA-256 (`MODEL-ARTIFACT-MANIFEST.md`,
captured 2026-09-01) is an exact artifact match. Full table:
`data/model-answers/NOTICE.md`.

- **B** — exact GGUF repo located: `endystrike/Endy-Qwen3.6-CyberSec-35B-A3B-GGUF`
  (author's own repo; AGPL-3.0). File `Endy-Qwen3.6-CyberSec-35B-A3B-Q4_K_M.gguf`,
  21,713,462,496 B, remote LFS OID `ed118e77…315ae1` == frozen local SHA-256 →
  **RESOLVED**. Note: the original local file is no longer on disk (post-benchmark
  C-drive cleanup); the SHA-256 evidence is the frozen 2026-09-01 record. Despite
  provenance RESOLVED, B's **answers remain WITHHELD** (output-terms dimension).
- **D** — `PocketAiHub/Ornith-1.5-35B-A3B-Abliterated-GGUF` (MIT).
  `Ornith-1.5-35B-A3B-Abliterated-Q4_K_M.gguf`, 21,166,757,664 B; local file
  still on disk with matching size; remote LFS OID `a07f299e…ed3d0` == frozen
  local SHA-256 → **RESOLVED** (full verification).
- **F** — `MegaPanchamZ/Qwen3.8-9B-abliterated-25-GGUF` (Apache-2.0).
  `Qwen3.8-9B-abliterated-25.Q4_K_M.gguf`, 5,629,108,864 B, remote LFS OID
  `542d41f6…894cf` == frozen local SHA-256 → **RESOLVED** (hash match; local
  file no longer on disk, frozen-record evidence). This replaces the previous
  "SOURCE NOT RECOVERED" status.
- **C / E / A** — keep their existing provenance records; license labels were
  re-checked from live model cards (C: gemma; E: apache-2.0; A: apache-2.0
  label + body wording) and recorded in `data/model-artifacts.csv`.

No RESOLVED claim is made anywhere without the exact-hash evidence above.

## Licensing Treatment

- Model-generated final-answer texts are reproduced as **benchmark/evaluation
  artifacts**. The project makes **no ownership or relicensing claim** over the
  model-generated text; it is covered by neither the MIT code license nor the
  CC BY 4.0 grant (`LICENSE-DOCS-DATA.md` rewritten accordingly).
- Project-authored code remains MIT; documentation, questions, figures and
  judge-derived evaluation data remain CC BY 4.0.
- The previous blanket "model-generated final-answer datasets: not included"
  statements were replaced everywhere; historical decision records
  (OUTPUT-REDISTRIBUTION-DECISION.md, REVIEW-RESPONSE-*.md,
  PROJECT-LICENSE-DECISION.md) are preserved unmodified with explicit
  historical/superseded banners.
- `data/model-answers/NOTICE.md` carries the full rights statement;
  `PUBLIC-RELEASE-CONTENTS.md` introduces class `M` (model-generated artifact,
  not relicensed) so no blanket license statement can be read as covering the
  model text.

## Traceability Validation

question → answer → locked question-level score → aggregation:

- IDs aligned with `data/questions-general.json` / `questions-cyber.json` per
  division (G1–G18 / C1–C14), no duplicates, none missing (validated).
- Every released (model, condition, question_id) row has a corresponding row
  in the locked `data/formal-{c,d}-scores.csv` (validated; no scores recomputed).
- Model labels in the dataset are **post-lock identity mapping / release
  metadata** — stated explicitly in `data/model-answers/NOTICE.md` and the
  README so no reader mistakes them for judge-visible identities.
- PASS: `build_model_answer_dataset.py --verify-only`.

## Privacy Validation

**PASS.**

- Generic scan (paths, tokens, keys, cookies, reasoning-channel filename
  detection): clean across the whole release tree (validator).
- Private denylist scan (machine-specific values: username, local project
  roots, internal tooling names — pattern file kept OUTSIDE the repository):
  zero hits.
- Answer-content scan: 1 hit in 384 answers, reviewed and anchored as
  **reviewed-FP-1** (`C-gemma4/formal-c.csv`, question C3 — the model's own
  teaching example of a dummy placeholder credential; the answer's topic is
  credential-scanner false positives). Kept byte-identical; the validator
  anchors the exception by SHA-256 of the exact matched substring and fails
  closed on any new, unlisted hit.
- The dataset contains final-answer text only — no reasoning content,
  telemetry, local paths, or pre-lock identity metadata.

## Files Added

- `data/model-answers/C-gemma4/{formal-c,formal-d}.csv`
- `data/model-answers/D-ornith/{formal-c,formal-d}.csv`
- `data/model-answers/E-nex/{formal-c,formal-d}.csv`
- `data/model-answers/F-qwen3.8/{formal-c,formal-d}.csv`
- `data/model-answers/NOTICE.md`
- `data/model-answers/MANIFEST.md`
- `scripts/build_model_answer_dataset.py`
- `OUTPUT-DATASET-ADDENDUM-IMPLEMENTATION-REPORT.md` (this file)

## Files Modified

- `README.md` — Final-answer dataset section; Data + License sections;
  status header
- `PUBLIC-RELEASE-CONTENTS.md` — INCLUDED (11 new entries, class `M`
  legend), EXCLUDED (A/B + superseded combined CSVs), RELEASE POLICY
- `LICENSE-DOCS-DATA.md`, `LICENSE-NOTES.md`, `PROJECT-LICENSE-DECISION.md`,
  `NOTICE.md` — licensing treatment updated, upstream labels re-checked
- `MODEL-SOURCE-TODO.md`, `MODEL-CARDS.md`, `data/model-artifacts.csv` —
  B/D/F provenance → RESOLVED with hash evidence; `present` column
  re-checked (A/B/F artifacts no longer on disk)
- `DATA-DICTIONARY.md` — dataset schema section rewritten for the split
- `OUTPUT-REDISTRIBUTION-DECISION.md`, `REVIEW-RESPONSE-R{1,2,2.1,2.1.1}.md`,
  `SECURITY-AND-PRIVACY.md`, `extensions/huihui…/README.md` — historical
  records preserved with superseded banners; current sections updated
- `scripts/validate_public_release_preview.py` — extended for the partial
  release (counts/schema/A-B absence/reviewed-FP anchors/doc consistency);
  default target is now the repository root
- `scripts/test_public_scanner.py` — fixed a pre-existing wrong EXPROOT path
  assumption in the publish tree; TEST F excludes released answer CSVs
  (governed by the validator's anchored reviewed-FP policy)

## Files Removed

None. (The combined 6-model CSVs were never part of this repository and are
now additionally guarded against by the validator.)

## Git Status

- 19 modified files (documents + 2 validation scripts) — see
  `git diff --stat`: 478 insertions(+), 136 deletions(-)
- 2 new untracked paths: `data/model-answers/`, `scripts/build_model_answer_dataset.py`
  (plus this report)
- **Locked artifacts untouched** (confirmed absent from the diff):
  `data/formal-{c,d}-scores.csv`, `data/d-vs-c.csv`, `data/formal-{c,d}-objective.csv`,
  `data/formal-{c,d}-loop-audit.csv`, `blind/*`, `extensions/*/…SCORES-LOCKED.md`
- Not committed (per instruction); no tag; no push; no GitHub Release.

## Remaining Blockers

None blocking local release readiness. A/B withholding is a deliberate
policy decision, not a blocker, and carries no promise of future release.

Suggested (not executed) next steps for the maintainer gate:
1. Review `git diff` and this report.
2. Local commit, e.g. `v1.1.0 — Partial Final-Answer Dataset Release`.
3. Push / tag / GitHub Release only after your own review.
