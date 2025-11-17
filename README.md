# Projet-5-OPC-Migration-MongoDB
Application Docker de migration pour fichiers de données CSV/JSON vers une base MongoDB paramétrable.

# Migration des données patients vers MongoDB

Ce guide explique comment exécuter la migration , ce qui se passe pendant le processus et comment vérifier son bon déroulement.

---

## Prérequis

- Docker et Docker Compose installés
- Le fichier CSV contenant les données (`healthcare_dataset.csv` est fourni dans le dossier /data/)
https://www.kaggle.com/datasets/prasad22/healthcare-dataset?resource=download

## Contenu de l'application

- un fichier dockercompose.yml qui construit l'architecture des conteneurs
- un fichier dockerfile qui permet d'éxécuter le script de migration
- un fichier requirements.txt dans lequel sont définis les dépendances du dockerfile
- un dossier /src/ qui contient le script python de migration
- un dossier /tests/ qui contient le script de tests automatisés

## Lancer la migration

Dans le répertoire du projet, exécuter :

```bash
docker compose run --rm migration && docker compose up -d
```

Cette commande :
- démarre le conteneur contenant la base MongoDB (mongo)
- exécute le conteneur de migration temporaire qui lit le fichier de données se trouvant dans /data/
- supprime le conteneur de migration temporaire
- exécute le conteneur de sauvegarde (mongo-backup)

## Lancer les tests

```bash
docker compose --profile run-tests up --build
```
Cette commande :
- démarre le conteneur contenant la base de test (mongo_test)
- démarre le conteneur qui lance pytest (migration_tests)

## Déroulement de la migration

1. Le conteneur "mongo" démarre et crée la base `healthcare` si elle n'existe pas                                                       
2. Le conteneur "migration" installe les dépendances configurées dans le fichier prerequis.txt
3. Le conteneur "migration" créer un utilisateur `healthcare_app`, puis charge le fichier CSV dans un DataFrame Pandas
4. Les données du DataFrame sont normalisés, puis leur intégrité est contrôlée.                                                          
5. Les enregistrements sont insérés dans la collection `healthcare.patients` par batch
6. L'intégrité des données importées dans MongoDB est vérifié à nouveau.
7. Le conteneur "migration" est supprimé
8. Le conteneur "mongo-backup" est démarré pour éxecuter les dumps de la base `healthcare`                                                    

##  Vérifier la migration

### Connexion avec Utilisateur/Mot de Passe

```bash
docker exec -it mongo mongosh "mongodb://healthcare_app:password123@mongo:27017/healthcare?authSource=admin"
```

### Vérifier le nombre de documents importés

```mongosh
db.patients.countDocuments()
```

### Afficher les 5 premiers documents

```mongosh
db.patients.find().limit(5).pretty()
```

##  Validation de fin de migration

La migration est considérée comme réussie si :
- Le nombre de documents correspond au nombre de lignes du fichiers de données ( sans les doublons qui sont ignorés)
- Les champs attendus sont présents et cohérents


## Sauvegardes

- Le conteneur mongo-backup effectue un dump de la base toutes les 2 heures, et ils sont supprimés après 3 jours.
- Il est recommandé de conserver le fichier de sauvegarde généré sur le volume "mongo_backups" pour archivage ou restauration ultérieure

## Configuration avancée

- Le fichier dockercompose.yml initialise l'Admnistrateur de la base via les deux lignes "MONGO_INITDB_*" 
- Le fichier /src/config.py contient les variables de configuration utilisés pour paramétrer les crédentiels de l'Administrateur (doit correspondre à ce qui se trouve dans le dockercompose) et de l'Utilisateur,
  ainsi que le nom de la base de donnée/collection utilisés dans MongoDB
- Le fichier /src/validation.py contient le schéma de données attendu (expected_schema) lors de la migration.
  Ce schéma de donnée peut facilement être adapté pour rendre le script compatible pour d'autres projets.
