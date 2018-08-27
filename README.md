# Welcome

This is the **Work at Olist Challenge** wiki implemented by **Daniel Pereira Poltronieri**. It is the documentation and execution manual for the **Python Django** server and the database that accompanies it.

## About

This software uses the **Django** API and the **Django REST Framework** to implement the server.

## Database

The database used was the default Django Models.

### Call

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

The charge table contains the pricing history of calls calculated by the server.

It was opted to store historic data so older calls can be verified in case of any error.

```python
class Charge(models.Model):
    standing_charge = models.FloatField()
    minute_charge = models.FloatField()
    reduced_tariff_start = models.DecimalField(max_digits=2, decimal_places=0)
    reduced_tariff_end = models.DecimalField(max_digits=2, decimal_places=0)
    enforced = models.DateTimeField(default=timezone.now)
```

## Development

The development ambient was an *Ubuntu Linux* installation with the *Atom* text editor.
All the tests are handled by the Django Unit Test Module, no test was done with selenium or other front end testing tool.

## Deployment


## Usage

### Call start fields

### Call end fields

### Last period bill fields

### Selected period bill fields
