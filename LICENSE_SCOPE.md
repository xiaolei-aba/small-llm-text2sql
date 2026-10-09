# License scope / 许可范围

2026-10-09，仓库所有者xiaolei-aba明确授权为其有权授权的项目代码采用Apache-2.0。根[LICENSE](LICENSE)采用Apache License 2.0标准条款；[NOTICE](NOTICE)给出项目归属。这项授权不扩大到无权重新许可的第三方内容。

|范围|适用规则|
|---|---|
|项目自行实现的src/、scripts/、tests/及自写配置、构建/检查文件|Apache-2.0，仅限所有者有权授权的实现；AI辅助编写不意味着第三方算法是原创。|
|通过configs/evaluator_lock.json与fetch_evaluator.py恢复的官方源码|继续适用固定上游Apache-2.0及原版权/许可；本地缓存被Git忽略。适配层是项目实现，被提取的官方函数仍归上游。|
|Spider原数据与问题、Gold SQL、schema摘录/改编（包括部分docs、data/manifests、results）|保留CC BY-SA 4.0归属、变更说明与ShareAlike要求；不由根代码许可覆盖。详细来源见THIRD_PARTY_NOTICES.md。|
|Qwen模型/tokenizer以及其他软件依赖|保留各自许可证；不分发基础权重、adapter或环境包。|
|LICENSES/中的许可副本和引用的上游材料|保留原内容与归属，不把本项目版权声明加到上游原件上。|
|混合实验报告与说明文档|根代码许可不替换其中数据/第三方材料的独立许可；引用或再分发应按THIRD_PARTY_NOTICES.md逐项保留归属，不将数据摘录视为Apache重许可。|

未移植两个无明确许可证参考仓库的实现；没有用添加根LICENSE弥补未知来源代码的授权。保留单库EX、单seed、dev反馈选方法、小样本benchmark和未部署vLLM等限制，授权不改变实验结论。

[Apache官方条款](https://www.apache.org/licenses/LICENSE-2.0.txt) · [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) · [第三方声明](THIRD_PARTY_NOTICES.md)
