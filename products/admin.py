from django.contrib import admin

from .models import (Basket, Product, ProductCategory, ProductSize,
                     ProductSizeMapping, Review)

# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(Review)
admin.site.register(ProductSize)


class ProductSizeMappingInline(admin.TabularInline):
    model = ProductSizeMapping


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'quantity']
    fields = ['name', 'description', ('price', 'quantity'), 'image',
              'category', 'slug', 'stripe_product_price_id']
    readonly_fields = ['description']
    search_fields = ['name']
    ordering = ['name']
    inlines = [ProductSizeMappingInline]


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ['product', 'quantity']
    extra = 0


admin.site.register(ProductSizeMapping)
