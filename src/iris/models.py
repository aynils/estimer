from django.contrib.gis.db import models


class IRIS(models.Model):
    """
    Données provenant du fichier IRIS:
    https://geoservices.ign.fr/contoursiris
    """

    insee_commune = models.CharField(max_length=255, null=True)
    nom_commune = models.CharField(max_length=255, null=True)
    iris = models.CharField(max_length=255, null=True)
    code_iris = models.CharField(max_length=255, null=True)
    nom_iris = models.CharField(max_length=255, null=True)
    type_iris = models.CharField(max_length=1, null=True)
    geometry = models.MultiPolygonField(srid=2154, null=True)
    geometry_4326 = models.MultiPolygonField(srid=4326, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["insee_commune"]),
        ]
