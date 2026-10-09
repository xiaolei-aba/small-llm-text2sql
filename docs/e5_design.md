# E5 预注册：原生 Transformers 推理资源对照

以下保留执行前设计及随后增加合并对照的决策。现六条件均已完成，实际结果见e5_report.md与e5_interpretation.md；没有vLLM部署。

[vLLM官方GPU安装文档](https://docs.vllm.ai/en/v0.18.0/getting_started/installation/gpu/) 明确原生Windows不受支持。本次不安装WSL2/Docker，不声称vLLM部署。E5采用现有PyTorch/Transformers SDPA的可行对照：底座Qwen同一revision，BF16/FP16 × batch1/batch2，共四种条件。

配置configs/e5.json；脚本scripts/benchmark_inference.py。按E0 manifest的输入token长度排序，均匀选择32个序位，再seed42打乱请求顺序；不根据Gold或正确率选样本。每条件重复3轮（96次请求），最终六条件顺序seed42打乱。每条件重新加载、泛化预热、重置峰值显存；计时含tokenize/generate/decode，排除加载、SQL评分。所有条件同一schema/Prompt、greedy+repetition_penalty1.1、256输出上限。批量输入左padding且传attention_mask。

请求延迟定义为所在batch完成的墙钟时间，因为此同步API在整个batch完成后一起返回；不是把batch时间除以batch_size。吞吐以全部实际输出token/各batch墙钟时间之和计算，不能把每个成员的相同batch用时再累加。按首个EOS截去padding计算有效输出token。记录96次请求和每batch时间；质量只评第1轮32条，不把3次重复冒充96个独立评测样本。

重复间输出变化单独记录。32条的EX只作为数值/批量改变的诊断，不与全量1034 dev EX直接比较。单机、固定条件顺序、单次会话存在温度/频率/背景负载误差，不声称通用速度提升。三轮之间的波动要展示；若优化没有更快，保留负结果。

E4 QLoRA为另一项可选训练效率实验；本脚本不包含4bit权重，也不能充当LoRA/QLoRA对照证据。

## E1 推理开始后的预先扩展（E5 尚未运行）

观察到未合并 LoRA 的逐token生成开销后，增加同一E1 adapter的BF16/batch1“unmerged / safe_merge_and_unload”两条件，其他输入和计时规则完全一致。共6条件，每条件96次请求。此选择基于工程开销观察，不根据dev准确率挑选模型；固定使用E1预算结束的adapter。模型加载计时包括adapter加载及适用时的一次性merge。合并后BF16舍入可能造成输出差异，仍评首轮32条，不预设精度无损或声称全量质量等价。只在对应配对内部归因，不把底座与已训练adapter的差异全归因于推理后端。
