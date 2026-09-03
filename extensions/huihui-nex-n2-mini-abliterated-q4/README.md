# Extension — Huihui Nex N2 Mini Abliterated Q4_K_M

Post-release extension entry of the [Reasoning Budget Arena](../../README.md).
This model was evaluated **after** the original Formal C release under the
identical frozen Formal C protocol (ctx 8192 · max_tokens 8192 · temp 0.1 ·
top_p 0.9 · native reasoning budget 4096 · no system prompt · one
llama-server at a time · llama.cpp b10375).

**This model's score is shown as a post-release extension and does not modify
the original six-contestant locked ranking.**

## Model

- Model: Huihui Nex N2 Mini Abliterated Q4_K_M
- GGUF repo: `quant-mind/Huihui-Nex-N2-mini-abliterated-GGUF` (frozen revision
  `22be29be9d6908060502f4ac984650a917afdbe6`)
- GGUF SHA256: `8e38d2a090ea8a850745032b212a96997d0dafeb4cadd74b840a599e2c70e8a0`
- Lineage: quant-mind GGUF → `huihui-ai/Huihui-Nex-N2-mini-abliterated` →
  `nex-agi/Nex-N2-mini`
- Identity metadata (abliterated / uncensored) verified from the GGUF itself

## Result (Formal C Extension, blind, locked)

| | score | max | % |
|---|---:|---:|---:|
| General | 395.0 | 450 | 87.78% |
| Cyber | 274.5 | 350 | 78.43% |
| **Overall** | **669.5** | **800** | **83.69%** |

- 32/32 scored, locked before identity reveal
- Scorebook: [FORMAL-C-EXTENSION-BLIND-SCORES-LOCKED.md](FORMAL-C-EXTENSION-BLIND-SCORES-LOCKED.md)

## Post-lock comparative placement (context only, not a re-ranking)

| dimension | placement vs original locked field |
|---|---:|
| General | 4 / 7 |
| Cyber | 5 / 7 |
| Overall | 4 / 7 |

The original six-contestant locked Formal C ranking is unchanged.

## Generation performance (formal frozen run)

- generation median: **40.51 t/s** (range 32.37-46.66)
- prompt processing median: 45.26 t/s (range 2.97-114.84)
- wall time / question median: 110.1 s
- completion tokens total: 120,348

Runtime-specific (llama.cpp b10375, MoE experts on CPU, RTX 5060 Laptop 8 GiB),
same runtime policy as the original field.

## Privacy / scope

- Questions, methodology and protocol: same frozen set as the original release.
- **Answer text datasets: this extension's 32 Formal C final answers are now
  public** —
  [`data/model-answers/G-huihui-nex/formal-c.csv`](../../data/model-answers/G-huihui-nex/formal-c.csv)
  (post-release answer addendum). They were extracted byte-faithfully from
  the frozen extension generation artifacts — final-answer field only, no
  reasoning content — and carry the same benchmark-artifact rights treatment
  introduced in v1.2.0. *(This supersedes the earlier "answer text remains
  withheld" wording for this extension.)*
- This answer release changes **nothing else**: the extension's locked score
  (669.5 / 800), its post-lock comparative placement, the original
  six-contestant locked ranking, and the runtime numbers above are all
  unmodified. Huihui has no Formal D answers and is not a seventh contestant
  of the original field.
- Output-terms basis: `quant-mind/Huihui-Nex-N2-mini-abliterated-GGUF`,
  `huihui-ai/Huihui-Nex-N2-mini-abliterated` and `nex-agi/Nex-N2-mini` are
  all Apache-2.0 (checked 2026-09-03); no term was found prohibiting
  reproduction of benchmark/evaluation outputs.
- Subjective observations about this model's behavior are in the main
  [README](../../README.md) under *Subjective observations* and are not part of
  the benchmark scores.
