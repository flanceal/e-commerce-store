from django.shortcuts import render
from .models import Product, ProductCategory


# Create your views here.
def index(request):
    return render(request, 'products/index.html')


def products(request):
    products_list = Product.objects.all()
    categories = ProductCategory.objects.all()
    return render(request, 'products/products.html', {
        'categories': categories,
        'products': products_list
    })
