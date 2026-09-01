"""Score validation + master-table generation for Formal D vs Formal C.

Input (already published in data/):

    data/formal-d-scores.csv
    data/formal-c-scores.csv

Format (one row per (model, division, question)):

    condition,model,division,question_id,
    correctness,completeness,visible_reasoning_result_quality,
    instruction_following,practical_usefulness,question_total

Validation performed:
  1. each condition has 6 models x 32 questions = 192 rows, no duplicates
  2. every dimension within 0-5
  3. question_total == sum of the five dimensions
  4. per model: General subtotal + Cyber subtotal == Overall
  5. division maximums respected (General 450, Cyber 350, Overall 800)
  6. if both conditions validate: emit data/d-vs-c.csv with deltas and ranks
     (rank change = D rank - C rank; positive = moved up)

Run:  python validate_scores.py
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RC = os.path.dirname(HERE)
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
CONDITIONS = {"formal-d": "formal-d-scores.csv", "formal-c": "formal-c-scores.csv"}
DIMS = ["correctness", "completeness", "visible_reasoning_result_quality",
        "instruction_following", "practical_usefulness"]
MAX = {"general": 450.0, "cyber": 350.0}
N_QUESTIONS, N_MODELS = 32, 6


def validate(condition, fname):
    path = os.path.join(DATA, fname)
    if not os.path.exists(path):
        print(f"[MISSING] {fname} — place the verified score CSV in data/ first.")
        return None
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
    problems = []
    if len(rows) != N_MODELS * N_QUESTIONS:
        problems.append(f"row count {len(rows)} != {N_MODELS * N_QUESTIONS}")
    seen = set()
    totals = {}
    for r in rows:
        key = (r["model"], r["division"], r["question_id"])
        if key in seen:
            problems.append(f"duplicate row {key}")
        seen.add(key)
        dims = []
        for d in DIMS:
            try:
                v = float(r[d])
            except (KeyError, ValueError):
                problems.append(f"missing/non-numeric dimension {d} in {key}")
                dims = None
                break
            if not (0.0 <= v <= 5.0):
                problems.append(f"dimension {d} out of range in {key}: {v}")
            dims.append(v)
        if dims is None:
            continue
        try:
            tot = float(r["question_total"])
        except (KeyError, ValueError):
            problems.append(f"missing question_total in {key}")
            continue
        if abs(sum(dims) - tot) > 1e-9:
            problems.append(f"{key}: question_total {tot} != sum(dims) {round(sum(dims), 4)}")
        m, div = r["model"], r["division"]
        totals.setdefault(m, {"general": 0.0, "cyber": 0.0})[div] += tot
    if len(totals) != N_MODELS:
        problems.append(f"model count {len(totals)} != {N_MODELS}")
    for m, sub in totals.items():
        if sub["general"] > MAX["general"] + 1e-9:
            problems.append(f"{m}: General {sub['general']} > 450")
        if sub["cyber"] > MAX["cyber"] + 1e-9:
            problems.append(f"{m}: Cyber {sub['cyber']} > 350")
        if abs((sub["general"] + sub["cyber"]) - round(sub["general"] + sub["cyber"], 1)) > 1e-9:
            problems.append(f"{m}: subtotal rounding")
    if problems:
        print(f"[FAIL] {condition}:")
        for p in problems:
            print("   -", p)
        return None
    print(f"[OK] {condition}: {len(rows)} rows, {len(totals)} models, "
          f"dimensions in range, totals consistent, maximums respected")
    return totals


def validate_question_set(condition):
    """Exact frozen-id coverage: 18 G-ids + 14 C-ids, per model, 6 models."""
    gen = {x["id"] for x in json.load(open(os.path.join(DATA, "questions-general.json"), encoding="utf-8"))}
    cyb = {x["id"] for x in json.load(open(os.path.join(DATA, "questions-cyber.json"), encoding="utf-8"))}
    rows = list(csv.DictReader(open(os.path.join(DATA, CONDITIONS[condition]), encoding="utf-8-sig")))
    problems = []
    models = sorted({r["model"] for r in rows})
    if len(models) != 6:
        problems.append(f"{condition}: {len(models)} models != 6")
    per_model = {}
    for m in models:
        mr = [r for r in rows if r["model"] == m]
        g = {r["question_id"] for r in mr if r["division"] == "general"}
        c = {r["question_id"] for r in mr if r["division"] == "cyber"}
        per_model[m] = (g, c)
        if g != gen:
            problems.append(f"{condition}/{m}: General ids differ {gen ^ g}")
        if c != cyb:
            problems.append(f"{condition}/{m}: Cyber ids differ {cyb ^ c}")
    if problems:
        print(f"[FAIL] {condition} question set:")
        for p in problems:
            print("   -", p)
        return False
    print(f"[OK] {condition}: 6 models, each exactly 18 General + 14 Cyber, frozen ids exact")
    return True


def validate_mapping():
    """Internal one-to-one check of the METHODOLOGY post-lock reveal table."""
    m = open(os.path.join(RC, "METHODOLOGY.md"), encoding="utf-8").read()
    # the reveal table header is unique to the post-lock identity section
    anchor = "| condition | contestant → experiment tag / model |"
    if anchor not in m:
        print("[FAIL] mapping: reveal table header not found in METHODOLOGY.md")
        return False
    segs = m.split(anchor)[-1]
    fd, fc = segs.split("Formal C |")[0], segs.split("Formal C |")[1]
    d_ids = re.findall(r"([A-Z]\d{2}) = ([A-F])\b", fd)
    c_ids = re.findall(r"([A-Z]\d{2}) = ([A-F])\b", fc)
    ok = True
    for name, pairs in (("formal-d", d_ids), ("formal-c", c_ids)):
        ids = [p[0] for p in pairs]
        tags = [p[1] for p in pairs]
        if len(set(ids)) != 6 or len(set(tags)) != 6 or len(pairs) != 6:
            print(f"[FAIL] mapping {name}: not a 1:1 six-token mapping ({len(pairs)})")
            ok = False
        else:
            print(f"[OK] mapping {name}: 6 opaque ids -> 6 tags, one-to-one")
    return ok


# canonical tag -> model display name (matches the score CSVs and MODEL-CARDS.md)
TAG_MODELS = {
    "A": "RavenX-CyberAgent-35B-v5.1-Q4_K_M",
    "B": "Endy-Qwen3.6-CyberSec-35B-A3B-Q4_K_M",
    "C": "Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-Q4_K_M",
    "D": "Ornith-1.5-35B-A3B-Abliterated-Q4_K_M",
    "E": "Nex-N2-mini-Q4_K_M",
    "F": "Qwen3.8-9B-abliterated-25-Q4_K_M",
}


def _opaque_to_model(condition):
    """Opaque-id -> model from the METHODOLOGY post-lock reveal (opaque=tag) +
    the canonical tag->model mapping above (no fragile markdown parsing)."""
    meth = open(os.path.join(RC, "METHODOLOGY.md"), encoding="utf-8").read()
    anchor = "| condition | contestant → experiment tag / model |"
    if anchor not in meth:
        return {}
    seg = meth.split(anchor)[-1]
    fd, fc = seg.split("Formal C |")[0], seg.split("Formal C |")[1]
    pairs = re.findall(r"([A-Z]\d{2}) = ([A-F])\b", fd if condition == "formal-d" else fc)
    return {oid: TAG_MODELS[tag] for oid, tag in pairs if tag in TAG_MODELS}


def validate_scorebook(condition):
    """Cross-check the locked scorebook against the score CSV (exact question totals)."""
    sb = os.path.join(RC, "blind", "FORMAL-" + ("D" if condition == "formal-d" else "C") +
                      "-BLIND-SCORES-LOCKED.md")
    if not os.path.exists(sb):
        print(f"[SKIP] scorebook cross-check: {os.path.basename(sb)} not present")
        return True
    txt = open(sb, encoding="utf-8").read()
    o2m = _opaque_to_model(condition)
    if len(o2m) != 6:
        print(f"[FAIL] {condition}: could not build 6-item opaque->model map ({len(o2m)})")
        return False
    sb_map = {}
    if condition == "formal-d":
        pat = re.compile(r"^\|\s*([GC]\d+)\s*\|\s*([A-Z]\d{2})\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|"
                         r"\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*[\\*]{0,4}([\d.]+)[\\*]{0,4}\s*\|")
        for line in txt.splitlines():
            m = pat.match(line.strip())
            if m:
                sb_map[(m.group(1), m.group(2))] = float(m.group(8))
    else:
        pat_c = re.compile(r"^\|\s*([A-Z]\d{2})\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|"
                           r"\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*[\\*]{0,4}([\d.]+)[\\*]{0,4}\s*\|")
        qid = None
        for line in txt.splitlines():
            h = re.match(r"^\\*#+\s*([GC]\d+)\s*$", line.strip())
            if h:
                qid = h.group(1)
                continue
            m = pat_c.match(line.strip())
            if m and qid:
                sb_map[(qid, m.group(1))] = float(m.group(7))
    if len(sb_map) != 192:
        print(f"[FAIL] {condition}: parsed {len(sb_map)} scorebook rows, expected 192")
        return False
    rows = list(csv.DictReader(open(os.path.join(DATA, CONDITIONS[condition]), encoding="utf-8-sig")))
    mism = 0
    for r in rows:
        model = r["model"]
        oid = next((o for o, m in o2m.items() if m == model), None)
        if oid is None:
            mism += 1
            print(f"   [WARN] no opaque id mapped for {model}")
            continue
        sb_tot = sb_map.get((r["question_id"], oid))
        if sb_tot is None:
            mism += 1
            if mism < 4:
                print(f"   [WARN] no scorebook row for {r['question_id']}/{oid}")
            continue
        if abs(sb_tot - float(r["question_total"])) > 1e-9:
            mism += 1
            print(f"   [MISMATCH] {r['question_id']}/{oid}: csv {r['question_total']} vs scorebook {sb_tot}")
    if mism:
        print(f"[FAIL] {condition} scorebook<->CSV exact mapping: {mism} mismatches")
        return False
    print(f"[OK] {condition} scorebook <-> CSV: {len(rows)} question totals matched exactly")
    return True


def main():
    import json
    out = {}
    ok_q = True
    for cond, fname in CONDITIONS.items():
        out[cond] = validate(cond, fname)
        ok_q = validate_question_set(cond) and ok_q
    ok_m = validate_mapping()
    ok_sb = all(validate_scorebook(c) for c in CONDITIONS)
    if any(v is None for v in out.values()) or not (ok_q and ok_m and ok_sb):
        print("\nMASTER TABLE: NOT GENERATED (validation failed above)")
        return 1

    if set(out["formal-d"]) != set(out["formal-c"]):
        print("[FAIL] model sets differ between conditions:",
              set(out["formal-d"]) ^ set(out["formal-c"]))
        return 1

    def ranks(totals, div=None):
        key = (lambda m: -(totals[m]["general"] + totals[m]["cyber"])) if div is None \
            else (lambda m: -totals[m][div])
        order = sorted(totals, key=lambda m: (key(m), m))
        return {m: i + 1 for i, m in enumerate(order)}

    d_rank, c_rank = ranks(out["formal-d"]), ranks(out["formal-c"])
    dg = ranks(out["formal-d"], "general")   # Formal D general ranks
    cg = ranks(out["formal-c"], "general")   # Formal C general ranks
    dcy = ranks(out["formal-d"], "cyber")
    ccy = ranks(out["formal-c"], "cyber")

    with open(os.path.join(DATA, "d-vs-c.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["model", "d_general", "c_general", "delta_general",
                    "d_cyber", "c_cyber", "delta_cyber",
                    "d_overall", "c_overall", "delta_overall",
                    "d_rank", "c_rank", "rank_change"])
        for m in sorted(out["formal-d"], key=lambda m: -(
                out["formal-c"][m]["general"] + out["formal-c"][m]["cyber"])):
            g_d = round(out["formal-d"][m]["general"], 1)
            g_c = round(out["formal-c"][m]["general"], 1)
            y_d = round(out["formal-d"][m]["cyber"], 1)
            y_c = round(out["formal-c"][m]["cyber"], 1)
            o_d, o_c = round(g_d + y_d, 1), round(g_c + y_c, 1)
            w.writerow([m, g_d, g_c, round(g_c - g_d, 1), y_d, y_c, round(y_c - y_d, 1),
                        o_d, o_c, round(o_c - o_d, 1), d_rank[m], c_rank[m],
                        d_rank[m] - c_rank[m]])
    print("\nwrote data/d-vs-c.csv")
    print("General ranks  D:", {m: dg[m] for m in dg})
    print("General ranks  C:", {m: cg[m] for m in cg})
    print("Cyber ranks    D:", {m: dcy[m] for m in dcy})
    print("Cyber ranks    C:", {m: ccy[m] for m in ccy})
    print("Overall ranks  D:", d_rank)
    print("Overall ranks  C:", c_rank)
    return 0


if __name__ == "__main__":
    sys.exit(main())
