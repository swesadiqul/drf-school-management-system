# Generated by Django 4.2.6 on 2023-10-16 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='is_active',
        ),
    ]