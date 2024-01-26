import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.detail import DetailView
import logging

from products.models import Basket, BasketsQuerySet
from products.views import TitleMixin

from .forms import OrderForm
from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)

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
        baskets = Basket.objects.filter(user=self.request.user)
        line_items = BasketsQuerySet.stripe_products(baskets)
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='http://{}{}'.format(settings.DOMAIN_NAME, reverse('orders:success-order')),
            cancel_url='http://{}{}'.format(settings.DOMAIN_NAME, reverse('orders:canceled-order')),
        )
        return redirect(checkout_session.url, code=303)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(CreateOrderView, self).form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f'ValueError in stripe_webhook_view: {e}')
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f'SignatureVerificationError in stripe_webhook_view: {e}')
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = session.metadata.order_id
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
    print("Fulfilling order")


class OrderListView(TitleMixin, ListView):
    title = 'View orders'
    queryset = Order.objects.all()
    template_name = 'orders/orders.html'
    ordering = ('-time_created')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailedView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = f'Order #{self.object.id}'
        return context
