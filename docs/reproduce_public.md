# 面向新机器的复现指南

本指南是从公开代码与官方资源重建实验的静态审查结果；本次发布审计没有在干净GPU机器上重新训练，因此不声称完成跨机端到端复现。原生Windows/单张RTX5060 Laptop是唯一实测环境。

## 0. 先隔离作者结果

作者仓库包含已有训练报告、逐条评分和metrics，但模型、adapter和原始预测未分发。evaluate_predictions.py遇到同run_id但不同预测哈希会拒绝复用评分，metrics与E5汇总也不会替换同名旧行。因此不要直接在作者工作区重跑。

取得代码后保留一份只读原副本，再另建一个用于复现的独立目录（建议名称small-llm-text2sql-reproduction）。**下列准备仅针对这个新副本，当前作者工作区不用执行：**

1. 将新副本的results整个目录移动到references/published_results，保留原分数、训练报告和逐条评分。
2. 新建results、results/predictions、results/profiles；从references/published_results/metrics.csv仅复制CSV表头到新的results/metrics.csv，不复制结果行。
3. 原configs、data/manifests、docs保留作为参考；重新运行数据/训练准备时会生成本次manifest、环境报告和审计。不要把已有docs/cuda_check.json当作新机器已验证。
4. 确认新副本没有作者的adapters、checkpoints或原始预测；绝不复制这些产物后把恢复/跳过当成重新训练。

这种隔离不要求改写Git历史，也不删除原成果。当前训练/benchmark入口有固定run名和相互依赖；隔离结果目录是目前代码下最清楚的全阶段复现方法，尚未实现通用run-root参数。

## 1. 环境（新机器执行，现有text2sql不重建）

```powershell
conda create -n text2sql python=3.11.16
conda activate text2sql
$env:PYTHONUTF8 = '1'
$projectPython = (Get-Command python).Source
& $projectPython -c "import sys; print(sys.executable); assert sys.prefix.replace(chr(92),'/').rstrip('/').endswith('/text2sql')"
& $projectPython -m pip install -r requirements.txt
& $projectPython -m pip install numpy==2.4.6
& $projectPython scripts/check_cuda.py
```

每条命令退出码非0就停止。PyTorch锁定2.11.0+cu128，需兼容的NVIDIA驱动；不要自动替换CPU版或修改驱动。CUDA检查是真实矩阵运算，不只检查torch.cuda.is_available。QLoRA阶段再安装requirements-qlora.txt。依赖锁和原环境快照见requirements*.txt、environment_e*.txt；不把Windows conda-explicit历史文件当作跨平台锁。

## 2. 官方数据与模型

Spider官方来源：[官网](https://yale-lily.github.io/spider)、[官方Google Drive](https://drive.google.com/file/d/1403EGqzIDoHMdQF4c9Bkyl7dZLZ5Wt6J/view)。CC BY-SA 4.0，必须保留归属。

- ZIP存放cache/downloads/spider_data.zip。
- ZIP版本SHA256：00636695dabed6b5f4b8328a16b13e069a2f16591d5efcce57660669c85b121b。
- 解压后data/raw/spider/spider_data应含train_spider.json、dev.json、tables.json与database目录。
- 若全新机器没有文件，可运行scripts/download_spider.py；若已从官方获取同ZIP，用`--reuse-archive`从已有ZIP恢复解压，不能重新下载覆盖。
- Windows无法创建的4个带冒号成员是两个test bakery CSV及两个macOS资源分叉，脚本记录跳过；不是训练JSON/SQLite缺失。正式审计仍须比对原ZIP，不手工“修复”原数据。

```powershell
# 仅已有官方ZIP但尚未完成解压时：
& $projectPython scripts/download_spider.py --reuse-archive
& $projectPython scripts/audit_spider.py --root data/raw/spider/spider_data
```

模型：[官方Qwen固定版本](https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct/tree/2e1fd397ee46e1388853d2af2c993145b0f1098a)，Apache-2.0。配置configs/model_lock.json同时锁定tokenizer。全新机器可运行scripts/download_model.py；已有完整snapshot时跳过。本快照不包含历史本机代理下载工具；仅使用上述官方snapshot入口。

模型权重model.safetensors应为3,087,467,144字节，SHA256 c1b9b30e907950516ba3c646bdf570d8084c25a6410a0cdca80cf04b11bc13a8；其他文件散列见model_download.json。校验后再加载，不只根据目录名判断版本。

## 3. 恢复评测器、测试和预处理

```powershell
& $projectPython scripts/fetch_evaluator.py
& $projectPython -m unittest discover -s tests -v
& $projectPython scripts/prepare_e0.py
```

fetch_evaluator同时下载官方源文件与LICENSE，按configs/evaluator_lock.json验证哈希；相同本地文件不重下，修改过的文件不覆盖。测试依赖本地tokenizer与评测源码，故须按上述顺序准备。测试共17项；不提供官方tokenizer时，3项tokenizer集成测试明确跳过，其余14项可在CPU执行。当前快照验证不加载预训练模型权重或执行GPU训练。

scripts/check_public_release.py用于本快照的文件、隐私和指标完整性校验；不要求研究仓库的Day0提交或私人Git身份。本机专用环境快照工具未分发。

## 4. 实验顺序

按[阶段命令](reproduce.md)执行E0→E1→E2→E3→E4→E5，每条检查退出码。E1前先prepare_sft.py，E3/E4沿用E1顺序；E4前安装requirements-qlora.txt并运行probe_qlora.py确认NF4算子和最长样本反向能完成。E5先生成、逐条件评分（不带--record-metrics），再report_benchmark.py合并三轮速度与首轮质量。

E2的原实验选择是hard/extra权重2、其他1并全局均值归一化，不在复现中根据新的dev分数重新搜索。恢复训练只能信任自己产生的checkpoint，因为torch.load(weights_only=False)反序列化不能用于陌生来源文件。

生成后才可运行report_comparison.py/build_project_report.py：这些脚本会验证原始预测与adapter哈希，只下载代码无法重新生成作者报告。已有逐条评分和summary可独立阅读，但不能替代缺失原始预测的重新验算。硬件变化可能导致贪心输出不同；任何新数字单独保留，不覆盖原作者声明后称为原实验。

## 5. 足够复现什么、仍有哪些限制

配置、模型/评测commit、ZIP与权重哈希、预处理/监督/生成/评分代码、样本顺序和全部正式指标都已提供，能够在官方资源可获取时重新运行同协议实验。未提供离线全资源镜像，依赖官方分发持续可用；没有自动化全新机器一键流水线，没有跨平台/多seed保证，也无法在不重新生成预测的情况下复算作者的每条输出。

官方数据/模型不可用或哈希变更时应停止并记录，不能悄悄换版本。公网发布须先解决../PUBLIC_RELEASE_REPORT.md中的隐私历史与授权问题。
