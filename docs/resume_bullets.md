# 简历素材：只引用已完成证据

## 建议选用的4条项目经历

- 在单张RTX 5060 Laptop约8GB显存上构建Qwen2.5-Coder-1.5B跨库Text-to-SQL链路，完成Spider 166库审计、完整schema序列化、SQL-only监督与只读执行评测；以7000条训练数据进行r8 LoRA SFT，在固定1034条dev上将单库EX由50.77%提升至69.15%（+18.38个百分点）。
- 根据真实错误设计同样本、同顺序、同token和438步预算的复杂度loss加权对照，EX达70.21%；保留可执行率下降和配对退化案例，并通过数据库聚类区间说明+1.06个百分点尚不足以证明稳定提升。
- 对比普通LoRA与NF4双重量化QLoRA：训练循环峰值allocated由4.516降至3.213GB（-28.86%），耗时由49.02增至62.17分钟（+26.84%），同协议EX69.15%对68.96%，量化呈现明确的显存/时间/质量权衡。
- 在固定32请求、三轮重复的原生Transformers基准中，对照同一LoRA adapter合并前后，输出吞吐18.44→34.30 token/s（1.86倍），平均完成延迟1742→938ms；首轮EX均18/32，同时记录2条输出变化，不宣称全量无损。

## 每个数字的证据

1. docs/e1_report.md、docs/e1_training_report.md、results/e0_dev_summary.json、results/e1_dev_summary.json。
2. docs/e2_decision.md、docs/e3_report.md、docs/e3_interpretation.md、results/e3_comparison.json。
3. docs/e4_report.md、docs/e4_interpretation.md、results/e4_qlora_seed42_training.json。
4. docs/e5_report.md、docs/e5_interpretation.md、results/e5_summary.json。

## 归属、负结果与未实施内容

LoRA、QLoRA、Qwen、Spider及官方比较函数均非原创；个人项目工作是监督与评测工程、内存实现、恢复验证、受控实验和分析。简单复杂度加权不是发明新领域算法。必须能够自己解释代码和数字再使用简历表述。

全部本轮实验已完成，没有仍在训练的内容。E3可执行率下降且区间含0；QLoRA更慢，EX略低；FP16 batch1未比BF16更快。vLLM服务部署、TSA/EM、多训练seed、独立最终测试集均未实施，不写为已完成。

allocated不代表全GPU物理占用，训练峰值测量不含加载/预检查的历史峰值；E1曾真实断点恢复并单列32.100837秒重算。dev参与E3选择，单库EX可能有数据巧合；本机32条推理benchmark不能替代全量质量验证。
