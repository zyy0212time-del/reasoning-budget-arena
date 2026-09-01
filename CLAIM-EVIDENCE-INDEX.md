# CLAIM → EVIDENCE INDEX (Revision 1)

Every primary claim points to a file that actually contains or derives it.
Reviewers should start at the primary evidence; supporting documents repeat
the numbers but are not the source. Note the D and C objective CSVs have
**different schemas** (DATA-DICTIONARY.md) — evidence paths below are
specific, not `{d,c}` shorthand where schemas differ.

| claim | primary evidence | supporting | validation |
|---|---|---|---|
| Formal D final delivery = 119/192 (61.98%), 73 empty | `data/formal-d-objective.csv` | `RESULTS.md` §1; `REPORT.md` §6 | `scripts/formal_d_objective.py` (recomputed from budget-probe-8192 + supplement) |
| Formal C final delivery = 192/192, 0 empty in this run | `data/formal-c-objective.csv` | `RESULTS.md` §1; `REPORT.md` §8 | `scripts/formal_c_objective.py` |
| structurally clean: D 115/192 | `data/formal-d-objective.csv` (`clean_final`) **+** `data/formal-d-loop-audit.csv` | `RESULTS.md` §4; `docs/FAILURE-MODE-ANALYSIS.md` | `scripts/formal_d_objective.py` (same detector, manual loop review) |
| structurally clean: C 184/192 | `data/formal-c-objective.csv` (`clean_final`) **+** `data/formal-c-loop-audit.csv` | `RESULTS.md` §4; `docs/FAILURE-MODE-ANALYSIS.md` | `scripts/formal_c_objective.py` |
| confirmed content-channel loops: C 6 (A/G4, B/C9, C/C9, F/C2, F/G3, F/G4) | `data/formal-c-loop-audit.csv` | `RESULTS.md` §5; `docs/FAILURE-MODE-ANALYSIS.md` | manual review of every candidate |
| confirmed content-channel loops: D 0 | `data/formal-d-loop-audit.csv` (77 candidates, 73 empty-final + 4 truncated non-loop, 0 confirmed) | `RESULTS.md` §5; `docs/FAILURE-MODE-ANALYSIS.md` | same detector as C; manual review of the 4 final-bearing candidates |
| context exhaustion: C 8 records, prompt+completion == 8192 | `data/formal-c-objective.csv` (`near_context_limit`) | `METHODOLOGY.md` §10; `RESULTS.md` §5 | recomputed; max completion 8093 < max_tokens |
| locked scores D (192 records, SCORES LOCKED) | `blind/FORMAL-D-BLIND-SCORES-LOCKED.md` | `data/formal-d-scores.csv` | `scripts/validate_scores.py` (recomputed, exact match vs artifact aggregation) |
| locked scores C (192 records, SCORES LOCKED) | `blind/FORMAL-C-BLIND-SCORES-LOCKED.md` | `data/formal-c-scores.csv` | `scripts/validate_scores.py` |
| blind lock before identity reveal | `blind/*-SCORES-LOCKED.md` (SCORES LOCKED marker + provenance header) | `METHODOLOGY.md` §9 | author-recorded audit trail, not cryptographic proof |
| mapping reveal (post-lock, one-to-one) | `METHODOLOGY.md` §9 (post-lock identity reveal) | `MODEL-CARDS.md` | archived project artifacts record the mapping and lock-before-reveal chronology; the public sanitized score artifacts are consistent with that record. The sealed original mapping file is NOT included in this bundle, so the public bundle does not independently prove the chronology. |
| master D-vs-C table (scores, deltas, ranks) | `data/d-vs-c.csv` | `RESULTS.md` §2; `REPORT.md` §11 | `scripts/validate_scores.py` (Gen+Cyber=Overall, 6×32, ranges) |
| General scores: D and C (each /450) | `data/formal-d-scores.csv` + `data/formal-c-scores.csv` | `RESULTS.md` §3 | recomputed from question-level locked scores |
| Cyber scores: D and C (each /350) | `data/formal-d-scores.csv` + `data/formal-c-scores.csv` | `RESULTS.md` §3 | recomputed from question-level locked scores |
| Overall scores and ranking (each /800) | `data/d-vs-c.csv` | `RESULTS.md` §2 | recomputed; matches artifact rankings exactly |
| rank changes (e.g. Nex #4 → #1) | `data/d-vs-c.csv` (`d_rank`,`c_rank`,`rank_change`) | `figures/rank-change.png` | `scripts/validate_scores.py` |
| score deltas (Nex +393.5, Qwen +302.5, RavenX +274.5) | `data/d-vs-c.csv` (`delta_*`) | `figures/score-delta.png`; `RESULTS.md` §2 | recomputed; C − D |
| Nex case study (delivery-limited under D; top under C) | `REPORT.md` §11.1 | `RESULTS.md` §2; `data/d-vs-c.csv` | delivery from objective CSVs; selection-bias caveat in REPORT §11.1 |
| Cyber-branded models not in Cyber top 3 in fixed-budget condition | `RESULTS.md` §3 (Cyber table) | `REPORT.md` §13 | from recomputed Cyber scores |
| frozen 32-question benchmark (18 General + 14 Cyber) | `data/questions-general.json`, `data/questions-cyber.json` | `METHODOLOGY.md` §7 | files are the exact sent prompts |
| per-model delivery under D (14/24/25/25/15/16) | `data/formal-d-objective.csv` | `RESULTS.md` §1 | recomputed |
| D composite baseline provenance (29Q + 3Q = 192) | `METHODOLOGY.md` §3 | `data/formal-d-objective.csv` (`source`) | assembly script `formal_d_objective.py` |
| figures (6 charts, SVG+PNG) | `figures/*.png` | `figures/*.svg` | `scripts/make_figures.py` reads verified CSVs only |
| model artifacts / SHA256 | `data/model-artifacts.csv`, `MODEL-ARTIFACT-MANIFEST.md` | `MODEL-CARDS.md` | SHA256 computed at R1 over the exact local files |
| no reasoning content published | whole bundle (scan) | `PUBLIC-LEAK-CHECK.md` | automated scans: 0 real findings |

## Numbers that must match everywhere

- Nex Formal C Overall: **746.5** (418.5 + 328.0), rank 1
- Ornith Formal D Overall: **569.5** (358.0 + 211.5), rank 1
- Delivery: **119/192** (D) vs **192/192** (C)
- Structurally clean: **115** (D) vs **184** (C)
- Confirmed loops: **0** (D) vs **6** (C)

All values use one decimal (half-point precision); a different rounding in any
document is a typo to flag, not a re-analysis.
