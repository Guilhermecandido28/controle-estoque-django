# Generated by Django 5.0.3 on 2024-06-18 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0006_alter_tarefas_inicio_alter_tarefas_prazo'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarefas',
            name='cor',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='tarefas',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
