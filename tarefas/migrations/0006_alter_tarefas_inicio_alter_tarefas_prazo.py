# Generated by Django 5.0.3 on 2024-06-13 14:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0005_alter_tarefas_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarefas',
            name='inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='tarefas',
            name='prazo',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]