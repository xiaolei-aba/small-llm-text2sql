# Efficient Post-Training of Small LLMs for Complex Text-to-SQL

**面向复杂 Text-to-SQL 的小参数大模型高效后训练与推理优化**

在单张 **RTX 5060 Laptop（8151 MiB，约8GB）** 上，使用固定的 **Qwen2.5-Coder-1.5B-Instruct**，研究普通LoRA、复杂度加权和QLoRA如何影响跨数据库SQL生成质量与资源开销。项目包含真实实验、失败案例与可追溯记录；LoRA/QLoRA本身不是原创算法。

E0–E4及原生Transformers E5已完成。本目录为独立公开候选快照，不包含研究仓库Git历史；旧报告中的commit仅标识私有研究版本。发布前检查见[PUBLIC_RELEASE_REPORT](PUBLIC_RELEASE_REPORT.md)。目前尚未创建远端或发布；所有者授权的项目代码采用[Apache-2.0](LICENSE)，具体范围见[LICENSE_SCOPE](LICENSE_SCOPE.md)，第三方与数据材料许可见[声明](THIRD_PARTY_NOTICES.md)。

## 问题与资源约束

输入自然语言问题与目标数据库完整schema，输出SQLite SQL。Spider训练与dev数据库不重叠，模型需要把问题中的概念对应到未用于本项目SFT的表、列与连接关系。选择1.5B模型，使BF16 LoRA能在本机运行，并测量量化是否值得其时间与质量代价。

- 数据：Spider 1.0，7000条train_spider/140库，1034条dev/20库，db_id交集为0；全部166个标注数据库完成审计。
- 输入：完整表/列/声明类型/键关系，不提供数据库行值；dev Gold SQL不进Prompt、不用于选择表列。
- 环境：独立Conda `text2sql`，Python3.11.16、PyTorch2.11.0+cu128、Transformers4.57.6、PEFT0.18.1；E4使用bitsandbytes0.47.0。
- 显存：监督位置logits、梯度检查点、micro-batch1/累积16；训练峰值allocated不是整个GPU进程的物理显存需求。

## 实验与真实结果

以下均为同一完整1034条dev的**原始单库Execution Accuracy（EX）**，不是Test Suite Accuracy、Exact Match或Spider排行榜成绩。

|阶段|方法/作用|EX|可执行率|训练循环分钟|训练峰值allocated GB|
|---|---|---:|---:|---:|---:|
|E0|Zero-shot BF16底座|50.77%|70.50%|—|—|
|E1|7000条SQL-only LoRA SFT|69.15%|88.97%|49.02|4.516|
|E2|E0/E1错误分析，选择一个优化假设|分析阶段，无新模型|—|—|—|
|E3|hard/extra样本loss加权|70.21%|88.01%|49.43|4.518|
|E4|均匀loss、NF4双重量化QLoRA|68.96%|87.62%|62.17|3.213|

E1/E3/E4同样本、顺序、3,023,191输入token、226,130监督token、438步；r8/alpha16/dropout0.05，固定预算结束adapter。每次完整推理均无生成失败/截断。数字来自[统一指标](results/metrics.csv)和[总报告](docs/final_report.md)，没有采用参考项目结果。

**有效与无效的部分都保留：**

- E1相对E0提升18.38个百分点，是主要质量收益。
- E3相对E1仅+1.06个百分点，32条改对、21条改错；可执行率下降，20库聚类95%区间[-0.31,+2.49]个百分点包含0，收益不稳定，不能声称稳定显著提升。
- E4训练allocated下降28.86%，但耗时增加26.84%，EX净少正确2条；不能描述为同时提速或量化无损。训练和推理都使用量化底座，未隔离二者的误差。
- E1为修复日志计数从200步恢复，额外32.100837秒重算单列；reserved受缓存历史影响，不能把reserved差值归因于算法。

## E5：原生推理对照

固定32条按输入长度选出的请求，每条件3轮；质量仅取首轮32条，速度取96次请求。**未运行vLLM、未部署推理服务。**

|条件|32条EX|平均完成延迟ms|输出token/s|
|---|---:|---:|---:|
|底座BF16 batch1|43.75%|1283.93|32.40|
|底座BF16 batch2|43.75%|1703.95|48.60|
|底座FP16 batch1|43.75%|1283.43|32.29|
|底座FP16 batch2|43.75%|1589.11|52.15|
|同E1 LoRA未合并，BF16 batch1|56.25%|1742.46|18.44|
|同E1 LoRA已合并，BF16 batch1|56.25%|937.61|34.30|

合并后本次吞吐为1.86倍，但2条原始输出改变；32条总分相同不证明全量无损。batch提高吞吐同时可能增加完成延迟，FP16 batch1本次没有提速。三轮波动及配对结果见[E5报告](docs/e5_report.md)。

## 快速理解与复现

**本仓库不包含原始数据、基础权重、adapter、checkpoint或原始预测。** 保留配置、哈希、样本清单、训练报告、逐条评分及汇总，其他人需从官方获取数据/模型后重新运行。当前GPU/平台只验证了上述Windows环境，不承诺其他硬件逐位一致。

1. 阅读[公开复现指南](docs/reproduce_public.md)，在独立新副本中隔离作者已发布结果，避免旧run记录混入新实验。
2. 创建Python3.11的Conda `text2sql`，安装固定依赖，执行真实CUDA检查。
3. 从[Spider官网](https://yale-lily.github.io/spider)下载数据；从[Qwen官方固定revision](https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct/tree/2e1fd397ee46e1388853d2af2c993145b0f1098a)获取模型；校验本项目版本哈希。
4. 恢复锁定官方评测源码与许可，完成审计和测试，再按[E0–E5命令](docs/reproduce.md)执行。

未经准备不要直接在作者现有工作区运行下载/训练命令。审计本身没有重新训练或下载权重。

```text
configs/                 固定实验、模型与评测版本
src/data/                schema与Prompt
src/train/               SQL-only编码、加权与batch
src/evaluation/          官方比较适配、只读SQLite执行
scripts/                 数据审计、训练、推理、评分和报告
data/manifests/         样本、顺序与版本证据
results/                 真实训练/评测记录（大产物忽略）
docs/                    复现、方法、错误、学习和发布审计
LICENSES/                实际使用的第三方许可副本
```

## 失败分析与结论边界

典型错误包括列属于错误表、JOIN改变答案、SQLite方言不匹配、聚合/嵌套查询错误。E3有些hard样本改进只是值大小写或选列修正，不证明复杂推理普遍增强。单个原库上结果相同也可能是空结果或数据巧合，不保证逻辑等价，详见[评测局限](docs/evaluation_limitations.md)。

只有一个训练seed；dev用于E3方向选择，后续结果是探索性的；没有独立最终测试或多库TSA；未知底座预训练是否接触Spider。资源数字为本机测量，时间含义与显存窗口见[指标协议](docs/metrics_protocol.md)。

## 来源、许可与阅读入口

Spider数据为CC BY-SA 4.0；上述Qwen版本及两套官方评测代码为Apache-2.0。参考仓库只作为思路来源，未把其代码或结果当作原创；项目工程为AI辅助实现。具体归属、引用与数据摘录许可见[THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md)。根Apache-2.0仅适用于有权授权的项目代码；Spider材料和第三方许可保留独立边界。

- [完整实验报告](docs/final_report.md) · [失败分析](docs/e3_interpretation.md) · [QLoRA权衡](docs/e4_interpretation.md)
- [学习与面试指南](docs/learning_guide.md) · [简历素材](docs/resume_bullets.md)
- [发布报告](PUBLIC_RELEASE_REPORT.md) · [文件清单](PUBLIC_FILE_MANIFEST.json)
