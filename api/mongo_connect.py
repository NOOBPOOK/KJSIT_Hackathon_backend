from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values
import os

mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

# Create a new client and connect to the server
client = MongoClient(mongo_uri, server_api=ServerApi('1'))
DB = None

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    DB = client.get_default_database(db_name)
    print("Connected to KJSIT database")
except Exception as e:
    print(e)