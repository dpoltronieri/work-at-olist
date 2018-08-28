#!/bin/bash

SERVER=http://dpoltronieri.pythonanywhere.com/

curl -d '{"standing_charge": "0.36","minute_charge": "0.09","reduced_tariff_start": "22","reduced_tariff_end": "6"}' -H "Content-Type: application/json" -X POST $SERVER/charges/

curl -d '{"type": "start","source": "99988526423","destination": "9993468278","start": "2016-02-29T12:00:00Z","call_id": "70"}' -H "Content-Type: application/json" -X POST $SERVER/calls/
curl -d '{"type": "end","end": "2016-02-29T14:00:00Z","call_id": "70"}' -H "Content-Type: application/json" -X POST $SERVER/calls/

curl -d '{"type": "start","source": "99988526423","destination": "9993468278","start": "2017-12-12T15:07:13Z","call_id": "71"}' -H "Content-Type: application/json" -X POST $SERVER/calls/
curl -d '{"type": "end","end": "2017-12-12T15:14:56Z","call_id": "71"}' -H "Content-Type: application/json" -X POST $SERVER/calls/

curl -d '{"type": "start","source": "99988526423","destination": "9993468278","start": "2017-12-12T22:47:56Z","call_id": "72"}' -H "Content-Type: application/json" -X POST $SERVER/calls/
curl -d '{"type": "end","end": "2017-12-12T22:50:56Z","call_id": "72"}' -H "Content-Type: application/json" -X POST $SERVER/calls/

curl -d '{"type": "start","source": "99988526423","destination": "9993468278","start": "2017-12-12T21:57:13Z","call_id": "73"}' -H "Content-Type: application/json" -X POST $SERVER/calls/
curl -d '{"type": "end","end": "2017-12-12T22:10:56Z","call_id": "73"}' -H "Content-Type: application/json" -X POST $SERVER/calls/

curl -d '{"type": "start","source": "99988526423","destination": "9993468278","start": "2017-12-12T04:57:13Z","call_id": "74"}' -H "Content-Type: application/json" -X POST $SERVER/calls/
curl -d '{"type": "end","end": "2017-12-12T06:10:56Z","call_id": "74"}' -H "Content-Type: application/json" -X POST $SERVER/calls/

curl -d '{"type": "start","source": "99988526423","destination": "9993468278","start": "2017-12-12T21:57:13Z","call_id": "75"}' -H "Content-Type: application/json" -X POST $SERVER/calls/
curl -d '{"type": "end","end": "2017-12-13T22:10:56Z","call_id": "75"}' -H "Content-Type: application/json" -X POST $SERVER/calls/

curl -d '{"type": "start","source": "99988526423","destination": "9993468278","start": "2017-12-12T15:07:58Z","call_id": "76"}' -H "Content-Type: application/json" -X POST $SERVER/calls/
curl -d '{"type": "end","end": "2017-12-12T15:12:56Z","call_id": "76"}' -H "Content-Type: application/json" -X POST $SERVER/calls/

curl -d '{"type": "start","source": "99988526423","destination": "9993468278","start": "2018-02-28T21:57:13Z","call_id": "77"}' -H "Content-Type: application/json" -X POST $SERVER/calls/
curl -d '{"type": "end","end": "2018-03-01T22:10:56Z","call_id": "77"}' -H "Content-Type: application/json" -X POST $SERVER/calls/

curl -d '{"type": "start","source": "99988526423","destination": "9993468278","start": "2018-07-12T15:07:58Z","call_id": "78"}' -H "Content-Type: application/json" -X POST $SERVER/calls/
curl -d '{"type": "end","end": "2018-07-12T15:12:56Z","call_id": "78"}' -H "Content-Type: application/json" -X POST $SERVER/calls/
