# 从真实错误理解 Text-to-SQL

以下只用于离线分析，结果不反馈到模型 Prompt。所有 SQL 在原始数据库上只读执行。

## dev:6 / concert_singer
Show the name and the release year of the song by the youngest singer.

Gold
```sql
SELECT song_name ,  song_release_year FROM singer ORDER BY age LIMIT 1
```
执行成功：True；错误：None；结果：[('Love', '2016')]

E0预测
```sql
SELECT T2.song_name, T2.song_release_year FROM singer AS T1 INNER JOIN singer_in_concert AS T2 ON T1.singer_id = T2.singer_id ORDER BY T1.age ASC LIMIT 1;
```
执行成功：False；错误：OperationalError: no such column: T2.song_name；结果：None

解释：模型把 singer 中的 song_name/song_release_year 错放到 singer_in_concert 别名上，数据库因此报 no such column。不是生成出了数据库中不存在的单词，而是列与所属表关联错误。

## dev:8 / concert_singer
What are all distinct countries where singers above age 20 are from?

Gold
```sql
SELECT DISTINCT country FROM singer WHERE age  >  20
```
执行成功：True；错误：None；结果：[('Netherlands',), ('United States',), ('France',)]

E0预测
```sql
SELECT DISTINCT T1.Country FROM singer AS T1 INNER JOIN singer_in_concert AS T2 ON T1.Singer_ID = T2.Singer_ID WHERE T1.Age > 20
```
执行成功：True；错误：None；结果：[('United States',), ('France',)]

解释：预测额外 INNER JOIN singer_in_concert，会排除没有演唱会记录的歌手。即便字段全存在、语法正确，问题只问歌手的国家，没有要求参加过演唱会，因此额外关联可能改变答案。
