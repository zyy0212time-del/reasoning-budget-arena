"""Build the MiMo-V2.6-Distill-Qwen-9B-Abliterated extension final-answer dataset.

Extracts the 32 frozen Formal C final answers of the post-release extension
contestant (opaque id TM91 / internal run tag I26 / release key I) from the
extension generation artifacts (two .jsonl files: 18 general + 14 cyber) and
writes
- `data/model-answers/I-mimo-v26-9b-abliterated-q4/formal-c.csv`   (repository schema)
- `data/model-answers/I-mimo-v26-9b-abliterated-q4/formal-c.jsonl` (full record incl.
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
  - aggregate totals must equal the locked 307.0 / 232.0 / 539.0

SOURCE KINDS
  --source-dir <dir>      the raw generation artifacts (two .jsonl files per run)
  --source-blind <file>   the FROZEN blind answer package, accepted only when its
                          SHA256 equals the recorded frozen digest below. This
                          path exists because the internal raw archive for the
                          general division was destroyed by an unrequested
                          second generation pass AFTER the score lock (see the
                          extension LIMITATIONS and the internal incident
                          record). The blind package is the artifact the judge
                          actually scored, and it was verified byte-identical
                          (32/32) to the raw `response` fields before the loss,
                          so it is the authoritative remaining answer source.
                          It carries prompts and final answers only.

Usage:
  python scripts/build_mimo_extension_answer_dataset.py --source-dir <dir>
  python scripts/build_mimo_extension_answer_dataset.py --source-blind <file>
  python scripts/build_mimo_extension_answer_dataset.py --verify-only
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

MODEL_NAME = "MiMo-V2.6-Distill-Qwen-9B-Abliterated-Q4_K_M"
DATASET_DIR = "I-mimo-v26-9b-abliterated-q4"
CONDITION = "formal-c"
FIELDS = ["condition", "model", "division", "question_id", "question", "final_answer"]
SRC_FILES = ["I26-general-questions.jsonl", "I26-cyber-questions.jsonl"]
SCOREBOOK_DIR = os.path.join("extensions", "mimo-v2.6-distill-qwen-9b-abliterated-q4")

# locked aggregate expectations (never recomputed from answers)
LOCKED_TOTALS = {"general": 307.0, "cyber": 232.0, "overall": 539.0}

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


# frozen digest of the blind answer package used to score this extension
BLIND_PACKAGE_SHA256 = \
    "787ae6806d69134f0a139353fce5d618f2435b25a7721da25a8b580b23a5f4af"

# fixed opaque contestant token and the blind-package block separators
OPAQUE = "TM91"
NO_FINAL = "[NO FINAL ANSWER WITHIN FIXED BUDGET]"


def load_rows_from_blind(path, repo_root):
    """Extract {id, prompt, response} from the frozen blind answer package.

    Fail-closed: the file's SHA256 must equal the recorded frozen digest, every
    block must be present, and the embedded question text must equal the frozen
    question text. Answers are taken exactly as they appear (no trimming).
    """
    with open(path, "rb") as f:
        raw_bytes = f.read()
    digest = hashlib.sha256(raw_bytes).hexdigest()
    if digest != BLIND_PACKAGE_SHA256:
        fail("blind package digest mismatch: %s" % digest)
    txt = raw_bytes.decode("utf-8")
    qs = read_questions(repo_root)
    rows = []
    ids = [q for q in qs if q.startswith("G") or q.startswith("C")]
    ids.sort(key=lambda x: (0 if x.startswith("G") else 1, int(x[1:])))
    for qid in ids:
        marker = "## %s\n\n%s\n\n### Contestant %s\n\n" % (qid, qs[qid], OPAQUE)
        i = txt.find(marker)
        if i < 0:
            fail("blind package block not found for %s" % qid)
        start = i + len(marker)
        nxt = None
        for other in ids:
            if other == qid:
                continue
            m2 = "## %s\n\n%s\n\n### Contestant %s\n\n" % (other, qs[other], OPAQUE)
            j = txt.find(m2)
            if j > start and (nxt is None or j < nxt):
                nxt = j
        capture = txt[start:] if nxt is None else txt[start:nxt]
        sep = "\n\n---\n" if nxt is None else "\n\n---\n\n"
        if not capture.endswith(sep):
            fail("unexpected block terminator for %s" % qid)
        body = capture[: -len(sep)]
        response = "" if body == NO_FINAL else body
        rows.append({"id": qid, "prompt": qs[qid], "response": response})
    return rows


def privacy_waiver(text, qid):
    """Return (ok, problem) for the generic public-release privacy scan."""
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
            continue
        return False, "privacy pattern %s at %s" % (cat, qid)
    return True, None


def privacy_scan(text, qid):
    ok, problem = privacy_waiver(text, qid)
    if not ok:
        fail("%s — row NOT released" % problem)
    if REVIEWED_FP:
        for cat, pat in GENERIC_PATTERNS:
            if pat.search(text or ""):
                print("  reviewed-FP (%s) at %s — exact row identity verified" % (cat, qid))


def verify(repo_root):
    """Re-check the published extension dataset against frozen artifacts."""
    problems = []
    ddir = os.path.join(repo_root, "data", "model-answers", DATASET_DIR)
    csvp = os.path.join(ddir, CONDITION + ".csv")
    jsonp = os.path.join(ddir, CONDITION + ".jsonl")
    if not os.path.exists(csvp):
        return ["missing %s" % csvp]
    if not os.path.exists(jsonp):
        return ["missing %s" % jsonp]
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
        ok, problem = privacy_waiver(x["final_answer"] or "", x["question_id"])
        if not ok:
            problems.append(problem)
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
    ap.add_argument("--source-blind", default=None)
    ap.add_argument("--repo-root", default=DEFAULT_REPO_ROOT)
    ap.add_argument("--verify-only", action="store_true")
    args = ap.parse_args()

    if args.verify_only:
        problems = verify(args.repo_root)
        print("verify-only: mimo extension dataset check")
        if problems:
            for p in problems:
                print("  FAIL  %s" % p)
            return 1
        print("  PASS  32 rows / schema / question+scorebook+score alignment / privacy")
        return 0

    if args.source_blind:
        if not os.path.exists(args.source_blind):
            fail("--source-blind file not found: %s" % args.source_blind)
        rows = load_rows_from_blind(args.source_blind, args.repo_root)
    elif args.source_dir and os.path.isdir(args.source_dir):
        rows = []
        for fn in SRC_FILES:
            p = os.path.join(args.source_dir, fn)
            if not os.path.exists(p):
                fail("missing source artifact: %s" % fn)
            for line in open(p, encoding="utf-8"):
                if line.strip():
                    rows.append(json.loads(line))
    else:
        fail("pass --source-dir <raw artifacts dir>, --source-blind <frozen blind "
             "package> or --verify-only")
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
