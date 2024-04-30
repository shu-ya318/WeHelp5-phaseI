# TASK2: Create database and table in  MySQL server
## request1: 
### Create a new database named website.
```
CREATE DATABASE website;
```
### 額外寫指令來呈現
```
SHOW DATABASES;
```
![創立資料庫](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/2.1.png?raw=true)



##    request2: 
###   Create a new table named member, in the website database.
```
USE website;
CREATE TABLE member (
    id BIGINT  AUTO_INCREMENT COMMENT 'Unique ID',
    name VARCHAR(255) NOT NULL COMMENT 'Name',
    username VARCHAR(255) NOT NULL COMMENT 'Username',
    password VARCHAR(255) NOT NULL COMMENT 'Password',
    follower_count INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Follower Count',
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Signup Time',
    PRIMARY KEY (id)
);
```
### 額外寫指令來呈現
```
SHOW FULL COLUMNS FROM member;
```
![資料庫內創立表格](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/2.2.png?raw=true)

<br/>

# TASK3: SQL CRUD
## request1: 
### INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data.
```
INSERT INTO member (name, username, password)
VALUES ('test', 'test', 'test');
INSERT INTO member (name, username, password, follower_count, time)
VALUES ('user1', 'username1', 'password1', 10, '2024-04-29 18:00:38'),
       ('user2', 'username2', 'password2', 20, '2024-04-29 18:01:38'),
       ('user3', 'username3', 'password3', 30, '2024-04-29 18:02:38'),
       ('user4', 'username4', 'password4', 40, '2024-04-29 18:03:38');

```
![新增1列指定值和4列任意值的資料](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/3.1.png?raw=true)


## request2: 
### SELECT all rows from the member table.
```
SELECT * FROM member;  
```
![顯示所有列的資料](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/3.2.png?raw=true)


## request3: 
### SELECT all rows from the member table, in descending order of time.
```
SELECT * FROM member ORDER BY time DESC;
```
![依時間由近到前降序排列資料](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/3.3.png?raw=true)


## request4: 
### SELECT total 3 rows, second to fourth, from the member table, in descending order of time. Note: it does not mean SELECT rows where id are 2, 3, or 4.
```
SELECT * FROM member ORDER BY time DESC LIMIT 3 OFFSET 1;

```
![從時間降序後的資料選出第2~4列資料](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/3.4.png?raw=true)


## request5: 
### SELECT rows where username equals to test.
```
SELECT * FROM member WHERE username = 'test';
```
![選出username欄位的值完全等同test的資料](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/3.5.png?raw=true)


## request6: 
### SELECT rows where name includes the es keyword.
```
SELECT * FROM member WHERE name LIKE '%es%';
```
![選出name欄位的值有含es的資料](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/3.6.png?raw=true)


## request7: 
### SELECT rows where both username and password equal to test.
```
SELECT * FROM member WHERE username = 'test' AND password = 'test';
```
![選出username欄位和password欄位的值完全等同test的資料](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/3.7.png?raw=true)


## request8: 
### UPDATE data in name column to test2 where username equals to test.
```
UPDATE member SET name = 'test2' WHERE username = 'test';
```
![選出username欄位的值完全等同test的資料，並將其name欄位的值更新為test2](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/3.8.png?raw=true)


<br/>

# TASK4: SQL Aggregation Functions
## request1: 
### SELECT how many rows from the member table.
```
SELECT COUNT(*) FROM member;
```
![計算member表格的總列數](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/4.1.png?raw=true)

## request2: 
### SELECT the sum of follower_count of all the rows from the member table.
```
SELECT SUM(follower_count) FROM member;
```
![計算follower_count欄位的值加總](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/4.2.png?raw=true
)


## request3: 
### SELECT the average of follower_count of all the rows from the member table.
```
SELECT AVG(follower_count) FROM member;
```
![計算follower_count欄位的平均值](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/4.3.png?raw=true)

## request4: 
### SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.
```
SELECT AVG(follower_count)
FROM (
    SELECT * 
    FROM member 
    ORDER BY follower_count DESC 
    LIMIT 2
) AS subquery;
```
![將資料依follower_count欄位降序排列後，計算前兩列的依follower_count欄位平均值](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/4.4.png?raw=true)



<br/>


# TASK5: SQL JOIN
## request1: 
### Create a new table named message, in the website database.
```
USE website;
CREATE TABLE message (
    id BIGINT  AUTO_INCREMENT COMMENT 'Unique ID',
    member_id BIGINT NOT NULL COMMENT 'Member ID for Message Sender',
    content VARCHAR(255) NOT NULL COMMENT 'Content',
    like_count INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Like Count',
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Publish Time',
    PRIMARY KEY (id),
    FOREIGN KEY (member_id) REFERENCES member(id)
);

```
### 額外用指令呈現
```
SHOW FULL COLUMNS FROM member;
```
![創立新的指定表格](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/5.1.png?raw=true)

### 額外新增5列資料來完成後續要求
```
INSERT INTO message (member_id, content, like_count, time)
VALUES (1, 'Hello, this is a message.', 10, '2024-05-01 10:00:00'),
       (2, 'This is another message.', 20, '2024-05-01 10:05:00'),
       (3, 'And this is yet another message.', 30, '2024-05-01 10:10:00'),
       (4, 'Here is one more message.', 40, '2024-05-01 10:15:00'),
       (5, 'Finally, this is the last message.', 50, '2024-05-01 10:20:00');
SELECT * FROM message;
```
![新增5列資料](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/5.1.1.png?raw=true)


## request2: 
### SELECT all messages, including sender names. We have to JOIN the member table to get that.
```
SELECT message.id, member.name AS sender_name, message.content, message.like_count, message.time 
FROM message 
INNER JOIN member ON message.member_id = member.id;
```
![找出所有的訊息資料，其中包含利用member表格的特定欄位值來對應發送者名稱](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/5.2.png?raw=true)


## request3: 
### SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that.

```
SELECT message.id, member.username AS sender_name, message.content, message.like_count, message.time 
FROM message 
INNER JOIN member ON message.member_id = member.id
WHERE member.username = 'test';
```
![從剛才有發送者名稱的表格中，找出特定發送者名稱的對應資料](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/5.3.png?raw=true)


## request4: 
### Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to test.
```
SELECT AVG(message.like_count)
FROM message 
INNER JOIN member ON message.member_id = member.id
WHERE member.username = 'test';
```
![計算所有發送者username所發送訊息的特定欄位值的平均數](
https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/5.4.png?raw=true)


## request5: 
### Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username.

```
SELECT member.username, AVG(message.like_count)
FROM message 
INNER JOIN member ON message.member_id = member.id
GROUP BY member.username;
```
![將資料依發送者username來分組，再計算每組發送訊息的特定欄位值的平均數](https://github.com/shu-ya318/WeHelp5-phaseI/blob/main/week5/screenshot/5.5.png?raw=true)

