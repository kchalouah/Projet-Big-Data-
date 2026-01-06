# How to Run the Project: Step-by-Step Guide

Follow these steps to bring up the Big Data Pipeline and interact with the Dashboard.

## Prerequisites
*   **Docker Desktop** installed and running.
*   **Python 3.x** installed (for local script execution, optional but recommended).
*   **Git** (optional).

---

## Step 1: Start the Infrastructure
We use Docker Compose to start all services (Hadoop, Kafka, Zookeeper, MySQL, Dashboard).

1.  Open your terminal/command prompt.
2.  Navigate to the project directory:
    ```powershell
    cd "C:\Users\Karim\Big data"
    ```
3.  Start the containers in the background:
    ```powershell
    docker-compose up -d --build
    ```
    *   *Note: The `--build` flag ensures any changes to `dashboard/app.py` or `flume/Dockerfile` are applied. This may take a few minutes the first time.*

4.  Verify all containers are running:
    ```powershell
    docker ps
    ```
    *   You should see: `dashboard`, `kafka`, `zookeeper`, `namenode`, `datanode`, `mysql`, `flume`, etc.

---

## Step 2: Initialize the Database (One-time Setup)
We need to load the historical data into MySQL so the pipeline has something to process.

1.  Run the setup script:
    ```powershell
    python datagen/setup_db.py
    ```
    *   *Output should say: "Data seeded successfully!"*

---

## Step 3: Run ETL Process (Batch Layer)
Now we move the data from MySQL to Hadoop (HDFS) using Sqoop.

1.  Execute the Sqoop import script inside the `sqoop` container:
    ```powershell
    docker exec sqoop sh /scripts/run_sqoop_import.sh
    ```
    *   *This runs a MapReduce job to import the `sales` table into `/user/sqoop/sales` on HDFS.*

---

## Step 4: Start Real-Time Data Generation
We need to generate live traffic for Kafka and Flume to consume.

1.  Open a **new** terminal window (keep the others open).
2.  Run the producer script:
    ```powershell
    python datagen/producer.py
    ```
    *   *You will see logs like: `Sent to Kafka: {'order_id': ...}`.*
    *   **Keep this script running!** It acts as the live users of your system.

---

## Step 5: Access the Dashboard
Now that the system is running and data is flowing, let's view the insights.

1.  Open your web browser.
2.  Go to: [http://localhost:18501](http://localhost:18501)

### What to check:
*   **System Health Tab**: Verify that **Zookeeper** and all services are marked as **Online**.
*   **Real-Time Stream Tab**: You should see new transactions appearing every few seconds (as long as `producer.py` is running). Click "Fetch Latest Stream" to update manually if needed used.
*   **Historical Analysis Tab**: Click "Refresh Data" to see charts based on the data we imported in Step 3.

---

## Step 6: Access Other UIs (Optional)
*   **Kafka UI**: [http://localhost:18080](http://localhost:18080) (To inspect topics/messages manually).
*   **Hadoop NameNode**: [http://localhost:19870](http://localhost:19870) (To browse files in HDFS).

---

## Step 7: Shutdown
When you are done:

1.  Stop the `producer.py` script (Ctrl+C).
2.  Stop the docker containers:
    ```powershell
    docker-compose down
    ```
