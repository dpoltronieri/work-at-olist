from django.test import TestCase
from billing.models import CallBill, CallStart, CallEnd


class ValidCallTest(TestCase):
    """
        Test cases containing successfull calls
    """

    def setUp(self):
        call_start_1 = CallStart.objects.create(
            source="991366272",
            destination="991970287",
            timestamp="2018-08-24 08:30:00",
        )
        print(call_start_1.timestamp)

    def testSanity(self):
        self.assertEqual(1, 1)


# class PuppyTest(TestCase):
#     """ Test module for Puppy model """
#
#     def setUp(self):
#         Puppy.objects.create(
#             name='Casper', age=3, breed='Bull Dog', color='Black')
#         Puppy.objects.create(
#             name='Muffin', age=1, breed='Gradane', color='Brown')
#
#     def test_puppy_breed(self):
#         puppy_casper = Puppy.objects.get(name='Casper')
#         puppy_muffin = Puppy.objects.get(name='Muffin')
#         self.assertEqual(
#             puppy_casper.get_breed(), "Casper belongs to Bull Dog breed.")
#         self.assertEqual(
#             puppy_muffin.get_breed(), "Muffin belongs to Gradane breed.")
