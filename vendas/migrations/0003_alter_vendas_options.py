# Generated by Django 5.0.3 on 2024-05-14 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0002_remove_caixa_saldo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vendas',
            options={'verbose_name': 'Venda', 'verbose_name_plural': 'Vendas'},
        ),
    ]