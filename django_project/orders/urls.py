from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('order_beer/', views.OrderedBeerView.as_view(), name='order-beer'),
    path('shopping_cart/', views.ShoppingCartView.as_view(), name='shopping-cart'),
    path('<int:pk>/delete', views.OrderedBeerDeleteView.as_view(), name='delete'),
    path('confirm_order/', views.ConfirmOrderView.as_view(), name='confirm-order'),
    path('change_order_status/', views.ChangeOrderStatus.as_view(), name='change-order-status'),
    path('proceed_payment/<int:pk>/', views.ProceedPaymentView.as_view(), name='proceed-payment'),
    path('paying_order/', views.PayingOrderDetailView.as_view(), name='order-detail')
]

