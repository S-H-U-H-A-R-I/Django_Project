# Generated by Django 5.0.4 on 2024-04-27 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_customer_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
