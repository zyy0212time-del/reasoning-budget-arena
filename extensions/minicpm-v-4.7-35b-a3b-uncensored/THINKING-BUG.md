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

## 2. Reproduced on the official OpenBMB weights

This extension runs the **AtomicChat refusal-direction-ablated** build. The same
termination pattern was reproduced on the **official OpenBMB weights**:

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
| D | **JSON-only with a system prompt** | 1, 2, 3 | **3/3 normal final content** |

The six failures are arms A and B (6/6). Arm **D did not reproduce**: adding a
system prompt made JSON-only prompts return normal final content on all three
seeds. So the pattern as reproduced is specific to JSON-only prompts **without**
a system prompt.

All six failures share one raw signature: `stop_type=eos`,
`truncated=false`, the last sampled token is **`248046` (`<|im_end|>`)**, and
**`248069` (`</think>`) is never sampled** — generations were 18–24 tokens long,
i.e. far below the 4,096-token reasoning budget. The early EOS is **not** a
budget-exhaustion event in this reproduction.

Special-token ids on both builds are identical: `<|im_start|>` = 248045,
`<|im_end|>` = 248046, `<think>` = 248068, `</think>` = 248069. The embedded
chat templates are also effectively identical (the official GGUF's template
carries one extra trailing newline; stripped of it, both hash to
`02faae121b9d3b83cdaabc9fd9220476f6a8ee8cffe49694d1454fc70d8a0535`).

## 3. What is established and what is not

**Established:** generation terminates with EOS from inside the thinking block,
without emitting `</think>`, on the **official** weights as well as on the
ablated build, for JSON-only prompts without a system prompt. The same
termination pattern was reproduced on the official OpenBMB Q4_K_M weights, so
the failure is not unique to the decensored checkpoint. The underlying cause
remains unknown.

**Not established:** any causal attribution. Quantization (Q4_K_M vs this
extension's AD-Q4_K-IQ4_XS), the chat template, the runtime (llama.cpp b11636
and its reasoning parser), and training-side factors were **not** excluded.
Fixed seeds make the runs deterministic replays, not independent samples, so
this is **not** evidence about how often the defect occurs in the wild — only
that it reproduces deterministically under these settings.

## 4. Consequence for this extension

- G10's 0/25 stands as scored and was not retried. Its published marker
  `[NO FINAL ANSWER WITHIN FIXED BUDGET]` is the frozen protocol's label for
  "no final answer was delivered"; it is **not** proof that the 4,096-token
  reasoning budget caused the failure.
- G10 (this Formal C run) and the JSON-only minimal reproduction on the
  official weights are **two separate observations** and must not be merged.
  The reproduction terminated after 18–24 tokens — far below the budget — so it
  is not a budget-exhaustion case, and G10's cause has not been established
  either.
- **Not a validated fix:** raising `max_tokens` was never tested as a remedy
  for the early-EOS pattern and must not be presented as one. What *is*
  observed is that arm D (JSON-only **with** a system prompt) returned normal
  output on 3/3 seeds while the same prompts without one failed 6/6 — an
  unverified lead, not a fix.
- The defect is a real usability caveat alongside the self-identification
  defect. It is moot in practice here: the model was **not retained**, and both
  GGUF sets were deleted after archiving.
