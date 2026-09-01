# CURRENT-FACT REFERENCES (time-sensitive benchmark questions)

Several benchmark questions require facts that change over time. This page
records what the locked evaluation artifacts establish about how those facts
were judged, and — where the artifacts are silent — states so explicitly.

## Method

For each time-sensitive question we traced the locked score artifacts (the
blind judge scorebooks in `blind/FORMAL-{D,C}-BLIND-SCORES-LOCKED.md`).
Per-question "locked justification" notes were inspected for any recorded
source reference (URL, publication, access date). **No per-question
justification records a URL, publication title, or access timestamp.**
Nothing below is inferred or invented; items the artifacts cannot support are
marked NOT RECOVERABLE.

## Identified time-sensitive questions

| question | time-sensitive aspect | judge-relevant fact recorded in the locked scorebook | source URL / title / org | accessed-at | source status |
|---|---|---|---|---|---|
| G15 | Uranus moon count; Statue of Liberty height; Ming dynasty start year | Judge justifications refer to Uranus having **29 moons as of 2026** and to **27 being outdated** (e.g. "Uranus 给 27–28/28，已落后于 2026 年的 29"; "Uranus 27 已过时") | NOT RECOVERABLE FROM ARCHIVED ARTIFACTS | NOT RECOVERABLE FROM ARCHIVED ARTIFACTS | NOT RECOVERABLE — the evaluation-year reference (2026) is recorded, the underlying source is not |
| G16 | "current (as of today)" status of Voyager 1 / Voyager 2 (power, instruments, mission status) | Judge justifications record several claims as outdated ("Voyager 2 'fully operational' 等状态已过时"; "速度与仪器状态多处不准"), i.e. the judge applied 2026-era knowledge | NOT RECOVERABLE FROM ARCHIVED ARTIFACTS | NOT RECOVERABLE FROM ARCHIVED ARTIFACTS | NOT RECOVERABLE — only the judge's 2026-era assessment is recorded |

## Reproducibility limitation

G15 and G16 are correctness-sensitive to the evaluation date. The Formal D
29-question probe **began on 2026-08-31 and completed on 2026-09-01**; the
supplement and Formal C were run on 2026-09-01 (Formal C generation window
13:35–18:02). The archived judge artifacts relied on 2026-era current facts
(e.g. Uranus = 29 moons), but the specific original sources relied upon were
**not recorded in any archived artifact**.
A re-judgement on a different date may legitimately reach different
conclusions on these two questions; no claim of date-independent correctness
is made for them. This limitation is also stated in LIMITATIONS.md (items 20–21).

## What is NOT claimed

- No access timestamps, archive URLs or historical snapshots are fabricated;
  those cells are NOT RECOVERABLE.
- No answer is re-graded; this document only records which facts the locked
  evaluation depended on and where the provenance trail ends.
