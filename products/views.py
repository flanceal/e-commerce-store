from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages

from common.view import TitleMixin

from .forms import ReviewForm
from .models import Basket, Product, ProductCategory, Review


# Create your views here.
class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


def products(request):
    products = Product.objects.all()

    context = paginate_products(request, products)
    context['title'] = 'All products'
    return render(request, 'products/products.html', context)


def products_by_category(request, category_id):
    get_object_or_404(ProductCategory, id=category_id)

    products = Product.objects.filter(category_id=category_id)

    context = paginate_products(request, products)
    context['title'] = ProductCategory.objects.get(id=category_id)
    return render(request, 'products/products.html', context)


def paginate_products(request, products):
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    context = {
        'page_obj': page_obj,
        'categories': ProductCategory.objects.all()
    }
    return context


class ProductView(TitleMixin, FormView):
    template_name = "products/one_product.html"
    form_class = ReviewForm
    success_url = reverse_lazy('products:product-info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        slug = self.kwargs.get('product_slug')
        size = self.kwargs.get('product_size')
        context['product'] = Product.objects.get(slug=slug)
        context['reviews'] = Review.objects.filter(product=context['product']).order_by('-created_timestamp')
        context['product_size'] = size
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        product = context['product']

        review = Review(
            product=product,
            review=form.cleaned_data['review'],
            username=self.request.user.username
        )
        review.save()
        return HttpResponseRedirect(reverse('products:product-info', args=[product.slug, None]))

    def get_title(self):
        slug = self.kwargs.get('product_slug')
        product = Product.objects.get(slug=slug)
        return product.name


@login_required(login_url='users:login')
def basket_add(request, product_id, product_size):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product, size=product_size)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1, size=product_size)
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
