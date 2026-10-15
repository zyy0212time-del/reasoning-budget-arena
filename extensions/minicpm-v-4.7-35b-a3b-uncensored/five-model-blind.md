# Independent cross-check — five-contestant same-session blind re-grade

**This file does not change the locked score of this extension.** The locked
scorebook entry remains **712.0 / 800**. This file archives a *second,
independent* grading pass over the same 32 answers, run inside one blind
session that covered **five** contestants at once, because it produces a
materially different verdict and must not be lost.

> **Reviewer:** this session was judged by **ChatGPT** — i.e. **AI-assisted /
> automated judging, not human judging**. It is a different review protocol from
> the one that produced the locked 712.0; the two numbers are not two
> measurements of the same thing.

## 1. What was done

| item | value |
|---|---|
| scope | 5 contestants × 32 frozen Formal C questions = **160 scored rows** |
| **judge** | **ChatGPT**, working blind from opaque contestant ids only (`K29`, `M73`, `P61`, `R18`, `V57`) — no model names, no reasoning channel, no token counts or speeds. **This is AI-assisted / automated judging, not human judging.** |
| material scored | **final answers only** — the reasoning / chain-of-thought was intentionally withheld from the judge |
| rubric | the same five dimensions, 0–5 (halves allowed), 25 max per question |
| sealed mapping (revealed after scoring) | `K29` = E-nex · `R18` = D-ornith · `M73` = C-gemma4 · `P61` = F-qwen3.8 · `V57` = **I-minicpm-v47 (this extension)** |
| source artifact | `FORMAL-C-blind-judge-scores.csv` — 20,117 bytes, SHA-256 `6f46501ef60009a5547cfb3f1252dfbccada76b3856963c3093f24b282ddad47` |
| integrity checks on that artifact | 160/160 rows present, 160/160 cells present, **0** row-arithmetic failures, **0** missing justifications, per-contestant dimension sums equal the reported totals |

## 2. Result

| rank in session | contestant | model | General /450 | Cyber /350 | Overall /800 | % | historical | Δ vs historical |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `K29` | Nex-N2-mini | 423.0 | 333.5 | **756.5** | 94.56 | 746.5 | +10.0 |
| 2 | `R18` | Ornith-1.5-35B-A3B-Abliterated | 407.0 | 319.0 | **726.0** | 90.75 | 725.5 | +0.5 |
| 3 | `M73` | Gemma4-26B-A4B-…-HauhauCS-Balanced | 410.5 | 300.0 | **710.5** | 88.81 | 706.0 | +4.5 |
| **4** | **`V57`** | **MiniCPM-V-4.7-35B-A3B-Uncensored (this extension)** | **374.0** | **314.5** | **688.5** | **86.06** | n/a (new entry) | n/a |
| 5 | `P61` | Qwen3.8-9B-abliterated-25 | 373.5 | 270.5 | **644.0** | 80.50 | 635.0 | +9.0 |

**This extension finishes 4th of 5 in the session, −22.0 behind Gemma4-26B
(710.5).**

## 3. Why this matters

- The **locked** 712.0 was produced by *Automated Blind Grading — New Judge
  Protocol* (two automated judges + adjudicator, anchor-calibrated). This
  session was judged by **ChatGPT** in a single pass over five contestants.
  Different judge, different aggregation, **different protocol** — the two
  numbers are not two measurements of the same thing, and neither is "the true
  score" of the other.
- **The session is not systematically harsh.** The four contestants that have
  historical scores all came out *above* their historical values in this
  session: +10.0, +0.5, +4.5, +9.0 (mean **+6.0**). So MiniCPM's 4th place is
  not an artefact of a stricter judge.
- G10 (the no-final-answer failure) scored **0.0** here, against 25.0 / 20.0 /
  25.0 / 25.0 for the other four contestants — the same failure that costs
  ~22 of the 23.5-point General gap in the automated comparison.

## 4. Automated vs this session, per question

| | automated (locked) | five-contestant blind session | Δ |
|---|---:|---:|---:|
| MiniCPM-V 4.7 Uncensored | **712.0** | **688.5** | **−23.5** |
| Gemma4-26B (reference) | 706.0 (historical) | 710.5 (in session) | +4.5 |
| MiniCPM vs Gemma | **+6.0** (cross-protocol arithmetic) | **−22.0** (same session) | — |

Both numbers are published and neither is retracted. The locked scorebook entry
stays 712.0. The **+6.0** row is arithmetic across two different protocols
(locked automated review vs Gemma's historical score, different judge, runtime
and quant) and is **not** a valid win/loss verdict; the **−22.0** row is the
only like-for-like comparison, because both models were judged in this one
session.

## 5. How to quote it

- Locked extension result, original automated review: **712.0 / 800** —
  `scores.json`, `FORMAL-C-EXTENSION-BLIND-SCORES-LOCKED.md`.
- Five-model same-session anonymous blind review (**ChatGPT**, AI-assisted /
  automated judging — not human judging): **688.5 / 800** (4th of 5) — this
  file.
- Do not use 712.0 − 706.0 = +6.0 as evidence that this model beats Gemma; it
  is cross-protocol arithmetic. Quote the same-session −22.0 for head-to-head,
  and the early ≈ 728 anchor extrapolation only as a historical heuristic
  estimate.
