from flask import Flask
from api.elastic_test import connect_elasticsearch
from api.insert_doc import insert_log

es = connect_elasticsearch()

with open('test/test_entry.json') as f:
    log_entry = f.read()
    f.close()

insert_log(log_entry)

app = Flask(__name__)


if __name__ == '__main__':
    app.run()
