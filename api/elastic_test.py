import logging

from elasticsearch import Elasticsearch
from config.config_handling import get_config_value


def connect_elasticsearch(**kwargs):
    _es_config = get_config_value('elastic', 'es_host')
    _es_hosts = [_es_config]
    _es_username = get_config_value('elastic', 'es_user')
    _es_passkey = get_config_value('elastic', 'es_pass')
    _es_ca_cert = get_config_value('elastic', 'ca_secret')
    if 'hosts' in kwargs.keys():
        _es_hosts = kwargs['hosts']

    _es_obj = None
    # ensure that you pass certs as well when using https
    _es_obj = Elasticsearch([{'host': 'localhost', 'port' : 9200, 'scheme': 'https'}], ssl_assert_fingerprint=_es_ca_cert, basic_auth=(_es_username, _es_passkey), timeout=10)
    _es_status = _es_obj.ping()
    if _es_status:
        logging.info('ElasticSearch connected')
        logging.debug(_es_obj.info())
    else:
        logging.error('ElasticSearch could not be connected')

    return _es_obj, _es_status


es, es_status = connect_elasticsearch()
