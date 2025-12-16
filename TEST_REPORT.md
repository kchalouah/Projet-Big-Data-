# Smoke Tests & Commands

Run from project root (`C:\Users\Karim\Big data`).

## 1) Stack status
- Command: `docker-compose ps`
- Expect: all services `Up`. Ports: Kafka 19092 (host), ZK 22181, Kafka-UI 18080, NN UI 19870, HDFS RPC 19000, MySQL 13307, Streamlit 18501.

## 2) MySQL data
- Command: `docker exec mysql mysql -uroot -proot -e "USE retail_db; SHOW TABLES; SELECT COUNT(*) FROM sales;"`
- Expect: table `sales` exists; count ≈ 2823 rows.

## 3) Kafka broker & topic
- Start kafka if needed: `docker-compose up -d kafka`
- List topics: `docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list`
- Expect: `__consumer_offsets`, `transactions`.
- Produce test: `docker exec kafka bash -lc "echo '{\"smoke\":\"ok\"}' | kafka-console-producer --broker-list localhost:9092 --topic transactions"`
- Consume sample: `docker exec kafka bash -lc "kafka-console-consumer --bootstrap-server localhost:9092 --topic transactions --from-beginning --timeout-ms 2000 | tail -n 5"`
- Expect: consumer outputs last messages (orders or the `smoke` message); a timeout stack trace is OK when exiting after timeout.

## 4) HDFS check
- Command: `docker exec namenode hdfs dfs -ls /`
- Expect: directories like `/user`, `/tmp`. If Sqoop ran, `/user/sqoop/sales` should appear.

## 5) Sqoop import (currently failing, see note)
- Status: FIXED. Script now writes a minimal `core-site.xml` (fs.defaultFS to namenode), sets `HADOOP_CONF_DIR=/tmp` and `HADOOP_CLASSPATH`.  
- Command: `docker exec sqoop /scripts/run_sqoop_import.sh`
- Expect: job succeeds; HDFS shows `/user/sqoop/sales/_SUCCESS` and `part-m-00000` (~533KB, 2823 records).

## 6) Flume/logs smoke
- Append a log: `echo "INFO test $(date)" >> logs/app.log`
- Check HDFS after a minute: `docker exec namenode hdfs dfs -ls /user/flume/logs`
- Expect: dated folder(s) containing log files.

## 7) UIs
- Kafka UI: http://localhost:18080 (broker `kafka:9092`, topic `transactions`).
- NameNode UI: http://localhost:19870 (browse `/user/...`).
- Streamlit dashboard: http://localhost:18501 (reads MySQL `sales`).

## Summary of current test run
- Containers: all Up (dashboard, datanode, flume, kafka-ui, mysql, namenode, sqoop, zookeeper). Kafka had to be started manually.
- MySQL: `sales` table present, ~2823 rows.
- Kafka: topics listed; consumer shows messages from previous producer runs; test produce command sent without error.
- Sqoop: failing; needs classpath override as noted.
- HDFS: accessible; path `/user/sqoop/sales` empty until Sqoop succeeds.

