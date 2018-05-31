import datetime
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
            #print("getBillableMinutes(", initialTime, ") + getBillableMinutes(", finalTime, ")\n")
            ################################################################
            # if the tariff pass from onde day to the next, (1) and (2) will complement each other and return only the billable minutes
            if self.reducedTariffEnd < self.reducedTariffStart:
                # I will start counting at the end of the reducedTariff (1)
                if(initialTime.hour < self.reducedTariffEnd):
                    _initialTime = initialTime.replace(hour=self.reducedTariffEnd, minute=0, second=0, microsecond=0)
                    return self.getBillableMinutes(_initialTime, finalTime)
                # it will end at midnight and the next day is treated in a different recursion
                elif(initialTime.hour >= self.reducedTariffStart):
                    return 0
                # It will stop counting at the start of the reducedTariff (2)
                elif(initialTime.hour >= self.reducedTariffEnd and finalTime.hour >= self.reducedTariffStart):
                    _finalTime = finalTime.replace(hour=self.reducedTariffStart, minute=0, second=0, microsecond=0) - datetime.timedelta(seconds=1)
                    return self.getBillableMinutes(initialTime, _finalTime)
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

    def getCharge(self, initialTime, finalTime):
        # A few typechecks
        if type(initialTime) != type(finalTime):
            raise TypeError("Types must match.")
        if type(initialTime) is float:
            initialTime = datetime.fromtimestamp(initialTime)
            finalTime = datetime.fromtimestamp(finalTime)
        if type(initialTime) is not datetime.datetime:
            raise TypeError("Types must be either datetime or float(timestamp).")

        billableMinutes = self.getBillableMinutes(initialTime, finalTime)
        charge = self.standingCharge + billableMinutes * self.minuteCharge
        return int(charge * 100) / 100


test = ChargeManager(0.36, 0.09, 22, 6)

localtime = datetime.datetime.now()
testtime = localtime.replace(month=6, day=2)
print("Local current time :", localtime, "test: ", testtime)
print(test.getCharge(localtime, testtime))
