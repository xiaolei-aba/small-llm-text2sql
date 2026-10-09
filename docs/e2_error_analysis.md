# 真实预测错误分析

分类为多标签启发式，分布之和可超过错误总数；只在 EX 错误样本上标记。词法表/列集合差异、JOIN/SELECT 数、聚合符、WHERE 字面量不构成确定因果；等价改写、别名、嵌套作用域可能误标。需人工读案例核验。

## e0_dev
EX=50.7737%；可执行率=70.5029%；错误 509/1034。

|难度|数量|EX|
|---|---:|---:|
|easy|248|66.53%|
|medium|446|50.90%|
|hard|174|37.36%|
|extra_hard|166|40.96%|

|诊断标签|次数|
|---|---:|
|Schema Linking Error|450|
|Column Selection Error|392|
|JOIN Error|343|
|Table Selection Error|325|
|Invalid Schema Reference|298|
|WHERE Condition Error|198|
|Nested Query Error|95|
|Aggregation / GROUP BY Error|67|
|Other|13|
|SQL Dialect / Function Error|2|
|Execution Timeout|1|
|SQL Syntax Error|1|

### Schema Linking Error：dev:6 / concert_singer
Show the name and the release year of the song by the youngest singer.

Gold（仅离线）：
```sql
SELECT song_name ,  song_release_year FROM singer ORDER BY age LIMIT 1
```
预测：
```sql
SELECT T2.song_name, T2.song_release_year FROM singer AS T1 INNER JOIN singer_in_concert AS T2 ON T1.singer_id = T2.singer_id ORDER BY T1.age ASC LIMIT 1;
```
诊断：Column Selection Error, Invalid Schema Reference, JOIN Error, Schema Linking Error, Table Selection Error；SQLite：OperationalError: no such column: T2.song_name

### Column Selection Error：dev:7 / concert_singer
What are the names and release years for all the songs of the youngest singer?

Gold（仅离线）：
```sql
SELECT song_name ,  song_release_year FROM singer ORDER BY age LIMIT 1
```
预测：
```sql
SELECT T2.song_name, T2.song_release_year FROM singer AS T1 INNER JOIN singer_in_concert AS T2 ON T1.singer_id = T2.singer_id ORDER BY T1.age ASC LIMIT 1;
```
诊断：Column Selection Error, Invalid Schema Reference, JOIN Error, Schema Linking Error, Table Selection Error；SQLite：OperationalError: no such column: T2.song_name

### JOIN Error：dev:8 / concert_singer
What are all distinct countries where singers above age 20 are from?

Gold（仅离线）：
```sql
SELECT DISTINCT country FROM singer WHERE age  >  20
```
预测：
```sql
SELECT DISTINCT T1.Country FROM singer AS T1 INNER JOIN singer_in_concert AS T2 ON T1.Singer_ID = T2.Singer_ID WHERE T1.Age > 20
```
诊断：Column Selection Error, JOIN Error, Schema Linking Error, Table Selection Error；SQLite：None

### Table Selection Error：dev:9 / concert_singer
What are  the different countries with singers above age 20?

Gold（仅离线）：
```sql
SELECT DISTINCT country FROM singer WHERE age  >  20
```
预测：
```sql
SELECT DISTINCT T1.Country FROM singer AS T1 INNER JOIN singer_in_concert AS T2 ON T1.Singer_ID = T2.Singer_ID WHERE T2.Age > 20
```
诊断：Column Selection Error, Invalid Schema Reference, JOIN Error, Schema Linking Error, Table Selection Error；SQLite：OperationalError: no such column: T2.Age

### Invalid Schema Reference：dev:10 / concert_singer
Show all countries and the number of singers in each country.

Gold（仅离线）：
```sql
SELECT country ,  count(*) FROM singer GROUP BY country
```
预测：
```sql
SELECT T2.Country, COUNT(T1.Singer_ID) FROM singer AS T1 INNER JOIN singer_in_concert AS T2 ON T1.Singer_ID = T2.Singer_ID GROUP BY T2.Country;
```
诊断：Column Selection Error, Invalid Schema Reference, JOIN Error, Schema Linking Error, Table Selection Error；SQLite：OperationalError: no such column: T2.Country

### WHERE Condition Error：dev:38 / concert_singer
What are the names of the singers who performed in a concert in 2014?

Gold（仅离线）：
```sql
SELECT T2.name FROM singer_in_concert AS T1 JOIN singer AS T2 ON T1.singer_id  =  T2.singer_id JOIN concert AS T3 ON T1.concert_id  =  T3.concert_id WHERE T3.year  =  2014
```
预测：
```sql
SELECT DISTINCT T3.Name FROM singer AS T1 INNER JOIN singer_in_concert AS T2 ON T1.Singer_ID = T2.Singer_ID INNER JOIN concert AS T3 ON T2.concert_ID = T3.concert_ID WHERE T3.Year = '2014';
```
诊断：Invalid Schema Reference, Schema Linking Error, WHERE Condition Error；SQLite：OperationalError: no such column: T3.Name

### Nested Query Error：dev:41 / concert_singer
Find the name and location of the stadiums which some concerts happened in the years of both 2014 and 2015.

Gold（仅离线）：
```sql
SELECT T2.name ,  T2.location FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.Year  =  2014 INTERSECT SELECT T2.name ,  T2.location FROM concert AS T1 JOIN stadium AS T2 ON T1.stadium_id  =  T2.stadium_id WHERE T1.Year  =  2015
```
预测：
```sql
SELECT T1.Name, T1.Location FROM stadium AS T1 INNER JOIN concert AS T2 ON T1.Stadium_ID = T2.Stadium_ID WHERE T2.Year IN ('2014', '2015')
```
诊断：JOIN Error, Nested Query Error, WHERE Condition Error；SQLite：None

### Aggregation / GROUP BY Error：dev:16 / concert_singer
What is the maximum capacity and the average of all stadiums ?

Gold（仅离线）：
```sql
select max(capacity), average from stadium
```
预测：
```sql
SELECT max(capacity) ,  avg(Average) FROM stadium;
```
诊断：Aggregation / GROUP BY Error；SQLite：None

### Other：dev:57 / pets_1
Find the first name of students who have cat or dog pet.

Gold（仅离线）：
```sql
SELECT DISTINCT T1.Fname FROM student AS T1 JOIN has_pet AS T2 ON T1.stuid  =  T2.stuid JOIN pets AS T3 ON T3.petid  =  T2.petid WHERE T3.pettype  =  'cat' OR T3.pettype  =  'dog'
```
预测：
```sql
SELECT T1.fname FROM student AS T1 INNER JOIN has_pet AS T2 ON T1.stuid = T2.stuid INNER JOIN pets AS T3 ON T2.petid = t3.petid WHERE T3.pettype IN ('cat', 'dog');
```
诊断：Other；SQLite：None

### SQL Dialect / Function Error：dev:481 / wta_1
Find the number of matches happened in each year.

Gold（仅离线）：
```sql
SELECT count(*) ,  YEAR FROM matches GROUP BY YEAR
```
预测：
```sql
SELECT YEAR(tourney_date) AS year, COUNT(*) AS num_matches
FROM matches
GROUP BY YEAR(tourney_date);
```
诊断：Column Selection Error, SQL Dialect / Function Error, Schema Linking Error；SQLite：OperationalError: no such function: YEAR

### Execution Timeout：dev:480 / wta_1
How many total tours were there for each ranking date?

Gold（仅离线）：
```sql
SELECT sum(tours) ,  ranking_date FROM rankings GROUP BY ranking_date
```
预测：
```sql
SELECT COUNT(DISTINCT T2.tourney_id) AS total_tours FROM rankings AS T1 INNER JOIN matches AS T2 ON T1.player_id = T2.winner_id OR T1.player_id = T2.loser_id
```
诊断：Aggregation / GROUP BY Error, Column Selection Error, Execution Timeout, JOIN Error, Schema Linking Error, Table Selection Error；SQLite：OperationalError: interrupted

### SQL Syntax Error：dev:775 / world_1
Which African countries have a smaller population than that of any country in Asia?

Gold（仅离线）：
```sql
SELECT Name FROM country WHERE Continent  =  "Africa"  AND population  <  (SELECT min(population) FROM country WHERE Continent  =  "Asia")
```
预测：
```sql
SELECT T1.Name FROM country AS T1 INNER JOIN country AS T2 ON T1.Code = T2.Code WHERE T1.Continent = 'Africa' AND T1.Population < ALL (SELECT Population FROM country WHERE Continent = 'Asia')
```
诊断：Aggregation / GROUP BY Error, Column Selection Error, JOIN Error, SQL Syntax Error, Schema Linking Error, WHERE Condition Error；SQLite：OperationalError: near "ALL": syntax error
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

## 配对变化 e0_dev → e1_dev
{
  "baseline": "e0_dev",
  "candidate": "e1_dev",
  "improved": 248,
  "regressed": 58,
  "delta_ex": 0.1837524177949711,
  "db_cluster_bootstrap_95_ci": [
    0.13600891861761427,
    0.24344312773180263
  ],
  "bootstrap_replicates": 10000,
  "seed": 42,
  "limitation": "20 DB clusters; conditional on these trained models, not multi-training-seed uncertainty"
}
