# NOTICE

Attribution and provenance notice for third-party artifacts referenced by this
release. This notice documents provenance; it does not grant any license over
third-party materials. Licensing of the project's own content is described in
`LICENSE` (MIT, code) and `LICENSE-DOCS-DATA.md` (CC BY 4.0 for documentation,
benchmark questions, figures, and project-derived evaluation data).

## Third-party model statement

- The six evaluated models are **third-party artifacts** (community GGUF
  fine-tunes of third-party base models).
- **Model weights are NOT distributed by this repository.** Only metadata and
  provenance records (filenames, sizes, SHA256 fingerprints, quantizations,
  upstream source identifiers) are included.
- Model names and metadata remain the property/responsibility of their
  upstream authors.
- Exact local benchmark-artifact fingerprints (SHA256) are provided **only for
  provenance/reproducibility** — they do not constitute distribution of any
  upstream artifact.
- The model-generated final-answer datasets are **withheld** from this initial
  public release (OUTPUT-REDISTRIBUTION-DECISION.md).
- Upstream source/license information is documented in MODEL-CARDS.md,
  MODEL-ARTIFACT-MANIFEST.md, `data/model-artifacts.csv`, and
  MODEL-SOURCE-TODO.md.
- Missing acquisition provenance for some artifacts (notably the F model's
  exact abliterated GGUF variant source) is explicitly documented as a
  known limitation; this repository does not assert that such provenance was
  recovered.
- This repository makes **no ownership claim over any third-party model**.

## Evaluated models (community GGUF fine-tunes)

| model | author/org | primary source |
|---|---|---|
| RavenX-CyberAgent-35B-v5.1 | DeadByDawn101 | huggingface.co/deadbydawn101/RavenX-CyberAgent-Qwen3.6-35B-A3B-Opus-4.7-OpenMythos-Pentester-BugHunter-RATH-GGUF |
| Endy-Qwen3.6-CyberSec-35B-A3B | endystrike | huggingface.co/endystrike/Endy-Qwen3.6-CyberSec-35B-A3B |
| Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced | HauhauCS | huggingface.co/HauhauCS/Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-MTP |
| Ornith-1.5-35B-A3B-Abliterated | ornith-ai (base); mradermacher / codecraftersllc (abliterated GGUF suites) | huggingface.co/ornith-ai/Ornith-1.5-35B-A3B; mradermacher/Ornith-1.5-35B-A3B-FULLY-OBLITERATED-i1-GGUF; codecraftersllc/ornith-1.5-35b-a3b-abliterated |
| Nex-N2-mini | nex-agi (original); bartowski (GGUF) | huggingface.co/nex-agi/Nex-N2-mini; huggingface.co/bartowski/nex-agi_Nex-N2-mini-GGUF |
| Qwen3.8-9B-abliterated-25 | base: QwenLM | github.com/QwenLM/Qwen3.8 (exact abliterated-25 GGUF repo SOURCE NOT RECOVERED) |

## Runtime

- llama.cpp (build `ba360efe1`, b10375) — llama.cpp project; its license
  applies upstream (MIT). Link-only; not redistributed.

## Base model families

- Qwen3.6 / Qwen3.8 (QwenLM, Alibaba) — Apache-2.0 (per Qwen3 series terms).
- Gemma 4 (Google) — Gemma license.
- Each fine-tune's exact terms must be confirmed from its own model card
  before any redistribution of its outputs (LICENSE-DOCS-DATA.md).
