import calendar
import datetime
from abc import ABCMeta, abstractmethod

import dateutil.parser

# https://dateutil.readthedocs.io/en/stable/parser.html


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


class ChargeManager(IChargeManager):

    '''
    standingCharge and minuteCharge are self explanatory.
    reducedTariffStart and reducedTariffEnd can be either:
    a dictionary with {"tm_hour":hh, "tm_min":mm}, seconds can be ignored (removed as per YAGNI)
    two ints, as the hour. Minutes and seconds are ignored
    '''

    def __init__(self, standingCharge, minuteCharge, reducedTariffStart, reducedTariffEnd):
        self.standingCharge = standingCharge
        self.minuteCharge = minuteCharge
        if type(reducedTariffStart) is int and type(reducedTariffEnd) is int:
            self.reducedTariffStart = reducedTariffStart
            self.reducedTariffEnd = reducedTariffEnd
        else:
            raise TypeError(
                "reducedTariffStart and reducedTariffEnd must be both integer.")

    def formatTime(time):
        if type(time) is float:
            time = datetime.datetime.fromtimestamp(time)
        if type(time) is int:
            time = datetime.datetime.fromtimestamp(float(time))
        if type(time) is str:
            time = dateutil.parser.parse(time)
        if type(time) is not datetime.datetime:
            raise TypeError("Types must be either datetime ,float(timestamp) or an ISO string.")
        return time

    def getBillableMinutes(self, initialTime, finalTime):
        billableMinutes = 0

        if finalTime.month != initialTime.month:
            rightMiddleTime = finalTime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            _delta = finalTime - rightMiddleTime
            leftmiddleTime = finalTime - _delta - datetime.timedelta(seconds=1)
            return self.getBillableMinutes(initialTime, leftmiddleTime) + self.getBillableMinutes(rightMiddleTime, finalTime)
        elif finalTime.day != initialTime.day:
            rightMiddleTime = finalTime.replace(hour=0, minute=0, second=0, microsecond=0)
            _delta = finalTime - rightMiddleTime
            leftmiddleTime = finalTime - _delta - datetime.timedelta(seconds=1)
            return self.getBillableMinutes(initialTime, leftmiddleTime) + self.getBillableMinutes(rightMiddleTime, finalTime)
        elif finalTime.day == initialTime.day:
            # if the tariff pass from onde day to the next, (1) and (2) will complement each other and return only the billable minutes
            if self.reducedTariffEnd < self.reducedTariffStart:
                # it started at midnight and the previous day is treated in a different recursion
                if(finalTime.hour < self.reducedTariffEnd):
                    return 0
                # it will end at midnight and the next day is treated in a different recursion
                elif(initialTime.hour >= self.reducedTariffStart):
                    return 0
                # I will start counting at the end of the reducedTariff (1)
                elif(initialTime.hour < self.reducedTariffEnd):
                    _initialTime = initialTime.replace(hour=self.reducedTariffEnd, minute=0, second=0, microsecond=0)
                    return self.getBillableMinutes(_initialTime, finalTime)
                # It will stop counting at the start of the reducedTariff (2)
                elif(initialTime.hour >= self.reducedTariffEnd and finalTime.hour >= self.reducedTariffStart):
                    _finalTime = finalTime.replace(hour=self.reducedTariffStart, minute=0, second=0, microsecond=0) - datetime.timedelta(seconds=1)
                    return self.getBillableMinutes(initialTime, _finalTime) + 1  # the plus 1 is to compensate the timedelta
            else:
                '''
                This is not yet implement do speed up the delivery process, it would mainly use the same logic as the above block.
                '''
                raise Exception("This is yet to be implemented")

        deltaSeconds = finalTime - initialTime
        billableMinutes = int(deltaSeconds.total_seconds() / 60)

        return billableMinutes

    def getCharge(self, initialTime, finalTime):
        initialTime = ChargeManager.formatTime(initialTime)
        finalTime = ChargeManager.formatTime(finalTime)

        if(finalTime < initialTime):
            raise ValueError("finalTime has to come after initialTime")

        billableMinutes = self.getBillableMinutes(initialTime, finalTime)
        charge = self.standingCharge + billableMinutes * self.minuteCharge
        return int(charge * 100) / 100
