# Generated by Django 5.1 on 2024-08-21 15:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapp', '0012_alter_order_address_alter_order_delivery_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordReset_c',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_c', models.CharField(max_length=10)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapp.reg')),
            ],
        ),
    ]
