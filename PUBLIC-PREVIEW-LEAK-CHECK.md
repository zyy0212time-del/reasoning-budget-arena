# PUBLIC PREVIEW LEAK CHECK

Generated: 2026-09-01 22:31:26

Dedicated generic scan of the final public artifact tree. Reports only
categories and counts — matched values are never shown.

Answer-dataset files found in preview: NONE (0)

## FINDINGS
**none**

## Scanner self-artifacts (documented design)
scripts/validate_public_release_preview.py and scripts/test_public_scanner.py
are excluded from this content scan because they necessarily contain the
generic path-detection literals and synthetic detection fixtures they
implement. They are verified instead by unit tests (test_public_scanner.py
TEST A-G) and by the private machine-specific denylist scan below.

## Private machine-specific denylist scan
Run separately by internal/private-release-check/scan_private.py (the
denylist itself never enters any public artifact or this report).
Result: PASS (0 hits).

**PUBLIC PREVIEW LEAK CHECK: PASS**
