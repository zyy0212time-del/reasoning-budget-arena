# MANIFEST — data/model-answers/

Per-model release manifest for the Output Dataset Addendum (2026-09-03).
Counts below are asserted by `scripts/build_model_answer_dataset.py --verify-only`.

| key | model | Formal C | Formal D | total | release status | provenance status | upstream repo (exact artifact where verified) | upstream license (card) | output-terms review |
|---|---|---:|---:|---:|---|---|---|---|---|
| C | Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced | 32 | 32 | 64 | **RELEASED** | RESOLVED (existing record) | `HauhauCS/Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-MTP` | gemma (Google) | reviewed 2026-09-03 — no term found prohibiting publication of benchmark output |
| D | Ornith-1.5-35B-A3B-Abliterated | 32 | 32 | 64 | **RELEASED** | RESOLVED — local artifact present and size-verified on 2026-09-03; exact LFS-OID == frozen local SHA-256 | `PocketAiHub/Ornith-1.5-35B-A3B-Abliterated-GGUF` (file `Ornith-1.5-35B-A3B-Abliterated-Q4_K_M.gguf`) | mit | reviewed 2026-09-03 — MIT; no prohibition found |
| E | Nex-N2-mini | 32 | 32 | 64 | **RELEASED** | RESOLVED (existing record) | `bartowski/nex-agi_Nex-N2-mini-GGUF` (original: `nex-agi/Nex-N2-mini`) | apache-2.0 | reviewed 2026-09-03 — no prohibition found |
| F | Qwen3.8-9B-abliterated-25 | 32 | 32 | 64 | **RELEASED** | RESOLVED via frozen benchmark SHA-256 record (2026-09-01) — remote LFS-OID match | `MegaPanchamZ/Qwen3.8-9B-abliterated-25-GGUF` (file `Qwen3.8-9B-abliterated-25.Q4_K_M.gguf`) | apache-2.0 | reviewed 2026-09-03 — no prohibition found |
| **G** | **Huihui-Nex-N2-mini-abliterated-Q4_K_M** — post-release Formal C extension, **not** part of the original six-model field | 32 | N/A (Formal D not run) | 32 | **RELEASED** | RESOLVED per the extension's frozen revision + GGUF SHA-256 record (`22be29be…`, `8e38d2a0…`) | `quant-mind/Huihui-Nex-N2-mini-abliterated-GGUF` (lineage: `huihui-ai/Huihui-Nex-N2-mini-abliterated` → `nex-agi/Nex-N2-mini`) | apache-2.0 (all three cards, checked 2026-09-03) | reviewed 2026-09-03 — no term found prohibiting benchmark-output reproduction |
| A | RavenX-CyberAgent-35B-v5.1 | 0 | 0 | 0 | **WITHHELD** | RESOLVED (existing record) | `deadbydawn101/RavenX-CyberAgent-Qwen3.6-35B-A3B-Opus-4.7-OpenMythos-Pentester-BugHunter-RATH-GGUF` | apache-2.0 card — model-card body adds research-purposes-only wording | **withheld pending additional upstream/output-terms review** |
| B | Endy-Qwen3.6-CyberSec-35B-A3B | 0 | 0 | 0 | **WITHHELD** | RESOLVED via frozen benchmark SHA-256 record (2026-09-01) — remote LFS-OID match | `endystrike/Endy-Qwen3.6-CyberSec-35B-A3B-GGUF` (file `Endy-Qwen3.6-CyberSec-35B-A3B-Q4_K_M.gguf`) | agpl-3.0 — card discloses proprietary-model distillation lineage | **withheld pending additional upstream/output-terms review** |

## Totals — original six-model field

| | Formal C | Formal D | total |
|---|---:|---:|---:|
| released (C + D + E + F) | 128 | 128 | **256** |
| withheld (A + B) | 64 | 64 | **128** |
| **grand total** | **192** | **192** | **384** |

## Totals — post-release extension (separate scope)

| | Formal C | Formal D | total |
|---|---:|---:|---:|
| Huihui Nex extension (G) | 32 | not run | **32** |

## Repository-level answer coverage

| scope | public | withheld | total |
|---|---:|---:|---:|
| original six-model field | 256 | 128 | 384 |
| Huihui Formal C extension | 32 | 0 | 32 |
| **repository total** | **288** | **128** | **416** |

Huihui Nex is **not** a seventh contestant of the original field and has **no
Formal D answers** — the repository total must not be read as
"7 models × 32 × 2".

Notes:
- Provenance "RESOLVED" describes **artifact identity** (which upstream file
  the benchmark ran) — see `NOTICE.md` for the full hash table. It is
  distinct from the **output-terms review** that governs whether the answers
  are published. B is provenance-RESOLVED and still release-WITHHELD by
  design.
- Evidence levels differ by design: **D** was re-verified directly against
  the still-present local artifact on 2026-09-03; **B and F** are RESOLVED
  **via the frozen benchmark SHA-256 record (captured 2026-09-01)** matched
  against the remote LFS OID — the original local artifacts were removed in
  the post-benchmark cleanup and were NOT re-hashed in 2026-09-03.
- A/B withholding is a deliberate conservative decision, not a blocker, and
  carries no promise of future release.
- The post-release Huihui Nex extension is a **separate scope**: its 32 Formal
  C answers are published under `G-huihui-nex/` with the same rights
  treatment, but it is not part of the 384-answer original field and ran
  Formal C only (see
  `extensions/huihui-nex-n2-mini-abliterated-q4/README.md`). Its locked
  extension scorebook is untouched by this answer release.
