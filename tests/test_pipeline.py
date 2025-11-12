import pandas as pd
from src.pipeline import insert_records 

def test_insert_records_without_duplicates(mongo_test_db):
    db=mongo_test_db
    db["collection_test"].delete_many({})
    df = pd.DataFrame([
        {"Name": "John", "Age": 63, "Gender": "Male", "Billing Amount": 23762.2,"Medication": "Penicillin", "Test Results": "Normal", "Blood Type": "B+", "Doctor": "Denise Galloway","Date of Admission": "2022-11-15", "Room Number": 465, "Medical Condition": "Asthma","Admission Type": "Elective", "Insurance Provider": "Cigna", "Discharge Date": "2022-11-22","Hospital": "Hammond Ltd"},
        {"Name": "Sylvie", "Age": 62, "Gender": "Female", "Billing Amount": 23762.2,"Medication": "Penicillin", "Test Results": "Normal", "Blood Type": "B+", "Doctor": "Denise Galloway","Date of Admission": "2022-11-15", "Room Number": 465, "Medical Condition": "Asthma","Admission Type": "Elective", "Insurance Provider": "Cigna", "Discharge Date": "2022-11-22","Hospital": "Hammond Ltd"},
        ])
    inserted, duplicates = insert_records(df,db=db,collectionname="collection_test")
    assert inserted == 2
    assert duplicates == 0


def test_insert_records_with_duplicates(mongo_test_db):
    db=mongo_test_db
    db["collection_test"].delete_many({})
    df = pd.DataFrame([
        {"Name": "John", "Age": 63, "Gender": "Male", "Billing Amount": 23762.2,"Medication": "Penicillin", "Test Results": "Normal", "Blood Type": "B+", "Doctor": "Denise Galloway","Date of Admission": "2022-11-15", "Room Number": 465, "Medical Condition": "Asthma","Admission Type": "Elective", "Insurance Provider": "Cigna", "Discharge Date": "2022-11-22","Hospital": "Hammond Ltd"},
        {"Name": "John", "Age": 63, "Gender": "Male", "Billing Amount": 23762.2,"Medication": "Penicillin", "Test Results": "Normal", "Blood Type": "B+", "Doctor": "Denise Galloway","Date of Admission": "2022-11-15", "Room Number": 465, "Medical Condition": "Asthma","Admission Type": "Elective", "Insurance Provider": "Cigna", "Discharge Date": "2022-11-22","Hospital": "Hammond Ltd"},
        ])
    inserted, duplicates = insert_records(df,db=db,collectionname="collection_test")
    assert inserted == 1
    assert duplicates == 1