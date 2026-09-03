# Response to Independent Pre-Publication Review — Revision 2 (final minor-fix pass)

> **Historical record.** This review response documents the state at its
> time, when all final answers were withheld (Option B). The 2026-09-03
> Output Dataset Addendum partially supersedes that decision — C/D/E/F
> final answers are now released under `data/model-answers/`; A/B remain
> withheld. The text below is preserved unmodified.


Second-round verdict: **READY AFTER MINOR FIXES**. This document responds to
every release-facing checklist item from the R2 review. Format per item:
REVIEW FINDING / ACTION / ARTIFACT / VALIDATION / STATUS / RESIDUAL LIMITATION.
No model inference was run; no locked score, mapping, or raw artifact was
changed; R1 is preserved unmodified in `release-candidate-pre-review-r1/`.

## 1. Formal D public reproduction contract (P1)
- **REVIEW FINDING:** REPRODUCIBILITY's Formal D raw layout disagreed with the
  layout `formal_d_objective.py` actually searched.
- **ACTION:** Refactored `formal_d_objective.py` to a single source of truth
  for path resolution, source discovery and assembly, supporting **both**
  (A) the historical archived layout (one probe file per tag containing all 29
  questions; supplement one file per tag) and (B) a public canonical layout
  (one file per tag/division), detected explicitly. Added frozen Stage-1
  question subsets derived from the final set (never hand-edited):
  `data/questions-formal-d-probe-general.json` (15 = final G-set minus
  G1/G8/G10), `questions-formal-d-probe-cyber.json` (14),
  `questions-formal-d-supplement-general.json` (3). Composition verified:
  15+14=29, +3, union 32, dups 0, missing 0.
- **ARTIFACT:** scripts/formal_d_objective.py, scripts/test_formal_d_release_contract.py,
  data/questions-formal-d-{probe-general,probe-cyber,supplement-general}.json,
  REPRODUCIBILITY.md §Formal D.
- **VALIDATION:** `test_formal_d_release_contract.py` — canonical assembly
  (192, 32 ids), historical assembly (192), rejection of duplicate / missing /
  unexpected records, no `raw/raw`, empty-root detection — **all PASS**;
  real historical archive assembles 192 via layout=historical.
- **STATUS:** FIXED.

## 2. Choose one canonical D release contract
- **ACTION:** Canonical public layout defined (`<root>/raw/budget-probe-8192/
  <tag>/<tag>-<div>-questions.jsonl`; supplement under `raw/formal-d-supplement/`),
  with explicit detection of the historical layout. Stage 1 is strictly the
  29-question set — the public canonical path never runs the full 18 General
  then supplements duplicates.
- **STATUS:** FIXED.

## 3. Historical vs reproduction sequencing
- **ACTION:** REPRODUCIBILITY now states the historical probe was executed as
  the archived 29-question union; the public canonical reproduction may store
  General/Cyber outputs separately while preserving the same 29+3 composition,
  and **does not reproduce the exact historical request sequence**. The
  phrase "exact historical sequencing" is not used for the reproduction path.
- **STATUS:** FIXED.

## 4. Formal D assembler strictness
- **ACTION:** `assemble_d_baseline` enforces exact expected ID sets per stage,
  per-source provenance, duplicate rejection, missing-record rejection, and
  unexpected-record (incl. unexpected supplement) rejection; final count must
  be exactly 192. Never silently mixes duplicate sources.
- **VALIDATION:** rejection cases tested with synthetic JSONL (dup / missing /
  unexpected) — PASS.
- **STATUS:** FIXED.

## 5. Formal D path-contract test
- **ACTION:** `test_formal_d_release_contract.py` exercises the **actual
  production functions** (path resolution, discovery, assembly, verification)
  from `formal_d_objective.py` with mock synthetic JSONL — no re-implemented
  formulas. Covers canonical paths, supplement paths, 29+3 composition,
  duplicate/missing/unexpected rejection, no `raw/raw`, final exact ID set.
- **STATUS:** FIXED.

## 6. D clean_final implementation hygiene
- **REVIEW FINDING:** `clean_final` was approximated as `has_final AND not cx`
  (valid only because D confirmed loops = 0).
- **ACTION:** `formal_d_objective.py` now computes `clean_final` as
  `has_final AND not confirmed_loop AND not context_exhausted`, where
  `confirmed_loop` is **joined from `data/formal-d-loop-audit.csv`** manual
  verdicts — never hardcoded.
- **VALIDATION:** recomputed: confirmed loops **0**, clean finals **115/192**.
- **STATUS:** FIXED.

## 7. DATA-DICTIONARY vs actual CSV headers
- **REVIEW FINDING:** DATA-DICTIONARY claimed `reasoning_chars`/`final_chars`
  in the C objective CSV (not present) and described D's `near_generation_cap`
  as absent (it is present as a sentinel).
- **ACTION:** Rewrote DATA-DICTIONARY column-by-column against the real
  headers (checked at R2): C has no reasoning_chars/final_chars; D's
  `near_generation_cap` is documented as a **present explicit
  `D-NOT-COMPUTABLE` sentinel** because archived D records lack the inputs.
- **ARTIFACT:** DATA-DICTIONARY.md.
- **VALIDATION:** headers re-read from the CSVs and matched to the doc.
- **STATUS:** FIXED.

## 8. Runtime evidence references
- **REVIEW FINDING:** METHODOLOGY still cited RUNTIME-CONFIGS.md.
- **ACTION:** All 4 METHODOLOGY table citations replaced with
  `docs/runtime-evidence.md`; full-tree scan: **0** dead RUNTIME-CONFIGS /
  MODEL-INVENTORY evidence references (R1 response narrative retains the
  historical mention of the finding, which is not an evidence citation).
- **STATUS:** FIXED.

## 9. REPORT subtitle causal residue
- **ACTION:** Subtitle changed to *"Final-answer delivery, structural
  failures, and ranking differences under two reasoning policies (native vs
  fixed reasoning-budget) across six local LLMs."*
- **STATUS:** FIXED (descriptive/comparative).

## 10. CLAIM-EVIDENCE blind wording
- **REVIEW FINDING:** "verified against sealed mapping artifacts" overstated
  what the public bundle contains.
- **ACTION:** Replaced with: *archived project artifacts record the mapping
  and lock-before-reveal chronology; the public sanitized score artifacts are
  consistent with that record; the sealed original mapping file is not in this
  bundle, so the public bundle does not independently prove the chronology.*
- **STATUS:** FIXED.

## 11. Model provenance: artifact identity vs acquisition
- **ACTION:** All provenance docs now separate:
  **ARTIFACT IDENTITY (6/6 strong** — filename, byte size, SHA256,
  quantization) from **ARTIFACT ACQUISITION PROVENANCE (partial)** — A/C/E
  resolved; B/D uploader not pinned; F variant SOURCE NOT RECOVERED. The
  "5/6 exact GGUF provenance fully resolved" phrasing was removed.
- **ARTIFACT:** MODEL-SOURCE-TODO.md, MODEL-CARDS.md, MODEL-ARTIFACT-MANIFEST.md,
  RELEASE-READINESS.md.
- **STATUS:** FIXED.

## 12. MODEL-ARTIFACT-MANIFEST stale source column
- **ACTION:** Added an explicit note that the manifest's `source` column is
  **hash-capture-time state** (2026-09-01, immutable) and that current
  provenance is in MODEL-SOURCE-TODO.md / data/model-artifacts.csv.
- **STATUS:** FIXED.

## 13. F source status
- **ACTION:** F kept as: exact artifact identity KNOWN (hash/filename/size);
  exact acquisition source **SOURCE NOT RECOVERED** — no URL/uploader guessed.
  Documented as a P2 reproducibility limitation, not a release blocker.
- **STATUS:** FIXED (retained as documented limitation).

## 14. License classification (C vs D)
- **REVIEW FINDING:** score CSVs were mislabeled as model-generated outputs.
- **ACTION:** LICENSE-NOTES.md now has **six classes**: A software, B
  questions/docs, **C model-generated answer text**, **D judge/project-derived
  evaluation data** (scores, objective metrics, loop audits, locked scorebook
  exports, hashes), E third-party metadata, F third-party code (none). C and D
  are never conflated.
- **STATUS:** FIXED.

## 15. Human license / output decision
- **ACTION:** Primary sources checked for the six models' base licenses
  (Qwen3.x Apache-2.0; Gemma 4 Gemma license; Ornith MIT per secondary
  reference — verify card). Fine-tune output-redistribution terms: **UNCLEAR**
  for most. `OUTPUT-REDISTRIBUTION-DECISION.md` defines two options and selects
  **OPTION B** for the initial release.
- **STATUS:** PARTIAL — decision reached for initial release (Option B);
  full verification remains for any follow-up answer-dataset release.

## 16. Do not delete internal answer data
- **ACTION:** Option B removes the two answer CSVs **only from the public
  release preview**; the internal experiment directory and private archival
  data are untouched and not deleted.
- **STATUS:** FIXED.

## 17. CURRENT-FACT date fix
- **ACTION:** `docs/CURRENT-FACT-REFERENCES.md` now states: the Formal D
  29-question probe **began 2026-08-31 and completed 2026-09-01**; the
  supplement and Formal C were run on 2026-09-01; archived judge artifacts
  relied on 2026-era facts with original URLs/timestamps NOT RECOVERABLE.
- **STATUS:** FIXED.

## 18. Current-fact remains a limitation
- **ACTION:** G15/G16 keep NOT RECOVERABLE for judge source URL/timestamp. No
  current web source is presented as the historical judge's evidence.
- **STATUS:** FIXED (limitation retained).

## 19. RELEASE-READINESS update
- **ACTION:** Regenerated with accurate statuses (A–W), including the D
  reproduction contract, model provenance split, F acquisition limitation,
  license/output decision, and the Option B inclusion/exclusion. With the
  uncertain output dataset excluded, the license item is re-scoped to the
  maintainer's choice for classes A/B/D rather than a whole-repo block.
- **STATUS:** FIXED.

## 20. Project license human choice prep
- **ACTION:** `PROJECT-LICENSE-DECISION.md` lists factual options for
  software, questions/docs, judge-derived data, and the separate answer-data
  path, with implications and compatibility concerns. **HUMAN DECISION
  REQUIRED** — nothing applied.
- **STATUS:** PARTIAL (by design — human decision).

## 21. Internal validation
- **ACTION:** Ran the full non-inference suite (see VALIDATION below) — all
  PASS.
- **STATUS:** PASS.

## Summary

All release-facing checklist items are closed or explicitly marked PARTIAL
with the residual limitation stated. No engineering blocker remains; the
remaining items are the human license decision, the documented F acquisition
limitation, and the final release-gate review.
