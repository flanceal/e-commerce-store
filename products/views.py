from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.db.models import F
from django.core.cache import cache

from common.view import TitleMixin

from .forms import ReviewForm
from .models import Basket, Product, ProductCategory, Review, ProductSizeMapping, has_available_product_size


# Create your views here.
class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


def products(request):
    products = cache.get('products')
    if not products:
        products = Product.objects.all()
        cache.set('products', products, timeout=15)
    context = paginate_products(request, products)
    context['title'] = 'All products'
    return render(request, 'products/products.html', context)


def products_by_category(request, category_id):
    category = get_object_or_404(ProductCategory, id=category_id)

    products = cache.get(f'product_{category_id}')
    if not products:
        products = Product.objects.filter(category=category)
        cache.set(f"products_{category_id}", products, 15)

    context = paginate_products(request, products)
    context['title'] = ProductCategory.objects.get(id=category_id)
    return render(request, 'products/products.html', context)


def paginate_products(request, products):
    paginator = Paginator(products.select_related('category'), 6)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.get_page(page_number)
    except (EmptyPage, PageNotAnInteger):
        page_obj = paginator.get_page(1)
    context = {
        'page_obj': page_obj,
        'categories': set(category for category in ProductCategory.objects.filter(product__isnull=False))
    }
    return context


class ProductView(FormView):
    template_name = "products/one_product.html"
    form_class = ReviewForm
    success_url = reverse_lazy('products:product-info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        slug = self.kwargs.get('product_slug')
        size = self.kwargs.get('product_size')
        context['product'] = get_object_or_404(Product, slug=slug)
        context['reviews'] = Review.objects.filter(product=context['product']).order_by('-created_timestamp')
        context['product_size'] = size
        context['available_sizes'] = context['product'].available_sizes
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
        product = self.get_context_data()['product']
        return product.name


@login_required(login_url='users:login')
def basket_add(request, product_id, product_size):
    if product_size == 'None':
        messages.add_message(request, messages.ERROR, "Please, Choose size of Product")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    product = get_object_or_404(Product, id=product_id)

    if not has_available_product_size(product=product, size_name=product_size):
        messages.add_message(request, messages.ERROR, "The product with this size is not available")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    baskets = Basket.objects.filter(user=request.user, product=product, size=product_size)
    mapping = ProductSizeMapping.objects.get(product=product, size__name=product_size)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1, size=product_size)
    else:
        basket = baskets.first()
        basket.quantity = F('quantity') + 1
        basket.save()

    # decreasing product quantity by one
    mapping.quantity = F('quantity') - 1
    mapping.save()
    messages.add_message(request, messages.SUCCESS, f"{product.name} was added to the Cart")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url='users:login')
def basket_remove(request, basket_id):
    basket = get_object_or_404(Basket, id=basket_id)
    mapping = get_object_or_404(ProductSizeMapping, product=basket.product, size__name=basket.size)
    mapping.quantity = F('quantity') + basket.quantity
    mapping.save()
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
