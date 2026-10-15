# Upstream reproduction evidence — OpenBMB/MiniCPM-V issue #1153

This directory archives the **minimal reproduction package** submitted upstream.
It exists so that the maintainers of MiniCPM-V can download and inspect the raw
evidence directly, without needing anything from this benchmark machine.

- **Upstream issue:** <https://github.com/OpenBMB/MiniCPM-V/issues/1153>
  — *MiniCPM-V 4.7 Q4_K_M: JSON-only prompts return empty content (missing
  `</think>`)*
- **Package:** [`minicpm-v47-thinking-repro-evidence.zip`](minicpm-v47-thinking-repro-evidence.zip)
  — 28,762 bytes, 19 entries
- **ZIP SHA-256:** `283da76687744f8f6e5cb641dbadc4f40bf125b03ad00ba89c82825869e69436`

## What was tested

| item | value |
|---|---|
| model repository | `openbmb/MiniCPM-V-4.7-35B-A3B-gguf` (official OpenBMB organisation account; `base_model` = `openbmb/MiniCPM-V-4.7-35B-A3B`, relation `quantized`) |
| pinned revision | `b3b8cd80c0900c7ca461fdc3b87cbe5780a6b6ff` |
| file | `MiniCPM-V-4_7-35B-A3B-Q4_K_M.gguf` — official Q4_K_M, not a third-party re-quant |
| size | 21,166,255,008 bytes |
| **GGUF SHA-256** | `bf3d1c67f7843193e4483aebd26c5dea6b6d1f6a06ffa03c2387a6f3cc6d7df5` (matches the upstream LFS OID; computed twice — by the downloader and independently afterwards) |
| runtime | llama.cpp **b11636** (binary reports commit `529ac893e`), CUDA, Windows, text-only (no `mmproj` loaded) |
| endpoint | `/v1/chat/completions`, plus llama.cpp native `/completion`, `/apply-template`, `/tokenize`, `/detokenize` for token-level checks |

## What the package contains

- `README.md` — package index and how to run the reproduction
- `MODEL-PROVENANCE.md` — repository, revision, file size and full SHA-256 of the
  official GGUF
- `reproduce.py` — minimal reproduction script (no absolute paths, host
  configurable)
- `chat/` — raw HTTP request and response for the Chinese (A-zh) and English
  (B-en) JSON-only prompts, seed 1
- `completion/` — `/apply-template` rendered prompt, `/completion` request and
  response, sampled-token records and `/detokenize` output for seeds 1–3
- `tokenizer/special-token-ids.json` — token ids as measured on the live server
- `server-props.json` — llama.cpp `/props` for the session
- `HASHES.sha256` — SHA-256 of every file in the package

## Result recorded in the package

| arm | prompt | seeds | result |
|---|---|---|---|
| A | JSON-only, Chinese | 1, 2, 3 | 3/3 empty final content |
| B | JSON-only, English | 1, 2, 3 | 3/3 empty final content |
| C | free-text control | 1, 2 | 2/2 normal final content |
| D | Chinese JSON-only, with a system message | 1, 2, 3 | 3/3 normal final content |

Every failure ends on token `248046` (`<|im_end|>`) and never samples
`248069` (`</think>`); generations were 18–24 tokens, i.e. far below the
4,096-token reasoning budget.

## Limits — read before citing

- **Code-level root cause is unknown.** The same termination pattern was
  reproduced on the official OpenBMB Q4_K_M weights, so the failure is not
  unique to a decensored checkpoint. Quantization, chat template, runtime and
  training factors were **not** excluded.
- **`reproduce.py` was tidied for publication and was then only checked
  statically** (`py_compile`). It was **not re-executed** after trimming, and no
  model weights remain on the machine that produced these artefacts.
- Fixed seeds make these **deterministic replays**, not independent samples, so
  the package says nothing about how often the defect occurs in the wild.
- This directory contains the evidence package only — no model weights, and no
  benchmark scores are changed by it.
