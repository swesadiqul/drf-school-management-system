# Generated by Django 4.2.6 on 2023-10-12 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='parent_email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
