# E0 固定输入与评测协议

模型/tokenizer：Qwen/Qwen2.5-Coder-1.5B-Instruct，revision见configs/model_lock.json。Prompt版本sqlite_zero_shot_v1；schema版本spider_schema_v2。数据审计已获用户接受，最新自主执行授权覆盖旧暂停说明。

系统消息：You are an expert SQL generator.

用户消息：Given the following database schema: + 完整schema + Question: + question + Generate a valid SQLite SQL query that answers the question. Return only the SQL query without explanation or Markdown.

使用原始tokenizer.apply_chat_template，add_generation_prompt=True；无few-shot、CoT、行值或gold输入。实际输入与token数见tokenizer_example.md。key标注差异沿用且披露，不按正确答案筛表。后续SFT沿用这两条输入消息，仅追加assistant SQL作为标签。

greedy，batch=1，BF16非量化，输入上限2048，输出上限256。已扫描固定dev输入，最大792 tokens，没有输入截断；输出达到上限另记truncated，不人工补SQL。256是Day0候选固定预算，不因dev效果调参。

完整生成配置还包含固定模型仓库 generation_config.json 的默认项：repetition_penalty=1.1，eos_token_id=[151645,151643]；代码将 pad_token_id 设为 tokenizer EOS=151645。do_sample=False 覆盖仓库默认采样开关，temperature/top_p/top_k 被忽略（Transformers 对此会提示 warning）。这是带重复惩罚的确定性 greedy，不能描述成 repetition_penalty=1.0。E0–E3 保持一致，不根据 dev 结果改动。文件内容和SHA见docs/model_download.json。

## 主指标

single_db_ex_official_result_eq_keep_distinct：在原始SQLite库安全执行gold/pred，使用固定test-suite上游exec_eval.py的原样result_eq及其纯函数依赖比较结果；行排序是否重要遵循上游gold包含order by规则。保留DISTINCT，保留模型自己预测的值，不plug gold values，不使用上游字符串改写或时间函数替换。

单库 EX 的局限：不同逻辑可能在当前数据库上碰巧返回相同结果（包括两者都为空）；结果比较允许一致的列顺序置换，沿用上游行为。因此它不能证明语义等价，也不能替代多数据库 Test Suite Accuracy。排序检测继承简单的 `order by` 字符串规则；这些限制统一作用于所有对照。

上游test-suite commit e97acc546ecbee8fa27fa8dbf025ef61493a876c；hardness使用Spider b7b5b8c890cd30e35427348bb9eb8c6d1350ca7c 的Evaluator.eval_hardness与官方数据sql AST。安全执行适配改变了资源/执行边界，故报告为基于官方结果比较的单库EX，不声称未经修改运行官方CLI或TSA。Exact Match尚未实现，留空。源码保留许可证，下载脚本/散列应随阶段存档。

只读mode=ro、query_only、SQLite authorizer阻止写入/ATTACH/PRAGMA/扩展；5秒SQL截止、最多100000行和32MB结果。执行资源失败计错，gold异常属于评测阻断，必须报告。完整进程时间限制用于评分进程防止无限比较。有效SQL率仅代表安全执行成功。

预先验证1034条gold发现dev:455/456超过原先10000行限制，且wta_1含非UTF-8文本。对齐上游get_cursor_from_path的text_factory decode(errors='ignore')，统一增加资源上限；发生于模型评分前，不依据预测调参。此解码可能合并无效字节不同的字符串，是沿用上游的已知限制。原始数据库不修改。

模型加载单独计时；泛化warmup不含Spider答案。generation_time为tokenize+generate+decode秒数，SQL执行排除。输出token/s汇总采用串行请求的生成时间总和，是生成阶段吞吐，非含SQL评测的端到端吞吐。峰值allocated/reserved分别保留，数值除1e9为GB。

Smoke采用seed42、固定结构/难度标准选10条，只验证通路。正式dev全部1034条，失败不可静默删分母。按sample_id断点恢复，配置散列不符拒绝混合结果。
