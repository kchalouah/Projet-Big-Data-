# Big Data Pipeline – Status & Usage Report

## Stack & Ports (host)
- Zookeeper: `localhost:22181`
- Kafka broker (PLAINTEXT_HOST): `localhost:19092`
- Kafka UI: http://localhost:18080
- Hadoop NameNode UI: http://localhost:19870
- HDFS RPC: `localhost:19000`
- MySQL: `localhost:13307`
- Streamlit dashboard: http://localhost:18501

## Quick Start
1) Lancer l’ensemble : `docker-compose down && docker-compose up -d`
2) Vérifier les conteneurs : `docker-compose ps`
3) (Option) initialiser MySQL si besoin : `cd datagen && pip install -r requirements.txt` (ou `pip install pandas sqlalchemy pymysql`) puis `python setup_db.py`  
   - Le script cible `localhost:13307`.
4) Import Sqoop : `docker exec sqoop /scripts/run_sqoop_import.sh`
5) Flume collecte `logs/app.log` et pousse vers HDFS `/user/flume/logs/`.
6) Producteur Kafka (transactions + logs) : `python datagen/producer.py` (utilise `localhost:19092` et écrit aussi dans `logs/app.log`).
7) Dashboard : ouvrir http://localhost:18501 (se connecte à `mysql:3306` dans le réseau docker).

## Vérifications rapides
- Kafka UI (http://localhost:18080) : voir le broker `kafka:29092`, topic `transactions` si créé par `producer.py`.
- NameNode UI (http://localhost:19870) : vérifier `/user/sqoop/sales` et `/user/flume/logs/`.
- MySQL (port 13307) : table `sales` présente et alimentée par `setup_db.py`.
- Streamlit (http://localhost:18501) : données visibles (requête `SELECT * FROM sales`).
- Sqoop : script `scripts/run_sqoop_import.sh` crée un core-site minimal (fs.defaultFS vers namenode) et importe désormais avec succès.

## Points d’attention
- Les ports ont été décalés pour éviter les conflits ; adapter vos clients externes et scripts à ces valeurs.
- Si MySQL met du temps à démarrer, relancer `setup_db.py` ou attendre avant Sqoop.
- Flume lit `logs/app.log` côté host (volume `./logs`).
- Pour accéder à Kafka depuis l’hôte, utiliser `localhost:19092`; depuis un conteneur, utiliser `kafka:29092`.

## Script de démo (oral)
1) Montrer `docker-compose ps` (tous les services up).  
2) Kafka UI : afficher broker et topic, produire un message rapide (CLI ou `producer.py`), consommer via UI.  
3) Sqoop : lancer `docker exec sqoop /scripts/run_sqoop_import.sh`, puis montrer `/user/sqoop/sales` dans NameNode UI.  
4) Flume : `echo "INFO test $(date)" >> logs/app.log`, puis vérifier `/user/flume/logs/` dans NameNode UI.  
5) Dashboard : rafraîchir et montrer les métriques/graphes.  

## Message à transmettre au professeur
- Tous les services sont conteneurisés et fonctionnent avec une configuration de ports ajustée pour éviter les conflits locaux.
- Ingestion temps réel via Kafka (topic `transactions`), ingestion logs via Flume vers HDFS, transfert batch MySQL→HDFS via Sqoop, visualisation via Streamlit.
- Les scripts de seed (`setup_db.py`) et d’import (`run_sqoop_import.sh`) sont prêts ; le producteur (`producer.py`) génère à la fois des événements Kafka et des logs pour Flume.
- Interfaces disponibles : Kafka UI (18080), NameNode UI (19870), Dashboard (18501). Hôte Kafka 19092, MySQL 13307.
- Démo prévue : production Kafka + Flume, import Sqoop, vérification HDFS, affichage dashboard. 

## Résultats de tests (11 Dec 2025)
- `docker-compose ps` : tous les services Up (dashboard, datanode healthy, flume, kafka, kafka-ui, mysql, namenode healthy, sqoop, zookeeper).
- MySQL : `SELECT COUNT(*) FROM sales;` → 2823 lignes.
- Kafka : topics `__consumer_offsets`, `transactions`; production test envoyée, consommation `--from-beginning` affiche les derniers messages (timeout attendu en fin de lecture).
- Sqoop : `docker exec sqoop /scripts/run_sqoop_import.sh` réussi; HDFS contient `/user/sqoop/sales/_SUCCESS` et `part-m-00000` (~546 KB).
- Flume : HDFS `/user/flume/logs` encore absent lors du check; envoyer un log (`echo "INFO test $(date)" >> logs/app.log`) puis vérifier après quelques secondes.

