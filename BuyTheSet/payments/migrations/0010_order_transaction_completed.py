# Generated by Django 5.0.4 on 2024-05-08 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0009_order_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transaction_completed',
            field=models.BooleanField(default=False),
        ),
    ]
