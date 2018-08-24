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
    source = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)

    def __str__(self):
        return "Call between the numbers {}(source) and {}(destination).".format(self.source, self.destination)
