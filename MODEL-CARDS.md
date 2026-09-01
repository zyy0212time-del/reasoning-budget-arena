# MODEL CARDS

Six contestants, all local GGUF files, all Q4_K_M quantization. Fields marked
**not independently verified** were not confirmed from upstream model cards
during the experiments; they come from filenames and GGUF metadata captured
locally. Source links are tracked in MODEL-SOURCE-TODO.md.

| tag | model file | size | architecture class (source) | parameter count | notes |
|---|---|---|---|---|---|
| A | RavenX-CyberAgent-35B-v5.1-Q4_K_M.gguf | 20.22 GB | Qwen3.6-35B-A3B MoE class (GGUF metadata: qwen35moe, 256 experts) | "35B" per filename — **not independently verified** | cyber-focused fine-tune (per name) |
| B | Endy-Qwen3.6-CyberSec-35B-A3B-Q4_K_M.gguf | 20.22 GB | Qwen3.6-35B-A3B MoE class (GGUF metadata: qwen35moe, 256 experts) | "35B" per filename — **not independently verified** | cyber-focused fine-tune (per name) |
| C | Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-Q4_K_M.gguf | 15.64 GB | Gemma4-class MoE (GGUF metadata: gemma4, 128 experts) | "26B-A4B" per filename — **not independently verified** | QAT; community fine-tune (per name) |
| D | Ornith-1.5-35B-A3B-Abliterated-Q4_K_M.gguf | 19.71 GB | Qwen3.5-35B-A3B MoE class (GGUF metadata: qwen35moe, 256 experts) | "35B" per filename — **not independently verified** | abliterated fine-tune (per name) |
| E | nex-agi_Nex-N2-mini-Q4_K_M.gguf | 19.92 GB | Qwen-style 35B MoE class (GGUF metadata: qwen35moe, 256 experts) | **not independently verified** | per name: "Nex-N2-mini" by nex-agi |
| F | Qwen3.8-9B-abliterated-25.Q4_K_M.gguf | 5.24 GB | dense (GGUF metadata: qwen3.8 family; ncmoe 0) | "~9B" per filename — **not independently verified** | abliterated fine-tune (per name) |

Runtime treatment (identical in both formal conditions): `-ngl 99`,
`--flash-attn on`, 24 threads, `-c 8192`; MoE experts on CPU via
`-ncmoe <experts>` (A/B/D/E 256, C 128, F 0 — the dense 9B needs none). No
system prompt, no model-specific persona; each model's native chat template
and native/default thinking behaviour.

Speed (RUNTIME-SPECIFIC, llama.cpp b10375, measured separately and never
folded into quality scores): A 44.8, B 45.2, C 37.7, D 43.5, E 47.0, F 58.2
tokens/s on the speed benchmark.

## Sources and artifact evidence

| tag | upstream source (verified) | local artifact evidence |
|---|---|---|
| A | huggingface.co/deadbydawn101/RavenX-CyberAgent-Qwen3.6-35B-A3B-Opus-4.7-OpenMythos-Pentester-BugHunter-RATH-GGUF | SHA256 + size: `data/model-artifacts.csv` |
| B | huggingface.co/endystrike/Endy-Qwen3.6-CyberSec-35B-A3B | `data/model-artifacts.csv` |
| C | huggingface.co/HauhauCS/Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-MTP | `data/model-artifacts.csv` |
| D | base huggingface.co/ornith-ai/Ornith-1.5-35B-A3B; abliterated suites mradermacher/…-FULLY-OBLITERATED-i1-GGUF, codecraftersllc/… | `data/model-artifacts.csv` |
| E | huggingface.co/bartowski/nex-agi_Nex-N2-mini-GGUF (original nex-agi/Nex-N2-mini) | `data/model-artifacts.csv` |
| F | base github.com/QwenLM/Qwen3.8; exact abliterated-25 GGUF repo **SOURCE NOT RECOVERED** | `data/model-artifacts.csv` |

SHA256 values were computed over the exact local benchmark files at R1
(2026-09-01) and are recorded immutably in `MODEL-ARTIFACT-MANIFEST.md` and
`data/model-artifacts.csv` so the benchmark can be re-downloaded or
reproduced after any C-drive cleanup. Full provenance status and caveats:
MODEL-SOURCE-TODO.md (re-solved for R1).
