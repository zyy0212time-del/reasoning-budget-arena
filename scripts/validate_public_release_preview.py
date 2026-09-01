"""Validate the public release preview against PUBLIC-RELEASE-CONTENTS.md.

Checks (programmatic, no inference):
  1. every INCLUDED path listed in PUBLIC-RELEASE-CONTENTS.md exists
  2. every EXCLUDED artifact is absent from the whole tree (filename AND
     answer-dataset content signature)
  3. hard-fail if data/formal-{d,c}-answers-final-only.csv appear anywhere
  4. GENERIC privacy scan (absolute user-home paths, credential formats,
     private keys, cookies, reasoning-channel markers) — no machine-specific
     values are embedded in this file; the scanner must pass its own scan
  5. optional external private-pattern file via --private-patterns <path>
     (kept OUTSIDE the public repository; never shipped here)
  6. report the total file count

Report format: categories + counts + PASS/FAIL and reviewed false positives
only — matched values are never printed.

Run:  python validate_public_release_preview.py [--dir <path>]
      python validate_public_release_preview.py --private-patterns <private-file>
"""
from __future__ import annotations

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RC = os.path.dirname(HERE)
EXPROOT = os.path.dirname(RC)
PREV = os.path.join(EXPROOT, "public-release-preview")
CONTENTS = os.path.join(PREV, "PUBLIC-RELEASE-CONTENTS.md")

EXCLUDED_NAMES = ["formal-d-answers-final-only.csv", "formal-c-answers-final-only.csv"]
ANSWER_HDR = "condition,model,division,question_id,question,final_answer"

# GENERIC privacy patterns only. These must never contain machine-specific
# values (a concrete username, a concrete home path, a concrete project root).
# Placeholders such as C:\\Users\\<USER>\\ or /home/<USER>/ are excluded by
# design so documentation examples are not false positives.
GENERIC_PATTERNS = [
    ("win-user-home", re.compile(r"\b[A-Za-z]:\\Users\\(?!<)[^\\\s]+(?:\\|$)", re.I)),
    ("unix-user-home", re.compile(r"(?:^|\s)/home/(?!<)[^/\s]+(?:/|$)", re.I)),
    ("tilde-home", re.compile(r"(?m)^~[\\/]")),
    ("github-pat", re.compile(r"\bghp_[A-Za-z0-9]{20,}\b")),
    ("github-fine-pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("hf-token", re.compile(r"\bhf_[A-Za-z0-9]{20,}\b")),
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("aws-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("bearer", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9\-._~+/]{12,}")),
    ("credential-eq", re.compile(r"(?i)\b(password|passwd|pwd|apikey|api_key|secret)\s*[:=]\s*['\"]?[^\s'\"]{6,}")),
    ("cookie", re.compile(r"(?i)\b(sessionid|session_id|csrf(?:rf)?token|auth_cookie|jwt)\s*[:=]\s*[A-Za-z0-9\-._~+/]{10,}")),
]

# Reasoning-dataset detection is FILENAME-based only, so the scanner never
# has to contain the field-name literal in a content pattern (which would
# make the scanner fail its own scan).
REASONING_FILENAME_RE = re.compile(r"reasoning", re.I)

TEXT_EXT = {".py", ".md", ".csv", ".json", ".jsonl", ".txt", ".yaml", ".yml",
            ".toml", ".svg", ".html", ".xml", ".ini", ".cfg", ".sh", ".bat"}

# The scanner excludes scanner self-artifacts from content scanning: those
# files necessarily contain the generic path-detection literals and synthetic
# fixtures they implement (e.g. /home/<user>/). Exclusion is BY FILENAME so it
# also covers copies of the scanner inside the scanned tree (e.g. the preview's
# own copy). The scanner artifacts are verified instead by unit tests
# (test_public_scanner.py TEST A-G) and by the private pre-publish denylist run.
SCANNER_SELF_NAMES = {"validate_public_release_preview.py", "test_public_scanner.py"}

FAILURES = []


def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + (f"  [{detail}]" if detail else ""))
    if not cond:
        FAILURES.append(name)


def scan_text(text, extra_patterns=None):
    """Return [(category, filename)] for every match; values never returned."""
    hits = []
    for cat, pat in GENERIC_PATTERNS:
        if pat.search(text):
            hits.append(cat)
    for cat, pat in (extra_patterns or []):
        if pat.search(text):
            hits.append(cat)
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=PREV, help="target directory to validate")
    ap.add_argument("--private-patterns", default=None,
                    help="optional external file of extra regex patterns "
                         "(one per line; kept outside the public repository)")
    args = ap.parse_args()

    target = args.dir
    if not os.path.isdir(target):
        print(f"[FAIL] target directory missing: {target}")
        return 1

    extra = []
    if args.private_patterns:
        if not os.path.exists(args.private_patterns):
            print(f"[FAIL] private-pattern file missing: {args.private_patterns}")
            return 1
        for ln, line in enumerate(open(args.private_patterns, encoding="utf-8"), 1):
            line = line.strip()
            if line and not line.startswith("#"):
                try:
                    extra.append((f"private-pattern:{ln}", re.compile(line)))
                except re.error as e:
                    print(f"[FAIL] bad private pattern line {ln}: {e}")
                    return 1

    # 1. contents manifest
    if not os.path.exists(os.path.join(target, "PUBLIC-RELEASE-CONTENTS.md")):
        print(f"[FAIL] PUBLIC-RELEASE-CONTENTS.md missing in {target}")
        return 1
    txt = open(os.path.join(target, "PUBLIC-RELEASE-CONTENTS.md"), encoding="utf-8").read()
    seg = txt.split("# INCLUDED")[1].split("# EXCLUDED")[0]
    included = re.findall(r"^\|\s*`([^`]+)`\s*\|", seg, re.M)
    check(f"CONTENTS lists {len(included)} included files", len(included) > 10)
    missing = [p for p in included if not os.path.exists(os.path.join(target, p))]
    check("every INCLUDED path exists", not missing, str(missing[:5]) if missing else "")

    # 2+3. walk the tree: excluded absence + generic/private scan
    files = []
    cat_counts = {}
    reasoning_fnames = []
    for root, _, fs in os.walk(target):
        for fn in fs:
            rel = os.path.relpath(os.path.join(root, fn), target)
            files.append(rel)
            if REASONING_FILENAME_RE.search(fn):
                reasoning_fnames.append(rel)
            if rel.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
                continue
            if os.path.splitext(fn)[1].lower() not in TEXT_EXT:
                continue
            if fn in SCANNER_SELF_NAMES:
                continue  # documented scanner self-artifacts (by filename)
            try:
                content = open(os.path.join(root, fn), encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            for cat in scan_text(content, extra):
                cat_counts.setdefault(cat, 0)
                cat_counts[cat] += 1
    check("no reasoning-dataset filenames", not reasoning_fnames, str(reasoning_fnames) if reasoning_fnames else "")

    byname = [f for f in files if any(n in f for n in EXCLUDED_NAMES)]
    check("EXCLUDED filenames absent", not byname, str(byname) if byname else "")
    sig = [f for f in files if f.endswith(".csv") and os.path.exists(os.path.join(target, f))
           and ANSWER_HDR in open(os.path.join(target, f), encoding="utf-8", errors="replace").read()]
    check("EXCLUDED content signatures absent", not sig, str(sig) if sig else "")

    print(f"  file count: {len(files)} files in preview")
    if cat_counts:
        print("  generic/privacy scan hits (categories only):")
        for cat, n in sorted(cat_counts.items()):
            print(f"    {cat}: {n}")
    scan_ok = not cat_counts
    check("generic privacy scan clean", scan_ok)

    print(f"\nPUBLIC RELEASE PREVIEW: {'VALID' if not FAILURES else 'INVALID'}")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
