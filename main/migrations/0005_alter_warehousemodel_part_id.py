# Generated by Django 4.1 on 2022-08-23 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_warehousemodel_part_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehousemodel',
            name='part_id',
            field=models.BigIntegerField(unique=True),
        ),
    ]