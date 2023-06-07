from pymongo import MongoClient
from util.color_log import Log

class Mongo:
    def __init__(self, host='localhost', port=27017, username=None, password=None, db_name=None):
        self.client = MongoClient(host, port, username=username, password=password)
        self.db = self.client[db_name]
        self.log = Log()

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def insert_one(self, collection_name, document):
        self.log.sql(f'mongo insert_one {collection_name}')
        collection = self.get_collection(collection_name)
        return collection.insert_one(document)

    def insert_many(self, collection_name, documents):
        self.log.sql(f'mongo insert_many {collection_name}')
        collection = self.get_collection(collection_name)
        return collection.insert_many(documents)

    def find(self, collection_name, query=None):
        collection = self.get_collection(collection_name)
        return collection.find(query)

    def find_one(self, collection_name, query=None):
        collection = self.get_collection(collection_name)
        return collection.find_one(query)

    def update_one(self, collection_name, query, update):
        collection = self.get_collection(collection_name)
        return collection.update_one(query, update)

    def update_many(self, collection_name, query, update):
        collection = self.get_collection(collection_name)
        return collection.update_many(query, update)

    def delete_one(self, collection_name, query):
        collection = self.get_collection(collection_name)
        return collection.delete_one(query)

    def delete_many(self, collection_name, query):
        collection = self.get_collection(collection_name)
        return collection.delete_many(query)
