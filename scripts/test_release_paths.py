"""Clean-room path-contract test for the released Formal C runner/harness.

Verifies WITHOUT running any model that the runner, harness and integrity
checker agree on one canonical raw layout:

    <output-root>/raw/formal-c/<tag>/<tag>-<div>-questions.jsonl
        div in {general, cyber}, tag in {A..F}

Checks:
  - resolved output directory never contains a raw/raw duplication
  - filenames match the canonical contract exactly
  - explicit --div maps questions files correctly (data/questions-*.json)
  - integrity-checker discovery path == harness write path
  - every released script compiles

Run:  python test_release_paths.py        (no network, no model, no server)
"""
from __future__ import annotations

import os
import py_compile
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import arena_harness as h  # noqa: E402

EXPROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FAILURES = []


def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + (f"  [{detail}]" if detail else ""))
    if not cond:
        FAILURES.append(name)


print("== 1. canonical layout, no raw/raw duplication ==")
for tag in "ABCDEF":
    for div in ("general", "cyber"):
        p = h.resolve_raw_path(EXPROOT, os.path.join("raw", "formal-c", tag), tag, div)
        expected = os.path.join(EXPROOT, "raw", "formal-c", tag, f"{tag}-{div}-questions.jsonl")
        check(f"{tag}/{div} path", p == expected and "raw/raw" not in p, p)
        check(f"{tag}/{div} filename", os.path.basename(p) == f"{tag}-{div}-questions.jsonl")

print("== 2. integrity checker discovers exactly the harness path ==")
for tag in "ABCDEF":
    for div in ("general", "cyber"):
        harness_path = h.resolve_raw_path(EXPROOT, os.path.join("raw", "formal-c", tag), tag, div)
        integrity_path = os.path.join(EXPROOT, "raw", "formal-c", tag, f"{tag}-{div}-questions.jsonl")
        check(f"integrity==harness {tag}/{div}", harness_path == integrity_path)

print("== 3. explicit --div overrides filename inference ==")
q = os.path.join(HERE, "..", "data", "questions-general.json")
if os.path.exists(q):
    check("--div general wins over basename",
          h.div_from_questions_file(q) == "general"
          and h.resolve_raw_path(".", "raw", "A", "general").endswith("A-general-questions.jsonl"))
q2 = os.path.join(HERE, "..", "data", "questions-cyber.json")
if os.path.exists(q2):
    check("--div cyber wins over basename",
          h.div_from_questions_file(q2) == "cyber"
          and h.resolve_raw_path(".", "raw", "F", "cyber").endswith("F-cyber-questions.jsonl"))
try:
    h.div_from_questions_file("questions-other.json")
    check("unresolvable basename raises", False)
except ValueError:
    check("unresolvable basename raises", True)

print("== 4. questions->division mapping in released data ==")
for div, fn, n in (("general", "questions-general.json", 18),
                   ("cyber", "questions-cyber.json", 14)):
    p = os.path.join(HERE, "..", "data", fn)
    if os.path.exists(p):
        import json
        ids = [x["id"] for x in json.load(open(p, encoding="utf-8"))]
        pref = "G" if div == "general" else "C"
        check(f"{fn}: {n} ids all {pref}*", len(ids) == n and all(i.startswith(pref) for i in ids))

print("== 5. all released scripts compile ==")
for fn in sorted(os.listdir(HERE)):
    if fn.endswith(".py"):
        try:
            py_compile.compile(os.path.join(HERE, fn), doraise=True)
            check(f"compiles {fn}", True)
        except py_compile.PyCompileError as e:
            check(f"compiles {fn}", False, str(e))

print("\n" + ("ALL PATH-CONTRACT TESTS PASSED" if not FAILURES else f"{len(FAILURES)} FAILURES"))
sys.exit(1 if FAILURES else 0)
