# Generated by Django 4.1.7 on 2023-04-25 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppPaginas', '0007_alter_pagina_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagina',
            name='subtitulo',
            field=models.CharField(max_length=200),
        ),
    ]
