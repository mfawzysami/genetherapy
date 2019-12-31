from core.db import MongoDBHelper
from core.indexing import ElasticSearchHelper
from core.tasks import perform_indexing


class CoreDBManager(object):

    def __init__(self):
        self.db_helper = MongoDBHelper()
        self.db_helper.connect()
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
            del component['_id']
            try:
                perform_indexing.delay(component)
            except Exception as e:
                pass

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





