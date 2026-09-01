"""Manual-audit preservation tests for Formal D objective aggregation.

Exercises the REAL production functions in formal_d_objective.py
(candidate detection via --init-audit template, manual-audit loading, and
aggregation) against synthetic JSONL. No models, no network, no server.

Tests:
  A. existing audit verdict `yes` is preserved and clean_final is subtracted
  B. existing audit verdict `no` is preserved
  C. UNREVIEWED verdict FAILS CLOSED
  D. missing audit row for a candidate FAILS CLOSED
  E. duplicate audit row FAILS CLOSED
  F. a normal aggregation run does NOT mutate the manual audit file

Run:  python test_formal_d_manual_audit.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import formal_d_objective as fdo  # noqa: E402

FAILURES = []


def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + (f"  [{detail}]" if detail else ""))
    if not cond:
        FAILURES.append(name)


def build_raw(td, hot=None):
    """Synthetic canonical Formal D archive. `hot` = (tag, qid, kind) where
    kind='cx' makes a context-exhausted candidate (has_final, not clean);
    kind='rep' makes a repetition candidate (has_final, NOT context-exhausted),
    so a manual `yes` verdict is what makes it not-clean."""
    exp = fdo.expected_sets()
    REP_LINE = "The buffer is 1 hour per city, and the travel time is 2 hours per leg. "
    for tag in "ABCDEF":
        def emit(base, stage, div, ids):
            fn = fdo.probe_file(base, tag, div, "canonical") if stage == "probe" \
                else fdo.supplement_file(base, tag, "canonical")
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            for qid in ids:
                kind = hot[2] if (hot and tag == hot[0] and qid == hot[1]) else None
                if kind == "cx":
                    u = {"prompt_tokens": 100, "completion_tokens": 8192, "total_tokens": 8292}
                    resp = "A detailed final answer that is truncated."
                elif kind == "rep":
                    u = {"prompt_tokens": 100, "completion_tokens": 500, "total_tokens": 600}
                    resp = "\n".join([REP_LINE.strip()] * 6)
                else:
                    u = {"prompt_tokens": 100, "completion_tokens": 500, "total_tokens": 600}
                    resp = "answer"
                rec = {"id": qid, "tag": tag, "prompt": f"p {qid}",
                       "response": resp, "reasoning": "", "usage": u}
                with open(fn, "a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        emit(os.path.join(td, "budget-probe-8192"), "probe", "general", exp[("probe", "general")])
        emit(os.path.join(td, "budget-probe-8192"), "probe", "cyber", exp[("probe", "cyber")])
        emit(os.path.join(td, "formal-d-supplement"), "supplement", "general",
             exp[("supplement", "general")])


def candidate_keys(raw_root):
    """Recompute the candidate set using the production detector."""
    baseline, _ = fdo.assemble_d_baseline(raw_root)
    keys = []
    for (tag, qid), (rec, _src) in baseline.items():
        div = "general" if qid.startswith("G") else "cyber"
        m = fdo.record_metrics(rec, div)
        if m["cand"]:
            keys.append((tag, div, qid))
    return keys


def write_audit(path, verdicts):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["tag", "division", "question_id", "candidate", "confirmed_loop",
                    "reason", "near_generation_cap", "has_final", "notes"])
        for (tag, div, qid), v in verdicts.items():
            w.writerow([tag, div, qid, "yes", v, "note", "D-NOT-COMPUTABLE", "yes", ""])


print("== TEST A: manual verdict `yes` is preserved and clean_final is subtracted ==")
with tempfile.TemporaryDirectory() as td:
    raw = os.path.join(td, "raw")
    build_raw(raw, hot=("A", "G2", "rep"))
    cands = candidate_keys(raw)
    check("one repetition candidate produced by detector", cands == [("A", "general", "G2")], str(cands))
    audit = os.path.join(td, "audit.csv")
    write_audit(audit, {("A", "general", "G2"): "yes"})
    rows, _ = fdo.aggregate(raw, audit)
    a2 = next(r for r in rows if r["original_tag"] == "A" and r["question_id"] == "G2")
    check("verdict yes preserved (clean_final=no)", a2["clean_final"] == "no")
    check("aggregation ran", len(rows) == 192)

print("== TEST B: manual verdict `no` is preserved (clean_final stays yes) ==")
with tempfile.TemporaryDirectory() as td:
    raw = os.path.join(td, "raw")
    build_raw(raw, hot=("A", "G2", "rep"))
    audit = os.path.join(td, "audit.csv")
    write_audit(audit, {("A", "general", "G2"): "no"})
    rows, _ = fdo.aggregate(raw, audit)
    a2 = next(r for r in rows if r["original_tag"] == "A" and r["question_id"] == "G2")
    check("verdict no preserved (clean_final=yes, no cx)", a2["clean_final"] == "yes")

print("== TEST C: UNREVIEWED verdict FAILS CLOSED ==")
with tempfile.TemporaryDirectory() as td:
    raw = os.path.join(td, "raw")
    build_raw(raw, hot=("A", "G2", "rep"))
    audit = os.path.join(td, "audit.csv")
    write_audit(audit, {("A", "general", "G2"): "UNREVIEWED"})
    try:
        fdo.aggregate(raw, audit)
        check("fails closed on UNREVIEWED", False)
    except ValueError as e:
        check("fails closed on UNREVIEWED", "UNREVIEWED" in str(e))

print("== TEST D: missing audit row FAILS CLOSED ==")
with tempfile.TemporaryDirectory() as td:
    raw = os.path.join(td, "raw")
    build_raw(raw, hot=("A", "G2", "rep"))
    audit = os.path.join(td, "audit.csv")
    # audit contains a row, but NOT the candidate A/G2's row
    write_audit(audit, {("B", "general", "G3"): "no"})
    try:
        fdo.aggregate(raw, audit)
        check("fails closed on missing row", False)
    except ValueError as e:
        check("fails closed on missing row", "no manual audit verdict" in str(e))

print("== TEST E: duplicate audit row FAILS CLOSED ==")
with tempfile.TemporaryDirectory() as td:
    raw = os.path.join(td, "raw")
    build_raw(raw, hot=("A", "G2", "rep"))
    audit = os.path.join(td, "audit.csv")
    write_audit(audit, {("A", "general", "G2"): "yes"})
    with open(audit, "a", encoding="utf-8") as f:
        f.write("A,general,G2,yes,no,note,D-NOT-COMPUTABLE,yes,\n")
    try:
        fdo.aggregate(raw, audit)
        check("fails closed on duplicate row", False)
    except ValueError as e:
        check("fails closed on duplicate row", "duplicate" in str(e))

print("== TEST F: normal aggregation does NOT mutate the manual audit ==")
with tempfile.TemporaryDirectory() as td:
    raw = os.path.join(td, "raw")
    build_raw(raw, hot=("A", "G2", "rep"))
    audit = os.path.join(td, "audit.csv")
    write_audit(audit, {("A", "general", "G2"): "no"})
    before = hashlib.sha256(open(audit, "rb").read()).hexdigest()
    fdo.aggregate(raw, audit)
    fdo.aggregate(raw, audit)
    after = hashlib.sha256(open(audit, "rb").read()).hexdigest()
    check("audit file bytes unchanged after two aggregations", before == after)

print("\n" + ("ALL MANUAL-AUDIT TESTS PASSED" if not FAILURES else f"{len(FAILURES)} FAILURES"))
sys.exit(1 if FAILURES else 0)
