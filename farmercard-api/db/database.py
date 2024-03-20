from pymongo import MongoClient




# MongoDB connection details
MONGO_IP = "mongodb"
MONGO_PORT = 27017
MONGO_USERNAME = "user"
MONGO_PASSWORD = "pass"
MONGO_DB = "farmerdb"
MONGO_DETAILS = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_IP}:{MONGO_PORT}/{MONGO_DB}?authSource=admin&retryWrites=true&w=majority"




client = MongoClient(MONGO_DETAILS)
database = client[MONGO_DB]
farmer_collection = database.get_collection("farmers_collection")