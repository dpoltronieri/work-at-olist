import time
from abc import ABCMeta, abstractmethod


class IChargeManager(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def getCharge(self, dictData):
        pass


class ChargeManager(IChargeManager):

    '''
    standingCharge and minuteCharge are self explanatory.
    reducedTariffStart and reducedTariffEnd are in GMT and can be either:
    a dictionary with {"tm_hour":hh, "tm_min":mm}, seconds can be ignored (removed as per YAGNI)
    two ints, as the hour. Minutes and seconds are ignored
    '''

    def __init__(self, standingCharge, minuteCharge, reducedTariffStart, reducedTariffEnd):
        self.__standingCharge = standingCharge
        self.__minuteCharge = minuteCharge
        if type(reducedTariffStart) is int and type(reducedTariffEnd) is int:
            self.__reducedTariffStart = reducedTariffStart
            self.__reducedTariffEnd = reducedTariffEnd
            '''
            elif type(reducedTariffStart) is dict and type(reducedTariffEnd) is dict:
                self.__reducedTariffStart = reducedTariffStart["tm_hour"]
                self.__reducedTariffStartMinute = reducedTariffStart["tm_min"]
                self.__reducedTariffEnd = reducedTariffEnd["tm_hour"]
                self.__reducedTariffEndMinute = reducedTariffEnd["tm_min"]
            '''
        else:
            raise Exception

        '''
        getCharge uses only timestamps, as per the YAGNI principle
        '''

    def getCharge(self, initialTimestamp, finalTimestamp):
        # gmtime was chosen for system independence
        initialTimeTuple = time.gmtime(initialTimestamp)
        finalTimeTuple = time.gmtime(finalTimestamp)

        def reducedTariff(gmt):
            # ["tm_hour"] is the same as [3]
            return True if (gmt[3] >= self.__reducedTariffStart or gmt[3] < self.__reducedTariffEnd) else False

        if not (reducedTariff(initialTimeTuple) or reducedTariff(finalTimeTuple)):
            print("normal call")
        else:
            print("Special call")


test = ChargeManager(0, 0, 23, 6)
test.getCharge(time.time(), time.time())

localtime = time.gmtime(time.time())
print("Local current time :", localtime)
