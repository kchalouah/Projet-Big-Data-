# Big Data Retail Analytics - Demo Guide

**Student:** [Your Name]
**Date:** December 11, 2025

---

## 1. Project Objective
The goal of this project is to build a **scalable Big Data Pipeline** capable of handling:
1.  **Batch Data**: Historical sales data ingested from relational databases (**MySQL**) into a distributed file system (**HDFS**) using **Sqoop**.
2.  **Streaming Data**: Real-time transactions processed via **Kafka**.
3.  **Log Data**: Application logs collected in real-time and archived in **HDFS** using **Flume**.
4.  **Analytics**: A unified dashboard (**Streamlit**) to visualize the insights.

This architecture demonstrates the ability to integrate heterogeneous systems (SQL vs NoSQL vs Streams) into a cohesive data platform.

---

## 2. Architecture Overview
We use **Docker containers** to orchestrate the entire stack, ensuring reproducibility.

*   **Ingestion (Batch)**: `Sqoop` (Connects MySQL $\to$ HDFS).
*   **Ingestion (Real-time)**: `Kafka` (Topic: `transactions`).
*   **Ingestion (Logs)**: `Flume` (Tail logs $\to$ HDFS).
*   **Storage**: `Hadoop HDFS` (NameNode/DataNode).
*   **Visualization**: `Streamlit` Dashboard & `Kafka UI`.

---

## 3. Demo Script (Step-by-Step)

### Step 1: Infrastructure Check
**Action**: Run `docker-compose ps` in the terminal.
**What to say**: "Here you can see all our services running in isolated containers. We have healthy NameNode, DataNode, Kafka, Flume, and MySQL services."

### Step 2: Real-Time Flow (Kafka)
**Action**:
1.  Open **Kafka UI** at [http://localhost:18080](http://localhost:18080).
2.  Go to **Topics** $\to$ click `transactions`.
3.  In terminal, run the producer: `python datagen/producer.py` (leave it running for a few seconds).
**What to say**: "This Python script simulates live store transactions. We can see them appearing instantly in the Kafka topic here."

### Step 3: Log Ingestion (Flume)
**Action**:
1.  While the producer is running, it also writes to `logs/app.log`.
2.  Flume is configured to 'tail' this file and dump it into HDFS.
3.  Open **HDFS NameNode** at [http://localhost:19870](http://localhost:19870).
4.  Go to **Utilities** $\to$ **Browse the file system**.
5.  Navigate to: `/user/flume/logs`.
**What to say**: "Simultaneously, Flume is capturing application logs and archiving them into HDFS for long-term storage and audit. You can see the new files appearing here."

### Step 4: Batch Import (Sqoop)
**Action**:
1.  Show the MySQL data exists (already seeded).
2.  Run the import command: `docker exec sqoop /scripts/run_sqoop_import.sh`
3.  Refresh the HDFS browser and navigate to `/user/sqoop/sales`.
**What to say**: "For our historical data, we use Sqoop to perform efficient bulk transfers from MySQL to HDFS. Here is the imported dataset residing in our Data Lake."

### Step 5: Dashboard
**Action**: Open [http://localhost:18501](http://localhost:18501).
**What to say**: "Finally, this dashboard consumes the structured data to provide business insights, completing the pipeline from raw data to visualization."

---

## 4. Key Technical Achievements
*   **Custom Flume Build**: Built a custom Docker image to resolve compatibility issues between Flume 1.9 and Hadoop 3 libraries.
*   **Integration**: Successfully networked 6+ distinct services (Zookeeper, Kafka, Hadoop, MySQL, etc.) with custom port mapping to avoid host conflicts.
*   **Automation**: Created a `start_project.ps1` script to bootstrap the entire environment in one click.
