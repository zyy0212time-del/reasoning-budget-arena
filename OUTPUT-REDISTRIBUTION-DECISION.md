# OUTPUT REDISTRIBUTION DECISION

> **STATUS (2026-09-03): PARTIALLY SUPERSEDED by the Output Dataset
> Addendum.** The Option B decision below is retained as the historical
> record of the initial release. As of the addendum, the C/D/E/F final
> answers (256) are released under `data/model-answers/` as not-relicensed
> benchmark artifacts; the A/B answers (128) remain withheld under the same
> conservative standard this document established. Current status lives in
> `data/model-answers/NOTICE.md` and `data/model-answers/MANIFEST.md`.

Question: may the two **model-generated final-answer datasets**
(`data/formal-d-answers-final-only.csv`, `data/formal-c-answers-final-only.csv`)
be included in the initial public release?

## Per-model upstream status (checked 2026-09-01; from model pages / primary sources where located)

| model | base | base-model license | fine-tune/GGUF card license | output-redistribution language found? | explicit restriction? | status |
|---|---|---|---|---|---|---|
| A — RavenX-CyberAgent-35B-v5.1 | Qwen3.6-35B-A3B | Apache-2.0 (Qwen3 series terms) | not verified from archived artifacts / search snippets | none found | none found | **UNCLEAR** |
| B — Endy-Qwen3.6-CyberSec-35B-A3B | Qwen3.6-35B-A3B | Apache-2.0 (Qwen3 series terms) | not verified | none found | none found | **UNCLEAR** |
| C — Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced | google/gemma4 (QAT) | Gemma license (Google) | HauhauCS card license not verified | none found | none found | **UNCLEAR** |
| D — Ornith-1.5-35B-A3B-Abliterated | ornith-ai/Ornith-1.5-35B-A3B | MIT (per secondary reference; verify card) | abliterated GGUF suite cards not verified | none found | none found | **UNCLEAR** (base likely permissive) |
| E — Nex-N2-mini | nex-agi/Nex-N2-mini (post-trained on Qwen3.5-35B-A3B) | Qwen3.5 Apache-2.0 (base); Nex-N2-mini card terms not verified | bartowski GGUF card: quant only | none found | none found | **UNCLEAR** |
| F — Qwen3.8-9B-abliterated-25 | Qwen3.8-9B (QwenLM) | Apache-2.0 (Qwen3.8 series) | abliterated-25 GGUF repo SOURCE NOT RECOVERED | none found | none found | **UNCLEAR** (variant source unrecovered) |

Notes:
- Base-model licenses (Apache-2.0 for Qwen 3.x families, Gemma license for
  Gemma 4, MIT per secondary reference for Ornith) are the strongest facts
  recovered. None of the fine-tune/community cards' **output-redistribution
  terms** could be confirmed from the archived artifacts or today's searches.
- "No explicit restriction found" is NOT the same as "redistribution permitted";
  several of these are community abliterated fine-tunes whose cards may impose
  terms we did not verify.

## Decision — OPTION B: REPORT / SCORES / CODE RELEASE (initial public release)

Because at least one model's output-redistribution terms remain unclear, the
**initial public release excludes**:

- `data/formal-d-answers-final-only.csv`
- `data/formal-c-answers-final-only.csv`

and includes everything else: questions, objective metrics, locked score
artifacts, score CSVs (judge-derived data — class D, not model text), master
tables, figures, scripts, methodology.

The README will state explicitly: **the final-answer text dataset is withheld
pending upstream output-redistribution review.**

Rationale:
- A permissive guess about a community fine-tune's output terms is not a safe
  basis for a public data release.
- The answer CSVs are a small fraction of the project's value; withholding
  them does not block the rest of the release.

## Later options

- If the maintainer verifies each model card's output terms and concludes they
  permit redistribution, publish the answer CSVs in a follow-up release
  (OPTION A — FULL DATA RELEASE).
- Re-distribution of the answer dataset may also be gated behind a separate
  data license per LICENSE-NOTES.md.

## Unchanged by this decision

- The internal experiment directory and the private archival data are
  **not deleted**. The answer CSVs remain available internally and in the
  reviewer bundle (marked REVIEW ONLY).

## 2026-09-03 UPDATE — Output Dataset Addendum (partial release)

A completed per-model upstream/output-terms review (with exact artifact
hash verification for B/D/F on 2026-09-03; see data/model-answers/NOTICE.md)
resolved the question this decision was waiting on, per model:

| model | outcome |
|---|---|
| C — Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced | no term found prohibiting publication of benchmark output → **released** |
| D — Ornith-1.5-35B-A3B-Abliterated | MIT; no prohibition found; exact artifact hash match → **released** |
| E — Nex-N2-mini | Apache-2.0; no prohibition found → **released** |
| F — Qwen3.8-9B-abliterated-25 | Apache-2.0; exact variant repo recovered and hash-verified → **released** |
| A — RavenX-CyberAgent-35B-v5.1 | Apache-2.0 card label, but the model-card body adds research-purposes-only wording → **still withheld pending additional review** |
| B — Endy-Qwen3.6-CyberSec-35B-A3B | AGPL-3.0 plus disclosed proprietary-model distillation lineage; exact artifact hash match → **still withheld pending additional review** |

Result: **256 of 384 answers released** under `data/model-answers/`; **128
withheld**. This is neither the original OPTION B (all withheld) nor a full
OPTION A (all released). Model-generated answer text is reproduced as a
benchmark/evaluation artifact with no ownership or relicensing claim by this
project; A/B withholding carries no promise of future release.
