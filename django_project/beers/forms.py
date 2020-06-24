from django import forms
from django.contrib.auth.models import User

from .models import Beer, Review


class AddBeerForm(forms.ModelForm):
    product_name = forms.CharField(label='')
    description = forms.CharField(label='')
    price = forms.DecimalField(label='')
    alcohol = forms.DecimalField(label='')

    def __init__(self, *args, **kwargs):
        super(AddBeerForm, self).__init__(*args, **kwargs)
        print(self.fields['image'])
        self.fields['product_name'].widget.attrs['placeholder'] = 'Product Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Description'
        self.fields['price'].widget.attrs['placeholder'] = 'Price'
        self.fields['alcohol'].widget.attrs['placeholder'] = 'Alcohol'

    class Meta:
        model = Beer
        fields = [
            'product_name',
            'description',
            'price',
            'alcohol',
            'image',
        ]


class ReviewForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        required=False,
        widget=forms.HiddenInput(),
        queryset=User.objects.all()
    )
    beer = forms.ModelChoiceField(
        required=False,
        widget=forms.HiddenInput(),
        queryset=Beer.objects.all()
    )

    class Meta:
        model = Review
        fields = [
            'content',
            'user',
            'beer',
            'rating',
        ]
