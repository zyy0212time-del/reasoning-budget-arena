# Extension — MiMo-V2.6-Distill-Qwen-9B-Abliterated Q4_K_M

Post-release extension entry of the [Reasoning Budget Arena](../../README.md).
This model was evaluated **after** the original Formal C release under the
identical frozen Formal C protocol (ctx 8192 · max_tokens 8192 · temp 0.1 ·
top_p 0.9 · native reasoning budget 4096 · no system prompt · one
llama-server at a time · llama.cpp b10375).

**This model's score is shown as a post-release extension and does not modify
the original six-contestant locked ranking.**

## Status

**EVALUATED — NOT RETAINED FOR LOCAL DEPLOYMENT**

- health, load, reasoning-channel and reasoning-budget probes all passed
- Formal C overall **539.0 / 800 (67.38%)**
- last of 9 on General, Cyber and Overall in the rolling extension view
- 96.0 points below the other 9B contestant of the original field
  (Qwen3.8-9B-abliterated, 635.0)
- it is nonetheless the **fastest** model measured in this arena
  (median decode 52.44 t/s vs ≈38–41 t/s for the retained MoE models)

This is a selection result: a very fast 9B whose blinded final-answer quality
does not reach the existing roster. The benchmark's extension process supports
rejection decisions, not only winner selection.

## Model

- Model: MiMo-V2.6-Distill-Qwen-9B-Abliterated Q4_K_M
- GGUF repo: `BoldingBuilds/MiMo-V2.6-Distill-Qwen-9B-Abliterated-Q8_0-GGUF`
  (frozen revision `ea8a846460d5643d7010d0500f7d7dd8c347cf59`)
- GGUF: `MiMo-V2.6-Distill-Qwen-9B-Abliterated-Q4_K_M.gguf`, 5,629,105,280 bytes
- GGUF SHA256: `8798617e1da0b324a7d4c04659c59bb8f712dd5a7332b4703a5a2875d977ecf2`
  (matches the HuggingFace LFS oid of the pinned revision; verified before and
  again after the Formal C generation run)
- Architecture from the GGUF itself: `qwen35`, **dense** (no MoE expert
  metadata), 32 blocks, 4096 embedding, 16/4 attention heads, native context
  262144, vocab 248320, hybrid SSM keys present (`full_attention_interval` 4),
  `nextn_predict_layers` 0
- Quantization: Q4_K_M (GGUF `general.file_type` 15)
- Native reasoning: the GGUF chat template is a Qwen3.5-style template with a
  `<think>` reasoning block, and the runtime reports that the template supports
  preserving reasoning. A separated reasoning channel
  (`message.reasoning_content`) was confirmed at runtime.
- Declared base model in the GGUF: `XiaomiMiMo/MiMo-V2.6-Distill-Qwen-9B`
  (a Qwen3.5-9B distill). Upstream licenses checked 2026-09-23: the GGUF repo
  and the MiMo base are **MIT**, the declared Qwen3.5-9B lineage is
  **Apache-2.0** — see [provenance.json](provenance.json)

## Result (Formal C Extension, blind, locked)

| | score | max | % |
|---|---:|---:|---:|
| General | 307.0 | 450 | 68.22% |
| Cyber | 232.0 | 350 | 66.29% |
| **Overall** | **539.0** | **800** | **67.38%** |

- 32/32 scored, **locked before identity reveal** (blind contestant id `TM91`,
  internal run tag `I26`)
- Scorebook: [FORMAL-C-EXTENSION-BLIND-SCORES-LOCKED.md](FORMAL-C-EXTENSION-BLIND-SCORES-LOCKED.md)
- Question-level scores: [question-scores.csv](question-scores.csv) /
  [question-scores.json](question-scores.json)
- Verbatim answers: [`data/model-answers/I-mimo-v26-9b-abliterated-q4/formal-c.csv`](../../data/model-answers/I-mimo-v26-9b-abliterated-q4/formal-c.csv)
- Provenance record: [provenance.json](provenance.json)
- Runtime probes: [responsiveness.json](responsiveness.json)
- [LIMITATIONS.md](LIMITATIONS.md)

The score profile is **bimodal**, not uniformly mediocre: thirteen questions
scored 22–25/25 (G1, G3, G4, G8, G10, G13–G16, C3, C4, C10–C12), while several
failed severely (G12 3.5, G5 4.5, G7 5.5, C13 6.0, C14 9.5, C9 10.5).

## Runtime (no deviation)

- Runtime: **llama.cpp `llama-server` b10375 (build `ba360efe1`)**, Clang 20.1.8,
  Windows x86_64 — the **same build used by the original Formal C field**
- `historical_build_compatible`: **YES**. The historical runtime loads and runs
  this model, produces a separated reasoning channel and enforces
  `--reasoning-budget`. **No isolated newer build was required and none was
  used**, so this extension is both protocol-matched and runtime-matched with
  the original field. `runtime_deviation: NONE`.
- `-ngl 99 --flash-attn on -t 24 -c 8192`; `-ncmoe` not applicable (dense model)
- Reasoning-budget reality check (non-Arena probe prompt; see
  [responsiveness.json](responsiveness.json)): reasoning-channel length scales
  monotonically with the configured budget — 64 → 234 chars, 256 → 773 chars,
  4096 → 10482 chars, no flag → 988 chars. The 4096 hard budget is therefore
  genuinely enforced by the backend.

## Generation performance (formal frozen run)

- generation median: **52.44 t/s** (General 52.34, Cyber 52.81; range 15.67–54.54)
- prompt processing median: 962.7 t/s
- wall time / question median: **14.97 s** (General 12.03 s, Cyber 15.69 s)
- completion tokens total: 66,404
- VRAM peak ≈ 6.5 GiB of 8 GiB; system RAM 31.4 GB
- isolated `llama-bench` on the same runtime: pp512 2,029.98 t/s, tg128 57.17 t/s

Speed is runtime-specific and is **never** folded into answer quality, and it
was never shown to the judge.

## Blind / lock / reveal chronology

| step | artifact | SHA256 |
|---|---|---|
| generation complete (32/32, 0 retries) | `I26-general|cyber-questions.jsonl` | internal run archive |
| blind package frozen | `TM91-FORMAL-C-BLIND-ANSWERS.md` | `787ae6806d69134f0a139353fce5d618f2435b25a7721da25a8b580b23a5f4af` |
| independent blind judge (separate session, new window) | `TM91-JUDGE-RETURNED-VERBATIM.md` | internal run archive |
| **SCORES LOCKED (identity absent)** | `FORMAL-C-EXTENSION-BLIND-SCORES-LOCKED.md` | **`648d2b2822064a7a08c15d7723d256aac56d57ca898ff1a9b6279888ecd9a2b8`** |
| identity revealed (appended only) | same file, post-reveal | `a6c10450c5fa3a7e54035aca02927073cf64637051f708586c40b37d187f7a8c` |

The sealed prefix of the published scorebook still hashes to the SCORES-LOCKED
digest, so nothing in the locked score section changed during the reveal.
The judge received only the frozen judge instructions and the anonymous answer
package — no identity, no telemetry, no historical scores, no leaderboard.

## Post-lock comparative placement (context only, not a re-ranking)

Within the 9-model rolling view (original six-contestant field + three
post-release extensions):

| dimension | placement |
|---|---:|
| General | 9 / 9 |
| Cyber | 9 / 9 |
| Overall | 9 / 9 |

| model | scope | General /450 | Cyber /350 | Overall /800 |
|---|---|---:|---:|---:|
| Nex-N2-mini | frozen field | 418.5 | 328.0 | 746.5 |
| Ornith-1.5-35B-A3B-Abliterated (Old Ornith) | frozen field | 405.0 | 320.5 | 725.5 |
| Gemma4-26B-A4B-HauhauCS | frozen field | 414.5 | 291.5 | 706.0 |
| Ornith-1.5-35B-A3B-Uncensored (0xKitkat, ext) | extension H | 397.5 | 274.5 | 672.0 |
| Huihui-Nex-N2-mini-abliterated (ext) | extension G | 395.0 | 274.5 | 669.5 |
| Endy-Qwen3.6-CyberSec-35B-A3B | frozen field | 357.0 | 287.0 | 644.0 |
| Qwen3.8-9B-abliterated-25 | frozen field | 368.5 | 266.5 | 635.0 |
| RavenX-CyberAgent-35B-v5.1 | frozen field | 319.5 | 256.5 | 576.0 |
| **MiMo-V2.6-Distill-Qwen-9B-Abliterated (ext)** | **extension I** | **307.0** | **232.0** | **539.0** |

Post-lock deltas (TM91 − comparison): vs Gemma −167.0 overall (−59.5 Cyber);
vs Old Ornith −186.5 (−88.5 Cyber); vs Nex −207.5 (−96.0 Cyber);
vs Huihui Nex −130.5; vs Ornith 0xKitkat −133.0; vs the original
Qwen3.8-9B-abliterated **−96.0** (−61.5 General, −34.5 Cyber).

This is a **post-lock comparative placement**, not a re-ranking. The original
six-contestant locked Formal C ranking is unchanged.

## Answer dataset

This extension's 32 Formal C final answers are public —
[`data/model-answers/I-mimo-v26-9b-abliterated-q4/`](../../data/model-answers/I-mimo-v26-9b-abliterated-q4/).
They are byte-faithful verbatim final answers (final-answer field only, no
reasoning content, no trimming or reformatting), including the G5 answer exactly
as generated (see [LIMITATIONS.md](LIMITATIONS.md) §4).

Answer source: the frozen blind answer package (digest-pinned), because the
internal raw JSONL of this run's **general** division was destroyed by an
unrequested second generation pass *after* the score lock. The package is the
artifact the judge scored and was verified byte-identical (32/32) to the raw
`response` fields before the loss. Full account:
[LIMITATIONS.md](LIMITATIONS.md) §14.

Output-terms basis: the GGUF repository is **MIT** with a disclosed
**MIT** (MiMo) + **Apache-2.0** (Qwen3.5-9B) lineage (checked 2026-09-23); no
term was found prohibiting reproduction of benchmark/evaluation outputs.

## Privacy / scope

- Questions, methodology and protocol: same frozen set as the original release.
- The original six-contestant locked Formal C ranking is unchanged.
- This extension ran **Formal C only**; no Formal D dataset exists and none was
  created.
- The blind package contains no identity, no telemetry, no speed and no
  reasoning content; the leak check reported **0 identity hits**.
