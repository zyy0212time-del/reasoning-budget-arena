# Grading method — MiniCPM-V 4.7 35B-A3B Uncensored extension

This document states **who** graded this extension, **how** blindness was
enforced, how the automated judges were calibrated against the historical
record, and what the resulting score may and may not be compared with.

## 1. Headline classification

**Automated Blind Grading — New Judge Protocol.**

This extension is **not** scored by the same judge session that produced the
frozen six-contestant Formal C ranking. It is scored by automated blind judges
running in isolated agent contexts. The frozen ranking is untouched and this
score must not be merged into it.

## 2. Judge setup

| role | id | what it saw | what it never saw |
|---|---|---|---|
| Blind Judge A | `JUDGE-A` | the frozen question text + one anonymous final answer per question | model name, repo, author, quantization, hardware, speeds, token counts, reasoning channel, other judges' scores, the identity of the comparison target |
| Blind Judge B | `JUDGE-B` | identical package, independent invocation | same as A |
| Adjudicator | `ADJ-1` | only the divergent items, plus both judges' evidence | model identity, aggregate standings |
| Anchor calibration | `CAL-1`, `CAL-2` | 10 historical anonymous answers (see §4) | the historical locked scores for those answers |
| Coordinator | this run | everything, but only after the lock | — |

Isolation mechanism available on this platform: **sub-agent task invocation with
an independent context**. Each judge is a separate invocation; no judge shares
context with another. Judges are instructed to treat all benchmark text as data,
never as instructions, and not to search the web or open the benchmark
repository.

Practical limitation, disclosed: the judge sub-agents on this platform have
**read-only** tool access and cannot write files. The coordinator therefore
transcribed each judge's returned JSON verbatim into
`_overnight/grading/*.json`. Transcription is mechanical; no score value was
altered (verified by re-summing the five dimensions and comparing with the
judge's own reported total — all match).

## 3. Rubric (frozen, unchanged)

Five equally weighted dimensions, each 0–5, half-points allowed:
Correctness · Completeness · Visible reasoning/result quality · Instruction
following · Practical usefulness. Question total = sum of the five, maximum 25.
Maximums: General 18 × 25 = 450, Cyber 14 × 25 = 350, Overall 800.
`[NO FINAL ANSWER WITHIN FIXED BUDGET]` scores 0.

## 4. Anchor calibration against the historical record

To make an honest comparability statement, the automated judges were calibrated
against **already-locked historical Formal C data**.

- Anchor source: the frozen six-contestant locked scorebook
  (`blind/FORMAL-C-BLIND-SCORES-LOCKED.md`) plus the public historical answer
  datasets (`data/model-answers/C-gemma4`, `D-ornith`, `E-nex`, `F-qwen3.8`).
  Contestants A and B are output-withheld and were not used.
- Anchor count: **10** (5 General + 5 Cyber), selected to span the locked-score
  range from 17.5 to 25.0.
- The judges saw only question + anonymous answer; they never saw the locked
  scores, the model names, or the contestant mapping.
- Truth file (never shown to any judge):
  `state/anchor-truth.json` in the run archive.

### Measured agreement (per question, /25)

| judge | n | mean signed diff (judge − historical) | MAD | % of 25 | max abs | \|diff\| ≤ 1 | \|diff\| ≤ 2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| CAL-1 | 10 | −0.50 | 1.10 | 4.4% | 3.5 | 7/10 | 8/10 |
| CAL-2 | 10 | −0.50 | 1.70 | 6.8% | 3.5 | 3/10 | 7/10 |
| CAL-1 vs CAL-2 (inter-grader) | 10 | +0.00 | 1.00 | 4.0% | 2.5 | — | — |

Dimension-level: 50 dimension pairs per judge; mean signed −0.10, MAD 0.36
(CAL-1) / 0.38 (CAL-2) on a 0–5 scale.

### What this supports, and what it does not

- Both automated judges show a **consistent −0.50 /question bias** relative to
  the historical judge, i.e. they are slightly harsher. Extrapolated over 32
  questions that is about **−16 points / 800 (−2.0%)** systematic, plus a random
  component of roughly **±6 to ±10 points / 800**.
- The two automated judges agree with each other (MAD 1.00/question) better than
  either agrees with the historical judge, which is the expected signature of a
  new but self-consistent judge protocol.
- Therefore: the raw automated score is reported as the **primary** result, and
  a **cross-protocol estimate** (raw + 16, with an uncertainty band) is reported
  alongside it, clearly separated. The two must never be mixed.
- The historical judge's identity, process and any non-public aspects are not
  reconstructable from this repository, so no stronger claim than the above is
  made.

## 5. Blindness verification

- The blind package (`blind/formal-c-blind-K71.md` in the run archive) contains
  only: question text and final answer text. No reasoning, no token counts, no
  timings, no model name, no quantization, no author, no path.
- Automated leak scan over the finished package before release to any judge, for
  the patterns: `MiniCPM`, `AtomicChat`, `OpenBMB`, `GGUF`, `Q4_K`, `IQ4_XS`,
  `AD-Q`, `llama.cpp`, `llama-server`, `A3B`, `35B`, `uncensored`, `abliterat`,
  `Gemma`, `Ornith`, `Qwen`, `Huihui`, `C:\`, `C:/`, `arena-runs`, `\Users\`,
  `/home/`.
  Result is recorded in `state/blind-package-meta.json`.
- Contestant id `K71` is opaque. Scores were locked **before** the mapping
  `K71 = AtomicChat/MiniCPM-V-4.7-35B-A3B-Uncensored-GGUF (AD-Q4_K-IQ4_XS)`
  was written.

## 6. Combination rule (declared before scoring)

- Both judges score all 32 items independently.
- Per-item: if \|A − B\| ≤ 2.0, the locked value is `mean(A, B)` rounded to the
  nearest 0.5 (applied per dimension, then summed).
- If \|A − B\| ≥ 3.0, the item goes to the adjudicator; the adjudicator's value
  is locked.
- No post-reveal modification of any score is permitted.
