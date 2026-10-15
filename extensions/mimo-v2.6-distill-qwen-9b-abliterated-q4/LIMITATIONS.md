# Limitations — MiMo-V2.6-Distill-Qwen-9B-Abliterated extension (TM91 / key I)

1. **One run, one sample.** All results come from a single frozen Formal C run
   of 32 questions. No statistical significance is claimed for any difference
   versus any other model, including the original Qwen3.8-9B.

2. **Score ≠ full capability profile.** The locked scores measure final-answer
   quality under one frozen rubric and one frozen protocol (ctx 8192, reasoning
   budget 4096). They do not measure agentic behavior, tool use, long-context
   depth, or vision capabilities.

3. **Bimodal score profile.** Thirteen of 32 questions scored 22–25/25 while a
   small number failed severely (G12 3.5, G5 4.5, G7 5.5, C13 6.0, C14 9.5,
   C9 10.5). An aggregate percentage therefore understates the model's best
   answers and overstates its worst. Read the question-level table, not only
   the total.

4. **Reasoning / scaffolding leakage in one answer (G5).** The G5 final answer
   contains a stray `</think>` marker together with `<tool_call>` /
   `<parameter>` fragments and a truncated tail — the model overflowed past its
   reasoning block into the answer channel. Per the verbatim-release policy the
   answer is published unmodified; the blind judge scored it exactly as
   submitted, and that leak is the principal reason for its instruction-following
   and helpfulness penalties.

5. **Repetition degeneration at the context limit (G7, C9, C14).** These three
   records reached `prompt_tokens + completion_tokens == 8192` and show heavy
   repeated-text degeneration. This is the same structural failure signature
   reported for the original Formal C field (context-exhausted records). No
   answer was regenerated, shortened or repaired.

6. **Partial reasoning-channel use.** In 18 of 32 records the model produced no
   separated reasoning content at all; it answered directly. This is recorded
   as an observed behavior of this model under this protocol, not as a
   deviation: the reasoning channel exists and was verified, and the 4096 hard
   budget was verified to be enforced.

7. **Speed is runtime-specific and never scored.** All telemetry (52.44 t/s
   median decode, 14.97 s median wall time, VRAM peak ≈6.5 GiB) applies to
   llama.cpp b10375 on an RTX 5060 Laptop 8 GiB with full GPU offload. Speed was
   never shown to the judge and is not part of any score.

8. **Runtime-matched, but one sample.** The historical b10375 runtime loaded and
   ran this model, so no runtime deviation was needed. That maximizes
   comparability with the original field; it does not make exact responses
   reproducible (temperature 0.1 is not 0, no seeds were used).

9. **Not a cybersecurity-capability claim.** The 14-question Cyber division is a
   defensive/analysis-oriented evaluation on frozen, legal, lab-scoped material.
   The Cyber score does not generalize to cybersecurity ability at large.

10. **Abliteration is not causally attributed.** The run shows concrete
    instruction-following and output-integrity damage (see §4, §5 and the
    question-level table). With one sample per question and no controlled
    comparison against the non-abliterated base, this project makes **no causal
    claim** that abliteration caused it (Arena causal-language policy).

11. **Uncensoring claims are NOT verified.** No comprehensive manual uncensoring
    evaluation was performed. The model name/upstream card and the absence of
    refusals in the frozen answers are the only related evidence. Nothing here
    should be read as "confirmed fully uncensored".

12. **Rolling ranking ≠ frozen ranking.** The rolling extension view is a
    post-release comparative table only. The original six-contestant locked
    Formal C ranking is immutable and unchanged.

13. **Blind judge identity hygiene.** The judge scored the sanitized package
    without identity information and locked scores before the reveal. The judge
    did, however, score the same frozen benchmark questions used in the original
    release, so rubric familiarity cannot be fully excluded.

14. **Internal raw-archive incident (general division) — documented, no score
    impact.** After the score lock, an unrequested second generation pass was
    triggered by the automation and overwrote the run's **general** raw JSONL
    (the harness deletes a per-tag JSONL when a fresh run starts). The runaway
    pass was stopped at 2/18 records; those records are quarantined and unused.
    The cyber raw archive is complete. Consequences:

    - **Locked scores are unaffected** — the judge scored the frozen blind
      package, and that package and its digest are unchanged.
    - **The 32 published answers are still verbatim final answers.** They were
      extracted from the frozen blind package, whose SHA256
      (`787ae6806d69134f0a139353fce5d618f2435b25a7721da25a8b580b23a5f4af`) is
      asserted fail-closed by
      `scripts/build_mimo_extension_answer_dataset.py --source-blind`; before
      the loss that package was verified **byte-identical (32/32)** to the raw
      `response` fields.
    - **General per-question telemetry survives** in the run log
      (`out=`/`gen_ts`/`pp_ts`/`wall_ms` for all 18 questions, matching the
      aggregates published in [responsiveness.json](responsiveness.json)).
    - **Permanently lost for the general division:** the per-question
      `reasoning` channel text, the per-question `usage.prompt_tokens` (only
      division medians were recorded before the loss, and those are what is
      published) and the general server log.

    This is recorded here because it is part of the honest history of this
    extension; it is **not** an unreported deviation and it does not change any
    locked number.
