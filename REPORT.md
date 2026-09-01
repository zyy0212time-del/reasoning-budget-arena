# Reasoning Budget Arena — Technical Report

*Final-answer delivery, structural failures, and ranking differences under two
reasoning policies (native vs fixed reasoning-budget) across six local LLMs.*

**Status: RELEASE CANDIDATE.** Objective and blind-scored results are both
verified: every score below was recomputed from the question-level locked
scorebooks and matched exactly against the artifacts' own aggregation and rank
tables. The remaining items are the maintainer's project-license decision, a
documented model-source limitation (F), and final human review — see
RELEASE-READINESS.md.

## Abstract

Six local LLMs (all Q4_K_M GGUF) answered the same final frozen 32-question
benchmark (18 General + 14 Cyber) under two protocol conditions with the same
target 8192-token server context window and closely matched sampling/runtime
settings (temperature 0.1, top_p 0.9, native chat templates, one server at a
time). The conditions differed in reasoning policy: Formal D used each model's
native/default thinking with no separate budget; Formal C additionally
configured a uniform, hard, backend-enforced reasoning budget of 4096 tokens.

The two conditions are **closely matched, not identical in execution
history**: Formal D's published baseline is a composite of a 29-question
8192 probe (174 responses) plus a later 3-question supplement (18 responses,
G1/G8/G10) that completes the same final 32-question set; Formal C was one
complete 32-question run (192 responses). All differences below are therefore
*observed under the two protocols*, not attributed to the budget causally
(METHODOLOGY.md §2–§4).

Under the native-thinking condition, 119 of 192 responses (61.98%) produced a
non-empty final answer; 73 produced none — in most cases the reasoning channel
consumed the available window before any final appeared. Under the
fixed-budget condition, all 192 responses produced a non-empty final (0 empty
finals observed in this run), 184 of them structurally clean; the residual
failures appeared in the final channel itself (6 manually confirmed
degenerate loops, 2 context-truncated non-loop answers).

Blind final-answer scores were collected for both conditions under a frozen
judge protocol and locked before any identity reveal. Every model scored
higher under the budget condition; the largest overall gain was Nex-N2-mini
(353.0 → 746.5, overall rank #4 → #1), while the two next-largest gains (Qwen
9B +302.5, RavenX +274.5) did not change those models' rank. Neither
Cyber-branded model placed in the top three of the 14-question Cyber division
under Formal C. These results are descriptive: one sample per cell, no seeds,
no replicates, one blind judge, no statistical inference (see §14).

## 1. Motivation

Local thinking-capable models routinely spend thousands of tokens reasoning
before answering. Under a fixed context window, unrestricted reasoning can
consume the entire envelope, leaving no room for a final answer. This project
asks whether a *uniform hard cap on the reasoning phase* — enforced by the
inference runtime, not by prompting — changes what gets delivered, at what
structural cost, and (via blind scoring) with what effect on final-answer
quality and relative rankings.

## 2. Research question

Under the same frozen benchmark and fixed 8192-token context window, how does
a uniform 4096-token hard reasoning budget affect (1) final-answer delivery,
(2) structural failure modes, (3) blind final-answer quality, (4) relative
model rankings? The six models are the experimental subjects for this
question, not a leaderboard in the usual sense.

## 3. Models

Six local GGUF models, all Q4_K_M (details and provenance caveats in
MODEL-CARDS.md):

| tag | model file | class |
|---|---|---|
| A | RavenX-CyberAgent-35B-v5.1 | Qwen3.6-35B-A3B MoE class (256 experts) |
| B | Endy-Qwen3.6-CyberSec-35B-A3B | Qwen3.6-35B-A3B MoE class (256 experts) |
| C | Gemma4-26B-A4B-QAT | Gemma4-class MoE (128 experts) |
| D | Ornith-1.5-35B-A3B | Qwen3.5-35B-A3B MoE class (256 experts) |
| E | Nex-N2-mini | Qwen-style 35B MoE class (256 experts) |
| F | Qwen3.8-9B-abliterated-25 | ~9B dense |

Two of the six (A, B) are Cyber-branded fine-tunes. Parameter counts are from
filenames/GGUF metadata and are not independently verified.

## 4. Hardware and runtime

- GPU: NVIDIA GeForce RTX 5060 Laptop, 8 GiB VRAM (sm_120); MoE experts on
  CPU (`-ncmoe`) because the 35B-A3B Q4_K_M files do not fit in VRAM.
- Backend: llama.cpp `llama-server` build `ba360efe1` (b10375), Windows
  x86_64. Flags: `-ngl 99 --flash-attn on -t 24 -c 8192`.
- No system prompt; each model's native chat template; native/default
  thinking in both conditions. The FreeToken engine was not used.
- One server at a time; per-division server logs retained in the experiment
  archive.
- System RAM was not recorded in the experiment documents.

## 5. Benchmark

Frozen, original question sets authored for this project:

- **General (G1–G18)**: logic, constrained reasoning, code generation and
  review, debugging, structured output, instruction following, ambiguity
  handling, calibration, planning.
- **Cyber (C1–C14)**: code audit, vulnerability locating, false-positive
  detection, exploitability reasoning, remediation, log analysis, CTF-style
  puzzles, tool planning, uncertainty judgment, threat modeling, hardening.
  Authorized/lab-only material; a defensive, analysis-oriented evaluation.

One formal sample per (condition, model, question): 6 × 32 = 192 responses
per condition, 384 total.

## 6. Formal D (native thinking, no reasoning budget — composite baseline)

Closely matched configuration (ctx 8192, max_tokens 8192, temperature 0.1,
top_p 0.9) with **no reasoning budget**. Its published baseline is **composite
by construction**: a 29-question 8192 probe (174 responses) plus a later
G1/G8/G10 supplement (18 responses) that completes the exact final frozen
32-question set shared with Formal C (METHODOLOGY.md §3). Verified results
(`data/formal-d-objective.csv`):

- non-empty finals: **119/192 (61.98%)**; empty finals: **73**
- per-model finals: A 14, B 24, C 25, D 25, E 15, F 16 (of 32)
- context-window exhaustion (prompt+completion ≥ 8192): 77 records
- structurally clean finals (same definition as Formal C, applied by the same
  audit): 115/192

The dominant failure: the reasoning channel consumed the available window and
no final answer was produced.

## 7. Budget calibration (why 4096)

The policy was not chosen up front; it emerged from a sequence of small,
controlled probes (full narrative: docs/CALIBRATION-HISTORY.md):

1. An early max_tokens=1024 round was **invalid as an ability test** (reasoning
   consumed the cap; finals were mostly missing).
2. A max_tokens=4096 round still left 61–75% empty finals per model.
3. An 8192 round (the eventual Formal D envelope) still left 73/174 empty.
4. The runtime's native `--reasoning-budget` was identified and verified as a
   hard, backend-level mechanism.
5. A 512 six-model smoke showed the mechanism worked but was too tight for
   two models (degenerate transitions).
6. 1024/2048 calibration still degenerated for one model — but a control run
   showed that model also failed **without** the intervention on that prompt.
7. A second, unambiguous diagnostic prompt did **not** reproduce the
   instability (4/4 healthy), localizing the earlier failures to a prompt-
   specific ambiguity rather than the budget mechanism.
8. A six-model validation at 4096 on the clean prompt: 5/5 healthy plus the
   previously affected model 2/2 healthy → 4096 adopted as operationally
   viable, and Formal C was run.

A suspected reasoning-budget runtime bug was investigated and **not** upheld
— the control runs prevented a false upstream report. No llama.cpp issue or
PR was filed.

## 8. Formal C (uniform 4096 budget, single contiguous run)

Same target settings as Formal D plus `--reasoning-budget 4096`
(server-level, hard), executed as **one complete 32-question run**.
Verified results (`data/formal-c-objective.csv`):

- non-empty finals: **192/192**; empty finals: **0 observed in this run**
- structurally clean finals: **184/192 (95.8%)**
- confirmed content-channel loops: **6** (A/G4, B/C9, C/C9, F/C2, F/G3, F/G4 —
  each manually verified against the actual content)
- context-truncated non-loop answers: **2** (A/C1, B/C8)
- context-window exhaustion (prompt+completion = 8192 exactly): **8** records
  (max completion 8093 — `max_tokens` was never the binding limit)

Per-response reasoning-budget usage is **NOT DIRECTLY MEASURABLE** (no
per-response reasoning token count stored): the budget is known to have been
uniformly configured and applied, nothing more.

## 9. Blind evaluation

Both conditions were scored under the same frozen protocol
(`blind/BLIND-JUDGE-INSTRUCTIONS.md`): six opaque contestant IDs per
condition, mapping sealed until score lock; final answers only (no reasoning,
no identities, no speeds, no token counts); presentation order randomized per
question; five dimensions × 0–5 per answer (Correctness, Completeness, Visible
reasoning/result quality, Instruction following, Practical usefulness);
maximums 25/question → 450 General + 350 Cyber = 800 Overall. Structural
annotations were never shown to judges and never filtered answers.

## 10. Results (objective)

See RESULTS.md for the verified tables and figures:
delivery 119/192 → 192/192; structurally clean 115 → 184; failure mode
shift from empty-finals to a smaller set of content-channel loops and
truncations; context exhaustion 77 → 8.

## 11. Blind-scored results

All values below were recomputed from the question-level locked scores in
`blind/FORMAL-{D,C}-BLIND-SCORES-LOCKED.md` and matched exactly against the
artifacts' own aggregation tables and rank tables before use
(6/6 contestants, both conditions; 192 records each; every question total
equals the sum of its five locked dimensions).

| model | D Overall /800 | C Overall /800 | Δ | rank D → C |
|---|---:|---:|---:|---|
| Nex-N2-mini | 353.0 | **746.5** | +393.5 | 4 → **1** |
| Ornith-1.5-35B-A3B | **569.5** | 725.5 | +156.0 | 1 → 2 |
| Gemma4-26B-A4B | 540.5 | 706.0 | +165.5 | 2 → 3 |
| Endy-Qwen3.6-CyberSec | 526.0 | 644.0 | +118.0 | 3 → 4 |
| Qwen3.8-9B-abliterated | 332.5 | 635.0 | +302.5 | 5 → 5 |
| RavenX-CyberAgent-35B | 301.5 | 576.0 | +274.5 | 6 → 6 |

- **Every model scored higher** under the budget condition.
- **Absolute gain and rank movement are different things**: the two largest
  gains after Nex (Qwen 9B +302.5, RavenX +274.5) left both models at the same
  overall rank, because they also started furthest behind. The only upward rank
  movement was Nex (+3).
- Division detail, normalized percentages, and the structural-vs-scored
  comparison are in RESULTS.md.

### 11.1 Case study — Nex

The most pronounced change in the experiment. Under Formal D, Nex delivered
15/32 finals and scored 353.0 (#4), with a striking split: General 290.0 (#2)
but Cyber 63.0 (#6). Under Formal C it delivered 32/32 and scored 746.5 (#1),
winning **both** divisions (General 418.5 #1, Cyber 328.0 #1).

**Selection-bias caveat (delivered answers are conditional on delivery):**
under Formal D, 17 of Nex's 32 questions produced no final at all. The
"answered-final average was already very high" observation is computed **only
over the 15 answers that were delivered**. Missing answers are not a random
sample — the questions without finals may be precisely the ones where Nex
would have scored poorly had it delivered. A high average over delivered
answers therefore does **not** estimate latent answer quality on the missing
questions; it bounds the interpretation of the Formal D score.

With that bound, the pattern is **consistent with** Nex having competitive
answer quality when it delivered, while its default/unrestricted reasoning
exhibited poor budget management on this hardware/context envelope. The
experiment does not isolate that mechanism, and the word used here is
*consistent with*, not *proves*.

### 11.2 Case study — Ornith

Ornith led Formal D (569.5 #1) and placed second under Formal C (725.5 #2),
with General #3 and Cyber #2 under Formal C. In this benchmark it was
**robust across both conditions**, and it was one of only two models with
zero structural failures under Formal C (32/32 structurally clean finals).
No claim beyond this benchmark is made.

### 11.3 Case study — Gemma4

Gemma4 led the Formal D Cyber division (271.0 #1) and placed third under
Formal C (291.5 #3), while improving strongly in General (269.5 → 414.5,
#4 → #2). Its Formal C profile is the most balanced across the two divisions.
**Cyber-branded specialization did not guarantee superiority over this
general-purpose model** in the Cyber division under either condition — an
observation about these specific models on 14 questions.

### 11.4 Case study — Qwen 9B (small/fast model)

The smallest model in the field improved from 332.5 (#5) to 635.0 (#5),
finishing 9 points behind Endy overall (635.0 vs 644.0) and 20.5 points behind
it in Cyber (266.5 vs 287.0). Under this protocol a small/fast model became
highly competitive with much larger MoE models. Speed was scored separately and
never folded into quality. Parameter counts are not independently verified
(MODEL-CARDS.md).

## 12. Failure modes

These are different phenomena and are never conflated
(docs/FAILURE-MODE-ANALYSIS.md):

- **EMPTY FINAL** — reasoning consumed the window; no final content.
- **CONTENT LOOP** — degenerate repetition inside the final channel
  (manually confirmed only).
- **CONTEXT EXHAUSTION** — prompt+completion reached the 8192 window.
- **STRUCTURALLY CLEAN** — none of the above; says nothing about correctness.
- **CORRECTNESS FAILURE** — a judge judgement, out of scope for structural
  analysis.

## 13. Cyber division

The Cyber division is a 14-question defensive/analysis-oriented evaluation.

Under Formal C, the Cyber top three were Nex (328.0), Ornith (320.5) and
Gemma4 (291.5). **Neither of the two Cyber-branded models placed in the top
three of the 14-question Cyber division under Formal C** — Endy was #4 (287.0)
and RavenX #6 (256.5). Under Formal D the Cyber ordering was Gemma4 #1,
Endy #2, Ornith #3.

This is an observation about two specific fine-tunes, at specific
quantizations, on 14 questions, in a single run. It does not support claims
about security fine-tuning in general, and it says nothing about offensive
capability (the division is defensive/analysis-oriented by design).

## 14. Limitations

Full list in LIMITATIONS.md (design, evaluation, measurement, and scope
limits, including: no seeds/replicates/CIs; one judge; reasoning-token usage
unmeasured per response; no claim that 4096 is optimal; no universal
ranking).

## 15. Reproducibility

REPRODUCIBILITY.md covers runtime, config, exact commands, runner semantics,
and what will not reproduce (exact responses, judge scores).

## 16. Conclusion

In this exploratory paired comparison, the condition with a uniform hard
4096-token reasoning budget (Formal C, one contiguous 32-question run) was
followed by complete final-answer delivery (192/192 vs 119/192), by a higher
overall blind score for every model, and by one substantial rank change at the
top (Nex #4 → #1) — all *observed under the two protocols*. The residual
failure mode did not disappear; it appeared in the final content channel
(6 loops + 2 truncations vs 73 empty finals). The 4096 budget was
operationally viable across all six models under this protocol.

These are descriptive results from one sample per (condition, model, question)
with a single blind judge, no seeds, no replicates and no confidence
intervals, and from two conditions whose execution histories are closely
matched but not identical (Formal D composite, Formal C contiguous). They are
**consistent with** reasoning-budget management being an important factor in
fixed-envelope evaluation, but the design does not isolate the mechanism,
does not establish 4096 as optimal, and does not establish a universal model
ranking.

## 17. Future work

Multiple seeds and repeated trials; a budget sweep (2048/3072/4096/6144);
more models; a larger question bank; separate coding and Chinese-dialogue
benchmarks; agent/tool-use tasks; long-context workloads; a stronger Cyber
suite; multiple blind judges with inter-rater reliability; bootstrap
confidence intervals; latency/quality trade-off analysis.
