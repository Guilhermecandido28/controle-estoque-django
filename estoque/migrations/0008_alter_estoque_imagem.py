# Generated by Django 5.0.3 on 2024-04-02 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0007_alter_estoque_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estoque',
            name='imagem',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
