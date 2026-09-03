# LICENSE NOTES — classification and upstream notes (Revision 2)

**Status: DECISION MADE (2026-09-01).** License files are now in place:
`LICENSE` (MIT — software/code) and `LICENSE-DOCS-DATA.md`
(CC BY 4.0 — documentation, benchmark questions, figures, and
project-derived evaluation data). Updated 2026-09-03 by the Output Dataset
Addendum: model-generated final answers for C/D/E/F are now released under
`data/model-answers/` as benchmark artifacts (NOT relicensed by this
project); A/B remain withheld pending additional upstream/output-terms
review. This document retains the content classification and recorded
upstream restrictions that informed the decisions.
No legal conclusions are asserted beyond what the linked sources state.

## Content classification (six classes)

| class | asset | known upstream restrictions / uncertainty |
|---|---|---|
| **A. Project-authored software** | `scripts/*.py`, tests | original work; no third-party code copied (verified). Calls llama.cpp's OpenAI-compatible API; contains no copied llama.cpp code. |
| **B. Project-authored benchmark questions / docs** | `data/questions-*.json`, all `.md` documentation | original question text authored for this project (2026-08-31). Original work. |
| **C. Model-generated final-answer text datasets** | `data/model-answers/` (per-model CSVs; since the 2026-09-03 Output Dataset Addendum) | outputs of the six models. **Partial release:** C/D/E/F answers (256) are released as benchmark artifacts and are NOT relicensed by this project (see data/model-answers/NOTICE.md). A/B answers (128) remain **withheld pending additional upstream/output-terms review**. The combined 6-model CSVs (`formal-{d,c}-answers-final-only.csv`) are superseded and must never be published (they would re-include the withheld A/B rows). |
| **D. Judge/project-derived evaluation data** | `data/formal-{d,c}-scores.csv`, `data/d-vs-c.csv`, `data/formal-{d,c}-objective.csv`, `data/formal-{d,c}-loop-audit.csv`, `blind/*-SCORES-LOCKED.md` (sanitized), `data/model-artifacts.csv` | produced by the project's blind-judge evaluation and post-run analysis — NOT model-generated text. Covered by the project's own data-license choice (PROJECT-LICENSE-DECISION.md), with attribution to the judge protocol. |
| **E. Third-party model metadata / upstream links** | MODEL-CARDS.md, MODEL-SOURCE-TODO.md, NOTICE.md | model identities and links belong to their respective authors (deadbydawn101, endystrike, HauhauCS, ornith-ai, mradermacher, codecraftersllc, nex-agi, bartowski, QwenLM). |
| **F. Third-party / adapted code** | none found | no third-party code was copied into the release scripts. |

## Important distinction (per R2 review)

**Class C (model-generated answer text) and class D (judge/project-derived
scores and aggregates) are different categories.** The score CSVs and locked
scorebooks are evaluation data produced by this project's blind-judge
protocol; they are not model outputs and are not subject to the model-output
redistribution uncertainty that gates class C.

## Recommended next step

- Classes A + B: one repository license chosen by the maintainer
  (PROJECT-LICENSE-DECISION.md lays out options) — **not applied here**.
- Class C: partially resolved by the 2026-09-03 Output Dataset Addendum —
  C/D/E/F released as not-relicensed benchmark artifacts; A/B still withheld
  pending additional upstream/output-terms review (no promise of release).
- Class D: covered by the project data-license choice; attribution to the
  judge protocol.
- Class E: attribution statements (NOTICE.md).

## Upstream verification TODO (status after the 2026-09-03 addendum)

1. ~~Read each of the six model cards / repo licenses~~ — DONE 2026-09-03 for
   the output-terms question: C/D/E/F reveal no term prohibiting publication
   of benchmark output; A and B retain additional upstream wording (A:
   research-purposes-only wording alongside the Apache-2.0 card label; B:
   AGPL-3.0 plus disclosed proprietary distillation lineage) and stay
   withheld pending additional review. Exact artifact hashes for B/D/F are
   recorded in data/model-answers/NOTICE.md.
2. Confirm whether the abliterated fine-tune cards permit derivative
   redistribution of their outputs — DONE for C/D/E/F to the extent needed
   for this partial release; A/B intentionally not pushed further.
3. ~~Choose the repository license for classes A+B~~ — DONE 2026-09-01
   (MIT + CC BY 4.0).
4. ~~Decide the data-license/statement for class D and any future class C
   release~~ — class D covered by CC BY 4.0; class C partially released
   2026-09-03 under the not-relicensed benchmark-artifact statement
   (data/model-answers/NOTICE.md).
