# Generated by Django 4.2.3 on 2023-08-01 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_alter_productsize_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
        migrations.AddField(
            model_name='productsize',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
