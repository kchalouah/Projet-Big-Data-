# PROJET BIG DATA - RAPPORT FINAL

**Étudiant :** [Votre Nom]
**Date :** 11 Décembre 2025

---

## I. Partie Générale : Le Big Data

### 1. Pourquoi le recours au Big Data ?
Le recours au Big Data est devenu nécessaire face à l'explosion quantitative des données (les "3V" : Volume, Variété, Vélocité). Les systèmes traditionnels (SGBDR) ne suffisent plus pour stocker et traiter efficacement des pétaoctets de données non structurées (logs, réseaux sociaux, capteurs). Le Big Data permet de transformer cette masse d'informations brute en valeur décisionnelle.

### 2. A quel niveau le Big Data est utilisé ?
Le Big Data intervient à tous les niveaux de la chaîne de valeur de la donnée :
*   **Stratégique** : Aide à la décision, prédiction des tendances.
*   **Opérationnel** : Optimisation des processus, logistique, maintenance prédictive.
*   **Client** : Personnalisation de l'expérience, recommandation, détection de fraude.

### 3. Comment le Big Data a été utilisé ?
Historiquement, il a été popularisé par les géants du web (Google, Yahoo) via le framework MapReduce et le système de fichiers distribué GFS (devenu HDFS). Aujourd'hui, il combine :
*   **Stockage distribué** (Hadoop HDFS, S3).
*   **Traitement massivement parallèle** (Spark, MapReduce).
*   **Streaming temps réel** (Kafka, Flink).

### 4. Les différentes étapes à faire
Une pipeline Big Data typique suit ces étapes :
1.  **Ingestion** : Collecte des données (Batch via Sqoop, Streaming via Kafka/Flume).
2.  **Stockage** : Dépôt dans un Data Lake (HDFS).
3.  **Traitement** : Nettoyage, transformation, agrégation (Spark, Hive).
4.  **Analyse & Visualisation** : Tableaux de bord, Machine Learning (Streamlit, Tableau).

---

## II. Partie Spécifique : Notre Projet Retail Analytics

### 1. Données Choisies
Nous utilisons un dataset de **ventes retail** (source Kaggle) contenant des transactions historiques (CSV). En complément, nous simulons un flux temps réel de nouvelles commandes et de logs applicatifs.

### 2. Solution Architecturale Proposée
Nous avons mis en œuvre une architecture **Lambda** simplifiée, capable de traiter à la fois le stock (batch) et le flux (speed layer).

#### Architecture Logique :
*   **Source SGBD** : MySQL (données historiques).
*   **Source Logs** : Application Python (logs temps réel).
*   **Layer Ingestion** : Apache Sqoop (Batch) et Apache Kafka + Flume (Temps réel).
*   **Layer Stockage** : HDFS (Hadoop Distributed File System).
*   **Layer Visualisation** : Dashboard Streamlit et monitoring Kafka UI.

### 3. Justification Théorique des Outils
*   **Apache Kafka** : Choisi pour sa capacité à découpler les producteurs de données des consommateurs, garantissant une haute résilience et une faible latence pour le streaming transactionnel.
*   **Apache Sqoop** : Indispensable pour le pont entre le monde relationnel (MySQL) et le monde distribué (Hadoop). Il parallélise les imports via MapReduce, ce qui est impossible avec de simples scripts SQL.
*   **Apache Flume** : L'outil idéal pour l'ingestion de logs. Sa configuration par "agents" (Source -> Channel -> Sink) est légère et permet d'écrire efficacement dans HDFS sans perdre de données en cas de pic de charge.

### 4. Mise en Œuvre Expérimentale
L'infrastructure est entièrement **conteneurisée avec Docker** pour garantir la portabilité.

#### Stack Technique :
*   **Hadoop (Namenode/Datanode)** : v3.2.1
*   **Kafka & Zookeeper** : Confluent Platform v7.3.0
*   **Flume** : v1.9.0 (Build personnalisé avec librairies Hadoop)
*   **Sqoop** : v1.4.7
*   **MySQL** : v8.0

---

## III. Livrables

### 1. Présentation (Résumé pour PPT)
*   **Problème** : Comment analyser simultanément des ventes historiques et des flux temps réel ?
*   **Solution** : Pipeline Dockerisée Kafka + Sqoop + Flume.
*   **Rôle des outils** :
    *   *Kafka* : Tampon temps réel.
    *   *Sqoop* : Import massif MySQL vers HDFS.
    *   *Flume* : Archivage des logs vers HDFS.
*   **Installation** : `docker-compose up -d`.

### 2. Démonstration Fonctionnelle
La plateforme est opérationnelle.
*   **Script de lancement** : `.\start_project.ps1`
*   **Preuve de fonctionnement** :
    *   *Sqoop* : Dossier `/user/sqoop/sales` présent dans HDFS.
    *   *Flume* : Dossier `/user/flume/logs` rempli en temps réel.
    *   *Kafka* : Topic `transactions` actif (visible sur port 18080).

### 3. Annexe : Instructions d'Installation
1.  **Prérequis** : Docker Desktop installé sur Windows.
2.  **Démarrage Rapide** :
    ```powershell
    cd "Big data"
    .\start_project.ps1
    ```
3.  **Commandes Manuelles** :
    *   *Import SQL* : `python datagen/setup_db.py`
    *   *Lancer Sqoop* : `docker exec sqoop /scripts/run_sqoop_import.sh`
    *   *Simuler Traffic* : `python datagen/producer.py`
