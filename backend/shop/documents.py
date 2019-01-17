from elasticsearch import Elasticsearch, RequestsHttpConnection

from elasticsearch_dsl import (
    DocType,
    Date,
    Keyword,
    Text,
    Boolean,
    Integer
)


# Elasticsearch document class
class ProductIndex(DocType):
    pk = Integer()
    name = Text(analyzer='russian')
    slug = Text(fields={'raw': Keyword()})
    image = Text(fields={'raw': Keyword()})
    image_thumbnail = Text(fields={'raw': Keyword()})
    description = Text(analyzer='russian')
    price = Integer()
    stock = Integer()
    available = Boolean()
    created = Date()
    updated = Date()

    class Index:
        name = 'product'

    class Meta:
        index = 'product'


# RUN ONCE for Elasticsearch index 'product' creation
# es_client = Elasticsearch(
#     hosts=['localhost:9200'],
#     connection_class=RequestsHttpConnection
# )
# ProductIndex.init(using=es_client)
