# Response to Final Gate — R2.1.1 privacy hotfix

Final-gate verdict: **P1 = 0, P0 = 1**. The sole blocker: the public leak
validator (`public-release-preview/scripts/validate_public_release_preview.py`)
embedded the real machine-specific identifiers it was meant to detect — the
local Windows username and the private local project path — directly in its
public source, so the scanner itself leaked the information. We acknowledge
this plainly: the public validator previously contained those private literals
and the fix below removes them.

## FINDING
- `validate_public_release_preview.py` contained, in its scan rules: the real
  Windows username literal and the private local project-path literal
  (both machine-specific denylist values), so running the "public" leak check
  published the very identifiers it scans for.

## ROOT CAUSE
- The public scanner was written with a machine-specific denylist embedded in
  the public source, instead of a generic-rules scanner plus an out-of-band
  private denylist.

## FIX
- The public scanner now contains **generic privacy patterns only**:
  - generic Windows user-home paths (`X:\Users\<user>\...`, any username)
  - generic Unix user-home paths (`/home/<user>/...`) and `~/`
  - API-key / PAT formats (GitHub `ghp_`/`github_pat_`, HF `hf_`, `sk-`, AWS
    `AKIA`)
  - private-key blocks, bearer credentials, cookie/credential-looking values
  - placeholders such as `C:\Users\<USER>\...`, `/home/<USER>/`,
    `C:\path\to\project` are **not** flagged (they are documentation examples,
    not identities)
- Scanner self-artifacts (the scanner and its unit-test fixtures) are excluded
  from the scanner's own content pass by documented design (they necessarily
  contain the generic path literals and synthetic fixtures they implement);
  they are verified instead by unit tests and by the private denylist run.
- The optional `--private-patterns <path>` flag lets the same validator accept
  an external private pattern file, but **no private pattern file ships** with
  the public release.

## PRIVATE-SCAN DESIGN
- `internal/private-release-check/` (outside the release candidate, the public
  preview, and any public package) holds the real machine-specific denylist and
  `scan_private.py`. It scans the entire `public-release-preview/` and reports
  only PASS/FAIL and counts — **never the denylist values or matched text**.
- Result: **PRIVATE PRE-PUBLISH SCAN: PASS** (68 files, 6 denylist patterns,
  0 hits) — including the validator source itself.

## PUBLIC GENERIC-SCAN DESIGN
- `scripts/validate_public_release_preview.py` validates the manifest,
  excluded-artifact absence (filename + content signature), the frozen
  question set presence, and the generic privacy scan; reports
  categories/counts/PASS only.
- `public-release-preview/PUBLIC-PREVIEW-LEAK-CHECK.md` reports the same
  generic scan result (PASS) plus the private-scan PASS line, with no values.

## REGRESSION TEST
- `scripts/test_public_scanner.py` (all PASS):
  A. generic Windows user-home detected
  B. generic Unix user-home detected
  C. credential-like patterns detected (PAT / bearer / private key / cookie)
  D. placeholder paths not treated as identity leaks
  E. validator source: no unexpected generic-scan hits, 0 private-denylist
     hits (private denylist read via `PRIVATE_DENYLIST` env var)
  F. public preview passes the generic scan and the private-denylist scan
  G. private denylist config is not inside the public preview

## VALIDATION
- Original P0 values (real username, real project path): **0 occurrences** in
  `public-release-preview/` and **0** in the validator source
  (private denylist scan, PASS).
- Public validator CLI on the preview: **PUBLIC RELEASE PREVIEW: VALID**,
  generic privacy scan clean, 68 files, 0 answer datasets.
- Research-data regression vs R2.1: all 11 core data files byte-identical
  (scores, objectives, loop audits, d-vs-c, locked scorebooks, frozen
  questions); D structural numbers unchanged (192/119/77/0/115); full
  non-inference validation suite PASS.
- Closed-P1 rechecks: preview exists with answer CSVs excluded (P1-1);
  D manual audit not mutated (P1-2, SHA unchanged); SECURITY-AND-PRIVACY
  matches Option B (P1-3).

## STATUS
- **CLOSED.** No research data, score, mapping, or methodology changed. R2.1
  is preserved unmodified. Not published.
