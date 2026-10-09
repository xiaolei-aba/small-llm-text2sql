# E3复杂度加权训练记录

训练进程session82417退出0，未中断恢复。7000条每条曝光一次，438步；完整样本顺序与E1一致，输入token3,023,191，监督SQL/EOS token226,130。

训练循环2965.570s（49.43分钟），非padding输入token吞吐1019.43/s。峰值allocated=4.518GB，reserved=4.891GB。

E1循环2941.031s，E3增加24.539s；这是单次真实运行差异，不是严格隔离背景负载后的系统benchmark。E1曾恢复，缓存历史不同；reserved下降不可归因为loss加权节省显存。E1恢复前归档已显示reserved4.891GB，与本轮相近。

前20步raw SQL CE均值0.2822；后20步0.1222。weighted_objective逐步单列，不能把raw loss与weighted objective混比，更不能用它代替dev EX。

唯一目标变化：train官方hard/extra原始loss权重2，easy/medium权重1，全局归一化均值1。配置configs/e3.json；训练实际执行代码commit4167109；过程中为E4准备的新代码没有作用于已经加载定义的此进程。控制核验见data/manifests/e3_control_check.json。

最终adapter SHA256：79841972891869741662f24b101a7cd700fe7f37c83b640e86d45bd289f19f0c。

全量dev推理session62039和评分session1853均退出0：EX726/1034=70.21%，valid910/1034=88.01%。固定最终adapter、同一完整dev与协议；解释及局限见docs/e3_interpretation.md。

显存统计范围：训练代码在模型加载、最长样本预检查之后重置peak计数，再测正式训练循环（包括optimizer状态的首次分配）。未单独测量加载/预检查的历史峰值；reserved仍可能包含此前缓存。allocated不是整个GPU进程的总占用，也不能据此宣称只需同等物理显存即可完成全流程。
