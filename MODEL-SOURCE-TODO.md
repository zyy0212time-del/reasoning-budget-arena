# MODEL SOURCES

Status of upstream source verification for the six benchmark models, resolved
for the R1 revision. Primary sources were located via web search (verified
pages), not guessed from filenames. Where the exact uploader of the local
GGUF cannot be pinned from archived artifacts, that is stated.

| tag | model | primary source (verified) | base model | license / terms | local GGUF provenance | status |
|---|---|---|---|---|---|---|
| A | RavenX-CyberAgent-35B-v5.1-Q4_K_M | `huggingface.co/deadbydawn101/RavenX-CyberAgent-Qwen3.6-35B-A3B-Opus-4.7-OpenMythos-Pentester-BugHunter-RATH-GGUF` (author DeadByDawn101; GitHub `DeadByDawn101`) | Qwen3.6-35B-A3B | see model card (UNDETERMINED from artifacts) | Q4_K_M variant of the same GGUF repo | **RESOLVED** (model + GGUF repo) |
| B | Endy-Qwen3.6-CyberSec-35B-A3B-Q4_K_M | `huggingface.co/endystrike/Endy-Qwen3.6-CyberSec-35B-A3B` (author endystrike; qwen3_5_moe, ~35B total / ~3B active) | Qwen3.6-35B-A3B | see model card (UNDETERMINED from artifacts) | Q4_K_M community quant of the above | **RESOLVED** (model page; exact GGUF uploader not pinned) |
| C | Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-Q4_K_M | `huggingface.co/HauhauCS/Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-MTP` (author HauhauCS) | google/gemma4 (QAT weights; unsloth `unsloth/gemma-4-26B-A4B-it-qat-GGUF` as the GGUF quant chain) | see model card (UNDETERMINED from artifacts) | Balanced Q4_K_M variant of the HauhauCS repo | **RESOLVED** |
| D | Ornith-1.5-35B-A3B-Abliterated-Q4_K_M | base: `huggingface.co/ornith-ai/Ornith-1.5-35B-A3B` (and `ornith-ai/Ornith-1.5-35B-A3B-GGUF`); refusal-ablated variant suites: `mradermacher/Ornith-1.5-35B-A3B-FULLY-OBLITERATED-i1-GGUF`, `codecraftersllc/ornith-1.5-35b-a3b-abliterated` | ornith-ai/Ornith-1.5-35B-A3B (Qwen3.5-35B-A3B class) | see model card (UNDETERMINED from artifacts) | abliterated GGUF; which of the variant suites produced the local file cannot be pinned | **RESOLVED** (base + variant suites; exact uploader not pinned) |
| E | Nex-N2-mini-Q4_K_M | GGUF: `huggingface.co/bartowski/nex-agi_Nex-N2-mini-GGUF`; original: `huggingface.co/nex-agi/Nex-N2-mini` (nex-agi) | Qwen3.5 series (Nex-N2-mini, per bartowski/Mungert cards) | see model card (UNDETERMINED from artifacts) | Q4_K_M imatrix quant from bartowski suite (filename matches `nex-agi_Nex-N2-mini-Q4_K_M.gguf`) | **RESOLVED** |
| F | Qwen3.8-9B-abliterated-25.Q4_K_M | base: `github.com/QwenLM/Qwen3.8` (Qwen3.8-9B family); exact "abliterated-25" GGUF repo **SOURCE NOT RECOVERED** | Qwen3.8-9B | see base model page | exact uploader/repo of the abliterated-25 GGUF not recovered from artifacts or search | **PARTIAL** (base recovered; exact variant repo NOT RECOVERED) |

## Status summary — two distinct things

**A. ARTIFACT IDENTITY — 6/6 strong.** For every model the exact local file is
immutably recorded: filename, byte size, SHA256, quantization
(`data/model-artifacts.csv`, MODEL-ARTIFACT-MANIFEST.md). No ambiguity.

**B. ARTIFACT ACQUISITION PROVENANCE — partial, per actual evidence.**
- **A**: primary GGUF repository located (deadbydawn101) — **resolved**.
- **B**: model page located (endystrike); the exact GGUF uploader for the local
  file is **not pinned** — partial.
- **C**: model repository located (HauhauCS Balanced-MTP) — **resolved**.
- **D**: base located (ornith-ai); refusal-ablated GGUF suites located
  (mradermacher, codecraftersllc), but which suite produced the local file is
  **not pinned** — partial.
- **E**: GGUF suite located (bartowski) + original (nex-agi) — **resolved**.
- **F**: base located (QwenLM/Qwen3.8); the exact "abliterated-25" GGUF
  uploader is **SOURCE NOT RECOVERED** — no URL is guessed.

This is a **P2 reproducibility limitation**, not a release blocker: artifact
identity is fully verifiable via hash; acquisition provenance for B/D (and the
F variant) is documented as unresolved rather than guessed.

Upstream licenses for the fine-tunes remain **UNDETERMINED** from archived
artifacts; LICENSE-NOTES.md / OUTPUT-REDISTRIBUTION-DECISION.md carry the
licensing items.

## llama.cpp runtime

- Runtime build used in the benchmark: llama.cpp `ba360efe1` (b10375).
  Provenance link: the llama.cpp repository (github.com/ggerganov/llama.cpp);
  the exact commit page was not archived in this project — recorded as
  build id only (RUNTIME evidence: harness start logs in the experiment
  archive).
