# 复现实验命令

新机器请先阅读[公开复现指南](reproduce_public.md)，隔离已有结果、恢复官方资源后再执行以下阶段命令。不要直接在作者工作区覆盖成果。

PowerShell 在项目根目录运行；仅使用项目独立 Conda 环境，不修改全局 PATH。硬件数值必须以本机实测为准，不把这里的依赖快照误当作跨平台保证。

```powershell
$env:PYTHONUTF8 = '1'
# 先激活独立Conda text2sql
$projectPython = (Get-Command python).Source
# 本机锁定的官方评测器已存在，无需重新下载。
& $projectPython -m unittest discover -s tests -v
```

下载与数据版本见 data/manifests/spider_download.json、docs/model_download.json、configs/model_lock.json。当前数据和模型已存在，不重下。新的干净机器才需要按这些来源恢复，并验证散列。运行环境快照见 docs/environment_e0.txt 和 docs/environment_e1.txt。可用的预处理原始入口与许可见 docs/data_audit.md。

## E0

```powershell
& $projectPython scripts/prepare_e0.py
& $projectPython scripts/run_e0.py --manifest data/manifests/e0_smoke.json --output results/predictions/e0_smoke.jsonl
& $projectPython scripts/evaluate_predictions.py --predictions results/predictions/e0_smoke.jsonl --manifest data/manifests/e0_smoke.json --run-id e0_smoke
& $projectPython scripts/run_e0.py --manifest data/manifests/e0_dev.json --output results/predictions/e0_dev.jsonl
& $projectPython scripts/evaluate_predictions.py --predictions results/predictions/e0_dev.jsonl --manifest data/manifests/e0_dev.json --run-id e0_dev --record-metrics
```

已保存的 sample_id 会跳过，配置指纹不符会停止，完整预测重复调用不重复推理。不删除成功结果；若要独立重跑，选择新 output/run-id。Windows Codex 沙箱可能阻止 multiprocessing Pipe 或 tempfile ACL；使用经过授权的本地权限执行相同命令，不能去掉只读/进程超时保护来规避。脚本抛异常时先检查退出码和日志，不能把错误当零准确率。

## E1（必须先有完整 E0 summary）

```powershell
& $projectPython scripts/prepare_sft.py
& $projectPython scripts/train_lora.py --config configs/e1.json
& $projectPython scripts/run_e0.py --manifest data/manifests/e0_dev.json --output results/predictions/e1_dev.jsonl --adapter adapters/e1_lora_seed42
& $projectPython scripts/evaluate_predictions.py --predictions results/predictions/e1_dev.jsonl --manifest data/manifests/e0_dev.json --run-id e1_dev --experiment E1 --record-metrics
& $projectPython scripts/analyze_errors.py --runs e0_dev e1_dev
```

中断后同一训练命令从自己创建的 latest.pt 恢复。最终完成的 adapter 不覆盖；模型与 adapter、原始数据和预测被 Git 忽略，但本地保留。报告/配置/manifest/汇总指标受 Git 管理。恢复训练会重新计算最后一次 checkpoint 后未持久化的步骤；优化器与 RNG 一起恢复，不把重复计算当作新增训练曝光。

## E3（已完成；以下为复现顺序）

```powershell
& $projectPython scripts/train_lora.py --config configs/e3.json
& $projectPython scripts/run_e0.py --manifest data/manifests/e0_dev.json --output results/predictions/e3_dev.jsonl --adapter adapters/e3_complexity_seed42
& $projectPython scripts/evaluate_predictions.py --predictions results/predictions/e3_dev.jsonl --manifest data/manifests/e0_dev.json --run-id e3_dev --experiment E3 --record-metrics
& $projectPython scripts/analyze_errors.py --runs e1_dev e3_dev --output e3_comparison
& $projectPython scripts/report_comparison.py --baseline e1_dev --candidate e3_dev --output e3_report --analysis e3_comparison
```

不要在当前已有GPU进程运行时再次启动训练/推理。依次运行，并在每条命令后检查 `$LASTEXITCODE`；上一条失败时先定位原因，不继续下一条。E0/E1/E3/E4与E5完整结果均已保存；完成状态和真实结果见阶段报告，命令清单本身不作为执行证据。

## E4（原生NF4，训练与评测已完成）

bitsandbytes0.47.0已在text2sql安装，依赖锁见requirements-qlora.txt与environment_e4.txt，原模型权重不重下。兼容探针已完成，不重复跑已有probe；5步临时权重不用于评测。

```powershell
& $projectPython scripts/train_lora.py --config configs/e4.json
& $projectPython scripts/run_e0.py --manifest data/manifests/e0_smoke.json --output results/predictions/e4_smoke.jsonl --adapter adapters/e4_qlora_seed42
& $projectPython scripts/evaluate_predictions.py --predictions results/predictions/e4_smoke.jsonl --manifest data/manifests/e0_smoke.json --run-id e4_smoke --experiment E4
& $projectPython scripts/run_e0.py --manifest data/manifests/e0_dev.json --output results/predictions/e4_dev.jsonl --adapter adapters/e4_qlora_seed42
& $projectPython scripts/evaluate_predictions.py --predictions results/predictions/e4_dev.jsonl --manifest data/manifests/e0_dev.json --run-id e4_dev --experiment E4 --record-metrics
& $projectPython scripts/analyze_errors.py --runs e1_dev e4_dev --output e4_comparison
& $projectPython scripts/report_comparison.py --baseline e1_dev --candidate e4_dev --output e4_report --analysis e4_comparison
```

每条成功且检查产物后再运行下一条。smoke必须先核实没有生成失败/OOM；正确率不作为调参信号。脚本从训练报告读取nf4_double，推理使用同一量化与非量化参数dtype准备策略，不把adapter挂到未量化底座。

## E5（六条件固定benchmark）

```powershell
& $projectPython scripts/benchmark_inference.py
if ($LASTEXITCODE -ne 0) { throw 'Benchmark generation failed; inspect outputs before continuing' }
$conditions = (Get-Content configs/e5.json -Raw | ConvertFrom-Json).conditions
foreach ($condition in $conditions) {
    $runName = $condition.name
    & $projectPython scripts/evaluate_predictions.py --predictions "results/predictions/$runName.jsonl" --manifest data/manifests/e5_benchmark.json --run-id $runName --experiment E5
    if ($LASTEXITCODE -ne 0) { throw "Scoring failed: $runName" }
}
& $projectPython scripts/report_benchmark.py
& $projectPython scripts/build_project_report.py
```

E5评分不带--record-metrics；report_benchmark.py组合首轮32条质量与三轮96次请求速度后统一写表，避免把32条计时误当三轮计时。没有vLLM步骤。Windows沙箱Pipe限制时使用同一安全执行器的授权本地执行权限，不移除隔离与只读保护。
