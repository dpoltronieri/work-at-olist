import datetime
import unittest

import chargeManager


class testChargeManager(unittest.TestCase):

    standingCharge = 0.36
    minuteCharge = 0.09
    reducedTariffStart = 22
    reducedTariffEnd = 6
    chargeManagerObject = chargeManager.ChargeManager(standingCharge, minuteCharge, reducedTariffStart, reducedTariffEnd)

    def test_same_day_reduced_call(self):

        testTime1 = datetime.datetime(year=2018, month=2, day=5, hour=self.__class__.reducedTariffStart, minute=10)
        testTime2 = datetime.datetime(year=2018, month=2, day=5, hour=self.__class__.reducedTariffStart, minute=20)
        testCharge = self.__class__.chargeManagerObject.getCharge(testTime1, testTime2)

        self.assertEqual(testCharge, self.__class__.standingCharge)
