from django import forms
from .models import Beer


class AddBeerForm(forms.ModelForm):

    class Meta:
        model = Beer
        fields = [
            'product_name',
            'description',
            'price',
            'alcohol',
            'image',
        ]