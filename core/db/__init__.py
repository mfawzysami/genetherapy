import pymongo as db
from utils.config import EnvironmentManager

class MongoDBHelper(object):
    def __init__(self):
        env = EnvironmentManager()
        self.host = env.get_item("mongodb","host")
        self.port = int(env.get_item("mongodb","port"))

    def connect(self):
        self.client = db.MongoClient(host=self.host,port=self.port)

    def is_connected(self):
        return self.client is not None

    def get_connection(self):
        return self.client