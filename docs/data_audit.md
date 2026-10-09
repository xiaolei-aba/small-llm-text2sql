# Spider 1.0 数据审计

用途：Text-to-SQL training / evaluation benchmark。E0 不训练；本阶段仅下载和审计，完成后暂停等待用户确认。

## 官方来源与版本

- 官方项目：[Spider 1.0](https://yale-lily.github.io/spider)，[官方 GitHub](https://github.com/taoyds/spider)。
- 官网 Dataset 链接：[spider_data.zip](https://drive.google.com/file/d/1403EGqzIDoHMdQF4c9Bkyl7dZLZ5Wt6J/view)。
- 下载使用同一 file ID 的 Google 官方 `drive.usercontent.google.com/download` 地址，不是第三方重打包。
- 数据许可：官网标注 CC BY-SA 4.0；注意这与 GitHub 评测代码许可不是同一概念。
- HEAD 实测：205800266 bytes；Last-Modified 为 2024-09-11 21:03:09 GMT。它是文件修改时间，不擅自称为语义版本号。
- 用实际下载日期、archive SHA256、逐文件 SHA256 固定快照，而不是只写“最新版”。正式下载记录在 `data/manifests/spider_download.json`；该文件只有成功下载后才生成。
- 预期原始目录：`data/raw/spider/`。保留官方 ZIP 的内部文件名和目录结构，实际结构下载后核实。

## 结构解释

`question` 是自然语言问题；`query` 是 gold SQL；`db_id` 把样本关联到一份数据库。

`tables.json` 保存按 db_id 索引的表、列、抽象类型、主键和外键元信息；`database/<db_id>/<db_id>.sqlite` 保存可执行 SQL 的真实 SQLite 数据库。元信息用于构造 schema，数据库用于核实实际声明类型及后续只读执行评测。

`schema.py` 仅接收 db_id、schema 元信息和 SQLite 路径，不接收 question/query。列与表顺序遵循固定 tables.json，类型来自 SQLite PRAGMA table_info；主外键采用 Spider 标注，复合主键单独展示为元组。不会读取数据库行值，也不会从 gold SQL 选择表或列。SQLite 主键/外键约束可能与标注不同，出现不一致应保留并审计，不修改原库。

## 数据用途与防泄漏

E0：不训练，后续仅 dev zero-shot 评测。train_spider 保留给 E1 以后；本阶段不使用其训练。train_others 或 test 若存在，只清点，不自动加入任何实验。

gold SQL 仅用于离线数据解释与评测，禁止进入 prompt。数据库例子和 schema 展示不是模型实验；没有 accuracy。严禁使用 dev 数据训练、把答案用于 prompt 构造或依据 dev gold 人工提供额外表列提示。

## 下载与检查命令

```powershell
# 先确保 scripts/check_cuda.py 已通过。
& 'python' scripts/download_spider.py --proxy [LOCAL_PROXY]
# --root 根据下载后的实际目录填写，不猜测：
& 'python' scripts/audit_spider.py --root <actual-root>
```

直连 Google 两个官方域名超时；现有 Windows 代理路径 HEAD 成功。脚本校验下载大小、ZIP CRC、路径边界并拒绝覆盖已有原始数据。数据包散列由本地生成用于复现，若官方没有发布独立 checksum，不能声称完成官方 checksum 比对。

## 实测清单与示例

正式审计日期：2026-10-08（Asia/Shanghai）。历史 CUDA 成功记录来自 2026-09-29，本次未重新验证 GPU、未安装依赖、未下载或加载模型。

实际根目录：`[PROJECT_ROOT]\data\raw\spider\spider_data`。本次没有重新下载数据。

| 本地程序实测项 | 结果 |
|---|---|
| train_spider 样本/数据库 | 7000 / 140 |
| dev 样本/数据库 | 1034 / 20 |
| train/dev db_id 交集 | 0 |
| tables.json schema | 166 |
| database/ SQLite 文件/目录 | 166 / 166 |
| integrity_check=ok | 166 / 166 |
| 成功生成确定性 schema | 166 / 166 |
| errors | 空列表 |
| 与归档逐字节散列匹配的解压文件 | 2230 |
| 未声明的归档文件缺失/内容差异 | 0 |
| 审计前后原始文件散列 | 全部不变 |

以上数字来自 spider_audit.json，而非复制 README。train_others 实测 1659 条，只清点不纳入训练；test.json 2147 条、test_tables 206 项，仅清点。test_database 中 SQLite 的归档内容被比对，但没有对 test 做 integrity/schema 全量语义检查。主完整性范围为 tables.json 的 166 个数据库（train/dev 合计160个，另6个），未执行 gold SQL，不能声称所有 gold 都正确可执行。

### 执行、问题和修复

首轮原脚本命令退出码1（audit_initial_output.txt）：soccer_1/store_1/world_1 报 sqlite_sequence 不存在。只读 sqlite_master 证明三个表实际存在，原因是我们自己的 read_sqlite_schema 排除了 sqlite_ 前缀表。修复为读取所有表，再按官方 tables.json 输出，未删改官方元信息。schema 版本升级 spider_schema_v2；新增 AUTOINCREMENT/sqlite_sequence 回归测试。三项 unittest 本次通过，退出码0。

增强审计后相同命令退出码0（audit_final_output.txt）：加入全166库只读 PRAGMA integrity_check、表列关联、PK/FK差异记录、原始文件前后散列、归档逐文件比对。只读连接使用 mode=ro 和 query_only=ON。完整性通过不等于外键数据关系或标准答案语义全部正确。

发现136个表的主键或外键声明与Spider标注不同，详情见 schema_annotation_differences.md 及 JSON 的 annotation_differences。它们被显式作为标注/DDL差异保留，不作为磁盘损坏处理，也没有隐藏或修改原库。formatter 继续沿用已有约定：表列与PK/FK来自Spider标注，类型来自SQLite声明；Spider的 number 等抽象类型不要求与 INT/REAL 字面一致。示例 singer_in_concert 在Spider标注中只有 concert_ID 为主键，而SQLite实际为 (concert_ID, Singer_ID) 复合主键。未来是否改变键来源必须单独验收，不能静默更改prompt协议。

随机预览从排序后的 train/dev 共160个 db_id 用 Random(42).sample 抽3个：county_public_safety、baseball_1、game_injury。已阅读输出；baseball_1 schema 较长且无Spider主键标注，不能伪造主键。完整内容在 schema_previews.md。

### 归档、跳过项和时间

ZIP为205800266 bytes，SHA256：`00636695dabed6b5f4b8328a16b13e069a2f16591d5efcce57660669c85b121b`，本次重新散列与历史下载manifest相符。2230个非跳过文件的内容均匹配ZIP；macOS元数据不计为数据库。

4个Windows不兼容成员均仍保存在原ZIP中，恢复解压时跳过：


- `spider_data/test_database/bakery_1/data_csv/receipts (3:11:18, 5:53 PM)_original.csv`
- `__MACOSX/spider_data/test_database/bakery_1/data_csv/._receipts (3:11:18, 5:53 PM)_original.csv`
- `spider_data/test_database/bakery_1/data_csv/items (3:11:18, 5:53 PM)_original.csv`
- `__MACOSX/spider_data/test_database/bakery_1/data_csv/._items (3:11:18, 5:53 PM)_original.csv`

它们是测试集 bakery_1 附属的两个 CSV 及对应两个 macOS 元数据，不是 train/dev JSON 或 SQLite 缺失。

历史下载完成时间字段为2026-09-29 14:27:16 UTC（基于ZIP mtime推断）。恢复开始14:28:49 UTC原被误命名为download_started_at_utc，本次改为recovery_started_at_utc并保留原值；首次下载开始时间未知，不补造。extraction_at_utc是开始解压时刻，不是完成时刻。此次审计时间独立记录。

### 真实 dev:0 示例与 formatter 输出

question：How many singers do we have?

db_id：`concert_singer`

Gold SQL：

```sql
SELECT count(*) FROM singer
```

实际 schema（Spider键标注 + SQLite声明类型）：

```text
Database schema:

Table stadium:
- Stadium_ID INT
- Location TEXT
- Name TEXT
- Capacity INT
- Highest INT
- Lowest INT
- Average INT
Primary key: (Stadium_ID)

Table singer:
- Singer_ID INT
- Name TEXT
- Country TEXT
- Song_Name TEXT
- Song_release_year TEXT
- Age INT
- Is_male bool
Primary key: (Singer_ID)

Table concert:
- concert_ID INT
- concert_Name TEXT
- Theme TEXT
- Stadium_ID TEXT
- Year TEXT
Primary key: (concert_ID)

Table singer_in_concert:
- concert_ID INT
- Singer_ID TEXT
Primary key: (concert_ID)

Foreign keys:
concert.Stadium_ID -> stadium.Stadium_ID
singer_in_concert.Singer_ID -> singer.Singer_ID
singer_in_concert.concert_ID -> concert.concert_ID
```

问题询问歌手总数；db_id关联整个concert_singer库。未来模型应接收问题和完整schema，自行选择singer表并生成COUNT查询；Gold SQL只在离线理解/评分侧使用，不能用于构造输入或挑表。此处没有执行Gold、生成预测或计算accuracy。

审计完成后暂停，等待用户验收；没有创建Prompt、下载模型、Smoke Test或训练。
