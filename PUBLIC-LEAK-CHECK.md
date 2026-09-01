# PUBLIC LEAK CHECK — release-candidate/

Files scanned: 47 (figures excluded: binary)
Patterns: local absolute paths, usernames, private roots, key/secret/password/
cookie patterns, private git remotes, reasoning-channel content, private-mapping
markers. Note: D/C contestant ids now appear only inside the two sanitized
locked scorebooks, whose mapping was revealed post-lock by design.

## FINDINGS

**none** — no real leaks (paths, usernames, credentials, mapping content).

## Reviewed non-leaks (NOT modified, per policy)

| file | pattern | context |
|---|---|---|
| METHODOLOGY.md | reasoning channel content markers | esponse (= API message.content), reasoning (= API reasoning_content), usage (completion_tokens, prompt_toke  [API field-name doc/code, not content] |
| data\formal-c-answers-final-only.csv | API key / secret patterns | sword is overridden by environment variables or a secrets manager in production.   - If the pass  [verbatim answer body, reviewed, unmodified] |
| data\formal-c-answers-final-only.csv | API key / secret patterns | ssword, but we don't know if it is a **functional secret** or a **placeholder**. If 'admin123' i  [verbatim answer body, reviewed, unmodified] |
| data\formal-c-answers-final-only.csv | API key / secret patterns | emote control via the API, usually from hardcoded secrets or absent pinning rather than broken T  [verbatim answer body, reviewed, unmodified] |
| data\formal-c-answers-final-only.csv | API key / secret patterns | h curl -i -sS \   -X POST \   -d ""username=admin&password=test"" \   http://<lab-ip>:<port>/login   [verbatim answer body, reviewed, unmodified] |
| data\formal-c-answers-final-only.csv | API key / secret patterns |  -X POST \   -d ""username=admin' OR '1'='1' -- -&password=x"" \   http://<lab-ip>:<port>/login ```  [verbatim answer body, reviewed, unmodified] |
| data\formal-c-answers-final-only.csv | API key / secret patterns | to the internet. Even if the repo is private, the secret is still a vulnerability if the passwor  [verbatim answer body, reviewed, unmodified] |
| data\formal-d-answers-final-only.csv | API key / secret patterns | assword, the scanner has correctly identified a ""secret in code."" In modern DevSecOps, secrets  [verbatim answer body, reviewed, unmodified] |
| data\formal-d-answers-final-only.csv | API key / secret patterns | tified a ""secret in code."" In modern DevSecOps, secrets (passwords, API keys, tokens) should b  [verbatim answer body, reviewed, unmodified] |
| data\formal-d-answers-final-only.csv | API key / secret patterns | should be injected via environment variables or a Secret Manager (like AWS Secrets Manager or Ha  [verbatim answer body, reviewed, unmodified] |
| data\formal-d-answers-final-only.csv | API key / secret patterns | vironment variables or a Secret Manager (like AWS Secrets Manager or HashiCorp Vault), not store  [verbatim answer body, reviewed, unmodified] |
| data\formal-d-answers-final-only.csv | API key / secret patterns | tenated directly into the path, so a key like `../secret` reads/writes arbitrary files. *Fix:* V  [verbatim answer body, reviewed, unmodified] |
| data\formal-d-answers-final-only.csv | API key / secret patterns | lue that could be a placeholder, default, or test secret rather than a live production secret. A  [verbatim answer body, reviewed, unmodified] |
| data\formal-d-answers-final-only.csv | API key / secret patterns | ult, or test secret rather than a live production secret. Actual impact depends on whether it's   [verbatim answer body, reviewed, unmodified] |
| data\formal-d-answers-final-only.csv | API key / secret patterns | e and replay: POST /login HTTP/1.1 username=admin&password=' OR 1=1-- ```  **Why a heavier tool is   [verbatim answer body, reviewed, unmodified] |
| data\formal-d-answers-final-only.csv | API key / secret patterns | n-based auth (e.g., a short-lived JWT or a shared secret) and enforcing HTTPS (or TLS 1.2+) on t  [verbatim answer body, reviewed, unmodified] |
| scripts\arena_harness.py | reasoning channel content markers | nse (= message.content),     reasoning (= message.reasoning_content), usage, timings, wall_ms, gen_ts,       [API field-name doc/code, not content] |
| scripts\arena_harness.py | reasoning channel content markers | "content") or ""             reasoning = msg.get("reasoning_content") or ""             usage = resp.get("u  [API field-name doc/code, not content] |

**PUBLIC LEAK CHECK: PASS**
