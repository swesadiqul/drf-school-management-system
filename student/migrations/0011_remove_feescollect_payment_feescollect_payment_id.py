# Generated by Django 4.2.6 on 2023-10-19 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_alter_payment_payment_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feescollect',
            name='payment',
        ),
        migrations.AddField(
            model_name='feescollect',
            name='payment_id',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True),
        ),
    ]