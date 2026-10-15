# Comparison with the incumbent Gemma — MiniCPM-V 4.7 35B-A3B Uncensored

This file answers the practical question that motivated the run: *is this model
a credible replacement for the Gemma build currently in daily use on this
machine?*

## 0. Which Gemma, exactly

| | |
|---|---|
| file | `.../Gemma4-26B-A4B-QAT-Uncensored-MTP-Q4_K_M/Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-Q4_K_M.gguf` (local model directory on the benchmark machine) |
| size | 16,796,015,520 bytes |
| SHA-256 | `3c13133469e431312fffb8b1d9c85ae42199e6bb5746ea1da84e8ddf2097d73c` |
| identity check | **byte-identical** to the artifact recorded in `data/model-artifacts.csv` for experiment tag **C** (= Formal C blind contestant **S47**) |
| quant | Q4_K_M |
| production launcher | `armory.bat start-gemma26`: llama.cpp b10375, `-ngl 99 --n-cpu-moe 999 -fa on -c 65536 --cache-type-k q8_0 --cache-type-v q8_0 --jinja --parallel 1`, port 30003 |
| Arena result reused | Formal C **706.0 / 800** — General 414.5 / 450, Cyber 291.5 / 350, rank 3 of the frozen six-model field |

**The local Gemma is the same artifact that produced the historical 706.0
score**, so that score is directly reusable and was not re-measured. No new
Formal C run was spent on Gemma.

## 1. Capability delta (Formal C, same frozen questions)

| | Gemma4-26B (frozen field, S47) | MiniCPM-V 4.7 Unc. (ext I, K71) | Δ |
|---|---:|---:|---:|
| General /450 | 414.5 | 391.0 | **−23.5** |
| Cyber /350 | 291.5 | 321.0 | **+29.5** |
| **Overall /800** | **706.0** | **712.0** | **+6.0** |

Calibrated view: the automated judges score ≈ −16 / 800 versus the historical
judge, so the cross-protocol estimate for MiniCPM is ≈ **728 / 800** (band
≈ 718–738) against Gemma's 706.0 — a difference that survives the calibration
band.

**Caveats that must travel with that number:** different judge protocol,
different llama.cpp build (b11617 vs b10375), different quantization
(AD-Q4_K-IQ4_XS vs Q4_K_M), different MoE placement (all MoE on CPU here).
Only the questions, sampling parameters, budget, rubric and the machine are
identical.

**Where the General gap comes from.** 22 of the 23.5 General points are the
single G10 no-final failure (scored 0/25). Excluding that one item the two
General subtotals are effectively level. This is stated as a sensitivity
observation only — the locked score remains 391.0.

### 1b. The same comparison in one blind session with five contestants

A separate blind session scored **five** contestants over the same 32 questions
in one pass (160 rows, final answers only, reasoning withheld). It gives the
opposite sign:

| | MiniCPM-V 4.7 Unc. | Gemma4-26B | Δ |
|---|---:|---:|---:|
| General /450 | 374.0 | 410.5 | **−36.5** |
| Cyber /350 | 314.5 | 300.0 | **+14.5** |
| **Overall /800** | **688.5** | **710.5** | **−22.0** |

MiniCPM finishes **4th of 5** in that session (behind Nex 756.5, Old Ornith
726.0 and Gemma 710.5, ahead of Qwen3.8-abliterated 644.0). The session is not
systematically harsh: the four contestants that have historical scores all came
out above them (+10.0, +0.5, +4.5, +9.0).

Full record: [five-model-blind.md](five-model-blind.md). The locked 712.0 is
unchanged; **both** comparisons are published.

## 2. Speed delta (same machine, same probe script)

| metric | MiniCPM-V 4.7 Unc. | Gemma4-26B | note |
|---|---:|---:|---|
| cold load | 6.6–21.6 s | 10.1 s | MiniCPM on b11617, Gemma on b10375 |
| TTFT median | 0.528 s | 0.509 s | tie |
| TTFT p95 | **0.662 s** | 1.908 s | MiniCPM has a much tighter tail |
| decode, short chats (median) | **33.2 t/s** | 30.8 t/s | |
| decode, Formal C questions (median) | ≈ 34.8 t/s | — | General 34–35, Cyber 35 |
| prefill at 8K | ≈ 310–315 t/s | ≈ 343–362 t/s | Gemma faster at prefill |
| RAM peak | 19.5 GB | 17.8 GB | MiniCPM needs ~1.7 GB more |
| VRAM peak | 4.4 GiB | 3.7 GiB | both comfortable |

MiniCPM is **not slower in practice** despite being a 35B-A3B model on an
8 GiB card: it ties Gemma on TTFT median, beats it on TTFT p95 and on decode,
and loses only on long-prompt prefill.

**8K context (frozen ctx 8192), observation, not a benchmark result:** with
prompts of 5,406 and 6,747 tokens MiniCPM returned the correct answer both
times; Gemma returned an **empty final answer** in both probes. This is
confounded — MiniCPM ran with the frozen `--reasoning-budget 4096` that caps
thinking, Gemma ran with its own default (no cap) and at ctx 8192 rather than
its production ctx 65536. Reported as an observation only.

## 3. Refusal / over-refusal

| | MiniCPM-V 4.7 Unc. | Gemma4-26B |
|---|---|---|
| false-refusal probes refused | **0 / 5** | **0 / 5** |
| corrects a factually false premise | 2 / 2 | not measured in this run |

Both are non-refusing on this small scripted set. MiniCPM did **not** show
blind agreement on the two factual false premises it was given (it corrected
"capital of Australia is Sydney" and "Python is faster than C for numerical
code"). On a social framing ("my code has no bugs") it joked and then
corrected. This matters because "uncensored" is not only about not refusing —
a model that agrees with everything is worse, not better.

## 4. Practical differences that the score does not capture

- **Memory.** MiniCPM needs ≈ 19.5 GB RAM peak versus Gemma's ≈ 17.8 GB. On a
  31 GB machine this is workable but leaves noticeably less headroom alongside
  a browser and desktop apps.
- **Multimodal capability it is not being used for.** This is a vision-capable
  build; this run is text-only and loaded no `mmproj`. On this machine the
  vision path is dead weight unless the maintainer wires up a projector
  (+ ~1.1 GB) and accepts more memory pressure.
- **Self-identification defect.** With no system prompt it claims to be a
  Google Gemini model. Gemma at least self-identifies plausibly. This does not
  affect benchmark scores but it does affect day-to-day trust.
- **Thinking is on by default** with this model's template. Short answers still
  arrive fast (TTFT median 0.53 s) but every turn pays a thinking cost; with a
  small `max_tokens` the model can spend the whole budget thinking and return
  nothing (exactly what happened on G10). Any real deployment should keep
  `max_tokens` generous or disable thinking per request.

## 5. Conclusion

**PROMISING — low-to-medium confidence, and NOT demonstrated as better than
Gemma.**

- Under the **locked automated protocol** it scores **above** the incumbent
  Gemma on the frozen Formal C set (712.0 raw, ≈ 728 calibrated, vs 706.0),
  driven by a large **Cyber +29.5** and offset by a **General −23.5** that is
  almost entirely one no-final failure.
- Under the **independent five-contestant same-session blind re-grade** it
  scores **below** Gemma (688.5 vs 710.5, **−22.0**, 4th of 5). The two
  sessions disagree; this is the single largest uncertainty about the model.
- It is **at least as fast** in the ways that are felt day to day (TTFT p95
  0.66 s vs 1.91 s; decode 33.2 vs 30.8 t/s).
- It shows **no false refusals** and **no measurable sycophancy** on the probes
  used here.
- The confidence is medium, not high, because the runtime, the quantization,
  the MoE placement and the judge all differ from the historical run, and
  because the uncensoring evidence here is a small scripted probe set rather
  than a manual trial.

**It is not installed and Gemma is not replaced.** The maintainer's own
hands-on uncensoring trial is the deciding test.
