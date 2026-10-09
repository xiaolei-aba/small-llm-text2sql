# E0 Zero-shot Baseline 实测报告

正式1034条dev推理与评分均退出0。Qwen/Qwen2.5-Coder-1.5B-Instruct，BF16非量化，单张RTX5060 Laptop，batch1。没有训练、没有gold prompt、没有few-shot。

单库 EX：50.7737%（525/1034）；可执行率：70.5029%（729/1034）。零生成失败、零输出到达256 token上限。

|难度|样本数|EX|
|---|---:|---:|
|easy|248|66.5323%|
|medium|446|50.8969%|
|hard|174|37.3563%|
|extra_hard|166|40.9639%|

平均请求生成延迟 1197.07 ms，p50 1231.05 ms，p95 2168.87 ms；生成阶段吞吐 33.53 token/s。峰值 allocated 3.221 GB，reserved 3.284 GB。模型加载 4.11 秒，独立于逐请求计时。

定义与局限：固定官方 result_eq 比较原始单库结果，保留DISTINCT且不plug values；不是TSA，不报告EM。详细规则、继承的repetition_penalty=1.1、安全限制及解码约定见 docs/prompt_protocol.md。速度不包含SQL评测，输出长度不同会影响阶段间速度比较。

复现命令见 docs/reproduce.md。完整预测本地保留、Git忽略；汇总与逐条评分受版本管理。
预测SHA256：faffd9309e8631d45121fab3ff0eaca083540f1bd742cd329d4f09b8e0debcad
生成代码版本：e321327aa11d118b7729f1afb8fe5abafd90efc0；生成入口文件SHA256：769bb10d873a558518f5476817bbcba7aa13db134d6e9aafa8eaad164417bb17。评分代码在2a3fb57（其后尚未提交变化只涉及文档/测试/包说明）。

Smoke：固定10条EX4/10、可执行6/10，仅工程检查，不用于估计整体效果或调Prompt。正式生成/评分均完整覆盖manifest，分母未删样本。

解释：约一半问题的结果匹配；能运行的SQL仍可能错表、错列、错条件。Hard/extra准确率较低，但先完成E1，再结合E2决定优化；不能仅凭难度分层就断言复杂度是唯一原因。

下一步：E1配置已在完整E0评分前写定；7000 train、438 steps、rank8/alpha16，SQL-only，2304最大训练长度，独立adapter。
