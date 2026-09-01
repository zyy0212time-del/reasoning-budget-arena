"""Arena benchmark harness — run one model against a question set via llama-server.

This is the sanitized release copy of the harness used for Formal D and
Formal C. Behavior is identical to the experiment version; machine-specific
absolute paths are replaced by CLI arguments / environment variables.

Usage:
    python arena_harness.py --model <gguf> --tag <ANON_TAG> --questions <json>
        [--outdir .] [--ctx 8192] [--max-tokens 8192] [--temp 0.1] [--top-p 0.9]
        [--ngl 99] [--ncmoe N] [--threads 24] [--port 0] [--system ""]
        [--ids ID1,ID2] [--rawdir raw] [--reasoning-budget N] [--no-speed]

Environment / arguments:
    --llama-server   path to llama-server (default: env LLAMA_SERVER, else
                     "llama-server" on PATH)

Notes:
  * starts llama-server, waits for /health ok, one request per question via
    /v1/chat/completions (model chat template applied)
  * writes raw per-question JSONL incrementally (crash-safe resume)
  * a fresh run (no --ids) deletes the existing per-tag JSONL to avoid mixing
    passes; targeted re-runs (--ids) append
  * raw records store: id, tag, prompt, response (= message.content),
    reasoning (= message.reasoning_content), usage, timings, wall_ms, gen_ts,
    pp_ts, and the request configuration (reasoning_budget, ctx, max_tokens,
    temperature, top_p, ncmoe). No finish_reason and no per-response reasoning
    token count are available from the backend as captured.
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request


def _post(port: int, path: str, payload: dict, timeout: int = 900) -> dict:
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}{path}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def _wait_ready(port: int, timeout: int = 900) -> None:
    t0 = time.time()
    last = ""
    while time.time() - t0 < timeout:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=5) as r:
                body = r.read().decode()
            if body and json.loads(body).get("status") == "ok":
                return
            last = body
        except Exception as exc:  # noqa: BLE001
            last = str(exc)
        time.sleep(5)
    raise TimeoutError(f"server not ready in {timeout}s; last health: {last}")


def _parse_timings(resp: dict) -> dict:
    t = resp.get("timings") or {}
    return {
        "prompt_n": t.get("prompt_n"),
        "prompt_ms": t.get("prompt_ms"),
        "predicted_n": t.get("predicted_n"),
        "predicted_ms": t.get("predicted_ms"),
    }


def _gen_ts(t: dict):
    n, ms = t.get("predicted_n"), t.get("predicted_ms")
    if n is None or ms is None or not ms:
        return None
    return n * 1000.0 / ms


def _pp_ts(t: dict):
    n, ms = t.get("prompt_n"), t.get("prompt_ms")
    if n is None or ms is None or not ms:
        return None
    return n * 1000.0 / ms


# ---- path contract (single source of truth) ----
# Canonical raw layout (used by runner, harness and integrity checker):
#   <outdir>/<rawdir>/<tag>-<div>-questions.jsonl
# with div in {"general", "cyber"} and tag in {"A".."F"}.
# `--div` is explicit; it is never inferred from the questions filename, so
# data/questions-general.json -> div=general regardless of file basename.


def resolve_raw_path(outdir, rawdir, tag, div):
    """Return the canonical raw JSONL path for (tag, div)."""
    return os.path.join(outdir, rawdir, f"{tag}-{div}-questions.jsonl")


def div_from_questions_file(qfile):
    """Backward-compatible fallback: derive div from the questions basename."""
    base = os.path.basename(qfile).lower()
    if "general" in base:
        return "general"
    if "cyber" in base:
        return "cyber"
    raise ValueError(f"cannot determine division from questions file name: {qfile}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--questions", required=True)
    ap.add_argument("--div", choices=["general", "cyber"], default=None,
                    help="explicit division (released usage passes this; fallback "
                         "infers it from the --questions basename)")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--ctx", type=int, default=8192)
    ap.add_argument("--max-tokens", type=int, default=8192)
    ap.add_argument("--temp", type=float, default=0.1)
    ap.add_argument("--top-p", type=float, default=0.9)
    ap.add_argument("--ngl", type=int, default=99)
    ap.add_argument("--ncmoe", type=int, default=0)
    ap.add_argument("--threads", type=int, default=24)
    ap.add_argument("--port", type=int, default=0)  # 0 = pick a free port
    ap.add_argument("--system", default="")
    ap.add_argument("--ids", default="")
    ap.add_argument("--rawdir", default="raw")
    ap.add_argument("--reasoning-budget", type=int, default=-1)
    ap.add_argument("--reasoning-budget-message", default=None)
    ap.add_argument("--no-speed", action="store_true")
    ap.add_argument("--llama-server", default=os.environ.get("LLAMA_SERVER", "llama-server"))
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    questions = json.load(open(args.questions, encoding="utf-8"))
    div = args.div or div_from_questions_file(args.questions)
    raw_path = resolve_raw_path(args.outdir, args.rawdir, args.tag, div)
    os.makedirs(os.path.dirname(raw_path), exist_ok=True)
    want_ids = {x.strip() for x in args.ids.split(",") if x.strip()}
    if want_ids:
        questions = [q for q in questions if q["id"] in want_ids]
    else:
        if os.path.exists(raw_path):
            os.remove(raw_path)

    if args.port:
        port = args.port
    else:
        sock = socket.socket()
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
        sock.close()

    cmd = [args.llama_server, "-m", args.model, "-c", str(args.ctx), "--flash-attn", "on",
           "-ngl", str(args.ngl), "-t", str(args.threads),
           "--host", "127.0.0.1", "--port", str(port)]
    if args.ncmoe:
        cmd += ["-ncmoe", str(args.ncmoe)]
    if args.reasoning_budget >= 0:
        cmd += ["--reasoning-budget", str(args.reasoning_budget)]
        if args.reasoning_budget_message is not None:
            cmd += ["--reasoning-budget-message", args.reasoning_budget_message]
    log_path = os.path.join(args.outdir, args.rawdir, f"{args.tag}-{div}-server.log")
    with open(log_path, "wb") as logf:
        proc = subprocess.Popen(cmd, stdout=logf, stderr=subprocess.STDOUT)
    try:
        _wait_ready(port)
        for q in questions:
            messages = []
            if args.system:
                messages.append({"role": "system", "content": args.system})
            messages.append({"role": "user", "content": q["prompt"]})
            t0 = time.time()
            resp = _post(port, "/v1/chat/completions",
                         {"model": args.tag, "messages": messages,
                          "temperature": args.temp, "top_p": args.top_p,
                          "max_tokens": args.max_tokens, "stream": False})
            wall_ms = (time.time() - t0) * 1000.0
            msg = resp["choices"][0]["message"]
            text = msg.get("content") or ""
            reasoning = msg.get("reasoning_content") or ""
            usage = resp.get("usage", {})
            tim = _parse_timings(resp)
            rec = {
                "id": q["id"], "tag": args.tag, "prompt": q["prompt"],
                "response": text, "reasoning": reasoning,
                "usage": usage, "timings": tim,
                "wall_ms": round(wall_ms, 1),
                "gen_ts": _gen_ts(tim), "pp_ts": _pp_ts(tim),
                "reasoning_budget": args.reasoning_budget,
                "ctx": args.ctx, "max_tokens": args.max_tokens,
                "temperature": args.temp, "top_p": args.top_p,
                "ncmoe": args.ncmoe,
            }
            with open(raw_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(f"[{args.tag}/{div}] {q['id']} out={usage.get('completion_tokens')} "
                  f"gen_ts={_gen_ts(tim)} pp_ts={_pp_ts(tim)} wall={wall_ms:.0f}ms",
                  flush=True)
        if args.no_speed:
            return
        bench_prompt = ("Write a detailed, well-structured technical explanation of "
                        "how virtual memory paging works on modern operating systems. "
                        "Continue until asked to stop.")
        t0 = time.time()
        resp = _post(port, "/v1/chat/completions",
                     {"model": args.tag, "messages": [{"role": "user", "content": bench_prompt}],
                      "temperature": 0.0, "max_tokens": 220, "stream": False})
        wall_ms = (time.time() - t0) * 1000.0
        tim = _parse_timings(resp)
        bench = {"id": "SPEED", "tag": args.tag,
                 "response": resp["choices"][0]["message"]["content"],
                 "usage": resp.get("usage", {}), "timings": tim,
                 "wall_ms": round(wall_ms, 1),
                 "gen_ts": _gen_ts(tim), "pp_ts": _pp_ts(tim)}
        with open(raw_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(bench, ensure_ascii=False) + "\n")
        print(f"[{args.tag}] SPEED gen_ts={_gen_ts(tim)} pp_ts={_pp_ts(tim)} wall={wall_ms:.0f}ms", flush=True)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main()
