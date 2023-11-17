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

    if _es_obj.ping():
        print('Yay Connect')
        print(_es_obj.info())
    else:
        print('Aww it could not connect')

    return _es_obj


es = connect_elasticsearch()
