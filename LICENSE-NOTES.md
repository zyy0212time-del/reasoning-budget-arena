# LICENSE NOTES — classification and upstream notes (Revision 2)

**Status: DECISION MADE (2026-09-01).** License files are now in place:
`LICENSE` (MIT — software/code) and `LICENSE-DOCS-DATA.md`
(CC BY 4.0 — documentation, benchmark questions, figures, and
project-derived evaluation data); the model-generated answer datasets are
withheld from the initial public release. This document retains the content
classification and recorded upstream restrictions that informed the decision.
No legal conclusions are asserted beyond what the linked sources state.

## Content classification (six classes)

| class | asset | known upstream restrictions / uncertainty |
|---|---|---|
| **A. Project-authored software** | `scripts/*.py`, tests | original work; no third-party code copied (verified). Calls llama.cpp's OpenAI-compatible API; contains no copied llama.cpp code. |
| **B. Project-authored benchmark questions / docs** | `data/questions-*.json`, all `.md` documentation | original question text authored for this project (2026-08-31). Original work. |
| **C. Model-generated final-answer text datasets** | `data/formal-{d,c}-answers-final-only.csv` | outputs of the six models. **EXCLUDED from the initial public release** pending upstream output-redistribution review (OUTPUT-REDISTRIBUTION-DECISION.md). Terms follow each model's upstream card; several are community abliterated fine-tunes whose output terms are UNCLEAR. |
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
- Class C: withheld from the initial release; a follow-up release or separate
  data license once each model card's output terms are verified.
- Class D: covered by the project data-license choice; attribution to the
  judge protocol.
- Class E: attribution statements (NOTICE.md).

## Upstream verification TODO (before any follow-up release of class C)

1. Read each of the six model cards / repo licenses (URLs in
   MODEL-SOURCE-TODO.md; F's exact variant repo is SOURCE NOT RECOVERED).
2. Confirm whether the abliterated fine-tune cards permit derivative
   redistribution of their outputs.
3. Choose the repository license for classes A+B.
4. Decide the data-license/statement for class D and any future class C
   release.
