from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse

from common.view import TitleMixin

from .models import Basket, Product, ProductCategory, Review
from .forms import ReviewForm


# Create your views here.
class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - Catalog'

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        if category_id:
            return queryset.filter(category_id=category_id)
        else:
            return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


class ProductView(TitleMixin, FormView):
    template_name = "products/one_product.html"
    form_class = ReviewForm
    success_url = reverse_lazy('products:product-info')

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data()
        slug = self.kwargs.get('product_slug')
        context['product'] = Product.objects.get(slug=slug)
        context['reviews'] = Review.objects.filter(product=context['product'])
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        product = context['product']

        review = Review(
            product=product,
            review=form.cleaned_data['review'],
            users=self.request.user
        )
        review.save()
        return HttpResponseRedirect(reverse('products:product-info', args=[product.slug]))


@login_required(login_url='users:login')
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url='users:login')
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
