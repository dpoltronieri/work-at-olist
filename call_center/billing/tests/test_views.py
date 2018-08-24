import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse

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
            call_id=50,
        )
        call_2 = Call.objects.create(
            source="991970287",
            destination="991905858",
            start="2018-08-24 12:30:00+00:00",
            end="2018-08-24 12:40:00+00:00",
            call_id=51,
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


class CreateNewCallTest(TestCase):
    """
    Test module for inserting a new start call
    """

    def setUp(self):
        self.valid_payload = {
            'source': "991366272",
            'destination': "991970287",
            'start': "2018-08-24 08:30:00+00:00",
            'call_id': '50'
        }

        self.invalid_payloads = ({
            'source': "",
            'destination': "991970287",
            'start': "2018-08-24 08:30:00+00:00",
            'call_id': '50'
        }, {
            'source': "991366272",
            'destination': "",
            'start': "2018-08-24 08:30:00+00:00",
            'call_id': '50'
        }, {
            'source': "991366272",
            'destination': "991970287",
            'start': "",
            'call_id': '50'
        }, {
            'source': "991366272",
            'destination': "991970287",
            'start': "2018-08-24 08:30:00+00:00",
            'call_id': ''
        },
        )

    def test_create_valid_call(self):
        response = client.post(
            reverse('get_post_calls'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_call(self):
        for payload in self.invalid_payloads:
            response = client.post(
                reverse('get_post_calls'),
                data=json.dumps(payload),
                content_type='application/json'
            )
            self.assertEqual(response.status_code,
                             status.HTTP_400_BAD_REQUEST, "Failed Payload: {}".format(payload))


class FinishCallTest(TestCase):
    """
    Test module for completing a call from begining to end and billing
    """

    def setUp(self):
        # IDEA: multiple valid start and end payloads
        self.valid_payload = {
            'end': "2018-08-24 08:30:00+00:00",
            'call_id': '50'
        }
        self.invalid_payloads = ({
            'end': "",
            'call_id': '50'
        }, {
            'end': "2018-08-24 08:30:00+00:00",
            'call_id': ''
        })

    def test_create_valid_call(self):
        pass

    def test_create_invalid_call(self):
        pass
