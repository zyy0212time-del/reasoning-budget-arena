# FAILURE MODE ANALYSIS

Five distinct phenomena that must never be conflated. Definitions are exact
(DATA-DICTIONARY.md); every claim below was recomputed from raw during the
independent post-run audit.

## The five modes

### 1. EMPTY FINAL
The final content channel is empty after whitespace strip. In Formal D this
was the dominant failure (73/192): with native thinking and no separate
budget, the reasoning channel consumed the available window and no final was
ever produced. **In Formal C: 0 observed in this run.**

### 2. CONTENT LOOP
Degenerate repetition inside the final channel: verbatim repeated lines or
blocks, identical content repeated under cosmetic renumbering, or the
reasoning process visibly continuing/restarting inside the final answer
(content head starts mid-derivation; reasoning-starter phrases throughout;
cycling hypothesis attempts). Confirmed **only after manual review** of
heuristic candidates — long answers, near-cap records, templated lists, and
short complete answers are NOT automatically loops.

Formal C: **6 confirmed** (A/G4, B/C9, C/C9, F/C2, F/G3, F/G4 — each also
truncated by context exhaustion). Formal D: 0 confirmed (its 4 heuristic
candidates were all coherent answers truncated by the window).

### 3. CONTEXT EXHAUSTION
`prompt_tokens + completion_tokens >= 8192` — the server context window was
filled. All 8 Formal C flagged records sit at **exactly** 8192 total (max
completion 8093), so this is window exhaustion, **not** a `max_tokens` hit,
and not (measurably) a reasoning-budget hit — the reasoning budget's
per-response usage was not stored. Formal D: 77 such records (73 of them with
empty finals).

### 4. STRUCTURALLY CLEAN FINAL
Final present AND not a confirmed loop AND not context-truncated.
Formal D: 115/192. Formal C: 184/192 (95.8%).
**Structurally clean ≠ correct, usable, or high-quality.** It is a statement
about delivery mechanics only.

### 5. CORRECTNESS FAILURE
A judge-level judgement about whether the content is right. It is assessed only
through the blind scoring protocol; the locked scores are now published
(`data/formal-{d,c}-scores.csv`, audit trail in `blind/`). It is independent of
every structural category above.

**Structural delivery is not quality.** Under Formal C all 192 responses
delivered a non-empty final and 184 were structurally clean, yet blind scores
still ranged from 576.0 to 746.5 out of 800 — a structurally perfect delivery
can still be a comparatively weak answer, and the two measurements must never
be read as the same thing.

## The shift (descriptive, single-sample)

| mode | Formal D | Formal C |
|---|---|---|
| empty final | 73 | 0 |
| confirmed content loop | 0 | 6 |
| context-truncated final (non-loop) | 4 | 2 |
| context exhaustion (any) | 77 | 8 |
| structurally clean | 115 | 184 |

Reading: under this frozen protocol the dominant failure **appears to shift**
from "no final at all" (reasoning eats the window) to "final delivered but
degraded" (loops/truncation after the forced transition). The mechanism is
plausible — the budget forces a transition the model would not have chosen —
but this design (one sample per cell, no seeds, no replicates) cannot isolate
it, and no causal claim is made.

## Audit note

The first post-run pass labelled all 8 high-usage Formal C records as
"looped". Manual review corrected this: 6 are confirmed loops; A/C1 (a
degenerate 146-item listing) and B/C8 (a genuine long computation) are
truncated non-loops; and one heuristic candidate (A/G3) flagged by shingle
duplication is actually a complete short answer whose dup-rate was a
small-sample artifact. Heuristics screen; humans confirm.
