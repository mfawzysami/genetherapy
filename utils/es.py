from elasticsearch import Elasticsearch

from utils.config import EnvironmentManager


def get_es_client():
    envManager = EnvironmentManager()
    es_hosts = envManager.get_item("elasticsearch", "index_hosts")
    es_nodes = []
    for host in es_hosts.split(','):
        host, port = host.split(':')
        es_nodes.append({
            "host": host,
            "port": int(port)
        })
    es = Elasticsearch(hosts=es_nodes)
    return es