import time
from abc import ABCMeta, abstractmethod


class IFinanceiro(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def callValue(self, dictData):
        pass


class Financeiro(IFinanceiro):

    def __init__(self, standingCharge, minuteCharge, reducedTariffStart, reducedTariffEnd):
        self.__standingCharge = standingCharge
        self.__minuteCharge = minuteCharge
        self.__reducedTariffStart = reducedTariffStart
        self.__reducedTariffEnd = reducedTariffEnd
