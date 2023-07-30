# Generated by Django 4.2.3 on 2023-07-27 22:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_remove_product_size_product_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.CreateModel(
            name='ProductSizeMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productsize')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(blank=True, through='products.ProductSizeMapping', to='products.productsize'),
        ),
    ]
