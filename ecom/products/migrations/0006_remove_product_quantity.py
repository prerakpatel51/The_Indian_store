# Generated by Django 4.2.3 on 2024-06-18 03:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
    ]