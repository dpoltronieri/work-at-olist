from django.db import models
from django.utils import timezone

# IDEA: There is no verification of more than a call being made by the same
# number at the same time


class Call(models.Model):
    # Explicit id
    id = models.AutoField(primary_key=True)
    # This default timezone seems like a good idea
    # IDEA: Put this in the documentation as a feature
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(null=True)
    #duration = models.DurationField(null=True)
    source = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    call_id = models.BigIntegerField(null=False, unique=True)

    def __str__(self):
        return "id: {},call_id: {},start: {},end: {},source: {},destination: {}".format(
            self.id,
            self.call_id,
            self.start,
            self.end,
            self.source,
            self.destination)
