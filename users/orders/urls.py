from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('create-order/', views.CreateOrderView.as_view(), name='create-order'),
    path('', views.OrderListView.as_view(), name='view-all-orders'),
    path('order/<int:pk>', views.OrderDetailedView.as_view(), name='order-info'),
    path('order-success/', views.SuccessOrderView.as_view(), name='success-order'),
    path('order-canceled/', views.CanceledOrderView.as_view(), name='canceled-order')
]
