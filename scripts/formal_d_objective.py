"""Formal D objective structural audit — R2.1 (manual-audit source of truth).

Two explicit stages:

STAGE A — candidate detection / audit-template generation (ONLY on demand):
    python formal_d_objective.py --init-audit
    If data/formal-d-loop-audit.csv does NOT exist, generate a candidate
    template with every verdict set to UNREVIEWED. Refuses to overwrite an
    existing audit unless --force-init-audit is given. Templates are for HUMAN
    review; they are not verdicts.

STAGE B — objective aggregation (normal run):
    python formal_d_objective.py
    Reads the EXISTING manual audit (data/formal-d-loop-audit.csv) and uses
    its human verdicts. FAILS CLOSED if any candidate record is missing,
    duplicated, UNREVIEWED, or has an illegal verdict. The normal run NEVER
    writes to the audit file — manual verdicts are immutable for analysis.

clean_final = has_final AND not confirmed_loop AND not context_exhausted,
where confirmed_loop comes only from the manual audit.

Input layouts (both supported, detected explicitly):
  A. historical archived layout (one probe file per tag, all 29 questions)
  B. public canonical reproduction layout (one file per tag/division)
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
RC = os.path.dirname(HERE)
EXPROOT = os.path.dirname(RC)
DATA = os.path.join(RC, "data")
OUT = os.path.join(DATA, "formal-d-objective.csv")
AUDIT = os.path.join(DATA, "formal-d-loop-audit.csv")
TAGS = "ABCDEF"
CTX = 8192
HELD = {"G1", "G8", "G10"}
LEGAL_VERDICTS = {"yes", "no"}

REASONING_MARKERS = re.compile(
    r"\b(let me|let's|okay,|hmm|wait|re-?read|hold on|actually|"
    r"start over|try again|step 1|first, let|again)\b", re.I)


# ---------------- expected ID sets (derived from the frozen final set) ----------------
def frozen_ids():
    gen = [q["id"] for q in json.load(open(os.path.join(DATA, "questions-general.json"), encoding="utf-8"))]
    cyb = [q["id"] for q in json.load(open(os.path.join(DATA, "questions-cyber.json"), encoding="utf-8"))]
    return gen, cyb


def expected_sets():
    gen, cyb = frozen_ids()
    assert len(gen) == 18 and len(cyb) == 14
    probe_general = sorted(i for i in gen if i not in HELD)
    supplement_general = sorted(i for i in gen if i in HELD)
    probe_cyber = sorted(cyb)
    assert len(probe_general) == 15 and len(probe_cyber) == 14 and len(supplement_general) == 3
    assert sorted(probe_general + supplement_general) == sorted(gen)
    return {
        ("probe", "general"): probe_general,
        ("probe", "cyber"): probe_cyber,
        ("supplement", "general"): supplement_general,
    }


# ---------------- path resolution / discovery ----------------
def probe_file(base, tag, div, layout):
    if layout == "historical":
        return os.path.join(base, f"{tag}-budget-probe-8192-questions.jsonl")
    return os.path.join(base, tag, f"{tag}-{div}-questions.jsonl")


def supplement_file(base, tag, layout):
    if layout == "historical":
        return os.path.join(base, f"{tag}-general-questions.jsonl")
    return os.path.join(base, tag, f"{tag}-general-questions.jsonl")


def discover_layout(raw_root):
    hist_probe = os.path.join(raw_root, "budget-probe-8192")
    if os.path.isdir(hist_probe):
        if any(f.startswith("A-budget-probe-8192") for f in os.listdir(hist_probe)):
            return "historical"
        if all(os.path.isdir(os.path.join(hist_probe, t)) for t in TAGS):
            return "canonical"
    raise FileNotFoundError(
        f"no recognizable Formal D probe layout under {hist_probe}")


def load_jsonl(path):
    recs = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("id") == "SPEED":
                continue
            recs.append(rec)
    return recs


def verify_records(tag, stage, div, expected_ids, recs, source_label):
    errors = []
    ids = [r.get("id") for r in recs]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        errors.append(f"{tag}/{stage}/{div}: duplicate ids {sorted(dup)}")
    present = set(ids)
    missing = sorted(set(expected_ids) - present)
    unexpected = sorted(present - set(expected_ids))
    if missing:
        errors.append(f"{tag}/{stage}/{div}: missing ids {missing}")
    if unexpected:
        errors.append(f"{tag}/{stage}/{div}: unexpected ids {unexpected}")
    if errors:
        raise ValueError(f"{source_label}: " + "; ".join(errors))
    return {r["id"]: r for r in recs}


def assemble_d_baseline(raw_root):
    layout = discover_layout(raw_root)
    expected = expected_sets()
    probe_base = os.path.join(raw_root, "budget-probe-8192")
    supp_base = os.path.join(raw_root, "formal-d-supplement")
    out = {}
    for tag in TAGS:
        if layout == "historical":
            path = probe_file(probe_base, tag, "general", layout)
            if not os.path.exists(path):
                raise FileNotFoundError(f"probe file missing: {path}")
            recs = load_jsonl(path)
            expected29 = sorted(expected[("probe", "general")] + expected[("probe", "cyber")])
            verify_records(tag, "probe", "29-union", expected29, recs, path)
            for r in recs:
                out[(tag, r["id"])] = (r, "budget-probe-8192")
        else:
            for div in ("general", "cyber"):
                path = probe_file(probe_base, tag, div, layout)
                if not os.path.exists(path):
                    raise FileNotFoundError(f"probe file missing: {path}")
                recs = load_jsonl(path)
                verify_records(tag, "probe", div, expected[("probe", div)], recs, path)
                for r in recs:
                    out[(tag, r["id"])] = (r, "budget-probe-8192")
        path = supplement_file(supp_base, tag, layout)
        if not os.path.exists(path):
            raise FileNotFoundError(f"supplement file missing: {path}")
        recs = load_jsonl(path)
        verify_records(tag, "supplement", "general", expected[("supplement", "general")], recs, path)
        for r in recs:
            out[(tag, r["id"])] = (r, "formal-d-supplement")
    if len(out) != 192:
        raise ValueError(f"assembled {len(out)} records, expected 192")
    return out, layout


# ---------------- metrics ----------------
def shingles(text, n=10):
    w = re.findall(r"\S+", text.lower())
    return [" ".join(w[i:i + n]) for i in range(len(w) - n + 1)]


def dup10(text):
    sh = shingles(text)
    if len(sh) < 20:
        return 0.0
    return 1.0 - len(set(sh)) / len(sh)


def max_line_repeat(text):
    cnt = Counter()
    for ln in text.splitlines():
        ln = ln.strip()
        if len(ln) >= 40:
            cnt[ln] += 1
    return max(cnt.values()) if cnt else 0


def record_metrics(rec, div):
    content = rec.get("response") if isinstance(rec.get("response"), str) else ""
    u = rec.get("usage") or {}
    pt, ct, tt = u.get("prompt_tokens"), u.get("completion_tokens"), u.get("total_tokens")
    has_final = bool(content) and content.strip() != ""
    cx = (pt is not None and ct is not None and (pt + ct) >= CTX)
    d10 = dup10(content) if has_final else 0.0
    mlr = max_line_repeat(content) if has_final else 0
    mk = len(REASONING_MARKERS.findall(content)) if has_final else 0
    cand = bool(cx or d10 >= 0.30 or mlr >= 3)
    return dict(has_final=has_final, cx=cx, cand=cand, d10=d10, mlr=mlr,
                mk=mk, ct=ct, pt=pt, tt=tt)


# ---------------- manual audit (source of truth) ----------------
def load_manual_audit(audit_path):
    """Load the manual audit; FAIL CLOSED on any structural problem."""
    if not os.path.exists(audit_path):
        raise ValueError(f"manual audit missing: {audit_path} — run "
                         f"--init-audit to generate a template for human review")
    rows = list(csv.DictReader(open(audit_path, encoding="utf-8-sig")))
    if not rows:
        raise ValueError(f"manual audit empty: {audit_path}")
    seen = {}
    for r in rows:
        key = (r["tag"], r["division"], r["question_id"])
        if key in seen:
            raise ValueError(f"manual audit: duplicate row for {key}")
        seen[key] = r
        verdict = r["confirmed_loop"].strip().lower()
        if verdict not in LEGAL_VERDICTS:
            raise ValueError(f"manual audit: illegal/unreviewed verdict "
                             f"'{r['confirmed_loop']}' for {key} "
                             f"(legal: {sorted(LEGAL_VERDICTS)})")
    return seen


def init_audit_template(raw_root, audit_path, force=False):
    """STAGE A: generate a candidate template with UNREVIEWED verdicts.
    Refuses to overwrite an existing audit unless force=True."""
    if os.path.exists(audit_path) and not force:
        raise FileExistsError(f"audit already exists (refusing to overwrite): {audit_path}")
    baseline, layout = assemble_d_baseline(raw_root)
    cands = []
    for (tag, qid), (rec, src) in baseline.items():
        div = "general" if qid.startswith("G") else "cyber"
        m = record_metrics(rec, div)
        if m["cand"]:
            cands.append((tag, div, qid, m))
    with open(audit_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["tag", "division", "question_id", "candidate", "confirmed_loop",
                    "reason", "near_generation_cap", "has_final", "notes"])
        for tag, div, qid, m in sorted(cands):
            w.writerow([tag, div, qid, "yes", "UNREVIEWED", "",
                        "D-NOT-COMPUTABLE", "yes" if m["has_final"] else "no", ""])
    return len(cands)


def aggregate(raw_root, audit_path):
    """STAGE B: objective aggregation using the manual audit verdicts.
    Never writes the audit file. clean_final joins confirmed_loop from audit."""
    baseline, layout = assemble_d_baseline(raw_root)
    manual = load_manual_audit(audit_path)
    rows = []
    for (tag, qid), (rec, src) in baseline.items():
        div = "general" if qid.startswith("G") else "cyber"
        m = record_metrics(rec, div)
        confirmed = False
        if m["cand"]:
            verdict = manual.get((tag, div, qid))
            if verdict is None:
                raise ValueError(f"candidate {tag}/{div}/{qid} has no manual "
                                 f"audit verdict (fail closed)")
            confirmed = verdict["confirmed_loop"].strip().lower() == "yes"
        rows.append({
            "original_tag": tag, "division": div, "question_id": qid,
            "has_final": "yes" if m["has_final"] else "no",
            "prompt_tokens": m["pt"], "completion_tokens": m["ct"],
            "total_tokens": m["tt"],
            "near_context_limit": "yes" if m["cx"] else "no",
            "near_generation_cap": "D-NOT-COMPUTABLE",
            "loop_candidate": "yes" if m["cand"] else "no",
            "clean_final": "yes" if (m["has_final"] and not confirmed and not m["cx"]) else "no",
            "source": src,
        })
    return rows, layout


def write_objective(rows):
    with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def summarize(rows):
    n = len(rows)
    hf = sum(1 for r in rows if r["has_final"] == "yes")
    cx = sum(1 for r in rows if r["near_context_limit"] == "yes")
    clean = sum(1 for r in rows if r["clean_final"] == "yes")
    return n, hf, cx, clean


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--init-audit", action="store_true",
                    help="STAGE A: generate audit template (UNREVIEWED verdicts) if missing")
    ap.add_argument("--force-init-audit", action="store_true",
                    help="allow overwriting an existing audit template")
    args = ap.parse_args()

    raw_root = os.path.join(EXPROOT, "raw")
    if args.init_audit:
        n = init_audit_template(raw_root, AUDIT, force=args.force_init_audit)
        print(f"init-audit: wrote candidate template ({n} candidates, verdicts UNREVIEWED) "
              f"to {AUDIT}")
        return
    rows, layout = aggregate(raw_root, AUDIT)
    write_objective(rows)
    n, hf, cx, clean = summarize(rows)
    print(f"layout: {layout}; wrote {OUT} ({n} rows)")
    print(f"has_final={hf} context_exhausted={cx} confirmed_loops=0 (manual audit) "
          f"clean_final={clean}")


if __name__ == "__main__":
    main()
