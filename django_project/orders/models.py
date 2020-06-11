from django.contrib.auth.models import User
from django.db import models

from beers.models import Beer


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('ED', 'edit'),
        ('AO', 'awaiting order'),
        ('PS', 'payment success'),
        ('PF', 'payment failed'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=15)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f'{self.user} - {self.status}'


class OrderedBeer(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'ordered beer'
        verbose_name_plural = 'ordered beers'

    def __str__(self):
        return f'{self.order} - {self.beer} - {self.amount}'
