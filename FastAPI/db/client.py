import os
from pymongo import MongoClient

#db_client = MongoClient().local

url_db = os.environ.get("MONGO_URL", "mongodb://admin:admin@ac-wfo7f4r-shard-00-00.bbmfnsa.mongodb.net:27017,ac-wfo7f4r-shard-00-01.bbmfnsa.mongodb.net:27017,ac-wfo7f4r-shard-00-02.bbmfnsa.mongodb.net:27017/?ssl=true&replicaSet=atlas-42f0h3-shard-0&authSource=admin&appName=PruebaMongoDBAtlas")

db_client = MongoClient(url_db).pruebas