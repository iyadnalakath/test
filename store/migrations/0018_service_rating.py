# Generated by Django 4.1.5 on 2023-01-27 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_remove_service_ratingss'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
