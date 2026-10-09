# Public Release Report / 独立公开快照报告

准备日期：2026-10-09。状态：**公开身份与代码许可已按所有者指令落实；本地复核完成后，等待最终发布确认。** 未创建GitHub远端、未push、未改写研究仓库历史。

## 来源与Git隔离

本目录small-llm-text2sql-public从研究仓库a88c1f0的已审核文件白名单复制而来，不复制.git。原研究仓库现有44个提交（43个实验提交加1个审计提交），全部保留。原始数据、模型和实验成果没有删除或改写。

新仓库仅一个独立初始提交。报告中的旧commit/hash仍用于指认私有研究版本，不是公开Git对象；本快照的文件哈希与改动说明见PUBLIC_FILE_MANIFEST.json、docs/snapshot_provenance.json。不能声称旧实验运行在这个新commit上。

公开仓库本地身份：name为`xiaolei-aba`，Author/Committer均使用`335571521+xiaolei-aba@users.noreply.github.com`。该地址由所有者在GitHub Settings → Emails核实后提供；仅设置本仓库Git配置，没有修改全局identity。已明确授权在本公开仓库修正唯一初始提交，原研究仓库不受影响。替换前的本地占位提交可能仍在本公开仓库reflog中，但不属于main可达历史；没有清理reflog或对原仓库做任何重写。

## 包含的文件

完整待跟踪列表、大小和SHA256在[PUBLIC_FILE_MANIFEST.json](PUBLIC_FILE_MANIFEST.json)。主要包括：

- src：schema/Prompt、SQL-only监督、复杂度权重、模型加载、官方比较适配和安全SQLite执行。
- scripts：官方资源下载/恢复、数据审计、预处理、训练/推理/评分、错误分析和报告；新增check_public_release.py用于独立公开仓库校验。
- configs、tests、requirements：固定模型与评测版本、E0/E1/E3/E4/E5参数、CPU测试和明确的tokenizer集成测试。
- data/manifests：样本ID、难度、token统计、顺序和数据哈希；机器路径改为相对路径/占位符，不包含完整原始数据集。
- results：正式metrics、训练报告、逐条评分、错误分析及恢复证据；指标保持研究仓库值。没有原始生成文件或模型权重。
- docs：必要方法、评测/失败分析、复现、学习说明、来源核验；原环境freeze中本地构建路径脱敏后仅供记录，不直接用于pip安装。
- README、THIRD_PARTY_NOTICES、LICENSES：问题/资源/结果/限制、归属与三个实际官方许可原文。

## 明确排除的内容

不复制研究Git历史、私人交接与历史计划、完整开源审计历史blob清单、pip安装原始日志、Conda显式本机锁、本机专用下载/代理工具、旧Git身份检查器，以及无关临时记录。逐个排除的研究跟踪文件见docs/snapshot_provenance.json。

原始Spider ZIP/JSON/SQLite、模型权重、adapter、checkpoint、下载缓存、训练日志、原始预测、逐轮profile、环境目录和本机编辑器配置不进入发布清单。本地用于测试的官方评测缓存位于被忽略的third_party；源码从固定上游恢复并验SHA256，不作为本项目原创代码提交。不要把整个工作目录压缩上传；只使用Git跟踪集合。

## 公开副本的变更

1. 私人邮箱/机器路径/代理记录脱敏，数据审计root改相对路径。研究原件没有修改。
2. 删除未选入的本机专用工具；报告生成器改用可移植环境描述，新增不依赖旧Git历史的公开检查器。
3. tests/test_sft.py把tokenizer集成测试与CPU数学测试分开；缺tokenizer仅跳过前者，不再让三个CPU测试被setUpClass连带阻塞。
4. 显式添加NumPy版本到公开requirements，原实验实际版本保持不变。
5. 公开文本统一LF换行，修复末尾多余空行，文件清单哈希按公开LF内容计算；修复只存在于私人研究档案的文档链接；旧版本commit不可在此仓库直接checkout，明确记录这一限制。
6. 复制时路径匹配曾误识别URL片段，在提交前从研究原件恢复并使用带单词边界的规则重做，官方URL/锁定哈希已验证。环境快照残余构建路径也在复检中去除。没有把初次失败的扫描算作成功。

## 实验结论保持不变

|实验|同一1034条dev单库EX|
|---|---:|
|E0|50.77%|
|E1 LoRA|69.15%|
|E3复杂度加权|70.21%|
|E4 QLoRA|68.96%|

E3仅+1.06个百分点，置信区间含0且可执行率下降，收益不稳定。QLoRA训练allocated降低28.86%，耗时增加26.84%，不能称量化无损或提速。同一adapter合并在32请求×3轮测量中吞吐18.44→34.30 token/s（1.86倍），首轮EX均18/32但2条原始输出不同；不等于全量无损。所有EX是单个原始数据库上的执行结果比较，不是TSA或Exact Match；未部署vLLM，没有独立最终测试/多训练seed。

本项目工程由AI辅助实现，不能声称全部本人手写；Qwen、Spider、LoRA/QLoRA及官方评分方法不是原创。贡献是工程整合、受控实验、资源测量及可解释的失败分析。

## 第三方授权与根许可

固定版本来源、许可证与适配边界详见[THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md)。Spider数据及本仓库问题/Gold/schema摘录按官方CC BY-SA 4.0归属/变更/相同方式共享要求处理；两套官方评测源码与所用Qwen版本为Apache-2.0，许可原文保留。数据摘录不因将来添加代码许可证而被重新许可。

两个参考仓库没有明确LICENSE，**未复制其实现、README或结果**；Lawson-Darrow为MIT，但本项目也未移植。抽样函数对比及历史记录支持该边界，不等于法律上的穷尽权属证明。第三方缓存只包括已明确授权且哈希锁定的官方文件。

所有者已明确授权其有权授权的项目代码采用Apache-2.0，根LICENSE与NOTICE已添加，范围见LICENSE_SCOPE.md。第三方原件、Spider数据摘录及改编继续遵守原许可；没有添加整体MIT，也不将项目代码许可覆盖全部材料。公开发布本身仍待最终确认。

## 验证结果

- CPU测试：17项发现，14通过、3因无官方tokenizer跳过；退出0。无预训练模型权重、无GPU训练/推理。微型随机模型的梯度/恢复单元测试不算E1重训。
- 官方比较测试使用5个SHA256锁定文件（含LICENSE）的本地忽略缓存；与研究缓存锁定内容一致。
- 全候选文件敏感信息规则检查通过：未命中私人邮箱、本机绝对路径、常见Token/Key/私钥及认证URL；不打印匹配值。未知秘密格式/混淆编码仍是规则扫描局限。
- 14类禁止上传文件的.gitignore检查通过；Git清单不含模型、原始数据库、adapter、checkpoint或缓存。
- 源码compileall、JSON解析、文档相对链接、正式10行metrics与summary一致性检查通过。
- 结果文件的文本内容与研究仓库一致；公开副本统一LF换行后，其Git规范化内容哈希一致；源代码除公开报告描述变更外不改训练、生成或评测算法。必要清单脱敏改动在来源清单中可追踪。

详细测试记录见docs/public_validation.json。没有在新机器重新完成端到端训练，复现仍需官方数据、模型、兼容GPU与依赖；这不是一键跨机器复现认证。

## 是否达到可公开条件

**身份、代码许可与本地工程检查达到发布准备条件，尚未执行公开发布。** 已使用所有者核实的noreply邮箱，根Apache-2.0范围和第三方例外已明确。剩余动作只有用户最终确认后才可创建远端/推送；目前没有远端、没有push。

## 本轮复核与停止点

已再次核查研究仓库HEAD、44个提交、refs、工作区、本地Git配置哈希、全部跟踪文件哈希和研究文件的大小/mtime；仅只读比较，不修改研究目录。正式results内容及上游LICENSES原件未变。测试仍是CPU必要测试，不重跑E0–E5或加载预训练权重。

[最终可发布检查清单](FINAL_RELEASE_CHECKLIST.md)列明实际验证与保留限制；文件清单哈希按最终公开LF字节更新。唯一初始提交的Author/Committer在提交后复核，准确commit以本仓库git log与交付回复为准，避免在提交中嵌入其自身哈希。
