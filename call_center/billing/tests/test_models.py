from django.test import TestCase
from billing.models import CallBill, CallStart, CallEnd
from django.utils import timezone


class ValidCallTest(TestCase):
    """
        Test cases containing successfull calls
    """

    def setUp(self):
        call_start_1 = CallStart.objects.create(
            source="991366272",
            destination="991970287",
            timestamp="2018-08-24 08:30:00+00:00",
        )
        call_start_2 = CallStart.objects.create(
            source="991970287",
            destination="991905858",
            timestamp="2018-08-24 12:30:00+00:00",
        )
        self.assertEqual(CallStart.objects.all().count(), 2)
        # print(call_start_1.id)
        # print(CallStart.objects.all().filter(source="991366272"))
        # print(CallStart.objects.all().count())
        # print(timezone.now())

    def tearDown(self):
        CallStart.objects.all().delete()
        self.assertEqual(CallStart.objects.all().count(), 0)
        self.assertEqual(CallEnd.objects.all().count(), 0)

    def test_vallid_call_ends(self):
        call_start_1 = CallStart.objects.get(id=1)
        call_start_2 = CallStart.objects.get(id=2)

        call_end_1 = CallEnd.objects.create(
            start=call_start_1,
            timestamp="2018-08-24 08:40:00+00:00",
        )

        call_end_2 = CallEnd.objects.create(
            start=call_start_2,
            timestamp="2018-08-24 08:40:00+00:00",
        )
        self.assertEqual(CallEnd.objects.all().count(), 2)
