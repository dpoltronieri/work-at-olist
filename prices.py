import calendar
import time
from abc import ABCMeta, abstractmethod


class IChargeManager(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def getCharge(self, initialTimestamp, finalTimestamp):
        pass

    @abstractmethod
    def getBillableMinutes(self, initialTimestamp, finalTimestamp):
        pass

    @property
    def reducedTariffStart(self):
        return self.__reducedTariffStart

    @property
    def reducedTariffEnd(self):
        return self.__reducedTariffEnd

    @property
    def standingCharge(self):
        return self.__standingCharge

    @property
    def minuteCharge(self):
        return self.__minuteCharge

    @reducedTariffStart.setter
    def reducedTariffStart(self, value):
        if value not in range(0, 23):
            raise ValueError("Invalid hour.")
        self.__reducedTariffStart = value

    @reducedTariffEnd.setter
    def reducedTariffEnd(self, value):
        if value not in range(0, 23):
            raise ValueError("Invalid hour.")
        self.__reducedTariffEnd = value

    @standingCharge.setter
    def standingCharge(self, value):
        # Could not figure how to check for type with an or
        if (type(value) is not float):
            if (type(value) is not int):
                raise ValueError(
                    "standingCharge type must be an integer or a float.")
        self.__standingCharge = value

    @minuteCharge.setter
    def minuteCharge(self, value):
        # Could not figure how to check for type with an or
        if (type(value) is not float):
            if (type(value) is not int):
                raise ValueError(
                    "minuteCharge type must be an integer or a float.")
        self.__minuteCharge = value

        '''
        getCharge uses only timestamps, as per the YAGNI principle
        '''


class ChargeManager(IChargeManager):

    '''
    standingCharge and minuteCharge are self explanatory.
    reducedTariffStart and reducedTariffEnd are in GMT and can be either:
    a dictionary with {"tm_hour":hh, "tm_min":mm}, seconds can be ignored (removed as per YAGNI)
    two ints, as the hour. Minutes and seconds are ignored
    '''

    def __init__(self, standingCharge, minuteCharge, reducedTariffStart, reducedTariffEnd):
        self.standingCharge = standingCharge
        self.minuteCharge = minuteCharge
        if type(reducedTariffStart) is int and type(reducedTariffEnd) is int:
            self.reducedTariffStart = reducedTariffStart
            self.reducedTariffEnd = reducedTariffEnd
            '''
            elif type(reducedTariffStart) is dict and type(reducedTariffEnd) is dict:
                self.reducedTariffStart = reducedTariffStart["tm_hour"]
                self.reducedTariffStartMinute = reducedTariffStart["tm_min"]
                self.reducedTariffEnd = reducedTariffEnd["tm_hour"]
                self.reducedTariffEndMinute = reducedTariffEnd["tm_min"]
            '''
        else:
            raise TypeError(
                "reducedTariffStart and reducedTariffEnd must be both integer.")

    def reducedTariff(gmt):
        # The first part is inclusive because it will use the remainder of the hour,
        # the second part is exclusive to stop at the end of the previous hour
        # ["tm_hour"] is the same as [3]
        return True if (gmt[3] >= self.reducedTariffStart or gmt[3] < self.reducedTariffEnd) else False

    def truncate2Digits(x):
        return int(x * 100) / 100

    def getBillableMinutes(self, initialTimeTuple, finalTimeTuple):
        billableMinutes = 0

        '''
        Index	Attributes	Values
        0	tm_year	2008
        1	tm_mon	1 to 12
        2	tm_mday	1 to 31
        3	tm_hour	0 to 23
        4	tm_min	0 to 59
        5	tm_sec	0 to 61 (60 or 61 are leap-seconds)
        6	tm_wday	0 to 6 (0 is Monday)
        7	tm_yday	1 to 366 (Julian day)
        8	tm_isdst	-1, 0, 1, -1 means library determines DST
        '''

        if finalTimeTuple[1] != initialTimeTuple[1]:
            pass
        elif finalTimeTuple[2] != initialTimeTuple[2]:
            # complex logic
            pass
        elif finalTimeTuple[3] != initialTimeTuple[3]:
            # complex logic
            pass

        return billableMinutes

    def getCharge(self, initialTimestamp, finalTimestamp):
        # gmtime was chosen for system independence
        billableMinutes = self.getBillableMinutes(
            time.gmtime(initialTimestamp),
            time.gmtime(finalTimestamp))
        return self.standingCharge + billableMinutes * self.minuteCharge


test = ChargeManager(0.36, 0.09, 20, 6)
print(test.getCharge(time.time(), time.time() + 80))

localtime = time.gmtime(time.time())
localtime.tm_year = 2010
print("Local current time :", localtime.tm_year)
