import json
import logging

from flask import Flask, request, jsonify
from api.elastic_test import connect_elasticsearch
from api.elasticsearch_util import insert_log_in_db, search_by_key, search_by_regexp
from config.config_handling import get_config_value

app = Flask(__name__)
index_name = get_config_value('log', 'debug_index_name')


@app.route('/', methods=['GET', 'POST'])
def home_handler():
    if request.method == 'POST':
        log_entry = request.get_json()
        resp = insert_log_in_db(log_entry, index_name)  # set index name in config.ini
        print(resp)
        return resp['result']
    return 'Not a valid method'


@app.route('/search-all')
def search_all_handler():
    if request.method == 'GET':
        search_key = request.get_json()
        resp_doc = search_by_key("match_all", search_key)
        app.logger.info("doc result" + str(resp_doc))
        hits = resp_doc['hits']['hits']

        # Extract relevant data for JSON response
        response_data = [{'_id': hit['_id'], '_source': hit['_source']} for hit in hits]
        return jsonify(response_data)
    return 'Not a valid method'


@app.route('/search')
def search_key_handler():
    if request.method == 'GET':
        search_key = request.get_json()
        """
        search_key should be like
        {
            "level": "info"
        }
        in place of "level" any key can be used
        """
        resp_doc = search_by_key("match", search_key)
        app.logger.info("doc result" + str(resp_doc))
        hits = resp_doc['hits']['hits']

        # Extract relevant data for JSON response
        response_data = [{'_id': hit['_id'], '_source': hit['_source']} for hit in hits]
        return jsonify(response_data)
    return 'Not a valid method'


@app.route("/search-reg")
def search_regex_handler():
    """
            search_key should be like
            {
              "query": {
                "regexp": {
                  "your_field": {
                    "value": "your_regular_expression"
                  }
                }
              }
            }
            in place of "level" any key can be used
    """
    if request.method == 'GET':
        # regexp_query = request.get_json()
        query_params = request.args.get('q')
        regexp_query = json.loads(query_params)
        resp_doc = search_by_regexp(regexp_query)
        app.logger.info("doc result" + str(resp_doc))
        hits = resp_doc['hits']['hits']

        # Extract relevant data for JSON response
        response_data = [{'_id': hit['_id'], '_source': hit['_source']} for hit in hits]
        return jsonify(response_data)
    return 'Not a valid method'


if __name__ == '__main__':
    _flask_host = get_config_value('flask', 'host')
    _flask_port = get_config_value('flask', 'port')
    app.run(host=_flask_host, port=_flask_port)
