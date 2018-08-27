from django.db import models
from django.utils import timezone

# IDEA: There is no verification of more than a call being made by the same
# number at the same time


class Call(models.Model):
    # Explicit id
    #id = models.AutoField(primary_key=True, unique=True)
    # This default timezone seems like a good idea
    # IDEA: Put this in the documentation as a feature
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(null=True)
    #duration = models.DurationField(null=True)
    source = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    call_id = models.BigIntegerField(primary_key=True, unique=True)

    def __str__(self):
        return "call_id: {},start: {},end: {},source: {},destination: {}".format(
            self.call_id,
            self.start,
            self.end,
            self.source,
            self.destination)


class Charge(models.Model):
    standing_charge = models.FloatField()
    minute_charge = models.FloatField()
    reduced_tariff_start = models.DecimalField(max_digits=2, decimal_places=0)
    reduced_tariff_end = models.DecimalField(max_digits=2, decimal_places=0)
    enforced = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "standing_charge: {},minute_charge: {},reduced_tariff_start: {},reduced_tariff_end: {},enforced: {}".format(
            self.standing_charge,
            self.minute_charge,
            self.reduced_tariff_start,
            self.reduced_tariff_end,
            self.enforced
        )
