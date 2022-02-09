from typing import List


from src.dvf.models import Commune
from src.population.models import PopulationStat


def get_cities_not_owned_by_agencies() -> List[Commune]:
    return Commune.objects.all().filter(agency_id__isnull=True).values("code_postal", "nom_commune", "code_commune")


def get_pricing_for_cities():
    cities = get_cities_not_owned_by_agencies()
    population = PopulationStat.objects.all().values("code_commune", "total_population")
    cities_with_population = []
    for city in cities:
        for populate in population:
            if city.get("code_commune") == populate.get("code_commune"):
                city_with_population = {
                    "code_commune": city.get("code_commune"),
                    "nom_commune": city.get("nom_commune"),
                    "total_population": populate.get("total_population"),
                }
                cities_with_population.append(city_with_population)
                break
    return cities_with_population
