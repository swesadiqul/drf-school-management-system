# Generated by Django 4.2.6 on 2023-10-16 04:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
        ('usermanager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='superadmin',
            name='business',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='business', to='business.business'),
        ),
    ]