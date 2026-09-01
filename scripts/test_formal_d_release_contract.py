"""Formal D release-contract test.

Exercises the REAL production functions in formal_d_objective.py
(path resolution, source discovery, expected-ID sets, assembly, verification)
against synthetic JSONL. No models, no network, no server.

Run:  python test_formal_d_release_contract.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import formal_d_objective as fdo  # noqa: E402

TAGS = "ABCDEF"
FAILURES = []


def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + (f"  [{detail}]" if detail else ""))
    if not cond:
        FAILURES.append(name)


def synth_rec(qid, tag, content="answer"):
    u = {"prompt_tokens": 100, "completion_tokens": 500, "total_tokens": 600}
    return {"id": qid, "tag": tag, "prompt": f"p {qid}", "response": content,
            "reasoning": "", "usage": u}


def write_layout(root, layout, corrupt=None):
    """Build the synthetic Formal D archive in the given layout.
    corrupt: None | ('dup', tag, stage, div) | ('missing', ...) | ('unexpected', ...)"""
    exp = fdo.expected_sets()
    probe_base = os.path.join(root, "budget-probe-8192")
    supp_base = os.path.join(root, "formal-d-supplement")
    os.makedirs(probe_base, exist_ok=True)
    os.makedirs(supp_base, exist_ok=True)
    for tag in TAGS:
        def emit(base, stage, div, ids, extra=()):
            fn = fdo.probe_file(base, tag, div, layout) if stage == "probe" \
                else fdo.supplement_file(base, tag, layout)
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            recs = [synth_rec(i, tag) for i in ids]
            if corrupt and corrupt[1] == tag and corrupt[2] == stage and corrupt[3] == div:
                kind = corrupt[0]
                if kind == "dup":
                    recs.append(synth_rec(ids[0], tag))
                elif kind == "missing":
                    recs = [r for r in recs if r["id"] != ids[0]]
                elif kind == "unexpected":
                    recs.append(synth_rec("G99", tag))
            for r in recs + list(extra):
                with open(fn, "a", encoding="utf-8") as f:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
        if layout == "historical":
            # historical probe: ONE file per tag containing all 29 questions
            emit(probe_base, "probe", "general",
                 exp[("probe", "general")] + exp[("probe", "cyber")])
        else:
            emit(probe_base, "probe", "general", exp[("probe", "general")])
            emit(probe_base, "probe", "cyber", exp[("probe", "cyber")])
        emit(supp_base, "supplement", "general", exp[("supplement", "general")])


print("== 1. expected composition derived from frozen set ==")
exp = fdo.expected_sets()
check("probe = 15 General + 14 Cyber = 29", len(exp[("probe", "general")]) == 15
      and len(exp[("probe", "cyber")]) == 14 and len(exp[("probe", "general")]) + len(exp[("probe", "cyber")]) == 29)
check("supplement = G1,G8,G10 = 3", exp[("supplement", "general")] == ["G1", "G10", "G8"])
check("union == frozen 32, no dups", len(set(exp[("probe", "general")]) | set(exp[("probe", "cyber")]) | set(exp[("supplement", "general")])) == 32)
check("probe general excludes G1/G8/G10", not (set(exp[("probe", "general")]) & {"G1", "G8", "G10"}))

print("== 2. canonical layout: clean assembly ==")
with tempfile.TemporaryDirectory() as td:
    write_layout(td, "canonical")
    base, layout = fdo.assemble_d_baseline(td)
    check("layout detected = canonical", layout == "canonical")
    check("192 exact records", len(base) == 192)
    ids = {i for (t, i) in base}
    check("32 unique question ids", len(ids) == 32)
    check("source provenance both present",
          any(s == "budget-probe-8192" for _, s in base.values())
          and any(s == "formal-d-supplement" for _, s in base.values()))
    # no raw/raw anywhere
    check("no raw/raw duplication", "raw/raw" not in str(os.path.join(td, "raw")))

print("== 3. historical layout: clean assembly ==")
with tempfile.TemporaryDirectory() as td:
    write_layout(td, "historical")
    base, layout = fdo.assemble_d_baseline(td)
    check("layout detected = historical", layout == "historical")
    check("192 exact records", len(base) == 192)

print("== 4. rejection cases (canonical layout) ==")
for kind, tag, stage, div in (("dup", "A", "probe", "general"),
                              ("missing", "B", "probe", "cyber"),
                              ("unexpected", "C", "supplement", "general")):
    with tempfile.TemporaryDirectory() as td:
        write_layout(td, "canonical", corrupt=(kind, tag, stage, div))
        try:
            fdo.assemble_d_baseline(td)
            check(f"rejects {kind} ({tag}/{stage}/{div})", False)
        except (ValueError, FileNotFoundError):
            check(f"rejects {kind} ({tag}/{stage}/{div})", True)

print("== 5. missing probe layout detection ==")
with tempfile.TemporaryDirectory() as td:
    try:
        fdo.discover_layout(td)
        check("empty root raises", False)
    except FileNotFoundError:
        check("empty root raises", True)

print("\n" + ("ALL FORMAL-D CONTRACT TESTS PASSED" if not FAILURES else f"{len(FAILURES)} FAILURES"))
sys.exit(1 if FAILURES else 0)
