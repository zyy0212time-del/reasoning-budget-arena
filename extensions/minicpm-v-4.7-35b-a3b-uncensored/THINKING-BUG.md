# Thinking early-EOS defect — reproduced on the official OpenBMB weights

Upstream issue: <https://github.com/OpenBMB/MiniCPM-V/issues/1153>
(title: *MiniCPM-V 4.7 Q4_K_M: JSON-only prompts return empty content
(missing `</think>`)*, opened 2026-10-15, author `zyy0212time-del`).

## 1. The symptom, as seen in this benchmark run

- General question **G10** produced reasoning content but an **empty
  final-answer field** (`finish_reason: stop`, 210 completion tokens). Under
  the frozen protocol it is published as
  `[NO FINAL ANSWER WITHIN FIXED BUDGET]` and scored **0/25**.
- A diagnostic pass with `--reasoning-format deepseek-legacy` reproduced the
  same split (content 0 chars, reasoning 461 chars): the answer exists, but
  only inside the thinking block.

## 2. Is it caused by the uncensoring ablation? No.

This extension runs the **AtomicChat refusal-direction-ablated** build. To test
whether the ablation was responsible, the same behaviour was reproduced on the
**official OpenBMB weights**:

| item | value |
|---|---|
| repo | `openbmb/MiniCPM-V-4.7-35B-A3B-gguf` (official organisation account; `base_model` = `openbmb/MiniCPM-V-4.7-35B-A3B`, relation `quantized`) |
| pinned revision | `b3b8cd80c0900c7ca461fdc3b87cbe5780a6b6ff` |
| file | `MiniCPM-V-4_7-35B-A3B-Q4_K_M.gguf` (official Q4_K_M, **not** a third-party re-quant) |
| size | 21,166,255,008 bytes |
| SHA-256 | `bf3d1c67f7843193e4483aebd26c5dea6b6d1f6a06ffa03c2387a6f3cc6d7df5` (matches the upstream LFS OID; computed twice, by the downloader and independently afterwards) |
| runtime | llama.cpp **b11636** (binary reports commit `529ac893e`), CUDA, Windows, text-only (no `mmproj` loaded) |

**Control arms on the official weights** (`/v1/chat/completions`, fixed seeds):

| arm | prompt | seeds | result |
|---|---|---|---|
| A | JSON-only, Chinese | 1, 2, 3 | **3/3** empty final content |
| B | JSON-only, English | 1, 2, 3 | **3/3** empty final content |
| C | free-text control | 1, 2 | **2/2** normal final content |
| D | JSON-only with a system prompt | 1, 2, 3 | **3/3** empty final content |

All six JSON-only failures share one raw signature: `stop_type=eos`,
`truncated=false`, the last sampled token is **`248046` (`<|im_end|>`)**, and
**`248069` (`</think>`) is never sampled** — generations were 18–24 tokens long.
The free-text controls terminate normally.

Special-token ids on both builds are identical: `<|im_start|>` = 248045,
`<|im_end|>` = 248046, `<think>` = 248068, `</think>` = 248069. The embedded
chat templates are also effectively identical (the official GGUF's template
carries one extra trailing newline; stripped of it, both hash to
`02faae121b9d3b83cdaabc9fd9220476f6a8ee8cffe49694d1454fc70d8a0535`).

## 3. What is established and what is not

**Established:** generation terminates with EOS from inside the thinking block,
without emitting `</think>`, on the **official** weights as well as on the
ablated build. The uncensoring ablation is therefore **not** the cause.

**Not established:** the code-level root cause. Confounders that were *not*
eliminated — quantization (Q4_K_M vs this extension's AD-Q4_K-IQ4_XS),
single-file vs 11-shard packaging, llama.cpp version, and the runtime's
thinking/reasoning parser. Fixed seeds make the runs deterministic replays,
not independent samples. So this is **not** evidence about how often the defect
occurs in the wild, only that it reproduces deterministically under these
settings.

## 4. Consequence for this extension

- G10's 0/25 is a **model output failure**, not infrastructure, so it was not
  retried and the score stands.
- For any deployment: keep `max_tokens` generous, or disable thinking
  per-request. A small token budget can be consumed entirely by thinking and
  yield an empty answer — exactly what happened on G10.
- The defect is independent of the score question but is a real usability
  caveat alongside the self-identification defect.
