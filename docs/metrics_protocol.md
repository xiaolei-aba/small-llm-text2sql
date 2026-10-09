# 统一结果记录协议

`results/metrics.csv` 一行对应一次真实模型运行与一个评测 split，唯一键为 run_id + split。Day 0 时仅有 header；当前已包含真实完成运行，状态见results/metrics.csv。未运行不建假行；未测或不适用留空，0 仅表示实测零。失败运行 status=failed，notes 说明故障；不得将部分评测标为完整成功。

## 质量与分母

- execution_accuracy：固定官方 evaluator 在原始单库上通过的样本数 / 完整 manifest 的 eval_samples，范围 [0,1]。生成失败、无 SQL、SQL 错误、执行超时计错，不能从分母删除。
- test_suite_accuracy：独立字段；只有用实际 test-suite 多数据库评测时填写。不得将单库 EX 改名 TSA。
- exact_match：固定官方解析与结构匹配口径，不是纯字符串相等。
- valid_sql_rate：单个模型输出能在对应数据库以只读查询成功执行且未超时的比例；能执行不保证正确，不能替代 EX。
- easy_accuracy / medium_accuracy / hard_accuracy / extra_hard_accuracy：按固定官方 hardness（gold SQL 结构）分桶的 EX；同时记录各桶 samples。空桶留空，不写 0；不按问题字数或主观感受分难度。
- 数据缺失或 gold 无法执行属于数据协议问题，先阻止完整运行并修复；确需排除必须生成统一新 manifest，向所有对照应用并报告排除数量，不能按模型结果过滤。
- 不把空输出换成 SELECT 1 后计为正确。需要占位维持行对齐时单独记录 failure mask 并强制计错。断点恢复的指标从全部记录重新聚合。

官方上游：[Spider](https://github.com/taoyds/spider)、[test-suite-sql-eval](https://github.com/taoyds/test-suite-sql-eval)。E0已固定版本并实现官方纯比较函数的受限执行适配（详见docs/prompt_protocol.md）；eval_protocol 必须说明 `single_db_ex` 或 `test_suite`，不能混用数字。官方当前指标说明见 [Spider 网站](https://yale-lily.github.io/spider)。

## 资源与计时

- peak_vram_gb：测量阶段内 `max_memory_allocated` / 1e9（十进制 GB）；peak_reserved_vram_gb 同口径。CUDA 同步并在阶段前重置峰值统计；注明训练还是推理，不将两者混合。nvidia-smi 进程/设备占用另存 profile，与 allocated 不等价。
- train_time：秒；从第一个训练 step 开始到最后一个 step 完成，含前后向与 optimizer，排除下载、预处理、模型初次加载、最终保存及评测。notes 记录 checkpoint/日志开销，必要时另存端到端时间。
- latency：毫秒，warmup 后从已构造好的问题/schema 开始，含 tokenize、生成和 decode，排除模型加载、SQL 执行与评测；mean，与 p50/p95 同一批请求。GPU 前后同步，保留逐请求记录。
- throughput：输出 token/s，全部输出 token / 整个测量窗口墙钟秒数；不含输入 token；并发不能用各请求用时相加作分母。requests_per_second 另记。
- benchmark_requests、generated_tokens、concurrency、backend、dtype、max_new_tokens 都要记录。warmup 数、prompt 长度分布、供电/其他进程及计时范围放 config/profile；不同负载数字不能直接比较。

## 复现与训练预算

train_samples 是唯一训练样本数；train_examples_seen 是含重复采样的暴露次数；train_tokens_seen 是实际非 padding 训练 token 数（需注明 SQL-only 监督 token 可另存），三者不同。E0 确实执行后 train_samples 可记 0，不提前填占位行。

model_revision、dataset_revision、manifest SHA256、seed、LoRA 参数、目标模块、optimizer、序列长度、micro-batch、梯度累积、steps、prompt/schema 版本、eval commit、项目 git commit、环境清单、config、predictions 引用均须可追溯。

一份预测记录至少含 example_id、db_id、split、difficulty、raw_output、predicted_sql、gold_sql（仅离线评测侧）、generation_status、error_type、elapsed_ms、prompt/output token 数、EX 与 valid 标志。推理 prompt 严禁包含 gold SQL。

分层比较给出桶大小及配对差值；样本 bootstrap CI 与多 seed 波动分别解释。小规模 smoke 只能验证通路，不能作为全量精度结论。

## 当前实现的显存测量窗口

显存统计范围：训练代码在模型加载、最长样本预检查之后重置peak计数，再测正式训练循环（包括optimizer状态的首次分配）。未单独测量加载/预检查的历史峰值；reserved仍可能包含此前缓存。allocated不是整个GPU进程的总占用，也不能据此宣称只需同等物理显存即可完成全流程。

完整E0/E1/E3/E4生成脚本在加载前重置peak，逐条记录的峰值可能包含加载/预热；E5在每条件预热后重置peak，用于独立benchmark。两个窗口不同，不能混在一起宣称某种后端减少了同一口径的峰值。
