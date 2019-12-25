from elasticsearch import Elasticsearch, ElasticsearchException
from utils.config import EnvironmentManager
from utils.es import get_es_client

from django.conf import settings
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch


class ElasticSearchHelper(object):
    def __init__(self):
        self.env = EnvironmentManager()
        es_hosts = self.env.get_item("elasticsearch", "index_hosts")
        self.index_name = self.env.get_item("elasticsearch", "index_name")
        self.doc_type = self.env.get_item("elasticsearch", "document_type")
        es_nodes = []
        for host in es_hosts.split(','):
            host, port = host.split(':')
            es_nodes.append({
                "host": host,
                "port": int(port)
            })
        self.server = Elasticsearch(hosts=es_nodes)

    def index(self, document):
        if not isinstance(document, dict):
            raise ElasticsearchException("document should be an instance of a python dictionary")
        return self.server.index(index=self.index_name, doc_type=self.doc_type, body=document)

    def search(self, query):
        if not query:
            raise ElasticsearchException("Search Query should at least have a value")
        search = Search(using=get_es_client(), index=self.index_name).query(
            MultiMatch(query=query))
        return search

    def delete(self,doc_id):
        return self.server.delete(index=self.index_name,doc_type=self.doc_type,id=doc_id)