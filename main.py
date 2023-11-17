from flask import Flask
from api.elastic_test import connect_elasticsearch

es = connect_elasticsearch()

app = Flask(__name__)


if __name__ == '__main__':
    app.run()