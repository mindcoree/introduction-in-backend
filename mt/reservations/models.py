from django.core.exceptions import ValidationError
# Create your models here.
from django.db import models
from customers.models import Customer
from tables.models import Table


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("canceled", "Canceled"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        if Reservation.objects.filter(table=self.table, date=self.date).exclude(id=self.id).exists():
            raise ValidationError(f"Cтолик {self.table.number} уже забронирован на {self.date}")

        if Reservation.objects.filter(customer=self.customer, date=self.date).exclude(id=self.id).exists():
            raise ValidationError(f"Клиент  {self.customer.name} Уже есть бронирование на {self.date}")


    def __str__(self):
        return f"Бронь {self.id} - {self.get_status_display()}"


