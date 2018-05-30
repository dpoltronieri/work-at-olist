import time
from json import dumps

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from sqlalchemy import create_engine

db_connect = create_engine('sqlite:///callDB.db')
app = Flask(__name__)
api = Api(app)

# export FLASK_DEBUG=1


class Test(Resource):  # rota utilizada apenas no teste inicial e para testes basicos
    def get(self):
        return {"Teste": "Mensagem de Get"}

    def post(self):
        print(request.json)
        return {'Key1': request.json['key1'], 'key2:': request.json['key2']}

# curl http://127.0.0.1:5000/test
# curl -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/test


api.add_resource(Test, '/test')  # Route_Test


if __name__ == '__main__':
    app.run()
