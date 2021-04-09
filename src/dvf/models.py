from django.db import models

class ValeursFoncieres(models.Model):
    """
    Données provenant du fichier DVF:
    https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/
    """
    id_mutation = models.CharField(max_length=255, null=True)
    date_mutation = models.DateField(null=True)
    numero_disposition = models.IntegerField(null=True)
    nature_mutation = models.CharField(max_length=255, null=True)
    valeur_fonciere = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    adresse_numero = models.IntegerField(null=True)
    adresse_suffixe = models.CharField(max_length=255, null=True)
    adresse_nom_voie = models.CharField(max_length=255, null=True)
    adresse_code_voie = models.CharField(max_length=255, null=True)
    code_postal = models.CharField(max_length=255, null=True)
    code_commune = models.CharField(max_length=255, null=True)
    nom_commune = models.CharField(max_length=255, null=True)
    code_departement = models.CharField(max_length=255, null=True)
    ancien_code_commune = models.CharField(max_length=255, null=True)
    ancien_nom_commune = models.CharField(max_length=255, null=True)
    id_parcelle = models.CharField(max_length=255, null=True)
    ancien_id_parcelle = models.CharField(max_length=255, null=True)
    numero_volume = models.CharField(max_length=255, null=True)
    lot1_numero = models.CharField(max_length=255, null=True)
    lot1_surface_carrez = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    lot2_numero = models.CharField(max_length=255, null=True)
    lot2_surface_carrez = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    lot3_numero = models.CharField(max_length=255, null=True)
    lot3_surface_carrez = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    lot4_numero = models.CharField(max_length=255, null=True)
    lot4_surface_carrez = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    lot5_numero = models.CharField(max_length=255, null=True)
    lot5_surface_carrez = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    nombre_lots = models.IntegerField(null=True)
    code_type_local = models.CharField(max_length=255, null=True)
    type_local = models.CharField(max_length=255, null=True)
    surface_reelle_bati = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    nombre_pieces_principales = models.IntegerField(null=True)
    code_nature_culture = models.CharField(max_length=255, null=True)
    nature_culture = models.CharField(max_length=255, null=True)
    code_nature_culture_speciale = models.CharField(max_length=255, null=True)
    nature_culture_speciale = models.CharField(max_length=255, null=True)
    surface_terrain = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    section_prefixe = models.CharField(max_length=5, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['date_mutation','code_commune','type_local'])
        ]
