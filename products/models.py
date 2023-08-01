import stripe
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from users.models import User

from .constants import ALL_SIZES

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your models here.
class ProductSize(models.Model):
    name = models.CharField(max_length=10, choices=ALL_SIZES)

    def __str__(self):
        return self.name


class ProductSizeMapping(models.Model):
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.name} - {self.size.name}'


class ProductFile(models.Model):
    image = models.FileField(upload_to="product_images")
    product = models.ForeignKey('Product', on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    stripe_product_price_id = models.CharField(max_length=128, blank=True, null=True)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    sizes = models.ManyToManyField(to=ProductSize, through=ProductSizeMapping, blank=True)

    slug = models.SlugField(max_length=255, unique=True, default=None, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.stripe_product_price_id:
            self.stripe_product_price_id = self.create_stripe_product_price()['id']
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_url(self):
        return reverse("products:product-info", kwargs={"product_slug": self.slug})

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            currency='usd',
            product=stripe_product['id'],
            unit_amount=round(self.price * 100))
        self.stripe_product_price_id = stripe_product_price['id']
        self.save()
        return stripe_product_price

    def get_size(self):
        return ",".join([size for size in self.sizes.all()])

    def images(self):
        return ProductFile.objects.filter(product=self)


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def is_empty(self):
        return not Product.objects.filter(category=self)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class BasketsQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    size = models.CharField(max_length=10, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    objects = BasketsQuerySet.as_manager()

    def __str__(self):
        return f"Basket for {self.user.username} | Product: {self.product.name}"

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.product.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum())
        }
        return basket_item


class Review(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, default='Anonymous')
    review = models.CharField(max_length=300)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review about {self.product.name} from {self.username}"
