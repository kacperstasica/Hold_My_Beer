from django.urls import path

from .views import DetailOrderView

app_name = 'orders'
urlpatterns = [
    path('order_detail/', DetailOrderView.as_view(), name='order-detail'),
]
