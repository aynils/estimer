# Generated by Django 3.1.7 on 2022-02-03 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dvf', '0009_auto_20211124_1912'),
    ]

    operations = [
        migrations.CreateModel(
            name='MutationIris',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_mutation', models.CharField(max_length=255)),
                ('code_iris', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddIndex(
            model_name='mutationiris',
            index=models.Index(fields=['id_mutation'], name='dvf_mutatio_id_muta_8487de_idx'),
        ),
        migrations.AddIndex(
            model_name='mutationiris',
            index=models.Index(fields=['code_iris'], name='dvf_mutatio_code_ir_89f8d4_idx'),
        ),
    ]
