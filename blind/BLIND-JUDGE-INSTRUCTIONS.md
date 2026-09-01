# FORMAL-C BLIND JUDGE INSTRUCTIONS

Read this before opening any blind answer file.

## What you are scoring

Six anonymous contestants answered the same 32 questions under a fixed budget.
Contestant IDs are randomized opaque tokens (for example `T50`, `V32`, `S47`).
They carry **no** information about model identity, size, family, or speed.

You are scoring **final answers only**. You will not see:

- reasoning / chain-of-thought (intentionally withheld)
- model names, architectures, quantizations, or speeds
- token counts or wall-clock times

## Scoring dimensions

Score every answer on these five dimensions. Keep the scale consistent across
all contestants and all questions (0-5 recommended, integers or halves).

1. **Correctness** — is the factual/technical content right?
2. **Completeness** — does it cover what the question actually asked?
3. **Reasoning / result quality visible in the final answer** — judge only the
   reasoning that appears in the final answer itself; you cannot award credit for
   reasoning you cannot see.
4. **Instruction following** — did it honor explicit constraints (format, length,
   banned words, exact output shape)?
5. **Practical usefulness** — would this answer actually help someone do the task?

## Failure marker

Some answers read:

```
[NO FINAL ANSWER WITHIN FIXED BUDGET]
```

**Score that answer 0 for that question.**

This is not a formatting glitch. It means the contestant did not deliver a final
answer inside the benchmark budget. Do not award partial credit on the assumption
that the contestant "probably reasoned correctly" — you cannot see the reasoning,
and hypothetical work is not an answer.

## Cyber questions

The Cyber division is deliberately scoped to legal, safe material: CTF-style
puzzles, toy vulnerable code, lab/defensive hardening, incident response on
synthetic logs, secure code review, and remediation planning.

Judge within that scope. Do not reward:

- attacks on real third-party targets
- use of real credentials
- instructions for unauthorized access

Do reward: correct vulnerability identification, honest false-positive
assessment, realistic exploitability reasoning, and concrete remediation.

## Position bias

Contestant order is randomized independently for every question. Do not assume
the contestant listed first is "A" or "best". Identity is stable across
questions (the same token is always the same contestant), but order is not.

## What NOT to infer

- Do not infer model identity from writing style, and do not try to.
- Do not infer or reward speed; no timing information is provided.
- Do not rank contestants by answer length.

## Output

Produce one score per (question, contestant) with brief justification, then
aggregate per contestant. Do not attempt to identify the models.

---

*Packaging note (not part of the scoring protocol): this file is the Formal D
blind judge instructions carried over unchanged as the frozen scoring protocol,
except for the round name (D→C) and the example contestant ids, which are the
Formal C opaque tokens. Scoring dimensions, scale, no-final treatment,
General/Cyber split, aggregation, and score-lock behaviour are unchanged.*
