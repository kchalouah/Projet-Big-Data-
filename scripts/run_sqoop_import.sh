#!/bin/bash

# Wait for services
sleep 10

# Sqoop Command
# Import from MySQL 'sales' table to HDFS
export HADOOP_OPTS="-Dmapreduce.framework.name=local -Dfs.defaultFS=hdfs://namenode:9000"

mkdir -p /tmp/sqoop_classes
sqoop import \
  --bindir /tmp/sqoop_classes \
  --class-name Sales \
  --connect jdbc:mysql://mysql:3306/retail_db \
  --username root \
  --password root \
  --table sales \
  --target-dir /user/sqoop/sales \
  --delete-target-dir \
  --m 1
