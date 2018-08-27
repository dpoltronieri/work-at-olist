from django.test import TestCase
from datetime import timedelta, datetime

from call_center.chargeManager import chargeManager
from billing.models import Charge
from billing.serializers import ChargeSerializer


class testChargeManager(TestCase):

    # standingCharge = 0.36
    # minuteCharge = 0.09
    # reducedTariffStart = 22
    # reducedTariffEnd = 6
    # chargeManagerObject = chargeManager.ChargeManager(
    #     standingCharge, minuteCharge, reducedTariffStart, reducedTariffEnd)

    def test_same_day_normal_call(self):

        testTime1 = datetime.datetime(
            year=2018, month=2, day=5,
            hour=Charge.objects.latest('enforced')['reducedTariffEnd'], minute=10)
        testTime2 = datetime.datetime(
            year=2018, month=2, day=5,
            hour=Charge.objects.latest('enforced')['reducedTariffEnd'], minute=20)
        testCharge = chargeManager.getCharge(testTime1, testTime2)

        expectedCharge = int(
            (Charge.objects.latest('enforced')['standingCharge']
             + Charge.objects.latest('enforced')['minuteCharge'] * 10)
            * 100) / 100
        self.assertEqual(testCharge, expectedCharge)

    # def test_same_day_reduced_call(self):
    #
    #     testTime1 = datetime.datetime(
    #         year=2018, month=2, day=5, hour=self.__class__.reducedTariffStart, minute=10)
    #     testTime2 = datetime.datetime(
    #         year=2018, month=2, day=5, hour=self.__class__.reducedTariffStart, minute=20)
    #     testCharge = self.__class__.chargeManagerObject.getCharge(
    #         testTime1, testTime2)
    #
    #     expectedCharge = self.__class__.standingCharge
    #     self.assertEqual(testCharge, expectedCharge)
    #
    # def test_same_day_normal_half_reduced_call(self):
    #
    #     testTime1 = datetime.datetime(
    #         year=2018, month=2, day=5, hour=self.__class__.reducedTariffStart - 1, minute=50)
    #     testTime2 = datetime.datetime(
    #         year=2018, month=2, day=5, hour=self.__class__.reducedTariffStart, minute=10)
    #     testCharge = self.__class__.chargeManagerObject.getCharge(
    #         testTime1, testTime2)
    #
    #     expectedCharge = int(
    #         (self.__class__.standingCharge + self.__class__.minuteCharge * 10) * 100) / 100
    #     self.assertEqual(testCharge, expectedCharge)
    #
    # def test_same_day_reduced_half_normal_call(self):
    #
    #     testTime1 = datetime.datetime(
    #         year=2018, month=2, day=5, hour=self.__class__.reducedTariffEnd - 1, minute=50)
    #     testTime2 = datetime.datetime(
    #         year=2018, month=2, day=5, hour=self.__class__.reducedTariffEnd, minute=10)
    #     testCharge = self.__class__.chargeManagerObject.getCharge(
    #         testTime1, testTime2)
    #
    #     expectedCharge = int(
    #         (self.__class__.standingCharge + self.__class__.minuteCharge * 10) * 100) / 100
    #     self.assertEqual(testCharge, expectedCharge)
    #
    # def test_next_day_over_reducedTariffTime_call(self):
    #
    #     testTime1 = datetime.datetime(
    #         year=2018, month=2, day=5, hour=self.__class__.reducedTariffStart - 1, minute=50)
    #     testTime2 = datetime.datetime(
    #         year=2018, month=2, day=6, hour=self.__class__.reducedTariffEnd, minute=10)
    #     testCharge = self.__class__.chargeManagerObject.getCharge(
    #         testTime1, testTime2)
    #
    #     expectedCharge = int(
    #         (self.__class__.standingCharge + self.__class__.minuteCharge * 20) * 100) / 100
    #     self.assertEqual(testCharge, expectedCharge)
    #
    # def test_next_day_under_reducedTariffTime_call(self):
    #
    #     testTime1 = datetime.datetime(
    #         year=2018, month=2, day=5, hour=self.__class__.reducedTariffStart, minute=10)
    #     testTime2 = datetime.datetime(
    #         year=2018, month=2, day=6, hour=self.__class__.reducedTariffEnd - 1, minute=10)
    #     testCharge = self.__class__.chargeManagerObject.getCharge(
    #         testTime1, testTime2)
    #
    #     expectedCharge = int(
    #         (self.__class__.standingCharge + self.__class__.minuteCharge * 0) * 100) / 100
    #     self.assertEqual(testCharge, expectedCharge)
    #
    # def test_incorrect_call_order(self):
    #
    #     testTime1 = datetime.datetime(
    #         year=2018, month=2, day=5, hour=self.__class__.reducedTariffStart, minute=10)
    #     testTime2 = datetime.datetime(
    #         year=2018, month=2, day=6, hour=self.__class__.reducedTariffEnd - 1, minute=10)
    #     # self.assertRaises(ValueError, self.__class__.chargeManagerObject.getCharge(testTime2, testTime1))
    #     with self.assertRaises(ValueError):
    #         self.__class__.chargeManagerObject.getCharge(testTime2, testTime1)
