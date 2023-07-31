from django.contrib import admin

from .models import (Basket, Product, ProductCategory, ProductFile,
                     ProductSize, ProductSizeMapping, Review)

# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(Review)
admin.site.register(ProductSize)


class ProductSizeMappingInline(admin.TabularInline):
    model = ProductSizeMapping


class ProductFileInline(admin.TabularInline):
    model = ProductFile


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductFileInline,
        ProductSizeMappingInline
    ]
    list_display = ['name', 'price', 'quantity', 'quantity']
    fields = ['name', 'description', ('price', 'quantity'),
              'category', 'slug', 'stripe_product_price_id']
    readonly_fields = ['description']
    search_fields = ['name']
    ordering = ['name']


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ['product', 'quantity']
    extra = 0


admin.site.register(ProductSizeMapping)
admin.site.register(Product, ProductAdmin)
