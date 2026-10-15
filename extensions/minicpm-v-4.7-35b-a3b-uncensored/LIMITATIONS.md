# Limitations — MiniCPM-V 4.7 35B-A3B Uncensored extension

## 1. Not comparable with the frozen six-contestant ranking

This extension is graded under **Automated Blind Grading — New Judge Protocol**
(see `grading-method.md`). The historical judge was a different session. Anchor
calibration against 10 locked historical items shows a consistent
**−0.50 /question** bias (≈ −16 / 800) and a per-question MAD of 1.10–1.70
(4.4%–6.8%). Any cross-run comparison must carry that band. The frozen
six-contestant ranking is unchanged and is not merged with this score.

## 2. Different runtime

The historical Formal C field used llama.cpp **b10375** (build `ba360efe1`).
This model's card requires llama.cpp at or after **69f201a**, so this extension
used llama.cpp **b11617** (commit `14310190c`) in an isolated directory. The
production llama.cpp build was not touched. Results are therefore
**same prompt/protocol, same hardware, NOT same runtime**.

## 3. Different quantization and offload strategy

- Quantization: AtomicChat `AD-Q4_K-IQ4_XS` (20,125,154,976 bytes, 11 shards).
  The frozen field and prior extensions were Q4_K_M builds. This is the only
  uncensored build of this model that fits this 8 GiB machine.
- Offload: the 18.74 GiB model cannot fit in 8 GiB VRAM. All MoE expert weights
  were placed on CPU (`--n-cpu-moe 40`); dense/attention weights on GPU
  (observed peak ≈ 4.4–4.6 GiB VRAM, ≈ 17–18 GB RAM). The historical field
  offloaded whole models at `-ngl 99`. CPU-side MoE changes the speed profile
  and is a real difference, but it does not change the questions, the sampling
  parameters, or the answers' content.

## 4. Vision was not evaluated

The model is a multimodal (image-text-to-text) build. This run is **text-only
Formal C**. No `mmproj` was downloaded or loaded, and `llama-server` reported
`modalities: {vision: false, video: false, audio: false}` for this session. No
claim is made about image or video capability.

## 5. Single run, no repeats

One formal generation pass per question, as the frozen protocol requires. No
significance claim is made from a single run.

## 6. Empty final answer (G10) — disclosed, not hidden

One General question (G10) produced reasoning content but an empty final-answer
field. A separate diagnostic pass was run to determine whether this was a model
failure or a runtime extraction artifact; the finding and its handling are
recorded in the run archive and summarised in `README.md` § Generation notes.
Under the frozen protocol the answer is published as
`[NO FINAL ANSWER WITHIN FIXED BUDGET]` and is scored 0/25. No re-prompt, no
answer replacement, no cherry-picking.

## 7. Uncensoring evaluation is partial

- The model is AtomicChat's refusal-direction-ablated build; upstream reports
  0% refusals on their held-out sets. **Upstream numbers are not this run's
  evidence.**
- This run's own evidence is a small scripted probe set (benign requests that
  over-aligned models commonly false-refuse, plus sycophancy / over-compliance
  probes). It is reported separately from Formal C and is **not** a
  comprehensive manual uncensoring evaluation.
- Output-terms review: upstream repo license label **apache-2.0**; base model
  MiniCPM-V 4.7 35B-A3B by OpenBMB under Apache-2.0. No term prohibiting
  reproduction of benchmark/evaluation outputs was found in the model card.

## 8. Judge platform limitation

The judge sub-agents available on this platform have read-only tool access and
cannot write files. Scores were returned as JSON in the judge's reply and
transcribed verbatim by the coordinator. Every transcribed item was checked for
internal arithmetic consistency (sum of the five dimensions equals the judge's
reported total).

## 9. Repository validator state

`scripts/validate_public_release_preview.py` **already failed before this
extension was added** (two pre-existing failures: the public-answer total and
the README count were left at 288 while the tree already contained 320 after
Extension 2). That pre-existing drift is not caused by this extension and is
reported as-is in the pull request. See §10 of the run report.

## 10. Deployment outcome (decided)

This extension was an evaluation. Nothing was installed, no launcher was
changed, the Hermes default model was not switched, and the incumbent Gemma
build was never touched or replaced. **The model was not retained**: after the
evidence was archived, both MiniCPM GGUF sets (the AtomicChat build and the
official OpenBMB control used for the Thinking-bug check) were deleted on
2026-10-15. The rest of this file records the limitations **as measured during
the run** and is kept as history, not as a live recommendation.

## 11. Two review protocols — not two measurements of the same thing

The locked result of this extension is **712.0 / 800** (*Automated Blind
Grading — New Judge Protocol*, the original automated review). Separately, the
same 32 answers were scored in one **five-contestant anonymous blind session
judged by ChatGPT** (AI-assisted / automated judging — **not** human judging),
giving **688.5 / 800 (4th of 5)** against Gemma4-26B's **710.5** in that same
session, i.e. **−22.0**.

- The session is not systematically stricter: the four contestants with
  historical scores all scored above their historical values in it (+10.0,
  +0.5, +4.5, +9.0; mean +6.0).
- The locked score is **not** changed by this. Both numbers are archived in
  `five-model-blind.md` and in `scores.json` under `independent_cross_check`.
- **712.0 − 706.0 = +6.0 is cross-protocol arithmetic** (different judge,
  runtime and quantization) and must **not** be read as a win/loss verdict. The
  only like-for-like comparison is the same-session **−22.0**.
- The early ≈ **728 / 800** anchor extrapolation is retained only as a
  historical heuristic estimate; it is not valid evidence that this model beats
  Gemma.
- These two numbers are not competing candidates for "the true score" — they
  belong to different protocols, so no third review is required to arbitrate.

## 12. Thinking early-EOS — not unique to the decensored checkpoint, cause unknown

On JSON-only prompts **without a system prompt**, `content` can come back empty
with the answer stranded in `reasoning_content`; `</think>` is never sampled and
generation ends on `<|im_end|>` after only 18–24 tokens — far below the 4,096
reasoning budget, so this is not a budget-exhaustion event. Adding a system
prompt (arm D) returned **3/3 normal** responses on the official weights.

The same termination pattern was reproduced on the official OpenBMB Q4_K_M
weights, so the failure is not unique to the decensored checkpoint. The
underlying cause remains unknown: quantization, chat template, runtime and
training factors were **not** excluded.

Also **not** established: how often this happens outside these settings (fixed
seeds make these deterministic replays, not independent samples), that G10
failed because of the token budget, and that raising `max_tokens` fixes it.
G10's published marker `[NO FINAL ANSWER WITHIN FIXED BUDGET]` is the frozen
protocol's label, not proof of a cause. See `THINKING-BUG.md` and upstream
issue [OpenBMB/MiniCPM-V#1153](https://github.com/OpenBMB/MiniCPM-V/issues/1153).
