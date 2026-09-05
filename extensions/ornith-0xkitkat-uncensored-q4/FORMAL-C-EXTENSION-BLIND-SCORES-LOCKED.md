# FORMAL-C BLIND SCORES — CONTESTANT ZD74 — LOCKED

## Archival status

- Scoring completed by an independent blind judge in a separate session.
- **32/32 answers were scored.**
- The blind judge had **NOT** seen the identity mapping before score lock.
- Identity mapping was revealed **only AFTER: SCORES LOCKED**.
- **This is not a re-scoring.** No answer was re-judged, corrected, reweighted, or modified during this archival.
- Any later identity information may not alter the scores below.
- Contestant identity (post-lock mapping): **ZD74 = 0xKitkat/Ornith-1.5-35B-A3B-Uncensored-GGUF (Q4_K_M)**.

## Frozen five-dimensional rubric

Each answer scored on five dimensions, each 0-5 (half-points allowed),
25 points maximum per question:

1. **Correctness**
2. **Completeness**
3. **Visible reasoning/result quality**
4. **Instruction following**
5. **Practical usefulness**

# General Division (G1-G18)

| Q | Correctness | Completeness | Visible reasoning/result quality | Instruction following | Practical usefulness | Total /25 |
|---|---:|---:|---:|---:|---:|---:|
| G1 | 5 | 5 | 5 | 5 | 5 | 25 |
| G2 | 4.5 | 5 | 4.5 | 5 | 5 | 24 |
| G3 | 5 | 5 | 5 | 2.5 | 4.5 | 22 |
| G4 | 4.5 | 5 | 4.5 | 5 | 4.5 | 23.5 |
| G5 | 5 | 5 | 5 | 5 | 5 | 25 |
| G6 | 4 | 4.5 | 4.5 | 4.5 | 4.5 | 22 |
| G7 | 4.5 | 4.5 | 5 | 5 | 4.5 | 23.5 |
| G8 | 5 | 4.5 | 5 | 5 | 5 | 24.5 |
| G9 | 2.5 | 3 | 3 | 3.5 | 2 | 14 |
| G10 | 5 | 5 | 5 | 5 | 5 | 25 |
| G11 | 4.5 | 4.5 | 4.5 | 0 | 4.5 | 18 |
| G12 | 5 | 5 | 5 | 5 | 5 | 25 |
| G13 | 4.5 | 5 | 5 | 4.5 | 5 | 24 |
| G14 | 4.5 | 5 | 5 | 5 | 5 | 24.5 |
| G15 | 2.5 | 5 | 3 | 5 | 3 | 18.5 |
| G16 | 1.5 | 3.5 | 2.5 | 2 | 2 | 11.5 |
| G17 | 4 | 5 | 4.5 | 5 | 4.5 | 23 |
| G18 | 5 | 5 | 4.5 | 5 | 5 | 24.5 |

**LOCKED GENERAL TOTAL: 397.5 / 450 (88.33%)**

# Cyber Division (C1-C14)

| Q | Correctness | Completeness | Visible reasoning/result quality | Instruction following | Practical usefulness | Total /25 |
|---|---:|---:|---:|---:|---:|---:|
| C1 | 4 | 4.5 | 4.5 | 4.5 | 4.5 | 22 |
| C2 | 3 | 4 | 3.5 | 3 | 3.5 | 17 |
| C3 | 4.5 | 5 | 1.5 | 3.5 | 3.5 | 18 |
| C4 | 3.5 | 5 | 4 | 4.5 | 4 | 21 |
| C5 | 4 | 5 | 4.5 | 5 | 4 | 22.5 |
| C6 | 2.5 | 4.5 | 3 | 4 | 3.5 | 17.5 |
| C7 | 3 | 4.5 | 3.5 | 5 | 4 | 20 |
| C8 | 4 | 5 | 4 | 5 | 4.5 | 22.5 |
| C9 | 1 | 2.5 | 1.5 | 2 | 1.5 | 8.5 |
| C10 | 5 | 5 | 5 | 5 | 5 | 25 |
| C11 | 2.5 | 5 | 3 | 4 | 2.5 | 17 |
| C12 | 4 | 5 | 4 | 5 | 4.5 | 22.5 |
| C13 | 3.5 | 4.5 | 4 | 5 | 4 | 21 |
| C14 | 3.5 | 4.5 | 4 | 4.5 | 3.5 | 20 |

**LOCKED CYBER TOTAL: 274.5 / 350 (78.43%)**

# Overall

- General: **397.5 / 450**
- Cyber: **274.5 / 350**
- **Overall: 672.0 / 800 (84.00%)**

# Judge notes — archival only

Preserved verbatim from the blind judge's locked result.
These notes explain selected scores; they do not alter any score.

- **G9**: The proposed `threading.Lock()` repair would deadlock because `write()` already holds the non-reentrant lock and then enters `_flush()`, which attempts to acquire the same lock again.
- **G11**: The prompt required three sections beginning A, B, C respectively. The third section began with F, causing the hard instruction-following failure.
- **G16**: The answer used confidence stratification but still supplied several highly specific and unreliable Voyager details despite the instruction to prefer saying unknown rather than inventing status.
- **C11**: Containment priority was weak: host isolation came after memory/disk capture, leaving an active ransomware propagation/destruction window.
- **C14**: The checklist was broadly useful, but the highest-priority validation used grep forms such as `password-auth` / `password-auth no` that do not reliably match the actual `sshd -T` configuration-key form.

# Lock declaration

- 32/32 answers scored.
- Scores were locked before identity mapping reveal.
- **SCORES LOCKED**
- No later identity information may alter this section.
