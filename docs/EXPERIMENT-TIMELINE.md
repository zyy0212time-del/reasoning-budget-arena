# EXPERIMENT TIMELINE

Reconstructed from the project run log and document timestamps. Entries
without a recorded time are marked accordingly; nothing is invented.

## 2026-08-31 — Arena design and first rounds

| time (local) | event |
|---|---|
| 14:15 | Arena directory created; frozen question sets authored (General G1–G18, Cyber C1–C14); harness written |
| 14:42 | Harness validation on the 9B model; Round 1 first pass begins |
| 14:42–17:07 | Round 1 first pass, all six contestants (max_tokens=1024) |
| 17:15 | **Data-quality issue found**: thinking content consumed the whole 1024 budget; most finals empty; round unusable for grading |
| 17:20–21:00 | **4096 calibration rerun** (max_tokens=4096): still 61–75% empty finals per model → 4096 insufficient as a total cap |
| 21:0x–03:15 (+1) | **8192 budget probe** (29-question union, all six): 73/174 empty finals → still insufficient |

## 2026-09-01 — Formal D, Mode C investigation, Formal C

| time (local) | event |
|---|---|
| morning | Formal D package assembled: 29-question probe + 3-question supplement (G1/G8/G10) = 192 responses; blind packaging, leak check, judge instructions, pre-judge report. *(exact run times not separately recorded)* |
| — | Mode C feasibility: native `--reasoning-budget` identified and verified as a hard backend mechanism (B1–B3) |
| — | 512 six-model smoke: mechanism verified on all six; too tight for B/F (B10) |
| — | B/F 1024/2048 calibration: B degenerated at every budget tested (B11) |
| — | B transition diagnostic #1: control run also failed → inconclusive (B12) |
| — | B diagnostic #2 on a clean unambiguous prompt: 4/4 healthy → earlier failures were prompt-specific, not budget-caused (B13) |
| — | Six-model 4096 validation on the clean prompt: all healthy → policy adopted (B14) |
| 13:35:30 | **Formal C generation start** |
| 18:02:02 | **Formal C generation complete** (192 requests, 0 infrastructure retries) |
| — | Independent post-run audit: raw integrity PASS; metrics rebuilt from raw; HY3 post-run corrected (claims audit) |
| 18:40 | Formal C blind packaging (opaque IDs, randomized order, leak check PASS) |
| — | Blind scoring, score lock, mapping reveal *(scores live in the experiment's score archive; not in this snapshot)* |

## Note on process honesty

The 4096 policy was not the starting plan. It survived a 1024 failure, a 4096
calibration failure, an 8192-envelope failure under native thinking, a
budget-policy search (512 → 1024/2048 → 4096), a suspected runtime bug that
turned out to be prompt-specific, and a control-run save from a false upstream
bug report. The full narrative is in CALIBRATION-HISTORY.md.
