"""Build the per-model public final-answer dataset (Output Dataset Addendum).

Extracts the C/D/E/F rows (4 models x 32 questions x 2 formal conditions =
256 answers) from the internal frozen final-only CSVs (192 rows each, 6
models) and writes per-model, per-condition CSVs under data/model-answers/.

A and B rows are NOT extracted and must NOT appear in the output
(withheld pending additional upstream/output-terms review).

INTEGRITY RULES
  - answer text is copied byte-for-byte from the frozen source; no
    normalization, no trimming, no rewriting, no reformatting
  - only CSV re-serialization is performed (same schema as the source)
  - the script round-trip-verifies every written row against the source
  - every extracted field is scanned with the generic public-release
    privacy patterns; on any hit the build FAILS and names the
    model/condition/question (never the matched content)

The source CSVs are internal frozen benchmark artifacts and are NOT part
of this public repository. Pass their directory explicitly; no
machine-specific path is embedded in this file.

Usage:
  python scripts/build_model_answer_dataset.py \
      --source-dir <dir containing formal-{c,d}-answers-final-only.csv> \
      [--repo-root <repo root>] [--dry-run]

  python scripts/build_model_answer_dataset.py --verify-only [--repo-root <path>]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REPO_ROOT = os.path.dirname(HERE)

# (tag, dataset dir, exact model name as used in all frozen artifacts)
RELEASED = [
    ("C", "C-gemma4", "Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-Q4_K_M"),
    ("D", "D-ornith", "Ornith-1.5-35B-A3B-Abliterated-Q4_K_M"),
    ("E", "E-nex", "Nex-N2-mini-Q4_K_M"),
    ("F", "F-qwen3.8", "Qwen3.8-9B-abliterated-25-Q4_K_M"),
]
WITHHELD_MODELS = [
    "RavenX-CyberAgent-35B-v5.1-Q4_K_M",        # A
    "Endy-Qwen3.6-CyberSec-35B-A3B-Q4_K_M",     # B
]
CONDITIONS = {"formal-c": "formal-c-answers-final-only.csv",
              "formal-d": "formal-d-answers-final-only.csv"}
FIELDS = ["condition", "model", "division", "question_id", "question", "final_answer"]

# Must stay identical to the generic patterns in
# validate_public_release_preview.py (single source of truth for this list
# is the validator; duplicated here so the builder fails closed on its own).
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


def fail(msg):
    print("FAIL: %s" % msg)
    sys.exit(1)


# Reviewed false positives inside model-answer text. An exemption is bound to
# the EXACT ROW IDENTITY — not just the matched substring:
#   condition + model + question_id   (which row)
#   pattern                           (which scanner rule)
#   anchor        = sha256(exact matched substring)
#   answer_sha256 = sha256(full final_answer text of that row)
# A hit counts as reviewed only when ALL five agree; anything else — the same
# substring in another row, a second occurrence anywhere, or a single edited
# character in the answer — fails closed. Reasons are described in
# data/model-answers/NOTICE.md. This source file deliberately never quotes
# the matched text (it must stay clean under its own generic scan).
REVIEWED_FP = {
    # C / formal-c / C3 — the answer itself constructs a dummy placeholder
    # credential as a teaching example; the answer's topic is credential-
    # scanner false positives. Reviewed 2026-09-03, answer kept byte-identical.
    "cb70ea5581c7fc874b407a1ff3eefdf8d13cdc7ffed6a1f19cbe6a6a829fb958": {
        "condition": "formal-c",
        "model": "Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-Q4_K_M",
        "question_id": "C3",
        "pattern": "credential-eq",
        "answer_sha256": "605b3689ae07e464b47c462b5d6b0d17c92b3c1b9b9d6be4bfa5dfa45ffc21b2",
    },
}


def read_source(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        if r.fieldnames != FIELDS:
            fail("unexpected schema in %s: %s" % (path, r.fieldnames))
        return list(r)


def verify(repo_root):
    """Re-check the published per-model CSVs against the locked score CSVs."""
    data = os.path.join(repo_root, "data")
    ma = os.path.join(data, "model-answers")
    problems = []

    for cond in CONDITIONS:
        scores = {}
        with open(os.path.join(data, "%s-scores.csv" % cond), encoding="utf-8-sig",
                  newline="") as f:
            for row in csv.DictReader(f):
                scores[(row["model"], row["question_id"])] = row

        for tag, d, model in RELEASED:
            p = os.path.join(ma, d, "%s.csv" % cond)
            if not os.path.exists(p):
                problems.append("missing %s" % p)
                continue
            with open(p, encoding="utf-8-sig", newline="") as f:
                rows = list(csv.DictReader(f))
            if len(rows) != 32:
                problems.append("%s: %d rows (expected 32)" % (p, len(rows)))
            qids = [r["question_id"] for r in rows]
            if len(set(qids)) != len(qids):
                problems.append("%s: duplicate question_id" % p)
            for r in rows:
                if r["model"] != model:
                    problems.append("%s: wrong model %r" % (p, r["model"]))
                if r["condition"] != cond:
                    problems.append("%s: wrong condition %r" % (p, r["condition"]))
                if (model, r["question_id"]) not in scores:
                    problems.append("%s: no locked score for %s"
                                    % (p, r["question_id"]))
            with open(os.path.join(data, "questions-general.json"), encoding="utf-8") as f:
                gq = set(re.findall(r'"id"\s*:\s*"(G\d+)"', f.read()))
            with open(os.path.join(data, "questions-cyber.json"), encoding="utf-8") as f:
                cq = set(re.findall(r'"id"\s*:\s*"(C\d+)"', f.read()))
            known = gq | cq
            unknown = [q for q in qids if q not in known]
            if unknown:
                problems.append("%s: question ids not in frozen question files: %s"
                                % (p, unknown[:5]))

    total = 0
    for tag, d, model in RELEASED:
        for cond in CONDITIONS:
            p = os.path.join(ma, d, "%s.csv" % cond)
            if os.path.exists(p):
                with open(p, encoding="utf-8-sig", newline="") as f:
                    total += sum(1 for _ in csv.DictReader(f))
    if total != 256:
        problems.append("total released answers = %d (expected 256)" % total)

    # A/B must be absent everywhere under data/model-answers/
    for root, _, files in os.walk(ma):
        for fn in files:
            if not fn.endswith(".csv"):
                continue
            content = open(os.path.join(root, fn), encoding="utf-8-sig",
                           errors="replace").read()
            for m in WITHHELD_MODELS:
                if m in content:
                    problems.append("WITHHELD MODEL LEAK %r in %s" % (m, fn))

    return problems, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default=None)
    ap.add_argument("--repo-root", default=DEFAULT_REPO_ROOT)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify-only", action="store_true")
    args = ap.parse_args()

    if args.verify_only:
        problems, total = verify(args.repo_root)
        print("verify-only: %d released answers counted" % total)
        if problems:
            for p in problems:
                print("  FAIL  %s" % p)
            return 1
        print("  PASS  per-model counts / IDs / locked-score linkage / A-B absence")
        return 0

    if not args.source_dir or not os.path.isdir(args.source_dir):
        fail("--source-dir must point at the directory holding the two frozen "
             "formal-{c,d}-answers-final-only.csv files")

    src = {cond: read_source(os.path.join(args.source_dir, fn))
           for cond, fn in CONDITIONS.items()}
    for cond, rows in src.items():
        if len(rows) != 192:
            fail("%s source has %d rows (expected 192)" % (cond, len(rows)))

    out_root = os.path.join(args.repo_root, "data", "model-answers")
    written = 0

    for cond, rows in src.items():
        for tag, d, model in RELEASED:
            sel = [r for r in rows if r["model"] == model]
            if len(sel) != 32:
                fail("source %s: model %s has %d rows (expected 32)"
                     % (cond, model, len(sel)))
            # privacy scan before writing anything
            for r in sel:
                for field in FIELDS:
                    text = r[field] or ""
                    for cat, pat in GENERIC_PATTERNS:
                        m = pat.search(text)
                        if not m:
                            continue
                        anchor = hashlib.sha256(
                            m.group(0).encode("utf-8")).hexdigest()
                        binding = REVIEWED_FP.get(anchor)
                        answer_sha = hashlib.sha256(
                            (r.get("final_answer") or "").encode("utf-8")).hexdigest()
                        if binding and all((
                                binding["pattern"] == cat,
                                binding["condition"] == cond,
                                binding["model"] == r["model"],
                                binding["question_id"] == r["question_id"],
                                binding["answer_sha256"] == answer_sha)):
                            print("    reviewed-FP (%s) in %s/%s/%s — exact row "
                                  "identity verified, kept byte-identical "
                                  "(data/model-answers/NOTICE.md)"
                                  % (cat, tag, cond, r["question_id"]))
                            continue
                        fail("privacy pattern %s in %s/%s/%s — row NOT released"
                             % (cat, tag, cond, r["question_id"]))
            dest = os.path.join(out_root, d, "%s.csv" % cond)
            print("  %-40s %2d rows -> %s" % (model[:40], len(sel),
                                              os.path.relpath(dest, args.repo_root)))
            if args.dry_run:
                written += len(sel)
                continue
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=FIELDS)
                w.writeheader()
                w.writerows(sel)
            # round-trip byte-integrity check
            back = read_source(dest)  # utf-8-sig read also tolerates no-BOM
            if len(back) != 32:
                fail("round-trip row count mismatch for %s" % dest)
            for a, b in zip(sel, back):
                for field in FIELDS:
                    if a[field] != b[field]:
                        fail("round-trip field %s differs for %s/%s (answer text "
                             "must stay byte-identical)" % (field, cond, a["question_id"]))
            written += len(sel)

    print("\n%s: wrote %d answers (expected 256)"
          % ("DRY-RUN" if args.dry_run else "BUILD OK", written))
    if written != 256:
        fail("expected exactly 256 released answers")
    if not args.dry_run:
        problems, total = verify(args.repo_root)
        if problems:
            for p in problems:
                print("  FAIL  %s" % p)
            return 1
        print("  PASS  post-build verify: counts / IDs / locked-score linkage / "
              "A-B absence / privacy scan")
    return 0


if __name__ == "__main__":
    sys.exit(main())
