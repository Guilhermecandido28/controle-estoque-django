# Generated by Django 5.0.3 on 2024-04-02 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_alter_clientes_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='url_instagram',
            field=models.URLField(blank=True),
        ),
    ]
