from django.shortcuts import render
from django.views.generic import TemplateView

from orders.models import Order


class DetailOrderView(TemplateView):
    model = Order
    context_object_name = 'orders'
    template_name='orders/order_detail.html'



    def add_beer(self, beer, amount, update_quantity=False):
        '''
        add product to an order or update quantity
        '''


    # def remove_beer(self, beer):
    #     '''
    #     removes a product from the order
    #     '''
    #     beer_id = str(beer.pk)
    #     if beer_id in self.order:
    #         del self.order[beer_id]
    #         self.save()

    # def get_total_price(self):
    #     return sum(Decimal(beer['price']) * OrderedBeer.amount['amount'] for beer in self.order.values())