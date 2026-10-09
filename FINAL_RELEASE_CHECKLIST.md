# 最终可发布检查清单

核验日期：2026-10-09。结论：发布准备已完成；**等待所有者最终确认，不创建远端、不push。** 本清单只针对small-llm-text2sql-public。

## 身份与历史

- [x] 本仓库local user.name为xiaolei-aba。
- [x] 本仓库local user.email为所有者核实的`335571521+xiaolei-aba@users.noreply.github.com`；未修改全局Git身份。
- [x] 工作树中不再使用占位邮箱，敏感信息扫描仅精确放行上述公开noreply地址。
- [x] 只对公开仓库唯一初始提交作授权的amend，最终Author/Committer与local身份一致；无研究Git历史导入。
- [x] 原研究仓库44个提交、HEAD/refs、184个跟踪文件哈希、本地配置哈希与2910个文件大小/mtime保持不变。

## 授权与材料范围

- [x] 所有者明确授权其有权授权的项目代码使用Apache-2.0；根LICENSE、NOTICE和LICENSE_SCOPE.md已提供。
- [x] Spider问题/Gold/schema等数据摘录和改编继续保留CC BY-SA 4.0边界及归属。
- [x] 官方评测器/Qwen及其他第三方保留各自许可；LICENSES副本未改动，两个无明确许可证参考项目的实现没有纳入。
- [x] README继续声明AI辅助工程实现，不把官方模型、评测方法、LoRA或QLoRA声称为原创。

## 文件与实验真实性

- [x] 跟踪文件清单见PUBLIC_FILE_MANIFEST.json，逐文件SHA256按公开LF内容记录；自身条目不递归计算哈希。
- [x] 无原始数据、SQLite、基础权重、adapter、checkpoint、下载缓存、环境目录或私人配置进入跟踪集合。
- [x] 候选文件未命中私人邮箱、绝对本机路径、常见密钥/Token/私钥及认证URL规则；扫描不打印匹配值。
- [x] 14类忽略规则检查通过；无≥10 MiB跟踪文件。
- [x] 10条正式metrics与summary一致；E0/E1/E3/E4为50.77%/69.15%/70.21%/68.96%，README已自动核对。
- [x] 保留E3收益不稳定、QLoRA训练变慢、单库EX限制、E5仅32请求三轮本机测量、未运行vLLM等事实。
- [x] 正式results、configs、src、数据清单和上游LICENSES在本轮未改动。

## 测试与工程检查

- [x] 再次执行python -m unittest discover -s tests -v：退出0，17项中14通过、3个tokenizer集成测试因未分发官方tokenizer而跳过。
- [x] 未加载预训练模型权重、未执行E0–E5实验；CPU微型随机模型梯度/恢复测试不算重新训练项目模型。
- [x] python scripts/check_public_release.py与compileall通过。
- [x] JSON解析、文档相对链接、git diff --check和提交文件哈希检查通过。
- [x] 提交后确认仅一个独立root commit、工作区干净、无remote；准确commit见交付回复或git log -1。

## 保留的限制与停止点

规则扫描不能排除未知格式或混淆编码的所有秘密；没有在全新机器重跑训练，三个tokenizer测试并未算作通过。单seed/dev反馈选择/单库EX等研究限制不因发布检查通过而消失。旧报告中的研究commit只表示私有研究版本，并不是公开仓库可checkout对象。

- [ ] 所有者最终确认创建GitHub远端并公开推送：**尚未授权，未执行**。

[发布报告](PUBLIC_RELEASE_REPORT.md) · [许可范围](LICENSE_SCOPE.md) · [验证记录](docs/public_validation.json)
