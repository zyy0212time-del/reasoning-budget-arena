# CALIBRATION HISTORY — how the 4096 policy was (and was not) chosen

This is the methodological story of the policy search. It is recorded because
the final protocol looks obvious in hindsight and was not. All events are
documented in the experiment archive (MODE-C-FEASIBILITY.md §B8–B14,
RUN-LOG.md).

## 1. 1024 round — invalid as an ability test (2026-08-31)

The first formal-style round capped total completion at 1024 tokens. Every
contestant was thinking-capable; reasoning consumed the cap and most answers
arrived with an empty final channel. The round was discarded **as an ability
test** — a useful negative result: total-completion caps are the wrong knob
when models think.

## 2. 4096 total-cap calibration — still insufficient

Raising the total cap to 4096 kept 61–75% empty finals per model. The knob
was still the wrong one.

## 3. 8192 envelope probe — the Formal D condition

With an 8192-token window and native thinking (no reasoning budget), 73 of
174 responses on the 29-question union still produced no final. This became
Formal D's configuration: a real, controlled condition worth scoring, and the
baseline against which the reasoning budget would later be compared.

## 4. Native reasoning budget discovered and verified

The local llama.cpp build exposes `--reasoning-budget N` — a backend token
budget over the thinking segment with automatic end-of-thinking injection.
A smoke test confirmed the mechanism works (reasoning capped/scaled as
configured; a full final still produced). This is a runtime mechanism, not a
prompt suggestion.

## 5. Budget-value search — 512 too tight, B/F anomalies

A six-model smoke at budget 512 verified the mechanism on every model, but
two models (B and F) degenerated after the forced transition — repeating
chain-of-thought prose inside the final channel until the envelope. A
1024/2048 calibration followed: F became healthy at 1024+; B degenerated at
**every** budget tested — including 1024, where its reasoning ended naturally
*under* budget and the final channel still looped.

## 6. The suspected runtime bug — and the control that stopped it

At this point a reasoning-budget runtime bug was a live hypothesis (B
degenerated at every budget). A controlled diagnostic was run: B on the same
synthetic question, unrestricted vs budgeted, two repeats each. The
**unrestricted control also failed** (reasoning runaway filled the whole
window in repeat 1). With the control failing, the bug hypothesis could not
be upheld — and a second diagnostic on a clean, unambiguous,
unique-solution prompt showed 4/4 healthy runs (budgeted and unrestricted).

**Verdict: the instability was prompt-specific** (a "lunch is during slot 4"
ambiguity acted as a reasoning attractor for that model), not budget-caused.
Consequently **no llama.cpp issue or PR was filed** — the control design
prevented a false upstream report. This is recorded as part of the
methodology, not as an embarrassment.

## 7. Six-model validation at 4096 → Formal C

A final validation ran all remaining models at budget 4096 on the clean
diagnostic prompt: all healthy, all correct on that prompt's verifiable
answer. 4096 was adopted as the uniform policy — a policy decision based on
operational viability on this benchmark, not a claim of optimality — and
Formal C was executed.

## What this history supports

- The 4096 value is a calibration outcome for this benchmark/hardware
  combination, not a universal constant.
- Control runs are what separated "runtime bug" from "prompt-specific
  instability".
- The prompt-design lesson (ambiguous constraint = reasoning attractor)
  fed back into diagnostic design.
