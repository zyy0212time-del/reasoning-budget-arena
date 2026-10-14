"""Build the MiniCPM-V 4.7 Uncensored extension final-answer dataset.

Extracts the 32 frozen Formal C final answers of the post-release extension
contestant (opaque id K71 / release key I) from the extension generation
artifacts (two .jsonl files: 18 general + 14 cyber) and writes
- `data/model-answers/I-minicpm-v47/formal-c.csv`   (repository schema)
- `data/model-answers/I-minicpm-v47/formal-c.jsonl` (full record incl.
  locked per-question score total)

INTEGRITY RULES
  - ONLY the `response` field is released. The artifacts also carry a
    `reasoning` field (hidden chain-of-thought) which is NEVER written out.
  - answer text is copied byte-for-byte; no normalization, trimming,
    reflowing or rewriting of any kind
  - an answer with an empty final-answer field is published as the frozen
    failure marker `[NO FINAL ANSWER WITHIN FIXED BUDGET]`, exactly as the
    frozen protocol requires — the marker is benchmark output, not an edit
  - round-trip verification against the source string
  - every row is scanned with the same generic public-release privacy
    patterns used by validate_public_release_preview.py; a hit fails closed
    unless it is bound to an exact-row-identity waiver in REVIEWED_FP
    (condition + model + question_id + pattern + matched-substring SHA-256 +
    full-answer SHA-256). There are currently no waivers for this extension.
  - no locked score is ever recomputed; per-question score totals are read
    from the locked extension scorebook artifact (question-scores.json)

TRACEABILITY
  - question ids must equal the frozen question files' ids
  - prompt text must equal the frozen question text
  - question ids must equal the locked extension scorebook rows
  - aggregate totals must equal the locked 391.0 / 321.0 / 712.0

The generation artifacts live outside this repository (internal run archive);
pass their directory with --source-dir. No machine-specific path is embedded.

Usage:
  python scripts/build_minicpm_extension_answer_dataset.py --source-dir <dir>
  python scripts/build_minicpm_extension_answer_dataset.py --verify-only
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

MODEL_NAME = "MiniCPM-V-4.7-35B-A3B-Uncensored-AD-Q4_K-IQ4_XS"
DATASET_DIR = "I-minicpm-v47"
CONDITION = "formal-c"
FIELDS = ["condition", "model", "division", "question_id", "question", "final_answer"]
SRC_FILES = ["I-general-questions.jsonl", "I-cyber-questions.jsonl"]
SCOREBOOK_DIR = os.path.join("extensions", "minicpm-v-4.7-35b-a3b-uncensored")
NO_FINAL = "[NO FINAL ANSWER WITHIN FIXED BUDGET]"

# locked aggregate expectations (never recomputed from answers)
LOCKED_TOTALS = {"general": 391.0, "cyber": 321.0, "overall": 712.0}

# reviewed false positives, bound to exact row identity (see module docstring).
REVIEWED_FP = {}

GENERIC_PATTERNS = [
    ("win-user-home", re.compile(r"\b[A-Za-z]:\\Users\\(?!<)[^\\\s]+(?:\\|$)", re.I)),
    ("unix-user-home", re.compile(r"(?:^|\s)/home/(?!<)[^/\s]+(?:/|$)", re.I)),
    ("tilde-home", re.compile(r"(?m)^~[\\/]")),
    ("github-pat", re.compile(r"\bghp_[A-Za-z0-9]{20,}\b")),
    ("github-oauth", re.compile(r"\bgho_[A-Za-z0-9]{20,}\b")),
    ("github-app", re.compile(r"\bgh[sur]_[A-Za-z0-9]{20,}\b")),
    ("hf-token", re.compile(r"\bhf_[A-Za-z0-9]{20,}\b")),
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("aws-akid", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("bearer", re.compile(r"Authorization:\s*Bearer\s+\S+", re.I)),
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("cookie", re.compile(r"Cookie:\s*\S+\s*=", re.I)),
]


def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_frozen_questions(root):
    out = {}
    for div, name in (("general", "questions-general.json"), ("cyber", "questions-cyber.json")):
        with open(os.path.join(root, "data", name), encoding="utf-8") as f:
            for q in json.load(f):
                out[q["id"]] = (div, q["prompt"])
    return out


def load_rows(source_dir):
    rows = []
    for fn in SRC_FILES:
        p = os.path.join(source_dir, fn)
        if not os.path.exists(p):
            raise SystemExit("missing source artifact: %s" % p)
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default=None)
    ap.add_argument("--repo-root", default=DEFAULT_REPO_ROOT)
    ap.add_argument("--verify-only", action="store_true")
    args = ap.parse_args()
    root = args.repo_root

    frozen = load_frozen_questions(root)
    out_dir = os.path.join(root, "data", "model-answers", DATASET_DIR)

    if args.verify_only or not args.source_dir:
        csv_path = os.path.join(out_dir, "formal-c.csv")
        if not os.path.exists(csv_path):
            print("FAIL: dataset not built: %s" % csv_path)
            return 1
        with open(csv_path, encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        ids = [r["question_id"] for r in rows]
        problems = []
        if len(rows) != 32 or len(set(ids)) != 32:
            problems.append("expected 32 unique rows, got %d" % len(rows))
        if set(ids) != set(frozen):
            problems.append("ids != frozen question ids")
        for r in rows:
            if r["question"] != frozen[r["question_id"]][1]:
                problems.append("question text drift on %s" % r["question_id"])
            if r["model"] != MODEL_NAME or r["condition"] != CONDITION:
                problems.append("label drift on %s" % r["question_id"])
        if os.path.exists(os.path.join(out_dir, "formal-d.csv")):
            problems.append("extension must not ship Formal D")
        print("FAIL: %s" % problems if problems
              else "OK: 32 rows, ids/questions/labels verified")
        return 1 if problems else 0

    rows = load_rows(args.source_dir)
    scorebook = json.load(open(os.path.join(root, SCOREBOOK_DIR, "question-scores.json"),
                               encoding="utf-8"))
    locked_rows = dict(scorebook["general"])
    locked_rows.update(scorebook["cyber"])
    if set(locked_rows) != set(frozen):
        raise SystemExit("scorebook ids != frozen question ids")
    got_g = sum(v["total"] for k, v in locked_rows.items() if k.startswith("G"))
    got_c = sum(v["total"] for k, v in locked_rows.items() if k.startswith("C"))
    if abs(got_g - LOCKED_TOTALS["general"]) > 1e-9 or \
       abs(got_c - LOCKED_TOTALS["cyber"]) > 1e-9 or \
       abs(got_g + got_c - LOCKED_TOTALS["overall"]) > 1e-9:
        raise SystemExit("locked totals mismatch: %s / %s" % (got_g, got_c))

    by_id = {r["id"]: r for r in rows}
    if set(by_id) != set(frozen):
        raise SystemExit("source ids != frozen question ids")
    order = [f"G{i}" for i in range(1, 19)] + [f"C{i}" for i in range(1, 15)]

    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "formal-c.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for qid in order:
            src = by_id[qid]
            div, prompt = frozen[qid]
            if src["prompt"] != prompt:
                raise SystemExit("prompt drift on %s" % qid)
            ans = src.get("response") or ""
            if not ans.strip():
                ans = NO_FINAL
            for pid, pat in GENERIC_PATTERNS:
                for m in pat.finditer(ans):
                    key = (CONDITION, MODEL_NAME, qid, pid, sha256(m.group(0)))
                    if REVIEWED_FP.get(sha256(m.group(0))) != key:
                        raise SystemExit("privacy hit %s on %s (fails closed)" % (pid, qid))
            w.writerow({"condition": CONDITION, "model": MODEL_NAME, "division": div,
                        "question_id": qid, "question": prompt, "final_answer": ans})

    with open(os.path.join(out_dir, "formal-c.jsonl"), "w", encoding="utf-8") as f:
        for qid in order:
            src = by_id[qid]
            div, prompt = frozen[qid]
            ans = src.get("response") or ""
            f.write(json.dumps({
                "condition": CONDITION, "model": MODEL_NAME, "division": div,
                "question_id": qid, "question": prompt,
                "final_answer": ans if ans.strip() else NO_FINAL,
                "locked_total": locked_rows[qid]["total"],
                "completion_status": src.get("completion_status"),
            }, ensure_ascii=False) + "\n")

    # round-trip verification
    with open(os.path.join(out_dir, "formal-c.csv"), encoding="utf-8", newline="") as f:
        written = {r["question_id"]: r["final_answer"] for r in csv.DictReader(f)}
    for qid in order:
        src = by_id[qid]
        expect = (src.get("response") or "")
        if not expect.strip():
            expect = NO_FINAL
        if written[qid] != expect:
            raise SystemExit("round-trip mismatch on %s" % qid)
    print("OK: wrote 32 rows to %s" % out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
