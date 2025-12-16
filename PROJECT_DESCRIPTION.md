# Description du projet Big Data Retail Analytics

## Contexte et objectif
- Besoin : centraliser et exploiter des données retail (ventes historiques, flux temps réel, logs applicatifs) pour analyser, monitorer et itérer rapidement.
- Enjeux : volume (historique + flux), variété (SGBD, logs), vélocité (événements en temps réel), coût et scalabilité (stockage distribué), observabilité.
- Objectif : mettre en place une chaîne d’ingestion, de stockage et de restitution permettant d’alimenter des analyses (tableau de bord Streamlit) et des usages temps réel (Kafka).

## Données traitées
- Historique ventes (CSV Kaggle) chargé dans MySQL puis ingéré vers HDFS via Sqoop.
- Flux simulé de transactions en temps réel (producteur Kafka + logs).
- Logs applicatifs collectés par Flume pour archivage/observabilité dans HDFS.

## Architecture (résumé)
- Ingestion temps réel : Kafka (topics `transactions`), producteur Python.
- Ingestion logs : Flume (source tail sur `logs/app.log`, sink HDFS).
- Transfert batch SGBD → HDFS : Sqoop (table `sales` → `/user/sqoop/sales`).
- Stockage : HDFS (NameNode/Datanode).
- Restitution : Streamlit dashboard (lecture MySQL).
- Outils de supervision : Kafka UI, NameNode UI.

## Rôles des principaux composants
- Kafka : bus d’événements temps réel pour décorréler producteurs/consommateurs.
- Flume : collecte continue des logs et dépôt dans HDFS (traçabilité, audit).
- Sqoop : transfert massif et automatisé MySQL ↔ HDFS.
- HDFS : data lake pour stockage durable (bronze / atterrissage).
- Streamlit : visualisation rapide des indicateurs métiers (ventes).
- MySQL : source transactionnelle pour l’historique structuré.

## Justification des choix
- Kafka pour la résilience et la faible latence des flux temps réel.
- Flume pour la simplicité de collecte de fichiers log en continu vers HDFS.
- Sqoop pour éviter les scripts maison et bénéficier du parallélisme Hadoop sur les imports.
- HDFS pour la capacité et la tolérance aux pannes sur les données brutes/ingérées.
- Stack conteneurisée (docker-compose) pour reproductibilité et isolation des ports.

## Flux end-to-end (bref)
1) Seed MySQL avec le CSV (script `datagen/setup_db.py`).
2) Import batch MySQL → HDFS via `run_sqoop_import.sh`.
3) Production d’événements Kafka (`producer.py`) et écriture simultanée dans les logs.
4) Flume suit `logs/app.log` et écrit les logs dans HDFS.
5) Dashboard lit MySQL et affiche les indicateurs; Kafka UI et NameNode UI exposent l’état des flux et du stockage.

## Livrables attendus (rappel)
- PPT : pourquoi Big Data, architecture, rôle/installation Kafka-Sqoop-Flume, use case.
- Démo : Kafka (prod/cons), Sqoop (import visible dans HDFS), Flume (log → HDFS), dashboard.
- Annexe : commandes d’installation et d’exécution.

