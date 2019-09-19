import logging
from pprint import pprint

from elasticsearch import Elasticsearch

logging.basicConfig(level=logging.ERROR)


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay connect!!')
    else:
        print('Aw, It could not connect.')
    return _es

def create_index(es_object, index_name='recipes'):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "salads": {
                "dynamic": "strict",
                "properties": {
                    "title": {
                        "type": "text"
                    },
                    "submitter": {
                        "type": "text"
                    },
                    "description": {
                        "type": "text"
                    },
                    "calories": {
                        "type": "integer"
                    },
                    "ingredients": {
                        "type": "nested",
                        "properties": {
                            "step": {
                                "type": "text"
                            }
                        }
                    },
                }
            }
        }
    }
    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
        created = True
    except Exception as e:
        print(str(e))
        created = False
    finally:
        return created

def store_record(es_object, index_name, record):
    is_stored = True
    try:
        outcome = es_object.index(index=index_name, doc_type='salads',
        body=record)
        print(outcome)
    except Exception as e:
        print('Error in indexing data')
        print(str(e))
        is_stored = False
    finally:
        return is_stored

def search(es_object, index_name, query):
    res = es_object.search(index=index_name, body=query)
    pprint(res,indent=2, depth=2, width=2)

