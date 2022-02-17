# Generated by Django 3.1.7 on 2022-02-17 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("iris", "0004_auto_20211027_1508"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="iris",
            index=models.Index(fields=["insee_commune"], name="iris_iris_insee_c_a0f662_idx"),
        ),
    ]