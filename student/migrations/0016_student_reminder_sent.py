# Generated by Django 4.2.6 on 2023-10-22 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0015_alter_payment_fees_master_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='reminder_sent',
            field=models.BooleanField(default=False),
        ),
    ]