from django.db import models


class PopulationStat(models.Model):
    """
    Données provenant de l'insee :
    https://www.insee.fr/fr/statistiques/5650720#consulter
    """

    iris = models.CharField(max_length=255, null=True)
    code_commune = models.CharField(max_length=255, null=True)
    type_iris = models.CharField(max_length=1, null=True)
    modification_iris = models.CharField(max_length=1, null=True)
    label_iris = models.CharField(max_length=1, null=True)
    total_population = models.FloatField(max_length=255, null=True)
    population_0_2 = models.FloatField(max_length=255, null=True)
    population_3_5 = models.FloatField(max_length=255, null=True)
    population_6_10 = models.FloatField(max_length=255, null=True)
    population_11_17 = models.FloatField(max_length=255, null=True)
    population_18_24 = models.FloatField(max_length=255, null=True)
    population_25_39 = models.FloatField(max_length=255, null=True)
    population_40_54 = models.FloatField(max_length=255, null=True)
    population_55_64 = models.FloatField(max_length=255, null=True)
    population_65_79 = models.FloatField(max_length=255, null=True)
    population_80_more = models.FloatField(max_length=255, null=True)
    population_0_14 = models.FloatField(max_length=255, null=True)
    population_15_29 = models.FloatField(max_length=255, null=True)
    population_30_44 = models.FloatField(max_length=255, null=True)
    population_45_59 = models.FloatField(max_length=255, null=True)
    population_60_74 = models.FloatField(max_length=255, null=True)
    population_75_more = models.FloatField(max_length=255, null=True)
    population_0_19 = models.FloatField(max_length=255, null=True)
    population_20_64 = models.FloatField(max_length=255, null=True)
    population_65_more = models.FloatField(max_length=255, null=True)
