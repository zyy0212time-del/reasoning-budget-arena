"""Formal C objective post-run analysis (sanitized release copy).

Recomputes per-request structural metrics from raw/formal-c/ JSONL:

  has_final            = final content non-empty after strip (never from reasoning)
  has_reasoning        = reasoning channel non-empty (presence only)
  near_context_limit   = prompt_tokens + completion_tokens >= ctx   (server window)
  near_generation_cap  = completion_tokens >= 0.9 * max_tokens      (request cap)
  loop_candidate       = heuristic screen (see METHODOLOGY.md); NOT a loop verdict
  confirmed_loop       = joined from the manually reviewed formal-c-loop-audit.csv
  clean_final          = has_final AND not confirmed_loop AND not near_context_limit

Known limitations (documented in METHODOLOGY.md):
  - no per-response reasoning token count exists in the raw records
  - no finish_reason is stored; context exhaustion is inferred from the
    exact-total signature (prompt+completion == ctx)
"""
from __future__ import annotations

import csv
import json
import os
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
RC = os.path.dirname(HERE)                              # release-candidate/
EXPROOT = os.path.dirname(RC)                           # experiment root
BASE = os.path.abspath(os.path.join(EXPROOT, "raw", "formal-c"))
OUT = os.path.abspath(os.path.join(RC, "data", "formal-c-objective.csv"))
LOOP_AUDIT = os.path.abspath(os.path.join(RC, "data", "formal-c-loop-audit.csv"))
TAGS = "ABCDEF"
CTX, MAXTOK = 8192, 8192

REASONING_MARKERS = re.compile(
    r"\b(let me|let's|okay,|hmm|wait|re-?read|hold on|actually|"
    r"start over|try again|step 1|first, let|again)\b", re.I)


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


def load(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def main():
    confirmed = {}
    if os.path.exists(LOOP_AUDIT):
        for r in csv.DictReader(open(LOOP_AUDIT, encoding="utf-8-sig")):
            confirmed[(r["tag"], r["division"], r["question_id"])] = r["confirmed_loop"] == "yes"

    rows = []
    for tag in TAGS:
        for div in ("general", "cyber"):
            path = os.path.join(BASE, tag, f"{tag}-{div}-questions.jsonl")
            for rec in load(path):
                content = rec.get("response") if isinstance(rec.get("response"), str) else ""
                reasoning = rec.get("reasoning") if isinstance(rec.get("reasoning"), str) else ""
                u = rec.get("usage") or {}
                pt, ct = u.get("prompt_tokens"), u.get("completion_tokens")
                has_final = bool(content) and content.strip() != ""
                cx = (pt is not None and ct is not None and (pt + ct) >= CTX)
                ngc = (ct is not None and ct >= 0.9 * MAXTOK)
                d10 = dup10(content) if has_final else 0.0
                mlr = max_line_repeat(content) if has_final else 0
                mk = len(REASONING_MARKERS.findall(content)) if has_final else 0
                key = (tag, div, rec["id"])
                confirmed_loop = confirmed.get(key, False)
                rows.append({
                    "original_tag": tag, "division": div, "question_id": rec["id"],
                    "has_reasoning": "yes" if reasoning.strip() else "no",
                    "has_final": "yes" if has_final else "no",
                    "prompt_tokens": pt, "completion_tokens": ct,
                    "total_tokens": u.get("total_tokens"),
                    "reasoning_tokens": "NA_NOT_STORED",
                    "reasoning_budget_hit": "UNKNOWN",
                    "finish_reason": "NA_NOT_STORED",
                    "near_generation_cap": "yes" if ngc else "no",
                    "near_context_limit": "yes" if cx else "no",
                    "loop_candidate": "yes" if (cx or d10 >= 0.30 or mlr >= 3) else "no",
                    "confirmed_loop": "yes" if confirmed_loop else "no",
                    "clean_final": "yes" if (has_final and not confirmed_loop and not cx) else "no",
                    "gen_t_s": round(rec.get("gen_ts") or 0, 2),
                    "pp_t_s": round(rec.get("pp_ts") or 0, 2),
                    "wall_ms": round(rec.get("wall_ms") or 0, 1),
                })
    with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT} ({len(rows)} rows)")
    print("has_final:", sum(1 for r in rows if r["has_final"] == "yes"))
    print("near_context_limit:", sum(1 for r in rows if r["near_context_limit"] == "yes"))
    print("confirmed_loop:", sum(1 for r in rows if r["confirmed_loop"] == "yes"))
    print("clean_final:", sum(1 for r in rows if r["clean_final"] == "yes"))


if __name__ == "__main__":
    main()
