"""FORMAL C runner — 6 models x 32 frozen questions, uniform hard reasoning budget.

Sanitized release copy of the Formal C runner. Reads model paths / llama-server
location from CONFIG.json (see CONFIG.example.json). Behavior matches the
experiment run:

- ctx=8192, max_tokens=8192, --reasoning-budget 4096, temp=0.1, top_p=0.9,
  native/default chat template and thinking, one server at a time
- raw -> raw/formal-c/{tag}/ (fresh dir; aborts if pre-existing non-empty)
- after each division: integrity check (18 General + 14 Cyber = 32 unique ids)
- infrastructure failures may be retried ONCE identically via --ids append
  (model failures are NEVER retried)

Formal D differs only in: no --reasoning-budget flag (native/default thinking),
raw under raw/formal-d/, plus a 3-question supplement for G1/G8/G10 (see
METHODOLOGY.md).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "CONFIG.json")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        sys.exit("CONFIG.json not found. Copy CONFIG.example.json to CONFIG.json "
                 "and fill in local paths.")
    return json.load(open(CONFIG_PATH, encoding="utf-8"))


def log(msg: str) -> None:
    print(f"{datetime.now().strftime('%H:%M:%S')} {msg}", flush=True)


def read_recs(path: str) -> list:
    if not os.path.exists(path):
        return []
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def load_ids(qfile: str) -> list:
    return [q["id"] for q in json.load(open(qfile, encoding="utf-8"))]


def division_integrity(tag: str, div: str, expected_ids: list, base: str):
    # path contract: base/<tag>/<tag>-<div>-questions.jsonl (div in {general, cyber})
    path = os.path.join(base, tag, f"{tag}-{div}-questions.jsonl")
    recs = read_recs(path)
    ids = [r.get("id") for r in recs]
    dups = {i for i in ids if ids.count(i) > 1}
    if dups:
        log(f"[FATAL] {tag}/{div}: duplicate question ids {sorted(dups)} - STOP")
        sys.exit(2)
    missing = [i for i in expected_ids if i not in set(ids)]
    empty = [r.get("id") for r in recs
             if not r.get("response") and not r.get("reasoning") and not (r.get("usage") or {})]
    return (len(missing) == 0 and not empty), missing


def main() -> None:
    cfg = load_config()
    harness = os.path.join(HERE, "arena_harness.py")
    # canonical raw layout: <experiment root>/raw/formal-c/<tag>/<tag>-<div>-questions.jsonl
    # --outdir is the experiment root; --rawdir is raw/formal-c/<tag>.
    exproot = os.path.abspath(os.path.join(HERE, "..", ".."))
    base = os.path.join(exproot, "raw", "formal-c")
    divs = [("general", os.path.abspath(os.path.join(HERE, "..", "data", "questions-general.json")), 18),
            ("cyber", os.path.abspath(os.path.join(HERE, "..", "data", "questions-cyber.json")), 14)]

    if os.path.exists(base) and os.listdir(base):
        log(f"[ABORT] {base} exists and is non-empty")
        sys.exit(1)
    os.makedirs(base, exist_ok=True)
    log("FORMAL C START (ctx=8192, max_tokens=8192, reasoning_budget=4096, temp=0.1, top_p=0.9)")

    infra_retries = 0
    done = {}
    for tag in "ABCDEF":
        model = cfg["models"][tag]["path"]
        ncmoe = cfg["models"][tag]["ncmoe"]
        if not os.path.exists(model):
            log(f"[ABORT] {tag}: model missing: {model}")
            sys.exit(1)
        log(f"=== MODEL {tag} START (ncmoe={ncmoe}) ===")
        for div, qfile, n_expected in divs:
            expected = load_ids(qfile)
            assert len(expected) == n_expected
            log(f"[{tag}/{div}] run start ({n_expected} questions)")
            cmd = [sys.executable, harness, "--model", model, "--tag", tag,
                   "--questions", qfile, "--div", div,
                   "--outdir", exproot,
                   "--ncmoe", str(ncmoe), "--ctx", "8192", "--max-tokens", "8192",
                   "--temp", "0.1", "--top-p", "0.9",
                   "--reasoning-budget", "4096", "--no-speed",
                   "--rawdir", os.path.join("raw", "formal-c", tag),
                   "--llama-server", cfg["llama_server"]]
            rc = subprocess.run(cmd).returncode
            ok, missing = division_integrity(tag, div, expected, base)
            if rc != 0 or not ok:
                if infra_retries >= 6:
                    log(f"[ABORT] {tag}/{div}: infrastructure retry budget exhausted")
                    sys.exit(3)
                infra_retries += 1
                log(f"[{tag}/{div}] INFRASTRUCTURE RETRY #{infra_retries} (rc={rc}, missing={missing})")
                cmd += ["--ids", ",".join(missing)]
                rc = subprocess.run(cmd).returncode
                ok, missing = division_integrity(tag, div, expected, base)
                if rc != 0 or not ok:
                    log(f"[ABORT] {tag}/{div}: still failing after retry")
                    sys.exit(3)
            recs = read_recs(os.path.join(base, tag, f"{tag}-{div}-questions.jsonl"))
            log(f"[{tag}/{div}] OK: {len({r.get('id') for r in recs})}/{n_expected} unique ids")
        done[tag] = True
        log(f"=== MODEL {tag} COMPLETE 32/32 ===")
    log(f"FORMAL C GENERATION COMPLETE: 6 models x 32 = 192 requests, "
        f"infrastructure retries = {infra_retries}")


if __name__ == "__main__":
    main()
