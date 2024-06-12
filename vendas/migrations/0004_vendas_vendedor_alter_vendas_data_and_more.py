# Generated by Django 5.0.3 on 2024-05-23 18:37

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0003_alter_vendas_options'),
        ('vendedores', '0009_remove_vendedores_produtos_vendidos_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendas',
            name='vendedor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vendedores.vendedores'),
        ),
        migrations.AlterField(
            model_name='vendas',
            name='data',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='vendas',
            name='forma_pagamento',
            field=models.CharField(choices=[('CREDITO', 'Cartão de Crédito'), ('DEBITO', 'Cartão de Débito'), ('DINHEIRO', 'Dinheiro'), ('PIX', 'PIX')], max_length=50),
        ),
    ]