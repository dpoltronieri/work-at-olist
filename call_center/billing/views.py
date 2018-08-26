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
        calls = Call.objects.all().exclude(end=None)
        serializer = CallSerializer(calls, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if request.data['type'] == 'start':
            serializer = CallSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # TODO: Evaluate refactor for this as PUT method
        elif request.data['type'] == 'end':

            try:
                running_call = Call.objects.get(
                    call_id=request.data['call_id'])
            except Call.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except KeyError:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            serializer = CallSerializer(
                running_call, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class get_incomplete_calls(APIView):
    """
    List only incomplete calls
    """

    def get(self, request, format=None):
        calls = Call.objects.all().filter(end=None)
        serializer = CallSerializer(calls, many=True)
        return Response(serializer.data)
