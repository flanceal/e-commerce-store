# Generated by Django 4.2.3 on 2023-07-31 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_alter_productfile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, default=None, max_length=255, null=True, unique=True),
        ),
    ]
