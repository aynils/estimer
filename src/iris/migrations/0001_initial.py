# Generated by Django 3.1.7 on 2021-10-27 14:23

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="IRIS",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("insee_commune", models.CharField(max_length=255, null=True)),
                ("nom_commune", models.CharField(max_length=255, null=True)),
                ("iris", models.IntegerField(null=True)),
                ("code_iris", models.IntegerField(null=True)),
                ("nom_iris", models.CharField(max_length=255, null=True)),
                ("type_iris", models.CharField(max_length=1, null=True)),
                ("geometry", django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            ],
        )
    ]