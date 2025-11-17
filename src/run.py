from src.loader import load_batch
from src.pipeline import insert_records
from src.validation import validate_dataframe, validate_after_migration
from src.db import create_user,index_unique,get_db
from src.config import MONGO_ADMIN_URI,DB_NAME,MONGO_URI,COLLECTION_NAME


if __name__ == "__main__":
# Chargement du fichier source dans un dataframe et nettoyage
    df= load_batch()

# Vérification du dataframe
    print("Vérification des données AVANT migration...")
    before_errors = validate_dataframe(df)
    if before_errors:
        print("Erreurs détectées dans les données sources :")
        for e in before_errors:
            print("  -", e)
            exit(1)
    else:
        print("Données conformes")

# Connexion $MONGO_ADMIN sur admin
    dbadmin=get_db(MONGO_ADMIN_URI,"admin")
# Création MONGO_USER sur admin avec droits sur DB_NAME
    create_user(dbadmin)
# Bascule avec MONGO_ADMIN sur DB_NAME
    dbadmin=get_db(MONGO_ADMIN_URI,DB_NAME)
# Création index unique avec MONGO_ADMIN
    index_unique(dbadmin,COLLECTION_NAME)
# Connexion avec MONGO_USER sur DB_NAME
    db=get_db(MONGO_URI,DB_NAME)

# Insertion des données dans MongoDB avec MONGO_USER
    inserted,duplicates= insert_records(df,db,COLLECTION_NAME)
    print(f"{inserted} documents insérés, {duplicates} doublons ont été ignorés.")

# Vérification de la base MongoDB
    print("\nVérification des données APRÈS migration...")
    after_errors = validate_after_migration(db)
    if after_errors:
        print(" Problèmes après migration :")
        for e in after_errors:
            print("  -", e)
    else:
        print("Intégrité confirmée après insertion")
