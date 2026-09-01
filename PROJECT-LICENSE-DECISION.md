# PROJECT LICENSE DECISION

## DECISION MADE — 2026-09-01

Final human maintainer decision (no longer "HUMAN DECISION REQUIRED"):

- **Code / software** (scripts, project-authored executable code, tests,
  utilities): **MIT License** — see `LICENSE`.
- **Documentation / benchmark questions / figures / project-derived
  evaluation data** (including score CSVs, objective and loop-audit metadata,
  aggregate/ranking/delta data, locked scorebook exports): **CC BY 4.0** —
  see `LICENSE-DOCS-DATA.md`.
- **Model-generated answer datasets** (`formal-{d,c}-answers-final-only.csv`):
  **withheld from initial public release**; future redistribution subject to
  separate upstream output-redistribution review.
- **Third-party materials**: not relicensed; remain under upstream terms
  (NOTICE.md, MODEL-SOURCE-TODO.md).

The sections below remain as historical decision-support context (they were
prepared while the decision was pending).

---
---

# PROJECT LICENSE DECISION — options for the maintainer (historical context)

**Status: SUPERSEDED by the DECISION MADE record above.**
This document
lists factual options with implications and compatibility notes. It does not
recommend a single choice; the maintainer (and any legal review) decides.

## 1. Software (class A — scripts, tests)

| option | implication summary | compatibility concern |
|---|---|---|
| MIT | permissive; attribution-only; no copyleft | fine with all other classes; standard for tooling |
| Apache-2.0 | permissive + explicit patent grant + NOTICE requirements | fine; slightly more formal; requires NOTICE retention |
| Other (BSD-3, GPL, etc.) | varies | GPL would be unusual for benchmark tooling; check before choosing |

## 2. Benchmark questions / docs (class B)

| option | implication | compatibility |
|---|---|---|
| CC BY 4.0 | reuse with attribution; no restrictions on modification | fine; no copyleft |
| CC BY-SA 4.0 | share-alike (derivatives must use same license) | affects anyone republishing modified questions |
| All Rights Reserved | no reuse without permission | simplest but least open |
| Same as software license | keep one license for A+B | simplest |

## 3. Judge-derived score / evaluation data (class D)

Scores, objective metrics, loop audits, locked scorebook exports, model
artifact hashes.

| option | note |
|---|---|
| Same license as A+B (if chosen open) | single-license simplicity |
| CC BY 4.0 (data/document terms) | common for evaluation data |
| Database-style license | only if a database abstraction is intended |

## 4. Model-generated answer datasets (class C)

**Handled separately** according to OUTPUT-REDISTRIBUTION-DECISION.md — the
initial release EXCLUDES these files; any later release must follow each
model's output terms.

## Facts that matter

- Base model families: Qwen3.x → Apache-2.0; Gemma 4 → Gemma license; Ornith
  → MIT per secondary reference (verify card). Fine-tune card terms are
  UNCLEAR for most (MODEL-SOURCE-TODO.md).
- No third-party code was copied into the release scripts (class F empty).

## Decision needed

- One license (or pair) for classes A + B (+ optionally D).
- A statement for class D.
- Confirmation of the Option B withholding for class C (or verification to
  move to Option A).
