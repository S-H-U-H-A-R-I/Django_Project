# Generated by Django 5.0.4 on 2024-04-27 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_cartitem_cart_remove_cartitem_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='password',
        ),
    ]
