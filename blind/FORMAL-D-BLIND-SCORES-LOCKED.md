# FORMAL-D BLIND SCORES — LOCKED (sanitized public copy)

This is a **sanitized release copy** of the locked Formal D blind evaluation
artifact. It is published so that readers can verify that the scores were
locked before any identity reveal.

Sanitization applied:
- the narrative judge commentary section (PART 4 — locked qualitative
  summary) was removed as conversational prose about contestants;
- markdown escaping from the export was normalized.

Nothing in the scorebook was altered: no score, half-point, subtotal,
percentage, division rank, or overall rank was changed.

The contestant-to-model identity mapping was revealed **after** this lock and
is documented separately in METHODOLOGY.md.

---
# FORMAL-D BLIND SCORES — LOCKED ARCHIVE



**Filename:** `FORMAL-D-BLIND-SCORES-LOCKED.md`



This document is an archival/export copy of the previously completed and locked Formal D blind evaluation.



**No re-scoring, re-ranking, reconciliation, correction, or score modification was performed during this export.**  

All question-level scores, half-points, subtotals, percentages, ranks, and the final lock state below are frozen exactly as previously locked.



The blind scores were locked **before any contestant-to-model identity mapping reveal**. Any later identity reveal, if supplied, may only be appended in a separate post-lock section and must not alter the blind score section.



\---



## FROZEN FIVE-DIMENSION RUBRIC



Each `(question, contestant)` answer was scored on five equally weighted dimensions using the frozen 0–5 scale, including half-points:



1\. **Correctness** — factual, logical, and technical correctness.

2\. **Completeness** — whether the answer covered what the question actually asked.

3\. **Reasoning / result quality visible in final answer** — only reasoning, proof, explanation, or result quality visible in the final answer; hidden reasoning was not credited.

4\. **Instruction following** — compliance with explicit constraints such as format, length, banned words, exact output shape, and similar requirements.

5\. **Practical usefulness** — whether the answer would actually help someone perform or solve the task reliably.



Each question is worth **25 points** total.



`[NO FINAL ANSWER WITHIN FIXED BUDGET]` received **0 / 25** with all five dimensions set to zero.



All questions and all five dimensions are equally weighted.



\---



# PART 1 — COMPLETE SCOREBOOK



Abbreviations:



\- **C** = Correctness

\- **Comp** = Completeness

\- **R** = Visible reasoning/result quality

\- **IF** = Instruction following

\- **PU** = Practical usefulness



## GENERAL — G1–G18



| Q | ID | C | Comp | R | IF | PU | Total | Locked justification |

|---|---|---:|---:|---:|---:|---:|---:|---|

| G1 | H45 | 5 | 5 | 5 | 5 | 5 | **25** | 正确由 C 运行反推 B、A 运行，唯一失败为 D。 |

| G1 | P40 | 5 | 5 | 5 | 5 | 5 | **25** | 推理链完整正确，结论唯一。 |

| G1 | S41 | 5 | 5 | 5 | 5 | 5 | **25** | 正确完整，反推逻辑清晰。 |

| G1 | W87 | 5 | 5 | 5 | 5 | 5 | **25** | 正确验证所有候选并得到 D。 |

| G1 | X68 | 5 | 5 | 5 | 5 | 5 | **25** | 正确排除 A/B/C 并验证 D。 |

| G1 | Y76 | 5 | 5 | 5 | 5 | 5 | **25** | 简洁且完整地证明 D 唯一可失败。 |

| G2 | H45 | 5 | 5 | 5 | 5 | 5 | **25** | 一阶翻译与单元素模型均严格成立。 |

| G2 | P40 | 5 | 4.5 | 5 | 5 | 5 | **24.5** | 模型正确，但先把 U 定为全体工程师又另引 E，记号略不严整。 |

| G2 | S41 | 5 | 4.5 | 4.5 | 5 | 5 | **24** | 一致性模型正确，但“Translate”部分形式化略简。 |

| G2 | W87 | 4.5 | 4.5 | 4.5 | 5 | 5 | **23.5** | 结论正确；把“认识至少一个框架”压成一元谓词，形式略简化。 |

| G2 | X68 | 5 | 5 | 5 | 5 | 5 | **25** | 集合翻译和见证模型均完整正确。 |

| G2 | Y76 | 5 | 5 | 5 | 5 | 5 | **25** | 关系谓词形式最严格，模型直接证明一致性。 |

| G3 | H45 | 5 | 5 | 5 | 2.5 | 5 | **22.5** | 7 小时证明正确，但题目要求“一句话”，额外解释违反硬约束。 |

| G3 | P40 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G3 | S41 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G3 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G3 | X68 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G3 | Y76 | 5 | 5 | 5 | 5 | 5 | **25** | 准确证明总时长固定为 7 小时，并严格只用一句话。 |

| G4 | H45 | 5 | 5 | 5 | 5 | 5 | **25** | 正确推出 Bob 因 >200 页被拒，队列规则不改变结果。 |

| G4 | P40 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G4 | S41 | 5 | 5 | 5 | 5 | 5 | **25** | 两阶段都完整回答，quota 的隐含条件也推出正确。 |

| G4 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G4 | X68 | 4.5 | 2.5 | 4 | 2.5 | 3 | **16.5** | 已推出 Bob 被拒，但答案截断在 Part 1，第二问未答。 |

| G4 | Y76 | 5 | 5 | 5 | 5 | 5 | **25** | 结论、规则和队列变化均准确完整。 |

| G5 | H45 | 5 | 5 | 5 | 5 | 5 | **25** | stdlib、Z/offset、异常、docstring 和四测试全部满足。 |

| G5 | P40 | 4.5 | 5 | 4.5 | 5 | 5 | **24** | 核心实现正确；非字符串输入导致的 TypeError 未统一兜底。 |

| G5 | S41 | 4.5 | 5 | 4.5 | 5 | 5 | **24** | 基本正确；Z 的全局 replace 与异常覆盖略粗。 |

| G5 | W87 | 5 | 5 | 4.5 | 5 | 5 | **24.5** | 实现和四个边界测试正确，仅 blanket `except Exception` 过宽。 |

| G5 | X68 | 4.5 | 4.5 | 4.5 | 4 | 5 | **22.5** | 基本正确，但给了 5 个测试，且 `int(timestamp())` 会截断小数秒。 |

| G5 | Y76 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G6 | H45 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G6 | P40 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G6 | S41 | 4 | 5 | 4.5 | 5 | 4 | **22.5** | 锁与 deque 正确，但 `time.time()` 会受系统时钟跳变影响。 |

| G6 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G6 | X68 | 4.5 | 5 | 4.5 | 5 | 4.5 | **23.5** | monotonic+deque+lock 正确；锁前采样时间在极端竞争下略不严谨。 |

| G6 | Y76 | 4.5 | 5 | 4.5 | 5 | 4.5 | **23.5** | 正确实现有界滑窗；锁前取 `now` 存在很小并发语义瑕疵。 |

| G7 | H45 | 4.5 | 5 | 4.5 | 5 | 4.5 | **23.5** | 主要真实缺陷齐全；atomic replace 不能完全消除重复计算，表述略宽。 |

| G7 | P40 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G7 | S41 | 3.5 | 4 | 3.5 | 5 | 3.5 | **19.5** | 抓到多项问题，但漏 key 路径穿越；relative-path 项不够具体。 |

| G7 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G7 | X68 | 4.5 | 4 | 4 | 5 | 4 | **21.5** | 四个主问题正确，但漏损坏 pickle 回退，basename 修复会有碰撞风险。 |

| G7 | Y76 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G8 | H45 | 5 | 5 | 5 | 5 | 5 | **25** | 正确识别偶数长度 median bug 并给有效修复和反例。 |

| G8 | P40 | 5 | 5 | 5 | 5 | 5 | **25** | 正确完整，无实质错误。 |

| G8 | S41 | 5 | 5 | 5 | 5 | 5 | **25** | 修复、bug class 与反例全部正确。 |

| G8 | W87 | 5 | 5 | 5 | 5 | 5 | **25** | 正确完整，无实质错误。 |

| G8 | X68 | 5 | 5 | 5 | 5 | 5 | **25** | 正确完整，无实质错误。 |

| G8 | Y76 | 5 | 5 | 5 | 5 | 5 | **25** | 简洁正确，并避免不必要地修改原列表。 |

| G9 | H45 | 2.5 | 2 | 3 | 2 | 2.5 | **12** | 指出 `+=` 非原子，但题面 B 只读不能造成丢行；修复代码也截断。 |

| G9 | P40 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G9 | S41 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G9 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G9 | X68 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G9 | Y76 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G10 | H45 | 5 | 5 | 5 | 5 | 5 | **25** | JSON 内容与严格输出要求全部满足。 |

| G10 | P40 | 5 | 5 | 5 | 5 | 5 | **25** | JSON 正确且无多余包装。 |

| G10 | S41 | 5 | 5 | 5 | 5 | 5 | **25** | 精确满足所需 JSON 结构。 |

| G10 | W87 | 5 | 5 | 5 | 2 | 3.5 | **20.5** | JSON 内容正确，但代码围栏违反“no prose around JSON”式硬输出约束。 |

| G10 | X68 | 5 | 5 | 5 | 2 | 3.5 | **20.5** | 内容正确，但代码围栏使输出不再是纯 API JSON。 |

| G10 | Y76 | 5 | 5 | 5 | 5 | 5 | **25** | 精确 JSON，格式完全合规。 |

| G11 | H45 | 4.5 | 4.5 | 4.5 | 0.5 | 2.5 | **16.5** | 技术基本正确且长度合规，但段首 A/T/O 而非 A/B/C，硬约束失败。 |

| G11 | P40 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G11 | S41 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G11 | W87 | 4 | 4 | 4 | 2 | 3 | **17** | 约 97 词且无禁词，但第三段从 O 开始；技术内容也略简化。 |

| G11 | X68 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G11 | Y76 | 5 | 5 | 5 | 5 | 5 | **25** | 三段依次 A/B/C、约 108 词、无禁词，TCP 关闭描述准确。 |

| G12 | H45 | 5 | 5 | 5 | 5 | 5 | **25** | 精确两行，所有数字 4 均正确替换。 |

| G12 | P40 | 5 | 5 | 5 | 5 | 5 | **25** | 格式和变换均完全正确。 |

| G12 | S41 | 3.5 | 4 | 4 | 3 | 4 | **18.5** | 漏掉 `42` 中的数字 4；其余顺序、两行和计数正确。 |

| G12 | W87 | 5 | 5 | 5 | 5 | 5 | **25** | 精确遵循转换和两行约束。 |

| G12 | X68 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G12 | Y76 | 5 | 5 | 5 | 5 | 5 | **25** | 输出严格且转换全部正确。 |

| G13 | H45 | 3.5 | 3 | 4 | 3.5 | 3.5 | **17.5** | 只问 bank 类别和时间，未确认具体 Tuesday/地点，并自行假定 nearest Tuesday。 |

| G13 | P40 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G13 | S41 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G13 | W87 | 3.5 | 3 | 4 | 4 | 3.5 | **18** | 两问数量合规，但未锁定具体 Tuesday 日期、确切时刻和最终地点。 |

| G13 | X68 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G13 | Y76 | 4 | 4 | 4 | 4 | 4 | **20** | 覆盖银行和 which Tuesday，但预设 after work，且地点仍未完全锁定。 |

| G14 | H45 | 5 | 5 | 5 | 5 | 4.5 | **24.5** | 四问诊断价值很高；第 4 问与第 1 问目标定义略有重叠。 |

| G14 | P40 | 4.5 | 4.5 | 4.5 | 5 | 4.5 | **23** | 问题有效，但缺直接询问 trace/profile 或耗时落点。 |

| G14 | S41 | 4 | 4 | 4 | 5 | 4 | **21** | 有目标、变更和影响，但缺负载触发与实际瓶颈位置两类关键问题。 |

| G14 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G14 | X68 | 5 | 5 | 4.5 | 5 | 5 | **24.5** | 四问结构很强，仅瓶颈问稍依赖已有观测数据。 |

| G14 | Y76 | 5 | 5 | 5 | 5 | 5 | **25** | 四个澄清问题高信息量且恰好满足数量要求。 |

| G15 | H45 | 4 | 5 | 4.5 | 5 | 4.5 | **23** | 前两项准确；Uranus 给 27–28/28，已落后于 2026 年的 29。 |

| G15 | P40 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G15 | S41 | 2 | 5 | 2.5 | 5 | 2.5 | **17** | 自由女神高度判断有明显错误，Uranus 27 也过时且置信过高。 |

| G15 | W87 | 3.5 | 5 | 4 | 5 | 4 | **21.5** | 前两项正确；Uranus 27 已过时，但不确定性表达较好。 |

| G15 | X68 | 3.5 | 5 | 4 | 5 | 4 | **21.5** | 前两项正确；Uranus 仍答 27，虽承认未来可能变化。 |

| G15 | Y76 | 3.5 | 5 | 4 | 5 | 4 | **21.5** | 前两项正确；把 27 称当前标准数量，事实已过时。 |

| G16 | H45 | 2.5 | 5 | 3.5 | 5 | 3 | **19** | 不确定性分层很好，但 Voyager 编号、速度、仪器状态有多处错误/过时。 |

| G16 | P40 | 2 | 4.5 | 3 | 5 | 2.5 | **17** | 态度诚实，但速度与仪器状态多处不准，current summary 可靠性不足。 |

| G16 | S41 | 1.5 | 4.5 | 2.5 | 5 | 2 | **15.5** | 多项仪器状态及通信叙述错误，虽承认知识截止。 |

| G16 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G16 | X68 | 4 | 4.5 | 4 | 4.5 | 4 | **21** | Voyager 1 恢复描述较好，但 Voyager 2“fully operational”等状态已过时。 |

| G16 | Y76 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G17 | H45 | 5 | 5 | 4.5 | 5 | 5 | **24.5** | 总体方案最稳；日程中休息与后续任务有 15 分钟重叠。 |

| G17 | P40 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G17 | S41 | 4 | 5 | 4 | 5 | 4 | **22** | 方案完整可做，但 aiosqlite 池、线程内存等技术表述有误/过度。 |

| G17 | W87 | 3.5 | 5 | 3.5 | 5 | 3.5 | **20.5** | 覆盖齐全，但 `gc.collect()`、额外依赖和离线 venv 可移植性较脆弱。 |

| G17 | X68 | 4.5 | 5 | 4 | 5 | 4.5 | **23** | Go+SQLite 方向好，但 Docker 和 SQLite 驱动/CGO 增添离线部署风险。 |

| G17 | Y76 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G18 | H45 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G18 | P40 | 2.5 | 3 | 3 | 3 | 2.5 | **14** | 选 X 有合理方向，但重解释题面速度关系、忽视 X 写慢基线，且末尾截断。 |

| G18 | S41 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G18 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G18 | X68 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| G18 | Y76 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |



\---



## CYBER — C1–C14



| Q | ID | C | Comp | R | IF | PU | Total | Locked justification |

|---|---|---:|---:|---:|---:|---:|---:|---|

| C1 | H45 | 4 | 5 | 4 | 5 | 4 | **22** | 主要缺陷齐全，但 `OR 1=1` 直接绕过后续密码比较/RCE 的影响略夸大。 |

| C1 | P40 | 3.5 | 4.5 | 3.5 | 5 | 3.5 | **20** | 抓到核心问题，但 timing 比较解释和枚举修复有误，SQLi 影响也略过度。 |

| C1 | S41 | 4 | 5 | 4 | 5 | 4 | **22** | 覆盖全面；输入验证不是 SQLi 核心修复，部分时序枚举表述略过度。 |

| C1 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C1 | X68 | 3 | 4 | 3.5 | 5 | 3.5 | **19** | SQLi/MD5 核心正确，但称 `OR 1=1` 可直接绕密码比较是实质错误。 |

| C1 | Y76 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C2 | H45 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C2 | P40 | 2.5 | 4 | 2.5 | 4 | 2.5 | **15.5** | 主栈溢出识别到，但额外 bug 判断和必然控制流劫持结论明显过度。 |

| C2 | S41 | 4.5 | 5 | 4.5 | 5 | 4.5 | **23.5** | 准确识别溢出、触发边界及现代缓解条件，仅轻微措辞可更谨慎。 |

| C2 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C2 | X68 | 3.5 | 4 | 3.5 | 4.5 | 3.5 | **19** | 核心 bug 和阈值正确，但把后果直接定为控制流劫持，缓解条件不足。 |

| C2 | Y76 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C3 | H45 | 5 | 5 | 5 | 5 | 5 | **25** | 三项真假、确认方式和风险语境都区分得很好。 |

| C3 | P40 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C3 | S41 | 4.5 | 5 | 4.5 | 5 | 4.5 | **23.5** | 三项分类基本准确；真实性与风险优先级还能分得更严格。 |

| C3 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C3 | X68 | 3.5 | 5 | 3.5 | 5 | 3.5 | **20.5** | #1 未确认真正 parameterization 就先判 FP；#3 真假与运维优先级有所混杂。 |

| C3 | Y76 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C4 | H45 | 4.5 | 5 | 5 | 5 | 4.5 | **24** | exploit primitive、控制流与权限边界讲得很清楚，仅少量环境假设。 |

| C4 | P40 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C4 | S41 | 4.5 | 5 | 4.5 | 5 | 4.5 | **23.5** | 正确识别 shell injection 与服务用户级影响；示例略依赖特定工具存在。 |

| C4 | W87 | 4 | 5 | 4 | 5 | 4 | **22** | 核心正确，但 `/bin/sh` 可用性等 caveat 表述不够严谨。 |

| C4 | X68 | 4.5 | 5 | 4.5 | 5 | 4.5 | **23.5** | 利用链与非 root 权限边界准确，仅有轻微系统工具假设。 |

| C4 | Y76 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C5 | H45 | 4 | 5 | 4 | 5 | 4 | **22** | 总体修复方向正确，但 stop-gap 存库转义易双编码，部分上下文示例不严谨。 |

| C5 | P40 | 1.5 | 4.5 | 2 | 5 | 1.5 | **14.5** | 关键错误：`Markup(user_input)` 会将不可信输入标安全，并可能保留 XSS。 |

| C5 | S41 | 3.5 | 5 | 3.5 | 5 | 3.5 | **20.5** | autoescape 主方向正确，但已存数据直接 escape 入库等会产生双编码/上下文问题。 |

| C5 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C5 | X68 | 2 | 4.5 | 2.5 | 5 | 2 | **16** | 关键实现错误：裸 `jinja2.Template` 默认不开 autoescape；Jinja 能力也被说得过强。 |

| C5 | Y76 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C6 | H45 | 4.5 | 5 | 4.5 | 5 | 4.5 | **23.5** | 时间线与异常识别好，也给合法替代解释；把 exfil 定为 most likely 略偏推断。 |

| C6 | P40 | 2.5 | 5 | 2.5 | 5 | 2.5 | **17.5** | 时间线完整，但推断 backup 删除/覆盖 config，日志证据不足。 |

| C6 | S41 | 3 | 5 | 3 | 5 | 3 | **19** | 重复下载识别正确，但进一步推测 tar/glob 删除 config 过度。 |

| C6 | W87 | 3 | 4.5 | 3 | 5 | 3 | **18.5** | 将第二次下载与 config 错误直接绑定，且异常信号综合不足。 |

| C6 | X68 | 3 | 4.5 | 3 | 5 | 3 | **18.5** | 将 download 扩展为 download/extraction 再推断覆盖 config，超出日志证据。 |

| C6 | Y76 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C7 | H45 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C7 | P40 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C7 | S41 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C7 | W87 | 3 | 4 | 3.5 | 5 | 3.5 | **19** | 承认 10.0.0.77 映射是弱推断，但主机到应用/数据库链仍未真正串证。 |

| C7 | X68 | 3.5 | 4 | 4 | 5 | 3.5 | **20** | 能指出 jump→app 的证据弱点并建议 flow logs，但仍假设 app-svc 参与 db brute-force。 |

| C7 | Y76 | 3 | 2.5 | 3 | 2.5 | 2.5 | **13.5** | plausible 链条有价值，但答案截断，缺最弱推断及新增日志源。 |

| C8 | H45 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C8 | P40 | 3.5 | 5 | 4 | 5 | 4 | **21.5** | 有效输入和数量级正确，但声称模 256 计数只差 1 的均匀近似不成立。 |

| C8 | S41 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C8 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C8 | X68 | 4 | 5 | 4 | 5 | 4.5 | **22.5** | 有效字符串和约 `10^11` 量级正确，但“几乎任意六字符都能补最后位”不严格。 |

| C8 | Y76 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C9 | H45 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C9 | P40 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C9 | S41 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C9 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C9 | X68 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C9 | Y76 | 5 | 5 | 5 | 5 | 5 | **25** | 正确识别数据与 `FLAG{` 前缀不相容，并正确说明已知明文推导。 |

| C10 | H45 | 4.5 | 5 | 4.5 | 5 | 4.5 | **23.5** | 工具映射清楚；Burp 对单表单未必绝对最小，个别操作稍超任务最窄范围。 |

| C10 | P40 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C10 | S41 | 4.5 | 5 | 4 | 5 | 4.5 | **23** | 三步覆盖完整，但单表单用 Python 脚本未必是最省工具方案。 |

| C10 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C10 | X68 | 5 | 4.5 | 4.5 | 5 | 4.5 | **23.5** | 两工具确实很精简，任务映射正确；部分选择理由略短。 |

| C10 | Y76 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C11 | H45 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C11 | P40 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C11 | S41 | 4.5 | 5 | 4.5 | 5 | 4 | **23** | containment/volatility 顺序基本正确；法院证据价值对 memory 的评价稍绝对。 |

| C11 | W87 | 4 | 5 | 4 | 5 | 3.5 | **21.5** | 先 review 再 preserve logs 的顺序不理想，memory 法律价值也说得过强。 |

| C11 | X68 | 3 | 5 | 3.5 | 5 | 3.5 | **20** | review/notify 放隔离之前延误 containment，且日志保存排序较晚。 |

| C11 | Y76 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C12 | H45 | 5 | 5 | 5 | 5 | 5 | **25** | 风险权衡、关联性确认和处置逻辑完整可靠。 |

| C12 | P40 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C12 | S41 | 5 | 5 | 4.5 | 5 | 5 | **24.5** | 相关性检查和风险权衡很强，只是“两项相关即隔离”略经验化。 |

| C12 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C12 | X68 | 4.5 | 5 | 4.5 | 5 | 4.5 | **23.5** | process lineage 检查很强；三级阈值合理，但三弱信号一律 monitor 略保守。 |

| C12 | Y76 | 5 | 5 | 4.5 | 5 | 5 | **24.5** | 相关性检查与误报/漏报不对称把握很好，仅阈值略规则化。 |

| C13 | H45 | 4 | 5 | 4.5 | 5 | 4.5 | **23** | STRIDE 覆盖和排序好；对已签名 OTA 绕过 likelihood 评得稍高。 |

| C13 | P40 | 3.5 | 5 | 3.5 | 5 | 3.5 | **20.5** | 结构完整，但多项威胁依赖题面未给出的弱 TLS/无认证/密钥存储假设。 |

| C13 | S41 | 3.5 | 4.5 | 3.5 | 5 | 3.5 | **20** | 覆盖五项，但签名绕过、默认弱凭据 likelihood 假设偏多。 |

| C13 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C13 | X68 | 4 | 5 | 4 | 5 | 4 | **22** | 覆盖较全面；仍有 local unauth/弱证书校验假设，但 OTA 根信任方向正确。 |

| C13 | Y76 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C14 | H45 | 4.5 | 5 | 4.5 | 5 | 4.5 | **23.5** | 清单及 effective-config 验证很强；部分后续措施在 key-only 后边际收益较低。 |

| C14 | P40 | 3.5 | 5 | 3.5 | 5 | 3.5 | **20.5** | 十项齐全，但 root-login 优先于 key-only，且 top 验证不足以证明 effective config。 |

| C14 | S41 | 3 | 5 | 3 | 5 | 3.5 | **19.5** | 改端口排第 3 收益很低，root 项验证方式也不能独立证明配置生效。 |

| C14 | W87 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |

| C14 | X68 | 4.5 | 4.5 | 4.5 | 5 | 4.5 | **23** | 七项精简且验证实际可用；firewall 范围稍泛，部分措施边际收益有限。 |

| C14 | Y76 | 0 | 0 | 0 | 0 | 0 | **0** | 固定预算内未交出 final answer。 |



\---



# PART 2 — DIVISION RESULTS



## GENERAL



Maximum possible: **450**.



| Rank | Contestant | Raw score | Maximum possible | Percentage | Answered | No-final |

|---:|---|---:|---:|---:|---:|---:|

| **1** | **H45** | **358.0** | 450 | **79.56%** | 16 | 2 |

| **2** | **Y76** | **290.0** | 450 | **64.44%** | 12 | 6 |

| **3** | **S41** | **284.0** | 450 | **63.11%** | 13 | 5 |

| **4** | **X68** | **269.5** | 450 | **59.89%** | 12 | 6 |

| **5** | **W87** | **220.5** | 450 | **49.00%** | 10 | 8 |

| **6** | **P40** | **202.5** | 450 | **45.00%** | 9 | 9 |



## CYBER



Maximum possible: **350**.



| Rank | Contestant | Raw score | Maximum possible | Percentage | Answered | No-final |

|---:|---|---:|---:|---:|---:|---:|

| **1** | **X68** | **271.0** | 350 | **77.43%** | 13 | 1 |

| **2** | **S41** | **242.0** | 350 | **69.14%** | 11 | 3 |

| **3** | **H45** | **211.5** | 350 | **60.43%** | 9 | 5 |

| **4** | **P40** | **130.0** | 350 | **37.14%** | 7 | 7 |

| **5** | **W87** | **81.0** | 350 | **23.14%** | 4 | 10 |

| **6** | **Y76** | **63.0** | 350 | **18.00%** | 3 | 11 |



\---



# PART 3 — OVERALL RESULTS



Maximum possible: **800**.



| Overall rank | Contestant | Total score | Max possible | Percentage | General rank | Cyber rank |

|---:|---|---:|---:|---:|---:|---:|

| **1** | **H45** | **569.5** | 800 | **71.19%** | **1** | **3** |

| **2** | **X68** | **540.5** | 800 | **67.56%** | **4** | **1** |

| **3** | **S41** | **526.0** | 800 | **65.75%** | **3** | **2** |

| **4** | **Y76** | **353.0** | 800 | **44.12%** | **2** | **6** |

| **5** | **P40** | **332.5** | 800 | **41.56%** | **6** | **4** |

| **6** | **W87** | **301.5** | 800 | **37.69%** | **5** | **5** |



No tie-break was required.



## LOCKED DELIVERY COUNTS



| Contestant | Answered / 32 | No-final / 32 | Delivery rate |

|---|---:|---:|---:|

| H45 | 25 | 7 | 78.13% |

| X68 | 25 | 7 | 78.13% |

| S41 | 24 | 8 | 75.00% |

| Y76 | 15 | 17 | 46.88% |

| P40 | 16 | 16 | 50.00% |

| W87 | 14 | 18 | 43.75% |



\---






| Contestant | General | General rank | Cyber | Cyber rank | Overall | Overall rank |

|---|---:|---:|---:|---:|---:|---:|

| **H45** | **358.0 / 450** | **#1** | **211.5 / 350** | **#3** | **569.5 / 800** | **#1** |

| **X68** | **269.5 / 450** | **#4** | **271.0 / 350** | **#1** | **540.5 / 800** | **#2** |

| **S41** | **284.0 / 450** | **#3** | **242.0 / 350** | **#2** | **526.0 / 800** | **#3** |

| **Y76** | **290.0 / 450** | **#2** | **63.0 / 350** | **#6** | **353.0 / 800** | **#4** |

| **P40** | **202.5 / 450** | **#6** | **130.0 / 350** | **#4** | **332.5 / 800** | **#5** |

| **W87** | **220.5 / 450** | **#5** | **81.0 / 350** | **#5** | **301.5 / 800** | **#6** |



These values are the frozen Formal D blind-evaluation results.



The scores were locked **before contestant identity mapping was revealed**. Any later contestant-to-model mapping may be used only to interpret the already-frozen results and **must not be used to modify any original score, half-point, subtotal, percentage, division rank, or overall rank**.



# SCORES LOCKED.