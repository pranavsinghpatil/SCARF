from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "readify_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "documents")

def get_db_client():
    if not MONGODB_URI:
        return None
    return MongoClient(MONGODB_URI)

def get_collection():
    client = get_db_client()
    if not client:
        return None
    db = client[DB_NAME]
    return db[COLLECTION_NAME]

def test_connection():
    try:
        client = get_db_client()
        if client:
            client.admin.command('ping')
            return True
    except Exception as e:
        return False
