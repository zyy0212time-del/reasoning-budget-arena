# Response to Independent Pre-Publication Review — Revision 1

Reviewer verdict on the first public RC: **MAJOR REVISION REQUIRED**. This
document addresses every P1 (must-fix) and P2 (should-fix) finding. Where a
finding was correct we say so; where we partially disagree we give the artifact
evidence. The previous RC is preserved unmodified in
`release-candidate-pre-review-r1/`; all changes were made in
`release-candidate-r1/`.

## P1 findings

### P1-1. Core methodology wording ("two identical runs" / "exactly one intervention")
- **REVIEW FINDING:** The RC claimed the two conditions were "identical runs"
  or differed by "exactly one intervention", which the real execution history
  does not support (Formal D is a composite probe+supplement baseline; Formal C
  is one contiguous run).
- **ACTION:** Rewrote the core comparability statement across README, REPORT,
  METHODOLOGY, RESULTS, REPRODUCIBILITY. New canonical wording: the conditions
  used the same models, final frozen 32-question set, target 8192 context and
  closely matched settings; Formal C added the 4096 reasoning budget; the
  comparison is "exploratory and closely matched — not a strict single-variable
  controlled experiment". A phrase audit found and eliminated all residual
  occurrences.
- **FILES CHANGED:** README.md, REPORT.md, METHODOLOGY.md, RESULTS.md,
  REPRODUCIBILITY.md.
- **STATUS:** FIXED.

### P1-2. README first screen / title causal flavor
- **REVIEW FINDING:** Title "How a Fixed Reasoning Budget Changed …" and key-
  result language carried causal flavor.
- **ACTION:** Title changed to *Reasoning Budget Arena: Final-Answer Delivery
  and Ranking Differences Under Two Reasoning Policies*. Key-result bullets now
  say "observed under the two protocols"; the comparability caveat is on the
  first screen.
- **FILES CHANGED:** README.md (title, status, key results, experiment diagram,
  results table).
- **STATUS:** FIXED.

### P1-3. REPORT abstract / Formal D / Formal C / Comparison / Conclusion
- **REVIEW FINDING:** Same overclaiming in the technical report.
- **ACTION:** Rewrote Abstract, §6 (composite D disclosure), §8 (contiguous C),
  the comparison statements and Conclusion with the *observed under the two
  protocols* language. Strong observed results (119/192 → 192/192; score/rank
  changes) retained.
- **FILES CHANGED:** REPORT.md.
- **STATUS:** FIXED.

### P1-4. METHODOLOGY: Formal D baseline provenance + comparability
- **REVIEW FINDING:** No disclosure that D is composite.
- **ACTION:** Added §3 "Formal D baseline provenance (composite)" (29Q probe =
  174 responses; G1/G8/G10 supplement = 18; published 192; why the supplement
  exists; `source` column provenance) and §4 "Comparability and non-identity"
  (matched vs not-identical lists).
- **FILES CHANGED:** METHODOLOGY.md.
- **STATUS:** FIXED.

### P1-5. Public Formal C runner path contract
- **REVIEW FINDING:** `--rawdir raw/formal-c/<tag>` + `--outdir parent` can
  create `raw/raw/...`; and the division filename can mismatch
  (`A-questions-general.jsonl` vs `A-general-questions.jsonl`) when the
  questions file is named `data/questions-general.json`.
- **ACTION:** The reviewer was correct on the filename issue (the harness
  inferred the division from the basename). Added a **single canonical path
  contract**: `<root>/raw/formal-c/<tag>/<tag>-<div>-questions.jsonl`, enforced
  by an explicit `--div general|cyber` argument (never inferred), a shared
  `resolve_raw_path` helper, and the integrity checker reading the same
  contract. `--outdir` is now the experiment root with `--rawdir
  raw/formal-c/<tag>` (single join — no `raw/raw` possible).
- **FILES CHANGED:** scripts/arena_harness.py, scripts/run_formal_c.py,
  REPRODUCIBILITY.md, METHODOLOGY.md.
- **STATUS:** FIXED.

### P1-6. Runner clean-room smoke test
- **REVIEW FINDING:** Static inspection alone does not prove generation
  reproducibility.
- **ACTION:** Added `scripts/test_release_paths.py` — a clean-room test that
  verifies resolved output directories, filenames, question mapping, tag paths
  and integrity-checker discovery without running any model, plus
  `py_compile` on every script. All assertions PASS.
- **FILES CHANGED:** scripts/test_release_paths.py (new), REPRODUCIBILITY.md.
- **STATUS:** FIXED. (Scope: path-contract only; exact responses are not
  reproducible by design — stated in REPRODUCIBILITY.)

### P1-7. Harness max_tokens default discrepancy
- **REVIEW FINDING:** Doc implied 8192 but argparse default was 4096.
- **ACTION:** Chose explicit-config over hidden defaults: the standalone
  harness default is now **8192** and every reproduction command passes it
  explicitly anyway; REPRODUCIBILITY documents the exact values.
- **FILES CHANGED:** scripts/arena_harness.py (default), REPRODUCIBILITY.md.
- **STATUS:** FIXED. (P2 — bundled here.)

### P1-8. Formal D structural audit
- **REVIEW FINDING:** "D confirmed loops = 0" and "D clean = 115" had no public
  evidence.
- **ACTION:** Applied the **same loop-candidate detector** as Formal C to the
  exact D baseline sources (budget-probe-8192 + supplement, 192 IDs verified).
  Produced `data/formal-d-loop-audit.csv` (77 candidates: 73 empty-final — no
  content channel existed for a content loop — and 4 final-bearing candidates
  manually reviewed as truncated, non-repetitive answers; **0 confirmed
  loops**). Limitation recorded: D records lack `ctx/max_tokens`, so
  `near_generation_cap` is D-NOT-COMPUTABLE.
- **FILES CHANGED:** scripts/formal_d_objective.py (new), data/formal-d-
  objective.csv (schema expanded), data/formal-d-loop-audit.csv (new),
  METHODOLOGY.md §10, RESULTS.md, CLAIM-EVIDENCE-INDEX.md.
- **STATUS:** FIXED.

### P1-9. Formal D structurally-clean recomputation
- **REVIEW FINDING:** "Do not assume 115."
- **ACTION:** Recomputed with the exact public definition
  (has_final AND not confirmed loop AND not context-truncated) = **115/192**,
  matching the previously claimed value, now backed by the audit chain above.
- **STATUS:** FIXED (115/192 confirmed; evidence chain documented).

### P1-10. D/C objective schema documentation
- **REVIEW FINDING:** `formal-d-objective.csv` did not contain all fields
  attributed to it; D and C schemas were treated as identical.
- **ACTION:** DATA-DICTIONARY.md rewritten to document the two CSVs
  **separately** with per-field scope (`D only` / `C only` / `both` /
  D-NOT-COMPUTABLE). No field is claimed for a file that lacks it.
- **FILES CHANGED:** DATA-DICTIONARY.md.
- **STATUS:** FIXED.

### P1-11. CLAIM-EVIDENCE index correctness
- **REVIEW FINDING:** The `formal-{d,c}-objective.csv (clean_final)` claim was
  wrong for D (no clean_final column at the time).
- **ACTION:** Rebuilt the index so every claim points to a file that actually
  contains or derives it: D clean → formal-d-objective.csv + formal-d-loop-
  audit.csv + formal_d_objective.py; C clean → formal-c-objective.csv +
  formal-c-loop-audit.csv.
- **FILES CHANGED:** CLAIM-EVIDENCE-INDEX.md.
- **STATUS:** FIXED.

### P1-12. Current-fact verification artifact
- **REVIEW FINDING:** No documentation of evaluation-date-dependent questions.
- **ACTION:** Added `docs/CURRENT-FACT-REFERENCES.md`. G15 (Uranus moon count)
  and G16 (current Voyager status) identified from the locked scorebooks, which
  record the judge's evaluation-year reliance (e.g. Uranus = 29 in 2026) but
  **no source URLs or access timestamps** — those cells are marked NOT
  RECOVERABLE FROM ARCHIVED ARTIFACTS, and nothing is fabricated.
- **FILES CHANGED:** docs/CURRENT-FACT-REFERENCES.md (new), LIMITATIONS.md,
  METHODOLOGY.md.
- **STATUS:** FIXED (provenance partially unrecoverable — documented, not
  invented).

### P1-13. Model source provenance
- **REVIEW FINDING:** MODEL-SOURCE-TODO unresolved.
- **ACTION:** Verified primary sources for **A/B/C/D/E** (deadbydawn101 GGUF
  repo; endystrike model page; HauhauCS repo; ornith-ai base + abliterated
  GGUF suites; bartowski GGUF + nex-agi original). **F** base (QwenLM/Qwen3.8)
  recovered but its exact abliterated-25 GGUF repo is marked **SOURCE NOT
  RECOVERED** — no URL guessed.
- **FILES CHANGED:** MODEL-SOURCE-TODO.md (re-resolved), MODEL-CARDS.md,
  NOTICE.md, data/model-artifacts.csv.
- **STATUS:** FIXED (5/6 fully; F caveated).

### P1-14. GGUF hashes + model-file retirement safety
- **REVIEW FINDING:** Hashes must be recorded before storage cleanup.
- **ACTION:** Computed **SHA256 + exact sizes for all six local GGUFs**
  (6/6). Recorded in `data/model-artifacts.csv` and
  `MODEL-ARTIFACT-MANIFEST.md` (immutable, dated 2026-09-01). No file deleted
  in this task.
- **FILES CHANGED:** data/model-artifacts.csv (new), MODEL-ARTIFACT-MANIFEST.md
  (new).
- **STATUS:** FIXED.

### P1-15. License / provenance
- **REVIEW FINDING:** Licensing unclear; no NOTICE.
- **ACTION:** LICENSE-NOTES.md rewritten with content classification A–E,
  known upstream restrictions, a **split-licensing recommendation** (software
  + questions; model-output dataset; attribution for third-party names), and
  an upstream verification TODO. NOTICE.md added with the attribution table.
  No license file was applied unilaterally.
- **FILES CHANGED:** LICENSE-NOTES.md, NOTICE.md (new).
- **STATUS:** PARTIAL — LICENSE DECISION REQUIRED remains (human/legal), but
  classification and upstream-fact status are resolved as far as possible.

### P1-16. Runtime config evidence links
- **REVIEW FINDING:** METHODOLOGY cited RUNTIME-CONFIGS.md / MODEL-INVENTORY.md
  which were absent from the RC.
- **ACTION:** Chose option A: added sanitized `docs/runtime-evidence.md`
  (runtime, flags, per-model settings, fairness rules) and re-pointed all
  methodology citations to files that exist in the release.
- **FILES CHANGED:** docs/runtime-evidence.md (new), METHODOLOGY.md.
- **STATUS:** FIXED.

### P1-17. Formal D reproducibility (three stages)
- **REVIEW FINDING:** REPRODUCIBILITY implied D was one contiguous 32Q run.
- **ACTION:** Rewrote REPRODUCIBILITY with the actual three-stage composite
  reproduction (29Q probe → G1/G8/G10 supplement → assembly), including how to
  rebuild the stage question files from the frozen set. No fake identical
  sequencing.
- **FILES CHANGED:** REPRODUCIBILITY.md.
- **STATUS:** FIXED.

### P1-18. Formal C reproducibility after runner fix
- **REVIEW FINDING:** Verify the runner command.
- **ACTION:** Exact command documented; verified by the clean-room path test
  (P1-6). No models re-run.
- **STATUS:** FIXED.

### P1-19. Release-readiness wording
- **REVIEW FINDING:** "No technical/data blocker remains" was premature.
- **ACTION:** Removed; RELEASE-READINESS.md regenerated with accurate statuses
  (A–R), including the remaining license/source/human-review items.
- **FILES CHANGED:** RELEASE-READINESS.md.
- **STATUS:** FIXED.

## P2 findings

### P2-20. Nex selection-bias caveat
- **REVIEW FINDING:** "high delivered-answer average" needed a conditional-
  delivery caveat.
- **ACTION:** Added an explicit selection-bias caveat to REPORT §11.1 and
  RESULTS §4: delivered answers are conditional on delivery; Nex's 17 missing
  questions are not a random sample; the delivered-only average does not
  estimate latent quality on the missing questions. The observation is
  retained, its interpretation bounded.
- **FILES CHANGED:** REPORT.md, RESULTS.md.
- **STATUS:** FIXED.

### P2-21. Causal language audit
- **REVIEW FINDING:** Audit caused/changed/produced/eliminated/etc.
- **ACTION:** Ran a full-text audit across the r1 tree. All hits are
  negations ("not claims that the budget caused them"), explicit
  *consistent-with* statements, or mechanical/technical statements with code
  evidence (e.g. the path test "verifies"). One borderline "proves" softened
  to "verifies". Statistical language avoided throughout.
- **STATUS:** FIXED.

### P2-22. validate_scores claim scope
- **REVIEW FINDING:** The script validated less than the docs claimed.
- **ACTION:** Chose option A: the script now verifies the exact G1–G18/C1–C14
  set per model, exactly 18G/14C per model, six models, one-to-one revealed
  mapping (from METHODOLOGY + a canonical tag→model constant — no fragile
  markdown parsing), and **locked scorebook ↔ score-CSV exact question-total
  matching (192/192 both conditions)**.
- **FILES CHANGED:** scripts/validate_scores.py.
- **STATUS:** FIXED.

### P2-23. Loop-heuristic doc/code consistency
- **REVIEW FINDING:** METHODOLOGY said the candidate heuristic included
  reasoning markers, but the code's candidate expression does not.
- **ACTION:** Confirmed the implementation (candidate = near_context_limit OR
  dup10 ≥ 0.30 OR max_line_repeat ≥ 3; markers computed but not part of the
  candidate expression). METHODOLOGY §10 now describes the detector exactly as
  implemented in both objective scripts. Historical candidate classifications
  were not changed to match prose.
- **FILES CHANGED:** METHODOLOGY.md.
- **STATUS:** FIXED.

### P2-24. Blind audit language
- **REVIEW FINDING:** "independently proves"/"cryptographically verifies"
  language was too strong.
- **ACTION:** Standardized to "archived project artifacts record that scores
  were locked before identity reveal" — an author-recorded process audit
  trail, not cryptographic proof. Applied in README, METHODOLOGY, RELEASE-
  READINESS, CLAIM-EVIDENCE-INDEX.
- **FILES CHANGED:** README.md, METHODOLOGY.md, RELEASE-READINESS.md,
  CLAIM-EVIDENCE-INDEX.md.
- **STATUS:** FIXED.

### P2-25. Optional blind-package provenance
- **REVIEW FINDING:** Optional hashes/manifest for blind packages; no fake
  pre-lock history.
- **ACTION:** The sanitized locked scorebooks are already archived as evidence
  with lock markers; the chronology is documented as author-recorded. No
  hashes of the blind packages were available to add without risk of
  misrepresenting chronology, so no such hashes are claimed.
- **STATUS:** DECLINED-with-note (no fabricated provenance; documented as
  author-recorded).

## Summary

All P1 items are fixed; P2 items are fixed or explicitly declined with
reasoning. The remaining human-facing items are LICENSE DECISION REQUIRED,
the single SOURCE NOT RECOVERED model variant (F), and reviewer re-read.
