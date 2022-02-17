from typing import List

from django.db.models import Sum

from src.agencies.models import Pricing
from src.dvf.models import Commune
from src.population.models import PopulationStat


def get_cities_not_owned_by_agencies(code_departement: int) -> List[Commune]:
    cities = (
        Commune.objects.all()
        .filter(agency_id__isnull=True)
        .filter(code_departement=code_departement)
        .values("id", "code_postal", "nom_commune", "code_commune")
    )
    return cities


def add_population_to_cities(cities: List):
    code_communes = [city.get("code_commune") for city in cities]
    population = (
        PopulationStat.objects.filter(code_commune__in=code_communes)
        .values("code_commune", "total_population")
        .annotate(population=Sum("total_population"))
    )
    population = {city.get("code_commune"): city for city in population}
    cities_with_population = []
    for city in cities:
        code_commune = city.get("code_commune")
        city_population = population.get(code_commune, {}).get("population")
        city_with_population = {
            "id": city.get("id"),
            "code_postal": city.get("code_postal"),
            "nom_commune": city.get("nom_commune"),
            "total_population": city_population,
        }
        cities_with_population.append(city_with_population)

    return cities_with_population


def add_pricing_to_cities(cities: List):
    pricing = Pricing.objects.all().values("min_population", "max_population", "pricing")
    cities_with_pricing = []
    for city in cities:
        code_postal = city.get("code_postal")
        total_population = city.get("total_population")
        if total_population is not None:
            total_population = int(city.get("total_population"))
        else:
            total_population = 0
        for price in pricing:
            population_min = price.get("min_population")
            population_max = price.get("max_population")
            if total_population > 0:
                if total_population in range(population_min, population_max):
                    city_with_pricing = {
                        "id": city.get("id"),
                        "code_postal": code_postal,
                        "nom_commune": city.get("nom_commune"),
                        "pricing": price.get("pricing"),
                    }
                    cities_with_pricing.append(city_with_pricing)

    return cities_with_pricing


def get_cities_with_pricing(code_departement: int):
    cities = get_cities_not_owned_by_agencies(code_departement)
    cities = add_population_to_cities(cities)
    cities = add_pricing_to_cities(cities)

    return cities
