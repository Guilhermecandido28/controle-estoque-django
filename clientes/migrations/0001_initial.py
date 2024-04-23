# Generated by Django 5.0.3 on 2024-04-02 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=250)),
                ('telefone', models.CharField(default='Não Possui', max_length=15)),
                ('email', models.EmailField(default='Não Possui', max_length=50)),
                ('instagram', models.CharField(default='Não Possui', max_length=50)),
            ],
        ),
    ]