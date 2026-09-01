# METHODOLOGY — Reasoning Budget Arena (Formal D vs Formal C)

This document describes exactly how the two formal conditions were executed
and how they may (and may not) be compared. Every parameter was verified
against the experiment runners, raw records, and runtime logs — not
reconstructed from memory.

## 1. Research question

Under the same frozen 32-question benchmark and the same target 8192-token
server context window, how does applying a uniform, hard, backend-enforced
reasoning budget of 4096 tokens relate to (1) final-answer delivery,
(2) structural failure modes, (3) blind-scored final-answer quality, and
(4) relative model rankings — for six local LLMs?

The six models are the experimental subjects for this question; the project is
not a leaderboard in the usual sense.

## 2. The two conditions

| | **Formal D** | **Formal C** |
|---|---|---|
| server context (`ctx`) | 8192 | 8192 |
| request `max_tokens` | 8192 | 8192 |
| reasoning behaviour | native/default (no separate budget) | native/default **+ `--reasoning-budget 4096`** |
| sampling | temperature 0.1, top_p 0.9 | identical |
| chat template | each model's native/default (no system prompt) | identical |
| questions | same final frozen 32-question set | identical |
| MoE expert placement (`-ncmoe`) | per-model from GGUF metadata | identical values |
| server sequencing | one llama-server at a time | identical |
| infrastructure retries | max 1 identical retry on infrastructure failure only | identical policy |

### Core comparability statement

Formal D and Formal C used the same six-model set, the same final frozen
32-question benchmark, the same target 8192-token context envelope, and
closely matched sampling/runtime settings. Formal C additionally configured a
uniform native hard reasoning budget of 4096. **However, Formal D's published
baseline was assembled from a 29-question 8192 probe plus a later three-
question supplement, whereas Formal C was executed as one complete 32-question
run. The comparison is therefore exploratory and closely matched — not a
strict single-variable controlled experiment.** All result language in this
project follows from that: numbers are *observed under the two protocols*,
not claims that the budget *caused* them.

### The three different limits (never conflate)

| limit | value | enforced by |
|---|---|---|
| reasoning hard budget | **4096** | llama-server `--reasoning-budget` (Formal C only) |
| request `max_tokens` | **8192** | request-level completion cap |
| server context window | **8192** | total prompt + completion window |

"8192" appears twice with different meanings. Formal C raw records do **not**
store a per-response reasoning token count, so it is **not known which
individual responses actually hit the 4096 reasoning budget** — the budget is
known to have been configured and applied by the runtime for all 192 requests
(`reasoning_budget: 4096` present in every Formal C raw record), nothing more.

## 3. Formal D baseline provenance (composite)

The published Formal D baseline is a **composite** of two execution stages
run under the same Formal D settings:

| stage | what | responses |
|---|---|---|
| 1. 8192 probe | 29-question union (G1–G18 minus G1/G8/G10 = 15 General + 14 Cyber) × 6 models | 29 × 6 = **174** |
| 2. supplement | G1, G8, G10 × 6 models | 3 × 6 = **18** |
| **published Formal D baseline** | exact frozen 32-question set × 6 models | **192** |

Why the supplement exists: the earlier calibration work ran a 29-question
union (G1/G8/G10 were the only questions clean for all six at 4096 and were
held out of the probe union). The published Formal D baseline adds those three
questions back, run under the identical Formal D conditions, so that Formal D
and Formal C share the exact same final frozen 32-question set.

Provenance is recorded per row in `data/formal-d-objective.csv` (`source` =
`budget-probe-8192` or `formal-d-supplement`). The probe raw lives in the
experiment archive under `raw/budget-probe-8192/`; the supplement raw under
`raw/formal-d-supplement/`. Formal C is a single contiguous 32-question run
(raw under `raw/formal-c/`). Both conditions were scored under the same frozen
blind protocol.

**Implication for interpretation:** the two conditions match in target
settings and final question set, but their execution histories differ (D is
composite; C is contiguous). This is why the report describes differences as
"observed under the two protocols" and does not claim strict causal isolation.

## 4. Comparability and non-identity

**Matched / closely matched:**

- six model identities (same local GGUF files; SHA256 recorded in
  `data/model-artifacts.csv` and `MODEL-ARTIFACT-MANIFEST.md`)
- final frozen 32-question set (identical files in both conditions)
- target context window `ctx = 8192`
- request `max_tokens = 8192`
- sampling: temperature 0.1, top_p 0.9
- runtime family: llama.cpp `llama-server` b10375 (`ba360efe1`)
- quantized artifacts: identical per model (Q4_K_M; MoE expert placement
  `-ncmoe` from GGUF metadata)

**Not identical:**

- execution schedule/history (D composite probe+supplement; C one contiguous
  run)
- timestamps (D probe and supplement ran on 2026-09-01 morning/window; C ran
  13:35:30–18:02:02 on 2026-09-01)
- possible stochastic variation (temperature 0.1 is low but not zero; no
  seeds)

## 5. Models

Six local GGUF models, all Q4_K_M quantization. See MODEL-CARDS.md for the
verified details, MODEL-SOURCES (MODEL-SOURCE-TODO.md) for upstream links, and
`data/model-artifacts.csv` / `MODEL-ARTIFACT-MANIFEST.md` for SHA256 and size
evidence.

| experiment tag | model file | MoE experts on CPU (`-ncmoe`) |
|---|---|---|
| A | RavenX-CyberAgent-35B-v5.1-Q4_K_M.gguf | 256 |
| B | Endy-Qwen3.6-CyberSec-35B-A3B-Q4_K_M.gguf | 256 |
| C | Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-Q4_K_M.gguf | 128 |
| D | Ornith-1.5-35B-A3B-Abliterated-Q4_K_M.gguf | 256 |
| E | nex-agi_Nex-N2-mini-Q4_K_M.gguf | 256 |
| F | Qwen3.8-9B-abliterated-25.Q4_K_M.gguf | 0 (dense) |

## 6. Hardware and runtime

| item | value | source |
|---|---|---|
| GPU | NVIDIA GeForce RTX 5060 Laptop, 8 GiB VRAM (sm_120) | `docs/runtime-evidence.md` |
| backend | llama.cpp `llama-server`, build `ba360efe1` (b10375), Windows x86_64 | `docs/runtime-evidence.md` |
| OS | Windows (x86_64) | build tag |
| flags | `-ngl 99 --flash-attn on -t 24 -c 8192` | harness command construction |
| MoE experts | on CPU via `-ncmoe N` (8 GiB VRAM cannot hold the full MoE files) | `docs/runtime-evidence.md` |
| system RAM | not recorded in the experiment documents | — |
| FreeToken engine | not used in Formal D or Formal C | `docs/runtime-evidence.md` |

Speed results are RUNTIME-SPECIFIC and are never folded into answer quality.

## 7. Benchmark (frozen)

- **General — 18 questions (G1–G18):** logic, constrained reasoning, code
  generation, code review, debugging, structured output, instruction
  following, ambiguity handling, calibration, planning. Two questions (G15,
  G16) are time-sensitive current-fact items — see
  `docs/CURRENT-FACT-REFERENCES.md` for their evaluation-date sensitivity and
  provenance limits.
- **Cyber — 14 questions (C1–C14):** code audit, vulnerability locating,
  false-positive detection, exploitability reasoning, remediation, log
  analysis, CTF-style puzzles, tool planning, uncertainty judgment, threat
  modeling, hardening. Authorized/CTF/lab-only material. This is a
  **defensive / analysis-oriented security evaluation**, not an
  offensive-hacking benchmark.

Both divisions use the identical frozen question files
(`data/questions-general.json`, `data/questions-cyber.json`). One formal run
per (condition, model, question); no repeats in the formal runs.

## 8. Raw record contents

Each Formal C raw JSONL record stores: `id, tag, prompt, response (= API
message.content), reasoning (= API reasoning_content), usage
(completion_tokens, prompt_tokens, total_tokens), timings (prompt/predicted
counts and milliseconds), wall_ms, gen_ts, pp_ts, reasoning_budget, ctx,
max_tokens, temperature, top_p, ncmoe`.

Not stored: `finish_reason`, any per-response reasoning-token count. This is
why per-response reasoning-budget usage is reported as NOT DIRECTLY
MEASURABLE throughout the public materials.

Formal D probe/supplement records (older harness output) store a subset:
`id, tag, prompt, response, reasoning, usage, timings, wall_ms, gen_ts,
pp_ts` — without `ctx/max_tokens/reasoning_budget` fields. Consequently some
Formal D columns are D-NOT-COMPUTABLE; the two objective CSVs are documented
**separately** in DATA-DICTIONARY.md.

## 9. Blind evaluation protocol

- Answers were packaged with six **opaque contestant IDs**; the mapping was
  sealed during scoring and revealed only after score lock. The archived
  artifacts (sanitized copies in `blind/`) record that scores were locked
  before identity reveal; this is an author-recorded process audit trail, not
  cryptographic proof.
- The blind package contains **final answers only** — no reasoning channel,
  no model names, no architecture/quantization, no speeds, no token counts.
- Contestant **presentation order was randomized independently per question**.
- Judges score five dimensions per answer, each **0–5**: Correctness,
  Completeness, Visible reasoning/result quality, Instruction following,
  Practical usefulness. Maximums: 25/question; General 18×25 = **450**; Cyber
  14×25 = **350**; Overall **800**.
- Formal D and Formal C were scored under the **same frozen judge protocol**
  (`blind/BLIND-JUDGE-INSTRUCTIONS.md`).
- Structural annotations (loop / truncation / clean) were NOT shown to judges
  and did NOT filter answers.

### Post-lock identity reveal (audit trail)

The mapping was sealed during scoring and revealed only after the lock. It is
published solely as the evaluation audit trail; it did not and cannot change
any locked score.

| condition | contestant → experiment tag / model |
|---|---|
| Formal D | H45 = D (Ornith-1.5-35B-A3B), S41 = B (Endy-Qwen3.6-CyberSec), X68 = C (Gemma4-26B-A4B), W87 = A (RavenX-CyberAgent), Y76 = E (Nex-N2-mini), P40 = F (Qwen3.8-9B-abliterated) |
| Formal C | T50 = A (RavenX-CyberAgent), V32 = B (Endy-Qwen3.6-CyberSec), S47 = C (Gemma4-26B-A4B), X49 = D (Ornith-1.5-35B-A3B), W60 = E (Nex-N2-mini), H86 = F (Qwen3.8-9B-abliterated) |

## 10. Structural post-run analysis (same detector for both conditions)

The structural audit applies one explicit detector to both conditions (as far
as the raw schema allows) and then manually reviews every candidate.

**Candidate heuristic (exact):** a record is a `loop_candidate` iff **any** of:

- `near_context_limit` is true (`prompt_tokens + completion_tokens >= 8192`),
  OR
- duplicated-10-word-shingle rate `dup10 >= 0.30`, OR
- the same stripped line (>= 40 chars) appears >= 3 times.

The reasoning-marker count is computed and recorded in the loop-audit CSV as a
review aid only; it is **not** part of the candidate expression. (This
documentation matches the implementation in `scripts/formal_c_objective.py`
and `scripts/formal_d_objective.py`.)

**Heuristic ≠ verdict.** Every candidate was manually reviewed against the
actual final content before a `confirmed_loop` value was recorded
(`data/formal-{d,c}-loop-audit.csv`). Long answers, near-cap records,
templated lists and short complete answers are NOT automatically loops.

**Audit workflow (Formal D):** candidate detection and manual verdicts are
two separate stages. `formal_d_objective.py --init-audit` only generates a
candidate template (verdicts `UNREVIEWED`) when the audit file is missing and
refuses to overwrite an existing one. The normal run reads the existing
manual audit and **fails closed** on any candidate whose verdict is missing,
duplicated, or UNREVIEWED; it never writes to the audit file. The script
therefore **never auto-confirms loops** — the manual verdicts are the source
of truth and are immutable for analysis.

**D limitation:** Formal D probe/supplement records lack `ctx/max_tokens`
fields, so `near_generation_cap` is D-NOT-COMPUTABLE; `ctx` is taken from the
documented protocol value. The detector itself is identical.

**Result (both conditions, same detector, manual review):**

| condition | candidates | confirmed content-channel loops | structurally clean finals |
|---|---|---|---|
| Formal D | 77 (73 empty-final + 4 truncated non-loop) | **0** | **115/192** |
| Formal C | 9 (8 context-exhausted + 1 shingle artifact) | **6** | **184/192** |

`clean_final` = has_final AND not a confirmed loop AND not context-truncated.
Structural only — says nothing about correctness or quality.

## 11. Reproducibility

Path contract, commands, and a clean-room path test are documented in
REPRODUCIBILITY.md; `scripts/test_release_paths.py` verifies the runner↔
harness↔integrity path agreement **without running any model**. Generation
reproducibility claims are limited to what that test and the archived
protocol can establish; stochastic/backend/quantization effects mean exact
responses are not reproducible.

## 12. Causal-language policy

The experiment is an exploratory paired comparison with one sample per cell,
no seeds, no replicates. Public materials use *observed under*, *associated
with*, *coincided with*, *in this run*, *under this protocol* — and never
*caused*, *proves*, *eliminates*, *optimal*, *fair*, or *significant* in the
statistical sense. Technical mechanisms with direct code evidence (e.g. the
runtime accepting `--reasoning-budget 4096`) may still be described as
mechanisms.
