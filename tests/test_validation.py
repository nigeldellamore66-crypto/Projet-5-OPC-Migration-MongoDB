import pandas as pd
from src.validation import validate_dataframe, validate_after_migration
from src.loader import clean_dataframe
from datetime import datetime

# --------------------------
# Tests unitaires validate_dataframe
# --------------------------

def test_validate_dataframe_correct():
    df = pd.DataFrame([{
        "Name": "Daniel Schmidt", "Age": 63, "Gender": "Male", "Billing Amount": 23762.2,
        "Medication": "Penicillin", "Test Results": "Normal", "Blood Type": "B+", "Doctor": "Denise Galloway",
        "Date of Admission": "2022-11-15", "Room Number": 465, "Medical Condition": "Asthma",
        "Admission Type": "Elective", "Insurance Provider": "Cigna", "Discharge Date": "2022-11-22",
        "Hospital": "Hammond Ltd"
    }])
    df_clean = clean_dataframe(df)
    errors = validate_dataframe(df_clean)
    assert errors == []

def test_validate_dataframe_missing_column():
    df = pd.DataFrame([{
        "Name": "Daniel Schmidt", "Age": 63, "Gender": "Male"  # Billing Amount manquant
    }])
    df_clean = clean_dataframe(df)
    errors = validate_dataframe(df_clean)
    assert any("Billing Amount - None : column_in_dataframe" in e for e in errors)
    assert any("Medication - None : column_in_dataframe" in e for e in errors)

def test_validate_dataframe_extra_column():
    df = pd.DataFrame([{
        "Name": "Daniel Schmidt", "Age": 63, "Gender": "Male", "Billing Amount": 23762.2,
        "Medication": "Penicillin", "Test Results": "Normal", "Blood Type": "B+", "Doctor": "Denise Galloway",
        "Date of Admission": "2022-11-15", "Room Number": 465, "Medical Condition": "Asthma",
        "Admission Type": "Elective", "Insurance Provider": "Cigna", "Discharge Date": "2022-11-22",
        "Hospital": "Hammond Ltd",
        "Extra": "oups"
    }])
    df_clean = clean_dataframe(df)
    errors = validate_dataframe(df_clean)
    assert any("Extra - None : column_in_schema" in e for e in errors)

def test_validate_dataframe_wrong_dtype():
    df = pd.DataFrame
    df = pd.DataFrame([{
        "Name": "Daniel Schmidt", "Age": "63", "Gender": "Male", "Billing Amount": 23762.2,  # Age en str
        "Medication": "Penicillin", "Test Results": "Normal", "Blood Type": "B+", "Doctor": "Denise Galloway",
        "Date of Admission": "2022-11-15", "Room Number": 465, "Medical Condition": "Asthma",
        "Admission Type": "Elective", "Insurance Provider": "Cigna", "Discharge Date": "2022-11-22",
        "Hospital": "Hammond Ltd"
    }])
    df_clean = clean_dataframe(df)
    errors = validate_dataframe(df_clean)
    assert any("dtype('int64')" in e for e in errors)


# --------------------------
# Tests unitaires validate_after_migration
# --------------------------

def test_validate_after_migration(mongo_test_db):
    db=mongo_test_db
    db["collection_test"].delete_many({})
    db["collection_test"].insert_one({
        "Name": "Daniel Schmidt", "Age": 63, "Gender": "Male", "Billing Amount": 23762.2,
        "Medication": "Penicillin", "Test Results": "Normal", "Blood Type": "B+", "Doctor": "Denise Galloway",
        "Date of Admission": "2022-11-15", "Room Number": 465, "Medical Condition": "Asthma",
        "Admission Type": "Elective", "Insurance Provider": "Cigna", "Discharge Date": "2022-11-22",
        "Hospital": "Hammond Ltd"
    })

    # Appel de la fonction sans passer de DataFrame
    errors = validate_after_migration(db=db, collection="collection_test", sample_size=1000)

    assert errors == []

def test_validate_after_migration_missing_field(mongo_test_db):
    # Insérer un document avec un champ manquant
    db=mongo_test_db
    db["collection_test"].delete_many({})
    db["collection_test"].insert_one({
        "Name": "Daniel Schmidt", "Gender": "Male", "Billing Amount": 23762.2,
        "Medication": "Penicillin", "Test Results": "Normal", "Blood Type": "B+", "Doctor": "Denise Galloway",
        "Date of Admission": "2022-11-15", "Room Number": 465, "Medical Condition": "Asthma",
        "Admission Type": "Elective", "Insurance Provider": "Cigna", "Discharge Date": "2022-11-22",
        "Hospital": "Hammond Ltd"
    })

    errors = validate_after_migration(db=db, collection="collection_test", sample_size=1000)
    assert any("Age" in e for e in errors)