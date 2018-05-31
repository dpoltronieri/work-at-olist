import datetime
from json import dumps

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from sqlalchemy import create_engine

from chargeManager import ChargeManager

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


class CallCentral(Resource):
    def post(self):
        print(request.json)
        try:
            op = request.json["type"]
        except:
            return {"error": "Empty field"}

        try:
            conn = db_connect.connect()  # Conecata ao BD
        except Exception as e:
            return{"DBerror": e}
        '''
        {
          "id":  // Record unique identificator;
          "type":  // Indicate if it's a call "start" or "end" record;
          "timestamp":  // The timestamp of when the event occured;
          "call_id":  // Unique for each call record pair;
          "source":  // The subscriber phone number that originated the call;
          "destination":  // The phone number receiving the call.
        }
        '''
        if op == "start":
            try:
                _call_id = request.json["call_id"]
                _timestamp = request.json["timestamp"]
                _source = request.json["source"]
                _destination = request.json["destination"]
            except:
                return {"error": "Empty field"}

            query = conn.execute('insert into Calls (call_id,callTimestamp,source,destination) values(?,?,?,?)',
                                 _call_id,
                                 _timestamp,
                                 _source,
                                 _destination)
            return {'status': 'Call registered'}
        elif op == "end":
            return {"error": "Invalid Operation"}
        else:
            return {"error": "Invalid Operation"}

        return {"Key1": "Working"}

# curl -d '{"type":"start","call_id":"1", "timestamp":1527789900,"source":"123456","destination":"654321"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/record
# curl -d '{"type":"end","call_id":"1", "timestamp":1527790500,"source":"123456","destination":"654321"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/record
# these timestamps are 10 minutes apart


api.add_resource(Test, '/test')  # Route_Test
api.add_resource(CallCentral, '/record')  # Route_Test


if __name__ == '__main__':
    app.run()
