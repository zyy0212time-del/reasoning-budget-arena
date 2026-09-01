# DATA DICTIONARY (Revision 2)

Definitions for every published field, checked column-by-column against the
actual CSV headers. Computed definitions are exact; unmeasurable fields are
marked rather than estimated. **The Formal D and Formal C objective CSVs have
different schemas and are documented separately.**

## data/questions-general.json / questions-cyber.json

| field | meaning |
|---|---|
| `id` | frozen question id (G1–G18 / C1–C14) |
| `prompt` | exact user prompt sent to every model in both conditions |

## Formal D stage question subsets (frozen, derived — never hand-edited)

| file | composition |
|---|---|
| `data/questions-formal-d-probe-general.json` | 15 General = final G-set minus G1/G8/G10 (G2–G7, G9, G11–G18) |
| `data/questions-formal-d-probe-cyber.json` | 14 Cyber (full C1–C14) |
| `data/questions-formal-d-supplement-general.json` | 3 General = G1, G8, G10 |

Stage 1 probe = 15 + 14 = **29**; supplement = **3**; union = 18 + 14 = **32**;
duplicates 0; missing 0. `scripts/test_formal_d_release_contract.py` verifies
this composition against the frozen set.

## data/formal-c-objective.csv (Formal C — 192 rows)

Actual header (checked): `original_tag, division, question_id, has_reasoning,
has_final, prompt_tokens, completion_tokens, total_tokens, reasoning_tokens,
reasoning_budget_hit, finish_reason, near_generation_cap, near_context_limit,
loop_candidate, confirmed_loop, clean_final, gen_t_s, pp_t_s, wall_ms`.

| field | definition | scope |
|---|---|---|
| `original_tag`, `division`, `question_id` | experiment tag, division, frozen id | C |
| `has_reasoning` | `yes` iff the reasoning channel is non-empty (presence only) | C |
| `has_final` | `yes` iff the final content field is non-empty after strip; never derived from the reasoning channel | C (D uses the same definition) |
| `prompt_tokens`, `completion_tokens`, `total_tokens` | server usage counts; `completion_tokens` is the **combined** reasoning+final count | C |
| `reasoning_tokens` | **NA_NOT_STORED** — no per-response reasoning-token count exists in the raw records | C |
| `reasoning_budget_hit` | **UNKNOWN** — the 4096 budget was configured/applied for every request; per-response hits are NOT DIRECTLY MEASURABLE | C |
| `finish_reason` | **NA_NOT_STORED** — not captured by the backend integration | C |
| `near_generation_cap` | `yes` iff `completion_tokens >= 0.9 × 8192` | C |
| `near_context_limit` | `yes` iff `prompt_tokens + completion_tokens >= 8192` (server context window exhaustion signature; NOT a `max_tokens` hit) | C |
| `loop_candidate` | heuristic screen: near_context_limit OR dup10 ≥ 0.30 OR repeated line ≥ 3 (screening flag only) | C |
| `confirmed_loop` | `yes` only after manual review (`data/formal-c-loop-audit.csv`) | C |
| `clean_final` | `has_final` AND not confirmed loop AND not near_context_limit. Structural only. | C |
| `gen_t_s`, `pp_t_s`, `wall_ms` | harness-computed timing columns | C |

Note: this CSV does **not** contain `reasoning_chars` or `final_chars`
(earlier documentation drafts listed them; the actual schema does not).

## data/formal-d-objective.csv (Formal D — 192 rows)

Actual header (checked): `original_tag, division, question_id, has_final,
prompt_tokens, completion_tokens, total_tokens, near_context_limit,
near_generation_cap, loop_candidate, clean_final, source`.

| field | definition | scope |
|---|---|---|
| `original_tag`, `division`, `question_id` | as above | D |
| `has_final` | same definition as C | D |
| `prompt_tokens`, `completion_tokens`, `total_tokens` | server usage counts (combined for completion) | D |
| `near_context_limit` | same definition as C | D |
| `near_generation_cap` | **column present as an explicit `D-NOT-COMPUTABLE` sentinel** — the archived D probe/supplement records do not store the `max_tokens` input this metric requires, so no value is computed. It is not a missing column; the non-computability is deliberate and explicit. | D |
| `loop_candidate` | same heuristic as C | D |
| `clean_final` | `has_final` AND not a manually confirmed loop AND not near_context_limit — the confirmed-loop term is **joined from `data/formal-d-loop-audit.csv`** (never hardcoded) | D |
| `source` | `budget-probe-8192` or `formal-d-supplement` (composite provenance) | D only |

Not present for D: `has_reasoning`, `reasoning_tokens`/`reasoning_budget_hit`/
`finish_reason` (D raw schema predates those fields), `confirmed_loop`
(represented in the loop-audit CSV, not this one), timing columns.

## data/formal-d-loop-audit.csv, data/formal-c-loop-audit.csv

| field | meaning |
|---|---|
| `tag/division/question_id` | flagged record |
| `candidate` | `yes` (heuristic fired) |
| `confirmed_loop` | `yes`/`no` after manual content review |
| `reason` | structural evidence / verdict rationale |
| `near_generation_cap`, `has_final` | recorded state |
| `notes` | heuristic measurements (shingle dup rate, repeated-line count, marker count, token totals) |

D note: 73 of 77 candidate rows have `has_final=no` (empty final — no content
channel existed in which a content loop could occur); the 4 final-bearing
candidates were manually reviewed as truncated, non-repetitive answers.

Workflow: `confirmed_loop` is a **manual** verdict. `formal_d_objective.py`
generates the candidate template only via `--init-audit` (verdicts
UNREVIEWED, refuses to overwrite) and its normal aggregation **reads** the
audit, fails closed on missing/duplicate/UNREVIEWED verdicts, and never
writes to it.

## data/formal-d-scores.csv, formal-c-scores.csv (locked blind scores)

One row per (condition, model, question) — 192 rows each, rebuilt from the
question-level locked scorebooks and validated by `scripts/validate_scores.py`.

| field | definition |
|---|---|
| `condition` | `formal-d` or `formal-c` |
| `model` | identity revealed post-lock (audit trail) |
| `division`, `question_id` | frozen reference |
| `correctness`, `completeness`, `visible_reasoning_result_quality`, `instruction_following`, `practical_usefulness` | five locked dimensions, each 0–5 (half-points) |
| `question_total` | sum of the five dimensions (max 25); validated as exact sum |

These CSVs are **judge/project-derived evaluation data** (not model-generated
text) — see LICENSE-NOTES.md class D.

## data/d-vs-c.csv (master table, generated)

| field | definition |
|---|---|
| `d_general`/`c_general` | General subtotals (max 450) |
| `d_cyber`/`c_cyber` | Cyber subtotals (max 350) |
| `d_overall`/`c_overall` | Overall (max 800; General + Cyber, validated) |
| `delta_*` | C − D in points |
| `d_rank`/`c_rank` | overall rank within the condition |
| `rank_change` | `d_rank − c_rank`; positive = moved up |

## data/formal-{d,c}-answers-final-only.csv

Sanitized final-only dataset, 192 rows each; verbatim, unmodified final
content (empty string = no final delivered; 73 rows under formal-d, 0 under
formal-c). **These files are model-generated text and are EXCLUDED from the
public release preview pending upstream output-redistribution review**
(see OUTPUT-REDISTRIBUTION-DECISION.md); they remain in the reviewer bundle
marked REVIEW ONLY. No reasoning channel, no local paths.

## data/model-artifacts.csv

| field | meaning |
|---|---|
| `tag`/`model`/`local_benchmark_filename` | exact local artifact identity |
| `sha256` | SHA256 of the exact local file (computed 2026-09-01) |
| `file_size_bytes` | exact size |
| `quantization` | Q4_K_M |
| `source_url` | current provenance status (see MODEL-SOURCE-TODO.md) |
| `revision_if_known` | revision/commit where recorded |
| `license` | `UNDETERMINED — see LICENSE-NOTES.md` until decision |

Deliberately **not published** anywhere: reasoning-channel text, character
counts presented as token counts, local paths.
