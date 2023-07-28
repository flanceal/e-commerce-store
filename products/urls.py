from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products, name='all-products'),
    path('category/<int:category_id>', views.products_by_category, name='filtered_products'),
    path('<str:product_slug>/<str:product_size>', views.ProductView.as_view(), name='product-info'),
    path("baskets/add/<int:product_id>/<str:product_size>", views.basket_add, name="basket-add"),
    path("baskets/remove/<int:basket_id>/", views.basket_remove, name="basket-remove")
]
