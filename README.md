# Projet-5-OPC-Migration-MongoDB
Application Docker de migration pour fichiers de données CSV/JSON vers une base MongoDB paramétrable.

Ce guide explique comment exécuter la migration des données patients, ce qui se passe pendant le processus et comment vérifier son bon déroulement.

Prérequis
Docker et Docker Compose installés
Le fichier CSV contenant les données (healthcare_dataset.csv) https://www.kaggle.com/datasets/prasad22/healthcare-dataset?resource=download
Le script Python de migration qui s'éxecute dans l'image migration https://github.com/nigeldellamore66-crypto/OPC-Projet5/tree/main
Le fichier prerequis.txt qui contient le nom des dépendances python à installer pour l'éxecution du script (paramétrable)
Lancer la migration
Dans le répertoire du projet, exécuter :

docker compose run --rm migration && docker compose up -d
Cette commande :

démarre le conteneur MongoDB (mongo)
exécute le conteneur de migration temporaire qui lit le CSV et insère les données(migration)
supprime le conteneur de migration temporaire
exécute le conteneur de sauvegarde (mongo-backup)
Lancer les tests
docker compose --profile run-tests up --build
Connexion avec user
docker exec -it mongo mongosh "mongodb://healthcare_app:password123@mongo:27017/healthcare?authSource=admin"
Déroulement de la migration
Le conteneur "mongo" démarre et crée la base healthcare si elle n'existe pas
Le conteneur "migration" installe les dépendances configurées dans le fichier prerequis.txt
Le conteneur "migration" créer un utilisateur healthcare_app, puis charge le fichier CSV dans un DataFrame Pandas
Le DataFrame est converti en liste de dictionnaires (records)
Les enregistrements sont insérés dans la collection healthcare.patients
Le conteneur "migration" est supprimé
Le conteneur "mongo-backup" effectue une sauvegarde (mongodump)
Vérifier la migration
Ouvrir un shell MongoDB
docker exec -it mongo mongosh
Utiliser la base "healthcare", puis s'authentifier en tant que "healthcare_app" :
use healthcare
db.auth("healthcare_app", "password123")
Vérifier le nombre de documents importés
db.patients.countDocuments()
Afficher quelques documents pour contrôle
db.patients.find().limit(5).pretty()
Validation de fin de migration
La migration est considérée comme réussie si :

Le nombre de documents correspond au nombre de lignes du CSV
Les champs attendus sont présents et cohérents
Notes supplémentaires
Il est recommandé de conserver le fichier de sauvegarde généré sur le volume /backup pour archivage ou restauration ultérieure
Les fichiers de sauvegarde sont générés toutes les deux heures, et sont supprimés après 3 jours.
