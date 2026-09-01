# RUNTIME EVIDENCE (sanitized)

Sanitized excerpt of the experiment's runtime configuration documents, so that
release readers have the evidence the methodology cites without private local
paths. Machine-specific absolute paths are removed.

## Runtime

- **llama.cpp** build `ba360efe1` (b10375), Clang 20.1.8, Windows x86_64;
  binaries `llama-server.exe`, `llama-cli.exe`, `llama-bench.exe`.
- GPU: NVIDIA GeForce RTX 5060 Laptop, **8 GiB VRAM**, sm_120.
- MoE expert placement: the 35B-A3B Q4_K_M files (~18–20 GB) do not fit in
  8 GiB VRAM; llama.cpp `-ncmoe <experts>` keeps attention/dense on GPU and
  MoE experts on CPU. Prior local benchmarks on the same GPU/build measured
  ~43 t/s with experts-on-CPU vs ~4 t/s with all on GPU for the 35B-A3B class.
- The FreeToken engine exists locally but was **not** used for Formal D or
  Formal C; llama.cpp was the canonical arena runtime (same GGUF format, same
  runtime for all models).

## Benchmark-time flags (Formal D and Formal C)

| parameter | value |
|---|---|
| runtime | llama-server b10375 |
| context (`-c`) | 8192 |
| flash-attn | on |
| offload (`-ngl`) | 99 (max) |
| threads (`-t`) | 24 |
| temperature | 0.1 (capability runs; 0.0 only on the separate speed benchmark) |
| top_p | 0.9 |
| max_tokens | 8192 (capability; 220 on the speed benchmark) |
| system prompt | none (vanilla) — no model-specific persona in the scored runs |
| MoE experts | `-ncmoe` per model from GGUF metadata (A/B/D/E 256, C 128, F 0) |
| reasoning budget | Formal D: none; Formal C: `--reasoning-budget 4096` |

## Fairness rules applied in the runs

- Same user prompt, same no-system policy, same ctx/fa/temp/top_p/max_tokens
  for every model within a condition.
- Speed measured separately and never folded into quality.
- One llama-server at a time; per-division server logs retained in the
  experiment archive.
