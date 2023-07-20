from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.shortcuts import redirect

from products.views import TitleMixin
from .forms import OrderForm

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessOrderView(TitleMixin, TemplateView):
    title = 'Success order'
    template_name = 'orders/success.html'


class CanceledOrderView(TitleMixin, TemplateView):
    title = 'Checkout canceled'
    template_name = 'products/cancel.html'


# Create your views here.
class CreateOrderView(TitleMixin, CreateView):
    title = 'Create order'
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:success-order')

    def post(self, request, *args, **kwargs):
        super(CreateOrderView, self).post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1NW0FDG0M7gTslJBZ9jvXPW1',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:success-order')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:canceled-order')),
        )
        return redirect(checkout_session.url, code=303)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(CreateOrderView, self).form_valid(form)


class OrderView(TitleMixin, TemplateView):
    title = 'View order'
    template_name = 'orders/order.html'


class OrdersView(TitleMixin, TemplateView):
    title = 'View orders'
    template_name = 'orders/orders.html'
