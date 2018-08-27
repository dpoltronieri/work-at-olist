from rest_framework import serializers
from billing.models import Call


class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = ('call_id',
                  'start',
                  'end',
                  'source',
                  'destination',
                  'call_price')


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = ('start',
                  'end',
                  'destination',
                  'call_price')
