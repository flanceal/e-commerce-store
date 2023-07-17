from django.views.generic import TemplateView
from products.views import TitleMixin


# Create your views here.
class CreateOrderView(TitleMixin, TemplateView):
    title = 'Create order'
    template_name = 'orders/order-create.html'


class OrderView(TitleMixin, TemplateView):
    title = 'View order'
    template_name = 'orders/order.html'


class OrdersView(TitleMixin, TemplateView):
    title = 'View orders'
    template_name = 'orders/orders.html'


class SuccessOrderView(TitleMixin, TemplateView):
    title = 'Success order'
    template_name = 'orders/success.html'
