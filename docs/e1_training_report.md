# E1 普通 LoRA 训练记录

状态：训练完成，最终进程退出0；完整 dev 推理与评分均退出 0：EX 715/1034（69.15%），可执行 920/1034（88.97%）。详见 docs/e1_report.md。

7000条训练样本各曝光一次，438 optimizer steps；输入序列token共3,023,191，监督SQL/EOS token共226,130，零截断/排除。
训练循环累计2941.031s（49.02分钟），保留轨迹吞吐1027.94非padding token/s。
峰值allocated=4.516GB，reserved=7.539GB。reserved包含缓存，不等于模型活跃tensor显存；两者都应披露。
前20步平均raw SQL CE=0.2824，后20步=0.1249；这不是dev指标。

rank8/alpha16/dropout0.05，七类线性层，BF16非量化底座，LoRA参数FP32；其他固定配置见configs/e1.json。
可训练参数9,232,384 / 总参数1,552,946,688。
最终adapter SHA256：8e2ce45a04a2161438dec1a8806b67cd1a56702b14a9afcfb1fb2fed7f96e002

恢复记录：日志计数修复时从200步checkpoint恢复，旧进程退出1（主动中止），后续完成进程退出0；201–205步loss/gradient norm与原记录一致。额外回滚计算32.100837s另列，未记录部分step耗时不补造。详情见results/e1_logging_fix_interruption.json、results/e1_recovery_check.json和训练report.resume_history。

评测仅用最终 budget adapter，在 E0 相同 dev/Prompt/schema/生成/评分协议下完成；未选择 dev 最优 checkpoint。下一步：根据 E0/E1 真实错误分析固定 E3 假设。

显存统计范围：训练代码在模型加载、最长样本预检查之后重置peak计数，再测正式训练循环（包括optimizer状态的首次分配）。未单独测量加载/预检查的历史峰值；reserved仍可能包含此前缓存。allocated不是整个GPU进程的总占用，也不能据此宣称只需同等物理显存即可完成全流程。
