# Database

## Call

The call table contains each call data, the only required fields are the necessary ones to start a call. It is intended to be updated when the call ends.

```python
class Call(models.Model):
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(null=True)
    source = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    call_id = models.BigIntegerField(primary_key=True, unique=True)
    call_price = models.FloatField(null=True)
```

## Charge

The charge table contains the pricing history of calls calculated by the server.

It was opted to store historic data so older calls can be verified in case of any error.

The charge manager class has it's own documentation [here](Docs/chargeManager.py.md).

```python
class Charge(models.Model):
    standing_charge = models.FloatField()
    minute_charge = models.FloatField()
    reduced_tariff_start = models.DecimalField(max_digits=2, decimal_places=0)
    reduced_tariff_end = models.DecimalField(max_digits=2, decimal_places=0)
    enforced = models.DateTimeField(default=timezone.now)
```
