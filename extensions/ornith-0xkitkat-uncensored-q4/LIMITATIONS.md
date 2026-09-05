# Limitations — Ornith-1.5-35B-A3B-Uncensored extension (ZD74 / key H)

1. **One run, one sample.** All results come from a single frozen Formal C
   run of 32 questions. No statistical significance is claimed for any
   difference versus any other model, including Old Ornith (Abliterated).

2. **Score ≠ full capability profile.** The locked scores measure
   final-answer quality under one frozen rubric and one frozen protocol
   (ctx 8192, reasoning budget 4096). They do not measure agentic behavior,
   tool use, long-context depth, or vision capabilities.

3. **Generation anomaly (cyber division).** The initial cyber run reached
   12/14 and aborted with a llama-server HTTP 500 ("output does not match
   the expected peg-native format") while generating C13. The frozen
   infrastructure retry rule allowed **one** identical retry via
   `--ids C13,C14`; the retry succeeded (rc=0) and completed 14/14.
   No answer was regenerated beyond those two questions, no answer was
   manually replaced, and no score was affected by the retry rule. C13/C14
   answers therefore come from the retry run; all other answers come from
   the initial run.

4. **Visible reasoning leakage in one answer (C3).** The final response of
   C3 contains residual internal reasoning text and a literal `</think>`
   tag: the model overflowed its reasoning budget into the answer channel
   and effectively answered the question twice. Per the verbatim-release
   policy the answer is published unmodified; the blind judge scored it as
   submitted (see the C3 row in the locked scorebook).

5. **Uncensoring claims are NOT verified.** No comprehensive manual
   uncensoring evaluation was performed by the maintainer. The lightweight
   scripted refusal sanity (D1, 4/4 COMPLIANCE) and the upstream model
   card/name are the only uncensoring-related evidence. Nothing here should
   be read as "confirmed fully uncensored" or "fewer refusals than Old
   Ornith".

6. **D1 telemetry is not Arena-comparable.** The responsiveness and
   context probes ran at server context 16384 with tiny prompts;
   Formal C telemetry ran at the frozen ctx 8192. The two are reported
   separately and must not be mixed.

7. **Rolling ranking ≠ frozen ranking.** The rolling extension ranking is a
   post-release comparative view only. The original six-model locked
   Formal C ranking is immutable and unchanged.

8. **Blind judge identity hygiene.** The judge scored sanitized answers
   without identity information and locked scores before the reveal. The
   judge did, however, score the same frozen benchmark questions used in
   the original release, so rubric familiarity cannot be fully excluded.
