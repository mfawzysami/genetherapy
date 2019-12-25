from core.db import MongoDBHelper
from core.indexing import ElasticSearchHelper

class CoreDBManager(object):

    def __init__(self):
        self.db_helper = MongoDBHelper()
        self.indexer = ElasticSearchHelper()

    def insert(self,db_name,collection_name,component):
        if not db_name or not collection_name:
            raise Exception("Database name and collection name should not be none or empty")
        client = self.db_helper.get_connection()
        db = client[db_name]
        collection = db[collection_name]
        inserted_id = collection.insert_one(component).inserted_id
        if inserted_id:
            component['id'] = str(inserted_id)
            component['doc_id'] = str(inserted_id)
            self.indexer.index(component)
        return inserted_id is not None , inserted_id

    def delete(self,db_name,collection_name,component_id):
        if not db_name or not collection_name:
            raise Exception("Database name and collection name should not be none or empty")
        self.indexer.delete(component_id)
        client = self.db_helper.get_connection()
        db = client[db_name]
        collection = db[collection_name]
        result = collection.delete_one({"_id":component_id})
        return result.deleted_count > 0





