# Generated by Django 3.1.7 on 2021-06-12 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dvf", "0007_auto_20210612_1348"),
    ]

    operations = [
        migrations.AlterField(
            model_name="valeursfoncieres",
            name="latitude",
            field=models.DecimalField(decimal_places=15, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name="valeursfoncieres",
            name="longitude",
            field=models.DecimalField(decimal_places=15, max_digits=20, null=True),
        ),
    ]
