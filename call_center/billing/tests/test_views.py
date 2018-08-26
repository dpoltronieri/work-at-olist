import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from datetime import timedelta, datetime

from billing.models import Call
from billing.serializers import CallSerializer

# initialize the APIClient app
client = Client()


class GetAllCallsTest(TestCase):
    """
    Test module for GET calls API
    """

    def setUp(self):
        call_1 = Call.objects.create(
            source="991366272",
            destination="991970287",
            start="2018-08-24 08:30:00+00:00",
            call_id=30
        )
        call_2 = Call.objects.create(
            source="991970287",
            destination="991905858",
            start="2018-08-24 12:30:00+00:00",
            end="2018-08-24 12:40:00+00:00",
            call_id=31
        )

    def test_get_all_completed_calls(self):
        # get API response
        response = client.get(reverse('get_post_calls'))
        # get data from db, exluding unfinished calls
        calls = Call.objects.all().exclude(end=None)
        serializer = CallSerializer(calls, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_incomplete_calls(self):
        # get API response
        response = client.get(reverse('get_incomplete_calls'))
        # get data from db, exluding unfinished calls
        calls = Call.objects.all().filter(end=None)
        serializer = CallSerializer(calls, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class POSTCallTest(TestCase):
    """
    Test module for completing a call from begining to end
    """

    def setUp(self):
        self.end_response = ""
        self.start_response = ""
        # IDEA: multiple valid start and end payloads
        self.valid_start_payload = {
            'type': "start",
            'source': "991366272",
            'destination': "991970287",
            'start': "2018-08-24 08:30:00+00:00",
            'call_id': "10"
        }
        self.valid_end_payload = {
            'type': "end",
            'end': "2018-08-24 08:40:00+00:00",
            'call_id': "10"
        }

        self.invalid_start_payloads = ({
            'type': "start",
            'source': "",
            'destination': "991970287",
            'start': "2018-08-24 08:30:00+00:00",
            'call_id': "10"
        }, {
            'type': "start",
            'source': "991366272",
            'destination': "",
            'start': "2018-08-24 08:30:00+00:00",
            'call_id': "10"
        }, {
            'type': "start",
            'source': "991366272",
            'destination': "991970287",
            'start': "",
            'call_id': "10"
        }, {
            'type': "start",
            'source': "991366272",
            'destination': "991970287",
            'start': "2018-08-24 08:30:00+00:00",
            'call_id': ""
        },)
        self.invalid_end_payloads = ({
            'type': "end",
            'end': "2018-08-24 08:40:00+00:00"
        }, {
            'type': "end",
            'end': "",
            'call_id': "10"
        }, {
            'type': "",
            'end': "2018-08-24 08:40:00+00:00",
            'call_id': "10"
        },
        )

    def test_start_valid_call(self):
        self.start_response = client.post(
            reverse('get_post_calls'),
            data=json.dumps(self.valid_start_payload),
            content_type='application/json'
        )
        self.assertEqual(self.start_response.status_code,
                         status.HTTP_201_CREATED)

    def test_start_invalid_call(self):
        for payload in self.invalid_start_payloads:
            self.start_response = client.post(
                reverse('get_post_calls'),
                data=json.dumps(payload),
                content_type='application/json'
            )
            self.assertEqual(self.start_response.status_code,
                             status.HTTP_400_BAD_REQUEST, "Failed Payload: {}".format(payload))

    def test_start_end_valid_call(self):
        # test looking through the client side
        self.start_response = client.post(
            reverse('get_post_calls'),
            data=json.dumps(self.valid_start_payload),
            content_type='application/json'
        )
        self.assertEqual(self.start_response.status_code,
                         status.HTTP_201_CREATED)

        self.end_response = client.post(
            reverse('get_post_calls'),
            data=json.dumps(self.valid_end_payload),
            content_type='application/json'
        )
        self.assertEqual(self.end_response.status_code,
                         status.HTTP_201_CREATED)

    def test_invalid_end_call(self):
        self.start_response = client.post(
            reverse('get_post_calls'),
            data=json.dumps(self.valid_start_payload),
            content_type='application/json'
        )
        self.assertEqual(self.start_response.status_code,
                         status.HTTP_201_CREATED)

        for payload in self.invalid_end_payloads:
            self.end_response = client.post(
                reverse('get_post_calls'),
                data=json.dumps(payload),
                content_type='application/json'
            )
            self.assertEqual(self.end_response.status_code,
                             status.HTTP_400_BAD_REQUEST, "Failed Payload: {}".format(payload))

    def test_billing_10_minutes_no_reduced_tariff(self):
        self.test_start_end_valid_call()

        self.assertEqual(self.end_response.data['billable_minutes'], 10)
        self.assertEqual(self.end_response.data['call_price'], 1.26)
        print(self.end_response.data)
