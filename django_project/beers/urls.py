from django.urls import path

from .views import AddBeerView

app_name = 'beers'
urlpatterns = [
    path('add_beer/', AddBeerView.as_view(), name='add-beer'),
]
