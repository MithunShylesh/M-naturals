# Generated by Django 5.1 on 2024-08-17 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapp', '0003_remove_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
    ]
