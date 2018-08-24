from django.db import models
from django.utils import timezone

# IDEA: There is no verification of more than a call being made by the same
# number at the same time


class CallStart(models.Model):
    # Explicit id
    id = models.AutoField(primary_key=True)
    # This default timezone seems like a good idea
    # IDEA: Put this in the documentation as a feature
    timestamp = models.DateTimeField(default=timezone.now)
    source = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)

    def __str__(self):
        return "Call between the numbers {}(source) and {}(destination).".format(self.source, self.destination)


class CallEnd(models.Model):
    # Foreign PK, used to give constraints
    start = models.OneToOneField(
        CallStart,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # Check the above
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Start: {} Timestamp: {}".format(self.start, self.timestamp)


class CallBill(models.Model):
    call_start = models.OneToOneField(
        CallStart,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    call_end = models.OneToOneField(
        CallEnd,
        on_delete=models.CASCADE,
    )
    # Probably is unecessary
    #duration = models.DurationField()
    billable_duration = models.DurationField()
    price = models.FloatField()


"""
    I wrestled with a single table or a few related tables and database
    good pratices pointed me to multiple tables.
"""
