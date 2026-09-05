"""Build the 0xKitkat Ornith Uncensored extension final-answer dataset.

Extracts the 32 frozen Formal C final answers of the post-release extension
contestant (opaque id ZD74 / release key H) from the extension generation
artifacts (two .jsonl files: 18 general + 14 cyber) and writes
- `data/model-answers/H-ornith-0xkitkat/formal-c.csv`   (repository schema)
- `data/model-answers/H-ornith-0xkitkat/formal-c.jsonl` (full record incl.
  locked per-question score total)

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
  - no locked score is ever recomputed; per-question score totals are read
    from the locked extension scorebook artifact (question-scores.json)

TRACEABILITY
  - question ids must equal the frozen question files' ids
  - prompt text must equal the frozen question text
  - question ids must equal the locked extension scorebook rows
  - aggregate totals must equal the locked 397.5 / 274.5 / 672.0

The generation artifacts live outside this repository (internal run archive);
pass their directory with --source-dir. No machine-specific path is embedded.

Usage:
  python scripts/build_ornith_extension_answer_dataset.py --source-dir <dir>
  python scripts/build_ornith_extension_answer_dataset.py --verify-only
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

MODEL_NAME = "Ornith-1.5-35B-A3B-Uncensored-Q4_K_M"
DATASET_DIR = "H-ornith-0xkitkat"
CONDITION = "formal-c"
FIELDS = ["condition", "model", "division", "question_id", "question", "final_answer"]
SRC_FILES = ["ZD74-general-questions.jsonl", "ZD74-cyber-questions.jsonl"]
SCOREBOOK_DIR = os.path.join("extensions", "ornith-0xkitkat-uncensored-q4")

# locked aggregate expectations (never recomputed from answers)
LOCKED_TOTALS = {"general": 397.5, "cyber": 274.5, "overall": 672.0}

# reviewed false positives, bound to exact row identity (see module docstring).
# Empty unless a benchmark answer triggers a generic pattern legitimately.
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


def read_locked_scores(repo_root):
    p = os.path.join(repo_root, SCOREBOOK_DIR, "question-scores.json")
    d = json.load(open(p, encoding="utf-8"))
    out = {}
    for div in ("general", "cyber"):
        for qid, rec in d[div].items():
            out[qid] = rec["total"]
    t = d["totals"]
    if (abs(t["general"] - LOCKED_TOTALS["general"]) > 1e-9
            or abs(t["cyber"] - LOCKED_TOTALS["cyber"]) > 1e-9
            or abs(t["overall"] - LOCKED_TOTALS["overall"]) > 1e-9):
        fail("locked totals drift in question-scores.json: %r" % t)
    return out


def read_scorebook_ids(repo_root):
    p = os.path.join(repo_root, SCOREBOOK_DIR,
                     "FORMAL-C-EXTENSION-BLIND-SCORES-LOCKED.md")
    txt = open(p, encoding="utf-8").read()
    seen = []
    for m in re.findall(r"^\|\s*(G\d+|C\d+)\s*\|", txt, re.M):
        if m not in seen:
            seen.append(m)
    return seen


def privacy_scan(text, qid):
    for cat, pat in GENERIC_PATTERNS:
        m = pat.search(text or "")
        if not m:
            continue
        anchor = hashlib.sha256(m.group(0).encode("utf-8")).hexdigest()
        answer_sha = hashlib.sha256((text or "").encode("utf-8")).hexdigest()
        b = REVIEWED_FP.get(anchor)
        if b and all((b["pattern"] == cat, b["condition"] == CONDITION,
                      b["model"] == MODEL_NAME, b["question_id"] == qid,
                      b["answer_sha256"] == answer_sha)):
            print("  reviewed-FP (%s) at %s — exact row identity verified" % (cat, qid))
            continue
        fail("privacy pattern %s at %s — row NOT released" % (cat, qid))


def verify(repo_root):
    """Re-check the published extension dataset against frozen artifacts."""
    problems = []
    ddir = os.path.join(repo_root, "data", "model-answers", DATASET_DIR)
    csvp = os.path.join(ddir, CONDITION + ".csv")
    jsonp = os.path.join(ddir, CONDITION + ".jsonl")
    if not os.path.exists(csvp):
        problems.append("missing %s" % csvp)
        return problems
    if not os.path.exists(jsonp):
        problems.append("missing %s" % jsonp)
        return problems
    with open(csvp, encoding="utf-8-sig", newline="") as f:
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
    scores = read_locked_scores(repo_root)
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
    # jsonl cross-check
    jrows = [json.loads(l) for l in open(jsonp, encoding="utf-8") if l.strip()]
    if len(jrows) != 32:
        problems.append("jsonl has %d records (expected 32)" % len(jrows))
    csv_by_id = {x["question_id"]: x for x in rows}
    for j in jrows:
        qid = j["question_id"]
        c = csv_by_id.get(qid)
        if c is None:
            problems.append("jsonl id %s missing from csv" % qid)
            continue
        if j["final_answer"] != c["final_answer"]:
            problems.append("csv/jsonl answer drift at %s" % qid)
        if j["question"] != qs[qid]:
            problems.append("jsonl question drift at %s" % qid)
        if "reasoning" in j or "reasoning_content" in j:
            problems.append("reasoning field present at %s" % qid)
        if abs(j.get("score_total", -1) - scores[qid]) > 1e-9:
            problems.append("score_total mismatch at %s" % qid)
        for k in ("general", "cyber"):
            pass
    if set(j["question_id"] for j in jrows) != sb:
        problems.append("jsonl id set != locked scorebook id set")
    g = sum(scores[q] for q in scores if q.startswith("G"))
    cy = sum(scores[q] for q in scores if q.startswith("C"))
    if abs(g - LOCKED_TOTALS["general"]) > 1e-9 or abs(cy - LOCKED_TOTALS["cyber"]) > 1e-9:
        problems.append("locked aggregate drift %r" % ((g, cy),))
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default=None)
    ap.add_argument("--repo-root", default=DEFAULT_REPO_ROOT)
    ap.add_argument("--verify-only", action="store_true")
    args = ap.parse_args()

    if args.verify_only:
        problems = verify(args.repo_root)
        print("verify-only: ornith extension dataset check")
        if problems:
            for p in problems:
                print("  FAIL  %s" % p)
            return 1
        print("  PASS  32 rows / schema / question+scorebook+score alignment / privacy")
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
    scores = read_locked_scores(args.repo_root)
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
        privacy_scan(text, qid)
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

    destj = os.path.join(dest_dir, CONDITION + ".jsonl")
    with open(destj, "w", encoding="utf-8", newline="\n") as f:
        for o in out:
            f.write(json.dumps({
                "question_id": o["question_id"],
                "division": o["division"],
                "question": o["question"],
                "final_answer": o["final_answer"],
                "score_total": scores[o["question_id"]],
            }, ensure_ascii=False) + "\n")

    # byte-faithful round-trip
    with open(dest, encoding="utf-8-sig", newline="") as f:
        back = list(csv.DictReader(f))
    if len(back) != 32:
        fail("round-trip row count mismatch")
    src_by_id = {r["id"]: r["response"] for r in rows}
    for b in back:
        if b["final_answer"] != src_by_id[b["question_id"]]:
            fail("round-trip answer text differs at %s" % b["question_id"])

    print("BUILD OK: wrote 32 answers -> %s{.csv,.jsonl}" % DATASET_DIR)
    problems = verify(args.repo_root)
    if problems:
        for p in problems:
            print("  FAIL  %s" % p)
        return 1
    print("  PASS  post-build verify: 32 rows / schema / question+scorebook+score "
          "alignment / privacy")
    return 0


if __name__ == "__main__":
    sys.exit(main())
