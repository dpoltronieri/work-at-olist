from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, permissions, renderers, viewsets, status
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from billing.models import Call
from billing.serializers import CallSerializer


class get_post_calls(APIView):
    """
    List all calls, or create a new call.
    """

    def get(self, request, format=None):
        calls = Call.objects.all()
        serializer = CallSerializer(calls, many=True)
        return Response(serializer.data)
