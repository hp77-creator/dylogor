import logging
import uuid

from api import elastic_test as et


def insert_log_in_db(log_entry, ind='test-index'):
    if et.es_status:
        new_id = uuid.uuid4()
        resp = et.es.index(index=ind, document=log_entry, id=new_id)
        #logging.info("Document inserted " + resp.body)
        return resp
    else:
        logging.error('DB Down')
        return None


def search_by_key(key, value, ind='test-index'):
    if et.es_status:
        resp = et.es.search(index=ind, query={key: value})

        display_logs(resp)
        return resp


def display_logs(resp):
    for hit in resp['hits']['hits']:
        print("%(level)s" % hit["_source"])