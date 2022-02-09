from typing import List

from src.dvf.models import Commune


def get_cities_not_owned_by_agencies() -> List[Commune]:
    return Commune.objects.all().filter(agency_id__isnull=True).values("code_postal", "nom_commune", "code_commune")
