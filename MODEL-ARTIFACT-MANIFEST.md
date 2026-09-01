# MODEL-ARTIFACT-MANIFEST

Generated: 2026-09-01 21:20:19

Purpose: record exact local benchmark artifacts BEFORE any C-drive
cleanup / model retirement, so the Formal D and Formal C benchmark
can be re-downloaded or reproduced later.

SHA256 covers the exact local file named below. If a file is already
missing, it is marked MISSING ON DISK and is NOT re-downloaded without
an explicit user request.

| tag | model | local benchmark filename | sha256 | size (bytes) | quantization | present | source | license |
|---|---|---|---|---|---|---|---|---|
| A | RavenX-CyberAgent-35B-v5.1-Q4_K_M | `RavenX-CyberAgent-35B-v5.1-Q4_K_M.gguf` | `8f75846d57b4947df776f400bbf7c85e7a9092bf9f596b315a775535d6de665f` | 21713463264 | Q4_K_M | yes | SOURCE NOT RECOVERED | UNDETERMINED - see LICENSE-NOTES.md |
| B | Endy-Qwen3.6-CyberSec-35B-A3B-Q4_K_M | `Endy-Qwen3.6-CyberSec-35B-A3B-Q4_K_M.gguf` | `ed118e7768330eb440ddc8ade42a04005ecab37f131d7e84bb08d14d1e315ae1` | 21713462496 | Q4_K_M | yes | SOURCE NOT RECOVERED | UNDETERMINED - see LICENSE-NOTES.md |
| C | Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-Q4_K_M | `Gemma4-26B-A4B-QAT-Uncensored-HauhauCS-Balanced-Q4_K_M.gguf` | `3c13133469e431312fffb8b1d9c85ae42199e6bb5746ea1da84e8ddf2097d73c` | 16796015520 | Q4_K_M | yes | SOURCE NOT RECOVERED | UNDETERMINED - see LICENSE-NOTES.md |
| D | Ornith-1.5-35B-A3B-Abliterated-Q4_K_M | `Ornith-1.5-35B-A3B-Abliterated-Q4_K_M.gguf` | `a07f299e83a398b5078c1cb8ab4ec96333c8ea9d10d0cb479cb073056fedd3d0` | 21166757664 | Q4_K_M | yes | SOURCE NOT RECOVERED | UNDETERMINED - see LICENSE-NOTES.md |
| E | Nex-N2-mini-Q4_K_M | `nex-agi_Nex-N2-mini-Q4_K_M.gguf` | `b158f66ba0bea9a4cc10864777abb9d345c00f0f2f886dc147032e4aa4a86340` | 21391448064 | Q4_K_M | yes | SOURCE NOT RECOVERED | UNDETERMINED - see LICENSE-NOTES.md |
| F | Qwen3.8-9B-abliterated-25-Q4_K_M | `Qwen3.8-9B-abliterated-25.Q4_K_M.gguf` | `542d41f6cf4cc450152651d0d8099bd4856f919f1a8909c3037976480cb894cf` | 5629108864 | Q4_K_M | yes | SOURCE NOT RECOVERED | UNDETERMINED - see LICENSE-NOTES.md |

IMPORTANT — source-status note: the `source` column in this manifest reflects
the state at HASH-CAPTURE time (2026-09-01) and is intentionally frozen as
immutable evidence of the exact artifacts used. For the CURRENT provenance
resolution status, see MODEL-SOURCE-TODO.md and data/model-artifacts.csv; do
not read this manifest's source column as the current provenance answer.

The hash record is immutable evidence for the exact artifacts used in the
Formal D / Formal C benchmark; it does not by itself resolve upstream
licenses or source URLs (see MODEL-SOURCE-TODO.md / LICENSE-NOTES.md).