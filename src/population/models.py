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
    total_population = models.CharField(max_length=255, null=True)
    population_0_2 = models.CharField(max_length=255, null=True)
    population_3_5 = models.CharField(max_length=255, null=True)
    population_6_10 = models.CharField(max_length=255, null=True)
    population_11_17 = models.CharField(max_length=255, null=True)
    population_18_24 = models.CharField(max_length=255, null=True)
    population_25_39 = models.CharField(max_length=255, null=True)
    population_40_54 = models.CharField(max_length=255, null=True)
    population_55_64 = models.CharField(max_length=255, null=True)
    population_65_79 = models.CharField(max_length=255, null=True)
    population_80_more = models.CharField(max_length=255, null=True)
    population_0_14 = models.CharField(max_length=255, null=True)
    population_15_29 = models.CharField(max_length=255, null=True)
    population_30_44 = models.CharField(max_length=255, null=True)
    population_45_59 = models.CharField(max_length=255, null=True)
    population_60_74 = models.CharField(max_length=255, null=True)
    population_75_more = models.CharField(max_length=255, null=True)
    population_0_19 = models.CharField(max_length=255, null=True)
    population_20_64 = models.CharField(max_length=255, null=True)
    population_65_more = models.CharField(max_length=255, null=True)
