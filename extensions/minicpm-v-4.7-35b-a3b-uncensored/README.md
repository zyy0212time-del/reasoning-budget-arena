# Extension — MiniCPM-V 4.7 35B-A3B Uncensored (AD-Q4_K-IQ4_XS)

Post-release extension entry of the [Reasoning Budget Arena](../../README.md).
This model was evaluated **after** the original Formal C release and after both
prior extensions, under the **frozen Formal C protocol** (ctx 8192 ·
max_tokens 8192 · temp 0.1 · top_p 0.9 · reasoning budget 4096 · no system
prompt · one llama-server at a time · 32 frozen questions · frozen
five-dimensional rubric).

**This model's score does not modify the original six-contestant locked
ranking.**

> **Read this before quoting the number.** This extension is graded under
> **Automated Blind Grading — New Judge Protocol**: two independent automated
> blind judges, calibrated against 10 locked historical anchor items. The
> historical field was scored by a different judge session, on a different
> llama.cpp build, with Q4_K_M quants. See
> [grading-method.md](grading-method.md) and [LIMITATIONS.md](LIMITATIONS.md).

## Status

**EVALUATED — PROMISING FOR THE MAINTAINER'S HANDS-ON UNCENSORING TRIAL; NOT
INSTALLED, NOT DEPLOYED, GEMMA NOT REPLACED.**

This extension is an evaluation only. Nothing was installed, no launcher was
changed, no default model was switched, and the incumbent Gemma build was not
touched. The deployment decision is deliberately left to the maintainer after
manual use.

## Model

- Model: MiniCPM-V 4.7 35B-A3B **Uncensored** (AtomicChat refusal-direction
  ablation baked into the weights)
- GGUF repo: `AtomicChat/MiniCPM-V-4.7-35B-A3B-Uncensored-GGUF`, pinned
  revision `948c2f37e34730f8abd9b80f86642f37e8f30960`
- Quant: `MiniCPM-V-4.7-35B-A3B-Uncensored-AD-Q4_K-IQ4_XS`
  (routed experts AD-Q4_K / IQ4_XS; attention, shared expert, embedding and
  output head at q8_0) — the only uncensored build of this model that fits an
  8 GiB card
- **11 GGUF shards, 20,125,154,976 bytes (18.74 GiB)**; all 11 SHA-256 digests
  match the LFS digests published by the authoritative Hugging Face tree at the
  pinned revision. See [hashes.json](hashes.json) /
  [provenance.json](provenance.json).
- No alternative model, alternative quant, alternative revision or alternative
  author was downloaded or run. ModelScope does not carry this repo (verified
  with a live control query); hf-mirror.com does, but it resolves to the same
  CDN as huggingface.co with no speed advantage, so the authoritative origin
  was used.

## Result (Formal C Extension, blind, locked)

| | score | max | % |
|---|---:|---:|---:|
| General | 391.0 | 450 | 86.89% |
| Cyber | 321.0 | 350 | 91.71% |
| **Overall** | **712.0** | **800** | **89.00%** |

- 32/32 scored, **locked before identity reveal** (blind contestant id `K71`).
- Two blind judges: `JUDGE-A` 723.0, `JUDGE-B` 705.0; inter-judge MAD
  **0.78 /question**; **0 items** needed adjudication.
- Scorebook: [FORMAL-C-EXTENSION-BLIND-SCORES-LOCKED.md](FORMAL-C-EXTENSION-BLIND-SCORES-LOCKED.md)
- Question-level: [question-scores.csv](question-scores.csv) /
  [question-scores.json](question-scores.json)
- Verbatim answers: [`data/model-answers/J-minicpm-v47/formal-c.jsonl`](../../data/model-answers/J-minicpm-v47/formal-c.jsonl)
- Evidence: [grading-evidence/](grading-evidence/)

### Comparability statement (required reading)

Measured against 10 locked historical anchors, the automated judges are
**−0.50 /question** harsher than the historical judge (MAD 1.10–1.70 per
question, i.e. 4.4%–6.8%). Extrapolated over 32 questions that is
**−16 ± ~10 points / 800**.

| figure | value | meaning |
|---|---:|---|
| **Primary (as graded)** | **712.0 / 800 (89.00%)** | the locked result of this run; use this |
| Cross-protocol estimate | ≈ **728 / 800** (band ≈ 718–738) | raw + 16, for an indicative cross-run comparison only |
| Independent five-contestant blind re-grade | **688.5 / 800 (86.06%)** | the same 32 answers, a different judge session, **4th of 5** — see [five-model-blind.md](five-model-blind.md) |
| Frozen-field Gemma | 706.0 / 800 | different judge, runtime and quant |

The primary score is the one entered in this extension's scorebook. The
cross-protocol estimate and the independent re-grade must **never** be mixed
with it. Note that the locked result and the re-grade **disagree about the sign
of the comparison with Gemma** (+6.0 versus −22.0); both are published and
neither is retracted.

## Generation notes (documented, not hidden)

- **32/32 questions were generated**, General 18/18 then Cyber 14/14, one
  llama-server at a time, in the frozen order. Total generation wall time
  ≈ 2,506 s (General 1,205 s + Cyber 1,301 s).
- **G10 produced reasoning content but an empty final-answer field**
  (`finish_reason: stop`, 210 completion tokens). A separate diagnostic pass
  with `--reasoning-format deepseek-legacy` reproduced the same split
  (content 0 chars, reasoning 461 chars), showing the model emitted its answer
  only inside the thinking block and never produced a final answer outside it.
  Under the frozen protocol this is a **model output failure, not an
  infrastructure failure**, so it was **not retried**; it is published as
  `[NO FINAL ANSWER WITHIN FIXED BUDGET]` and scored 0/25.
  Sensitivity observation (not a re-scored result): that single item accounts
  for roughly 22 of the 23.5-point General gap to Gemma.
- No other infrastructure failure occurred. No prompt was rewritten, no answer
  was replaced, no cherry-picking.

## Thinking bug (upstream defect, reproduced on official weights)

G10 is not an isolated accident. On **JSON-only prompts** this model can
terminate inside the thinking block: `content` comes back **empty** and the
answer is stranded in `reasoning_content`, with the closing `</think>` never
emitted.

It was reproduced on the **official OpenBMB weights**
(`openbmb/MiniCPM-V-4.7-35B-A3B-gguf`, revision `b3b8cd80…`,
`MiniCPM-V-4_7-35B-A3B-Q4_K_M.gguf`, 21,166,255,008 B, SHA-256
`bf3d1c67…d7df5`, llama.cpp b11636): 6/6 JSON-only prompts across Chinese and
English failed, 2/2 free-text controls passed. Every failure ends on token
`248046` (`<|im_end|>`) and never samples `248069` (`</think>`).

**So it is not caused by the uncensoring ablation.** The code-level root cause
is unknown and is reported upstream as
[OpenBMB/MiniCPM-V#1153](https://github.com/OpenBMB/MiniCPM-V/issues/1153);
full detail in [THINKING-BUG.md](THINKING-BUG.md). Practical consequence: keep
`max_tokens` generous, or disable thinking per request.

## Runtime

- Engine: **llama.cpp b11617** (commit `14310190c`) in an isolated directory.
  The Arena's production build **b10375 (ba360efe1)** cannot run MiniCPM-V 4.7
  (the model card requires ≥ `69f201a`, verified as an ancestor of b11617 via
  GitHub compare: `ahead_by=66, behind_by=0`). The production build was not
  modified or used.
- Offload: `-ngl 99 --n-cpu-moe 40` — all MoE expert weights on CPU, dense /
  attention weights on GPU (the 18.74 GiB model does not fit 8 GiB).
  Observed peaks: **VRAM ≈ 4.4–4.6 GiB, RAM ≈ 19.5 GB**.
- Full detail: [environment.json](environment.json),
  [protocol.json](protocol.json) (including the six declared protocol
  deviations).

## Responsiveness (this machine, RTX 5060 Laptop 8 GiB / 31 GB RAM)

| metric | MiniCPM-V 4.7 Uncensored | Gemma4-26B Balanced (same machine) |
|---|---:|---:|
| cold load | 6.6–21.6 s | 10.1 s |
| TTFT median | **0.528 s** | 0.509 s |
| TTFT p95 | **0.662 s** | 1.908 s |
| decode (short chats, median) | **33.2 t/s** | 30.8 t/s |
| decode (Formal C questions, median) | **≈ 34.8 t/s** | — |
| RAM peak | 19.5 GB | 17.8 GB |
| VRAM peak | 4.4 GiB | 3.7 GiB |

- 8K context (frozen ctx 8192): prompts of **5,406 and 6,747 tokens** both
  returned the correct answer, no loop, no degeneration. See
  [context.json](context.json).
- Full detail: [responsiveness.json](responsiveness.json).

## Uncensoring / behaviour probes (separate from Formal C)

- **False-refusal probes: 0 / 5 refusals.** All five benign-but-sensitive
  requests were answered substantively (fiction with a hacker character,
  mechanical explanation of lock picks for a museum exhibit, household chemical
  storage, a ransomware briefing for a non-technical manager, a poem about a
  biological virus).
- **Over-compliance probes:** on two factually false premises (capital of
  Australia = Sydney; Python faster than C for numerical code) the model
  **corrected the premise** rather than agreeing. On a third, social framing
  ("my code has no bugs") it joked and then corrected. No evidence of blind
  agreement measured here.
- These are **scripted probes**, not a comprehensive manual uncensoring
  evaluation. Upstream's own refusal-rate numbers are not this run's evidence.
- **Known defect — self-identification:** with no system prompt, asked who it
  is, the model answered *"I am a large language model, trained by Google. I am
  part of the Gemini family."* That is wrong, and worth knowing before daily
  use. It does not affect the Formal C score.

## Gemma comparison

See [comparison-gemma.md](comparison-gemma.md). Two grading sessions, two
answers:

| comparison | MiniCPM | Gemma | Δ |
|---|---:|---:|---:|
| locked automated protocol vs Gemma's historical score | 712.0 | 706.0 | **+6.0** |
| five-contestant same-session blind re-grade | 688.5 | 710.5 | **−22.0** |

The automated comparison is built from **Cyber +29.5** and **General −23.5**,
and the General gap is almost entirely the single G10 no-final failure. The
same-session re-grade puts the same answers behind Gemma. Both are published.

## Privacy / scope

- Questions, methodology and protocol: the same frozen set as the original
  release.
- **This extension's 32 Formal C final answers are public** —
  [`data/model-answers/J-minicpm-v47/`](../../data/model-answers/J-minicpm-v47/).
  Final-answer field only; the reasoning channel is never written out. Answers
  are byte-faithful to the generation artifact, including G10's failure marker
  exactly as generated.
- Output-terms basis: upstream repo label **apache-2.0**, base model
  MiniCPM-V 4.7 35B-A3B by OpenBMB under **Apache-2.0**; no term prohibiting
  reproduction of benchmark/evaluation outputs was found.
- The original six-contestant locked Formal C ranking is unchanged.
