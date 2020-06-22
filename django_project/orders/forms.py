from django import forms

from .models import OrderedBeer, Order


class OrderedBeerForm(forms.ModelForm):
    class Meta:
        model = OrderedBeer
        fields = ['beer', 'amount']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(OrderedBeerForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        # 1. get or create order for user
        obj, created = Order.objects.get_or_create(user=self.user)
        # 2. create orderedbeer
        ordered_beer = OrderedBeer.objects.create(
            order=obj,
            beer=self.cleaned_data['beer'],
            amount=self.cleaned_data['amount']
        )
        return ordered_beer
