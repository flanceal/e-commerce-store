from django.contrib import admin
from .models import ProductCategory, Product
from users.models import User


# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(User)
