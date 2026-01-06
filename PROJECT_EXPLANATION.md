# Project Explanation: Retail Big Data Pipeline

This document explains the architecture, components, and data flow of the project.

## 🏗 System Architecture

The project is a containerized Big Data pipeline that ingestion, processing, and visualizes retail data. All services run in Docker containers.

### Components
1.  **Zookeeper** (`zookeeper`):
    *   **Role**: Coordination Service.
    *   **Why**: It is the "brain" of the distributed system. Kafka relies on Zookeeper to manage broker metadata, topic configurations, and leader election. Without Zookeeper, our Kafka cluster cannot function.
2.  **Kafka** (`kafka`):
    *   **Role**: Message Broker (Real-time Streaming).
    *   **Why**: Handles high-throughput real-time data feeds. In this project, it receives live "transaction" events from our producer script, buffering them for consumption by the dashboard or other consumers.
3.  **Hadoop HDFS** (`namenode`, `datanode`):
    *   **Role**: Distributed File System (Storage).
    *   **Why**: Provides scalable, fault-tolerant storage for large datasets (Data Lake). We use it to store historical sales data (from MySQL) and application logs (from Flume).
4.  **MySQL** (`mysql`):
    *   **Role**: Relational Database (Source of Truth).
    *   **Why**: Acts as the legacy operational database containing historical sales records. We extract data from here to perform analytics.
5.  **Sqoop** (`sqoop`):
    *   **Role**: ETL Tool (Structured Data).
    *   **Why**: Efficiently transfers bulk data between structured datastores (MySQL) and Hadoop. We use it to "scoop" data from MySQL into HDFS for batch analysis.
6.  **Flume** (`flume`):
    *   **Role**: Data Collector (Unstructured Logs).
    *   **Why**: Designed to collect, aggregate, and move large amounts of log data. We use it to tail application logs and write them directly into HDFS.
7.  **Dashboard** (`dashboard`):
    *   **Role**: Visualization & Monitoring (Streamlit).
    *   **Why**: Provides the user interface. It connects to:
        *   **MySQL**: For historical sales analysis.
        *   **Kafka**: For real-time transaction monitoring.
        *   **Zookeeper**: For system health checks.

## 🔄 Data Flow

### 1. Historical Analysis Flow (Batch)
*   **Source**: `sales_data_sample.csv` is loaded into **MySQL** via `setup_db.py`.
*   **Ingestion**: **Sqoop** connects to MySQL, extracts the `sales` table, and writes it to **HDFS**.
*   **Analytics**: The Dashboard queries MySQL (simulating a serving layer) to visualize historical trends, top customers, and product revenue.

### 2. Real-Time Streaming Flow
*   **Source**: `producer.py` generates random transaction events.
*   **Ingestion**: Events are sent to a **Kafka** topic named `transactions`.
*   **Visualization**: The Dashboard acts as a Kafka Consumer, reading these events in real-time and displaying them in the "Real-Time Stream" tab.

### 3. Log Aggregation Flow
*   **Source**: `producer.py` also writes logs to `logs/app.log`.
*   **Ingestion**: **Flume** tails this log file (inside the container volume).
*   **Storage**: Flume buffers the logs and writes them as files into **HDFS** (`/user/flume/logs/...`).

## 🛠 Why use Zookeeper here?
While newer versions of Kafka (KRaft mode) can run without Zookeeper, this project uses the standard Kafka deployment which **requires** Zookeeper.
*   **Dashboard Integration**: We successfully leveraged Zookeeper in the dashboard's "System Health" tab. By connecting to Zookeeper using the `kazoo` library, we can query the live status of the Kafka cluster (brokers, topics) directly, proving that the distributed coordination is active and healthy.
