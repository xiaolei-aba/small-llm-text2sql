# 项目总报告

状态：全部计划内本机实验已完成。
生成观察时间UTC：2026-10-08T16:49:39.747015+00:00；生成前仓库HEAD：`44411156bbd00154d90ce216ca41cca1e447d2f1`。

## 目标与设备

在单张RTX5060 Laptop（8151MiB）上，研究Qwen2.5-Coder-1.5B-Instruct的跨库Text-to-SQL后训练与推理成本。基础模型固定，不改用更大模型。独立Conda text2sql / Python3.11.16 / PyTorch2.11.0+cu128 / Transformers4.57.6 / PEFT0.18.1；E4新增bitsandbytes0.47.0，未替换Torch。完整依赖见environment_e0.txt、environment_e1.txt、environment_e4.txt；E5实际环境见其报告。

## 数据与评测

Spider1.0：7000条train_spider（140库）、1034条dev（20库），库交集0；166库审计通过。没有内部train_val、额外训练数据或dev Gold混入训练。原ZIP哈希、官方来源和CC BY-SA4.0许可见[data_audit.md](data_audit.md)。4个Windows不兼容ZIP成员不是训练JSON或SQLite缺失，已如实记录；键标注差异保留。

统一完整schema（表/列/SQLite声明类型/Spider PK与FK）、固定零样本Prompt、greedy+repetition_penalty1.1、最多256输出token。Gold只用于训练集监督和离线dev评分/分析，不用于dev Prompt或筛表列。主指标是锁定官方result_eq纯函数适配的原始单库EX，保留DISTINCT、无Gold值填充；不是TSA或Exact Match。只读数据库、查询/进程期限与结果资源限制统一应用。

## 全量dev质量（同一1034条）

|运行|EX|正确条数|可执行率|easy|medium|hard|extra-hard|
|---|---:|---:|---:|---:|---:|---:|---:|
|e0_dev|50.77%|525/1034|70.50%|66.53%|50.90%|37.36%|40.96%|
|e1_dev|69.15%|715/1034|88.97%|86.69%|70.18%|57.47%|52.41%|
|e3_dev|70.21%|726/1034|88.01%|87.10%|71.52%|59.77%|52.41%|
|e4_dev|68.96%|713/1034|87.62%|86.69%|70.63%|56.32%|51.20%|

E2是离线错误分析，不是新模型运行，因此没有虚构E2准确率行。E4只有完整评分存在时才进入上表。

## 训练资源与控制变量

|运行|训练分钟|输入token/s|峰值allocated GB|峰值reserved GB|样本/步数|
|---|---:|---:|---:|---:|---|
|e1_dev|49.02|1027.94|4.516|7.539|7000/438|
|e3_dev|49.43|1019.43|4.518|4.891|7000/438|
|e4_dev|62.17|810.42|3.213|3.764|7000/438|

E1/E3/E4保持7000条、相同顺序、3,023,191输入token、226,130监督token、438步；rank8、alpha16、dropout0.05、micro1/累积16、相同AdamW与学习率调度。E3只改复杂度loss权重；E4用均匀目标并改变底座量化与标准kbit dtype准备。9,232,384个可训练LoRA参数，七类线性层。

计时是训练循环，不含下载/预处理/加载/预检查/最终保存/评测。E1为修复计数字段曾从200步恢复，额外丢弃32.100837秒单列，未记录半步耗时未知。E1恢复前reserved约4.891GB，恢复后峰值7.539GB；缓存历史不同，不能把E3较低reserved归因为算法收益。GB采用1e9字节，allocated不等于nvidia-smi总占用。训练peak在加载/预检查后重置，不含其历史峰值；不可把该数值当作整个流程的物理显存需求。

## 核心实现与真实结论

- 数据/输入：确定性schema、锁定模型tokenizer与数据哈希，完整问题/schema输入，无Gold线索。
- 训练：SQL/EOS-only labels、padding屏蔽与因果移位；仅监督位置计算词表logits，loss/梯度等价性测试；非重入梯度检查点与累积。
- 恢复：optimizer、adapter、CPU/CUDA RNG与固定顺序；E1真实恢复后201–205步loss/梯度范数和旧轨迹相同，不只验证文件能打开。
- 评测：安全只读执行、完整分母、官方比较适配、逐条预测/评分及哈希；训练loss不替代EX。
- E1取得主要收益：EX50.77%→69.15%，+18.38个百分点；248条改对、58条改错。
- E3的复杂度loss权重为hard/extra原始2、其他1，全局均值归一化。EX69.15%→70.21%，+1.06个百分点；32改对、21改错。hard+extra从55.00%→56.18%，但valid88.97%→88.01%。20库聚类95%区间[-0.31,+2.49]个百分点包含0，不能声称稳定显著收益。

E4状态：完整训练和全量dev评测已完成。
E4相对E1：allocated峰值降低28.86%，训练循环耗时比1.268x，EX变化-0.19个百分点。量化后训练和推理均使用同一NF4底座；该质量差异同时包含量化训练与推理的作用，并非只隔离推理量化误差。

## E5本机推理对照

固定32个按输入长度选出的请求，每条件3轮；质量只评第一轮32条，不能与上面的1034条EX混比。

|条件|32条EX|平均完成延迟ms|输出token/s|峰值allocated GB|
|---|---:|---:|---:|---:|
|e5_bf16_b1|43.75%|1283.93|32.40|3.221|
|e5_bf16_b2|43.75%|1703.95|48.60|3.251|
|e5_fp16_b1|43.75%|1283.43|32.29|3.222|
|e5_fp16_b2|43.75%|1589.11|52.15|3.253|
|e5_lora_unmerged_b1|56.25%|1742.46|18.44|3.259|
|e5_lora_merged_b1|56.25%|937.61|34.30|3.221|

同E1 adapter合并/未合并的输出吞吐比为1.860x；首轮原始输出变化2/32，改对0、改错0。不能据此证明全量质量无损或通用加速倍数。

batch成员延迟等于整个batch返回时间，不除以batch；吞吐分母只累计各batch墙钟一次。加载与逐请求时间分开，生成时间含tokenize/generate/decode，不含SQL评分。三轮波动、reserved、p95及加载时间见[e5_report.md](e5_report.md)与metrics.csv。

本项目未运行vLLM、未部署服务、未安装WSL/Docker，也不声称做到这些。E5使用原生Transformers SDPA。

## 典型错误与负结果

- dev:6：E1仍把singer.song_name放到singer_in_concert别名下，产生不存在的列。
- dev:54：E3把Dog改为dog而通过，JOIN结构没有改变；hard桶收益并不全是复杂结构推理收益。
- dev:64：E3把pettype写成pet_type，从E1正确退化为执行失败。
- dev:48：Gold未过滤dog，但原库最年轻宠物恰是dog；单库结果相等不能证明所有数据状态下逻辑等价。未修改Gold或原库。

详细SQL与解释见[e0_case_walkthrough.md](e0_case_walkthrough.md)、[e3_interpretation.md](e3_interpretation.md)、[evaluation_limitations.md](evaluation_limitations.md)。自动错误标签多标签重叠、可能漏检/误标，不是人工真值。

## 限制

单个训练seed；20个dev数据库；dev参与E3方向选择；底座预训练是否见过Spider未知；单库EX允许数据巧合、空结果匹配及官方列顺序置换；没有TSA/EM或独立最终测试。资源实测是本机一次运行，频率/温度/缓存历史影响时间和reserved。E5小集合诊断不能证明全量质量。LoRA/QLoRA/官方评测器不是原创；项目贡献是工程实现、受控实验与真实分析。

## 复现与证据索引

唯一解释器：`python`。完整命令见[reproduce.md](reproduce.md)；运行前核对agent_progress.md和活跃进程，不重复成功实验。配置在configs，固定样本与顺序在data/manifests，真实统一指标在results/metrics.csv。原始预测、模型、adapter/checkpoint本地保留但Git忽略，不上传远端。

每阶段summary关联预测SHA256，训练报告关联adapter SHA256、代码commit和配置；Git工作是本地提交。最近一次完整测试在E4依赖安装后通过17项，包括只读执行、schema、监督mask、梯度等价、恢复、权重控制和加载策略；具体错误与修复见engineering_log.md。

## 简历与面试入口

简历只使用[resume_bullets.md](resume_bullets.md)中的已完成条目。先阅读[learning_guide.md](learning_guide.md)，能解释问题/schema/Gold边界、SQL-only loss、LoRA参数量、QLoRA数据类型、EX与TSA、控制变量、bootstrap及负结果，再使用项目经历。项目故事线见[project_story.md](project_story.md)。
