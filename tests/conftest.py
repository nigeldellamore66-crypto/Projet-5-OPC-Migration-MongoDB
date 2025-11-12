from src.db import index_unique
import pytest
from pymongo import MongoClient
from src.db import get_db, index_unique  

@pytest.fixture
def mongo_test_db():
    # Connexion à la base Mongo de test
    db = get_db("mongodb://mongo_test:27017/", "db_test")
    collection = db["collection_test"]

    # Crée ou vérifie l'index unique
    index_unique(db, "collection_test")

    # Nettoie la collection avant les tests
    collection.delete_many({})
    list(collection.list_indexes())  # force la création effective de l’index
    print(list(collection.list_indexes()))

    yield db  # <-- permet d’utiliser cette DB dans les tests

    # Nettoie après les tests
    collection.delete_many({})

