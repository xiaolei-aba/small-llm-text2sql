# E4 QLoRA：预先固定的资源对照

E3核心实验已经完成。bitsandbytes0.47.0安装成功且pip check通过；17项测试通过。真实NF4线性层反向及完整Qwen最长2226token反向通过；5步探针粗估59.83分钟，低于90分钟门槛，决定运行完整E4。探针结果不充当正式训练指标。

依据 [bitsandbytes 0.47.0 官方安装文档](https://huggingface.co/docs/bitsandbytes/v0.47.0/en/installation)，Windows x86-64 CUDA12.8 构建列出 sm120。pip dry-run 实际解析到官方 win_amd64 wheel，只需新增 bitsandbytes0.47.0；现有 PyTorch2.11.0+cu128 和 numpy 满足依赖。dry-run 曾一次网络超时后自动重试成功，不是安装或 CUDA 成功证据。计划见 docs/bnb_dependency_plan.json。

固定 NF4、double quantization、BF16 compute；普通 AdamW 保持与 E1 一致，不另外切换8bit优化器。标准 prepare_model_for_kbit_training 会冻结底座并把非4bit浮点参数提升到FP32；模型 forward 在BF16 autocast下运行。与普通LoRA相比不仅是4bit存储，还存在这一标准dtype准备差异，必须披露。推理复用相同准备策略和量化底座，adapter不合并；不能把QLoRA adapter加载到未量化底座后称为同一配置。

configs/e4.json 保持 E1 的7000样本顺序、token数、438步、r8/alpha16/dropout0.05、学习率、调度和监督边界。无复杂度加权；E4是对E1的资源比较，不是E3的后续训练。使用新adapter目录，不覆盖既有结果。

先做最小4bit算子前后向和完整模型最长样本检查，再以固定前5个累积更新步估计运行成本。该预检查的权重丢弃、不用于评测，时间单列；正式训练重置同一seed从底座开始。估计只代表短段、存在长度及热状态误差。若兼容性失败，记录异常；若预计完整训练超过90分钟，则本轮保留预检查证据并延后完整E4，优先交付核心E0–E3与E5。不得把短段估计写作完整训练结果或虚构准确率。

正式实验若运行，应测量训练时间、输入/监督token、allocated/reserved、全量dev EX/可执行率，并披露QLoRA可能省显存但更慢；不能预设提速。不会安装WSL、Docker、驱动或替换PyTorch。

正式训练完成后，先对原固定10条e0_smoke集合进行量化adapter生成与评分，只检查链路/故障，不据其精度调参；再做全1034dev。量化训练和推理属于同一方法配置，E4对E1不能单独分解训练量化误差与推理量化误差。

## 执行结果

探针后完成全预算训练与1034条dev评分，结果见e4_report.md与e4_interpretation.md。上面的阈值和配置是执行前决定，未根据结果修改。
