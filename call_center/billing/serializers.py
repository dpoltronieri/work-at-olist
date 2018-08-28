from rest_framework import serializers
from billing.models import Call, Charge


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


class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = ('standing_charge',
                  'minute_charge',
                  'reduced_tariff_start',
                  'reduced_tariff_end',
                  'enforced')
