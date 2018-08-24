from rest_framework import serializers
from billing.models import Call


class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = ('id', 'start', 'end', 'source', 'destination')
