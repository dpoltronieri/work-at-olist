from rest_framework import serializers
from billing.models import Call


class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = ('start', 'end', 'source', 'destination', 'call_id')
