# Generated by Django 4.2.6 on 2023-10-19 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_remove_payment_payment_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentreminder',
            name='payment_id',
        ),
    ]
