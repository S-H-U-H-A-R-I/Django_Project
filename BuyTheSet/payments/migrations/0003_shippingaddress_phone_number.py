# Generated by Django 5.0.4 on 2024-04-23 22:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_shippingaddress_address2'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='phone_number',
            field=models.CharField(default=0, max_length=255, validators=[django.core.validators.RegexValidator('^(?:\\+27\\d{9}|0\\d{9})$', message="Phone number must be entered in the format: '+27123456789' or '0123456789'.")]),
            preserve_default=False,
        ),
    ]