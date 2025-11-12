import pandas as pd
from src.db import get_db
from src.config import COLLECTION_NAME, MONGO_URI, DB_NAME
import pandera as pa
from pandera import Column, DataFrameSchema, Check

# Définition du schéma de donnée attendu
expected_schema = DataFrameSchema({
    "Name": Column(str, nullable=False),
    "Age": Column(int, Check.ge(0), nullable=False),
    "Gender": Column(str, nullable=True),
    "Billing Amount": Column(float, nullable=True),
    "Medication": Column(str, nullable=True),
    "Test Results": Column(str, nullable=True),
    "Blood Type": Column(str, nullable=True),
    "Doctor": Column(str, nullable=True),
    "Date of Admission": Column(str, nullable=False),
    "Room Number": Column(int, Check.ge(0), nullable=True),
    "Medical Condition": Column(str, nullable=True),
    "Admission Type": Column(str, nullable=False),
    "Insurance Provider": Column(str, nullable=True),
    "Discharge Date": Column(str, nullable=True),
    "Hospital": Column(str, nullable=False),
}, strict=True)

# Validation du schéma du dataframe en comparant avec le schéma attendu
def validate_dataframe(df):
    try:
        expected_schema.validate(df, lazy=True)  # lazy=True collecte toutes les erreurs
        return []
    except pa.errors.SchemaErrors as e:
        # Renvoie la liste des messages d'erreurs
        return [f"{row['failure_case']} - {row['column']} : {row['check']}" 
                for row in e.failure_cases.to_dict(orient="records")]
    

def validate_after_migration(db=None, collection=COLLECTION_NAME, sample_size=1000):
    
    # Vérifie la présence de données dans la collection
    data = list(db[collection].find().limit(sample_size))
    if not data:
        return ["Aucune donnée trouvée après migration"]

    # Récupère les données dans un dataframe
    df = pd.DataFrame(data)

    df = df.drop(columns=["_id"], errors="ignore") # Ignore les erreurs liées à la colonne _id

    errors = []
    
    # Appelle de la fonction validate_dataframe sur les données migrées
    errors += validate_dataframe(df)

    return errors
