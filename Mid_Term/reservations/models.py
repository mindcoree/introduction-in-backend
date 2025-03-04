from django.db import models
from django.utils.translation import gettext_lazy as _
from customers.models import Customer
from tables.models import Table

class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        CONFIRMED = 'confirmed', _('Confirmed')
        CANCELED = 'canceled', _('Canceled')

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices)

    def __str__(self):
        return f'Reservation {self.id} for {self.customer}'