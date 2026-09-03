"""Regression tests for the public release scanner.

Tests (no inference, no network):
  A. generic Windows user-home path is detected
  B. generic Unix user-home path is detected
  C. credential-like patterns are detected (PAT / bearer / private key / cookie)
  D. placeholder paths (e.g. C:\\path\\to\\project, C:\\Users\\<USER>\\) are NOT
     treated as identity leaks
  E. the public validator source passes its own generic scan and contains no
     machine-specific denylist literals (private denylist read from the
     PRIVATE_DENYLIST env var, if provided)
  F. the public release preview passes the generic scan (and, if
     PRIVATE_DENYLIST is set, the private denylist scan too)
  G. the private denylist config is not inside the public preview

This file intentionally contains NO machine-specific identifiers.

Run:  python test_public_scanner.py
      (set PRIVATE_DENYLIST=/path/to/internal/denylist to enable the
       private-denylist sub-tests of E/F)
"""
from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import validate_public_release_preview as v  # noqa: E402

RC = os.path.dirname(HERE)
EXPROOT = os.path.dirname(RC)
# The git tree IS the release tree, so by default the scanner tests run
# against the repository root itself (same default as the validator).
# Set PUBLIC_PREVIEW_DIR to point the tests at a staged preview copy instead.
PREV = os.environ.get("PUBLIC_PREVIEW_DIR") or RC
FAILURES = []


def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + (f"  [{detail}]" if detail else ""))
    if not cond:
        FAILURES.append(name)


def read_file(p):
    return open(p, encoding="utf-8", errors="replace").read()


def scan_paths(paths, extra):
    hits = []
    for p in paths:
        for cat in v.scan_text(read_file(p), extra):
            hits.append((os.path.basename(p), cat))
    return hits


print("== A. generic Windows user-home detected ==")
# Python source: double-backslashes produce a single-backslash runtime string
src = "const P = 'C:\\Users\\jsmith\\Documents\\x';"
check("C:\\Users\\<user>\\ detected", "win-user-home" in v.scan_text(src))

print("== B. generic Unix user-home detected ==")
src = "from /home/jsmitty/project read"
check("/home/<user>/ detected", "unix-user-home" in v.scan_text(src))

print("== C. credential-like patterns detected ==")
checks = [
    ("github PAT", "ghp_" + "A" * 36),
    ("HF token", "hf_" + "B" * 24),
    ("bearer token", "Authorization: Bearer abcDEF0123456789"),
    ("private key", "-----BEGIN RSA PRIVATE KEY-----"),
    ("cookie", "sessionid=" + "C" * 12),
]
for name, sample in checks:
    check(f"{name} detected", len(v.scan_text(sample)) > 0)

print("== D. placeholder paths are NOT identity leaks ==")
for name, sample in [
    ("drive placeholder", "C:\\path\\to\\project\\data"),
    ("win home placeholder", "C:\\Users\\<USER>\\Documents"),
    ("unix home placeholder", "/home/<USER>/project"),
    ("relative path", "raw/formal-c/E/file.jsonl"),
]:
    check(f"placeholder not flagged: {name}", v.scan_text(sample) == [])

print("== E. validator source: self-scan clean + no machine-specific literals ==")
val_src = read_file(os.path.join(HERE, "validate_public_release_preview.py"))
self_hits = v.scan_text(val_src)
# The path-detection literals (win-user-home / unix-user-home / tilde-home)
# legitimately self-reference by design; every OTHER category must be empty.
designed = {"win-user-home", "unix-user-home", "tilde-home"}
unexpected = [c for c in self_hits if c not in designed]
check("validator source: no unexpected generic-scan hits", unexpected == [], str(unexpected))
check("validator source: only designed path-literal self-references",
      set(self_hits) <= designed, str(self_hits))
def load_extra():
    deny = os.environ.get("PRIVATE_DENYLIST")
    if not deny or not os.path.exists(deny):
        return None
    return [("deny", re.compile(l.strip())) for l in open(deny, encoding="utf-8")
            if l.strip() and not l.startswith("#")]


extra = load_extra()
if extra is not None:
    # check ONLY the private denylist patterns (generic patterns are checked above)
    check("validator source: 0 private-denylist hits",
          [c for c in v.scan_text(val_src, extra) if c.startswith("deny")] == [])
else:
    print("  SKIP  private-denylist sub-test (PRIVATE_DENYLIST not set)")

print("== F. public preview passes the generic scan ==")
if os.path.isdir(PREV):
    prev_files = []
    for root, _, fs in os.walk(PREV):
        for fn in fs:
            p = os.path.join(root, fn)
            if fn in v.SCANNER_SELF_NAMES:
                continue  # scanner self-artifacts excluded by design (unit-tested)
            if os.path.join("data", "model-answers") in p:
                continue  # released answer text is governed by the validator's
                          # anchored reviewed-FP policy (its items 4 and 6)
            if os.path.splitext(fn)[1].lower() in v.TEXT_EXT:
                prev_files.append(p)
    hits = scan_paths(prev_files, [])
    check("preview generic scan clean", hits == [], str(hits[:5]) if hits else "")
    if extra is not None:
        dhits = scan_paths(prev_files, extra)
        check("preview private-denylist scan clean",
              [h for h in dhits if h[1].startswith("deny")] == [],
              str([h for h in dhits if h[1].startswith("deny")][:5]) if dhits else "")
    else:
        print("  SKIP  preview private-denylist sub-test (PRIVATE_DENYLIST not set)")
else:
    check("preview exists (TEST F)", False, "public-release-preview missing")

print("== G. private denylist config is not inside the public preview ==")
if os.path.isdir(PREV):
    names = []
    for root, _, fs in os.walk(PREV):
        for fn in fs:
            names.append(os.path.relpath(os.path.join(root, fn), PREV))
    bad = [n for n in names if "private-release-check" in n or "denylist" in n.lower()]
    check("no private config in preview", not bad, str(bad) if bad else "")
else:
    check("preview exists (TEST G)", False, "public-release-preview missing")

print("\n" + ("ALL PUBLIC-SCANNER TESTS PASSED" if not FAILURES else f"{len(FAILURES)} FAILURES"))
sys.exit(1 if FAILURES else 0)
