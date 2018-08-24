import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from billing.models import Call

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
        )
        call_2 = Call.objects.create(
            source="991970287",
            destination="991905858",
            start="2018-08-24 12:30:00+00:00",
            end="2018-08-24 12:40:00+00:00",
        )

    def test_get_all_completed_calls(self):
        # get API response
        response = client.get(reverse('get_post_calls'))
        # get data from db
        calls = Call.objects.all().exclude(end=Null)
        # serializer = PuppySerializer(puppies, many=True)
        # self.assertEqual(response.data, serializer.data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
