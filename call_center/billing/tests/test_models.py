from django.test import TestCase
from billing.models import Call
from django.utils import timezone
from datetime import timedelta


class ValidCallTest(TestCase):
    """
        Test cases containing successfull calls
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
        )
        self.assertEqual(Call.objects.all().count(), 2)
        # print(call_start_1.id)
        # print(CallStart.objects.all().filter(source="991366272"))
        # print(CallStart.objects.all().count())
        # print(timezone.now())

    def test_vallid_call_ends_manually(self):
        call_1 = Call.objects.get(id=1)

        call_1.end = "2018-08-24 08:40:00+00:00"
        call_1.save()

        self.assertEqual(Call.objects.all().count(), 2)

    def test_vallid_call_ends_by_function(self):
        call_2 = Call.objects.get(id=2)

        call_2.end_call("2018-08-24 12:40:00+00:00")
        self.assertEqual(call_2.duration, datetime.timedelta(minutes=10))
        self.assertEqual(Call.objects.all().count(), 2)
