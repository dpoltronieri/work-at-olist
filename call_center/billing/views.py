from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, permissions, renderers, viewsets, status
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from datetime import timedelta, datetime

from billing.models import Call, Charge
from billing.serializers import CallSerializer, BillSerializer, ChargeSerializer
from billing.chargeManager import ChargeManager


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
                serializer.validated_data['call_price'] = ChargeManager.getCharge(
                    running_call.start, serializer.initial_data['end'])
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


class get_period_bills(APIView):

    def get(self, request, source, year, month, format=None):
        if (Call.objects.filter(source=source).exists()
                and datetime(year, month, 1) < datetime.now(tz=None).replace(day=1)):
            calls = Call.objects.filter(source=source).filter(
                end__year=year).filter(end__month=month)
            serializer = BillSerializer(calls, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class get_last_period_bills(APIView):

    def get(self, request, source, format=None):
        if Call.objects.filter(source=source).exists():
            bill_period = datetime.now(tz=None).replace(
                day=1) - timedelta(days=1)
            calls = Call.objects.filter(source=source).filter(
                end__year=bill_period.year).filter(end__month=bill_period.month)
            serializer = BillSerializer(calls, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class get_post_charges(APIView):
    """
    List the most recent charge, or create a new charge.
    """

    def get(self, request, format=None):
        charge = Charge.objects.latest('enforced')
        serializer = ChargeSerializer(charge)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ChargeSerializer(data=request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
