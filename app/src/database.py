from pymongo import MongoClient

mongo_url = "mongodb://root:example@localhost:27017/"
db_client = MongoClient(mongo_url)