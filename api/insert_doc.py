from api import elastic_test as et



def insert_log(log_entry, ind='test-index'):
    resp = et.es.index(index=ind, document=log_entry)
