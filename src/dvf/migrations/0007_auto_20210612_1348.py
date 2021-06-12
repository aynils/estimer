# Generated by Django 3.1.7 on 2021-06-12 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dvf", "0006_auto_20210503_1648"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="valeursfoncieres",
            name="dvf_valeurs_date_mu_c781de_idx",
        ),
        migrations.AddIndex(
            model_name="valeursfoncieres",
            index=models.Index(
                fields=[
                    "date_mutation",
                    "code_commune",
                    "type_local",
                    "longitude",
                    "latitude",
                ],
                name="dvf_valeurs_date_mu_d6c4a7_idx",
            ),
        ),
    ]
