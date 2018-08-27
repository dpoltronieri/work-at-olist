from django.test import TestCase
from datetime import timedelta, datetime

from billing.chargeManager import ChargeManager
from billing.models import Charge


class testChargeManager(TestCase):

    def setUp(self):
        Charge.objects.create(
            standing_charge=0.36,
            minute_charge=0.09,
            reduced_tariff_start=22,
            reduced_tariff_end=6
        )

    def test_same_day_normal_call(self):

        testTime1 = datetime(
            year=2018, month=2, day=5,
            hour=Charge.objects.latest('enforced').reduced_tariff_end, minute=10)
        testTime2 = datetime(
            year=2018, month=2, day=5,
            hour=Charge.objects.latest('enforced').reduced_tariff_end, minute=20)
        testCharge = ChargeManager.getCharge(testTime1, testTime2)

        expectedCharge = int(
            (Charge.objects.latest('enforced').standing_charge
             + Charge.objects.latest('enforced').minute_charge * 10)
            * 100) / 100
        self.assertEqual(testCharge, expectedCharge)

    def test_same_day_reduced_call(self):

        testTime1 = datetime(
            year=2018, month=2, day=5, hour=Charge.objects.latest('enforced').reduced_tariff_start, minute=10)
        testTime2 = datetime(
            year=2018, month=2, day=5, hour=Charge.objects.latest('enforced').reduced_tariff_start, minute=20)
        testCharge = ChargeManager.getCharge(testTime1, testTime2)

        expectedCharge = Charge.objects.latest('enforced').standing_charge
        self.assertEqual(testCharge, expectedCharge)

    def test_same_day_normal_half_reduced_call(self):

        testTime1 = datetime(
            year=2018, month=2, day=5, hour=Charge.objects.latest('enforced').reduced_tariff_start - 1, minute=50)
        testTime2 = datetime(
            year=2018, month=2, day=5, hour=Charge.objects.latest('enforced').reduced_tariff_start, minute=10)
        testCharge = ChargeManager.getCharge(
            testTime1, testTime2)

        expectedCharge = int(
            (Charge.objects.latest('enforced').standing_charge + Charge.objects.latest('enforced').minute_charge * 10) * 100) / 100
        self.assertEqual(testCharge, expectedCharge)

    def test_same_day_reduced_half_normal_call(self):

        testTime1 = datetime(
            year=2018, month=2, day=5, hour=Charge.objects.latest('enforced').reduced_tariff_end - 1, minute=50)
        testTime2 = datetime(
            year=2018, month=2, day=5, hour=Charge.objects.latest('enforced').reduced_tariff_end, minute=10)
        testCharge = ChargeManager.getCharge(
            testTime1, testTime2)

        expectedCharge = int(
            (Charge.objects.latest('enforced').standing_charge + Charge.objects.latest('enforced').minute_charge * 10) * 100) / 100
        self.assertEqual(testCharge, expectedCharge)

    def test_next_day_over_reducedTariffTime_call(self):

        testTime1 = datetime(
            year=2018, month=2, day=5, hour=Charge.objects.latest('enforced').reduced_tariff_start - 1, minute=50)
        testTime2 = datetime(
            year=2018, month=2, day=6, hour=Charge.objects.latest('enforced').reduced_tariff_end, minute=10)
        testCharge = ChargeManager.getCharge(
            testTime1, testTime2)

        expectedCharge = int(
            (Charge.objects.latest('enforced').standing_charge + Charge.objects.latest('enforced').minute_charge * 20) * 100) / 100
        self.assertEqual(testCharge, expectedCharge)

    def test_next_day_under_reducedTariffTime_call(self):

        testTime1 = datetime(
            year=2018, month=2, day=5, hour=Charge.objects.latest('enforced').reduced_tariff_start, minute=10)
        testTime2 = datetime(
            year=2018, month=2, day=6, hour=Charge.objects.latest('enforced').reduced_tariff_end - 1, minute=10)
        testCharge = ChargeManager.getCharge(
            testTime1, testTime2)

        expectedCharge = int(
            (Charge.objects.latest('enforced').standing_charge + Charge.objects.latest('enforced').minute_charge * 0) * 100) / 100
        self.assertEqual(testCharge, expectedCharge)

    def test_incorrect_call_order(self):

        testTime1 = datetime(
            year=2018, month=2, day=5, hour=Charge.objects.latest('enforced').reduced_tariff_start, minute=10)
        testTime2 = datetime(
            year=2018, month=2, day=6, hour=Charge.objects.latest('enforced').reduced_tariff_end - 1, minute=10)
        # self.assertRaises(ValueError, ChargeManager.getCharge(testTime2, testTime1))
        with self.assertRaises(ValueError):
            ChargeManager.getCharge(testTime2, testTime1)
