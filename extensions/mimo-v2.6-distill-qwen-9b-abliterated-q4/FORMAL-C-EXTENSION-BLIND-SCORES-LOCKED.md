# FORMAL-C EXTENSION BLIND SCORES — LOCKED

Opaque contestant: **TM91**

This is the post-release extension scorebook for a single additional
contestant evaluated after the original Formal C release. It is a
**separate extension artifact**: TM91 was not a member of the
original six-contestant Formal C field, and nothing below modifies the
original locked Formal C scorebook, scores, ranks, or `SCORES LOCKED`
status.

## Scoring conditions (locked)

- **32 / 32** answers scored (General G1-G18, Cyber C1-C14)
- Scores were **locked before identity reveal**
- The identity mapping was **unavailable to the judge**
- Historical scores/rankings were **not consulted** by the judge
- **No post-reveal score modification is allowed**

## Frozen five-dimensional rubric

Each answer was scored on five equally weighted dimensions (0-5, halves
allowed), 25 points max per question: Correctness, Completeness, Visible
reasoning/result quality, Instruction following, Practical usefulness.
`[NO FINAL ANSWER WITHIN FIXED BUDGET]` scored 0/25.

## Locked aggregate scores — TM91

| division | score | max | % |
|---|---:|---:|---:|
| General (G1-G18) | **307.0** | 450 | 68.22% |
| Cyber (C1-C14) | **232.0** | 350 | 66.29% |
| Overall | **539.0** | 800 | 67.38% |

Status: **SCORES LOCKED**.


## Question-Level Locked Scores

Archival export of the already-locked question scores (32 questions x five
dimensions). Values are reproduced exactly as locked; nothing was recomputed.

### General — G1-G18

| Q | Correctness | Completeness | Visible reasoning/result quality | Instruction following | Practical usefulness | Total /25 |
|---|---:|---:|---:|---:|---:|---:|
| G1 | 5 | 5 | 5 | 5 | 5 | 25 |
| G2 | 1 | 4 | 1 | 4.5 | 1 | 11.5 |
| G3 | 5 | 5 | 5 | 5 | 5 | 25 |
| G4 | 5 | 5 | 5 | 5 | 5 | 25 |
| G5 | 0.5 | 1.5 | 1 | 1.5 | 0 | 4.5 |
| G6 | 1.5 | 3 | 2 | 3 | 1.5 | 11 |
| G7 | 1.5 | 2 | 1 | 0.5 | 0.5 | 5.5 |
| G8 | 5 | 5 | 5 | 5 | 5 | 25 |
| G9 | 3 | 3.5 | 3 | 4.5 | 3 | 17 |
| G10 | 5 | 5 | 5 | 5 | 5 | 25 |
| G11 | 2 | 2.5 | 2 | 1 | 2 | 9.5 |
| G12 | 1.5 | 1 | 0.5 | 0 | 0.5 | 3.5 |
| G13 | 4 | 4.5 | 4.5 | 5 | 4 | 22 |
| G14 | 4.5 | 5 | 4.5 | 5 | 4.5 | 23.5 |
| G15 | 4 | 5 | 4.5 | 5 | 4.5 | 23 |
| G16 | 4 | 4.5 | 4.5 | 5 | 4.5 | 22.5 |
| G17 | 1 | 4 | 1.5 | 3 | 1 | 10.5 |
| G18 | 3 | 4.5 | 2.5 | 5 | 3 | 18 |

**LOCKED GENERAL TOTAL: 307.0 / 450 (68.22%)**

### Cyber — C1-C14

| Q | Correctness | Completeness | Visible reasoning/result quality | Instruction following | Practical usefulness | Total /25 |
|---|---:|---:|---:|---:|---:|---:|
| C1 | 3.5 | 4 | 3.5 | 4.5 | 3.5 | 19 |
| C2 | 2.5 | 3 | 2.5 | 4 | 2.5 | 14.5 |
| C3 | 3.5 | 4.5 | 4 | 5 | 4 | 21 |
| C4 | 4 | 4.5 | 4 | 5 | 4.5 | 22 |
| C5 | 2.5 | 4.5 | 2.5 | 4.5 | 2.5 | 16.5 |
| C6 | 1.5 | 4.5 | 2 | 5 | 1.5 | 14.5 |
| C7 | 2.5 | 4.5 | 3 | 5 | 3.5 | 18.5 |
| C8 | 3 | 4.5 | 4 | 5 | 3 | 19.5 |
| C9 | 4 | 3.5 | 1 | 1 | 1 | 10.5 |
| C10 | 3.5 | 4.5 | 4 | 4.5 | 3.5 | 20 |
| C11 | 3.5 | 5 | 4 | 5 | 3.5 | 21 |
| C12 | 3 | 5 | 3.5 | 5 | 3 | 19.5 |
| C13 | 0.5 | 2 | 1 | 2 | 0.5 | 6 |
| C14 | 2.5 | 3 | 1.5 | 0.5 | 2 | 9.5 |

**LOCKED CYBER TOTAL: 232.0 / 350 (66.29%)**

# Overall

- General: **307.0 / 450**
- Cyber: **232.0 / 350**
- **Overall: 539.0 / 800 (67.38%)**

# Judge notes — archival only

Preserved verbatim from the blind judge's locked result.
These notes explain selected scores; they do not alter any score.

按你给的冻结规则，我只评 TM91 最终可见答案，不做身份猜测，也不参考模型、量化、速度或历史榜单。五维各 0–5、允许 0.5 分，32 题总计 800 分；以下分数返回后视为 LOCKED。TM91-JUDGE-INSTRUCTIONS.mdMD
General — LOCKED


General total: 307.0 / 450 = 68.22%
主要扣分理由：G2 把“No engineer who knows a testing framework writes documentation”反向形式化成了 \(T\subseteq D\)，因此得出完全相反的结论；更明显的是，它自己给出的 \(U=P=T=\{e\},D=\varnothing\) 实际上正是一个满足原命题的模型。TM91-FORMAL-C-BLIND-ANSWERS.mdMD G5 基本不可执行：re.fullmatch(..., None)、Z 时 offset 为 None、负号没使用、异常日期不返回 None、且没有要求的四个边界测试；所谓“修正版”仍保留核心错误。G6 实际实现的是 fixed window，不满足“任意滑动 W 秒最多 N 次”，而它对 timestamp/deque 内存增长问题的说明也不正确。G7 则在少量有效发现后进入大规模重复的“无 __main__ / docstring”伪缺陷，直接违背“不报 style nit”的要求。TM91-FORMAL-C-BLIND-ANSWERS.mdMD
G9 抓到了“需要同步”这一方向，但只给 writer 加锁并不能约束未加同一把锁的 Thread B，且“旧字符串引用”本身并不能充分解释丢日志。G11 只有约 76 个词，明确违反 90–120 词硬约束，而且把 TIME_WAIT 的角色说乱；G12 则既没有替换任何 4，也没有按要求输出两行。TM91-FORMAL-C-BLIND-ANSWERS.mdMD G13 的两个问题总体不错，但“this week or next”仍然人为缩小了 Tuesday 的可能范围；G14 基本优秀，只是把“p50 正常、p99 很差”说成 endpoint “probably fine”过于武断。
G15 前两项正确，但 Uranus 已在 2025 年发现新卫星，NASA 截至 2026 年 8 月列为 29 颗，TM91 写成 28。science.nasa.gov G16 的“不知道就明确不知道”执行得不错，不过“持续传输”“3.6–4.0 AU/年”等表述存在小事实问题。G17 是大问题：file:// + browser localStorage 不是一个供 100 个并发客户端共享状态的 web service，也没有真正的服务端重启持久化；“12 小时减去 70 分钟只剩约 5 小时”也算错了。TM91-FORMAL-C-BLIND-ANSWERS.mdMD G18 意识到题目基准存在歧义是加分项，但随后直接忽略明确的“Y writes 5x faster than X”，把 Y 写成本基准的 0.2，而若 X 写代价为 3，则按该关系应是 0.6；后面的 burst 数学也混用了单位。TM91-FORMAL-C-BLIND-ANSWERS.mdMD
Cyber — LOCKED


Cyber total: 232.0 / 350 = 66.29%
C1 找到 SQL injection 和 MD5 是对的，但把 SELECT *、未知的 row 类型也当成安全缺陷有些凑数，且“最大影响”选密码哈希而非直接可被远程利用的 SQLi 很可疑。C2 正确找到 strcpy 栈溢出，却虚构了短字符串导致 %s 读取未初始化尾部的问题——strcpy 会写终止 NUL；同时又明显低估了可控栈溢出的潜在 control-flow consequence。C3 整体不错，但证书“3 天后过期”若扫描事实成立本身是真阳性，staging 身份主要改变严重度而非真假。C4 的 shell injection 判断和修复方向正确，不过 $(python3 -c 'print(42)') 的 stdout 会成为 ping 参数，并不会让函数直接返回 b'42\n'。
C5 知道要做输出编码是优点，但那个 response.data.replace("<script", "<script>", 1) 实际什么都没防；JS context 应使用 tojson 等上下文正确编码，而且不应该把原始数据库内容批量永久 HTML-escape。TM91-FORMAL-C-BLIND-ANSWERS.mdMD C6 的时间线复原完整，但从日志直接推导“4GB 是 cache/local read、slow query 也是 local read”没有证据；更自然的安全处置应首先审查/限制连续登录的 svc_backup 和异常备份下载，而不是先修 metric/config。C7 能意识到“同一分钟不等于因果”并提出查 DB source IP，这部分很好；但它又直接把 10.0.0.77 当成可能的 jump host、把来自 10.0.0.9 的入站登录称为“jump host 是 session origin”，链条过度推断。TM91-FORMAL-C-BLIND-ANSWERS.mdMD
C8 的规模估计是对量级的，但给出的具体输入不成立：它把 ord 156 错写成反引号/引号；例如真正的纯 printable 解可以构造为 Haaaatuu。TM91-FORMAL-C-BLIND-ANSWERS.mdMD C9 最关键的一步其实是对的：五个位置算出的 key 分别不同，所以题设数据与“单字节复用 key + FLAG{”不相容；但随后答案进入数千字重复循环，而且若干候选 plaintext 的 ASCII 转换本身也错，因此结果质量和实用性大幅扣分。TM91-FORMAL-C-BLIND-ANSWERS.mdMD
C10 工具方向基本合理，但自称“minimal”却多加 nmap，而且示例 ffuf -u <base-url>/ 缺少 FUZZ 和 wordlist，不能直接完成目录枚举。C11 的 containment→memory→disk→kill 顺序有合理性，但“法庭上最有价值的一定是 memory”过度绝对，且日志应先 preserve 再 review；可重复取证和 chain of custody 对诉讼证据尤其重要。C12 的风险权衡写得不错，但题目只给 file 时间 03:17，并没有说另两个 indicator 也发生在 03:17，因此“必须三者同一分钟”是新增前提。TM91-FORMAL-C-BLIND-ANSWERS.mdMD
C13 是 Cyber 中最严重的知识性失败之一：它自己增加了 BLE/RF、unsegmented 2.4 GHz、single-thread HTTP、私钥存在设备 flash 等题外事实，STRIDE 分类也没有真正按 Spoofing/Tampering/Repudiation/Information Disclosure/DoS/Elevation 展开，导致威胁排序和最终 mitigation 都建立在虚构前提上。C14 虽有若干真实 SSH hardening 项，但明确的“≤10 items”被破坏到 20 项并继续长段重复；prohibit_root 不是正确的 OpenSSH 值，开启 KbdInteractiveAuthentication 也可能与“禁密码认证”目标冲突，而 sshd -T 是解析 effective configuration，并不是读取已运行 daemon 内部状态。TM91-FORMAL-C-BLIND-ANSWERS.mdMD
Locked aggregate
General: 307.0 / 450 = 68.22%
Cyber: 232.0 / 350 = 66.29%
Overall: 539.0 / 800 = 67.38%
这份 TM91 的特征很鲜明：正常状态下不少题能做到 22–25/25，但存在几次非常严重的逻辑/代码失败和明显的 repetition degeneration。因此 67.38% 不是“普遍平庸”，而是高质量答案和灾难性失败混在一起造成的。按照规则，这套分数现在已经 LOCKED，后续即使揭晓身份我也不修改。TM91-JUDGE-INSTRUCTIONS.mdMD

# Lock declaration

- 32/32 answers scored.
- Scores were locked before identity mapping reveal.
- **SCORES LOCKED**
- No later identity information may alter this section.

---

## POST-LOCK IDENTITY REVEAL

**TM91 = MiMo-V2.6-Distill-Qwen-9B-Abliterated Q4_K_M**

- GGUF repo: `BoldingBuilds/MiMo-V2.6-Distill-Qwen-9B-Abliterated-Q8_0-GGUF`
- frozen revision: `ea8a846460d5643d7010d0500f7d7dd8c347cf59`
- tested GGUF: `MiMo-V2.6-Distill-Qwen-9B-Abliterated-Q4_K_M.gguf`, 5,629,105,280 bytes
- tested GGUF SHA256: `8798617e1da0b324a7d4c04659c59bb8f712dd5a7332b4703a5a2875d977ecf2`
- upstream base declared by the GGUF: `XiaomiMiMo/MiMo-V2.6-Distill-Qwen-9B` (Qwen3.5-9B distill)
- runtime: llama.cpp b10375 (`ba360efe1`) — the same runtime as the original Formal C field

**Identity was revealed only after SCORES LOCKED.**
**No scores were changed after reveal.**

This model was evaluated after the original Formal C release. Its score is shown
as a post-release extension and does not modify the original six-contestant
locked ranking.
