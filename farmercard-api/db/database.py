from pymongo import MongoClient
from pymongo.database import Database
from fastapi import Depends
from pymongo.collection import Collection

# MongoDB connection details
MONGO_IP = "mongodb"
MONGO_PORT = 27017
MONGO_USERNAME = "user"
MONGO_PASSWORD = "pass"
MONGO_DB = "farmerdb"
MONGO_DETAILS = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_IP}:{MONGO_PORT}/{MONGO_DB}?authSource=admin&retryWrites=true&w=majority"

# Function to get the MongoDB database instance
def get_database() -> Database:
    client = MongoClient(MONGO_DETAILS)
    return client[MONGO_DB]

# Dependency to get the collection instance
def get_farmer_collection() -> Collection:
    db = get_database()
    return db["farmers_collection"]