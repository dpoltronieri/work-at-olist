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
        print("tipo do formattime: ", type(time))
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
            ################################################################
            #print("Month call:")
            #print("getBillableMinutes(", initialTime, leftmiddleTime, ") + getBillableMinutes(", rightMiddleTime, finalTime, ")\n")
            ################################################################
            return self.getBillableMinutes(initialTime, leftmiddleTime) + self.getBillableMinutes(rightMiddleTime, finalTime)
        elif finalTime.day != initialTime.day:
            rightMiddleTime = finalTime.replace(hour=0, minute=0, second=0, microsecond=0)
            _delta = finalTime - rightMiddleTime
            leftmiddleTime = finalTime - _delta - datetime.timedelta(seconds=1)
            ################################################################
            #print("Day call:")
            #print("getBillableMinutes(", initialTime, leftmiddleTime, ") + getBillableMinutes(", rightMiddleTime, finalTime, ")\n")
            ################################################################
            return self.getBillableMinutes(initialTime, leftmiddleTime) + self.getBillableMinutes(rightMiddleTime, finalTime)
        elif finalTime.day == initialTime.day:
            ################################################################
            #print("Same Day call:")
            #print("getBillableMinutes(", initialTime, finalTime, ")\n")
            ################################################################
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
        ################################################################
        #print("timdelta: ", deltaSeconds, "total minutes", int(deltaSeconds.total_seconds() / 60))
        ################################################################
        billableMinutes = int(deltaSeconds.total_seconds() / 60)

        return billableMinutes

    def getCharge_old(self, initialTime, finalTime):
        # A few typechecks
        if type(initialTime) != type(finalTime):
            raise TypeError("Types must match.")
        if type(initialTime) is float:
            initialTime = datetime.datetime.fromtimestamp(initialTime)
            finalTime = datetime.datetime.fromtimestamp(finalTime)
        if type(initialTime) is string:
            initialTime = dateutil.parser.parse(initialTime)
            finalTime = dateutil.parser.parse(finalTime)
        if type(initialTime) is not datetime.datetime:
            raise TypeError("Types must be either datetime or float(timestamp).")

        billableMinutes = self.getBillableMinutes(initialTime, finalTime)
        charge = self.standingCharge + billableMinutes * self.minuteCharge
        return int(charge * 100) / 100

    def getCharge(self, initialTime, finalTime):
        initialTime = ChargeManager.formatTime(initialTime)
        finalTime = ChargeManager.formatTime(finalTime)

        billableMinutes = self.getBillableMinutes(initialTime, finalTime)
        charge = self.standingCharge + billableMinutes * self.minuteCharge
        return int(charge * 100) / 100


'''
test = ChargeManager(0.36, 0.09, 22, 6)

#localtime = datetime.datetime.now()
#testtime = localtime.replace(month=6, day=2)
#print("Local current time :", localtime, "test: ", testtime)

localtime = '2016-02-29T12:00:00Z'
testtime = dateutil.parser.parse('2016-02-29T12:05:00Z')
print(test.getCharge(localtime, testtime))

#localtime2 = datetime.datetime(year=2018, month=2, day=5, hour=12, minute=0)
# print(localtime2)


print(dateutil.parser.parse('2016-02-29T12:00:00Z'))
'''

lastDay = calendar.monthrange(2018, 5)[1]
firstTime = datetime.datetime(year=2018, month=5, day=1)
lastTime = datetime.datetime(year=2018, month=5, day=lastDay) + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)

print("F: ", firstTime, "L: ", lastTime)
