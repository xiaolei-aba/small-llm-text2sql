# 项目计划与实际实验协议

项目：Efficient Post-Training of Small LLMs for Complex Text-to-SQL。当前执行状态见docs/agent_progress.md；原早期候选方案保存在docs/history/project_plan_before_experiment_update.md，不是当前数据划分。

## 背景与问题

在单张RTX5060 Laptop（8151MiB）上，用小参数模型把自然语言问题与数据库schema转换为SQLite查询，研究监督微调、基于错误证据的训练优化及资源效率。要求结果可追溯、可解释，不把已有LoRA/QLoRA称为原创算法，也不预设优化有效。

Text-to-SQL同时考察语言理解、schema linking和结构化生成，并能用数据库执行检查结果。选择Spider1.0是为了跨数据库训练/评测、固定SQL结构难度分层和公开比较实现；它不等价于Spider2.0或生产数据库任务。Qwen2.5-Coder-1.5B-Instruct由用户固定，规模适合在约8GB显存下探索普通LoRA与QLoRA，代码预训练提供可检验的起点，不声称它必然是所有小模型中最优。

## 已固定的数据与Baseline

使用官方train_spider.json全部7000条（140库）训练，dev.json全部1034条（20库）评测，数据库交集0。不使用train_others，不另建内部train_val，不改变数据或Gold。全部166库的审计结果和原始ZIP哈希见docs/data_audit.md。早期90/10内部划分只是未执行的建议，已被用户指定协议替代。

E0使用锁定的原始Qwen权重，无adapter/few-shot/CoT/repair。完整schema与question组成固定Prompt，schema含表/列/SQLite声明类型及Spider键标注，不含行值或Gold线索。BF16、batch1、greedy、repetition_penalty1.1、输入上限2048、输出上限256。实际dev最大输入792，无静默截断。模型与tokenizer版本见configs/model_lock.json，详细生成与评分定义见docs/prompt_protocol.md。

E1/E3训练均为7000条、相同顺序、3,023,191输入token、226,130监督token、438步。r8、alpha16、dropout0.05、七类线性层、AdamW lr2e-4、22步warmup后cosine、micro1/累积16（末批8）、最长2304、非重入梯度检查点。仅SQL/EOS监督；按监督位置投影logits降低内存，等价性有loss/梯度测试。单条实际最长2226，全部保留。固定结束预算adapter，不按dev选择checkpoint。

## 指标与有效性边界

主指标为原始单个SQLite数据库上的EX，采用锁定官方result_eq纯比较函数与本项目受限只读执行器。保留DISTINCT、不填Gold值、不修改预测SQL语义；失败计错，Gold失败阻断评分。不是Test Suite Accuracy，也未运行Exact Match。辅助指标：SQL可执行率、官方hardness四桶EX、生成失败/截断、延迟ms、输出token/s、训练秒数、allocated/reserved显存GB。

E2读取dev错误来选择E3，所以E3结果是探索性，不声称独立无偏测试。只运行一个训练seed；20数据库聚类bootstrap不能替代多seed训练或消除方法选择偏差。底座预训练是否包含Spider未知。“跨库”仅指本项目训练/评测数据库不重叠。

## 实验路线

|实验|要验证的假设|输入与方法|输出与指标|相对前一阶段的变化|
|---|---|---|---|---|
|E0|原始小模型能否完成跨库SQL生成、主要失败在哪里|锁定BF16底座、完整schema、固定zero-shot；10条通路检查后全1034dev|逐条预测与评分；EX/valid/四桶/速度/显存|建立无任务SFT控制组|
|E1|SQL-only LoRA SFT能否改善任务适应性|仅7000train、固定438步r8 LoRA；最终adapter同协议dev|adapter/checkpoint/训练日志；质量与训练/推理成本|只增加任务SFT，Prompt/schema/评分不变|
|E2|E1后残余错误是否呈现可干预结构|E0/E1真实预测、SQLite异常、多标签词法诊断加人工案例|错误分布、配对改进/退化、DB聚类区间、方法决策|只做离线分析，不训练新模型|
|E3|适度提高结构复杂训练样本的优化贡献能否提高困难子集与总体EX|train官方hard/extra原始loss权重2，其他1，全局均值归一化；从相同底座重新训练|独立adapter/完整dev/配对分析；重点hard+extra固定340条，兼顾easy/medium退化|相对E1仅改变loss权重，样本覆盖/顺序/token/步数不变；不重采样|
|E4|量化冻结底座能否降低训练内存且保留可接受质量|先native NF4探针，再视成本决定完整QLoRA；NF4+double quant+BF16 compute，普通AdamW与E1预算相同|兼容性/失败证据；若完整运行才填写EX、训练时间/吞吐/显存|相对E1改变底座存储与标准kbit dtype准备；不延续E3权重|
|E5|精度、batch和adapter合并能否改善本机推理成本|固定按输入长度选32请求×3重复，BF16/FP16×batch1/2以及同E1adapter合并前后|首轮32条质量检查、全三轮延迟/吞吐/峰值/加载时间/输出变化|推理配置为变量，训练模型固定；不是全量1034质量结论，也不是vLLM部署|

E3选择依据与预注册见docs/e2_decision.md；E4成本门槛见docs/e4_design.md；E5测量方案见docs/e5_design.md。各实验未经真实运行不填结果，失败与负结果同样保留。

## 资源和恢复

普通LoRA已在本机可行，不因预算擅自换模型。E1实际训练循环约49.02分钟、allocated4.516GB/reserved7.539GB；后者受缓存与恢复历史影响。一次GPU任务，每50步保存optimizer/adapter/RNG状态；推理按sample_id恢复且校验配置/adapter哈希。所有成功产物保留，原始数据/权重/大文件由Git忽略，不推送远端。

优先核心E0–E3，再开展可行E4/E5；不安装WSL/Docker/驱动，不改全局环境。新模型、数据、付费资源或公开发布仍需用户授权。普通阶段遵照最新Master Prompt连续推进，不沿用早期人工验收暂停规则。
