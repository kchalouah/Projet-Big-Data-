# Présentation du Projet Big Data Retail Analytics

Ce document sert de support complet pour la présentation du projet.

---

## 1. Contexte & Objectifs

### Le Besoin Métier
*   **Secteur** : Retail (Vente au détail).
*   **Problématique** : Les données sont dispersées (bases de données cloisonnées, fichiers de logs isolés, flux temps réel non exploités).
*   **Objectif** : Construire une plateforme unifiée capable d'ingérer, stocker et visualiser ces données pour permettre une prise de décision rapide.

### Les Enjeux Techniques (Les 3 V)
*   **Volume** : Capacité à gérer un historique important de ventes (gestion via HDFS).
*   **Variété** : Capacité à traiter du structuré (SQL) et du non-structuré (Logs).
*   **Vélocité** : Capacité à capter des événements en temps réel (Kafka).

---

## 2. Architecture & Choix Technologiques

Nous avons opté pour une architecture **Lambda** simplifiée, conteneurisée avec Docker.

### Cœur du Système
*   **Apache Zookeeper** : *Le Coordinateur*.
    *   Gestion de l'état du cluster Kafka.
    *   Assure la tolérance aux pannes.

### Couche d'Ingestion (Collection)
*   **Apache Sqoop** : *Le Déménageur (Batch)*.
    *   Import massif depuis MySQL vers HDFS.
    *   Optimisé pour les bases de données relationnelles.
*   **Apache Flume** : *Le Collecteur (Stream)*.
    *   Agent léger pour la collecte de logs (`tail` en temps réel).
    *   Écriture directe dans HDFS.
*   **Apache Kafka** : *Le Bus de Messages (Temps Réel)*.
    *   Découplage producteur/consommateur.
    *   Tampon haute performance pour les pics de charge.

### Couche de Stockage
*   **Hadoop HDFS** : *Le Data Lake*.
    *   Stockage distribué, fiable et scalable.
    *   Centralise toutes les données brutes (zone "Bronze").

### Couche de Présentation
*   **Streamlit** : *L'Interface Utilisateur*.
    *   Dashboard interactif en Python.
    *   Visualisation hybride : Ventes (SQL) + Flux Live (Kafka) + Santé Système (Zookeeper).

---

## 3. Le Dataset : Sales Data Sample

Données issues d'un scénario de vente de véhicules miniatures de collection.

*   **Structure** : Relationnelle (Tables Clients, Commandes, Produits).
*   **Volume** : ~3000 commandes historiques.
*   **Attributs Clés** :
    *   `SALES` : Montant de la vente.
    *   `STATUS` : État de la commande (Shipped, Cancelled...).
    *   `PRODUCTLINE` : Gamme de produit (Classic Cars, Motorcycles...).
    *   `DEALSIZE` : Taille de la transaction.

---

## 4. Workflow des Données

### Flux A : L'Historique (Traitement Batch)
1.  **Source** : Base de données MySQL (ERP simulé).
2.  **Action** : Job Sqoop planifié (`sqoop import`).
3.  **Destination** : Dossier `/user/sqoop/sales` sur HDFS.
4.  **Usage** : Analyse de tendances longue durée.

### Flux B : Le Temps Réel (Speed Layer)
1.  **Source** : Script simulateur (`producer.py`).
2.  **Action** : Envoi de messages JSON dans le topic Kafka `transactions`.
3.  **Destination** : Consommation directe par le Dashboard.
4.  **Usage** : Monitoring des ventes minute par minute.

### Flux C : L'Observabilité (Logs)
1.  **Source** : Logs techniques de l'application (`app.log`).
2.  **Action** : Agent Flume en écoute continue.
3.  **Destination** : Stockage archivé sur HDFS `/user/flume/logs`.
4.  **Usage** : Audit, debugging et sécurité.

---

## 5. Défis Techniques Rencontrés

Durant la mise en œuvre, nous avons surmonté plusieurs obstacles :

*   **Orchestration Docker** :
    *   *Défi* : Assurer que les services démarrent dans le bon ordre (Zookeeper avant Kafka, HDFS prêt avant Sqoop).
    *   *Solution* : Utilisation de `depends_on` et de `healthchecks` dans Docker Compose.
*   **Connectivité Réseau** :
    *   *Défi* : Faire communiquer Sqoop (conteneur Java) avec MySQL (conteneur SGBD).
    *   *Solution* : Utilisation d'un réseau Docker dédié (`hadoop_net`) et résolution DNS par nom de service.
*   **Compatibilité des Versions** :
    *   *Défi* : Conflits entre les librairies client Kafka Python et le broker Java.
    *   *Solution* : Choix précis des versions (`kafka-python`, image `wurstmeister/kafka`).

---

## 6. Scénario de Démonstration

Voici le déroulé de la démo technique :

1.  **Initialisation** : Lancement du cluster (`docker-compose up`).
2.  **Vérification** : Montrer via l'UI Hadoop que HDFS est vide au départ.
3.  **Ingestion Batch** : Exécution du script Sqoop.
    *   *Preuve* : Visualisation des fichiers `part-m-00000` créés dans HDFS.
4.  **Streaming Live** : Lancement du Producer Python.
    *   *Preuve* : Voir les courbes s'animer en temps réel sur le Dashboard Streamlit.
5.  **Logs** :
    *   *Preuve* : Montrer que le fichier de log local grandit et retrouver sa copie asynchrone dans HDFS via Flume.

---

## 7. Perspectives & Améliorations

Pour aller plus loin, ce projet pourrait évoluer vers :

*   **Traitement Distribué** : Ajouter **Apache Spark** pour effectuer des calculs complexes sur HDFS (ETL).
*   **Indexation** : Brancher **Elasticsearch + Kibana** pour explorer les logs Flume plus facilement.
*   **Data Quality** : Mettre en place des règles de validation sur les données ingérées.
*   **Cloud** : Migrer l'infrastructure vers AWS EMR ou Google Dataproc.

---

## Conclusion

Ce projet a permis de construire une chaîne de valeur complète de la donnée (Data Value Chain).
Nous avons démontré qu'il est possible d'intégrer des technologies robustes (Hadoop, Kafka) dans une architecture moderne et légère pour répondre aux besoins d'analyse historique et temps réel.
