from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, DeleteView
from django.views.generic.base import View, TemplateView

from getpaid.forms import PaymentMethodForm

from orders.forms import OrderedBeerForm
from orders.models import Order, PayingOrder, OrderedBeer


class OrderedBeerView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = OrderedBeerForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy(
        'orders:shopping-cart'
    )
    success_message = 'Your order has been updated.'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        order = Order.objects.filter(user=self.request.user).first()
        if not order:
            order = Order.objects.create(user=self.request.user)
        ctx['order_status'] = self.request.user.order.status
        return ctx

    def get_form_kwargs(self):
        kwargs = super(OrderedBeerView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ChangeOrderStatus(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user)
        except Exception as e:
            return render(request, 'orders/error.html', {'error': 'Something went wrong... Please try again.({})'.format(e)})
        order.status = 'ED'
        order.save(update_fields=['status'])
        return redirect('orders:order-beer')


class ShoppingCartView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/shopping_cart.html'

    def get_object(self, queryset=None):
        return Order.objects.filter(user=self.request.user).first()


class RemoveOrderedBeerView(LoginRequiredMixin, DeleteView):
    model = OrderedBeer
    template_name = 'orders/shopping_cart.html'
    success_url = reverse_lazy('orders:shopping-cart')

    def get_object(self, **kwargs):
        return OrderedBeer.objects.filter(order_id=self.kwargs.get("id")).last()


class ConfirmOrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user)
        except Exception as e:
            return render(request, 'orders/error.html', {'error': 'Something went wrong... Please try again.({})'.format(e)})
        payment_order = order.process_order()
        return redirect('orders:proceed-payment', payment_order.id)


class ProceedPaymentView(LoginRequiredMixin, DetailView):
    model = PayingOrder
    template_name = 'orders/proceed_payment_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["payment_form"] = PaymentMethodForm(
            initial={"order": self.object, "currency": self.object.currency}
        )
        return context


class PayingOrderDetailView(LoginRequiredMixin, TemplateView):
    model = PayingOrder
    template_name = 'orders/paying_order_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_order'] = PayingOrder.objects.all().last()
        return context
