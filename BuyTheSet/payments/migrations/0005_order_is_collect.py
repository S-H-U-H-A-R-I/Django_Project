# Generated by Django 5.0.4 on 2024-04-29 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_collect',
            field=models.BooleanField(default=False),
        ),
    ]
