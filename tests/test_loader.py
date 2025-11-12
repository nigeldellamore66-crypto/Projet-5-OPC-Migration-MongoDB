import pandas as pd
import pytest
from src.loader import load_batch, clean_dataframe

# --------------------------
# Test clean_dataframe
# --------------------------

def test_clean_dataframe_basic():
    df = pd.DataFrame({"Name": ["  jean  "], "Billing Amount": [10.457]})
    cleaned = clean_dataframe(df)

    assert cleaned["Name"][0] == "Jean"
    assert cleaned["Billing Amount"][0] == 10.46

def test_clean_dataframe_missing_columns():
    df = pd.DataFrame({"Other": [123]})
    cleaned = clean_dataframe(df)
    # Renvoie le DataFrame sans erreur
    assert "Other" in cleaned

# --------------------------
# Test load_batch
# --------------------------

def test_load_batch_csv(tmp_path):
    # Création d'un fichier CSV temporaire
    file = tmp_path / "test.csv"
    file.write_text("Name,Billing Amount\nJean,10.457")
    
    df = load_batch(str(tmp_path))
    
    assert df["Name"][0] == "Jean"
    assert df["Billing Amount"][0] == 10.46

def test_load_batch_json(tmp_path):
    # Création d'un fichier JSON temporaire
    file = tmp_path / "test.json"
    file.write_text('[{"Name":"Jean","Billing Amount":10.457}]')
    
    df = load_batch(str(tmp_path))
    
    assert df["Name"][0] == "Jean"
    assert df["Billing Amount"][0] == 10.46

def test_load_batch_no_files(tmp_path):
    # Aucun fichier CSV ou JSON
    with pytest.raises(FileNotFoundError):
        load_batch(str(tmp_path))

def test_load_batch_multiple_files(tmp_path, capsys):
    # Plusieurs fichiers CSV
    file1 = tmp_path / "a.csv"
    file1.write_text("Name,Billing Amount\nJean,10.457")
    file2 = tmp_path / "b.csv"
    file2.write_text("Name,Billing Amount\nPaul,12.345")

    df = load_batch(str(tmp_path))
    
    captured = capsys.readouterr()
    assert "Plusieurs fichiers trouvés" in captured.out
    assert df["Name"][0] == "Jean"
