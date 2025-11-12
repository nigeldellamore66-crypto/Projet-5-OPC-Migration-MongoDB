import pandas as pd
import os
import numpy as np

# Détecte le type de fichiers et charge le fichier dans un dataframe
def load_batch(directory: str = "/data"):
    # Cherche les fichiers dans le dossier /data
    files = os.listdir(directory)

    # Filtre CSV ou JSON
    candidates = [f for f in files if f.lower().endswith((".csv", ".json"))]

    # Détecte l'absence de fichiers dans le dossier
    if not candidates:
        raise FileNotFoundError("Aucun fichier .csv ou .json trouvé dans /data")
    # Détecte si il y a plusieurs fichiers dans le dossier
    if len(candidates) > 1:
        print("Plusieurs fichiers trouvés, le premier sera utilisé :", candidates)

    # On sélectionne le premier fichier
    filepath = os.path.join(directory, candidates[0])
    print('Le fichier suivant a été chargé: ', filepath)

    #O n charge le fichier selon son type
    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    elif filepath.endswith(".json"):
        df = pd.read_json(filepath)
    else:
        raise ValueError("Format non supporté")
    return clean_dataframe(df)

# Récupère le Dataframe chargé, normalise les chaîne de caractères et les dates, arrondis les valeurs numériques
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    for col in df.columns:
        if df[col].dtype == "object":
            # Normalisation des chaînes de caractère
            df[col] = df[col].astype(str).str.strip().str.title()
            
        elif pd.api.types.is_numeric_dtype(df[col]):
            # Arrondir les numériques
            df[col] = pd.to_numeric(df[col], errors="coerce").round(2)
    
    # Remplacer None et chaînes vides par NaN
    df = df.replace({None: np.nan, "": np.nan, " ": np.nan})

    return df