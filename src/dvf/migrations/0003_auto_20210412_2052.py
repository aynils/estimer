# Generated by Django 3.1.7 on 2021-04-12 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dvf", "0002_auto_20210409_1221"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="valeursfoncieres",
            index=models.Index(
                fields=["date_mutation"], name="dvf_valeurs_date_mu_a05127_idx"
            ),
        ),
    ]
