# Generated by Django 5.0.6 on 2024-11-19 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_cart', '0009_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
