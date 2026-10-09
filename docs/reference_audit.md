# 三个参考仓库审计

2026-09-29：三个远端均可访问。当前空工作区没有本地仓库；通过 GitHub API 树和固定 commit 的 raw 源码只读核实，未 clone、未运行、未修改任何参考项目。没有对所有文件逐行验证；下面区分源码事实、作者报告和我们的设计判断。未复现实验，因此所有上游结果仅属于作者。

## 1. Gansaw98/text-to-sql-spider

[仓库](https://github.com/Gansaw98/text-to-sql-spider)，审计版本 `71b6b083cf27d2da562a51dd4d7b5faac664cee8`。

| 维度 | 已核实内容 |
|---|---|
| 目录 | training/（notebook）、evaluation/、deployment/、results/、requirements.txt |
| 数据入口 | training/text-to-sql.ipynb：load_dataset("xlangai/spider")，读取 tables.json，构建 prompt/completion；按 1024 token 上限过滤 |
| 训练入口 | 同一 notebook 的 SFTTrainer；包含 Kaggle secrets、安装命令、训练后自动上传 Hub，不能直接整体执行 |
| 评测入口 | evaluation/finetuned_eval.py 生成；evaluation/evaluation.py 和 process_sql.py 为仓库附带的 Spider 评测代码；groq_baseline.py 为远端 API 对照 |
| schema | evaluation/schema_utils.py 的 build_schema_index/get_schema_prompt；原表列名、类型映射、行内 PRIMARY KEY 和 FK 注释构造 CREATE TABLE 风格 prompt |
| 模型 | Qwen2.5-Coder-7B-Instruct；作者以 Groq Llama 3.3-70B 作 zero-shot 对照，并非同底座 SFT 消融 |
| 配置 | 4-bit NF4、double quant、FP16 compute；r=16、alpha=32、dropout=0.05，q/k/v/o/gate/up/down 投影；2 epochs、LR=2e-4、batch=2、累积=8、paged_adamw_8bit、completion_only_loss=True |
| 指标 | 作者报告官方 EX/EM 与难度分层；sql_executor.py 是另一个快速执行比较，不应充当官方主指标 |

关键来源：[schema_utils.py](https://github.com/Gansaw98/text-to-sql-spider/blob/71b6b083cf27d2da562a51dd4d7b5faac664cee8/evaluation/schema_utils.py)、[训练 notebook](https://github.com/Gansaw98/text-to-sql-spider/blob/71b6b083cf27d2da562a51dd4d7b5faac664cee8/training/text-to-sql.ipynb)、[sql_executor.py](https://github.com/Gansaw98/text-to-sql-spider/blob/71b6b083cf27d2da562a51dd4d7b5faac664cee8/evaluation/sql_executor.py)、[推理入口](https://github.com/Gansaw98/text-to-sql-spider/blob/71b6b083cf27d2da562a51dd4d7b5faac664cee8/evaluation/finetuned_eval.py)。

值得参考：db_id 索引、显式 schema、训练/推理模板一致性、逐样本记录与官方 scorer 的分工。

需重写：统一配置与路径、可恢复预测统计、数据超长策略、只读执行与超时、完整评测封装。源码的 busy_timeout 是 SQLite 锁等待，并不是查询运行时间上限；普通 sqlite3.connect 不是只读连接。快速比较对结果字符串 lower/sort，会改变大小写/排序语义。空预测替为 SELECT 1 也需防止误计正确。PK 格式应考虑复合键和标识符转义。不能照抄 notebook 的自动上传步骤。

特别注意：这是量化底座 + LoRA，即 QLoRA，不能作为我们的普通 16-bit LoRA 基线。README 提及的 training/_measure_lengths.py 不在审计版本树中，不能把它列作已存在入口。

不归属我们：作者全部 EX、EM、分难度结果、与 70B 的差值、训练耗时、可训练参数数值、保存的预测 SQL 及上传 adapter。今天一项也未复现。

许可：此版本根目录未见 LICENSE，直接移植代码前需核实授权；本次只参考设计，未复制实现。官方评测器应直接追溯官方上游而非把此副本当唯一依据。

## 2. thdwhtls/Execution-Guided-Text-to-SQL-Post-Training

用户只给项目名，经搜索定位到[此仓库](https://github.com/thdwhtls/Execution-Guided-Text-to-SQL-Post-Training)；若用户原指不同 owner，应重新核对。审计版本 `4ada9b4f4c637528346cf1011954c624d8c6518a`。

| 维度 | 已核实内容 |
|---|---|
| 目录 | text2sql_trajectory_builder.py、training/、scripts/、analysis/、experiments/、outputs_key/ |
| 数据入口 | builder 的 read_json_or_jsonl、resolve_db_path、rollout_example；scripts/make_demo_dataset.py 是演示入口 |
| 训练入口 | training/train_lora_sft.py 与 train_lora_dpo.py；读取 trajectories 或偏好 pairs |
| 评测入口 | 同一个 builder 生成/执行并 summarize；analysis/ 含错误、repair、pair quality、schema retrieval 等报告工具 |
| schema | SQLite sqlite_master 与 PRAGMA table_info/foreign_key_list；full/retrieved/bm25/bm25_fk，top_k_tables 默认 6，FK 扩展 hops 默认 1 |
| 模型 | README 主实验 Qwen2.5-Coder-3B-Instruct；代码允许指定模型路径；HF loader GPU 分支 BF16 |
| LoRA | SFT 默认 r=16、alpha=32、dropout=0.05、LR=2e-4、1 epoch、length=2048、batch=2、累积=8；target_modules 未显式指定，依赖 PEFT 默认映射 |
| DPO | 默认 LR=5e-5、beta=0.1、batch=1、累积=8；支持接续 SFT adapter |
| QLoRA | 已读 SFT/DPO 入口没有 BitsAndBytesConfig 或 4-bit 加载；不能说它已实现或验证 QLoRA |
| 指标 | first-turn/final EX、repair success、executable rate；区分 example 与 candidate 分母 |

来源：[builder](https://github.com/thdwhtls/Execution-Guided-Text-to-SQL-Post-Training/blob/4ada9b4f4c637528346cf1011954c624d8c6518a/text2sql_trajectory_builder.py)、[SFT](https://github.com/thdwhtls/Execution-Guided-Text-to-SQL-Post-Training/blob/4ada9b4f4c637528346cf1011954c624d8c6518a/training/train_lora_sft.py)、[DPO](https://github.com/thdwhtls/Execution-Guided-Text-to-SQL-Post-Training/blob/4ada9b4f4c637528346cf1011954c624d8c6518a/training/train_lora_dpo.py)。

值得参考：只读 SQLite URI、set_progress_handler 执行时限、错误信息与列归属诊断、修复轨迹结构、训练集与评测集隔离思想。仅作为后续 repair 扩展，首周不搬入 DPO/GRPO。

需重写：把庞大 builder 拆成推理、验证和诊断接口；不要用其自定义 canonicalize_rows 替代官方语义评分；SFT 截断会从输入左侧裁剪，需记录上下文丢失；dtype、target_modules 和随机性需显式固定。

协议风险：build_feedback 接受 gold 执行结果，result_status 路径可把结果是否匹配告知模型；这种 oracle-assisted 离线修复与只获得 SQLite 错误的线上修复不同。mock 模式直接使用扰动 gold/原 gold，仅供通路演示，永不能记为模型能力。代码的 first-turn 与 final、候选级 executable 分母不同；bad_gold 的剔除也需审计后才能与我们的 EX 比较。

不归属我们：README 全部 Base/SFT/DPO/SFT+DPO/CM Repair 数字、Spider200 消融、pair 数量与过滤结论、所有“修复提升”。CM Repair 本身是作者方法；未来只引用不能改名认领。

许可：当前树未见 LICENSE。仿照思想自写接口不等于已获直接复制许可，今天无移植。

## 3. Lawson-Darrow/Text-to-SQL-Finetune

[仓库](https://github.com/Lawson-Darrow/Text-to-SQL-Finetune)，版本 `b2d6be8b1646e73e9b4ab4116346e21a1ce5fca7`，GitHub license API 返回 MIT。

| 维度 | 已核实内容 |
|---|---|
| 目录 | src/text2sql/、scripts/、docs/、results/、REPORT.md、SPEC.md、pyproject.toml |
| 数据入口 | scripts/prepare_data.sh；src/text2sql/data.py 的 load_schemas/load_examples；run_finetune.py 从 HF 加载训练 split |
| 训练入口 | scripts/run_finetune.py → src/text2sql/train.py 的 build_messages/finetune |
| evaluation | scripts/run_baseline.py、run_ablation.py、run_ladder.py；src/text2sql/evaluate.py 包装外部官方脚本并提供逐例评测与 bootstrap |
| schema | data.py 中 minimal（表列）、with_types（加类型）、with_keys（再加主外键）三档 |
| 模型 | Qwen2.5-Coder-Instruct 1.5B/3B/7B 阶梯；训练脚本默认 1.5B；README 有外部 frontier 对照 |
| LoRA | BF16 非量化加载；r=16、alpha=2r、dropout=0.05，七类投影；LR=2e-4、1 epoch、length=768、累积=8；函数 batch 默认2，但 CLI 默认8覆盖；gradient_checkpointing=False |
| 实现差异 | train.py 注释写 assistant-only，但实际 assistant_only_loss=False；不能宣传它的真实设置是答案独占 loss |
| QLoRA | README 计划涉及 QLoRA/unsloth，已读训练入口实际是 Transformers/TRL/PEFT 普通 BF16 LoRA；未见该入口的 4-bit 路径 |
| 指标 | EX/EM、bootstrap 区间、schema/size/SFT 消融；parse_report 实际只取 overall，分桶需要我们补齐 |

来源：[data.py](https://github.com/Lawson-Darrow/Text-to-SQL-Finetune/blob/b2d6be8b1646e73e9b4ab4116346e21a1ce5fca7/src/text2sql/data.py)、[train.py](https://github.com/Lawson-Darrow/Text-to-SQL-Finetune/blob/b2d6be8b1646e73e9b4ab4116346e21a1ce5fca7/src/text2sql/train.py)、[run_finetune.py](https://github.com/Lawson-Darrow/Text-to-SQL-Finetune/blob/b2d6be8b1646e73e9b4ab4116346e21a1ce5fca7/scripts/run_finetune.py)、[evaluate.py](https://github.com/Lawson-Darrow/Text-to-SQL-Finetune/blob/b2d6be8b1646e73e9b4ab4116346e21a1ce5fca7/src/text2sql/evaluate.py)。

值得参考：schema 可控变量、结构化样本、外部官方评测封装、逐样本正确标志与区间估计。若以后移植小函数，保留 MIT 版权/许可、记录文件和 commit。

需重写：面向 8 GiB 的训练与配置、真正 SQL-only 标签、完整分桶计分、执行器返回码处理与输入长度/行数检查。evaluate.py 用 zip 可能忽略长度不匹配，空 SQL 改 SELECT 1 有统计风险，subprocess 未 check 返回码；不能照搬就称严格可复现。调用 test-suite evaluator 的原始数据库路径也不自动等于完成多库 TSA。

不归属我们：REPORT、blog 和 results 下全部性能曲线、置信区间、阶梯结论、schema 效果、微调增益和 4090 资源经验。1.5B 在 24 GB 上能跑不能证明本机能跑相同 batch。

## 基础设施复用与自己的贡献

| 内容 | 归属和处理 |
|---|---|
| Spider 数据/难度定义、官方 scorer | 社区基础设施；标注来源、版本和许可，不声称原创 |
| Hugging Face、PEFT、LoRA、QLoRA | 现成框架/方法；正确集成是工程工作，不是发明方法 |
| schema 序列化/日志/官方 scorer wrapper | 可参考重写或许可允许后移植；说明具体来源与改动 |
| CM Repair、作者 DPO pipeline | 作者已有方法；本项目首周不实现，不冒充新算法 |
| 我们的复杂度采样 | 待验证的项目方法设计，须给公式、动机、控制变量与消融；简单加权采样本身不是新领域算法 |
| 资源/质量对照、错误分析 | 只有由我们的数据划分、代码和硬件运行产生，才可计入我们的实验贡献 |
| 所有上游结果 | 只能作为有来源的相关工作；不能写入 metrics.csv 或简历当作本机结果 |

## 后续如需本地 clone

以下仅为待执行清单，Day 0 未 clone。建议放在新项目被忽略的 references/，保留原仓库不修改；clone 后 checkout 上述固定 SHA 再研究。

```text
git clone https://github.com/Gansaw98/text-to-sql-spider.git references/gansaw-spider
git clone https://github.com/thdwhtls/Execution-Guided-Text-to-SQL-Post-Training.git references/execution-guided
git clone https://github.com/Lawson-Darrow/Text-to-SQL-Finetune.git references/lawson-finetune
```

无需为完成本项目把三个仓库全部作为依赖。E0 真正需要的是数据与固定官方 evaluator；后者选择并审核后另记录 clone/commit。
