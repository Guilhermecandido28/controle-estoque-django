# Generated by Django 5.0.3 on 2024-04-02 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0006_alter_estoque_marca'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estoque',
            name='imagem',
            field=models.BinaryField(null=True),
        ),
    ]
