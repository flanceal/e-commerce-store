from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from users.models import User


# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, default=None, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_url(self):
        return reverse("products:product-info", kwargs={"product_slug": self.slug})


class BasketsQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    objects = BasketsQuerySet.as_manager()

    def __str__(self):
        return f"Basket for {self.user.username} | Product: {self.product.name}"

    def sum(self):
        return self.product.price * self.quantity


class Review(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, default='Anonymous')
    review = models.CharField(max_length=300)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review about {self.product.name} from {self.username}"
