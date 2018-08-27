from datetime import timedelta, datetime

from billing.models import Charge
#from billing.serializers import ChargeSerializer


class ChargeManager():

    """
    This is a support class for DRYness of the code.
    It connects to the model Charge and uses the latest values to calculate a
    call price.
    """

    def formatTime(time):
        """
        Accepts a timestamp, a string or a datetime and parses it into a datetime.
        """
        if type(time) is float:
            time = datetime.datetime.fromtimestamp(time)
        if type(time) is int:
            time = datetime.datetime.fromtimestamp(float(time))
        if type(time) is str:
            time = dateutil.parser.parse(time)
        if type(time) is not datetime.datetime:
            raise TypeError(
                "Types must be either datetime ,float(timestamp) or an ISO string.")
        return time

    def getCharge(self, initialTime, finalTime):
        """

        """
        initialTime = ChargeManager.formatTime(initialTime)
        finalTime = ChargeManager.formatTime(finalTime)

        if(finalTime < initialTime):
            raise ValueError("finalTime has to come after initialTime")

        billableMinutes = self.getBillableMinutes(initialTime, finalTime)
        charge = (Charge.objects.latest('enforced')['standingCharge']
                  + Charge.objects.latest('enforced')['minuteCharge'] * billableMinutes)

        return int(charge * 100) / 100

    def getBillableMinutes(self, initialTime, finalTime):
        billableMinutes = 0

        if finalTime.month != initialTime.month:
            rightMiddleTime = finalTime.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0)
            _delta = finalTime - rightMiddleTime
            leftmiddleTime = finalTime - _delta - datetime.timedelta(seconds=1)
            return self.getBillableMinutes(initialTime, leftmiddleTime) + self.getBillableMinutes(rightMiddleTime, finalTime)
        elif finalTime.day != initialTime.day:
            rightMiddleTime = finalTime.replace(
                hour=0, minute=0, second=0, microsecond=0)
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
                    _initialTime = initialTime.replace(
                        hour=self.reducedTariffEnd, minute=0, second=0, microsecond=0)
                    return self.getBillableMinutes(_initialTime, finalTime)
                # It will stop counting at the start of the reducedTariff (2)
                elif(initialTime.hour >= self.reducedTariffEnd and finalTime.hour >= self.reducedTariffStart):
                    _finalTime = finalTime.replace(
                        hour=self.reducedTariffStart, minute=0, second=0, microsecond=0) - datetime.timedelta(seconds=1)
                    # the plus 1 is to compensate the timedelta
                    return self.getBillableMinutes(initialTime, _finalTime) + 1
            else:
                '''
                This is not yet implement do speed up the delivery process, it would mainly use the same logic as the above block.
                '''
                raise Exception("This is yet to be implemented")

        deltaSeconds = finalTime - initialTime
        billableMinutes = int(deltaSeconds.total_seconds() / 60)

        return billableMinutes
