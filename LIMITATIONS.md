# LIMITATIONS

Read this before quoting any number from this project.

## Experimental design

1. **Only six models**, all running locally, all in Q4_K_M quantization.
2. **Specific quantizations / builds**: results apply to these exact GGUF
   files under this exact llama.cpp build (`ba360efe1` / b10375). Other
   quantizations or backends may behave differently.
3. **One local hardware/runtime setup** (RTX 5060 Laptop 8 GiB, experts-on-CPU
   MoE placement). No cloud or multi-GPU validation.
4. **32 questions only** (18 General + 14 Cyber). Small question counts mean
   single questions can move division results noticeably.
5. **Division imbalance**: 18 General vs 14 Cyber — division-level
   comparisons have different resolution.
6. **Single formal sample per (condition, model, question)**; no repeats in
   the formal runs.
7. **temperature 0.1** is low but not zero — stochastic variation is possible,
   particularly for borderline answers.
8. **No repeated seeds, no confidence intervals, no statistical tests.** Any
   "large"/"substantial" wording is descriptive, not inferential.

## Blind evaluation

9. **One primary blind judge** produced the locked scores.
10. **No inter-rater reliability** was measured (no second judge).

## Measurement limits

11. **Reasoning token count was not stored per response**; the harness
    captured only combined `completion_tokens` and no `finish_reason`.
12. Consequently it is **not known which individual responses actually hit
    the 4096 reasoning budget** — only that the budget was uniformly
    configured and applied by the runtime.
13. **Model-native reasoning implementations differ** (different template
    families); the budget interacts with each model's own thinking format.
14. Context exhaustion was inferred from the exact-total signature
    (prompt + completion == 8192) because `finish_reason` was unavailable.

## What the results do NOT establish

15. They do **not establish 4096 as an optimal, universally recommended
    budget**. The value was chosen through calibration for operational
    viability on this benchmark.
16. They do **not establish a universal model ranking**. Rankings are blind
    final-answer scores on one 32-question benchmark by one judge.
17. The **Cyber result does not generalize** to cybersecurity ability at
    large: 14 questions, single run, specific models and quantizations.
18. **No agent / tool-use evaluation** was performed.
19. **No long-context, real-world security workloads** were evaluated.
20. Some questions deliberately test **strict instruction following and
    formatting**, so scores partly measure format compliance, not only
    knowledge or reasoning.
21. Some questions required **time-specific or current-fact** answers whose
    verification depends on the evaluation date. G15 (Uranus moon count) and
    G16 (current Voyager status) are the identified cases; the locked judge
    artifacts record the facts relied on (evaluation-year knowledge) but **no
    source URLs or access timestamps** — see
    `docs/CURRENT-FACT-REFERENCES.md` (provenance cells marked NOT
    RECOVERABLE; nothing fabricated).

## Publication scope

22. The release candidate intentionally excludes reasoning-channel content;
    only final answers, objective structural metadata, protocol, and scripts
    are published.
23. The locked blind scores have been attached and independently recomputed
   (see RELEASE-READINESS.md items B/C/D). Remaining items are license,
   model source links, and human review — not data.
