# 真实预测错误分析

分类为多标签启发式，分布之和可超过错误总数；只在 EX 错误样本上标记。词法表/列集合差异、JOIN/SELECT 数、聚合符、WHERE 字面量不构成确定因果；等价改写、别名、嵌套作用域可能误标。需人工读案例核验。

## e1_dev
EX=69.1489%；可执行率=88.9749%；错误 319/1034。

|难度|数量|EX|
|---|---:|---:|
|easy|248|86.69%|
|medium|446|70.18%|
|hard|174|57.47%|
|extra_hard|166|52.41%|

|诊断标签|次数|
|---|---:|
|Schema Linking Error|245|
|Column Selection Error|227|
|Table Selection Error|156|
|JOIN Error|155|
|Invalid Schema Reference|112|
|WHERE Condition Error|107|
|Aggregation / GROUP BY Error|55|
|Nested Query Error|52|
|Other|32|

### Schema Linking Error：dev:6 / concert_singer
Show the name and the release year of the song by the youngest singer.

Gold（仅离线）：
```sql
SELECT song_name ,  song_release_year FROM singer ORDER BY age LIMIT 1
```
预测：
```sql
SELECT T2.song_name ,  T1.song_release_year FROM singer AS T1 JOIN singer_in_concert AS T2 ON T1.singer_id  =  T2.singer_id WHERE T1.age  =  ( SELECT min(age) FROM singer )
```
诊断：Aggregation / GROUP BY Error, Column Selection Error, Invalid Schema Reference, JOIN Error, Nested Query Error, Schema Linking Error, Table Selection Error, WHERE Condition Error；SQLite：OperationalError: no such column: T2.song_name

### Column Selection Error：dev:7 / concert_singer
What are the names and release years for all the songs of the youngest singer?

Gold（仅离线）：
```sql
SELECT song_name ,  song_release_year FROM singer ORDER BY age LIMIT 1
```
预测：
```sql
SELECT T1.Name ,  T2.song_release_year FROM singer AS T1 JOIN singer_in_concert AS T2 ON T1.singer_id  =  T2.singer_id WHERE T1.age  =  (SELECT min(age) FROM singer)
```
诊断：Aggregation / GROUP BY Error, Column Selection Error, Invalid Schema Reference, JOIN Error, Nested Query Error, Schema Linking Error, Table Selection Error, WHERE Condition Error；SQLite：OperationalError: no such column: T2.song_release_year

### Table Selection Error：dev:12 / concert_singer
List all song names by singers above the average age.

Gold（仅离线）：
```sql
SELECT song_name FROM singer WHERE age  >  (SELECT avg(age) FROM singer)
```
预测：
```sql
SELECT T2.song_name FROM singer AS T1 JOIN singer_in_concert AS T2 ON T1.singer_id  =  T2.singer_id WHERE T1.age  >  (SELECT avg(age) FROM singer)
```
诊断：Column Selection Error, Invalid Schema Reference, JOIN Error, Schema Linking Error, Table Selection Error；SQLite：OperationalError: no such column: T2.song_name

### JOIN Error：dev:13 / concert_singer
What are all the song names by singers who are older than average?

Gold（仅离线）：
```sql
SELECT song_name FROM singer WHERE age  >  (SELECT avg(age) FROM singer)
```
预测：
```sql
SELECT T2.song_name FROM singer AS T1 JOIN singer_in_concert AS T2 ON T1.singer_id  =  T2.singer_id WHERE T1.age  >  (SELECT avg(age) FROM singer)
```
诊断：Column Selection Error, Invalid Schema Reference, JOIN Error, Schema Linking Error, Table Selection Error；SQLite：OperationalError: no such column: T2.song_name

### Invalid Schema Reference：dev:33 / concert_singer
Show the name and theme for all concerts and the number of singers in each concert.

Gold（仅离线）：
```sql
SELECT T2.concert_name ,  T2.theme ,  count(*) FROM singer_in_concert AS T1 JOIN concert AS T2 ON T1.concert_id  =  T2.concert_id GROUP BY T2.concert_id
```
预测：
```sql
SELECT T2.concert_name ,  T1.theme ,  count(*) FROM concert AS T1 JOIN concert_in_singer AS T2 ON T1.concert_id  =  T2.concert_id GROUP BY T1.concert_id
```
诊断：Invalid Schema Reference, Schema Linking Error, Table Selection Error；SQLite：OperationalError: no such table: concert_in_singer

### WHERE Condition Error：dev:40 / concert_singer
What is the name and country of origin of every singer who has a song with the word 'Hey' in its title?

Gold（仅离线）：
```sql
SELECT name ,  country FROM singer WHERE song_name LIKE '%Hey%'
```
预测：
```sql
SELECT T2.Name ,  T2.Country FROM singer AS T1 JOIN singer_in_concert AS T2 ON T1.Singer_ID  =  T2.Singer_ID WHERE T1.song_name LIKE "%Hey%"
```
诊断：Column Selection Error, Invalid Schema Reference, JOIN Error, Schema Linking Error, Table Selection Error, WHERE Condition Error；SQLite：OperationalError: no such column: T2.Name

### Aggregation / GROUP BY Error：dev:16 / concert_singer
What is the maximum capacity and the average of all stadiums ?

Gold（仅离线）：
```sql
select max(capacity), average from stadium
```
预测：
```sql
SELECT max(capacity) ,  avg(capacity) FROM stadium
```
诊断：Aggregation / GROUP BY Error, Column Selection Error, Schema Linking Error；SQLite：None

### Nested Query Error：dev:48 / pets_1
How much does the youngest dog weigh?

Gold（仅离线）：
```sql
SELECT weight FROM pets ORDER BY pet_age LIMIT 1
```
预测：
```sql
SELECT sum(weight) FROM pets WHERE pettype  =  'dog' AND age  =  ( SELECT min(age) FROM pets WHERE pettype  =  'dog' )
```
诊断：Aggregation / GROUP BY Error, Column Selection Error, Invalid Schema Reference, Nested Query Error, Schema Linking Error, WHERE Condition Error；SQLite：OperationalError: no such column: age

### Other：dev:75 / pets_1
Find the first name and age of students who have a pet.

Gold（仅离线）：
```sql
SELECT DISTINCT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid
```
预测：
```sql
SELECT T1.fname ,  T1.age FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid
```
诊断：Other；SQLite：None
## e3_dev
EX=70.2128%；可执行率=88.0077%；错误 308/1034。

|难度|数量|EX|
|---|---:|---:|
|easy|248|87.10%|
|medium|446|71.52%|
|hard|174|59.77%|
|extra_hard|166|52.41%|

|诊断标签|次数|
|---|---:|
|Schema Linking Error|238|
|Column Selection Error|218|
|JOIN Error|151|
|Table Selection Error|140|
|Invalid Schema Reference|124|
|WHERE Condition Error|100|
|Aggregation / GROUP BY Error|49|
|Nested Query Error|47|
|Other|31|

### Schema Linking Error：dev:6 / concert_singer
Show the name and the release year of the song by the youngest singer.

Gold（仅离线）：
```sql
SELECT song_name ,  song_release_year FROM singer ORDER BY age LIMIT 1
```
预测：
```sql
SELECT T1.Name ,  T2.song_release_year FROM singer AS T1 JOIN singer AS T2 ON T1.singer_id  =  T2.singer_id ORDER BY T2.age LIMIT 1
```
诊断：Column Selection Error, JOIN Error, Schema Linking Error；SQLite：None

### Column Selection Error：dev:7 / concert_singer
What are the names and release years for all the songs of the youngest singer?

Gold（仅离线）：
```sql
SELECT song_name ,  song_release_year FROM singer ORDER BY age LIMIT 1
```
预测：
```sql
SELECT T1.Name ,  T2.song_release_year FROM singer AS T1 JOIN singer AS T2 ON T1.singer_id  =  T2.singer_id ORDER BY T2.age LIMIT 1
```
诊断：Column Selection Error, JOIN Error, Schema Linking Error；SQLite：None

### JOIN Error：dev:12 / concert_singer
List all song names by singers above the average age.

Gold（仅离线）：
```sql
SELECT song_name FROM singer WHERE age  >  (SELECT avg(age) FROM singer)
```
预测：
```sql
SELECT T2.song_name FROM singer AS T1 JOIN singer_in_concert AS T2 ON T1.singer_id  =  T2.singer_id WHERE T1.age  >  (SELECT avg(age) FROM singer)
```
诊断：Column Selection Error, Invalid Schema Reference, JOIN Error, Schema Linking Error, Table Selection Error；SQLite：OperationalError: no such column: T2.song_name

### Table Selection Error：dev:13 / concert_singer
What are all the song names by singers who are older than average?

Gold（仅离线）：
```sql
SELECT song_name FROM singer WHERE age  >  (SELECT avg(age) FROM singer)
```
预测：
```sql
SELECT T2.song_name FROM singer AS T1 JOIN singer_in_concert AS T2 ON T1.singer_id  =  T2.singer_id WHERE T1.age  >  (SELECT avg(age) FROM singer)
```
诊断：Column Selection Error, Invalid Schema Reference, JOIN Error, Schema Linking Error, Table Selection Error；SQLite：OperationalError: no such column: T2.song_name

### Invalid Schema Reference：dev:33 / concert_singer
Show the name and theme for all concerts and the number of singers in each concert.

Gold（仅离线）：
```sql
SELECT T2.concert_name ,  T2.theme ,  count(*) FROM singer_in_concert AS T1 JOIN concert AS T2 ON T1.concert_id  =  T2.concert_id GROUP BY T2.concert_id
```
预测：
```sql
SELECT T1.concert_name ,  T2.theme ,  count(*) FROM concert AS T1 JOIN singer_in_concert AS T2 ON T1.concert_id  =  T2.concert_id GROUP BY T1.concert_id
```
诊断：Invalid Schema Reference, Schema Linking Error；SQLite：OperationalError: no such column: T2.theme

### WHERE Condition Error：dev:43 / concert_singer
Find the number of concerts happened in the stadium with the highest capacity .

Gold（仅离线）：
```sql
select count(*) from concert where stadium_id = (select stadium_id from stadium order by capacity desc limit 1)
```
预测：
```sql
SELECT count(*) FROM stadium WHERE capacity  =  ( SELECT max(capacity) FROM stadium )
```
诊断：Aggregation / GROUP BY Error, Column Selection Error, Schema Linking Error, Table Selection Error, WHERE Condition Error；SQLite：None

### Aggregation / GROUP BY Error：dev:16 / concert_singer
What is the maximum capacity and the average of all stadiums ?

Gold（仅离线）：
```sql
select max(capacity), average from stadium
```
预测：
```sql
SELECT max(capacity) ,  avg(Average) FROM stadium
```
诊断：Aggregation / GROUP BY Error；SQLite：None

### Nested Query Error：dev:47 / pets_1
Find the weight of the youngest dog.

Gold（仅离线）：
```sql
SELECT weight FROM pets ORDER BY pet_age LIMIT 1
```
预测：
```sql
SELECT T2.weight FROM pets AS T1 JOIN student AS T2 ON T1.petid  =  T2.stuid WHERE T1.pettype  =  "dog" AND T2.age  =  (SELECT min(age) FROM student WHERE major  =  4)
```
诊断：Aggregation / GROUP BY Error, Column Selection Error, Invalid Schema Reference, JOIN Error, Nested Query Error, Schema Linking Error, Table Selection Error, WHERE Condition Error；SQLite：OperationalError: no such column: T2.weight

### Other：dev:57 / pets_1
Find the first name of students who have cat or dog pet.

Gold（仅离线）：
```sql
SELECT DISTINCT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat' OR T3.pettype  =  'dog'
```
预测：
```sql
SELECT T1.fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T2.petid  =  T3.petid WHERE T3.pettype  =  'cat' OR T3.pettype  =  'dog'
```
诊断：Other；SQLite：None

## 配对变化 e1_dev → e3_dev
{
  "baseline": "e1_dev",
  "candidate": "e3_dev",
  "improved": 32,
  "regressed": 21,
  "delta_ex": 0.010638297872340385,
  "db_cluster_bootstrap_95_ci": [
    -0.0030967008513931886,
    0.02487146173079713
  ],
  "bootstrap_replicates": 10000,
  "seed": 42,
  "limitation": "20 DB clusters; conditional on these trained models, not multi-training-seed uncertainty"
}
