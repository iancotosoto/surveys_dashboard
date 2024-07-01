import os

from src.database.mongo_db import MongoDB

# Constants
DB_NAME = os.getenv("DB_NAME")
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_SERVER = os.getenv("MONGODB_SERVER")
MONGODB_PORT = os.getenv("MONGODB_PORT")

# MongoDB data insertion
db = MongoDB(database=DB_NAME, 
             username=MONGODB_USERNAME, 
             password=MONGODB_PASSWORD, 
             server=MONGODB_SERVER, 
             port=MONGODB_PORT)

db.insert_all_mongodb()