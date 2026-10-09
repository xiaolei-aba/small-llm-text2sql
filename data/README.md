# 数据约定

尚未下载数据。目标为 Spider 1.0，非 Spider 2.0。

- `raw/`：原始数据与 SQLite，只读使用，不提交。
- `processed/`：派生样本/token 缓存，不提交。
- `manifests/`：未来记录来源 URL、版本/散列、样本 ID、split 和筛除原因；今天仅占位。

E0 再核实 `train_spider.json`、`dev.json`、`tables.json` 和 `database/<db_id>/<db_id>.sqlite` 的完整性。`train_others.json` 是否纳入必须显式决定，不能无记录混合镜像版本。按数据库划分内部 train_fit/train_val；官方 dev 不参与训练或采样选择。
