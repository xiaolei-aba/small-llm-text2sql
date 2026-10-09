# e0_dev → e1_dev 实测对照

同一固定 1034 条 Spider dev、完整 schema、零样本任务 Prompt、greedy 生成（repetition_penalty=1.1）及只读单库 EX。只评预算结束的 adapter，未按 dev 挑 checkpoint。

|指标|e0_dev|e1_dev|变化|
|---|---:|---:|---:|
|execution_accuracy|50.77%|69.15%|+18.38 百分点|
|valid_sql_rate|70.50%|88.97%|+18.47 百分点|
|easy_accuracy|66.53%|86.69%|+20.16 百分点|
|medium_accuracy|50.90%|70.18%|+19.28 百分点|
|hard_accuracy|37.36%|57.47%|+20.11 百分点|
|extra_hard_accuracy|40.96%|52.41%|+11.45 百分点|
|hard+extra-hard 合并（340条）|39.12%|55.00%|+15.88 百分点|
|generation_failures|0.000|0.000|+0.000|
|truncated_outputs|0.000|0.000|+0.000|
|latency|1197.068|1671.544|+474.476|
|latency_p95_ms|2168.872|3582.919|+1414.047|
|throughput|33.533|19.156|-14.377|
|peak_vram_gb|3.221|3.259|+0.038|
|peak_reserved_vram_gb|3.284|3.343|+0.059|

Latency 单位 ms/request；throughput 为输出 token/s，计时不含模型加载和 SQL 评分。显存单位十进制 GB；reserved 包含缓存。模型输出长度可能不同，因此全量生成速度差异不能完全归因于加载后端。

## 配对结果

改对 248 条、改错 58 条。20个数据库聚类bootstrap的总体EX差值95%区间为 [+13.60, +24.34] 个百分点（10000次，seed42）。
完整错误诊断与案例：docs/e2_error_analysis.md；这是多标签启发式，不是确定因果。

## e0_dev 证据
- 预测 SHA256：`faffd9309e8631d45121fab3ff0eaca083540f1bd742cd329d4f09b8e0debcad`。
- 原始输出：`results/predictions/e0_dev.jsonl`；逐条评分：`results/e0_dev_evaluation.jsonl`；汇总：`results/e0_dev_summary.json`。
- 输出 token：41506；生成代码 commit：`e321327aa11d118b7729f1afb8fe5abafd90efc0`。

## e1_dev 证据
- 预测 SHA256：`d66f13c6b294c90c831b455cc6cd338f408ce1a51e934879beea5f9a16d348a3`。
- 原始输出：`results/predictions/e1_dev.jsonl`；逐条评分：`results/e1_dev_evaluation.jsonl`；汇总：`results/e1_dev_summary.json`。
- 输出 token：33109；生成代码 commit：`399d919137ad18ad19e0a69a6510c388ce9c4766`。
- 训练 7000 条曝光 / 7000 唯一样本 / 438 步；序列 token 3023191，监督 token 226130。
- 训练循环 2941.031 秒；allocated 4.516 GB；reserved 7.539 GB。
- adapter SHA256：`8e2ce45a04a2161438dec1a8806b67cd1a56702b14a9afcfb1fb2fed7f96e002`；训练配置与恢复历史：`results/e1_lora_seed42_training.json`。
- 训练曾恢复：计时排除停机与丢弃步骤。额外成本与恢复证据见训练报告，不把保留轨迹时间当作全部项目耗时。

## 解释范围

这是单个训练 seed、固定模型与 20 个 dev 数据库上的比较。单库 EX 可能因空结果或当前数据巧合判相等，不是 Test Suite Accuracy 或 Exact Match。官方难度是结构标签，不保证对具体模型单调。dev 参与优化方向选择后，后续结论为探索性；数据库聚类 bootstrap 也不能消除方法选择偏差或衡量训练 seed 方差。

错误类别、配对改进/退化及数据库聚类区间由 scripts/analyze_errors.py 的对应报告补充；不要把训练 loss 或自动词法诊断当作准确率或确定因果。
