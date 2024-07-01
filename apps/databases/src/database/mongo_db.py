from pymongo import MongoClient
from datetime import datetime
import json
import os

from src.schemas.answer import answer_schema
from src.schemas.survey import survey_schema

# Database class (only for insertion)
class MongoDB:

    ##### Constructor #####
    def __init__(self, 
                 database="db_name", 
                 username="user",
                 password="pass",
                 server="server",
                 port="27017"):

        # Paths
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.current_dir, '..', '..', 'data')

        # MongoDB
        # Connect to MongoDB
        self.client = MongoClient(f"mongodb://{username}:{password}@{server}:{port}/")
        self.db = self.client[database]

        # Create collections
        self.encuestas = self.create_or_update_collection("encuestas", survey_schema)
        self.encuestas.create_index([("NumeroEncuesta", 1)], unique=True)
        self.respuestas = self.create_or_update_collection("respuestas", answer_schema)

    ##### Methods #####
    ### MongoDB ###
    # Create or update collection
    def create_or_update_collection(self, collection_name, schema):
        schema_for_db = {'validator': schema}  
        if collection_name not in self.db.list_collection_names():
            self.db.create_collection(collection_name, **schema_for_db)
        else:
            self.db.command('collMod', collection_name, **schema_for_db)
        return self.db[collection_name]
    
    ### Insert data ###
    def insert_all_mongodb(self):
        self.insert_surveys_mongodb()
        self.insert_answers_mongodb()

    # Insert surveys
    def insert_surveys_mongodb(self):
        ruta = os.path.join(self.data_dir, 'surveys.jsonl')
        if self.encuestas.count_documents({}) == 0:
            with open(ruta, 'r') as file:
                for line in file:
                    data = json.loads(line)
                    data['FechaCreacion'] = datetime.fromisoformat(data['FechaCreacion'])
                    data['FechaActualizacion'] = datetime.fromisoformat(data['FechaActualizacion'])
                    self.encuestas.insert_one(data)

    # Insert answers
    def insert_answers_mongodb(self):
        ruta = os.path.join(self.data_dir, 'answers.jsonl')
        if self.respuestas.count_documents({}) == 0:
            with open(ruta, 'r') as file:
                for line in file:
                    data = json.loads(line)
                    data['FechaRealizado'] = datetime.fromisoformat(data['FechaRealizado'])
                    self.respuestas.insert_one(data)