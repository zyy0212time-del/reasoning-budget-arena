# REPRODUCIBILITY

What another machine needs in order to re-run this experiment, what the
released scripts can and cannot establish, and how the two conditions'
histories differ.

## Requirements

- **Runtime**: llama.cpp `llama-server` (experiment used build `ba360efe1`,
  b10375; see `docs/runtime-evidence.md`). Pin the build for comparability —
  newer builds may change reasoning-budget behaviour.
- **Python**: 3.10+ for the harness/runners; `matplotlib` for figures.
- **Hardware**: the experiment ran on an RTX 5060 Laptop 8 GiB with MoE
  experts on CPU (`-ncmoe`). Other machines will differ in speed and possibly
  in token-level behaviour.
- **Models**: the six GGUF files (Q4_K_M; SHA256 in
  `data/model-artifacts.csv`). Paths go in `scripts/CONFIG.json`.

## Path contract (single source of truth)

The runner, harness, and integrity checker agree on one canonical raw layout
(`scripts/test_release_paths.py` verifies this without running any model):

```
<experiment-root>/raw/formal-c/<tag>/<tag>-<div>-questions.jsonl
    div in {general, cyber}, tag in {A..F}
```

- `--div` is passed explicitly; it is never inferred from the questions
  filename, so `data/questions-general.json` always maps to `div=general`.
- No `raw/raw/...` nesting can occur: the runner passes `--outdir <root>` and
  `--rawdir raw/formal-c/<tag>`; the harness joins them once.

## Setup

1. Copy `scripts/CONFIG.example.json` to `scripts/CONFIG.json`; fill in the
   llama-server path and the six model paths (never commit real paths).
2. Keep the frozen question files in `data/`; do not edit them (edits
   invalidate the comparison).

## Formal C reproduction (single contiguous 32-question run)

```
python scripts/run_formal_c.py        # requires scripts/CONFIG.json
```

The runner invokes the harness six times (tags A–F), each time for both
divisions, with `ctx=8192, max_tokens=8192, --reasoning-budget 4096,
temp=0.1, top_p=0.9, --no-speed`, one server at a time, and runs the
integrity check (32 unique ids per tag) after each division. Infrastructure
failures get at most one identical retry; model failures are never retried.

Standalone harness equivalent (explicit values — do not rely on defaults):

```
python scripts/arena_harness.py --model <gguf> --tag A --questions data/questions-general.json \
  --div general --outdir <root> --rawdir raw/formal-c/A \
  --ctx 8192 --max-tokens 8192 --temp 0.1 --top-p 0.9 \
  --ncmoe 256 --reasoning-budget 4096 --no-speed --llama-server <path>
```

## Formal D reproduction (composite — three stages, do not run as one)

Formal D was **not** a single contiguous 32-question run. Its published
baseline is assembled from three stages (METHODOLOGY.md §3), and the release
distinguishes two layouts:

### Historical execution (the experiment archive)
The actual Formal D probe was executed as the archived **29-question union**
(G2–G7, G9, G11–G18 General + C1–C14 Cyber), one file per tag:
`raw/budget-probe-8192/{tag}-budget-probe-8192-questions.jsonl`, with
`raw/formal-d-supplement/{tag}-general-questions.jsonl` for G1/G8/G10.
`scripts/formal_d_objective.py` auto-detects this layout and assembles the
published 192-record baseline from it.

### Public canonical reproduction (clean-room, release path)
For a clean release path, the **same 29-question Stage-1 set** may be stored
as one file per division:

```
<root>/raw/
  budget-probe-8192/
    A/A-general-questions.jsonl      # 15 General (G2–G7,G9,G11–G18)
    A/A-cyber-questions.jsonl        # 14 Cyber
    ...
  formal-d-supplement/
    A/A-general-questions.jsonl      # G1, G8, G10
    ...
```

Stage question files are shipped in `data/` (derived from the frozen set,
never hand-edited):
`questions-formal-d-probe-general.json` (15), `questions-formal-d-probe-cyber.json`
(14), `questions-formal-d-supplement-general.json` (3).

```
Stage 1 — 29-question probe (15 General + 14 Cyber):
    python scripts/arena_harness.py --model <gguf> --tag A \
      --questions data/questions-formal-d-probe-general.json --div general \
      --outdir <root> --rawdir raw/budget-probe-8192/A \
      --ctx 8192 --max-tokens 8192 --temp 0.1 --top-p 0.9 --ncmoe 256 --no-speed
    python scripts/arena_harness.py --model <gguf> --tag A \
      --questions data/questions-formal-d-probe-cyber.json --div cyber \
      --outdir <root> --rawdir raw/budget-probe-8192/A \
      --ctx 8192 --max-tokens 8192 --temp 0.1 --top-p 0.9 --ncmoe 256 --no-speed
    ... tags B–F ...

Stage 2 — G1/G8/G10 supplement, same settings as Stage 1:
    python scripts/arena_harness.py --model <gguf> --tag A \
      --questions data/questions-formal-d-supplement-general.json --div general \
      --outdir <root> --rawdir raw/formal-d-supplement/A \
      --ctx 8192 --max-tokens 8192 --temp 0.1 --top-p 0.9 --ncmoe 256 --no-speed
    ... tags B–F ...

Stage 3 — assemble the published D baseline (192 records):
    python scripts/formal_d_objective.py   # auto-detects layout, verifies exact IDs
```

### Sequencing caveat
The public canonical reproduction preserves the **same Stage-1 29-question set
and the same 3-question supplement**, but if you run it freshly it **does not
reproduce the exact historical request sequence** of the archived run (the
historical probe interleaved divisions per its own ordering). No claim of exact
historical sequencing is made for the reproduction path.

## Post-run analysis

```
python scripts/formal_d_objective.py --init-audit   # STAGE A: candidate template (UNREVIEWED) if missing
# human review of data/formal-d-loop-audit.csv verdicts (yes/no) is required before aggregation
python scripts/formal_d_objective.py   # STAGE B: aggregation reads the manual audit; fails closed on
                                       #   missing/duplicate/UNREVIEWED verdicts; never overwrites it
python scripts/formal_c_objective.py   # Formal C structural metrics
python scripts/validate_scores.py      # score validation + master table
python scripts/make_figures.py         # figures (from verified CSVs)
python scripts/test_release_paths.py   # clean-room path-contract test (no models)
python scripts/test_formal_d_release_contract.py
python scripts/test_formal_d_manual_audit.py
python scripts/validate_public_release_preview.py
```

The manual audit is the source of truth for `confirmed_loop`: the aggregation
script never auto-fills verdicts and never mutates the audit file
(`test_formal_d_manual_audit.py` TEST F proves this by hash).

## What will and will not reproduce

- The **protocol and path contract** reproduce and are machine-checkable
  (`test_release_paths.py`).
- **Exact responses will not**: temperature 0.1 is not 0; GGUF/backend builds
  differ; MoE expert placement affects numerics. Treat any run as one sample.
- Structural metrics are re-derivable from raw with
  `formal_{d,c}_objective.py`, but their values are run-specific.
- **Blind scores require the judge protocol** (`blind/BLIND-JUDGE-
  INSTRUCTIONS.md`); a different judge will not reproduce the numbers, and no
  claim is made that they would.
- Stochastic, backend and quantization effects are acknowledged; generation
  reproducibility is not claimed beyond the above.

## Raw data format

- Formal C records: `id, tag, prompt, response, reasoning, usage, timings,
  wall_ms, gen_ts, pp_ts, reasoning_budget, ctx, max_tokens, temperature,
  top_p, ncmoe`. No `finish_reason`; no per-response reasoning-token count.
- Formal D probe/supplement records store a subset (no
  `ctx/max_tokens/reasoning_budget` fields) — see DATA-DICTIONARY.md.
