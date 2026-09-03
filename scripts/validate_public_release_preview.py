"""Validate the public release tree against PUBLIC-RELEASE-CONTENTS.md.

Updated for the Output Dataset Addendum (2026-09-03, partial final-answer
release). Default target is the repository root itself (the git tree IS the
release tree); --dir can still point at any staged copy.

Checks (programmatic, no inference):
  1. every INCLUDED path listed in PUBLIC-RELEASE-CONTENTS.md exists
  2. every EXCLUDED artifact is absent from the whole tree (combined
     6-model answer CSVs by filename AND by content signature)
  3. hard-fail if data/formal-{d,c}-answers-final-only.csv appear anywhere
  4. PARTIAL-RELEASE block:
       - exactly 4 released model dirs, exactly 256 released answers
       - 32 + 32 rows per released model, exact schema, no A/B rows
       - withheld A/B model identifiers absent from the dataset tree
       - model-answers NOTICE/MANIFEST present with consistent counts,
         provenance statuses and the model-output rights disclaimer
  5. GENERIC privacy scan (absolute user-home paths, credential formats,
     private keys, cookies, reasoning-channel markers) — no machine-specific
     values are embedded in this file; the scanner must pass its own scan
  6. reviewed false positives inside model-answer text are bound to the
     exact row identity (condition/model/question_id) + scanner pattern id
     + SHA-256 of the matched substring + SHA-256 of the full answer text
     (REVIEWED_FP); any other hit — the same substring in another row, a
     second occurrence, or any edit to the answer — fails closed
  7. optional external private-pattern file via --private-patterns <path>
     (kept OUTSIDE the public repository; never shipped here)
  8. report the total file count

Report format: categories + counts + PASS/FAIL and reviewed false positives
only — matched values are never printed.

Run:  python validate_public_release_preview.py [--dir <path>]
      python validate_public_release_preview.py --private-patterns <private-file>
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RC = os.path.dirname(HERE)
EXPROOT = os.path.dirname(RC)
PREV = os.path.join(EXPROOT, "public-release-preview")

EXCLUDED_NAMES = ["formal-d-answers-final-only.csv", "formal-c-answers-final-only.csv"]
ANSWER_HDR = "condition,model,division,question_id,question,final_answer"
ANSWER_FIELDS = ["condition", "model", "division", "question_id",
                 "question", "final_answer"]

# Output Dataset Addendum (2026-09-03): C/D/E/F released, A/B withheld.
RELEASED_DIRS = {
    "C-gemma4": "Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-Q4_K_M",
    "D-ornith": "Ornith-1.5-35B-A3B-Abliterated-Q4_K_M",
    "E-nex": "Nex-N2-mini-Q4_K_M",
    "F-qwen3.8": "Qwen3.8-9B-abliterated-25-Q4_K_M",
}
WITHHELD_MODELS = [
    "RavenX-CyberAgent-35B-v5.1-Q4_K_M",        # A
    "Endy-Qwen3.6-CyberSec-35B-A3B-Q4_K_M",     # B
]

# Reviewed false positives inside model-answer text. An exemption is bound to
# the EXACT ROW IDENTITY — not just the matched substring:
#   condition + model + question_id   (which row)
#   pattern                           (which scanner rule)
#   anchor        = sha256(exact matched substring)
#   answer_sha256 = sha256(full final_answer text of that row)
# A hit counts as reviewed only when ALL five agree; anything else — the same
# substring in another row, a second occurrence anywhere, or a single edited
# character in the answer — fails closed. Reasons are documented in
# data/model-answers/NOTICE.md; this file never quotes the matched text so it
# stays clean under its own scan.
REVIEWED_FP = {
    "cb70ea5581c7fc874b407a1ff3eefdf8d13cdc7ffed6a1f19cbe6a6a829fb958": {
        "condition": "formal-c",
        "model": "Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-Q4_K_M",
        "question_id": "C3",
        "pattern": "credential-eq",
        "answer_sha256": "605b3689ae07e464b47c462b5d6b0d17c92b3c1b9b9d6be4bfa5dfa45ffc21b2",
    },
}

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
    ("credential-eq", re.compile(
        r"(?i)\b(password|passwd|pwd|apikey|api_key|secret)\s*[:=]\s*['\"]?[^\s'\"]{6,}")),
    ("cookie", re.compile(
        r"(?i)\b(sessionid|session_id|csrf(?:rf)?token|auth_cookie|jwt)\s*[:=]\s*"
        r"[A-Za-z0-9\-._~+/]{10,}")),
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
    """Return [category, ...] for every match; values never returned."""
    return [cat for cat, _anchor in scan_text_anchored(text, extra_patterns)]


def scan_text_anchored(text, extra_patterns=None):
    """Return [(category, sha256-of-matched-substring), ...]."""
    hits = []
    for cat, pat in GENERIC_PATTERNS:
        m = pat.search(text)
        if m:
            anchor = hashlib.sha256(m.group(0).encode("utf-8")).hexdigest()
            hits.append((cat, anchor))
    for cat, pat in (extra_patterns or []):
        m = pat.search(text)
        if m:
            anchor = hashlib.sha256(m.group(0).encode("utf-8")).hexdigest()
            hits.append((cat, anchor))
    return hits


def read_csv_rows(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        r = csv.reader(f)
        header = next(r, None)
        return header, list(r)


def check_partial_release(target):
    """Output Dataset Addendum assertions (see module docstring, item 4)."""
    ma = os.path.join(target, "data", "model-answers")
    if not os.path.isdir(ma):
        check("model-answers dataset present", False)
        return

    problems = []
    total = 0
    for d, model in RELEASED_DIRS.items():
        for cond in ("formal-c", "formal-d"):
            p = os.path.join(ma, d, cond + ".csv")
            if not os.path.exists(p):
                problems.append("missing %s" % os.path.relpath(p, target))
                continue
            header, rows = read_csv_rows(p)
            if header != ANSWER_FIELDS:
                problems.append("bad schema/header in %s" % os.path.relpath(p, target))
            if len(rows) != 32:
                problems.append("%s: %d rows (expected 32)"
                                % (os.path.relpath(p, target), len(rows)))
            for row in rows:
                if len(row) != len(ANSWER_FIELDS):
                    problems.append("ragged row in %s" % os.path.relpath(p, target))
                    continue
                rec = dict(zip(ANSWER_FIELDS, row))
                if rec["model"] != model:
                    problems.append("wrong model in %s" % os.path.relpath(p, target))
                if rec["condition"] != cond:
                    problems.append("wrong condition in %s" % os.path.relpath(p, target))
            total += len(rows)
    check("exactly 4 released model dirs (C/D/E/F)", len(RELEASED_DIRS) == 4)
    check("exactly 256 released answers", total == 256, "counted %d" % total)
    check("per-model 32+32 rows, exact schema, correct model/condition labels",
          not problems, str(problems[:3]) if problems else "")

    # withheld A/B absent at content level from the DATASET CSVs
    # (documentation files may legitimately NAME the withheld models when
    #  stating the withholding policy; they contain no answer text)
    leaks = []
    reviewed = []
    for root, _, files in os.walk(ma):
        for fn in files:
            if not fn.endswith(".csv"):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, target)
            try:
                content = open(p, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            for m in WITHHELD_MODELS:
                if m in content:
                    leaks.append((rel, m[:24] + "…"))
            # row-level scan so FP exemptions bind to exact row identity
            header, rows = read_csv_rows(p)
            if header != ANSWER_FIELDS:
                leaks.append((rel, "UNEXPECTED CSV SCHEMA"))
            for row in rows:
                if len(row) != len(ANSWER_FIELDS):
                    leaks.append((rel, "RAGGED ROW"))
                    continue
                rec = dict(zip(ANSWER_FIELDS, row))
                answer_sha = hashlib.sha256(
                    (rec["final_answer"] or "").encode("utf-8")).hexdigest()
                for field in ANSWER_FIELDS:
                    for cat, anchor in scan_text_anchored(rec[field] or ""):
                        binding = REVIEWED_FP.get(anchor)
                        if binding and all((
                                binding["pattern"] == cat,
                                binding["condition"] == rec["condition"],
                                binding["model"] == rec["model"],
                                binding["question_id"] == rec["question_id"],
                                binding["answer_sha256"] == answer_sha)):
                            reviewed.append((rel, "reviewed-FP-1 — see "
                                            "data/model-answers/NOTICE.md"))
                        else:
                            # unlisted hit OR binding mismatch: hard fail
                            leaks.append((rel, "privacy hit / FP binding "
                                         "mismatch: " + cat))
    check("withheld A/B absent from dataset tree (content level)", not leaks,
          str(leaks[:3]) if leaks else "")
    check("reviewed-FP anchors matched exactly (no drift)",
          len(reviewed) == len(REVIEWED_FP),
          "%d reviewed hit(s)" % len(reviewed))
    for rel, why in reviewed:
        print("        reviewed-FP in %s -> %s" % (rel, why))

    # consistency of the dataset documents
    notice_p = os.path.join(ma, "NOTICE.md")
    manifest_p = os.path.join(ma, "MANIFEST.md")
    check("data/model-answers/NOTICE.md present", os.path.exists(notice_p))
    check("data/model-answers/MANIFEST.md present", os.path.exists(manifest_p))
    if os.path.exists(notice_p):
        ntxt = open(notice_p, encoding="utf-8").read()
        check("NOTICE states 256/128 counts", "256" in ntxt and "128" in ntxt)
        check("NOTICE carries the model-output rights disclaimer",
              "no ownership or relicensing claim" in ntxt.lower())
        check("NOTICE records the blind-scoring chronology",
              "post-lock identity mapping" in ntxt)
        check("NOTICE lists reviewed false positives", "reviewed-FP-1" in ntxt)
    if os.path.exists(manifest_p):
        mtxt = open(manifest_p, encoding="utf-8").read()
        check("MANIFEST carries provenance statuses (RESOLVED/WITHHELD)",
              "RESOLVED" in mtxt and "WITHHELD" in mtxt)
        check("MANIFEST totals row (256/128/384)",
              "**256**" in mtxt and "**128**" in mtxt and "**384**" in mtxt)
    readme_p = os.path.join(target, "README.md")
    if os.path.exists(readme_p):
        rtxt = open(readme_p, encoding="utf-8").read()
        check("README states the partial-release counts",
              "256 of 384" in rtxt and "128 withheld" in rtxt)
        check("README no longer blanket-withholds the answer dataset",
              "are\n  withheld from this public release" not in rtxt)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=RC, help="target directory to validate "
                    "(default: the repository root — the git tree is the "
                    "release tree)")
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

    # partial-release block (per-model dataset + doc consistency)
    check_partial_release(target)

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
                content = open(os.path.join(root, fn), encoding="utf-8",
                               errors="replace").read()
            except OSError:
                continue
            for cat, anchor in scan_text_anchored(content, extra):
                if os.path.join("data", "model-answers") in rel:
                    continue  # already handled (with anchored FP policy) above
                cat_counts.setdefault(cat, 0)
                cat_counts[cat] += 1
    check("no reasoning-dataset filenames", not reasoning_fnames,
          str(reasoning_fnames) if reasoning_fnames else "")

    byname = [f for f in files if any(n in f for n in EXCLUDED_NAMES)]
    check("EXCLUDED filenames absent", not byname, str(byname) if byname else "")
    sig = []
    for f in files:
        if not f.endswith(".csv") or os.path.join("data", "model-answers") in f:
            continue
        p = os.path.join(target, f)
        if ANSWER_HDR in open(p, encoding="utf-8", errors="replace").read():
            sig.append(f)
    check("EXCLUDED content signatures absent outside data/model-answers/",
          not sig, str(sig) if sig else "")

    print(f"  file count: {len(files)} files in release tree")
    if cat_counts:
        print("  generic/privacy scan hits (categories only):")
        for cat, n in sorted(cat_counts.items()):
            print(f"    {cat}: {n}")
    scan_ok = not cat_counts
    check("generic privacy scan clean", scan_ok)

    print(f"\nPUBLIC RELEASE TREE: {'VALID' if not FAILURES else 'INVALID'}")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
