# Generated by Django 4.2.6 on 2023-10-09 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0004_customuser_is_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_verified',
        ),
    ]