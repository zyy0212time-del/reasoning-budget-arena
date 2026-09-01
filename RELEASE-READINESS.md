# RELEASE READINESS — REVISION 2.1.1 (final publication pass)

Generated: 2026-09-01 (R2.1.1). Final status: **READY TO PUBLISH**.
The maintainer's project-license decision is recorded (2026-09-01); the
independent final-gate review concluded P0 = 0, P1 = 0.

Every PASS below corresponds to an artifact that physically exists in R2.1 and
to a validation that actually ran (no claimed-by-prose statuses).

| # | check | evidence in R2.1 | status |
|---|---|---|---|
| A | RAW EXPERIMENT DATA | `scripts/formal_d_objective.py` (192 assembly from historical archive), `scripts/formal_c_objective.py` | **PASS** — D 192 (29+3), C 192; exact frozen IDs; 0 retries. |
| B | D RESULTS VERIFIED | `scripts/validate_scores.py` scorebook↔CSV cross-check | **PASS** — 192/192 exact; aggregation match 6/6. |
| C | C RESULTS VERIFIED | same | **PASS** — 192/192 exact. |
| D | MASTER TABLE VERIFIED | `data/d-vs-c.csv` + `validate_scores.py` (question set, 18G/14C, 6 models, mapping, scorebook) | **PASS**. |
| E | BLIND PROTOCOL DOCUMENTED | `blind/`, METHODOLOGY §9 | **PASS** — author-recorded audit trail wording. |
| F | REASONING CONTENT EXCLUDED | leak scans | **PASS** — 0 content leaks. |
| G | PRIVATE PATHS REMOVED | leak scans | **PASS** — 0. |
| H | QUESTIONS INCLUDED | `data/questions-*.json` (final + D stage subsets) | **PASS**. |
| I | FORMAL D REPRODUCTION CONTRACT | `scripts/test_formal_d_release_contract.py` (PASS), `formal_d_objective.py` dual-layout | **PASS**. |
| J | FORMAL C PATH CONTRACT | `scripts/test_release_paths.py` (PASS) | **PASS**. |
| K | D STRUCTURAL AUDIT (manual-audit truth) | `data/formal-d-loop-audit.csv` (SHA256 unchanged from R2 source), `scripts/test_formal_d_manual_audit.py` (A–F PASS) | **PASS** — 192 / 119 / 77 / 0 / 115 from pipeline. |
| L | DATA DICTIONARY / SCHEMA | `DATA-DICTIONARY.md` column-by-column vs real headers | **PASS**. |
| M | DEAD EVIDENCE REFERENCES | link scan + plain-text ref scan | **PASS** — 0 dead refs (all runtime-config citations point to `docs/runtime-evidence.md`). |
| N | REPORT CAUSAL RESIDUE | full-text causal audit | **PASS** — 0. |
| O | BLIND AUDIT WORDING | CLAIM-EVIDENCE-INDEX.md, METHODOLOGY §9 | **PASS** — no in-bundle independence claim. |
| P | MODEL ARTIFACT IDENTITY | MODEL-ARTIFACT-MANIFEST.md, data/model-artifacts.csv | **PASS** — 6/6 (filename, size, SHA256, quant). |
| Q | MODEL ACQUISITION PROVENANCE | MODEL-SOURCE-TODO.md | **PARTIAL (honest)** — A/C/E resolved; B/D uploader not pinned; F NOT RECOVERED (documented P2, not a blocker). |
| R | CURRENT-FACT REFERENCES | docs/CURRENT-FACT-REFERENCES.md | **PARTIAL (honest)** — G15/G16 identified; original URLs/timestamps NOT RECOVERABLE; dates fixed. |
| S | LICENSE CLASSIFICATION | LICENSE-NOTES.md (classes A–F; C vs D split) | **PASS**. |
| T | OUTPUT REDISTRIBUTION | OUTPUT-REDISTRIBUTION-DECISION.md (Option B) | **PASS** — answer datasets excluded from public release; internal copies not deleted. |
| U | PROJECT LICENSE | PROJECT-LICENSE-DECISION.md (DECISION MADE 2026-09-01), LICENSE (MIT), LICENSE-DOCS-DATA.md (CC BY 4.0) | **RESOLVED** — code: MIT; docs/questions/figures/project-derived evaluation data: CC BY 4.0; model answers: withheld. |
| V | PUBLIC RELEASE PREVIEW | `public-release-preview/` (real tree), `PUBLIC-RELEASE-CONTENTS.md`, `scripts/validate_public_release_preview.py` (**VALID**), `PUBLIC-PREVIEW-LEAK-CHECK.md` (**PASS**) | **PASS** — directory, manifest, validator and leak check all physically present and green. |
| W | REVIEWER BUNDLE | `review-bundle-r2.1/` + `REASONING-BUDGET-ARENA-RC-R2.1-FINAL-GATE.zip` (ZIP members programmatically verified) | **PASS** — preview + manifest + leak check inside; answer datasets only under `review-only/`. |

## Documented non-blocking limitations (P2)

- **MODEL ACQUISITION PROVENANCE** — F variant SOURCE NOT RECOVERED; B/D
  uploader not pinned (documented P2 reproducibility limitation).
- **CURRENT-FACT REFERENCES** — historical source URLs/timestamps for G15/G16
  not recoverable; dates fixed (docs/CURRENT-FACT-REFERENCES.md).
- **FINAL ANSWER DATASETS** — withheld from initial public release (OPTION B);
  internal copies are not deleted.

These are non-blocking and do not affect the publication gate.

## READY TO PUBLISH: **YES** (P0 = 0, P1 = 0)

Output-redistribution policy: **OPTION B** — report + scores + code, without
the model-generated final-answer dataset.

All engineering, verification, and packaging work is complete and
machine-checked. The publication action (GitHub public repository
`reasoning-budget-arena`) is executed in the final publication pass.
