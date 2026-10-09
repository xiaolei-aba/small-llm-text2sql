# E1 预注册训练设置

在 E0 完整评分前写定；E0 完成后才启动训练。普通 LoRA 控制组使用全部 7000 条 train_spider，seed=42，随机打乱一次无放回，每条曝光一次。dev 的问题/答案不进入训练；训练和 dev 的 db_id 交集为零。E3 依据 E2 的诊断做一次采样改变，保留相同 7000 曝光、438 optimizer steps、初始化、LoRA/优化器参数，不承诺提升。

配置：configs/e1.json。rank=8、alpha=16、dropout=.05；注意力 q/k/v/o 与 MLP gate/up/down 七类线性层。BF16 冻结底座，PEFT 默认 FP32 LoRA 参数，AdamW，lr=2e-4，weight_decay=.01，warmup22 steps 后 cosine，梯度裁剪1.0。micro batch=1，accumulation16；最后一步只有8条且按8正确归一化。训练上限2304，实测最长2226；零排除、零截断，SQL加结束token监督，Prompt/padding屏蔽。无 dev early stopping 或最优 checkpoint 选择；只使用预算结束的 adapter。

显存策略：非量化 BF16 底座、SDPA、non-reentrant gradient checkpointing、仅在监督位置计算词表 logits。后者不是少算标签：causal 位置 t-1 预测 token t，省去所有 masked prompt 的词表投影；已用小型 Qwen2 的完整 masked CE 验证 loss 与 lm_head 梯度等价。全部 decoder 上下文仍保留。参考 [PEFT LoRA 文档](https://huggingface.co/docs/peft/en/package_reference/lora)；LoRA 本身不属于项目原创。

训练前在最长训练样本进行一次前后向检查，不更新优化器；随后恢复随机状态、清空梯度再训练。只更新 lora_ 参数。每50步存本地断点（adapter、optimizer、CPU/CUDA RNG、曝光顺序、历史、计时），成功最终产物不覆盖。checkpoint只加载本项目自己创建的文件。

训练时间排除模型加载/预检查，含步骤日志和中间 checkpoint 开销，排除最终 adapter 保存；中断恢复排除停机时间。训练显存和推理显存分字段保存。单次训练 seed 的结果不能当作多 seed 稳定性结论。

环境：PEFT 0.18.1 经 pip dry-run 确认依赖已满足后使用 --no-deps 安装，未改 torch/transformers。测试遭遇 Windows sandbox tempfile ACL 拒绝访问（即使项目内临时目录），使用本地提升权限运行原测试后9/9通过；不是删除或跳过测试。

入口：scripts/prepare_sft.py → scripts/train_lora.py --config configs/e1.json → scripts/run_e0.py --adapter adapters/e1_lora_seed42（同一 dev manifest 和生成配置）→ scripts/evaluate_predictions.py。

## 运行中记录修复

E1因运行中seen字段误用计划计数，在第200步断点后主动暂停，最后旧进程完成205步。恢复第200步并重算5步；对比loss和gradient norm均完全一致。旧报告与退出1被归档（results/e1_logging_fix_interruption.json），未冒称整次不中断。32.100837秒已完成但回滚的计算另记；未记录部分step耗时不伪造。train_seconds为保留轨迹的累计循环计时，不包含修复停机/回滚额外计算，资源比较需同时披露。训练目标、超参数、样本顺序和438步预算未改。
