# 第三方实现

E0 已从官方固定 commit 获取 Spider 与 test-suite 的必要源码及 LICENSE，清单/URL/SHA256 在 configs/evaluator_lock.json，恢复命令 scripts/fetch_evaluator.py。本地副本被 Git 忽略；不修改上游文件。src/evaluation/official.py 提取原样纯函数；自写安全执行层的差异见 docs/prompt_protocol.md。执行结果比较复用 test-suite（Apache-2.0），难度分类复用 Spider；不得包装为自己的评测算法。源码许可证保留在对应目录。

参考仓库的完整 clone 可放在被忽略的 `references/`，不作为项目实现提交。Gansaw98 和 thdwhtls 当前树未见 LICENSE 文件，不能据“公开可读”直接认为允许复制。Lawson-Darrow 仓库为 MIT，复制时须保留版权与许可。

公开发布的来源、数据摘录和许可边界见根目录THIRD_PARTY_NOTICES.md；LICENSES目录保存实际官方许可文本。根代码已采用Apache-2.0，仅覆盖所有者有权授权的实现；上游许可原文和数据CC BY-SA边界不变，见LICENSE_SCOPE.md。
