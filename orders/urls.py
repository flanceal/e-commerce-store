from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('create-order/', views.CreateOrderView.as_view(), name='create-order'),
    path('all-orders/', views.OrderListView.as_view(), name='view-all-orders'),
    path('order/<int:order_id>', views.OrderView.as_view(), name='order-info'),
    path('success/', views.SuccessOrderView.as_view(), name='success-order'),
    path('canceled/', views.CanceledOrderView.as_view(), name='canceled-order')
]
