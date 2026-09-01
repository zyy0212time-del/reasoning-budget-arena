# License — Documentation, Benchmark, and Evaluation Data

This repository uses **split licensing** for its contents.

## Software / code — MIT

Everything under `scripts/`, together with project-authored executable source
code, tests, and utilities, is licensed under the MIT License. See the
repository `LICENSE` file (MIT License, Copyright (c) 2026 Reasoning Budget
Arena maintainers) for the full license text.

## Project-authored documentation, benchmark questions, figures, and
project-derived evaluation data — Creative Commons Attribution 4.0 International
(CC BY 4.0)

Unless expressly stated otherwise, the following are licensed under the
[Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/):

- documentation (README, REPORT, METHODOLOGY, RESULTS, LIMITATIONS,
  reproducibility and provenance documents, decision records, review
  responses, and other explanatory documentation)
- project-authored benchmark questions (`data/questions-*.json`)
- project-authored figures (`figures/`)
- judge/project-derived evaluation data (score CSVs, aggregate and
  ranking/delta tables, objective and loop-audit metadata, model artifact
  fingerprint files, and the locked blind-scorebook exports under `blind/`)

For this content, attribution must include the license identifier
(CC BY 4.0) and a link to the license: <https://creativecommons.org/licenses/by/4.0/>.

## Model-generated final-answer datasets — NOT INCLUDED

The model-generated final-answer datasets
(`data/formal-d-answers-final-only.csv` and
`data/formal-c-answers-final-only.csv`) are **not included** in this initial
public release and are **not covered** by this release's license statement.
Their future redistribution remains subject to a separate upstream
output-redistribution review of the evaluated models (see
OUTPUT-REDISTRIBUTION-DECISION.md).

## Third-party materials — not relicensed

This repository does not claim ownership over, and does not relicense:

- model weights and model binaries
- model names and upstream model metadata
- upstream licenses and terms of the evaluated models, llama.cpp, or any other
  third-party software or content referenced here

These remain subject to their respective upstream terms. See NOTICE.md and
MODEL-SOURCE-TODO.md for provenance information.
