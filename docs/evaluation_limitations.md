# 单库 EX 的一个真实限制案例

离线查看 Spider dev:48，db_id=pets_1：

Question：`How much does the youngest dog weigh?`

官方 Gold SQL（原样，不修改）：

```sql
SELECT weight FROM pets ORDER BY pet_age LIMIT 1
```

通过项目只读执行器实际查询 `SELECT petid, pettype, pet_age, weight FROM pets ORDER BY pet_age LIMIT 8`，得到：

|petid|pettype|pet_age|weight|
|---:|---|---:|---:|
|2003|dog|1|9.3|
|2002|dog|2|13.4|
|2001|cat|3|12.0|

Gold 未显式过滤 dog，但原始库最年轻的宠物恰好是 dog，因此当前结果与“先过滤dog再按年龄取最小”的查询相同。假设换成存在更年轻cat的数据状态，两种SQL可能不同；这是逻辑上的反例说明，本项目没有修改原始SQLite来构造该状态。

下列SQL是讲解用的替代写法，**不是模型输出或新增Gold**，没有送入Prompt，也不用于替换评测答案：

```sql
SELECT weight FROM pets WHERE pettype = 'dog' ORDER BY pet_age LIMIT 1
```

这说明单个原始数据库上的结果相等，无法证明语义在所有数据状态下一致，也不能排除标注与自然语言之间的细节问题。我们保持官方数据不变，并对所有模型使用相同协议；不根据人工偏好改Gold或删样本。

E1对这题的实际输出见results/e2_error_analysis.json：它还存在`age`字段引用错误，不能用这里的讲解SQL替它纠正答案。这个案例用于解释指标边界，不改变任何已报告分数。
