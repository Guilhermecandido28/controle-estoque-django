# Generated by Django 5.0.3 on 2024-07-03 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_rename_messagem_notification_mensagem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'verbose_name': 'Notificação', 'verbose_name_plural': 'Notificações'},
        ),
        migrations.AlterField(
            model_name='notification',
            name='data_criacao',
            field=models.DateTimeField(),
        ),
    ]
