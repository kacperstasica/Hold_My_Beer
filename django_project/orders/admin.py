from django.contrib import admin

from orders.models import Order, OrderedBeer


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderedBeer)
class OrderedBeerModelAdmin(admin.ModelAdmin):
    pass
