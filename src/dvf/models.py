from django.db import models

from src.iris.models import IRIS


class ValeursFoncieres(models.Model):
    """
    Données provenant du fichier DVF:
    https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/
    """

    id_mutation = models.CharField(max_length=255, null=True)
    date_mutation = models.DateField(null=True)
    numero_disposition = models.IntegerField(null=True)
    nature_mutation = models.CharField(max_length=255, null=True)
    valeur_fonciere = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    adresse_numero = models.IntegerField(null=True)
    adresse_suffixe = models.CharField(max_length=255, null=True)
    adresse_nom_voie = models.CharField(max_length=255, null=True)
    adresse_code_voie = models.CharField(max_length=255, null=True)
    code_postal = models.CharField(max_length=255, null=True)
    code_commune = models.CharField(max_length=255, null=True)  # code INSEE
    nom_commune = models.CharField(max_length=255, null=True)
    code_departement = models.CharField(max_length=255, null=True)
    ancien_code_commune = models.CharField(max_length=255, null=True)
    ancien_nom_commune = models.CharField(max_length=255, null=True)
    id_parcelle = models.CharField(max_length=255, null=True)
    ancien_id_parcelle = models.CharField(max_length=255, null=True)
    numero_volume = models.CharField(max_length=255, null=True)
    lot1_numero = models.CharField(max_length=255, null=True)
    lot1_surface_carrez = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    lot2_numero = models.CharField(max_length=255, null=True)
    lot2_surface_carrez = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    lot3_numero = models.CharField(max_length=255, null=True)
    lot3_surface_carrez = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    lot4_numero = models.CharField(max_length=255, null=True)
    lot4_surface_carrez = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    lot5_numero = models.CharField(max_length=255, null=True)
    lot5_surface_carrez = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    nombre_lots = models.IntegerField(null=True)
    code_type_local = models.CharField(max_length=255, null=True)
    type_local = models.CharField(max_length=255, null=True)
    surface_reelle_bati = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    nombre_pieces_principales = models.IntegerField(null=True)
    code_nature_culture = models.CharField(max_length=255, null=True)
    nature_culture = models.CharField(max_length=255, null=True)
    code_nature_culture_speciale = models.CharField(max_length=255, null=True)
    nature_culture_speciale = models.CharField(max_length=255, null=True)
    surface_terrain = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=15, null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=15, null=True)
    section_prefixe = models.CharField(max_length=5, null=True)

    @property
    def code_iris(self):
        mutation_iris = MutationIris.objects.find(id_mutation=self.id_mutation).first()
        if mutation_iris:
            return mutation_iris.code_iris

    class Meta:
        indexes = [
            models.Index(fields=["code_commune", "type_local", "date_mutation", "longitude", "latitude"]),
            models.Index(fields=["date_mutation"]),
        ]


class Commune(models.Model):
    code_postal = models.CharField(max_length=255, null=True)
    code_commune = models.CharField(max_length=255, null=False, unique=True)
    nom_commune = models.CharField(max_length=255, null=True)
    code_departement = models.CharField(max_length=255, null=True)
    slug = models.CharField(max_length=255, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["code_postal"]),
            models.Index(fields=["code_commune"]),
            models.Index(fields=["nom_commune"]),
            models.Index(fields=["slug"]),
        ]

    def get_absolute_url(self):
        return f"/commune/{self.slug}"


class MutationIris(models.Model):
    id_mutation = models.CharField(max_length=255, null=False)
    code_iris = models.CharField(max_length=255, null=False)

    class Meta:
        indexes = [
            models.Index(fields=["id_mutation"]),
            models.Index(fields=["code_iris"]),
        ]
