# 配置占位

Day 0 不提供可执行训练配置。E0 确认后再固定模型 revision、数据来源与散列、schema/prompt 版本、seed、生成长度、dtype、评测器 commit。

E1/E3/E4 须共享基础配置；差异配置仅暴露当次变量。不得通过修改 batch、序列长度、数据量掩盖量化的独立效果。
