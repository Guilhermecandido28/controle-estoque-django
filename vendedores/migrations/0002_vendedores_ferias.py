# Generated by Django 5.0.3 on 2024-05-14 12:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendedores', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendedores',
            name='ferias',
            field=models.DateField(default=datetime.datetime(2024, 5, 14, 9, 25, 20, 600774)),
        ),
    ]
