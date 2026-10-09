# Third-party notices / 第三方来源与权利边界

核查日期：2026-10-09。所有者已授权其有权授权的项目代码采用[Apache-2.0](LICENSE)，范围见[LICENSE_SCOPE.md](LICENSE_SCOPE.md)。各上游许可证保持独立；根代码许可不覆盖或重新许可模型、Spider数据及第三方材料。

## 实际使用的官方组件

|组件|固定版本与官方来源|许可|本项目用途与处理|
|---|---|---|---|
|Spider 1.0数据|[官方网站](https://yale-lily.github.io/spider)、[官方下载入口](https://drive.google.com/file/d/1403EGqzIDoHMdQF4c9Bkyl7dZLZ5Wt6J/view)|[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)|train_spider 7000、dev 1034；不分发完整数据、SQLite或原ZIP。问题、Gold SQL、schema摘录及其改编仍须归属Spider，不能受本项目代码许可替代。|
|Spider官方评测代码|[taoyds/spider](https://github.com/taoyds/spider/tree/b7b5b8c890cd30e35427348bb9eb8c6d1350ca7c)，commit b7b5b8c890cd30e35427348bb9eb8c6d1350ca7c|Apache-2.0；Copyright 2024 XLANG NLP Lab|从evaluation.py调用官方hardness；process_sql.py只作为锁定缓存恢复，不在本项目解析/评分路径中导入。许可副本：[Spider](LICENSES/Spider-Apache-2.0.txt)。|
|Test-suite SQL evaluator|[taoyds/test-suite-sql-eval](https://github.com/taoyds/test-suite-sql-eval/tree/e97acc546ecbee8fa27fa8dbf025ef61493a876c)，commit e97acc546ecbee8fa27fa8dbf025ef61493a876c|Apache-2.0，见[原许可副本](LICENSES/TestSuite-Apache-2.0.txt)|只复用exec_eval.py的结果比较函数，不运行多数据库test suite，不把本项目EX称作TSA。|
|Qwen2.5-Coder-1.5B-Instruct|[官方模型及固定revision](https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct/tree/2e1fd397ee46e1388853d2af2c993145b0f1098a)|[Apache-2.0](https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct/blob/2e1fd397ee46e1388853d2af2c993145b0f1098a/LICENSE)，[本地许可副本](LICENSES/Qwen-Apache-2.0.txt)|模型/tokenizer同revision；仅分发锁定信息和指标，不分发基础权重、adapter或checkpoint。其他Qwen型号的许可不由此推断。|

两个官方评测仓库在上述版本的根目录没有NOTICE文件；已重新检查未截断的GitHub树。原始源码在忽略的third_party目录，恢复时scripts/fetch_evaluator.py同时下载源码与LICENSE并校验SHA256。配置见configs/evaluator_lock.json，未把第三方评测代码重许可为本项目原创。

src/evaluation/official.py是本项目适配层：AST提取Spider定义及test-suite的permute_tuple、unorder_row、quick_rej、multiset_eq、get_constraint_permutation、result_eq，函数体保持上游内容；调用时固定随机种子，根据Gold是否有ORDER BY决定顺序比较。SQLite执行层src/evaluation/safe_sql.py由本项目实现，增加只读连接、权限限制、时间/结果资源限制。完整协议见docs/metrics_protocol.md。

## 数据来源、引用与派生材料

Spider：Tao Yu et al., *Spider: A Large-Scale Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL Task*, EMNLP 2018，[论文](https://aclanthology.org/D18-1425/)。官方原ZIP的本地SHA256为00636695dabed6b5f4b8328a16b13e069a2f16591d5efcce57660669c85b121b；这是本地版本标识，不冒称官方独立校验和。

本仓库docs/schema_previews.md、docs/tokenizer_example.md、docs/data_audit.md、错误案例文档，以及results中的逐条评分/错误分析内含Spider问题、Gold SQL或schema摘录；相关摘录与改编按CC BY-SA 4.0标注归属，不施加限制该许可的额外条款。格式化schema、抽取案例和错误分析属于所作变更，原始Gold和原库未改写。模型生成SQL和自行计算的指标单独标记为本项目输出，不把上游作者的结果据为己有。数据衍生内容与项目代码许可应分开处理。

Test-suite比较方法引用：Ruiqi Zhong, Tao Yu, Dan Klein, *Semantic Evaluation for Text-to-SQL with Distilled Test Suites*, EMNLP 2020，[论文](https://aclanthology.org/2020.emnlp-main.29/)。引用方法不表示本项目运行了完整TSA。

## 仅作为设计参考的三个项目

|参考项目与审查版本|许可核实|本项目关系|
|---|---|---|
|[Gansaw98/text-to-sql-spider](https://github.com/Gansaw98/text-to-sql-spider/tree/71b6b083cf27d2da562a51dd4d7b5faac664cee8)|固定版本树未见LICENSE/COPYING/NOTICE|参考schema与训练流程；未纳入其源码/README/结果，不将公开可读视为复制授权。|
|[thdwhtls/Execution-Guided-Text-to-SQL-Post-Training](https://github.com/thdwhtls/Execution-Guided-Text-to-SQL-Post-Training/tree/4ada9b4f4c637528346cf1011954c624d8c6518a)|固定版本树未见LICENSE/COPYING/NOTICE|参考执行反馈思想；未实现其CM Repair/DPO，不复制其代码或结果。|
|[Lawson-Darrow/Text-to-SQL-Finetune](https://github.com/Lawson-Darrow/Text-to-SQL-Finetune/tree/b2d6be8b1646e73e9b4ab4116346e21a1ce5fca7)|[MIT](https://github.com/Lawson-Darrow/Text-to-SQL-Finetune/blob/b2d6be8b1646e73e9b4ab4116346e21a1ce5fca7/LICENSE)|参考小模型消融设计；未移植其实现。未来移植须保留版权和许可。|

历史实现记录及本次九个入口的AST函数体精确比较未发现直接匹配；这不是所有可能改写/片段的穷尽检测，也不能证明独立著作权。证据docs/publication_sources.json与docs/publication_code_comparison.json；详细参考差异见docs/reference_audit.md。

## 本项目实现与依赖

schema序列化、prompt封装、SQL-only数据/损失与选择性logits、训练/恢复循环、复杂度加权、只读执行封装、运行记录、错误分析和benchmark脚本为本项目工程实现（AI辅助编写），不声称发明LoRA、QLoRA或官方评分算法。标准库与外部库通过import使用，不将其源代码作为本项目重新发布。

外部依赖包括Python、PyTorch、Transformers、PEFT、Accelerate、Hugging Face Hub、safetensors、NumPy、tqdm、bitsandbytes；版本见requirements*.txt与docs/environment_e*.txt，各自许可由其官方发行包提供。安装报告保留的上游许可/作者元数据属于第三方，公开作者邮箱不等于本项目秘密。为减少冗余复制，安装报告的包README说明已从公开副本中省略，原记录仍保留本地。

## 根目录LICENSE结论

已按所有者2026-10-09的明确指令添加Apache-2.0 LICENSE，并在NOTICE标注项目代码版权与第三方例外。授权依据为所有者对其有权授权代码的选择，不是将所有材料推定为原创。Spider衍生材料的CC BY-SA要求和各上游许可证不变，详见LICENSE_SCOPE.md。
