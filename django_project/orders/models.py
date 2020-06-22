from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from getpaid.models import AbstractOrder

from beers.models import Beer
from orders.errors import OrderError


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('ED', 'edit'),
        ('AO', 'awaiting order'),
        ('PS', 'payment success'),
        ('PF', 'payment failed'),
    )
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    status = models.CharField(
        choices=ORDER_STATUS_CHOICES,
        max_length=15,
        default='ED'
    )

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f'{self.user} - {self.status}'

    @property
    def calculate_order_payment(self):
        order_payment = []
        for ordered_beer in self.orderedbeer_set.all():
            order_payment.append(ordered_beer.beer.price * ordered_beer.amount)
        return int(sum(order_payment))

    def process_order(self):
        self.status = 'AO'
        self.save(update_fields=['status', ])
        order = Order.objects.get(user=self.user)
        new_payment = PayingOrder.objects.create(
            order=order,
            buyer=self.user,
            total=self.calculate_order_payment,
            currency='PLN'
        )
        return new_payment


class OrderedBeer(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE, null=True)
    amount = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'ordered beer'
        verbose_name_plural = 'ordered beers'

    def __str__(self):
        return '{} / {} / {}'.format(self.order, self.beer, self.amount)

    def save(self, **kwargs):
        if self.order and not self.order.status == 'ED':
            raise OrderError(
                "Can't save ordered beer related to not editable order; order id {}"
                .format(self.order.id)
            )
        super().save(**kwargs)


class PayingOrder(AbstractOrder):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.DecimalField(decimal_places=2, max_digits=8)
    currency = models.CharField(max_length=3, default='PLN')

    def get_buyer_info(self):
        return {"email": getattr(self.buyer, 'email', 'asdf@wp.pl')}

    def get_redirect_url(self, *args, success=None, **kwargs):
        # this method will be called to get the url that will be displayed
        # after returning from the paywall page and you can use `success` param
        # to differentiate the behavior in case the backend supports it.
        # By default it returns this:
        return self.get_absolute_url()

    def get_continue_url(self):
        return 'http://127.0.0.1:8000/orders/paying_order'

    def get_absolute_url(self):
        # This is a standard method recommended in Django documentation.
        # It should return an URL with order details. Here's an example:
        return reverse("orders:order-detail", kwargs={"pk": self.pk})

    # these are optional:
    def is_ready_for_payment(self):
        # Most of the validation will be handled by the form
        # but if you need any extra logic beyond that, you can write it here.
        # This is the default implementation:
        return True

    def get_total_amount(self):
        return int(self.order.calculate_order_payment)

    def get_items(self):
        # Some backends expect you to provide the list of items.
        # This is the default implementation:
        return [{
            "name": self.get_description(),
            "quantity": 1,
            "unit_price": int(self.get_total_amount()),
        }]

    def get_description(self):
        return 'Order description'

    def get_currency(self):
        return 'PLN'
