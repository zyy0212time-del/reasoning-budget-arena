# Model-Answers Dataset — Partial Final-Answer Release

Part of the **Output Dataset Addendum** (draft `v1.1.0 — Partial Final-Answer
Dataset Release`; not yet tagged — pending maintainer release gate).
Date of this addendum: 2026-09-03.

## What is released here

`data/model-answers/` contains **verbatim final-answer texts** for 4 of the 6
benchmark models, split per model and per formal condition:

| directory | model | `formal-c.csv` | `formal-d.csv` | total |
|---|---|---:|---:|---:|
| `C-gemma4/` | Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced | 32 | 32 | 64 |
| `D-ornith/` | Ornith-1.5-35B-A3B-Abliterated | 32 | 32 | 64 |
| `E-nex/` | Nex-N2-mini | 32 | 32 | 64 |
| `F-qwen3.8/` | Qwen3.8-9B-abliterated-25 | 32 | 32 | 64 |
| **released total (original six-model field)** | | **128** | **128** | **256** |
| `G-huihui-nex/` | Huihui-Nex-N2-mini-abliterated-Q4_K_M — **post-release extension** | 32 | not run | 32 |
| `H-ornith-0xkitkat/` | Ornith-1.5-35B-A3B-Uncensored-Q4_K_M — **post-release extension** | 32 | not run | 32 |
| `I-mimo-v26-9b-abliterated-q4/` | MiMo-V2.6-Distill-Qwen-9B-Abliterated-Q4_K_M — **post-release extension** | 32 | not run | 32 |
| **repository total (public)** | | **192** | **128** | **352** |

**Withheld — not present anywhere in this repository:**

| model | status |
|---|---|
| A — RavenX-CyberAgent-35B-v5.1 | withheld pending additional upstream/output-terms review |
| B — Endy-Qwen3.6-CyberSec-35B-A3B | withheld pending additional upstream/output-terms review |

The benchmark grand total is unchanged: 6 models × 32 questions × 2 formal
conditions = **384 answers = 256 released + 128 withheld**. No statement in
this repository should be read as a promise that A/B will be released later.

### Separate scope — post-release extensions

Three post-release extension directories hold **32 further final answers each**
(96 in total), evaluated under the identical frozen Formal C protocol **after**
the original release:

| directory | extension opaque id | status |
|---|---|---|
| `G-huihui-nex/` | `LR37` | scores locked before identity reveal |
| `H-ornith-0xkitkat/` | `ZD74` | scores locked before identity reveal |
| `I-mimo-v26-9b-abliterated-q4/` | `TM91` | scores locked before identity reveal |

This is a **separate scope**:

- it is **not** part of the original 384-answer six-model field
- it has **no Formal D answers** (each extension ran Formal C only)
- each locked extension scorebook is untouched by this answer release
- none of the three is a contestant of the original field and none is ranked
  against it in the frozen ranking

Repository-level public coverage is therefore **352 answers** (256 original
field + 96 extension), with **128 still withheld** (A/B). It must not be read
as "9 models × 32 × 2".

## Why partial

The original public release (Option B) withheld all 384 final answers because
output-redistribution terms of several community fine-tunes were unverified —
not because of any content-safety finding in the answers themselves. For this
addendum the per-model upstream/output-terms review was completed: C/D/E/F
revealed no terms prohibiting publication of benchmark output, while A/B
retain additional upstream wording that has not been cleared. A/B answers
remain withheld as a conservative measure.

## Rights — model-generated text is NOT relicensed by this project

Model-generated final-answer texts are reproduced as **benchmark/evaluation
artifacts**. No ownership or relicensing claim is made over the
model-generated text itself. Model names, provenance, and upstream license
information are provided per model (see `MANIFEST.md`). Dataset structure,
annotations, scores, metadata, and project-authored analysis remain covered by
the project's stated licenses where applicable (MIT for code, CC BY 4.0 for
project-authored documentation and evaluation data — see the repository
`LICENSE`, `LICENSE-DOCS-DATA.md`, and `LICENSE-NOTES.md`).

## Schema

Identical to the frozen final-only dataset (one CSV per model per condition):

```
condition,model,division,question_id,question,final_answer
```

- `condition` — `formal-c` or `formal-d`
- `model` — exact model artifact name used across all frozen benchmark
  artifacts (post-lock release metadata; see chronology below)
- `division` — `general` or `cyber`
- `question_id` — `G1..G18` / `C1..C14`, aligned with `data/questions-*.json`
  and the locked score CSVs
- `question` — the frozen question text (duplicate of the public question
  files, kept for stand-alone readability)
- `final_answer` — the model's verbatim final answer

## Blind-scoring chronology — read this before citing

All scores were assigned and locked **before** the contestant→model identity
mapping was revealed (`blind/FORMAL-{C,D}-BLIND-SCORES-LOCKED.md`). The
`model` column in these CSVs is **post-lock identity mapping / release
metadata**. The judge did not know model identities at scoring time; nothing
in this dataset changes that. The same holds for the extension datasets: their
scores were locked under the opaque ids `LR37`, `ZD74` and `TM91` before
identity reveal (`extensions/*/FORMAL-C-EXTENSION-BLIND-SCORES-LOCKED.md`), so
the `model` value in each extension CSV is post-lock release metadata too.

## What is NOT in these files

- no reasoning content, hidden chain-of-thought, scratchpad, raw sampler
  internals, or runtime telemetry — final-answer text only
- no regeneration, re-scoring, or rewriting: answer text is byte-identical to
  the frozen generation artifacts
- no local machine paths, usernames, credentials, or private endpoints

## Source and integrity

The rows were extracted from the internal frozen final-only CSVs
(192 rows each, 6 models). All ten archived copies of the Formal C source are
byte-identical (SHA-256 `354149aff19a6d13…`, full value recorded in the
internal build log); the Formal D source likewise. A/B rows were never
extracted into this repository. The extraction tool is
`scripts/build_model_answer_dataset.py` (per-row privacy scan + byte-level
round-trip verification + locked-score linkage check).

The extension answers come from a different frozen artifact shape: the
extension generation JSONL (18 general + 14 cyber), which carries both a
`response` field (the final answer) and a `reasoning` field (hidden
chain-of-thought). **Only `response` is released** — the `reasoning` field is
never written to any public file.

| extension | extraction tool | answer source |
|---|---|---|
| G — Huihui Nex | `scripts/build_extension_answer_dataset.py` | extension generation JSONL |
| H — Ornith-0xKitkat | `scripts/build_ornith_extension_answer_dataset.py` | extension generation JSONL |
| I — MiMo-V2.6 | `scripts/build_mimo_extension_answer_dataset.py` | **frozen blind answer package** (digest-pinned), because the general-division raw JSONL of that run was destroyed by an unrequested second generation pass *after* the score lock |

For the MiMo extension the builder accepts `--source-blind` only when the file
SHA-256 equals the recorded frozen digest
`787ae6806d69134f0a139353fce5d618f2435b25a7721da25a8b580b23a5f4af`; the package
is the artifact the judge scored and was verified byte-identical (32/32) to the
raw `response` fields before the loss. All three tools apply the same per-row
privacy scan, byte-level round-trip, frozen-question and locked-scorebook
alignment checks.

## Provenance verification (exact artifact level, checked 2026-09-03)

HF `x-linked` LFS OIDs are SHA-256 of file content, so an OID match against
the frozen local artifact SHA-256 (`MODEL-ARTIFACT-MANIFEST.md`, captured
2026-09-01) is an exact artifact match.

| model | local benchmark file | local bytes | frozen local SHA-256 | remote artifact (exact file) | remote LFS OID / size | status |
|---|---|---:|---|---|---|---|
| B | `Endy-Qwen3.6-CyberSec-35B-A3B-Q4_K_M.gguf` | 21713462496 | `ed118e7768330eb440ddc8ade42a04005ecab37f131d7e84bb08d14d1e315ae1` | `endystrike/Endy-Qwen3.6-CyberSec-35B-A3B-GGUF` | `ed118e77…315ae1` / 21713462496 | **RESOLVED via frozen benchmark SHA-256 record** (2026-09-01; original local file no longer on disk — NOT a fresh re-hash; remote LFS OID + size match) |
| D | `Ornith-1.5-35B-A3B-Abliterated-Q4_K_M.gguf` | 21166757664 | `a07f299e83a398b5078c1cb8ab4ec96333c8ea9d10d0cb479cb073056fedd3d0` | `PocketAiHub/Ornith-1.5-35B-A3B-Abliterated-GGUF` | `a07f299e…73056fedd3d0` / 21166757664 | **RESOLVED** (full verification: local file present, size match, frozen SHA == remote LFS OID) |
| F | `Qwen3.8-9B-abliterated-25.Q4_K_M.gguf` | 5629108864 | `542d41f6cf4cc450152651d0d8099bd4856f919f1a8909c3037976480cb894cf` | `MegaPanchamZ/Qwen3.8-9B-abliterated-25-GGUF` | `542d41f6…6480cb894cf` / 5629108864 | **RESOLVED via frozen benchmark SHA-256 record** (2026-09-01; original local file no longer on disk — NOT a fresh re-hash; remote LFS OID + size match) |

C and E keep their existing provenance records (`MODEL-SOURCE-TODO.md`,
`data/model-artifacts.csv`); this addendum adds no new claim for them.

## Reviewed false positives (answer text kept byte-identical)

- **reviewed-FP-1** — `C-gemma4/formal-c.csv`, question `C3`: the answer
  constructs a dummy placeholder credential as an inline teaching example;
  the answer's own topic is credential-scanner false positives. Reviewed
  2026-09-03, judged a benchmark artifact (not a real secret), and the answer
  text is kept byte-identical. The exemption is bound to the exact row
  identity (condition / model / question_id = `formal-c` / `C-gemma4` / `C3`)
  plus the scanner pattern id, the SHA-256 of the matched substring, and the
  SHA-256 of the full answer text; any other row, a second occurrence, or a
  single edited character fails closed.
- **Extensions (G-huihui-nex, H-ornith-0xkitkat, I-mimo-v26-9b-abliterated-q4)**
  — all 32 answers of each extension produced **zero** generic-pattern hits, so
  no waiver is registered for them and none is needed; the same
  row-identity-bound, fail-closed policy applies
  (`scripts/build_extension_answer_dataset.py`,
  `scripts/build_ornith_extension_answer_dataset.py`,
  `scripts/build_mimo_extension_answer_dataset.py`).
