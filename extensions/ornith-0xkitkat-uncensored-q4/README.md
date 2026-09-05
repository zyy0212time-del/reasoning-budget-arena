# Extension — Ornith-1.5-35B-A3B-Uncensored Q4_K_M (0xKitkat)

Post-release extension entry of the [Reasoning Budget Arena](../../README.md).
This model was evaluated **after** the original Formal C release under the
identical frozen Formal C protocol (ctx 8192 · max_tokens 8192 · temp 0.1 ·
top_p 0.9 · native reasoning budget 4096 · no system prompt · one
llama-server at a time · llama.cpp b10375).

**This model's score is shown as a post-release extension and does not modify
the original six-contestant locked ranking.**

## Status

**EVALUATED — NOT RETAINED FOR LOCAL DEPLOYMENT**

- technically healthy (load, sanity, context and responsiveness probes all passed)
- Formal C overall **672.0 / 800 (84.00%)**
- General performance remained relatively strong (397.5 / 450, 88.33%)
- Cyber dropped materially relative to the existing Old Ornith
  (Abliterated) result (274.5 vs 320.5 / 350)
- practical role overlaps the existing Huihui/Nex deployment options
- no clear deployment advantage remained for the maintainer's current local stack

This is a **negative/selection result**: the model passes health and quality
sanity checks yet does not improve the existing roster. The benchmark's
extension process supports rejection decisions, not only winner selection.

## Model

- Model: Ornith-1.5-35B-A3B-Uncensored Q4_K_M
- GGUF repo: `0xKitkat/Ornith-1.5-35B-A3B-Uncensored-GGUF` (pinned revision
  `ab0eed77c73880afda789a3914003db2273fd64a`)
- GGUF: `Ornith-1.5-35B-Uncensored-Q4_K_M.gguf`, 21,713,463,264 bytes
- GGUF SHA256: `081fa0babd0e32432acf67d6af80b7e7550ae8a102a6ca6c48e4e39aab685bc9`
  (verified before and again after the Formal C generation run)
- Construction: task-vector transplant —
  `output = Ornith-1.5 + 1.0 × (Qwen3.6-abliterated − Qwen3.6-base)`;
  102 of 693 compatible tensors modified
- Upstream licenses: repo label **apache-2.0**; lineage Ornith-1.5 (**MIT**)
  + Qwen3.6-35B-A3B (**apache-2.0**) — checked 2026-09-05, see
  [provenance.json](provenance.json)

## Result (Formal C Extension, blind, locked)

| | score | max | % |
|---|---:|---:|---:|
| General | 397.5 | 450 | 88.33% |
| Cyber | 274.5 | 350 | 78.43% |
| **Overall** | **672.0** | **800** | **84.00%** |

- 32/32 scored, **locked before identity reveal** (blind contestant id ZD74)
- Scorebook: [FORMAL-C-EXTENSION-BLIND-SCORES-LOCKED.md](FORMAL-C-EXTENSION-BLIND-SCORES-LOCKED.md)
- Question-level scores: [question-scores.csv](question-scores.csv) /
  [question-scores.json](question-scores.json)
- Verbatim answers: [`data/model-answers/H-ornith-0xkitkat/formal-c.jsonl`](../../data/model-answers/H-ornith-0xkitkat/formal-c.jsonl)

## Generation anomaly (documented, not hidden)

The initial cyber run reached 12/14 and aborted with a llama-server HTTP 500
("output does not match the expected peg-native format") while generating C13.
The frozen infrastructure retry rule allowed **one** identical retry via
`--ids C13,C14`; the retry completed 14/14. No cherry-picking, no manual
answer replacement. See [LIMITATIONS.md](LIMITATIONS.md).

## Old Ornith vs New Ornith (same frozen benchmark, same protocol family)

| | Old Ornith (Abliterated, PocketAiHub) | New Ornith (Uncensored, 0xKitkat) | Δ new − old |
|---|---:|---:|---:|
| General /450 | 405.0 | 397.5 | **−7.5** |
| Cyber /350 | 320.5 | 274.5 | **−46.0** |
| **Overall /800** | **725.5** | **672.0** | **−53.5** |

Interpretation (one run, no significance claim): General capability remained
relatively close; Cyber showed a substantial regression.

## Comparison with the Huihui Nex extension

| | Huihui Nex (G) | New Ornith (H) | Δ |
|---|---:|---:|---:|
| General /450 | 395.0 | 397.5 | +2.5 |
| Cyber /350 | 274.5 | 274.5 | identical |
| Overall /800 | 669.5 | 672.0 | +2.5 |

This near-identical profile supports the deployment conclusion that the new
model substantially **overlaps the Huihui/Nex practical role** rather than
preserving the old Ornith Cyber advantage. Overlap is not equivalence.

## Uncensoring note

No comprehensive manual uncensoring evaluation was performed. Evidence is
limited to the lightweight scripted refusal sanity (4/4 COMPLIANCE) and the
upstream model card/name. This is **not** a manual uncensoring validation.

## Runtime probes

See [responsiveness.json](responsiveness.json) and [context.json](context.json).
The D1 probes ran at server ctx 16384 and are **preliminary health probes**,
not Arena-comparable ctx-8192 benchmark conditions. Frozen-protocol Formal C
telemetry (per-question medians): General decode ≈ 39.4 t/s (median wall
69.1 s), Cyber decode ≈ 37.7 t/s (median wall 126.5 s).

## Privacy / scope

- Questions, methodology and protocol: same frozen set as the original release.
- **This extension's 32 Formal C final answers are public** —
  [`data/model-answers/H-ornith-0xkitkat/`](../../data/model-answers/H-ornith-0xkitkat/)
  (Formal C only; no Formal D was run). Answers are byte-faithful to the
  frozen generation artifacts — final-answer field only, no hidden reasoning —
  including the C3 answer exactly as generated (see LIMITATIONS.md §4).
- Output-terms basis: upstream repo is Apache-2.0 with disclosed MIT +
  Apache-2.0 lineage; no term was found prohibiting reproduction of
  benchmark/evaluation outputs.
- The original six-contestant locked Formal C ranking is unchanged.
