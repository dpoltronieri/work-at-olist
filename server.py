import calendar
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
    standingCharge = 0.36
    minuteCharge = 0.09
    reducedTariffStart = 22
    reducedTariffEnd = 6
    chargeManagerObject = ChargeManager(standingCharge, minuteCharge, reducedTariffStart, reducedTariffEnd)

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
                _timestamp = ChargeManager.formatTime(_timestamp).timestamp()
                _source = request.json["source"]
                _destination = request.json["destination"]
            except:
                return {"error": "Empty field"}

            query = conn.execute('insert into Calls (call_id,callTimestamp,source,destination) values(?,?,?,?)',
                                 _call_id,
                                 _timestamp,
                                 _source,
                                 _destination)

            return {'status': "Call registered"}

        elif op == "end":
            try:
                _call_id = request.json["call_id"]
                _endTimestamp = request.json["timestamp"]
                _endTimestamp = ChargeManager.formatTime(_endTimestamp).timestamp()
            except:
                return {"error": "Empty field"}

            __startTimestamp = conn.execute('select callTimestamp from Calls where call_id = ?;', _call_id)
            _startTimestamp = __startTimestamp.fetchone()[0]
            if not (_startTimestamp):
                return {"error": "This call does not exist"}

            print("Valores: ", _startTimestamp, _endTimestamp, "tipos: ", type(_startTimestamp), type(_endTimestamp))
            _callValue = self.__class__.chargeManagerObject.getCharge(initialTime=float(_startTimestamp), finalTime=float(_endTimestamp))

            query = conn.execute('update Calls set callEndTimestamp = ?, callValue = ? where call_id = ?',
                                 _endTimestamp,
                                 _callValue,
                                 _call_id)

            return {"status": "Call registered"}
        else:
            return {"error": "Invalid Operation"}

# curl -d '{"type":"start","call_id":"1", "timestamp":1527789900,"source":"123456","destination":"654321"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/record
# curl -d '{"type":"end","call_id":"1", "timestamp":1527790500}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/record
# curl -d '{"type":"start","call_id":"4", "timestamp":"2016-05-29T12:00:00Z","source":"123456","destination":"654321"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/record
# curl -d '{"type":"end","call_id":"4", "timestamp":"2016-05-29T14:00:00Z"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/record
# these timestamps are 10 minutes apart


class BillCentral(Resource):

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

        if op == "last":
            try:
                _subscriber = request.json["subscriber"]
            except:
                return {"error": "Empty field"}

            _lastPeriodEnd = datetime.datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(seconds=1)
            _lastPeriodStart = _lastPeriodEnd.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            _periodStart = _lastPeriodStart.timestamp()
            _periodEnd = _lastPeriodEnd.timestamp()

        elif op == "period":
            try:
                _subscriber = request.json["subscriber"]
                _periodStartMonth = request.json["periodStartMonth"]
                _periodStartYear = request.json["periodStartYear"]
                _periodEndMonth = request.json["periodEndMonth"]
                _periodEndYear = request.json["periodEndYear"]
            except:
                return {"error": "Empty field"}

            if all(map(lambda k: type(k) is int,
                       [_periodStartMonth, _periodStartYear,
                        _periodEndMonth, _periodEndYear])):

                _periodStart = datetime.datetime(year=_periodStartYear,
                                                 month=_periodStartMonth,
                                                 day=1, hour=0, minute=0)
                _periodEnd = datetime.datetime(year=_periodEndYear,
                                               month=(_periodEndMonth + 1) % 12,
                                               day=1, hour=0, minute=0) - datetime.timedelta(seconds=1)
            else:
                return {"error": "Periods must all be interger numbers"}

        _periodStart = _periodStart.timestamp()
        _periodEnd = _periodEnd.timestamp()
        _query = conn.execute('select call_id, destination, callTimestamp, callEndTimestamp, callValue from Calls where source = ? and callTimestamp between ? and ?;',
                              _subscriber,
                              _periodStart,
                              _periodEnd)

        calls_json = {}
        bill_json = {}
        for call in _query.fetchall():
            calls_json["Destination"] = call[1]
            # TODO check this again
            calls_json["Start"] = datetime.datetime.fromtimestamp(call[2]).isoformat()
            calls_json["End"] = datetime.datetime.fromtimestamp(call[3]).isoformat()
            calls_json["Value"] = call[4]
            bill_json[str(call[0])] = calls_json
            calls_json = {}  # limpa o temporario

        return bill_json

# curl -d '{"type":"period","subscriber":"123456","periodStartMonth":1,"periodStartYear":2018,"periodEndMonth":2,"periodEndYear":2018}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/bill
# curl -d '{"type":"last","subscriber":"123456"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/bill


api.add_resource(Test, '/test')  # Route_Test
api.add_resource(CallCentral, '/record')
api.add_resource(BillCentral, '/bill')


if __name__ == '__main__':
    app.run()
