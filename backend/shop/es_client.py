from elasticsearch import Elasticsearch, RequestsHttpConnection

es_client = Elasticsearch(
    hosts=['localhost:9200'],
    connection_class=RequestsHttpConnection
)
