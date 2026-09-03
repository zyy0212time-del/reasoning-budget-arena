# MODEL SOURCES

Status of upstream source verification for the six benchmark models, resolved
for the R1 revision. Primary sources were located via web search (verified
pages), not guessed from filenames. Where the exact uploader of the local
GGUF cannot be pinned from archived artifacts, that is stated.

| tag | model | primary source (verified) | base model | license / terms | local GGUF provenance | status |
|---|---|---|---|---|---|---|
| A | RavenX-CyberAgent-35B-v5.1-Q4_K_M | `huggingface.co/deadbydawn101/RavenX-CyberAgent-Qwen3.6-35B-A3B-Opus-4.7-OpenMythos-Pentester-BugHunter-RATH-GGUF` (author DeadByDawn101; GitHub `DeadByDawn101`) | Qwen3.6-35B-A3B | see model card (UNDETERMINED from artifacts) | Q4_K_M variant of the same GGUF repo | **RESOLVED** (model + GGUF repo) |
| B | Endy-Qwen3.6-CyberSec-35B-A3B-Q4_K_M | `huggingface.co/endystrike/Endy-Qwen3.6-CyberSec-35B-A3B` (model page) and `huggingface.co/endystrike/Endy-Qwen3.6-CyberSec-35B-A3B-GGUF` (author's own exact GGUF repo, AGPL-3.0) (author endystrike; qwen3_5_moe, ~35B total / ~3B active) | Qwen3.6-35B-A3B | see model card (UNDETERMINED from artifacts) | exact artifact match: `endystrike/Endy-Qwen3.6-CyberSec-35B-A3B-GGUF` / `Endy-Qwen3.6-CyberSec-35B-A3B-Q4_K_M.gguf` — remote LFS OID == frozen local SHA-256 (verified 2026-09-03; original local file since removed from disk) | **RESOLVED** (exact artifact hash match, 2026-09-03) |
| C | Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-Q4_K_M | `huggingface.co/HauhauCS/Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-MTP` (author HauhauCS) | google/gemma4 (QAT weights; unsloth `unsloth/gemma-4-26B-A4B-it-qat-GGUF` as the GGUF quant chain) | see model card (UNDETERMINED from artifacts) | Balanced Q4_K_M variant of the HauhauCS repo | **RESOLVED** |
| D | Ornith-1.5-35B-A3B-Abliterated-Q4_K_M | base: `huggingface.co/ornith-ai/Ornith-1.5-35B-A3B`; exact abliterated GGUF: `huggingface.co/PocketAiHub/Ornith-1.5-35B-A3B-Abliterated-GGUF` (MIT) | ornith-ai/Ornith-1.5-35B-A3B (Qwen3.5-35B-A3B class) | see model card (UNDETERMINED from artifacts) | exact artifact match: `PocketAiHub/Ornith-1.5-35B-A3B-Abliterated-GGUF` / `Ornith-1.5-35B-A3B-Abliterated-Q4_K_M.gguf` — remote LFS OID == frozen local SHA-256, local file still on disk with matching size (verified 2026-09-03) | **RESOLVED** (exact artifact hash match, 2026-09-03) |
| E | Nex-N2-mini-Q4_K_M | GGUF: `huggingface.co/bartowski/nex-agi_Nex-N2-mini-GGUF`; original: `huggingface.co/nex-agi/Nex-N2-mini` (nex-agi) | Qwen3.5 series (Nex-N2-mini, per bartowski/Mungert cards) | see model card (UNDETERMINED from artifacts) | Q4_K_M imatrix quant from bartowski suite (filename matches `nex-agi_Nex-N2-mini-Q4_K_M.gguf`) | **RESOLVED** |
| F | Qwen3.8-9B-abliterated-25.Q4_K_M | base: `github.com/QwenLM/Qwen3.8` (Qwen3.8-9B family); exact "abliterated-25" GGUF: `huggingface.co/MegaPanchamZ/Qwen3.8-9B-abliterated-25-GGUF` (Apache-2.0) | Qwen3.8-9B | see base model page | exact artifact match: `MegaPanchamZ/Qwen3.8-9B-abliterated-25-GGUF` / `Qwen3.8-9B-abliterated-25.Q4_K_M.gguf` — remote LFS OID == frozen local SHA-256 (verified 2026-09-03; original local file since removed from disk) | **RESOLVED** (exact artifact hash match, 2026-09-03) |

## Status summary — two distinct things

**A. ARTIFACT IDENTITY — 6/6 strong.** For every model the exact local file is
immutably recorded: filename, byte size, SHA256, quantization
(`data/model-artifacts.csv`, MODEL-ARTIFACT-MANIFEST.md). No ambiguity.

**B. ARTIFACT ACQUISITION PROVENANCE — partial, per actual evidence.**
- **A**: primary GGUF repository located (deadbydawn101) — **resolved**.
- **B**: author's own exact GGUF repo located (endystrike/…-GGUF) and the
  local artifact hash-matched against it — **resolved** (2026-09-03).
- **C**: model repository located (HauhauCS Balanced-MTP) — **resolved**.
- **D**: exact abliterated GGUF repo identified (PocketAiHub/…-GGUF) and
  hash-matched — **resolved** (2026-09-03).
- **E**: GGUF suite located (bartowski) + original (nex-agi) — **resolved**.
- **F**: exact "abliterated-25" GGUF repo recovered (MegaPanchamZ) and
  hash-matched — **resolved** (2026-09-03).

Resolved 2026-09-03: the previously unresolved acquisition provenance (the B
exact uploader, the D exact abliterated uploader, the F exact variant repo)
is now exact-artifact-hash-verified (remote LFS OID == frozen local SHA-256;
full table in data/model-answers/NOTICE.md). What remains intentionally open
is the **output-terms review for A and B** (OUTPUT-REDISTRIBUTION-DECISION.md,
data/model-answers/MANIFEST.md) — provenance resolution does not by itself
authorize publication of a model's answers.

Upstream license labels were re-checked from live model cards on 2026-09-03
where relevant to the addendum (B: AGPL-3.0; D GGUF: MIT; F: Apache-2.0;
E: Apache-2.0; C: Gemma license; A: Apache-2.0 card label with additional
research-purposes-only wording in the card body). The per-model output-terms
review that gates answer publication is recorded in
OUTPUT-REDISTRIBUTION-DECISION.md (2026-09-03 update) and
data/model-answers/MANIFEST.md.

## llama.cpp runtime

- Runtime build used in the benchmark: llama.cpp `ba360efe1` (b10375).
  Provenance link: the llama.cpp repository (github.com/ggerganov/llama.cpp);
  the exact commit page was not archived in this project — recorded as
  build id only (RUNTIME evidence: harness start logs in the experiment
  archive).
