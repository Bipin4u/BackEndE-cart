# Generated by Django 5.0.6 on 2024-11-18 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('e_cart', '0005_alter_review_username'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('username', 'item')},
        ),
    ]
