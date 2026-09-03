"""Build the Huihui Nex extension final-answer dataset (v1.2.1 candidate).

Extracts the 32 frozen Formal C final answers of the post-release extension
contestant (opaque id LR37 / internal tag H7) from the extension generation
artifacts (two .jsonl files: 18 general + 14 cyber) and writes
`data/model-answers/G-huihui-nex/formal-c.csv`.

INTEGRITY RULES
  - ONLY the `response` field is released. The artifacts also carry a
    `reasoning` field (hidden chain-of-thought) which is NEVER written out.
  - answer text is copied byte-for-byte; no normalization, trimming,
    reflowing or rewriting of any kind
  - round-trip verification against the source string
  - every row is scanned with the same generic public-release privacy
    patterns used by validate_public_release_preview.py; a hit fails closed
    unless it is bound to an exact-row-identity waiver in REVIEWED_FP
    (condition + model + question_id + pattern + matched-substring SHA-256 +
    full-answer SHA-256). There are currently no waivers for this extension.

TRACEABILITY
  - question ids must equal the frozen question files' ids
  - prompt text must equal the frozen question text
  - question ids must equal the locked extension scorebook rows
  - no locked score is ever recomputed

The generation artifacts live outside this repository (internal run archive);
pass their directory with --source-dir. No machine-specific path is embedded.

Usage:
  python scripts/build_extension_answer_dataset.py --source-dir <dir with the two jsonl>
  python scripts/build_extension_answer_dataset.py --verify-only
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REPO_ROOT = os.path.dirname(HERE)

MODEL_NAME = "Huihui-Nex-N2-mini-abliterated-Q4_K_M"
DATASET_DIR = "G-huihui-nex"
CONDITION = "formal-c"
FIELDS = ["condition", "model", "division", "question_id", "question", "final_answer"]
SRC_FILES = ["H7-general-questions.jsonl", "H7-cyber-questions.jsonl"]

# reviewed false positives, bound to exact row identity (see module docstring).
# Empty: the extension answers produced no generic-pattern hits.
REVIEWED_FP = {}

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


def division_of(qid):
    return "general" if qid.upper().startswith("G") else "cyber"


def read_questions(repo_root):
    out = {}
    for fn in ("questions-general.json", "questions-cyber.json"):
        p = os.path.join(repo_root, "data", fn)
        for q in json.load(open(p, encoding="utf-8")):
            out[q["id"]] = q["prompt"]
    return out


def read_scorebook_ids(repo_root):
    p = os.path.join(repo_root, "extensions", "huihui-nex-n2-mini-abliterated-q4",
                     "FORMAL-C-EXTENSION-BLIND-SCORES-LOCKED.md")
    txt = open(p, encoding="utf-8").read()
    seen = []
    for m in re.findall(r"^\|\s*(G\d+|C\d+)\s*\|", txt, re.M):
        if m not in seen:
            seen.append(m)
    return seen


def verify(repo_root):
    """Re-check the published extension CSV against frozen artifacts."""
    p = os.path.join(repo_root, "data", "model-answers", DATASET_DIR, CONDITION + ".csv")
    problems = []
    if not os.path.exists(p):
        return ["missing %s" % p]
    with open(p, encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        rows = list(r)
        header = r.fieldnames
    if header != FIELDS:
        problems.append("bad schema: %s" % header)
    if len(rows) != 32:
        problems.append("%d rows (expected 32)" % len(rows))
    ids = [x["question_id"] for x in rows]
    if len(set(ids)) != 32:
        problems.append("duplicate/missing question ids")
    qs = read_questions(repo_root)
    sb = set(read_scorebook_ids(repo_root))
    for x in rows:
        if x["model"] != MODEL_NAME:
            problems.append("wrong model %r" % x["model"])
        if x["condition"] != CONDITION:
            problems.append("wrong condition %r" % x["condition"])
        if x["question_id"] not in qs:
            problems.append("unknown question id %s" % x["question_id"])
        elif x["question"] != qs[x["question_id"]]:
            problems.append("question text drift at %s" % x["question_id"])
        if x["question_id"] not in sb:
            problems.append("no locked score row for %s" % x["question_id"])
        if division_of(x["question_id"]) != x["division"]:
            problems.append("division mismatch at %s" % x["question_id"])
    if set(ids) != sb:
        problems.append("id set != locked scorebook id set")
    # privacy re-scan with row-identity binding
    for x in rows:
        for cat, pat in GENERIC_PATTERNS:
            m = pat.search(x["final_answer"] or "")
            if not m:
                continue
            anchor = hashlib.sha256(m.group(0).encode("utf-8")).hexdigest()
            answer_sha = hashlib.sha256((x["final_answer"] or "").encode("utf-8")).hexdigest()
            b = REVIEWED_FP.get(anchor)
            if b and all((b["pattern"] == cat,
                          b["condition"] == x["condition"],
                          b["model"] == x["model"],
                          b["question_id"] == x["question_id"],
                          b["answer_sha256"] == answer_sha)):
                continue
            problems.append("privacy hit %s at %s" % (cat, x["question_id"]))
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default=None)
    ap.add_argument("--repo-root", default=DEFAULT_REPO_ROOT)
    ap.add_argument("--verify-only", action="store_true")
    args = ap.parse_args()

    if args.verify_only:
        problems = verify(args.repo_root)
        print("verify-only: extension dataset check")
        if problems:
            for p in problems:
                print("  FAIL  %s" % p)
            return 1
        print("  PASS  32 rows / schema / question+scorebook alignment / privacy")
        return 0

    if not args.source_dir or not os.path.isdir(args.source_dir):
        fail("--source-dir must point at the directory holding the two extension jsonl files")

    rows = []
    for fn in SRC_FILES:
        p = os.path.join(args.source_dir, fn)
        if not os.path.exists(p):
            fail("missing source artifact: %s" % fn)
        for line in open(p, encoding="utf-8"):
            if line.strip():
                rows.append(json.loads(line))
    if len(rows) != 32:
        fail("source has %d rows (expected 32)" % len(rows))

    qs = read_questions(args.repo_root)
    sb = set(read_scorebook_ids(args.repo_root))
    src_ids = [r["id"] for r in rows]
    if len(set(src_ids)) != 32:
        fail("source ids not unique/complete")
    if set(src_ids) != sb:
        fail("source ids != locked scorebook ids")

    out = []
    for r in rows:
        qid = r["id"]
        text = r["response"] if r.get("response") is not None else ""
        if qid not in qs:
            fail("question %s not in frozen question files" % qid)
        if r.get("prompt") != qs[qid]:
            fail("prompt drift at %s — refusing to build" % qid)
        for cat, pat in GENERIC_PATTERNS:
            m = pat.search(text or "")
            if not m:
                continue
            anchor = hashlib.sha256(m.group(0).encode("utf-8")).hexdigest()
            answer_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
            b = REVIEWED_FP.get(anchor)
            if b and all((b["pattern"] == cat, b["condition"] == CONDITION,
                          b["model"] == MODEL_NAME, b["question_id"] == qid,
                          b["answer_sha256"] == answer_sha)):
                print("  reviewed-FP (%s) at %s — exact row identity verified" % (cat, qid))
                continue
            fail("privacy pattern %s at %s — row NOT released" % (cat, qid))
        out.append({"condition": CONDITION, "model": MODEL_NAME,
                    "division": division_of(qid), "question_id": qid,
                    "question": qs[qid], "final_answer": text})

    out.sort(key=lambda x: (0 if x["division"] == "general" else 1,
                            int(re.sub(r"\D", "", x["question_id"]))))

    dest_dir = os.path.join(args.repo_root, "data", "model-answers", DATASET_DIR)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, CONDITION + ".csv")
    with open(dest, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(out)

    # byte-faithful round-trip
    with open(dest, encoding="utf-8-sig", newline="") as f:
        back = list(csv.DictReader(f))
    if len(back) != 32:
        fail("round-trip row count mismatch")
    src_by_id = {r["id"]: r["response"] for r in rows}
    for b in back:
        if b["final_answer"] != src_by_id[b["question_id"]]:
            fail("round-trip answer text differs at %s" % b["question_id"])
        if "reasoning" in b:
            fail("reasoning field leaked into output")

    print("BUILD OK: wrote 32 answers -> %s"
          % os.path.relpath(dest, args.repo_root))
    problems = verify(args.repo_root)
    if problems:
        for p in problems:
            print("  FAIL  %s" % p)
        return 1
    print("  PASS  post-build verify: 32 rows / schema / question+scorebook "
          "alignment / privacy")
    return 0


if __name__ == "__main__":
    sys.exit(main())
